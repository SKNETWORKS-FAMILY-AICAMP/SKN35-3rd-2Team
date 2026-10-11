"""
우리 MCP 서버의 도구 5개 시험. 외부 API(PyPI, GitHub)는 가짜 응답으로 바꿔 끼워서 네트워크 없이 돈다.
(심볼 확인은 실제로 설치된 langgraph, mcp를 쓴다.)
실행: uv run pytest tests/mcp_integration/test_tools.py -q
"""

import asyncio
import email.message
import json
import urllib.error
from urllib.parse import unquote

import pytest
from mcp import Client
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from src.const import mcp_config as cfg
from src.mcp_integration.server.tools import common, github_tools, register_all, symbol_tools, version_tools


@pytest.fixture(autouse=True)
def clear_cache():
    common._CACHE.clear()


def run(coro):
    return asyncio.run(coro)


def fake_fetch(monkeypatch, routes: dict):
    """URL에 키가 들어 있으면 그 값을 돌려준다 (값이 예외면 던진다). 호출한 URL을 기록해 돌려준다."""
    calls: list[str] = []

    async def fetch(url, **kwargs):
        calls.append(url)
        for key, value in routes.items():
            if key in url:
                if isinstance(value, Exception):
                    raise value
                return value
        raise AssertionError(f"예상하지 못한 요청: {url}")

    monkeypatch.setattr(common, "fetch_json", fetch)
    return calls


# ================================================================ common.fetch_json
def http_error(code, headers=None):
    msg = email.message.Message()
    for k, v in (headers or {}).items():
        msg[k] = v
    return urllib.error.HTTPError("https://x", code, "err", msg, None)


def patch_fetch(monkeypatch, outcome):
    calls = []

    def _fetch(url, headers):
        calls.append(url)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    monkeypatch.setattr(common, "_fetch", _fetch)
    return calls


def test_fetch_json_returns_data_and_caches(monkeypatch):
    calls = patch_fetch(monkeypatch, {"ok": 1})
    assert run(common.fetch_json("https://x/a")) == {"ok": 1}
    assert run(common.fetch_json("https://x/a")) == {"ok": 1}
    assert len(calls) == 1  # 같은 요청은 기억해 둔다


@pytest.mark.parametrize(
    "error, expected",
    [
        (http_error(404), "찾을 수 없습니다"),
        (http_error(500), "HTTP 500"),
        (urllib.error.URLError("no network"), "연결하지 못했습니다"),
        (TimeoutError(), "연결하지 못했습니다"),
    ],
)
def test_fetch_json_errors_become_readable_tool_errors(monkeypatch, error, expected):
    patch_fetch(monkeypatch, error)
    with pytest.raises(ToolError, match=expected):
        run(common.fetch_json("https://x/b", what="테스트"))


def test_fetch_json_rate_limit_message_has_reset_time(monkeypatch):
    patch_fetch(monkeypatch, http_error(403, {"X-RateLimit-Reset": "1760000000"}))
    with pytest.raises(ToolError, match=r"요청 제한.*2025-10-09 08:53:20 UTC"):
        run(common.fetch_json("https://x/c", what="GitHub"))


def test_failed_requests_are_not_cached(monkeypatch):
    calls = patch_fetch(monkeypatch, http_error(500))
    for _ in range(2):
        with pytest.raises(ToolError):
            run(common.fetch_json("https://x/d"))
    assert len(calls) == 2


# ================================================================ get_latest_version
def pypi_data():
    def files(at, yanked=False):
        return [{"upload_time_iso_8601": at, "yanked": yanked}]

    return {
        "info": {
            "name": "langgraph",
            "version": "1.2.14",
            "requires_python": ">=3.10",
            "summary": "Building stateful agents",
            "project_urls": {"Source": "https://github.com/langchain-ai/langgraph", "Twitter": "https://x.com/y", "Changelog": "https://c"},
        },
        "releases": {
            "1.2.13": files("2026-09-20T00:00:00Z"),
            "1.2.14": files("2026-10-01T00:00:00.5Z"),
            "1.3.0rc1": files("2026-10-05T00:00:00Z"),  # 시험판은 최신이 아니다
            "1.2.15": files("2026-10-06T00:00:00Z", yanked=True),  # 철회된 버전도 아니다
            "not-a-version": files("2026-01-01T00:00:00Z"),
            "0.0.1": [],
        },
        "urls": [],
    }


