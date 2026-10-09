"""간편 접근 함수(session.py) 확인. 메모리 SQLite 사용."""

import secrets

import pytest

from src.db import create_user, init_db
from src.db.models import User
from src.db.session import db_session, get_engine, get_session_factory, reset_engine


@pytest.fixture(autouse=True)
def memory_db(monkeypatch):
    for key in ("DB_HOST", "DB_USERNAME", "ENV_FILE"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    reset_engine()
    init_db(get_engine())
    yield
    reset_engine()


def pw() -> str:
    return "pw-" + secrets.token_urlsafe(12)


def test_engine_and_factory_are_created_once():
    assert get_engine() is get_engine()
    assert get_session_factory() is get_session_factory()


def test_commit_on_success():
    with db_session() as s:
        create_user(s, "alice01", pw())
    with db_session() as s:
        assert s.query(User).filter_by(username="alice01").count() == 1


def test_rollback_on_exception():
    with pytest.raises(RuntimeError):
        with db_session() as s:
            create_user(s, "bob_001", pw())
            raise RuntimeError("실패하면 되돌려져야 한다")
    with db_session() as s:
        assert s.query(User).filter_by(username="bob_001").count() == 0


def test_reset_engine_creates_a_new_engine():
    first = get_engine()
    reset_engine()
    assert get_engine() is not first


def test_explicit_env_file_overrides_already_loaded_values(tmp_path, monkeypatch):
    """ENV_FILE을 명시하면 그 파일이 이긴다. (다른 모듈이 먼저 .env를 읽어 로컬 DB 값을 올려 두었어도,
    ENV_FILE=.env.tidb로 고르면 TiDB를 가리켜야 한다.)"""
    import os

    from src.db.session import _load_env

    env_file = tmp_path / "tidb.env"
    env_file.write_text("DB_HOST=remote.example.com\nSOME_FROM_FILE=file-value\n", encoding="utf-8")
    monkeypatch.setenv("DB_HOST", "localhost")  # 먼저 읽힌 .env(로컬 MySQL)의 값이라고 가정
    monkeypatch.setenv("ENV_FILE", str(env_file))
    monkeypatch.delenv("SOME_FROM_FILE", raising=False)
    _load_env()
    assert os.environ["DB_HOST"] == "remote.example.com"      # 명시한 파일이 이긴다
    assert os.environ["SOME_FROM_FILE"] == "file-value"
    monkeypatch.delenv("SOME_FROM_FILE", raising=False)


def test_default_env_file_does_not_override_existing_values(tmp_path, monkeypatch):
    """ENV_FILE을 지정하지 않으면 기본 .env를 읽되, 이미 설정된 환경변수(예: 배포 환경에서 주입한 값)는 덮어쓰지 않는다."""
    import os

    from src.db.session import _load_env

    monkeypatch.delenv("ENV_FILE", raising=False)
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("DB_HOST=from-dotenv\nONLY_IN_DOTENV=yes\n", encoding="utf-8")
    # load_dotenv()는 코드 위치에서 위로 올라가며 .env를 찾는다. 실제 .env가 읽히지 않게 찾는 함수를 대체한다.
    monkeypatch.setattr("dotenv.main.find_dotenv", lambda *a, **k: str(dotenv_path))
    monkeypatch.setenv("DB_HOST", "injected-by-environment")
    monkeypatch.delenv("ONLY_IN_DOTENV", raising=False)
    _load_env()
    assert os.environ["DB_HOST"] == "injected-by-environment"  # 이미 있는 값이 이긴다
    assert os.environ.get("ONLY_IN_DOTENV") == "yes"             # 없는 값은 .env에서 채운다
    monkeypatch.delenv("ONLY_IN_DOTENV", raising=False)
