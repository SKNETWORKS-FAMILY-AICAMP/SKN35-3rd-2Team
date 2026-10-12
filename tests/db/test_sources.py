"""답변 출처 목록 만들기(build_sources) 확인. 메모리 SQLite를 쓴다."""

import secrets

import pytest
from langchain_core.documents import Document

from src.const import db_config as cfg
from src.db import (
    build_sources,
    create_user,
    get_sources,
    init_db,
    make_engine,
    make_session_factory,
    record_assistant_turn,
    record_user_turn,
    session_scope,
)

KEYS = {"url", "title", "tech", "version", "doc_type", "snippet", "score"}


def rag_doc(url="https://docs.langchain.com/oss/python/langgraph/graph-api", **extra):
    """retriever가 돌려주는 문서의 모양 (2026-10 실제 메타데이터 키)."""
    metadata = {
        "chunk_id": "langgraph-graph-api-034",
        "document_type": "documentation",
        "file_name": "graph-api.mdx",
        "source": "data/raw/langgraph/graph-api.mdx",
        "source_url": url,
        "technology": "langgraph",
        "title": "Graph API overview",
        "score": 0.4537,
    }
    metadata.update(extra)
    return Document(page_content="Nodes are Python functions that receive the state. " * 30, metadata=metadata)


def mcp_record(*sources, status="success"):
    return {"status": status, "tool": "search_github_issues", "sources": list(sources)}


ISSUE = {
    "url": "https://github.com/langchain-ai/langgraph/issues/9163",
    "title": "langchain-ai/langgraph#9163 GraphRecursionError raised after the graph finished",
    "tech": "langgraph",
    "doc_type": "issue",
    "snippet": "[open] The error is raised although...",
}


# ---------------------------------------------------------------- RAG 문서
def test_rag_document_becomes_a_db_source():
    [source] = build_sources([rag_doc()])
    assert set(source) == KEYS
    assert source["url"] == "https://docs.langchain.com/oss/python/langgraph/graph-api"
    assert source["title"] == "Graph API overview" and source["tech"] == "langgraph" and source["doc_type"] == "documentation"
    assert source["score"] == pytest.approx(0.4537) and source["version"] is None
    assert len(source["snippet"]) <= cfg.SOURCES_SNIPPET_CHARS


def test_rag_document_as_plain_dict_and_fallback_title():
    doc = {"page_content": "본문", "metadata": {"source_url": "https://docs.example.com/a", "file_name": "a.mdx"}}
    [source] = build_sources([doc])
    assert source["title"] == "a.mdx" and source["snippet"] == "본문"
    [no_title] = build_sources([{"page_content": "x", "metadata": {"url": "https://docs.example.com/b"}}])
    assert no_title["title"] == "https://docs.example.com/b"  # 제목이 없으면 주소를 제목으로 쓴다


def test_rag_documents_without_a_url_are_skipped():
    docs = [rag_doc(url=None), Document(page_content="x", metadata={"title": "no url"}), rag_doc("https://docs.example.com/ok")]
    assert [s["url"] for s in build_sources(docs)] == ["https://docs.example.com/ok"]


# ---------------------------------------------------------------- MCP 결과
def test_successful_mcp_results_contribute_their_sources():
    results = [mcp_record(ISSUE), {"status": "success", "tool": "check_symbol_exists", "sources": []}]
    assert [s["url"] for s in build_sources(None, results)] == [ISSUE["url"]]


def test_failed_and_no_tool_mcp_results_are_not_sources():
    results = [mcp_record(ISSUE, status="failed"), mcp_record(ISSUE, status="no_tool")]
    assert build_sources(None, results) == []


def test_rag_first_then_mcp_and_duplicates_are_merged():
    same = {"url": "https://docs.example.com/x", "title": "MCP가 준 같은 주소"}
    sources = build_sources([rag_doc("https://docs.example.com/x"), rag_doc("https://docs.example.com/y")], [mcp_record(same, ISSUE)])
    assert [s["url"] for s in sources] == ["https://docs.example.com/x", "https://docs.example.com/y", ISSUE["url"]]
    assert sources[0]["title"] == "Graph API overview"  # 먼저 나온 것을 남긴다


