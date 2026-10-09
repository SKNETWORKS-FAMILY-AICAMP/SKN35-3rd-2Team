"""src/db 동작 확인 (메모리 SQLite 사용 — 실제 TiDB/MySQL에는 연결하지 않는다).

실행 (프로젝트 루트에서, torch 등 무거운 의존성을 설치하지 않는 방법):
    uv run --no-project --python 3.12 --with sqlalchemy==2.1.3 --with pytest \
        env PYTHONPATH=. python -m pytest tests/db -q
"""

import secrets
from datetime import datetime, timedelta, timezone

import pytest

from src.db import (
    HistoryConfig,
    UsernameTakenError,
    add_message,
    authenticate,
    create_conversation,
    create_user,
    delete_conversation,
    get_conversation,
    get_history_context,
    init_db,
    list_conversations,
    make_engine,
    make_session_factory,
    select_history,
    session_scope,
    set_summary,
    update_profile,
)
from src.db.models import Message, User
from src.db.security import hash_password, verify_password


def new_password() -> str:
    return "pw-" + secrets.token_urlsafe(12)


@pytest.fixture()
def session():
    engine = make_engine("sqlite://")
    init_db(engine)
    factory = make_session_factory(engine)
    with session_scope(factory) as s:
        yield s


# ---------------------------------------------------------------- 비밀번호
def test_hash_roundtrip_and_salt():
    pw = new_password()
    h1, h2 = hash_password(pw), hash_password(pw)
    assert h1 != h2  # 같은 비밀번호도 salt가 달라 해시가 다르다
    assert pw not in h1
    assert verify_password(pw, h1) and verify_password(pw, h2)
    assert not verify_password(pw + "x", h1)


@pytest.mark.parametrize("broken", ["", "plain", "scrypt$1$2", "bcrypt$a$b$c$d$e", "scrypt$x$y$z$@@$@@"])
def test_verify_rejects_malformed_hash(broken):
    assert verify_password("anything", broken) is False


# ---------------------------------------------------------------- 가입 / 로그인
def test_create_user_normalizes_and_blocks_duplicates(session):
    pw = new_password()
    user = create_user(session, "  Alice_01 ", pw)
    assert user.username == "alice_01"
    assert user.password_hash != pw
    with pytest.raises(UsernameTakenError):
        create_user(session, "ALICE_01", new_password())


@pytest.mark.parametrize("name", ["ab", "has space", "한글아이디", "x" * 31, "semi;colon"])
def test_create_user_rejects_bad_username(session, name):
    with pytest.raises(ValueError):
        create_user(session, name, new_password())


def test_create_user_rejects_short_password(session):
    with pytest.raises(ValueError):
        create_user(session, "bob_01", "short")


def test_authenticate(session):
    pw = new_password()
    user = create_user(session, "carol", pw)
    assert user.last_login_at is None
    ok = authenticate(session, "CAROL", pw)
    assert ok is not None and ok.id == user.id
    assert ok.last_login_at is not None
    assert authenticate(session, "carol", pw + "!") is None
    assert authenticate(session, "nobody", pw) is None


def test_timestamps_are_utc(session):
    user = create_user(session, "dave", new_password())
    session.flush()
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    assert abs(now_utc - user.created_at) < timedelta(seconds=5)


# ---------------------------------------------------------------- 대화 접근 권한
def test_conversation_isolation_between_users(session):
    a = create_user(session, "user_a", new_password())
    b = create_user(session, "user_b", new_password())
    conv = create_conversation(session, a.id)
    add_message(session, conv.id, a.id, "user", "내 질문")

    assert get_conversation(session, conv.id, a.id) is not None
    assert get_conversation(session, conv.id, b.id) is None  # 남의 대화는 보이지 않는다
    with pytest.raises(PermissionError):
        add_message(session, conv.id, b.id, "user", "끼어들기")
    with pytest.raises(PermissionError):
        get_history_context(session, conv.id, b.id)
    assert delete_conversation(session, conv.id, b.id) is False
    assert list_conversations(session, b.id) == []
    assert len(list_conversations(session, a.id)) == 1


# ---------------------------------------------------------------- 메시지
def test_add_message_sets_title_tokens_and_env(session):
    u = create_user(session, "erin", new_password())
    conv = create_conversation(session, u.id)
    env = {"python": "3.12", "langgraph": "1.2.14"}
    m = add_message(session, conv.id, u.id, "user", "LangGraph에서 State가 전달되지 않아요", env_snapshot=env)
    assert conv.title.startswith("LangGraph에서 State")
    assert m.token_count > 0
    assert m.env_snapshot == env
    with pytest.raises(ValueError):
        add_message(session, conv.id, u.id, "system", "x")
    with pytest.raises(ValueError):
        add_message(session, conv.id, u.id, "user", "x", input_type="video")


def test_list_conversations_most_recent_first(session):
    u = create_user(session, "frank", new_password())
    c1 = create_conversation(session, u.id, "첫 번째")
    c2 = create_conversation(session, u.id, "두 번째")
    # 시계 해상도에 기대지 않도록 갱신 시각을 명시한다 (윈도우 시계는 거칠어서 두 시각이 같아질 수 있다).
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    c1.updated_at = now
    c2.updated_at = now - timedelta(seconds=30)
    session.flush()
    assert [c.id for c in list_conversations(session, u.id)] == [c1.id, c2.id]  # 최근 갱신된 c1이 먼저
    c2.updated_at = now + timedelta(seconds=30)
    session.flush()
    assert [c.id for c in list_conversations(session, u.id)] == [c2.id, c1.id]  # 갱신 순서가 바뀌면 따라 바뀜


