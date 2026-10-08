# Pinecone Hybrid 검색 모듈 (LangChain PineconeHybridSearchRetriever)
#
# Dense 와 Sparse 를 따로 만들고 섞지 않고, LangChain 의 Hybrid Retriever 하나로 처리한다.
#   PineconeHybridSearchRetriever(
#       embeddings     = OpenAI 임베딩 (src/const/models.py, 1536차원)   → 뜻이 비슷한 문서
#       sparse_encoder = BM25Encoder (우리 청크로 학습)                   → GraphRecursionError, -32601 같은 정확한 단어
#       index          = Pinecone 인덱스 (metric=dotproduct)
#       alpha          = 0.7   → 점수 = 0.7 × Dense + 0.3 × Sparse  (1.0 이면 Dense 만, 0.0 이면 Sparse 만)
#   )
#   저장: retriever.add_texts(...)   검색: retriever.invoke(질문)   → 둘 다 Dense + Sparse 를 한 번에 처리
#
# BM25Encoder 는 build 할 때 청크로 학습해서 data/processed/bm25_params.json 에 저장하고,
# 검색할 때 그 파일을 다시 읽는다. (팀원은 이 파일만 공유받으면 build 없이 검색 가능)
#
# 검색 옵션 (PineconeHybridRetriever 필드, 모두 선택)
#   filters           {"technology": "langgraph"} / {"technology": ["langchain", "langgraph"]}
#   use_query_rewrite 질문을 영어 검색어로 정리 (BM25 가 영어 문서 단어로 찾으므로 한국어 질문에 효과 큼)
#                     filters 가 없으면 감지한 technology 로 자동 필터
#   use_multi_query   영어 검색어 여러 개로 검색해서 RRF 로 합침
#   use_rerank        Cross-Encoder 로 상위 후보 재정렬
#   history           대화 기록 (query_rewrite 에 사용)
#
# 실행 (프로젝트 루트에서)
#   python -m src.vectorstore.build                     # 문서 → 청크 → Pinecone 업로드 + BM25 저장
#   python -m src.rag.retriever "LangGraph 재귀 한도 오류" --tech langgraph --rewrite --rerank
#
# 코드에서
#   retriever = create_hybrid_retriever(top_k=5, use_query_rewrite=True)
#   documents = retriever.invoke("MCP 서버 연결하면 -32601 오류가 나요")

from functools import lru_cache

from langchain_community.retrievers import PineconeHybridSearchRetriever
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pinecone import Pinecone, ServerlessSpec
from pinecone_text.sparse import BM25Encoder

from src.const.config import (
    BM25_PATH,
    EMBEDDING_DIM,
    PINECONE_API_KEY,
    PINECONE_CLOUD,
    PINECONE_INDEX_NAME,
    PINECONE_REGION,
)
from src.const.models import create_openai_embedding
from src.rag.loader import load_documents
from src.rag.splitter import split_documents

DENSE_DIMENSION = EMBEDDING_DIM

CLOUD = PINECONE_CLOUD
REGION = PINECONE_REGION

TOP_K = 5
ALPHA = 0.7

# 여러 검색어를 합치거나 재정렬할 때 1차로 가져오는 후보 수
FETCH_K = 20

# Pinecone metadata 에서 본문을 담는 키
TEXT_KEY = "text"


def get_pinecone_client():
    if not PINECONE_API_KEY:
        raise RuntimeError(".env 에 PINECONE_API_KEY 가 없습니다.")

    return Pinecone(api_key=PINECONE_API_KEY)


def create_pinecone_index():
    pc = get_pinecone_client()

    existing_indexes = [index.name for index in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Pinecone Index 생성 중: {PINECONE_INDEX_NAME}")

        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=DENSE_DIMENSION,
            metric="dotproduct",          # Hybrid(Dense + Sparse) 검색은 dotproduct 만 지원
            spec=ServerlessSpec(
                cloud=CLOUD,
                region=REGION,
            ),
        )

        print(f"Pinecone Index 생성 완료: {PINECONE_INDEX_NAME}")

    else:
        description = pc.describe_index(PINECONE_INDEX_NAME)

        if description.metric != "dotproduct" or description.dimension != DENSE_DIMENSION:
            raise RuntimeError(
                f"기존 인덱스 '{PINECONE_INDEX_NAME}' 는 metric={description.metric}, "
                f"dimension={description.dimension} 입니다. Hybrid 검색에는 metric=dotproduct, "
                f"dimension={DENSE_DIMENSION} 이 필요합니다. .env 의 PINECONE_INDEX_NAME 을 새 이름으로 "
                "바꾸거나 Pinecone 콘솔에서 기존 인덱스를 지운 뒤 다시 실행하세요."
            )

        print(f"Pinecone Index 이미 존재: {PINECONE_INDEX_NAME}")

    return pc.Index(PINECONE_INDEX_NAME)