def test_latest_version_picks_latest_stable_and_shapes_result(monkeypatch):
    fake_fetch(monkeypatch, {"pypi.org/pypi/langgraph/json": pypi_data()})
    result = run(version_tools.latest_version("langgraph"))
    assert result["latest_version"] == "1.2.14" and result["released_at"] == "2026-10-01T00:00:00.5Z"
    assert [v["version"] for v in result["recent_versions"]] == ["1.2.14", "1.2.13"]
    assert result["links"] == {"Changelog": "https://c", "Source": "https://github.com/langchain-ai/langgraph"}
    assert result["requires_python"] == ">=3.10" and result["source"] == "PyPI"
    assert result["url"] == "https://pypi.org/project/langgraph/" and result["retrieved_at"].endswith("+00:00")


def test_latest_version_with_only_prereleases_falls_back_to_pypi_latest(monkeypatch):
    data = {"info": {"name": "x", "version": "0.1.0a1"}, "releases": {"0.1.0a1": [{"upload_time_iso_8601": "2026-01-01T00:00:00Z"}]}, "urls": []}
    fake_fetch(monkeypatch, {"pypi.org/pypi/x/json": data})
    result = run(version_tools.latest_version("x"))
    assert result["latest_version"] == "0.1.0a1" and result["recent_versions"] == []


@pytest.mark.parametrize("name", ["", "../etc", "a b", "-x", "x" * 101, "a/b"])
def test_latest_version_rejects_bad_names_without_requests(monkeypatch, name):
    calls = fake_fetch(monkeypatch, {})
    with pytest.raises(ToolError, match="올바른 패키지 이름"):
        run(version_tools.latest_version(name))
    assert calls == []


def test_latest_version_unknown_package_passes_the_reason(monkeypatch):
    fake_fetch(monkeypatch, {"pypi.org": ToolError("PyPI에서 찾을 수 없습니다 (404).")})
    with pytest.raises(ToolError, match="찾을 수 없습니다"):
        run(version_tools.latest_version("no-such-package-xyz"))


# ================================================================ check_version_compat
def info(requires_dist=(), requires_python=">=3.10"):
    return {"info": {"requires_dist": list(requires_dist), "requires_python": requires_python}}


LANGCHAIN_DEPS = [
    "langchain-core<2.0.0,>=1.6.0",
    "langgraph<1.3.0,>=1.2.11",
    "pydantic>=2.7",
    "langgraph-sdk>=0.1; extra == 'sdk'",
]


def compat_routes(**extra):
    releases = {v: [{"upload_time_iso_8601": "2026-01-01T00:00:00Z"}] for v in ("1.2.10", "1.2.11", "1.2.14", "1.3.0", "1.3.1rc1")}
    routes = {
        "pypi.org/pypi/langchain/1.4.0/json": info(LANGCHAIN_DEPS),
        "pypi.org/pypi/langgraph/0.2.0/json": info(["langchain-core>=0.2"], ">=3.9"),
        "pypi.org/pypi/langgraph/1.2.14/json": info([]),
        "pypi.org/pypi/langgraph/json": {"info": {}, "releases": releases},
    }
    routes.update(extra)
    return routes


def test_compat_finds_conflict_and_suggests_a_version(monkeypatch):
    fake_fetch(monkeypatch, compat_routes())
    result = run(version_tools.check_compat(["langchain==1.4.0", "langgraph==0.2.0"]))
    assert result["compatible"] is False
    assert result["conflicts"] == [
        {"package": "langgraph==0.2.0", "required_by": "langchain==1.4.0", "requirement": "langgraph<1.3.0,>=1.2.11"}
    ]
    suggestion = result["suggestions"][0]
    assert suggestion["package"] == "langgraph" and suggestion["suggested_version"] == "1.2.14"  # 1.3.0과 시험판은 조건 밖
    assert "langchain==1.4.0: <1.3.0,>=1.2.11" in suggestion["satisfies"][0]
    assert result["sources"][0] == "https://pypi.org/project/langchain/1.4.0/" and result["retrieved_at"]


