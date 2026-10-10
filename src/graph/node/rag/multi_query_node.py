from src.graph.state import RAGState
from src.rag.multi_query import multi_query


def multi_query_node(state: RAGState):
    question = (
        state["rewritten_question"]
        if state["rewritten_question"]
        else state["original_question"]
    )

    query_list = multi_query(question)

    return {"multi_questions": query_list}