def create_bm25_encoder(documents: list[Document]) -> BM25Encoder:
    """청크로 BM25 를 학습하고 data/processed/bm25_params.json 에 저장 (처음 실행 때 nltk 데이터 자동 다운로드)"""

    encoder = BM25Encoder()
    encoder.fit([document.page_content for document in documents])

    BM25_PATH.parent.mkdir(parents=True, exist_ok=True)
    encoder.dump(str(BM25_PATH))

    print(f"BM25 저장: {BM25_PATH}")

    load_bm25_encoder.cache_clear()

    return encoder


@lru_cache(maxsize=1)
def load_bm25_encoder() -> BM25Encoder:
    if not BM25_PATH.exists():
        raise FileNotFoundError(f"{BM25_PATH} 가 없습니다. 먼저 python -m src.vectorstore.build 를 실행하세요.")

    return BM25Encoder().load(str(BM25_PATH))


def create_hybrid_search_retriever(top_k: int = TOP_K, alpha: float = ALPHA) -> PineconeHybridSearchRetriever:
    """LangChain Hybrid Retriever (Dense + Sparse 를 한 객체가 처리)"""

    return PineconeHybridSearchRetriever(
        embeddings=create_openai_embedding(),
        sparse_encoder=load_bm25_encoder(),
        index=get_pinecone_client().Index(PINECONE_INDEX_NAME),
        top_k=top_k,
        alpha=alpha,
        text_key=TEXT_KEY,
    )


def _clean_metadata(metadata: dict) -> dict:
    """Pinecone metadata 는 문자열·숫자·불리언·문자열 리스트만 가능 (None → "")"""

    cleaned = {}

    for key, value in metadata.items():
        if value is None:
            value = ""
        elif not isinstance(value, (str, int, float, bool, list)):
            value = str(value)
        cleaned[key] = value

    return cleaned


def to_pinecone_filter(filters: dict | None) -> dict | None:
    """{"technology": "mcp", "document_type": ["error", "documentation"]}
       → {"technology": {"$eq": "mcp"}, "document_type": {"$in": [...]}}   (여러 키는 AND)"""

    if not filters:
        return None

    pinecone_filter = {}

    for key, value in filters.items():
        if value is None:
            continue

        if isinstance(value, (list, tuple, set)):
            pinecone_filter[key] = {"$in": list(value)}
        else:
            pinecone_filter[key] = {"$eq": value}

    return pinecone_filter or None


def hybrid_search(
    query: str,
    top_k: int = TOP_K,
    filters: dict | None = None,
    alpha: float = ALPHA,
) -> list[Document]:
    retriever = create_hybrid_search_retriever(top_k=top_k, alpha=alpha)

    pinecone_filter = to_pinecone_filter(filters)

    # filter 는 PineconeHybridSearchRetriever 가 index.query(filter=...) 로 그대로 넘김
    if pinecone_filter:
        return retriever.invoke(query, filter=pinecone_filter)

    return retriever.invoke(query)


class PineconeHybridRetriever(BaseRetriever):
    """hybrid_search 에 Query Rewrite / Multi-Query / Rerank 옵션을 더한 Retriever"""

    top_k: int = TOP_K
    filters: dict | None = None
    alpha: float = ALPHA
    use_query_rewrite: bool = False
    use_multi_query: bool = False
    use_rerank: bool = False
    fetch_k: int = FETCH_K
    history: list | None = None

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager=None,
    ) -> list[Document]:

        queries = [query]
        search_query = query
        filters = self.filters

        # 1. 질문 재작성: 대화 맥락 반영 + 영어 검색어 (원래 질문과 함께 검색)
        if self.use_query_rewrite:
            from src.rag.query_rewrite import rewrite_query, to_filters

            rewritten = rewrite_query(query, history=self.history)
            search_query = rewritten.search_query
            queries.append(search_query)

            if filters is None:
                filters = to_filters(rewritten)

        # 2. Multi-Query: 다른 각도의 영어 검색어 추가
        if self.use_multi_query:
            from src.rag.multi_query import generate_queries

            queries.extend(generate_queries(search_query, include_original=False))

        queries = list(dict.fromkeys(q.strip() for q in queries if q.strip()))

        many = len(queries) > 1 or self.use_rerank
        top_k = max(self.fetch_k, self.top_k) if many else self.top_k

        # 3. 검색어마다 Hybrid 검색
        result_lists = [
            hybrid_search(query=q, top_k=top_k, filters=filters, alpha=self.alpha)
            for q in queries
        ]

        # 4. 여러 검색어 결과는 RRF 로 합침
        if len(result_lists) == 1:
            ranked = [(document, document.metadata.get("score", 0.0)) for document in result_lists[0]]
        else:
            from src.rag.rrf import reciprocal_rank_fusion

            ranked = reciprocal_rank_fusion(result_lists, top_n=top_k)

        # 5. 재정렬
        if self.use_rerank:
            from src.rag.rerank import rerank

            ranked = rerank(query, [document for document, _ in ranked], top_n=self.top_k)

        documents = []

        for document, score in ranked[: self.top_k]:
            document.metadata["score"] = round(float(score), 6)
            documents.append(document)

        return documents


