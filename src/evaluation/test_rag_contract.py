from unittest.mock import Mock
   # 가상적인 Graph 객체를 만들기 위해 Mock을 사용합니다. 실제 Graph 객체를 사용하지 않고 테스트를 수행할 수 있습니다.
import pytest
from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from src.app.chat_service import run_chat, document_sources


def test_final_rag_documents_return_as_references():
    graph = Mock()
    graph.invoke.return_value = {
        "route": "answer", "messages": [AIMessage(content="fallback")],
        "answer": "문서 기반 답변",
        "retrieved_docs": [Document(page_content="종료 조건", metadata={
            "source_url": "https://docs.example.org/graph", "technology": "langgraph",
            "document_type": "documentation", "title": "Graph API", "rerank_score": 0.8})],
    }
    result = run_chat([{"role": "user", "content": "종료 방법"}], graph=graph)
    assert result["status"] == "success" and result["answer"] == "문서 기반 답변"
    assert result["sources"] == [{"url": "https://docs.example.org/graph",
        "tech": "langgraph", "doc_type": "documentation", "title": "Graph API",
        "snippet": "종료 조건", "score": 0.8}]
    assert "is_grounded" not in result["sources"][0]
    assert "version" not in result["sources"][0]


def test_missing_invalid_and_duplicate_urls_do_not_break_answer():
    docs = [Document(page_content="text", metadata=metadata) for metadata in (
        {"source": "data/raw/local.mdx"}, {"source_url": "javascript:alert(1)"},
        {"source_url": "https://docs.example.org/a", "score": float("nan")},
        {"source_url": "https://docs.example.org/a"},
        {"github_url": "https://github.com/example/docs"},
    )]
    sources = document_sources(docs)
    assert len(sources) == 2 and "score" not in sources[0]
    graph = Mock()
    graph.invoke.return_value = {"route": "answer", "messages": [AIMessage(content="資料なし")], "retrieved_docs": []}
    assert run_chat([{"role": "user", "content": "質問"}], graph=graph)["sources"] == []


@pytest.mark.parametrize("route", ["mcp", "multi_modal"])
def test_unconnected_routes_stay_unsupported(route):
    graph = Mock()
    graph.invoke.side_effect = KeyError(route)
    assert run_chat([{"role": "user", "content": "質問"}], graph=graph)["status"] == "unsupported"


def test_rag_internal_key_error_is_not_misreported_as_pending():
    graph = Mock()
    graph.invoke.side_effect = KeyError("rag")
    assert run_chat([{"role": "user", "content": "質問"}], graph=graph)["error"]["code"] == "GRAPH_ERROR"


def test_recursion_error_has_specific_safe_notice():
    from langgraph.errors import GraphRecursionError
    graph = Mock()
    graph.invoke.side_effect = GraphRecursionError("private-question-secret")
    result = run_chat([{"role": "user", "content": "재검색 종료 확인"}], graph=graph)
    assert result["status"] == "error"
    assert result["error"]["code"] == "GRAPH_RECURSION_LIMIT"
    assert "종료 조건" in result["error"]["message"]
    assert "private-question-secret" not in str(result)
    assert not result["answer"] and not result["sources"]


def test_team_source_limits_and_masking_are_used():
    from src.const.db_config import SOURCES_MAX_PER_ANSWER
    docs = [Document(page_content="OPENAI_API_KEY=sk-" + "a" * 40,
        metadata={"source_url": f"https://docs.example.org/{index}"})
        for index in range(SOURCES_MAX_PER_ANSWER + 3)]
    sources = document_sources(docs)
    assert len(sources) == SOURCES_MAX_PER_ANSWER
    assert "sk-" + "a" * 40 not in str(sources)


def test_rag_answer_and_sources_render_in_chat():
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_string('''
import streamlit as st
from unittest.mock import Mock
from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from src.app.chat_service import run_chat
from src.app.chat import render_sources
graph = Mock()
graph.invoke.return_value = {"route": "answer", "answer": "문서 기반 답변",
    "messages": [AIMessage(content="문서 기반 답변")],
    "retrieved_docs": [Document(page_content="근거 문서", metadata={
        "source_url": "https://docs.example.org/graph", "title": "Graph API"})]}
result = run_chat([{"role": "user", "content": "문서 검색"}], graph=graph)
with st.chat_message("assistant"):
    st.markdown(result["answer"])
    render_sources(result["sources"])
''').run()
    assert not app.exception
    assert app.chat_message[0].name == "assistant"
    assert app.markdown[0].value == "문서 기반 답변"
    assert app.expander[0].label == "참고 자료"
    assert "Graph API" in app.markdown[1].value
    assert app.get("link_button")[0].url == "https://docs.example.org/graph"
