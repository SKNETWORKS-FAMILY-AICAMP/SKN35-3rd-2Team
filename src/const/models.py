=======
"""
LLM / Embedding / Reranker 모델 설정

  get_llm()         Multi-Query, Context 압축 등에 쓰는 Chat 모델
  get_embeddings()  임베딩 모델 (한국어 질문 ↔ 영어 문서 → 다국어 모델)
  EMBEDDING_DIM     Pinecone 인덱스 차원 (임베딩 모델과 반드시 같아야 함)
  get_reranker()    Cross-Encoder 재정렬 모델

임베딩 모델을 바꾸면 Pinecone 인덱스 차원이 달라지므로 인덱스 이름을 바꾸거나 지우고 다시 만들어야 합니다.
"""

import os
from functools import lru_cache

import src.const.config  # noqa: F401  (.env 로드)

LLM_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai")          # openai | hf
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
HF_EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL", "BAAI/bge-m3")

# 모델별 벡터 차원
_DIMS = {"text-embedding-3-small": 1536, "text-embedding-3-large": 3072, "BAAI/bge-m3": 1024}
EMBEDDING_MODEL = HF_EMBEDDING_MODEL if EMBEDDING_PROVIDER == "hf" else OPENAI_EMBEDDING_MODEL
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", _DIMS.get(EMBEDDING_MODEL, 1536)))

RERANK_MODEL = os.getenv("RERANK_MODEL", "BAAI/bge-reranker-v2-m3")


@lru_cache(maxsize=None)
def get_llm(temperature: float = 0.0):
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=LLM_MODEL, temperature=temperature)


@lru_cache(maxsize=1)
def get_embeddings():
    if EMBEDDING_PROVIDER == "hf":
        # 무료/로컬: pip install langchain-huggingface sentence-transformers (첫 실행 때 약 2GB 다운로드)
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=HF_EMBEDDING_MODEL,
                                     encode_kwargs={"normalize_embeddings": True})
    from langchain_openai import OpenAIEmbeddings
    return OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)


@lru_cache(maxsize=1)
def get_reranker():
    # pip install sentence-transformers  (첫 실행 때 약 2GB 다운로드, GPU 없으면 다소 느림)
    from sentence_transformers import CrossEncoder
    return CrossEncoder(RERANK_MODEL, max_length=512)
