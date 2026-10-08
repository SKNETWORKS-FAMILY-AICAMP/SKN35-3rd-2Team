from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.const.config import (
    OPEN_API_KEY,
    OPEN_EMBEDDING_MODEL,
    OPEN_MODEL,
    RERANK_MODEL,
)


# OPENAI LLM MODEL
def create_openai_model(temperature=0.0, timeout=600):
    model = ChatOpenAI(
        api_key=OPEN_API_KEY,
        model=OPEN_MODEL,
        temperature=temperature,
        timeout=timeout,
    )

    return model


# OPENAI EMBEDDING MODEL
def create_openai_embedding():
    embedding = OpenAIEmbeddings(api_key=OPEN_API_KEY, model=OPEN_EMBEDDING_MODEL)

    return embedding


# RERANK MODEL (Cross-Encoder)
def create_rerank():
    # pip install sentence-transformers (첫 실행 때 모델 약 2GB 다운로드, GPU 없으면 다소 느림)
    from sentence_transformers import CrossEncoder

    rerank = CrossEncoder(RERANK_MODEL, max_length=512)

    return rerank
