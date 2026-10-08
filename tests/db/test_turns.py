"""턴 기록 함수(record_user_turn, record_assistant_turn) 확인. 메모리 SQLite, 합성 이미지는 Pillow."""

import io
import secrets

import pytest

PIL = pytest.importorskip("PIL")
from PIL import Image  # noqa: E402

from src.db import (  # noqa: E402
    HistoryConfig,
    create_conversation,
    create_user,
    get_history_context,
    get_message,
    get_sources,
    init_db,
    list_images,
    list_messages,
    make_engine,
    make_session_factory,
    record_assistant_turn,
    record_user_turn,
    session_scope,
    update_profile,
)
from src.db.models import Conversation, Message, MessageAttachment  # noqa: E402


def png(size=(200, 120), color=(30, 120, 200)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", size, color).save(buf, "PNG")
    return buf.getvalue()


@pytest.fixture()
def session():
    engine = make_engine("sqlite://")
    init_db(engine)
    with session_scope(make_session_factory(engine)) as s:
        yield s


@pytest.fixture()
def user(session):
    return create_user(session, "turn_user", "pw-" + secrets.token_urlsafe(12))


def counts(session):
    return (session.query(Conversation).count(), session.query(Message).count(), session.query(MessageAttachment).count())


# ---------------------------------------------------------------- 사용자 턴
def test_text_turn_creates_conversation(session, user):
    turn = record_user_turn(session, user.id, "LangGraph State가 전달되지 않아요")
    assert turn.attachment_ids == []
    msgs = list_messages(session, turn.conversation_id, user.id)
    assert [(m.role, m.input_type) for m in msgs] == [("user", "text")]


def test_turn_continues_existing_conversation(session, user):
    first = record_user_turn(session, user.id, "첫 질문")
    second = record_user_turn(session, user.id, "두 번째 질문", conversation_id=first.conversation_id)
    assert second.conversation_id == first.conversation_id
    assert session.query(Conversation).count() == 1


def test_image_turn_stores_images_and_marks_input_type(session, user):
    turn = record_user_turn(session, user.id, "이 오류 좀 봐 주세요", images=[png(), png((50, 50)), png((60, 60))])
    msg = get_message(session, turn.message_id, user.id)
    assert msg.input_type == "image" and len(turn.attachment_ids) == 3
    assert [a.position for a in list_images(session, msg.id, user.id)] == [0, 1, 2]


def test_image_only_turn_is_allowed_and_titled(session, user):
    turn = record_user_turn(session, user.id, "", images=[png()])
    conv = session.get(Conversation, turn.conversation_id)
    assert conv.title == "이미지 질문"


def test_nothing_to_record_is_rejected(session, user):
    for text, images in (("", None), ("   ", []), (None, None)):
        with pytest.raises(ValueError):
            record_user_turn(session, user.id, text, images=images)
    assert counts(session) == (0, 0, 0)


@pytest.mark.parametrize(
    "bad_images",
    [
        [png(), png(), png(), png()],        # 4장: 한도 초과
        [png(), b"not an image"],            # 두 번째가 이미지가 아님
        [png(), b""],                        # 비어 있음
    ],
)
def test_invalid_images_write_nothing(session, user, bad_images):
    """이미지 검사에 실패하면 대화도 메시지도 만들어지지 않는다 (일부만 저장되지 않음)."""
    with pytest.raises(ValueError):
        record_user_turn(session, user.id, "질문", images=bad_images)
    assert counts(session) == (0, 0, 0)


def test_too_long_text_writes_nothing(session, user, monkeypatch):
    monkeypatch.setenv("MESSAGE_MAX_CHARS", "50")
    with pytest.raises(ValueError, match="50자"):
        record_user_turn(session, user.id, "가" * 51)
    assert counts(session) == (0, 0, 0)


def test_other_users_conversation_is_rejected_before_writing(session, user):
    other = create_user(session, "someone_else", "pw-" + secrets.token_urlsafe(12))
    conv = create_conversation(session, other.id)
    with pytest.raises(PermissionError):
        record_user_turn(session, user.id, "끼어들기", conversation_id=conv.id, images=[png()])
    assert counts(session) == (1, 0, 0)  # 남의 대화는 그대로이고 아무것도 추가되지 않았다


def test_env_snapshot_defaults_to_profile_and_can_be_overridden(session, user):
    update_profile(session, user.id, python_version="3.12", os="Windows 11", lib_versions={"langgraph": "1.2.14"})
    auto = record_user_turn(session, user.id, "프로필 환경으로")
    snap = get_message(session, auto.message_id, user.id).env_snapshot
    assert snap == {"python_version": "3.12", "os": "Windows 11", "lib_versions": {"langgraph": "1.2.14"}}
    manual = record_user_turn(session, user.id, "직접 지정", conversation_id=auto.conversation_id, env_snapshot={"python_version": "3.11"})
    assert get_message(session, manual.message_id, user.id).env_snapshot == {"python_version": "3.11"}
    bare = create_user(session, "no_profile", "pw-" + secrets.token_urlsafe(12))
    assert get_message(session, record_user_turn(session, bare.id, "프로필 없음").message_id, bare.id).env_snapshot is None


# ---------------------------------------------------------------- 답변 턴
def test_assistant_turn_saves_answer_and_sources(session, user):
    turn = record_user_turn(session, user.id, "질문")
    sources = [{"url": "https://docs.langchain.com/a", "title": "A", "tech": "langgraph", "score": 0.9}, {"url": "https://github.com/x/issues/1", "doc_type": "issue"}]
    done = record_assistant_turn(session, user.id, turn.conversation_id, "원인은 reducer입니다", sources=sources, user_message_id=turn.message_id)
    assert len(done.source_ids) == 2
    assert [s.rank for s in get_sources(session, done.message_id, user.id)] == [0, 1]
    assert [m.role for m in list_messages(session, turn.conversation_id, user.id)] == ["user", "assistant"]


def test_assistant_turn_without_sources_and_long_answer_is_clipped(session, user, monkeypatch):
    monkeypatch.setenv("MESSAGE_MAX_CHARS", "100")
    turn = record_user_turn(session, user.id, "질문")
    done = record_assistant_turn(session, user.id, turn.conversation_id, "답" * 1000)
    assert done.source_ids == []
    assert get_message(session, done.message_id, user.id).content.endswith("(이하 생략)")


def test_assistant_turn_validation(session, user):
    turn = record_user_turn(session, user.id, "질문")
    other = create_user(session, "someone_else", "pw-" + secrets.token_urlsafe(12))
    with pytest.raises(ValueError, match="user_message_id"):
        record_assistant_turn(session, user.id, turn.conversation_id, "답", image_analysis="분석만 있음")
    with pytest.raises(PermissionError):
        record_assistant_turn(session, other.id, turn.conversation_id, "남의 대화")
    with pytest.raises(PermissionError):
        record_assistant_turn(session, other.id, turn.conversation_id, "답", user_message_id=turn.message_id)
    other_conv = create_conversation(session, user.id)
    with pytest.raises(ValueError, match="이 대화의 사용자 메시지"):
        record_assistant_turn(session, user.id, other_conv.id, "다른 대화에 답", user_message_id=turn.message_id)
    done = record_assistant_turn(session, user.id, turn.conversation_id, "정상 답변")
    with pytest.raises(ValueError, match="이 대화의 사용자 메시지"):
        record_assistant_turn(session, user.id, turn.conversation_id, "답", user_message_id=done.message_id)  # 답변 메시지는 안 됨


# ---------------------------------------------------------------- 이미지 분석이 이력에 반영되는지
def test_image_analysis_is_saved_and_used_in_history(session, user):
    turn = record_user_turn(session, user.id, "이 에러가 뭐죠?", images=[png()])
    record_assistant_turn(session, user.id, turn.conversation_id, "모듈이 없다는 뜻입니다", user_message_id=turn.message_id,
                          image_analysis="ModuleNotFoundError: No module named 'langgraph.prebuilt'")
    nxt = record_user_turn(session, user.id, "그럼 어떻게 설치하죠?", conversation_id=turn.conversation_id)
    history = get_history_context(session, turn.conversation_id, user.id, HistoryConfig(max_turns=5, max_tokens=5000))
    first_user = history[0]
    assert first_user["role"] == "user" and "이 에러가 뭐죠?" in first_user["content"]
    assert "[첨부 이미지에서 읽은 내용] ModuleNotFoundError" in first_user["content"]   # 원본 이미지가 아니라 읽어 낸 텍스트
    assert history[-1]["content"] == "그럼 어떻게 설치하죠?"
    assert nxt.message_id != turn.message_id


def test_history_without_analysis_is_unchanged(session, user):
    turn = record_user_turn(session, user.id, "텍스트만")
    record_assistant_turn(session, user.id, turn.conversation_id, "답")
    history = get_history_context(session, turn.conversation_id, user.id)
    assert [m["content"] for m in history] == ["텍스트만", "답"]


def test_history_does_not_load_image_bytes(session, user):
    from sqlalchemy import inspect

    turn = record_user_turn(session, user.id, "이미지 질문", images=[png()])
    session.flush(); session.expire_all()
    get_history_context(session, turn.conversation_id, user.id)
    att = session.query(MessageAttachment).one()
    assert "data" in inspect(att).unloaded   # 이력을 만드는 데 원본 이미지를 읽지 않았다
