"""
문서 검색 (팀 공유 인터페이스: search / get_chunk / get_retriever)

검색 흐름
  질문
   ├─(선택) query_rewrite: 대화 맥락을 반영하고 영어 검색어 1개로 정리 (원래 질문과 함께 검색)
   ├─(선택) multi_query: 질문을 영어 검색어 여러 개로 확장
   ├─ 질문마다  벡터 검색(Pinecone)  +  키워드 검색(BM25)
   ├─ rrf: 모든 결과 목록을 RRF 로 하나로 합침  (하이브리드 검색)
   ├─(선택) rerank: Cross-Encoder 로 상위 후보 재정렬
   └─ 상위 k개 반환

  벡터 검색은 뜻이 비슷한 문서를, BM25 는 `GraphRecursionError`, `-32601` 같은 정확한 단어를 잘 찾습니다.

B·C·D 파트가 쓰는 함수
  search(query, k=5, filters=None, use_query_rewrite=False, use_multi_query=False, use_rerank=False,
         history=None) -> list[dict]
      filters 예: {"tech": "langgraph"}, {"tech": ["langchain", "langgraph"], "doc_type": "official_doc"}
      반환 dict: chunk_id, text, title, tech, doc_type, doc_path, source, page_start, page_end,
                 parent_id, source_url(없으면 ""), score
  get_chunk(chunk_id) -> dict | None
  get_retriever(k=5, filters=None, ...) -> LangChain BaseRetriever  (체인·LangGraph 노드에 바로 연결)

사용 예
  from src.rag.retriever import search
  for r in search("LangGraph 재귀 한도 오류 해결법", k=5, filters={"tech": "langgraph"}):
      print(r["score"], r["title"], r["doc_path"])

  python -m src.rag.retriever "MCP 서버 연결 오류" --tech mcp --multi --rerank
"""

import re
from functools import lru_cache

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from rank_bm25 import BM25Okapi                     # pip install rank_bm25

from src.rag.rrf import reciprocal_rank_fusion
from src.rag.splitter import load_chunks
from src.vectorstore.pinecone_store import vector_search

TOKEN_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.\-]*|[가-힣]+")
RESULT_FIELDS = ["chunk_id", "title", "tech", "doc_type", "doc_path", "source",
                 "page_start", "page_end", "parent_id", "source_url"]


# ---------------------------------------------------------------------------
# BM25 (키워드 검색) — chunks.jsonl 로 메모리에 색인
# ---------------------------------------------------------------------------
def tokenize(text: str) -> list[str]:
    tokens = []
    for t in TOKEN_RE.findall(text.lower()):
        tokens.append(t)
        if "." in t or "-" in t:                     # langgraph.prebuilt → langgraph, prebuilt 도 추가
            tokens.extend(p for p in re.split(r"[.\-]", t) if p)
    return tokens


@lru_cache(maxsize=1)
def _bm25_index():
    chunks = load_chunks()
    bm25 = BM25Okapi([tokenize(c.page_content) for c in chunks])
    by_id = {c.metadata["chunk_id"]: c for c in chunks}
    return bm25, chunks, by_id


def _match_filters(meta: dict, filters: dict | None) -> bool:
    if not filters:
        return True
    for key, value in filters.items():
        if value is None:
            continue
        allowed = set(value) if isinstance(value, (list, tuple, set)) else {value}
        if meta.get(key) not in allowed:
            return False
    return True


def bm25_search(query: str, k: int = 20, filters: dict | None = None) -> list[Document]:
    bm25, chunks, _ = _bm25_index()
    scores = bm25.get_scores(tokenize(query))
    order = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)
    out = []
    for i in order:
        if scores[i] <= 0:
            break
        if _match_filters(chunks[i].metadata, filters):
            out.append(chunks[i])
            if len(out) >= k:
                break
    return out


