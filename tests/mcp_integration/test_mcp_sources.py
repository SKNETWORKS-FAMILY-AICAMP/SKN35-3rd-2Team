"""MCP 도구 결과에서 출처 뽑기(extract_sources) 확인. 도구의 실제 출력과 모양이 어긋나지 않는지도 확인한다."""

import asyncio
import json

import pytest

from src.mcp_integration.client.sources import extract_sources
from src.mcp_integration.server.tools import common, github_tools, version_tools


def run(coro):
    return asyncio.run(coro)


def fake_fetch(monkeypatch, routes):
    async def fetch(url, **kwargs):
        for key, value in routes.items():
            if key in url:
                return value
        raise AssertionError(f"예상하지 못한 요청: {url}")

    monkeypatch.setattr(common, "fetch_json", fetch)


SEARCH = {
    "total_count": 2,
    "items": [
        {"repository_url": "https://api.github.com/repos/langchain-ai/langgraph", "number": 9163, "title": "GraphRecursionError raised after the graph finished",
         "state": "open", "html_url": "https://github.com/langchain-ai/langgraph/issues/9163", "labels": [], "comments": 2, "body": "본문 " * 200},
        {"repository_url": "https://api.github.com/repos/modelcontextprotocol/python-sdk", "number": 12, "title": "-32601 on connect",
         "state": "closed", "html_url": "https://github.com/modelcontextprotocol/python-sdk/issues/12", "labels": [], "comments": 0, "body": None},
    ],
}
ISSUE = {"title": "GraphRecursionError raised", "state": "closed", "state_reason": "completed", "html_url": "https://github.com/langchain-ai/langgraph/issues/9163",
         "user": {"login": "u"}, "labels": [], "body": "상세 본문", "comments": 0}
PYPI = {"info": {"name": "langgraph", "version": "1.2.14", "requires_python": ">=3.10", "summary": "Building stateful agents", "project_urls": {}},
        "releases": {"1.2.14": [{"upload_time_iso_8601": "2026-10-01T00:00:00Z"}]}, "urls": []}


# ---------------------------------------------------------------- 도구의 실제 출력으로 확인 (출력 모양이 바뀌면 여기서 알 수 있다)
def test_search_issues_output_yields_one_source_per_issue(monkeypatch):
    fake_fetch(monkeypatch, {"search/issues": SEARCH})
    text = common.dump(run(github_tools.search_issues("GraphRecursionError")))
    first, second = extract_sources("search_github_issues", text)
    assert first["url"].endswith("/langgraph/issues/9163") and first["tech"] == "langgraph" and first["doc_type"] == "issue"
    assert first["title"].startswith("langchain-ai/langgraph#9163 GraphRecursionError") and first["snippet"].startswith("[open] 본문")
    assert second["tech"] == "mcp" and second["snippet"] == "[closed]"


def test_issue_output_yields_the_issue(monkeypatch):
    fake_fetch(monkeypatch, {"/issues/9163": ISSUE})
    text = common.dump(run(github_tools.get_issue("langchain-ai/langgraph", 9163, 0)))
    [source] = extract_sources("get_github_issue", text)
    assert source["url"] == ISSUE["html_url"] and source["tech"] == "langgraph" and source["snippet"].startswith("[closed] 상세")


def test_latest_version_output_yields_the_pypi_page(monkeypatch):
    fake_fetch(monkeypatch, {"pypi.org/pypi/langgraph/json": PYPI})
    text = common.dump(run(version_tools.latest_version("langgraph")))
    [source] = extract_sources("get_latest_version", text)
    assert source["url"] == "https://pypi.org/project/langgraph/" and source["version"] == "1.2.14"
    assert source["tech"] == "langgraph" and source["doc_type"] == "release" and source["title"] == "langgraph (PyPI)"


def test_compat_output_yields_one_source_per_checked_package(monkeypatch):
    info = {"info": {"requires_dist": [], "requires_python": ">=3.10"}}
    fake_fetch(monkeypatch, {"pypi.org/pypi/langchain/1.4.0/json": info, "pypi.org/pypi/mcp/2.3.0/json": info})
    text = common.dump(run(version_tools.check_compat(["langchain==1.4.0", "mcp==2.3.0"])))
    sources = extract_sources("check_version_compat", text)
    assert [(s["title"], s["tech"], s["version"]) for s in sources] == [("langchain==1.4.0 (PyPI)", "langchain", "1.4.0"), ("mcp==2.3.0 (PyPI)", "mcp", "2.3.0")]
    assert all(s["url"].startswith("https://pypi.org/project/") for s in sources)


# ---------------------------------------------------------------- 그 밖의 경우
def test_tools_without_web_sources_return_nothing():
    text = json.dumps({"symbol": "langgraph.graph.StateGraph", "exists": True})
    assert extract_sources("check_symbol_exists", text) == []


def test_server_prefixed_tool_names_are_understood():
    text = json.dumps({"package": "mcp", "latest_version": "2.3.0", "url": "https://pypi.org/project/mcp/"})
    assert extract_sources("dev_helper__get_latest_version", text)[0]["tech"] == "mcp"


@pytest.mark.parametrize(
    "tool, text",
    [
        ("unknown_tool", '{"url": "https://x.com"}'),
        ("get_latest_version", ""),
        ("get_latest_version", None),
        ("get_latest_version", "그냥 글입니다"),
        ("get_latest_version", '{"package": "x", "url": "https://pypi.org/p'),  # 길이 제한으로 잘린 JSON
        ("get_latest_version", "[1, 2, 3]"),
        ("search_github_issues", '{"issues": "not a list"}'),
        ("search_github_issues", '{"issues": [5, null, {"title": "주소 없음"}]}'),
        (None, "{}"),
    ],
)
def test_unreadable_output_gives_no_sources_without_errors(tool, text):
    assert extract_sources(tool, text) == []
