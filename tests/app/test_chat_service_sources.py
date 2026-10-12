"""chat_service가 그래프 결과에서 출처를 만들어 화면과 DB에 넘기는지 확인 (그래프는 가짜)."""

from types import SimpleNamespace

from langchain_core.documents import Document
from langchain_core.messages import AIMessage

from src.app.chat_service import run_chat

HISTORY = [{"role": "user", "content": "langgraph 최신 버전과 Node 설명"}]


def fake_graph(**extra):
    result = {"messages": [AIMessage(content="답변입니다")], "answer": "답변입니다", "route": "answer", **extra}
    return SimpleNamespace(invoke=lambda state, config=None: result)


DOC = Document(
    page_content="Nodes are Python functions.",
    metadata={"source_url": "https://docs.langchain.com/oss/python/langgraph/graph-api", "title": "Graph API overview", "technology": "langgraph", "document_type": "documentation", "score": 0.87},
)
MCP = {"status": "success", "tool": "get_latest_version", "sources": [{"url": "https://pypi.org/project/langgraph/", "title": "langgraph (PyPI)", "tech": "langgraph", "version": "1.2.14", "doc_type": "release"}]}


def test_rag_documents_and_mcp_results_become_sources():
    result = run_chat(HISTORY, graph=fake_graph(retrieved_docs=[DOC], mcp_results=[MCP]))
    assert result["status"] == "success" and result["answer"] == "답변입니다"
    assert [s["url"] for s in result["sources"]] == [DOC.metadata["source_url"], "https://pypi.org/project/langgraph/"]
    assert result["sources"][0]["title"] == "Graph API overview" and result["sources"][1]["version"] == "1.2.14"


def test_no_documents_or_tool_results_means_no_sources():
    assert run_chat(HISTORY, graph=fake_graph())["sources"] == []
    assert run_chat(HISTORY, graph=fake_graph(retrieved_docs=[], mcp_results=[]))["sources"] == []


def test_failed_mcp_results_are_not_sources():
    failed = {"status": "failed", "sources": [{"url": "https://example.com/x"}]}
    assert run_chat(HISTORY, graph=fake_graph(mcp_results=[failed]))["sources"] == []


def test_the_answer_is_still_returned_when_building_sources_fails(monkeypatch):
    import src.db

    def broken(*args, **kwargs):
        raise RuntimeError("source builder broke")

    monkeypatch.setattr(src.db, "build_sources", broken)
    result = run_chat(HISTORY, graph=fake_graph(retrieved_docs=[DOC]))
    assert result["status"] == "success" and result["answer"] == "답변입니다" and result["sources"] == []


def test_a_graph_that_ends_on_an_unfinished_route_is_still_reported_as_unsupported():
    """은하님의 기존 안전장치: route가 rag/mcp/multimodal로 끝난 그래프(연결이 안 끝난 경우)는 그대로 "준비 중"으로 안내한다."""
    for route in ("rag", "mcp", "multimodal"):
        result = run_chat(HISTORY, graph=fake_graph(route=route, retrieved_docs=[DOC]))
        assert result["status"] == "unsupported" and result["sources"] == []
