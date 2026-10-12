"""
진짜 Supervisor가 질문마다 첫 번째로 어떤 route를 고르는지 확인한다 (MCP를 연결하고 Supervisor 프롬프트에 도구 목록을 넣은 뒤의 점검).
진짜 모델을 부르므로(질문마다 1번, 몇 센트) 기본으로는 건너뛴다.

    RUN_LIVE_TESTS=1 uv run pytest tests/graph/test_routing_live.py -q -s
"""

import os

import pytest

pytestmark = pytest.mark.skipif(os.getenv("RUN_LIVE_TESTS") != "1", reason="진짜 모델을 부르는 시험이라 RUN_LIVE_TESTS=1일 때만 돈다")

# (질문, 정답으로 인정하는 첫 route들)
CASES = [
    # 지금 확인해야 하는 사실 -> mcp
    ("langgraph 최신 버전이 뭐야?", {"mcp"}),
    ("langchain 1.4.0이랑 langgraph 0.2.0 같이 써도 돼? 파이썬은 3.12야", {"mcp"}),
    ("GraphRecursionError 관련 GitHub 이슈 찾아줘", {"mcp"}),
    ("langgraph 이슈 9163번 내용 알려줘", {"mcp"}),
    ("langgraph.graph.magic_autofix_everything 함수가 있는지 확인해줘", {"mcp"}),
    ("mcp 파이썬 SDK 최신 릴리스 알려줘", {"mcp"}),
    # 개념 설명, 사용법 -> rag
    ("LangGraph에서 Node의 역할이 뭐야?", {"rag"}),
    ("StateGraph에서 checkpointer를 쓰는 방법 알려줘", {"rag"}),
    ("MCP 서버를 처음부터 만드는 방법 알려줘", {"rag"}),
    ("GraphRecursionError는 왜 발생하고 어떻게 해결해?", {"rag", "mcp"}),  # 문서와 이슈 둘 다 합리적
    # 존재하지 않는 함수의 사용법 (환각 방지): mcp로 존재를 확인하거나, rag를 거친 뒤 mcp로 확인해야 한다 (general이면 환각이 된다)
    ("langgraph.graph.magic_autofix_everything 함수 사용법 알려줘", {"mcp", "rag"}),
    # 일반 질문 -> general
    ("파이썬 리스트와 튜플의 차이를 알려줘", {"general"}),
    ("안녕하세요", {"general"}),
    ("오늘 점심 뭐 먹을까?", {"general"}),
]


def first_route(question):
    from langchain_core.messages import HumanMessage

    from src.graph.node.supervisor_node import supervisor_node

    state = {"messages": [HumanMessage(content=question)], "original_question": question, "image": None, "image_analysis": "",
             "retrieved_docs": [], "mcp_results": [], "completed_routes": []}
    return supervisor_node(state)["route"]


def test_supervisor_first_route_accuracy_live():
    results = [(q, first_route(q), ok) for q, ok in CASES]
    wrong = [(q, got, ok) for q, got, ok in results if got not in ok]
    print(f"\nSupervisor 첫 route 정확도: {len(results) - len(wrong)}/{len(results)}")
    for q, got, ok in wrong:
        print(f"  - {q!r}: 기대 {sorted(ok)} / 고른 것 {got}")
    mcp_cases = [(q, got) for q, got, ok in results if ok == {"mcp"}]
    assert all(got == "mcp" for _, got in mcp_cases), "mcp가 맞는 질문에서 mcp를 고르지 못했다"
    assert len(wrong) <= 1
