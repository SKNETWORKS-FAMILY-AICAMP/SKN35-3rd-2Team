"""
MCP 클라이언트와 우리 서버 시험. 우리 서버(src/mcp_integration/server)를 진짜 자식 프로세스로 띄우므로 한 번에 2초쯤 걸린다.
실행: uv run pytest tests/mcp_integration -q
"""

import asyncio
from dataclasses import replace
from pathlib import Path

import pytest

from src.const.mcp_config import OWN_SERVER
from src.mcp_integration.client.tools import call_tool, describe_error, list_tools, run_sync


# 시험용 서버 (예: repeat_text는 times가 1~5가 아니면 도구 오류를 낸다)
EXAMPLE = replace(OWN_SERVER, name="example", args=(str(Path(__file__).with_name("example_server.py")),))


def test_lists_our_real_tools_with_descriptions():
    tools = {t["name"]: t for t in list_tools(OWN_SERVER)}
    assert set(tools) == {
        "get_latest_version",
        "check_version_compat",
        "search_github_issues",
        "get_github_issue",
        "check_symbol_exists",
    }
    assert all(t["server"] == OWN_SERVER.name and t["description"] for t in tools.values())
    assert tools["check_version_compat"]["input_schema"]["required"] == ["packages"]


def test_lists_example_server_tools_with_schema():
    tools = {t["name"]: t for t in list_tools(EXAMPLE)}
    assert {"get_utc_time", "repeat_text"} == set(tools)
    assert tools["repeat_text"]["input_schema"]["required"] == ["text", "times"]


def test_call_success_and_deliberate_tool_error():
    ok = call_tool(EXAMPLE, "repeat_text", {"text": "hi", "times": 3})
    assert ok == {"text": "hi hi hi", "is_error": False}
    # 도구가 스스로 실패하면 예외가 아니라 is_error로 오고, ToolError의 이유가 그대로 전달된다
    bad = call_tool(EXAMPLE, "repeat_text", {"text": "hi", "times": 10})
    assert bad["is_error"] is True and "1에서 5 사이" in bad["text"]


def test_unsupported_transport_is_reported():
    with pytest.raises(NotImplementedError, match="http"):
        list_tools(replace(OWN_SERVER, transport="http", url="http://localhost:8000/mcp"))


def test_server_that_cannot_start_raises():
    broken = replace(OWN_SERVER, command="this-command-does-not-exist-12345", args=())
    with pytest.raises(Exception):
        list_tools(broken, timeout=15)


def test_call_timeout_raises_timeout_error():
    with pytest.raises(TimeoutError):
        call_tool(EXAMPLE, "get_utc_time", {}, timeout=0.01)


def test_run_sync_works_inside_a_running_event_loop():
    async def inside_loop():
        return run_sync(asyncio.sleep(0, result="done"))

    assert asyncio.run(inside_loop()) == "done"


def test_describe_error_masks_secrets_and_is_short():
    key = "sk-" + "a1B2c3D4e5F6g7H8i9J0k1L2"
    text = describe_error(RuntimeError(f"bad key {key} " + "x " * 500))
    assert key not in text and text.startswith("RuntimeError:") and len(text) <= 300
