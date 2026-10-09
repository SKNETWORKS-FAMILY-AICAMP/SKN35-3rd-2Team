"""텍스트 길이 상한 확인 (TiDB는 한 행이 6MiB를 넘으면 오류가 나므로, 그 전에 처리한다)."""

import secrets

import pytest

from src.db import (
    add_message,
    add_sources,
    create_conversation,
    create_user,
    get_sources,
    init_db,
    make_engine,
    make_session_factory,
    session_scope,
    set_summary,
)
from src.db.limits import CLIP_SUFFIX, clip_text, message_max_chars, snippet_max_chars, summary_max_chars


@pytest.fixture()
def session():
    engine = make_engine("sqlite://")
    init_db(engine)
    with session_scope(make_session_factory(engine)) as s:
        yield s


@pytest.fixture()
def conv(session):
    user = create_user(session, "limit_user", "pw-" + secrets.token_urlsafe(12))
    return user, create_conversation(session, user.id)


def test_clip_text_basics():
    assert clip_text("abc", 10) == "abc"
    assert clip_text("a" * 10, 10) == "a" * 10          # 딱 맞으면 그대로
    assert clip_text("a" * 11, 10) == "a" * 10 + CLIP_SUFFIX
    assert clip_text(None, 10) is None and clip_text("", 10) == ""


def test_defaults_and_env_override(monkeypatch):
    assert (message_max_chars(), snippet_max_chars(), summary_max_chars()) == (200_000, 50_000, 50_000)
    monkeypatch.setenv("MESSAGE_MAX_CHARS", "1234")
    assert message_max_chars() == 1234


def test_user_message_over_limit_is_rejected_with_reason(session, conv, monkeypatch):
    user, c = conv
    monkeypatch.setenv("MESSAGE_MAX_CHARS", "100")
    add_message(session, c.id, user.id, "user", "가" * 100)  # 딱 맞으면 허용
    with pytest.raises(ValueError, match=r"100자 이하.*101자"):
        add_message(session, c.id, user.id, "user", "가" * 101)


def test_assistant_message_over_limit_is_clipped_not_rejected(session, conv, monkeypatch):
    user, c = conv
    monkeypatch.setenv("MESSAGE_MAX_CHARS", "100")
    m = add_message(session, c.id, user.id, "assistant", "답" * 500)
    assert m.content.endswith(CLIP_SUFFIX) and len(m.content) == 100 + len(CLIP_SUFFIX)


def test_masking_happens_before_length_check(session, conv, monkeypatch):
    """비밀이 가려지면서 짧아지는 경우를 길이 초과로 오판하지 않는다."""
    user, c = conv
    fake_key = "nvapi" + "-" + "A1b2C3d4" * 4  # 36자
    monkeypatch.setenv("MESSAGE_MAX_CHARS", "60")
    text = f"key={fake_key}"  # 가리기 전 40자, 가린 뒤에는 [MASKED:nvidia-key] 포함 약 29자
    assert add_message(session, c.id, user.id, "user", text).content.startswith("key=[MASKED")


def test_source_snippet_and_summary_are_clipped(session, conv, monkeypatch):
    user, c = conv
    monkeypatch.setenv("SNIPPET_MAX_CHARS", "50")
    monkeypatch.setenv("SUMMARY_MAX_CHARS", "40")
    answer = add_message(session, c.id, user.id, "assistant", "답변")
    add_sources(session, answer.id, user.id, [{"url": "https://x.example", "snippet": "발" * 500}])
    snip = get_sources(session, answer.id, user.id)[0].snippet
    assert snip.endswith(CLIP_SUFFIX) and len(snip) == 50 + len(CLIP_SUFFIX)
    set_summary(session, c.id, user.id, "요" * 500, answer.id)
    assert c.summary.endswith(CLIP_SUFFIX) and len(c.summary) == 40 + len(CLIP_SUFFIX)