def test_limit_is_respected():
    docs = [rag_doc(f"https://docs.example.com/{i}") for i in range(30)]
    assert len(build_sources(docs)) == cfg.SOURCES_MAX_PER_ANSWER
    assert len(build_sources(docs, limit=3)) == 3


# ---------------------------------------------------------------- 안전: 주소, 길이, 비밀값, 이상한 입력
@pytest.mark.parametrize(
    "url",
    ["javascript:alert(1)", "file:///etc/passwd", "ftp://example.com/a", "data:text/html,x", "//example.com/a",
     "https://exa mple.com/a", "https://example.com/" + "a" * 1100, "", "   ", None, 123],
)
def test_unsafe_or_unusable_urls_are_dropped(url):
    assert build_sources([rag_doc(url)]) == []
    assert build_sources(None, [mcp_record({"url": url})]) == []


def test_http_urls_are_accepted_case_insensitively():
    assert len(build_sources(None, [mcp_record({"url": "HTTPS://Example.com/A"}, {"url": "http://example.com/b"})])) == 2


def test_long_text_fields_are_clipped_to_the_db_columns():
    [source] = build_sources([rag_doc(title="가" * 1000, technology="t" * 100, document_type="d" * 100, version="v" * 100)])
    assert len(source["title"]) == 300 and len(source["tech"]) == 30 and len(source["doc_type"]) == 30 and len(source["version"]) == 30


def test_secrets_in_title_and_snippet_are_masked():
    key = "sk-" + "a1B2c3D4e5F6g7H8i9J0k1L2"
    [source] = build_sources([Document(page_content=f"OPENAI_API_KEY={key} 로 호출", metadata={"source_url": "https://docs.example.com/k", "title": f"키 {key} 예시"})])
    assert key not in source["title"] and key not in source["snippet"]


@pytest.mark.parametrize(
    "score, expected",
    [("0.5", 0.5), (1, 1.0), (0, 0.0), (None, None), ("abc", None), (True, None), ([1], None), (float("nan"), None), (float("inf"), None)],
    ids=["str-number", "int", "zero", "none", "text", "bool", "list", "nan", "inf"],
)
def test_score_is_a_finite_float_or_none(score, expected):
    [source] = build_sources([rag_doc(score=score)])
    assert source["score"] == expected  # NaN과 무한대는 DB에 저장할 수 없어서 점수 없음으로 바꾼다


@pytest.mark.parametrize("junk", [None, 5, "text", [], {}, object()])
def test_garbage_items_are_ignored_without_errors(junk):
    assert build_sources([junk, rag_doc()], [junk, {"status": "success", "sources": [junk, 5, None]}]) == build_sources([rag_doc()])


def test_empty_inputs():
    assert build_sources() == [] and build_sources([], []) == [] and build_sources(None, None) == []


# ---------------------------------------------------------------- DB까지 저장되는지
@pytest.fixture()
def session():
    engine = make_engine("sqlite://")
    init_db(engine)
    with session_scope(make_session_factory(engine)) as s:
        yield s


def test_built_sources_can_be_saved_and_read_back(session):
    user = create_user(session, "src_user", "pw-" + secrets.token_urlsafe(12))
    turn = record_user_turn(session, user.id, "GraphRecursionError가 나요")
    sources = build_sources([rag_doc()], [mcp_record(ISSUE)])
    done = record_assistant_turn(session, user.id, turn.conversation_id, "원인은 ...", sources=sources, user_message_id=turn.message_id)
    saved = get_sources(session, done.message_id, user.id)
    assert [s.url for s in saved] == [s["url"] for s in sources] and [s.rank for s in saved] == [0, 1]
    assert saved[1].doc_type == "issue" and saved[0].tech == "langgraph" and saved[0].score == pytest.approx(0.4537)
