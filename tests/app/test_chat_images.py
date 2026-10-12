"""이미지 첨부 연결: 서비스(상태 전달, 저장, 오류 문구)와 입력 값 나누기, 그래프의 multimodal 연결."""
import io
import os
from contextlib import contextmanager
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from langchain_core.messages import AIMessage
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("OPENAI_API_KEY", "test-key-not-real")

from src.app import chat_service  # noqa: E402
from src.app.chat import DEFAULT_IMAGE_TEXT, split_composer_value  # noqa: E402
from src.db import create_user, list_messages  # noqa: E402
from src.db.models import Base  # noqa: E402


def png(size=(40, 30), noisy=False):
    image = Image.new("RGB", size, (200, 30, 30))
    if noisy:
        image = Image.frombytes("RGB", size, os.urandom(size[0] * size[1] * 3))
    buffer = io.BytesIO()
    image.save(buffer, "PNG")
    return buffer.getvalue()


@pytest.fixture
def local_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)

    @contextmanager
    def scope():
        with factory() as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise

    import src.db
    monkeypatch.setattr(src.db, "db_session", scope)
    with scope() as session:
        uid = create_user(session, "imguser01", "test-pass-123").id
    yield scope, uid
    engine.dispose()


def fake_graph(monkeypatch, analysis="읽은 글"):
    graph = Mock()
    graph.invoke.return_value = {"messages": [AIMessage(content="답")], "answer": "답", "image_analysis": analysis}
    monkeypatch.setattr(chat_service, "get_graph", lambda: graph)
    return graph


def test_images_reach_state_and_analysis_comes_back(monkeypatch):
    graph = fake_graph(monkeypatch)
    data = png()
    result = chat_service.run_chat([{"role": "user", "content": "이거 봐줘"}], images=[data])
    assert graph.invoke.call_args.args[0]["image"] == [data]
    assert result["status"] == "success" and result["image_analysis"] == "읽은 글"


def test_no_images_keeps_old_behavior(monkeypatch):
    graph = fake_graph(monkeypatch, analysis="남은 값")
    result = chat_service.run_chat([{"role": "user", "content": "질문"}])
    assert graph.invoke.call_args.args[0]["image"] is None
    assert result["image_analysis"] is None


def test_too_many_or_wrong_format_gives_image_message():
    four = chat_service.run_chat([{"role": "user", "content": "q"}], images=[png()] * 4)
    assert four["error"]["code"] == "INVALID_IMAGE" and "3장" in four["error"]["message"]
    bad = chat_service.run_chat([{"role": "user", "content": "q"}], images=[b"not an image"])
    assert bad["error"]["code"] == "INVALID_IMAGE" and "형식" in bad["error"]["message"]


def test_oversized_image_is_shrunk(monkeypatch):
    big = png((1500, 1500), noisy=True)
    assert len(big) > 2_000_000
    out = chat_service.prepare_images([big])
    assert len(out) == 1 and len(out[0]) <= 2_000_000


def test_db_roundtrip_saves_images_and_analysis(local_db, monkeypatch):
    scope, uid = local_db
    graph = fake_graph(monkeypatch)
    result = chat_service.run_db_chat("스크린샷이에요", user_id=uid, images=[png(), png((20, 20))])
    assert result["status"] == "success"
    with scope() as session:
        rows = list_messages(session, result["conversation_id"], uid)
        user = rows[0]
        assert len(user.attachments) == 2 and all(a.thumb_data for a in user.attachments)
        assert user.image_analysis == "읽은 글"
    assert len(graph.invoke.call_args.args[0]["image"]) == 2


def test_image_only_question_uses_default_text(local_db, monkeypatch):
    scope, uid = local_db
    graph = fake_graph(monkeypatch)
    result = chat_service.run_db_chat("", user_id=uid, images=[png()])
    assert result["status"] == "success"
    assert graph.invoke.call_args.args[0]["messages"][-1]["content"] == chat_service.IMAGE_ONLY_QUESTION
    assert chat_service.run_db_chat("", user_id=uid)["error"]["code"] == "INVALID_INPUT"


def test_split_composer_value():
    assert split_composer_value(None) == ("", [], None)
    assert split_composer_value("글") == ("글", [], None)
    files = [SimpleNamespace(getvalue=lambda i=i: bytes([i])) for i in range(5)]
    text, images, notice = split_composer_value(SimpleNamespace(text="t", files=files))
    assert text == "t" and images == [bytes([i]) for i in range(3)] and "3장" in notice
    assert split_composer_value({"text": "", "files": files[:1]})[1] == [b"\x00"]
    assert DEFAULT_IMAGE_TEXT == chat_service.IMAGE_ONLY_QUESTION
