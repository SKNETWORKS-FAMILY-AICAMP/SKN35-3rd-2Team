from src.graph.state import RAGState
from src.rag.query_rewrite import query_rewrite


def query_rewrite_node(state: RAGState):
    print("query_rewrite 진입", end="\n\n")
    question = (
        state["rewritten_question"]
        if state["rewritten_question"]
        else state["original_question"]
    )
    rewritten_question = query_rewrite(question)

    return {"rewritten_question": rewritten_question}