def test_compat_ok_when_versions_fit(monkeypatch):
    fake_fetch(monkeypatch, compat_routes())
    result = run(version_tools.check_compat(["langchain==1.4.0", "langgraph==1.2.14"], "3.12"))
    assert result["compatible"] is True and result["conflicts"] == [] and result["suggestions"] == []
    assert result["python_version"] == "3.12" and result["python_problems"] == []


def test_compat_only_checks_packages_the_user_listed_and_ignores_extras(monkeypatch):
    fake_fetch(monkeypatch, compat_routes())
    # langchain-core, pydantic은 목록에 없으므로 검사하지 않고, extra 전용 조건(langgraph-sdk)은 무시한다
    result = run(version_tools.check_compat(["langchain==1.4.0"]))
    assert result["compatible"] is True and result["checked_packages"] == ["langchain==1.4.0"]


def test_compat_reports_python_version_problem(monkeypatch):
    fake_fetch(monkeypatch, compat_routes())
    result = run(version_tools.check_compat(["langchain==1.4.0"], "3.9"))
    assert result["compatible"] is False
    assert result["python_problems"] == [{"package": "langchain==1.4.0", "requires_python": ">=3.10", "python_version": "3.9"}]


def test_compat_environment_markers_depend_on_python_version(monkeypatch):
    marked = info(["langgraph>=2.0; python_version >= '3.11'"])
    fake_fetch(monkeypatch, {"pypi.org/pypi/a/1.0/json": marked, "pypi.org/pypi/langgraph/1.2.14/json": info([]), "pypi.org/pypi/langgraph/json": {"releases": {}}})
    on_311 = run(version_tools.check_compat(["a==1.0", "langgraph==1.2.14"], "3.11"))
    on_310 = run(version_tools.check_compat(["a==1.0", "langgraph==1.2.14"], "3.10"))
    assert on_311["compatible"] is False and on_310["compatible"] is True  # 3.10에서는 그 조건이 적용되지 않는다
    assert on_311["suggestions"][0]["suggested_version"] is None  # 조건을 만족하는 버전이 없을 때


def test_compat_unresolved_package_is_reported_but_others_are_checked(monkeypatch):
    fake_fetch(monkeypatch, compat_routes(**{"pypi.org/pypi/ghost/9.9/json": ToolError("PyPI에서 찾을 수 없습니다 (404).")}))
    result = run(version_tools.check_compat(["langchain==1.4.0", "ghost==9.9"]))
    assert result["checked_packages"] == ["langchain==1.4.0"]
    assert result["unresolved"] == [{"package": "ghost==9.9", "reason": "PyPI에서 찾을 수 없습니다 (404)."}]


def test_compat_fails_when_nothing_could_be_checked(monkeypatch):
    fake_fetch(monkeypatch, {"pypi.org": ToolError("PyPI에서 찾을 수 없습니다 (404).")})
    with pytest.raises(ToolError, match="하나도 PyPI에서 확인하지 못했습니다"):
        run(version_tools.check_compat(["ghost==9.9"]))


@pytest.mark.parametrize(
    "packages, message",
    [
        ([], "비어 있지 않은 목록"),
        ("langchain==1.4.0", "비어 있지 않은 목록"),
        (["langchain"], "'패키지==버전' 형태가 아닙니다"),
        (["langchain==abc"], "형태가 아닙니다|올바르지 않습니다"),
        (["langchain==1.0", "langchain==2.0"], "두 번 들어 있습니다"),
        ([f"p{i}==1.0" for i in range(cfg.COMPAT_MAX_PACKAGES + 1)], "까지만 점검"),
    ],
)
def test_compat_rejects_bad_input_without_requests(monkeypatch, packages, message):
    calls = fake_fetch(monkeypatch, {})
    with pytest.raises(ToolError, match=message):
        run(version_tools.check_compat(packages))
    assert calls == []


