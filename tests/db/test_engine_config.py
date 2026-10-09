"""엔진 설정(TLS 사용 여부, 접속 URL 선택 규칙) 확인. DB에 접속하지 않는다."""

import pytest
from sqlalchemy.engine import make_url

from src.db.engine import build_url, use_tls

_DB_KEYS = ("DATABASE_URL", "DB_HOST", "DB_PORT", "DB_USERNAME", "DB_PASSWORD", "DB_DATABASE", "DB_SSL")


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for key in _DB_KEYS:
        monkeypatch.delenv(key, raising=False)


@pytest.mark.parametrize(
    "host, expected",
    [
        ("localhost", False),
        ("LOCALHOST", False),
        ("127.0.0.1", False),
        ("::1", False),
        ("tidb.example.com", True),  # 원격(TiDB Cloud 같은 외부 서버)은 켠다
        ("db.example.com", True),
        (None, True),  # 호스트가 없으면 원격으로 보고 켠다(안전한 쪽)
    ],
)
def test_use_tls_default_depends_on_host(host, expected):
    url = make_url("mysql+pymysql://u:p@x/db").set(host=host)
    assert use_tls(url) is expected


@pytest.mark.parametrize("flag, expected", [("true", True), ("1", True), ("YES", True), ("false", False), ("0", False), ("off", False)])
def test_use_tls_explicit_flag_wins_over_host(monkeypatch, flag, expected):
    monkeypatch.setenv("DB_SSL", flag)
    assert use_tls(make_url("mysql+pymysql://u:p@localhost/db")) is expected
    assert use_tls(make_url("mysql+pymysql://u:p@db.example.com/db")) is expected


def test_empty_flag_falls_back_to_host_rule(monkeypatch):
    monkeypatch.setenv("DB_SSL", "  ")
    assert use_tls(make_url("mysql+pymysql://u:p@localhost/db")) is False


def test_build_url_priority_and_special_characters(monkeypatch):
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_USERNAME", "app_user")
    monkeypatch.setenv("DB_PASSWORD", "p@ss:w/rd#1")  # 접속 문자열을 깨뜨리기 쉬운 문자들
    monkeypatch.setenv("DB_DATABASE", "skn35_3rd")
    url = build_url()
    assert (url.drivername, url.host, url.port, url.username, url.database) == (
        "mysql+pymysql", "localhost", 4000, "app_user", "skn35_3rd")
    assert url.password == "p@ss:w/rd#1"  # 그대로 보존된다
    monkeypatch.setenv("DB_PORT", "3306")
    assert build_url().port == 3306
    monkeypatch.setenv("DATABASE_URL", "sqlite:///x.db")  # DATABASE_URL이 우선
    assert build_url().drivername == "sqlite"


def test_build_url_falls_back_to_local_sqlite_when_nothing_configured():
    url = build_url()
    assert url.drivername == "sqlite" and str(url.database).endswith("app.sqlite3")
