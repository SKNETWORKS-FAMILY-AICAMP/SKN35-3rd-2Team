"""계정 관리, 출처 저장, 저장 시 마스킹 확인 (메모리 SQLite)."""

import secrets

import pytest

from src.db import (
    add_message,
    add_sources,
    authenticate,
    change_password,
    create_conversation,
    create_user,
    get_message,
    get_sources,
    init_db,
    list_users,
    make_engine,
    make_session_factory,
    reset_password,
    session_scope,
    set_source_grounded,
    set_user_active,
)

NV = "nvapi" + "-" + "A1b2C3d4" * 4


def pw() -> str:
    return "pw-" + secrets.token_urlsafe(12)


@pytest.fixture()
def session():
    engine = make_engine("sqlite://")
    init_db(engine)
    with session_scope(make_session_factory(engine)) as s:
        yield s


# ---------------------------------------------------------------- 계정 관리
def test_change_password(session):
    old, new = pw(), pw()
    u = create_user(session, "alice01", old)
    assert change_password(session, u.id, "wrong-password", new) is False
    assert change_password(session, u.id, old, new) is True
    assert authenticate(session, "alice01", old) is None
    assert authenticate(session, "alice01", new) is not None
    with pytest.raises(ValueError):
        change_password(session, u.id, new, "short")


def test_inactive_user_cannot_login_and_can_be_reactivated(session):
    admin_pw, user_pw = pw(), pw()
    admin = create_user(session, "admin01", admin_pw, is_admin=True)
    create_user(session, "bob_01", user_pw)
    assert authenticate(session, "bob_01", user_pw) is not None
    assert set_user_active(session, admin.id, "bob_01", False) is True
    assert authenticate(session, "bob_01", user_pw) is None  # 비밀번호가 맞아도 막힌다
    assert set_user_active(session, admin.id, "bob_01", True) is True
    assert authenticate(session, "bob_01", user_pw) is not None
    assert set_user_active(session, admin.id, "nobody", False) is False


def test_admin_only_actions_and_self_deactivation_blocked(session):
    admin = create_user(session, "admin01", pw(), is_admin=True)
    normal = create_user(session, "normal1", pw())
    for call in (
        lambda: list_users(session, normal.id),
        lambda: set_user_active(session, normal.id, "admin01", False),
        lambda: reset_password(session, normal.id, "admin01", pw()),
    ):
        with pytest.raises(PermissionError):
            call()
    with pytest.raises(ValueError):
        set_user_active(session, admin.id, "admin01", False)  # 관리자가 자기 자신을 막는 실수 방지
    assert [u.username for u in list_users(session, admin.id)] == ["admin01", "normal1"]


def test_admin_reset_password(session):
    admin = create_user(session, "admin01", pw(), is_admin=True)
    create_user(session, "carol01", pw())
    new = pw()
    assert reset_password(session, admin.id, "carol01", new) is True
    assert authenticate(session, "carol01", new) is not None


def test_deactivated_admin_loses_admin_rights(session):
    a1 = create_user(session, "admin01", pw(), is_admin=True)
    a2 = create_user(session, "admin02", pw(), is_admin=True)
    set_user_active(session, a1.id, "admin02", False)
    with pytest.raises(PermissionError):
        list_users(session, a2.id)


# ---------------------------------------------------------------- 저장 시 마스킹
def test_add_message_masks_secrets_by_default(session):
    u = create_user(session, "dave_01", pw())
    conv = create_conversation(session, u.id)
    m = add_message(session, conv.id, u.id, "user", f"에러가 나요 NVIDIA_API_KEY={NV}")
    assert NV not in m.content and "[MASKED" in m.content and "에러가 나요" in m.content
    raw = add_message(session, conv.id, u.id, "user", f"원문 보존 key={NV}", mask=False)
    assert NV in raw.content


# ---------------------------------------------------------------- 출처
def _answer(session, name="erin_01"):
    u = create_user(session, name, pw())
    conv = create_conversation(session, u.id)
    q = add_message(session, conv.id, u.id, "user", "State가 전달되지 않아요")
    a = add_message(session, conv.id, u.id, "assistant", "reducer를 확인하세요")
    return u, conv, q, a


def test_add_and_get_sources_keep_order(session):
    u, conv, q, a = _answer(session)
    add_sources(session, a.id, u.id, [
        {"url": "https://docs.langchain.com/oss/python/langgraph/graph-api", "title": "Graph API",
         "tech": "langgraph", "version": "1.x", "doc_type": "docs", "snippet": "State reducer", "score": 0.91},
        {"url": "https://github.com/langchain-ai/langgraph/issues/1", "doc_type": "issue", "score": 0.7},
    ])
    got = get_sources(session, a.id, u.id)
    assert [s.rank for s in got] == [0, 1]
    assert got[0].title == "Graph API" and got[1].title is None
    assert all(s.is_grounded is None for s in got)  # 점검 전
    set_source_grounded(session, got[0].id, True)
    assert get_sources(session, a.id, u.id)[0].is_grounded is True


def test_sources_validation_and_ownership(session):
    u, conv, q, a = _answer(session)
    other = create_user(session, "frank_01", pw())
    with pytest.raises(ValueError):
        add_sources(session, q.id, u.id, [{"url": "https://x.example"}])       # user 메시지에는 불가
    with pytest.raises(ValueError):
        add_sources(session, a.id, u.id, [{"title": "url 없음"}])
    with pytest.raises(ValueError):
        add_sources(session, a.id, u.id, [{"url": "https://x.example", "bogus": 1}])
    with pytest.raises(PermissionError):
        add_sources(session, a.id, other.id, [{"url": "https://x.example"}])   # 남의 메시지
    with pytest.raises(PermissionError):
        get_sources(session, a.id, other.id)
    assert get_message(session, a.id, other.id) is None


def test_source_snippet_is_masked(session):
    u, conv, q, a = _answer(session)
    add_sources(session, a.id, u.id, [{"url": "https://x.example", "snippet": f"예제 key={NV}"}])
    assert NV not in get_sources(session, a.id, u.id)[0].snippet


def test_deleting_conversation_removes_sources(session):
    from src.db import delete_conversation
    from src.db.models import MessageSource

    u, conv, q, a = _answer(session)
    add_sources(session, a.id, u.id, [{"url": "https://x.example"}])
    assert session.query(MessageSource).count() == 1
    delete_conversation(session, conv.id, u.id)
    session.flush()
    assert session.query(MessageSource).count() == 0
