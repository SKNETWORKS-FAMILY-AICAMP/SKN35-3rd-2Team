from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings, NVIDIARerank

from src.const.config import (
    OPENAI_API_KEY,
    NVIDIA_API_KEY,
    NVIDIA_EMBEDDING_MODEL,
    NVIDIA_MODEL,
    NVIDIA_RERANK_API_KEY,
    NVIDIA_RERANK_MODEL,
)


# NVIDIA LLM MODEL
def create_nvidia_model(temperature=0.0, timeout=600):
    model = ChatNVIDIA(
        api_key=NVIDIA_API_KEY,
        model=NVIDIA_MODEL,
        temperature=temperature,
        timeout=timeout,
    )

    return model


# NVIDIA EMBEDDING MODEL
def create_nvidia_embedding():
    embedding = NVIDIAEmbeddings(api_key=NVIDIA_API_KEY, model=NVIDIA_EMBEDDING_MODEL)

    return embedding


# NVIDIA RERANK MODEL
def create_nvidia_rerank():
    rerank = NVIDIARerank(api_key=NVIDIA_RERANK_API_KEY, model=NVIDIA_RERANK_MODEL)

    return rerank


# OPENAI CLIENT
def create_openai_client(timeout=60):
    from openai import OpenAI

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY 설정이 필요합니다.")
    return OpenAI(api_key=OPENAI_API_KEY, timeout=timeout, max_retries=0)
