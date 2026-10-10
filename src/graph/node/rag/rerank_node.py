from src.graph.state import RAGState
from src.rag.rerank import rerank


def rerank_node(state: RAGState):
    documents = rerank(state["documents"], state["rewritten_question"], top_n=5)

    return {"documents": documents}