# ---------------------------------------------------------------------------
# 하이브리드 검색
# ---------------------------------------------------------------------------
def search_documents(query: str, k: int = 5, filters: dict | None = None,
                     use_query_rewrite: bool = False, use_multi_query: bool = False,
                     use_rerank: bool = False, history=None,
                     fetch_k: int = 20, vector_weight: float = 0.6,
                     bm25_weight: float = 0.4) -> list[Document]:
    """search() 와 같지만 Document 로 반환 (metadata["score"] 에 점수)."""
    base_question = query
    extra = []
    if use_query_rewrite:
        from src.rag.query_rewrite import rewrite_query
        rq = rewrite_query(query, history=history)
        base_question = rq.standalone_question or query     # 대화 맥락이 반영된 질문
        extra = [rq.search_query]                           # 영어 검색어 (에러 이름 그대로)

    if use_multi_query:
        from src.rag.multi_query import generate_queries
        queries = generate_queries(base_question)
    else:
        queries = [base_question]
    for q in extra:
        if q and q.lower() not in {x.lower() for x in queries}:
            queries.append(q)

    result_lists, weights = [], []
    for q in queries:
        result_lists.append([d for d, _ in vector_search(q, k=fetch_k, filters=filters)])
        weights.append(vector_weight)
        result_lists.append(bm25_search(q, k=fetch_k, filters=filters))
        weights.append(bm25_weight)

    fused = reciprocal_rank_fusion(result_lists, weights=weights, top_n=fetch_k)

    if use_rerank:
        from src.rag.rerank import rerank
        ranked = rerank(base_question, [d for d, _ in fused], top_n=k)
    else:
        ranked = fused[:k]

    return [Document(page_content=d.page_content, metadata={**d.metadata, "score": round(s, 6)})
            for d, s in ranked]


def _to_dict(doc: Document) -> dict:
    m = doc.metadata
    row = {f: m.get(f, "") for f in RESULT_FIELDS}
    row["text"] = doc.page_content
    row["score"] = m.get("score", 0.0)
    return row


def search(query: str, k: int = 5, filters: dict | None = None, **options) -> list[dict]:
    """팀 공유 검색 함수.
    options: use_query_rewrite, use_multi_query, use_rerank, history, fetch_k, vector_weight, bm25_weight"""
    return [_to_dict(d) for d in search_documents(query, k=k, filters=filters, **options)]


def get_chunk(chunk_id: str) -> dict | None:
    """청크 ID 로 원문 조회 (C 파트 환각 점검, 앞뒤 청크 보기 등)."""
    _, _, by_id = _bm25_index()
    doc = by_id.get(chunk_id)
    return _to_dict(doc) if doc else None


# ---------------------------------------------------------------------------
# LangChain Retriever (체인 / LangGraph 노드에 연결)
# ---------------------------------------------------------------------------
class HybridRetriever(BaseRetriever):
    k: int = 5
    filters: dict | None = None
    use_query_rewrite: bool = False
    use_multi_query: bool = False
    use_rerank: bool = False
    fetch_k: int = 20

    def _get_relevant_documents(self, query: str, *,
                                run_manager: CallbackManagerForRetrieverRun) -> list[Document]:
        return search_documents(query, k=self.k, filters=self.filters,
                                use_query_rewrite=self.use_query_rewrite,
                                use_multi_query=self.use_multi_query,
                                use_rerank=self.use_rerank, fetch_k=self.fetch_k)


def get_retriever(k: int = 5, filters: dict | None = None, **options) -> HybridRetriever:
    return HybridRetriever(k=k, filters=filters, **options)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("-k", type=int, default=5)
    ap.add_argument("--tech", nargs="+")
    ap.add_argument("--rewrite", action="store_true", help="Query Rewrite 사용")
    ap.add_argument("--multi", action="store_true", help="Multi-Query 사용")
    ap.add_argument("--rerank", action="store_true", help="Cross-Encoder 재정렬 사용")
    a = ap.parse_args()
    flt = {"tech": a.tech} if a.tech else None
    for r in search(a.query, k=a.k, filters=flt, use_query_rewrite=a.rewrite,
                    use_multi_query=a.multi, use_rerank=a.rerank):
        print(f"{r['score']:.4f}  [{r['tech']}] {r['title']}  ({r['doc_path']} p.{r['page_start']})")
        print("        ", r["text"][:120].replace("\n", " "))
