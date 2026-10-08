"""
Vector DB 저장 및 검색 관리 (Pinecone, 서버리스)

  ensure_index()            인덱스가 없으면 만듦 (차원 = 임베딩 모델 차원, 코사인 유사도)
  build_vectorstore(chunks) 청크를 임베딩해서 Pinecone 에 업로드 (namespace 를 비우고 새로)
  load_vectorstore()        LangChain PineconeVectorStore 객체
  vector_search(query, k, filters)  벡터 유사도 검색 → [(Document, 점수)]
  to_pinecone_filter(filters)       {"tech": "mcp", "doc_type": [...]} → Pinecone 필터 문법

준비
  1. https://app.pinecone.io 가입 → API Keys 에서 키 발급
  2. .env 에 PINECONE_API_KEY=... 추가 (인덱스는 코드가 자동으로 만듦)

주의
  - 임베딩 모델을 바꾸면 차원이 달라집니다 → PINECONE_INDEX_NAME 을 바꾸거나 기존 인덱스를 지우고 다시 build
  - Pinecone 은 업로드 직후 몇 초간 검색에 안 잡힐 수 있습니다 (최종 일관성)
  - 메타데이터 값은 문자열·숫자·불리언·문자열 리스트만 가능, 벡터 1개당 40KB 이하
"""

from functools import lru_cache

from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore      # pip install langchain-pinecone
from pinecone import Pinecone, ServerlessSpec

from src.const.config import (PINECONE_API_KEY, PINECONE_CLOUD, PINECONE_INDEX_NAME,
                              PINECONE_NAMESPACE, PINECONE_REGION)
from src.const.models import EMBEDDING_DIM, get_embeddings

BATCH_SIZE = 100                    # 한 번에 업로드하는 청크 수 (Pinecone 요청 크기 2MB 제한 고려)


@lru_cache(maxsize=1)
def _client() -> Pinecone:
    if not PINECONE_API_KEY:
        raise RuntimeError(".env 에 PINECONE_API_KEY 가 없습니다.")
    return Pinecone(api_key=PINECONE_API_KEY)


def ensure_index(index_name: str = PINECONE_INDEX_NAME, dimension: int = EMBEDDING_DIM):
    pc = _client()
    if not pc.has_index(index_name):
        print(f"[pinecone] 인덱스 생성: {index_name} (dim={dimension}, cosine)")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION),
        )                                   # timeout 을 안 주면 인덱스가 준비될 때까지 기다림
    else:
        existing = pc.describe_index(index_name).dimension
        if existing != dimension:
            raise RuntimeError(
                f"인덱스 '{index_name}' 차원({existing})과 임베딩 차원({dimension})이 다릅니다. "
                "PINECONE_INDEX_NAME 을 바꾸거나 기존 인덱스를 지우세요.")
    return pc.Index(index_name)


@lru_cache(maxsize=1)
def load_vectorstore() -> PineconeVectorStore:
    index = ensure_index()
    return PineconeVectorStore(index=index, embedding=get_embeddings(),
                               namespace=PINECONE_NAMESPACE, text_key="text")


def _clean_metadata(meta: dict) -> dict:
    """Pinecone 은 None 값을 못 받음 → 빈 문자열로."""
    return {k: ("" if v is None else v) for k, v in meta.items()}


def build_vectorstore(chunks: list[Document], reset: bool = True) -> PineconeVectorStore:
    index = ensure_index()
    if reset:
        try:
            index.delete(delete_all=True, namespace=PINECONE_NAMESPACE)   # 예전 청크가 섞이지 않게
            print(f"[pinecone] namespace '{PINECONE_NAMESPACE}' 비움")
        except Exception:
            pass                                                        # 처음이라 namespace 가 없으면 무시
    store = load_vectorstore()
    for start in range(0, len(chunks), BATCH_SIZE):
        batch = [Document(page_content=c.page_content, metadata=_clean_metadata(c.metadata))
                 for c in chunks[start:start + BATCH_SIZE]]
        store.add_documents(batch, ids=[c.metadata["chunk_id"] for c in batch])
        print(f"[pinecone] {min(start + BATCH_SIZE, len(chunks))}/{len(chunks)} 업로드")
    return store


def to_pinecone_filter(filters: dict | None) -> dict | None:
    """{"tech": "mcp", "doc_type": ["official_doc", "github_issue"]}
       → {"tech": {"$eq": "mcp"}, "doc_type": {"$in": [...]}}   (여러 키는 AND)"""
    if not filters:
        return None
    out = {}
    for key, value in filters.items():
        if value is None:
            continue
        if isinstance(value, (list, tuple, set)):
            out[key] = {"$in": list(value)}
        else:
            out[key] = {"$eq": value}
    return out or None


def vector_search(query: str, k: int = 10, filters: dict | None = None) -> list[tuple[Document, float]]:
    """코사인 유사도 점수와 함께 반환 (클수록 비슷함)."""
    return load_vectorstore().similarity_search_with_score(query, k=k, filter=to_pinecone_filter(filters))
