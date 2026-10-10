from langgraph.graph import END, START, StateGraph

from src.graph.node.rag.context_compressor_node import context_compressor_node
from src.graph.node.rag.multi_query_node import multi_query_node
from src.graph.node.rag.query_rewrite_node import query_rewrite_node
from src.graph.node.rag.rerank_node import rerank_node
from src.graph.node.rag.retriever_node import retriever_node
from src.graph.node.rag.rrf_node import rrf_node
from src.graph.state import RAGState


def rag_agent():

    builder = StateGraph(RAGState)

    builder.add_node("query_rewrite", query_rewrite_node)
    builder.add_node("retriever", retriever_node)
    builder.add_node("multi_query", multi_query_node)
    builder.add_node("rrf", rrf_node)
    builder.add_node("rerank", rerank_node)
    builder.add_node("context_compressor", context_compressor_node)

    builder.add_edge(START, "query_rewrite")

    # 이후로 계속 그래프 만들 예정

    builder.add_edge("context_compressor", END)

    rag_graph = builder.compile()

    return rag_graph
