"""
도구 선택 정확도 시험.

- 위쪽 시험들은 네트워크와 모델 없이 도는 "시험 세트 점검"이다 (기본으로 같이 돈다).
- test_tool_selection_accuracy_live는 진짜 모델을 부르므로(35번 호출, 몇 센트) 기본으로는 건너뛴다. 도구 설명이나 프롬프트를 고친 뒤에 켠다.

    RUN_LIVE_TESTS=1 uv run pytest tests/mcp_integration/test_tool_selection.py -q -s     (PowerShell: $env:RUN_LIVE_TESTS=1)

  이 시험은 도구를 실제로 실행하지는 않는다. 모델이 어떤 도구와 인자를 고르는지만 본다 (GitHub, PyPI 요청 없음).
"""

import asyncio
import os
from collections import defaultdict

import pytest
from mcp import Client
from mcp.server import MCPServer

from src.graph.node.mcp.list_tools_node import assign_display_names
from src.graph.node.mcp.select_tool_node import select_tool_node
from src.mcp_integration.server.tools import register_all
from tool_selection_cases import CASES, HARD_CASES, args_match

# 이 정확도 아래로 떨어지면 도구 설명이나 프롬프트가 망가진 것으로 본다 (2026-10 측정값에서 약간 낮춰 잡았다)
MIN_TOOL_ACCURACY = 0.90
MIN_ARGS_ACCURACY = 0.85

TOOLS = ("get_latest_version", "check_version_compat", "search_github_issues", "get_github_issue", "check_symbol_exists")


def registered_tools() -> list[dict]:
    """우리 서버에 등록된 도구를 모델이 보는 모양으로 (서버를 띄우지 않고 같은 프로세스에서)."""
    server = MCPServer("selection-test")
    register_all(server)

    async def listing():
        async with Client(server) as client:
            return (await client.list_tools()).tools

    tools = [
        {"server": "dev_helper", "name": t.name, "description": t.description or "", "input_schema": t.input_schema}
        for t in asyncio.run(listing())
    ]
    return assign_display_names(tools)


# ---------------------------------------------------------------- 시험 세트 자체의 점검 (모델 호출 없음)
def test_case_ids_are_unique_and_the_set_is_big_enough():
    ids = [c.id for c in CASES]
    assert len(ids) == len(set(ids)) and len(CASES) >= 30


def test_expected_tools_exist_and_every_tool_is_covered():
    names = {t["name"] for t in registered_tools()}
    assert names == set(TOOLS)
    covered = defaultdict(int)
    for case in CASES:
        for tool in (case.expected, *case.ok_tools):
            assert tool is None or tool in names, case.id
        if case.expected:
            covered[case.expected] += 1
    assert all(covered[t] >= 3 for t in TOOLS), dict(covered)  # 도구마다 최소 3개 질문
    assert sum(1 for c in CASES if c.expected is None) >= 5  # "도구를 쓰지 않아야 하는" 질문도 충분히


def test_argument_conditions_only_exist_for_cases_with_a_tool():
    assert all(not c.args for c in CASES if c.expected is None)


def test_argument_matching_rules():
    from tool_selection_cases import contains, contains_all, eq

    assert args_match({"a": "Hello World", "n": 3, "l": ["x==1", "y==2"]}, {"a": contains("hello"), "n": eq(3), "l": contains_all("x==1", "y==2")}) == []
    assert len(args_match({"a": "x", "n": 4, "l": ["x==1"]}, {"a": contains("zzz"), "n": eq(3), "l": contains_all("x==1", "y==2")})) == 3
    assert args_match({}, {"a": eq(1)})  # 인자가 없으면 어긋남


# ---------------------------------------------------------------- 진짜 모델로 선택 정확도 측정
def select(case, tools):
    state = {"original_question": case.question, "image_analysis": case.image_analysis, "mcp_tools": tools, "mcp_attempts": 0, "mcp_failures": []}
    update = select_tool_node(state)
    call = update.get("mcp_call")
    return (call["display_name"], call["arguments"]) if call else (None, {})


def run_selection(cases=CASES):
    """모든 질문을 진짜 모델로 돌려 결과 목록을 돌려준다: [(case, 고른 도구, 인자, 도구 맞음, 인자 문제 목록), ...]"""
    tools = registered_tools()
    results = []
    for case in cases:
        tool, arguments = select(case, tools)
        accepted = {case.expected, *case.ok_tools}
        tool_ok = tool in accepted
        problems = args_match(arguments, case.args) if tool_ok and tool == case.expected and case.args else []
        results.append((case, tool, arguments, tool_ok, problems))
    return results


def summarize(results) -> str:
    by_category = defaultdict(lambda: [0, 0])
    lines = []
    for case, tool, arguments, tool_ok, problems in results:
        by_category[case.category][1] += 1
        by_category[case.category][0] += tool_ok
        if not tool_ok or problems:
            lines.append(f"  - {case.id} {case.question!r}: 기대 {case.expected} (허용 {case.ok_tools}) / 고른 것 {tool} {arguments} {problems}")
    head = [f"{name}: {ok}/{total}" for name, (ok, total) in by_category.items()]
    return "도구 선택 정확도 " + ", ".join(head) + ("\n어긋난 질문:\n" + "\n".join(lines) if lines else "\n어긋난 질문 없음")


@pytest.mark.skipif(os.getenv("RUN_LIVE_TESTS") != "1", reason="진짜 모델을 부르는 시험이라 RUN_LIVE_TESTS=1일 때만 돈다")
def test_tool_selection_accuracy_live():
    results = run_selection()
    print("\n" + summarize(results))
    tool_accuracy = sum(r[3] for r in results) / len(results)
    with_args = [r for r in results if r[0].args and r[3] and r[1] == r[0].expected]
    args_accuracy = sum(not r[4] for r in with_args) / max(len(with_args), 1)
    print(f"전체 도구 선택 {tool_accuracy:.0%}, 인자 {args_accuracy:.0%} ({len(with_args)}건)")
    assert tool_accuracy >= MIN_TOOL_ACCURACY
    assert args_accuracy >= MIN_ARGS_ACCURACY


@pytest.mark.skipif(os.getenv("RUN_LIVE_TESTS") != "1", reason="진짜 모델을 부르는 시험이라 RUN_LIVE_TESTS=1일 때만 돈다")
def test_hard_cases_report_live():
    """어려운 질문의 결과를 보고만 한다 (기준을 넘지 못해도 실패시키지 않는다). 못 하는 것의 목록을 보는 용도다."""
    results = run_selection(HARD_CASES)
    print("\n" + summarize(results))