def test_compat_rejects_bad_python_version(monkeypatch):
    fake_fetch(monkeypatch, {})
    with pytest.raises(ToolError, match="python_version"):
        run(version_tools.check_compat(["langchain==1.4.0"], "python3.12"))


def test_parse_pins_normalizes_names_and_accepts_space_form():
    assert version_tools.parse_pins(["Lang_Chain==1.4.0", "langgraph 1.2.14"]) == {"lang-chain": "1.4.0", "langgraph": "1.2.14"}


# ================================================================ GitHub 이슈
SEARCH = {
    "total_count": 18,
    "items": [
        {
            "repository_url": "https://api.github.com/repos/langchain-ai/langgraph",
            "number": 9163,
            "title": "GraphRecursionError raised after the graph already finished",
            "state": "open",
            "html_url": "https://github.com/langchain-ai/langgraph/issues/9163",
            "labels": [{"name": "bug"}, {"name": "pending"}],
            "comments": 3,
            "created_at": "2026-10-01T00:00:00Z",
            "updated_at": "2026-10-02T00:00:00Z",
            "body": "x" * 1000,
        }
    ],
}


def test_search_issues_shapes_results_and_builds_a_safe_query(monkeypatch):
    calls = fake_fetch(monkeypatch, {"search/issues": SEARCH})
    result = run(github_tools.search_issues("GraphRecursionError", state="open", limit=3))
    url = unquote(calls[0])
    assert "q=GraphRecursionError is:issue state:open repo:langchain-ai/langchain repo:langchain-ai/langgraph repo:modelcontextprotocol/python-sdk" in url
    assert url.endswith("per_page=3")
    issue = result["issues"][0]
    assert issue["repo"] == "langchain-ai/langgraph" and issue["number"] == 9163 and issue["labels"] == ["bug", "pending"]
    assert issue["url"].endswith("/issues/9163") and len(issue["snippet"]) <= cfg.GITHUB_SNIPPET_CHARS + len(cfg.CLIP_SUFFIX)
    assert result["total_count"] == 18 and result["returned"] == 1 and result["source"] == "GitHub Search API"
    assert result["retrieved_at"] and "get_github_issue" in result["note"]


def test_search_issues_limits_to_one_repo_and_all_states(monkeypatch):
    calls = fake_fetch(monkeypatch, {"search/issues": {"total_count": 0, "items": []}})
    result = run(github_tools.search_issues("nothing", repo="langchain-ai/langgraph"))
    url = unquote(calls[0])
    assert "repo:langchain-ai/langgraph" in url and "repo:langchain-ai/langchain " not in url and "state:" not in url
    assert result["issues"] == [] and "검색 결과가 없습니다" in result["note"]


@pytest.mark.parametrize(
    "query, expected",
    [
        ("repo:evil/other is:pr foo", "repo evil/other is pr foo"),  # 다른 저장소를 검색하게 만드는 한정자를 막는다
        ("-label:bug org:x", "label bug org x"),
        ("ModuleNotFoundError: No module named 'langgraph.prebuilt'", "ModuleNotFoundError: No module named 'langgraph.prebuilt'"),
        ("langgraph.errors.GraphRecursionError: Recursion limit of 25", "langgraph.errors.GraphRecursionError: Recursion limit of 25"),
    ],
)
def test_sanitize_query_neutralizes_search_qualifiers(query, expected):
    assert github_tools.sanitize_query(query) == expected


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"query": "  "}, "query가 비어 있습니다"),
        ({"query": "x" * 257}, "256자 이하"),
        ({"query": "a", "repo": "torvalds/linux"}, "조회할 수 없는 저장소.*langchain-ai/langgraph"),
        ({"query": "a", "state": "merged"}, "state는"),
        ({"query": "a", "limit": 0}, "limit는"),
        ({"query": "a", "limit": cfg.GITHUB_SEARCH_MAX_RESULTS + 1}, "limit는"),
    ],
)
def test_search_issues_rejects_bad_input_without_requests(monkeypatch, kwargs, message):
    calls = fake_fetch(monkeypatch, {})
    with pytest.raises(ToolError, match=message):
        run(github_tools.search_issues(**kwargs))
    assert calls == []


