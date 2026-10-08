import time

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pinecone import Pinecone, ServerlessSpec

from src.const.config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from src.rag.loader import load_documents
from src.rag.splitter import split_documents

DENSE_MODEL = "llama-text-embed-v2"
SPARSE_MODEL = "pinecone-sparse-english-v0"

DENSE_DIMENSION = 1024

CLOUD = "aws"
REGION = "us-east-1"

TOP_K = 5
ALPHA = 0.7


def get_pinecone_client():
    return Pinecone(api_key=PINECONE_API_KEY)


def create_pinecone_index():
    pc = get_pinecone_client()

    existing_indexes = [index.name for index in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Pinecone Index 생성 중: {PINECONE_INDEX_NAME}")

        pc.create_index(
            name=PINECONE_INDEX_NAME,
            vector_type="dense",
            dimension=DENSE_DIMENSION,
            metric="dotproduct",
            spec=ServerlessSpec(
                cloud=CLOUD,
                region=REGION,
            ),
        )

        print(f"Pinecone Index 생성 완료: {PINECONE_INDEX_NAME}")

    else:
        print(f"Pinecone Index 이미 존재: {PINECONE_INDEX_NAME}")

    return pc.Index(PINECONE_INDEX_NAME)


def create_dense_embeddings(
    pc,
    texts: list[str],
    batch_size: int = 20,
    sleep_seconds: float = 2.0,
):
    all_embeddings = []

    total = len(texts)

    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        batch = texts[start:end]

        print(f"Dense Embedding: {start + 1}~{end}/{total}")

        result = pc.inference.embed(
            model=DENSE_MODEL,
            inputs=batch,
            parameters={
                "input_type": "passage",
                "truncate": "END",
            },
        )

        all_embeddings.extend(result.data)

        time.sleep(sleep_seconds)

    return all_embeddings


def create_sparse_embeddings(
    pc,
    texts: list[str],
    batch_size: int = 20,
    sleep_seconds: float = 2.0,
):
    all_embeddings = []

    total = len(texts)

    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        batch = texts[start:end]

        print(f"Sparse Embedding: {start + 1}~{end}/{total}")

        result = pc.inference.embed(
            model=SPARSE_MODEL,
            inputs=batch,
            parameters={
                "input_type": "passage",
            },
        )

        all_embeddings.extend(result.data)

        time.sleep(sleep_seconds)

    return all_embeddings


def create_vectors(
    pc,
    documents: list[Document],
    dense_alpha: float = 0.7,
):
    texts = [doc.page_content for doc in documents]

    dense_embeddings = create_dense_embeddings(
        pc,
        texts,
        batch_size=20,
        sleep_seconds=2.0,
    )

    sparse_embeddings = create_sparse_embeddings(
        pc,
        texts,
        batch_size=20,
        sleep_seconds=2.0,
    )

    vectors = []

    for i, document in enumerate(documents):
        dense_embedding = dense_embeddings[i]
        sparse_embedding = sparse_embeddings[i]

        vector = {
            "id": f"doc-{i}",
            "values": [value * dense_alpha for value in dense_embedding.values],
            "sparse_values": {
                "indices": sparse_embedding.sparse_indices,
                "values": [
                    value * (1 - dense_alpha)
                    for value in sparse_embedding.sparse_values
                ],
            },
            "metadata": document.metadata
            | {
                "text": document.page_content,
            },
        }

        vectors.append(vector)

    return vectors


def upsert_documents(
    index,
    vectors,
    batch_size: int = 50,
):
    total = len(vectors)

    print(f"Pinecone Upsert 시작: {total}개")

    for start in range(
        0,
        total,
        batch_size,
    ):
        end = start + batch_size

        batch = vectors[start:end]

        index.upsert(vectors=batch)

        print(f"Upsert 완료: {min(end, total)}/{total}")

    print("Pinecone Upsert 완료")


def create_query_embeddings(
    pc,
    query: str,
):
    dense_result = pc.inference.embed(
        model=DENSE_MODEL,
        inputs=[query],
        parameters={
            "input_type": "query",
            "truncate": "END",
        },
    )

    sparse_result = pc.inference.embed(
        model=SPARSE_MODEL,
        inputs=[query],
        parameters={
            "input_type": "query",
        },
    )

    dense = dense_result.data[0]
    sparse = sparse_result.data[0]

    return dense, sparse


def hybrid_search(
    query: str,
    top_k: int = TOP_K,
):
    pc = get_pinecone_client()

    index = pc.Index(PINECONE_INDEX_NAME)
    print(index.describe_index_stats())

    dense, sparse = create_query_embeddings(
        pc,
        query,
    )

    # Dense / Sparse 가중치 적용
    dense_values = [value * ALPHA for value in dense.values]

    sparse_values = [value * (1 - ALPHA) for value in sparse.sparse_values]

    results = index.query(
        vector=dense_values,
        sparse_vector={
            "indices": sparse.sparse_indices,
            "values": sparse_values,
        },
        top_k=top_k,
        include_metadata=True,
    )

    return results


def convert_to_documents(results):
    documents = []

    for match in results.matches:
        metadata = match.metadata or {}

        text = metadata.get(
            "text",
            "",
        )

        document_metadata = {
            key: value for key, value in metadata.items() if key != "text"
        }

        document_metadata["score"] = match.score
        document_metadata["id"] = match.id

        document = Document(
            page_content=text,
            metadata=document_metadata,
        )

        documents.append(document)

    return documents


class PineconeHybridRetriever(BaseRetriever):
    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager=None,
    ) -> list[Document]:

        results = hybrid_search(
            query=query,
            top_k=TOP_K,
        )

        documents = convert_to_documents(results)

        return documents


def build_pinecone():
    print("Pinecone Hybrid Index 구축")

    documents = load_documents()

    print(f"전체 Document 개수: {len(documents)}")

    chunks = split_documents(documents)

    print(f"전체 Chunk 개수: {len(chunks)}")

    pc = get_pinecone_client()

    index = create_pinecone_index()

    vectors = create_vectors(
        pc,
        chunks,
    )

    upsert_documents(
        index,
        vectors,
    )
    print("Pinecone Hybrid Index 구축 완료")

    return index


def create_hybrid_retriever():
    pc = get_pinecone_client()

    existing_indexes = [index.name for index in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing_indexes:
        print("Pinecone Index가 없습니다.")

        build_pinecone()

    else:
        print(f"Pinecone Index 사용: {PINECONE_INDEX_NAME}")

    retriever = PineconeHybridRetriever()

    return retriever


if __name__ == "__main__":
    retriever = create_hybrid_retriever()

    query = "LangGraph에서 GRAPH_RECURSION_LIMIT 에러가 발생하는 이유는?"

    documents = retriever.invoke(query)

    print("검색 결과")

    for i, document in enumerate(
        documents,
        start=1,
    ):
        print()
        print(f"[{i}]")
        print(
            "score:",
            document.metadata.get("score"),
        )
        print(
            "technology:",
            document.metadata.get("technology"),
        )
        print(
            "document_type:",
            document.metadata.get("document_type"),
        )
        print(
            "source:",
            document.metadata.get("source"),
        )
        print(document.page_content[:500])
=======
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

