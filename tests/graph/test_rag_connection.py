from types import SimpleNamespace
from unittest.mock import Mock

from langchain_core.documents import Document
from langchain_core.messages import AIMessage

from src.graph.chat_service import run_chat
from src.graph.node.answer.answer_node import cited_sources


def setup_graph(monkeypatch, documents):
    from src.graph.node import supervisor_node as supervisor
    from src.graph.node import rag_node as rag
    from src.graph.node.answer import answer_node as answer
    from src.graph.workflow import workflow
    router = Mock()
    router.with_structured_output.return_value.invoke.return_value = SimpleNamespace(route="rag", reason="docs")
    model = Mock()
    model.invoke.return_value = AIMessage(content="State는 공유 상태입니다. [1]")
    monkeypatch.setattr(supervisor, "create_openai_model", lambda **_: router)
    monkeypatch.setattr(answer, "create_openai_model", lambda **_: model)
    search = Mock(return_value=documents)
    monkeypatch.setattr(rag, "search_documents", search)
    return workflow(), search, model


def test_retrieved_content_reaches_answer_and_returns_real_source(monkeypatch):
    docs = [Document(page_content="State is shared graph data", metadata={
        "source_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "title": "Graph API", "technology": "langgraph", "document_type": "documentation",
    })]
    graph, search, model = setup_graph(monkeypatch, docs)
    messages = [{"role": "user", "content": "LangGraph 공부 중"},
        {"role": "assistant", "content": "좋아요"}, {"role": "user", "content": "State는?"}]
    result = run_chat(messages, graph=graph)
    assert result["status"] == "success" and result["sources"][0]["url"] == docs[0].metadata["source_url"]
    assert "State is shared graph data" in model.invoke.call_args.args[0][-1]["content"]
    assert search.call_args.args[0] == "State는?"
    assert len(search.call_args.args[1]) == 2


def test_no_results_does_not_generate_unsupported_facts(monkeypatch):
    graph, search, model = setup_graph(monkeypatch, [])
    result = run_chat([{"role": "user", "content": "없는 API 사용법"}], graph=graph)
    assert result["status"] == "success" and "근거를 찾지 못했습니다" in result["answer"]
    assert result["sources"] == []
    model.invoke.assert_not_called()


def test_search_failure_stops_before_answer_and_hides_exception(monkeypatch):
    graph, search, model = setup_graph(monkeypatch, [])
    search.side_effect = RuntimeError("secret-key")
    result = run_chat([{"role": "user", "content": "State는?"}], graph=graph)
    assert result["error"]["code"] == "RAG_ERROR" and "secret-key" not in str(result)
    model.invoke.assert_not_called()


def test_only_valid_cited_urls_are_returned():
    docs = [Document(page_content="A", metadata={"source_url": "https://example.com/a"}),
        Document(page_content="B", metadata={"source_url": "javascript:alert(1)"}),
        Document(page_content="C", metadata={"source_url": "https://example.com/c"})]
    result = cited_sources("Claim [1] repeated [1] invalid [2] invented [99]", docs)
    assert [s["url"] for s in result] == ["https://example.com/a"]


def test_context_budget_and_fresh_documents(monkeypatch):
    from src.graph.node import rag_node as rag
    docs = [Document(page_content="a" * 4500), Document(page_content="b" * 4500)]
    monkeypatch.setattr(rag, "search_documents", lambda *_: docs)
    result = rag.rag_node({"original_question": "query", "messages": []})
    assert sum(len(d.page_content) for d in result["retrieved_docs"]) == 6000
    assert len(docs[1].page_content) == 4500


def test_search_uses_existing_retriever_without_build(monkeypatch):
    import sys
    from src.const import config
    from src.graph.node.rag_node import search_documents
    monkeypatch.setattr(config, "PINECONE_API_KEY", "test-key")
    monkeypatch.setattr(config, "BM25_PATH", SimpleNamespace(is_file=lambda: True))
    retriever = Mock()
    retriever.invoke.return_value = []
    factory = Mock(return_value=retriever)
    # The read path must not need any index-building function.
    monkeypatch.setitem(sys.modules, "src.rag.retriever", SimpleNamespace(PineconeHybridRetriever=factory))
    history = [("user", "LangGraph 공부")]
    assert search_documents("State는?", history) == []
    assert factory.call_args.kwargs["use_query_rewrite"] is True
    assert factory.call_args.kwargs["history"] == history
    retriever.invoke.assert_called_once_with("State는?")


def test_missing_key_stops_before_search(monkeypatch):
    import pytest
    from src.const import config
    from src.graph.node.rag_node import search_documents
    monkeypatch.setattr(config, "PINECONE_API_KEY", "")
    with pytest.raises(ValueError, match="not configured"):
        search_documents("State는?", [])
