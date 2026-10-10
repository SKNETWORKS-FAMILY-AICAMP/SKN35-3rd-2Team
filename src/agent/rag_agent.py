from langgraph.graph import END, START, StateGraph

from src.graph.node.rag import (
    context_compressor_node,
    multi_query_node,
    query_rewrite_node,
    rerank_node,
    retriever_node,
    rrf_node,
)
from src.graph.state import RAGState

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
