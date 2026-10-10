from src.graph.state import RAGState
from src.rag.rrf import reciprocal_rank_fusion


def rrf_node(state: RAGState):
    documents = reciprocal_rank_fusion(
        state["multi_questions_documents"], k=60, top_n=5
    )

    return {"documents": documents}
