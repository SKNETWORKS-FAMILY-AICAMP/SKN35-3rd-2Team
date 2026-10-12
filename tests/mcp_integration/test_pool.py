"""MCP 서버 연결 재사용(pool.py) 시험. 진짜 시험용 서버를 자식 프로세스로 띄운다."""

import asyncio
from dataclasses import replace
from pathlib import Path

import pytest

from src.const import mcp_config as cfg
from src.const.mcp_config import OWN_SERVER
from src.mcp_integration.client import pool
from src.mcp_integration.client.tools import call_tool, list_tools

EXAMPLE = replace(OWN_SERVER, name="example_pool", args=(str(Path(__file__).with_name("example_server.py")),))


@pytest.fixture(autouse=True)
def fresh_pool():
    pool.close_all()
    pool._connections.clear()
    yield
    pool.close_all()


def current_connection():
    return pool._connections[pool._key(EXAMPLE)]


def test_same_connection_is_reused_across_calls_and_list():
    list_tools(EXAMPLE)
    first = current_connection()
    assert call_tool(EXAMPLE, "repeat_text", {"text": "a", "times": 2})["text"] == "a a"
    assert call_tool(EXAMPLE, "get_utc_time", {})["is_error"] is False
    assert current_connection() is first


def test_reused_connection_is_much_faster_than_a_fresh_server():
    import time

    call_tool(EXAMPLE, "get_utc_time", {})  # 서버를 띄우는 첫 호출
    started = time.monotonic()
    for _ in range(5):
        call_tool(EXAMPLE, "get_utc_time", {})
    assert (time.monotonic() - started) / 5 < 0.5  # 서버를 새로 띄우면 호출마다 1초 이상


def test_closed_connection_is_replaced_on_next_call():
    call_tool(EXAMPLE, "get_utc_time", {})
    old = current_connection()
    pool._loop.call_soon_threadsafe(old._stop.set)  # 서버가 끝난 것과 같은 상황
    for _ in range(50):
        if not old.alive:
            break
        import time

        time.sleep(0.1)
    assert call_tool(EXAMPLE, "repeat_text", {"text": "x", "times": 1})["text"] == "x"
    assert current_connection() is not old


def test_failed_call_is_retried_once_on_a_new_connection():
    call_tool(EXAMPLE, "get_utc_time", {})
    old = current_connection()
    attempts = []

    async def operation(client):
        attempts.append(client)
        if len(attempts) == 1:
            raise ConnectionError("broken pipe")
        return "ok"

    assert pool.run(EXAMPLE, operation, 20) == "ok"
    assert len(attempts) == 2 and attempts[0] is not attempts[1]
    assert current_connection() is not old


def test_failure_twice_raises_the_error():
    async def always_fails(client):
        raise ConnectionError("down")

    with pytest.raises(ConnectionError):
        pool.run(EXAMPLE, always_fails, 20)


def test_timeout_drops_the_connection_and_next_call_works():
    call_tool(EXAMPLE, "get_utc_time", {})
    old = current_connection()

    async def hangs(client):
        await asyncio.sleep(30)

    with pytest.raises(TimeoutError):
        pool.run(EXAMPLE, hangs, 0.3)
    assert pool._key(EXAMPLE) not in pool._connections
    assert call_tool(EXAMPLE, "get_utc_time", {})["is_error"] is False
    assert current_connection() is not old


def test_tool_error_does_not_drop_the_connection():
    call_tool(EXAMPLE, "get_utc_time", {})
    old = current_connection()
    assert call_tool(EXAMPLE, "repeat_text", {"text": "x", "times": 10})["is_error"] is True
    assert current_connection() is old


def test_switch_off_uses_a_fresh_server_each_time(monkeypatch):
    monkeypatch.setattr(cfg, "REUSE_SERVER_CONNECTION", False)
    assert call_tool(EXAMPLE, "repeat_text", {"text": "z", "times": 2})["text"] == "z z"
    assert pool._key(EXAMPLE) not in pool._connections


def test_two_threads_can_call_at_the_same_time():
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(4) as executor:
        results = list(executor.map(lambda i: call_tool(EXAMPLE, "repeat_text", {"text": str(i), "times": 2})["text"], range(8)))
    assert results == [f"{i} {i}" for i in range(8)]