ISSUE = {
    "title": "GraphRecursionError raised after the graph already finished",
    "state": "closed",
    "state_reason": "completed",
    "html_url": "https://github.com/langchain-ai/langgraph/issues/9163",
    "user": {"login": "reporter"},
    "labels": [{"name": "bug"}],
    "created_at": "2026-10-01T00:00:00Z",
    "closed_at": "2026-10-03T00:00:00Z",
    "body": "본문 " * 2000,
    "comments": 2,
}
COMMENTS = [
    {"user": {"login": "maintainer"}, "author_association": "MEMBER", "created_at": "2026-10-02T00:00:00Z", "html_url": "https://github.com/c1", "body": "fixed in 1.2.15"},
    {"user": None, "author_association": "NONE", "created_at": "2026-10-02T01:00:00Z", "html_url": "https://github.com/c2", "body": "y" * 5000},
]


def test_get_issue_returns_body_and_comments_with_limits(monkeypatch):
    calls = fake_fetch(monkeypatch, {"/issues/9163/comments": COMMENTS, "/issues/9163": ISSUE})
    result = run(github_tools.get_issue("langchain-ai/langgraph", 9163, 2))
    assert result["state"] == "closed" and result["state_reason"] == "completed" and result["is_pull_request"] is False
    assert result["author"] == "reporter" and result["labels"] == ["bug"] and result["comments_total"] == 2
    assert len(result["body"]) <= cfg.GITHUB_ISSUE_BODY_CHARS + len(cfg.CLIP_SUFFIX)
    first, second = result["comments"]
    assert first["author_association"] == "MEMBER" and first["body"] == "fixed in 1.2.15"
    assert second["author"] is None and len(second["body"]) <= cfg.GITHUB_COMMENT_CHARS + len(cfg.CLIP_SUFFIX)
    assert any("per_page=2" in c for c in calls) and result["retrieved_at"]


def test_get_issue_skips_comment_request_when_not_needed(monkeypatch):
    calls = fake_fetch(monkeypatch, {"/issues/9163": {**ISSUE, "comments": 0}})
    assert run(github_tools.get_issue("langchain-ai/langgraph", 9163, 5))["comments"] == []
    calls_zero = fake_fetch(monkeypatch, {"/issues/9163": ISSUE})
    assert run(github_tools.get_issue("langchain-ai/langgraph", 9163, 0))["comments"] == []
    assert len(calls) == 1 and len(calls_zero) == 1


def test_get_issue_flags_pull_requests(monkeypatch):
    fake_fetch(monkeypatch, {"/issues/5": {**ISSUE, "comments": 0, "pull_request": {"url": "x"}}})
    assert run(github_tools.get_issue("langchain-ai/langchain", 5, 0))["is_pull_request"] is True


@pytest.mark.parametrize(
    "args, message",
    [
        (("evil/repo", 1, 5), "조회할 수 없는 저장소"),
        (("langchain-ai/langgraph", 0, 5), "number는"),
        (("langchain-ai/langgraph", "9", 5), "number는"),
        (("langchain-ai/langgraph", 1, -1), "max_comments는"),
        (("langchain-ai/langgraph", 1, cfg.GITHUB_MAX_COMMENTS + 1), "max_comments는"),
    ],
)
def test_get_issue_rejects_bad_input_without_requests(monkeypatch, args, message):
    calls = fake_fetch(monkeypatch, {})
    with pytest.raises(ToolError, match=message):
        run(github_tools.get_issue(*args))
    assert calls == []


def test_get_issue_not_found_passes_the_reason(monkeypatch):
    fake_fetch(monkeypatch, {"/issues/99999999": ToolError("langchain-ai/langgraph #99999999에서 찾을 수 없습니다 (404).")})
    with pytest.raises(ToolError, match="찾을 수 없습니다"):
        run(github_tools.get_issue("langchain-ai/langgraph", 99999999, 0))


