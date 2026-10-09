"""마이그레이션 확인: 새 DB에서 끝까지 적용한 결과가 모델과 같은지, 기존 데이터가 보존되는지."""

from pathlib import Path

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import inspect, text

from src.db.engine import make_engine
from src.db.models import Base

ALEMBIC_INI = Path(__file__).resolve().parents[2] / "src" / "db" / "alembic.ini"


@pytest.fixture()
def engine():
    return make_engine("sqlite://")


def _cfg(conn) -> Config:
    cfg = Config(str(ALEMBIC_INI))
    cfg.attributes["connection"] = conn
    return cfg


def test_upgrade_head_matches_models(engine):
    """마이그레이션만으로 만든 구조가 models.py와 어긋나지 않는다 (모델만 고치고 마이그레이션을 빼먹으면 실패)."""
    with engine.begin() as conn:
        command.upgrade(_cfg(conn), "head")
        diffs = compare_metadata(MigrationContext.configure(conn), Base.metadata)
    assert diffs == [], diffs


def test_upgrade_preserves_existing_rows_and_defaults_active(engine):
    """0001 구조에 이미 계정이 있어도, 0002로 올리면 계정은 남고 모두 활성이 된다."""
    with engine.begin() as conn:
        cfg = _cfg(conn)
        command.upgrade(cfg, "0001")
        assert "is_active" not in {c["name"] for c in inspect(conn).get_columns("users")}
        conn.execute(text(
            "INSERT INTO users (username, password_hash, is_admin, created_at) "
            "VALUES ('legacy_user', 'x', 0, '2026-01-01 00:00:00')"
        ))
        command.upgrade(cfg, "head")
        row = conn.execute(text("SELECT username, is_active FROM users")).one()
        assert row.username == "legacy_user" and bool(row.is_active) is True
        assert "message_sources" in inspect(conn).get_table_names()


def test_downgrade_to_base_removes_everything(engine):
    with engine.begin() as conn:
        cfg = _cfg(conn)
        command.upgrade(cfg, "head")
        command.downgrade(cfg, "base")
        assert [t for t in inspect(conn).get_table_names() if t != "alembic_version"] == []
