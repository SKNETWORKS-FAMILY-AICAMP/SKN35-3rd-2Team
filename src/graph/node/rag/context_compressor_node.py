from src.graph.state import RAGState
from src.rag.context_compressor import context_compressor


def context_compressor_node(state: RAGState):
    documents = context_compressor(state["documents"])

    return {"documents": documents}