def build_pinecone(technologies: list[str] | None = None, reset: bool = True):
    """
    문서 → 청크 → BM25 학습·저장 → Pinecone 업로드 (Dense + Sparse 를 add_texts 가 한 번에).
    reset=True 이고 전체를 올릴 때는 예전 벡터를 먼저 지운다 (없어진 문서의 청크가 남지 않게).
    """

    print("Pinecone Hybrid Index 구축")

    documents = load_documents(technologies)

    chunks = split_documents(documents)

    index = create_pinecone_index()

    if reset and not technologies:
        try:
            index.delete(delete_all=True)
            print("기존 벡터 삭제")
        except Exception:
            pass                                    # 비어 있는 새 인덱스면 무시

    # 일부 기술만 올릴 때는 기존 BM25 를 유지 (전체 문서 기준 통계가 바뀌지 않게)
    if technologies and BM25_PATH.exists():
        load_bm25_encoder()
    else:
        create_bm25_encoder(chunks)

    retriever = create_hybrid_search_retriever()

    print(f"Pinecone Upsert 시작: {len(chunks)}개")

    retriever.add_texts(
        texts=[chunk.page_content for chunk in chunks],
        # 같은 청크는 항상 같은 ID → 다시 올려도 중복 없이 덮어씀
        ids=[chunk.metadata["chunk_id"] for chunk in chunks],
        metadatas=[_clean_metadata(chunk.metadata) for chunk in chunks],
    )

    print("Pinecone Hybrid Index 구축 완료")

    return index


def create_hybrid_retriever(**options):
    """options: top_k, filters, alpha, use_query_rewrite, use_multi_query, use_rerank, fetch_k, history"""

    pc = get_pinecone_client()

    existing_indexes = [index.name for index in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing_indexes or not BM25_PATH.exists():
        print("Pinecone Index 또는 BM25 파일이 없습니다.")

        build_pinecone()

    else:
        print(f"Pinecone Index 사용: {PINECONE_INDEX_NAME}")

    retriever = PineconeHybridRetriever(**options)

    return retriever


def get_chunk(chunk_id: str) -> Document | None:
    """청크 ID 로 원문 조회 (C 파트 환각 점검 등)"""

    index = get_pinecone_client().Index(PINECONE_INDEX_NAME)

    vector = index.fetch(ids=[chunk_id]).vectors.get(chunk_id)

    if vector is None:
        return None

    metadata = dict(vector.metadata or {})
    text = metadata.pop(TEXT_KEY, "")

    return Document(page_content=text, metadata=metadata)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="LangGraph에서 GRAPH_RECURSION_LIMIT 에러가 발생하는 이유는?")
    parser.add_argument("--build", action="store_true", help="문서를 다시 읽어 Pinecone 에 업로드")
    parser.add_argument("--tech", nargs="+", help="langchain / langgraph / mcp 로 필터")
    parser.add_argument("--rewrite", action="store_true", help="Query Rewrite 사용")
    parser.add_argument("--multi", action="store_true", help="Multi-Query 사용")
    parser.add_argument("--rerank", action="store_true", help="Cross-Encoder 재정렬 사용")
    args = parser.parse_args()

    if args.build:
        build_pinecone()

    retriever = create_hybrid_retriever(
        filters={"technology": args.tech} if args.tech else None,
        use_query_rewrite=args.rewrite,
        use_multi_query=args.multi,
        use_rerank=args.rerank,
    )

    documents = retriever.invoke(args.query)

    print("검색 결과")

    for i, document in enumerate(
        documents,
        start=1,
    ):
        print()
        print(f"[{i}]")
        print("score:", document.metadata.get("score"))
        print("technology:", document.metadata.get("technology"))
        print("document_type:", document.metadata.get("document_type"))
        print("source:", document.metadata.get("source"))
        print("source_url:", document.metadata.get("source_url"))
        print(document.page_content[:500])
