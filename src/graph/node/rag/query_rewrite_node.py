from src.graph.state import RAGState
from src.rag.query_rewrite import query_rewrite


def query_rewrite_node(state: RAGState):
    rewritten_question = query_rewrite(state["original_question"])

    return {"rewritten_question": rewritten_question}