def test_profile_partial_update(session):
    u = create_user(session, "gina", new_password())
    update_profile(session, u.id, python_version="3.12", lib_versions={"langchain": "1.4.3"})
    p = update_profile(session, u.id, os="Windows 11")  # 일부만 바꿔도 기존 값은 유지
    assert (p.python_version, p.os, p.lib_versions) == ("3.12", "Windows 11", {"langchain": "1.4.3"})


def test_deleting_user_removes_conversations_and_messages(session):
    u = create_user(session, "hank", new_password())
    conv = create_conversation(session, u.id)
    add_message(session, conv.id, u.id, "user", "질문")
    session.delete(u)
    session.flush()
    assert session.query(Message).count() == 0
    assert session.query(User).count() == 0


# ---------------------------------------------------------------- 이력 반영 (DB 연결)
def _fill(session, user, conv, pairs):
    for i in range(pairs):
        add_message(session, conv.id, user.id, "user", f"질문{i}")
        add_message(session, conv.id, user.id, "assistant", f"답변{i}")


def test_history_context_respects_max_turns(session):
    u = create_user(session, "iris", new_password())
    conv = create_conversation(session, u.id)
    _fill(session, u, conv, 10)
    ctx = get_history_context(session, conv.id, u.id, HistoryConfig(max_turns=3, max_tokens=10_000))
    assert [m["content"] for m in ctx] == ["질문7", "답변7", "질문8", "답변8", "질문9", "답변9"]


def test_history_context_empty_conversation(session):
    u = create_user(session, "jack", new_password())
    conv = create_conversation(session, u.id)
    assert get_history_context(session, conv.id, u.id) == []


def test_history_context_uses_summary_and_skips_summarized_messages(session):
    u = create_user(session, "kate", new_password())
    conv = create_conversation(session, u.id)
    _fill(session, u, conv, 5)
    msgs = session.query(Message).order_by(Message.id).all()
    upto = msgs[5].id  # 앞의 6개 메시지(질문0~답변2)는 요약에 반영됐다고 가정
    set_summary(session, conv.id, u.id, "State 업데이트 문제를 논의함", upto)
    ctx = get_history_context(session, conv.id, u.id, HistoryConfig(max_turns=10, max_tokens=10_000))
    assert ctx[0]["role"] == "system" and "State 업데이트 문제" in ctx[0]["content"]
    assert [m["content"] for m in ctx[1:]] == ["질문3", "답변3", "질문4", "답변4"]


# ---------------------------------------------------------------- 이력 선택 규칙 (순수 함수)
def _m(role, content, tokens=None):
    return {"role": role, "content": content, "token_count": tokens or len(content) // 3 or 1}


def test_select_history_trims_oldest_by_token_budget():
    msgs = [_m("user", "a" * 300, 100), _m("assistant", "b" * 300, 100),
            _m("user", "c" * 300, 100), _m("assistant", "d" * 300, 100)]
    out = select_history(msgs, None, HistoryConfig(max_turns=10, max_tokens=250))
    assert [m["role"] for m in out] == ["user", "assistant"]  # 오래된 쌍부터 버려져 최근 쌍만 남음
    assert out[0]["content"].startswith("c")


def test_select_history_never_starts_with_assistant():
    msgs = [_m("user", "q0", 100), _m("assistant", "a0", 100), _m("user", "q1", 100), _m("assistant", "a1", 100)]
    out = select_history(msgs, None, HistoryConfig(max_turns=10, max_tokens=300))
    assert out[0]["role"] == "user"


def test_select_history_truncates_single_oversized_message():
    out = select_history([_m("user", "x" * 30_000, 10_000)], None, HistoryConfig(max_turns=3, max_tokens=300))
    assert len(out) == 1 and len(out[0]["content"]) < 2_000


def test_select_history_zero_turns_returns_only_summary():
    out = select_history([_m("user", "q", 5)], "요약", HistoryConfig(max_turns=0, max_tokens=300))
    assert [m["role"] for m in out] == ["system"]
    assert select_history([_m("user", "q", 5)], None, HistoryConfig(max_turns=0, max_tokens=300)) == []


def test_history_total_tokens_stay_within_budget():
    msgs = [_m("user" if i % 2 == 0 else "assistant", "z" * 90, 30) for i in range(40)]
    cfg = HistoryConfig(max_turns=6, max_tokens=200)
    out = select_history(msgs, "요" * 600, cfg)
    total = sum(max(1, len(m["content"]) // 3) for m in out)
    assert total <= cfg.max_tokens + 10  # 접두어("[이전 대화 요약] ") 길이만큼의 오차 허용


# ---------------------------------------------------------------- 시드
def test_seed_is_idempotent_and_skips_missing_env(session, monkeypatch):
    from src.db.seed import seed

    for key in ("SEED_ADMIN_USERNAME", "SEED_ADMIN_PASSWORD", "SEED_USER_USERNAME", "SEED_USER_PASSWORD"):
        monkeypatch.delenv(key, raising=False)
    assert seed(session) == []  # 환경변수가 없으면 아무것도 만들지 않는다

    monkeypatch.setenv("SEED_ADMIN_USERNAME", "Admin")
    monkeypatch.setenv("SEED_ADMIN_PASSWORD", new_password())
    assert seed(session) == ["admin"]
    assert seed(session) == []  # 두 번째 실행은 건너뛴다
    assert session.query(User).filter_by(username="admin").one().is_admin is True