# ================================================================ 심볼 존재 확인 (실제 설치된 패키지)
def test_symbol_exists_with_kind_signature_and_version():
    result = symbol_tools.resolve_symbol("langgraph.graph.StateGraph")
    assert result["exists"] is True and result["kind"] == "class" and result["installed_package_version"]
    assert result["signature"].startswith("(") and result["retrieved_at"]


def test_symbol_exists_for_modules_and_lazy_submodules():
    assert symbol_tools.resolve_symbol("langgraph.graph")["kind"] == "module"
    assert symbol_tools.resolve_symbol("mcp.Client")["exists"] is True
    assert symbol_tools.resolve_symbol("langgraph.checkpoint.memory.InMemorySaver")["exists"] is True  # 아직 불러오지 않은 하위 모듈


def test_missing_symbol_suggests_similar_names():
    result = symbol_tools.resolve_symbol("langgraph.graph.StateGrap")
    assert result["exists"] is False and result["resolved_up_to"] == "langgraph.graph" and result["missing"] == "StateGrap"
    assert "StateGraph" in result["similar_names"] and "설치된 버전 기준" in result["note"]


def test_invented_function_does_not_exist():
    result = symbol_tools.resolve_symbol("langgraph.graph.magic_autofix_everything")  # 평가표 E07의 예
    assert result["exists"] is False and result["similar_names"] == []


def test_missing_package_part_is_reported_where_it_stops():
    result = symbol_tools.resolve_symbol("langgraph.nonexistent.thing")
    assert result["exists"] is False and result["resolved_up_to"] == "langgraph" and result["missing"] == "nonexistent"


@pytest.mark.parametrize(
    "symbol, message",
    [
        ("os.system", "확인할 수 없습니다.*langgraph"),  # 허용 목록 밖의 패키지는 불러오지 않는다
        ("subprocess.run", "확인할 수 없습니다"),
        ("langgraph..x", "올바른 심볼 이름이 아닙니다"),
        ("langgraph.graph; import os", "올바른 심볼 이름이 아닙니다"),
        ("", "올바른 심볼 이름이 아닙니다"),
    ],
)
def test_symbol_rejects_disallowed_or_malformed_names(symbol, message):
    with pytest.raises(ToolError, match=message):
        symbol_tools.resolve_symbol(symbol)


# ================================================================ 서버에 등록된 도구 (모델이 보는 모습)
def test_all_tools_register_with_model_facing_descriptions():
    server = MCPServer("t")
    register_all(server)

    async def listing():
        async with Client(server) as client:
            return (await client.list_tools()).tools

    tools = {t.name: t for t in run(listing())}
    assert set(tools) == {"get_latest_version", "check_version_compat", "search_github_issues", "get_github_issue", "check_symbol_exists"}
    assert len(tools) <= 6  # 모델이 도구를 고를 때 헷갈리지 않도록 많지 않게 둔다
    for tool in tools.values():
        assert len(tool.description) > 60, tool.name  # "언제 쓰는지"를 설명한다
        assert tool.input_schema["type"] == "object"
    assert tools["search_github_issues"].input_schema["required"] == ["query"]
    assert tools["check_version_compat"].input_schema["required"] == ["packages"]


def test_registered_tool_returns_json_text_through_the_mcp_client(monkeypatch):
    fake_fetch(monkeypatch, {"pypi.org/pypi/langgraph/json": pypi_data()})
    server = MCPServer("t")
    register_all(server)

    async def call(name, args):
        async with Client(server) as client:
            return await client.call_tool(name, args)

    ok = run(call("get_latest_version", {"package": "langgraph"}))
    assert not ok.is_error and json.loads(ok.content[0].text)["latest_version"] == "1.2.14"
    bad = run(call("get_latest_version", {"package": "../x"}))
    assert bad.is_error and "올바른 패키지 이름" in bad.content[0].text  # ToolError의 이유가 모델에게 전달된다
    sym = run(call("check_symbol_exists", {"symbol": "langgraph.graph.StateGraph"}))
    assert json.loads(sym.content[0].text)["exists"] is True
