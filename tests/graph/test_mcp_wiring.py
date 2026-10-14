"""
메인 그래프(src/graph/workflow.py)에 MCP가 연결된 모양 확인. Supervisor, RAG, 답변 노드는 가짜로 바꿔 끼우고, 연결(노드 등록, 되돌아오는 선, 완료 목록)만 본다.
진짜 모델로 Supervisor가 mcp를 고르는지는 test_routing_live.py (RUN_LIVE_TESTS=1)에서 본다.
"""

import os
from types import SimpleNamespace

import pytest
from langchain_core.messages import AIMessage

# 노드 파일들이 import할 때 모델 객체를 만들어서 키 값이 필요하다 (이 시험은 모델을 부르지 않는다)
os.environ.setdefault("OPENAI_API_KEY", "test-key-not-real")

import src.const.models as models  # noqa: E402


class _StubReranker:
    def predict(self, pairs):
        return [0.0 for _ in pairs]


# 리랭커 모델(약 2GB)을 내려받거나 불러오지 않게, workflow를 처음 import할 때만 대역으로 바꿔 둔다
_real_create_rerank = models.create_rerank
models.create_rerank = lambda: _StubReranker()
try:
    import src.graph.workflow as workflow_module  # noqa: E402
finally:
    models.create_rerank = _real_create_rerank

import src.agent.mcp_agent as mcp_agent_module  # noqa: E402


class FakeSupervisor:
    """script: 호출마다 고를 route 목록. 호출할 때 보게 된 completed_routes도 기록한다."""

    def __init__(self, script):
        self.script, self.seen = list(script), []

    def __call__(self, state):
        self.seen.append(list(state.get("completed_routes") or []))
        return {"route": self.script.pop(0), "reason": "test"}


def answer_node(state):
    return {"answer": "최종 답변", "messages": [AIMessage(content="최종 답변")]}


def build(monkeypatch, supervisor, mcp=None):
    monkeypatch.setattr(workflow_module, "supervisor_node", supervisor)
    monkeypatch.setattr(workflow_module, "general_agent", lambda: (lambda state: {}))
    monkeypatch.setattr(workflow_module, "answer_agent", lambda: answer_node)
    monkeypatch.setattr(workflow_module, "rag_node", lambda state: {"retrieved_docs": [], "completed_routes": [*(state.get("completed_routes") or []), "rag"]})
    if mcp is not None:
        monkeypatch.setattr(workflow_module, "mcp_node", mcp)
    return workflow_module.workflow()


def initial(question="langgraph 최신 버전 알려줘"):
    return {"messages": [{"role": "user", "content": question}], "original_question": question, "image": None, "image_analysis": "", "retrieved_docs": [], "mcp_results": [], "answer": ""}


def run(graph, thread="t"):
    # 그래프에 checkpointer가 없어서(workflow에서 InMemorySaver를 뺐다) get_state를 쓸 수 없다. 노드가 돌려준 갱신을 차례로 모아 최종 상태를 만든다.
    path, result = [], dict(initial())
    for chunk in graph.stream(initial(), config={"configurable": {"thread_id": thread}}, stream_mode="updates"):
        for node, update in chunk.items():
            path.append(node)
            if isinstance(update, dict):
                result.update(update)
    return path, result


def test_mcp_is_registered_and_the_loop_returns_to_the_supervisor(monkeypatch):
    graph = build(monkeypatch, FakeSupervisor(["mcp", "answer"]), mcp=lambda state: {"mcp_results": [{"status": "success"}], "completed_routes": ["mcp"]})
    path, result = run(graph)
    assert path == ["reset_turn_state", "supervisor", "mcp", "supervisor", "answer"]
    assert result["answer"] == "최종 답변" and result["mcp_results"] == [{"status": "success"}]
    assert "mcp" in graph.get_graph().nodes  # 노드로 등록되어 있다


def test_rag_then_mcp_then_answer(monkeypatch):
    mcp = lambda state: {"mcp_results": [{"status": "success"}], "completed_routes": [*(state.get("completed_routes") or []), "mcp"]}  # noqa: E731
    supervisor = FakeSupervisor(["rag", "mcp", "answer"])
    path, _ = run(build(monkeypatch, supervisor, mcp=mcp))
    assert path == ["reset_turn_state", "supervisor", "rag", "supervisor", "mcp", "supervisor", "answer"]
    assert supervisor.seen == [[], ["rag"], ["rag", "mcp"]]  # Supervisor가 끝낸 route를 볼 수 있다


def test_the_real_mcp_node_reports_itself_as_completed(monkeypatch):
    """진짜 mcp_node가 completed_routes에 "mcp"를 더해서, Supervisor가 다음 호출에서 MCP가 끝난 것을 안다."""
    monkeypatch.setattr(mcp_agent_module, "mcp_agent", lambda: SimpleNamespace(invoke=lambda state: {"mcp_results": [{"status": "success", "tool": "get_latest_version"}]}))
    supervisor = FakeSupervisor(["mcp", "answer"])
    path, result = run(build(monkeypatch, supervisor, mcp=mcp_agent_module.mcp_node))
    assert path == ["reset_turn_state", "supervisor", "mcp", "supervisor", "answer"]
    assert supervisor.seen[1] == ["mcp"]
    assert result["mcp_results"][0]["tool"] == "get_latest_version"


def test_unexpected_mcp_failure_does_not_stop_the_answer(monkeypatch):
    def broken():
        raise RuntimeError("boom")

    monkeypatch.setattr(mcp_agent_module, "mcp_agent", broken)
    supervisor = FakeSupervisor(["mcp", "answer"])
    _, result = run(build(monkeypatch, supervisor, mcp=mcp_agent_module.mcp_node))
    assert result["answer"] == "최종 답변"  # 질문 전체가 실패하지 않는다
    assert result["mcp_results"][-1]["status"] == "failed" and supervisor.seen[1] == ["mcp"]


def test_each_turn_starts_without_old_mcp_results(monkeypatch):
    """같은 대화의 다음 질문에서는 이전 질문의 MCP 결과와 완료 목록이 비워진다 (reset_turn_state)."""
    mcp = lambda state: {"mcp_results": [{"status": "success"}], "completed_routes": [*(state.get("completed_routes") or []), "mcp"]}  # noqa: E731
    supervisor = FakeSupervisor(["mcp", "answer", "answer"])
    graph = build(monkeypatch, supervisor, mcp=mcp)
    run(graph, thread="same")
    graph.invoke(initial("다음 질문"), config={"configurable": {"thread_id": "same"}})
    assert supervisor.seen[-1] == []  # 두 번째 질문의 첫 Supervisor 호출 때 완료 목록이 비어 있다


def test_multi_modal_route_returns_to_supervisor_and_is_recorded(monkeypatch):
    """supervisor가 multi_modal → rag → answer로 고르면 multi_modal 노드를 거쳐 supervisor로 돌아오고 completed_routes에 남는다."""
    supervisor = FakeSupervisor(["multi_modal", "rag", "answer"])
    monkeypatch.setattr(workflow_module, "multi_modal_node", lambda state: {"image_analysis": "읽음", "completed_routes": [*(state.get("completed_routes") or []), "multi_modal"]})
    graph = build(monkeypatch, supervisor)
    path, result = run(graph)
    assert path[:5] == ["reset_turn_state", "supervisor", "multi_modal", "supervisor", "rag"]
    assert supervisor.seen[1] == ["multi_modal"] and supervisor.seen[2] == ["multi_modal", "rag"]
    assert result["image_analysis"] == "읽음"
