"""Read existing Pinecone documents without building or resetting the index."""
from langchain_core.documents import Document


def search_documents(question, history):
    from src.const.config import BM25_PATH, PINECONE_API_KEY
    if not PINECONE_API_KEY:
        raise ValueError("Pinecone is not configured")
    if not BM25_PATH.is_file():
        raise FileNotFoundError("BM25 parameters are missing")
    # Do not use create_hybrid_retriever(): it may automatically rebuild the index.
    from src.rag.retriever import PineconeHybridRetriever
    return PineconeHybridRetriever(
        top_k=5, use_query_rewrite=True, history=history,
        use_multi_query=False, use_rerank=False,
    ).invoke(question)


def rag_node(state):
    try:
        docs = search_documents(state["original_question"], state["messages"][:-1])
        # Bound the prompt; copy documents rather than modifying shared metadata.
        bounded, remaining = [], 6000
        for doc in docs:
            if remaining <= 0:
                break
            text = doc.page_content.strip()[:remaining]
            if text:
                bounded.append(Document(page_content=text, metadata=dict(doc.metadata)))
                remaining -= len(text)
        return {"retrieved_docs": bounded, "rag_error": "", "sources": []}
    except Exception:
        # External exception text may contain credentials; return only a safe notice.
        return {"retrieved_docs": [], "sources": [], "rag_error":
            "문서 검색에 실패했습니다. Pinecone 설정, 인덱스와 BM25 파일을 확인해 주세요."}
