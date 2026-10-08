"""DB 설정값이 src/const/db_config.py 한곳에서 오는지 확인한다."""

import re
import subprocess
import sys
from pathlib import Path

import pytest

from src.const import db_config as cfg
from src.db import HistoryConfig
from src.db.history import estimate_tokens
from src.db.images import max_image_bytes, max_images_per_message
from src.db.limits import message_max_chars, snippet_max_chars, summary_max_chars

ROOT = Path(__file__).resolve().parents[2]
_ENV_KEYS = ("IMAGE_MAX_BYTES", "IMAGE_MAX_PER_MESSAGE", "MESSAGE_MAX_CHARS", "SNIPPET_MAX_CHARS",
             "SUMMARY_MAX_CHARS", "HISTORY_MAX_TURNS", "HISTORY_MAX_TOKENS")


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for key in _ENV_KEYS:
        monkeypatch.delenv(key, raising=False)


def test_defaults_come_from_const():
    assert max_image_bytes() == cfg.DEFAULT_IMAGE_MAX_BYTES
    assert max_images_per_message() == cfg.DEFAULT_IMAGE_MAX_PER_MESSAGE == 3
    assert message_max_chars() == cfg.DEFAULT_MESSAGE_MAX_CHARS
    assert snippet_max_chars() == cfg.DEFAULT_SNIPPET_MAX_CHARS
    assert summary_max_chars() == cfg.DEFAULT_SUMMARY_MAX_CHARS
    default = HistoryConfig()
    assert (default.max_turns, default.max_tokens) == (cfg.DEFAULT_HISTORY_MAX_TURNS, cfg.DEFAULT_HISTORY_MAX_TOKENS)
    assert HistoryConfig.from_env() == default
    assert estimate_tokens("a" * 30) == 30 // cfg.TOKEN_ESTIMATE_DIVISOR


def test_env_still_overrides_const_defaults(monkeypatch):
    """const는 기본값만 정하고, 환경변수로 호출 시점마다 바꿀 수 있어야 한다 (테스트와 배포 환경에서 필요)."""
    monkeypatch.setenv("IMAGE_MAX_BYTES", "123")
    monkeypatch.setenv("IMAGE_MAX_PER_MESSAGE", "2")
    monkeypatch.setenv("MESSAGE_MAX_CHARS", "77")
    monkeypatch.setenv("HISTORY_MAX_TURNS", "9")
    assert (max_image_bytes(), max_images_per_message(), message_max_chars()) == (123, 2, 77)
    assert HistoryConfig.from_env().max_turns == 9


def test_empty_env_values_fall_back_to_defaults(monkeypatch):
    """.env.example을 복사해 빈 값("IMAGE_MAX_BYTES=")으로 둔 경우에도 오류 없이 기본값을 쓴다."""
    for key in _ENV_KEYS:
        monkeypatch.setenv(key, "")
    assert max_image_bytes() == cfg.DEFAULT_IMAGE_MAX_BYTES
    assert max_images_per_message() == cfg.DEFAULT_IMAGE_MAX_PER_MESSAGE
    assert (message_max_chars(), snippet_max_chars(), summary_max_chars()) == (
        cfg.DEFAULT_MESSAGE_MAX_CHARS, cfg.DEFAULT_SNIPPET_MAX_CHARS, cfg.DEFAULT_SUMMARY_MAX_CHARS)
    assert HistoryConfig.from_env() == HistoryConfig()


def test_empty_db_env_values_use_defaults(monkeypatch):
    from src.db.engine import build_url, use_tls

    for key in ("DATABASE_URL", "DB_SSL", "DB_SSL_CA", "DB_PORT"):
        monkeypatch.setenv(key, "")
    monkeypatch.setenv("DB_HOST", "remote.example.com")
    monkeypatch.setenv("DB_USERNAME", "u")
    url = build_url()
    assert url.port == cfg.DEFAULT_DB_PORT
    assert use_tls(url) is True   # DB_SSL이 비어 있으면 호스트 규칙을 따른다


def test_const_values_are_sane_for_the_tidb_row_limit():
    """TiDB 한 행 6MiB 제한 안에 한참 여유가 있어야 한다 (한글 3바이트, 이모지 4바이트 기준)."""
    tidb_row_limit = 6_291_456
    assert cfg.DEFAULT_IMAGE_MAX_BYTES * 2 < tidb_row_limit
    assert cfg.DEFAULT_MESSAGE_MAX_CHARS * 4 < tidb_row_limit / 4
    assert cfg.IMAGE_ANALYSIS_MAX_CHARS * 4 + cfg.DEFAULT_IMAGE_MAX_BYTES < tidb_row_limit


def test_no_hardcoded_setting_numbers_left_in_src_db():
    """설정 숫자가 src/db에 중복으로 남아 있으면 안 된다 (const와 어긋나는 일을 막는다)."""
    pattern = re.compile(r"\b(2_000_000|200_000|50_000|100_000|40_000_000)\b|getenv\(\"DB_PORT\", \"4000\"\)")
    offenders = []
    for path in sorted((ROOT / "src" / "db").glob("*.py")):
        for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if pattern.search(line.split("#")[0]):  # 주석은 제외
                offenders.append(f"{path.name}:{no}: {line.strip()}")
    assert offenders == []


def test_importing_src_db_does_not_pull_in_teammates_config():
    """src/db는 다른 담당자의 src/const/config.py(와 그 안의 load_dotenv, 모델 설정)에 의존하지 않는다."""
    code = "import sys; import src.db; print('src.const.config' in sys.modules, 'src.const.models' in sys.modules)"
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, timeout=60,
                         env={**__import__("os").environ, "PYTHONPATH": str(ROOT)})
    assert out.returncode == 0, out.stderr[-500:]
    assert out.stdout.strip() == "False False"
