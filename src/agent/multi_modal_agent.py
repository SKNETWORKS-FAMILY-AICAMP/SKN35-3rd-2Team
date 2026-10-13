from langgraph.graph import END, START, StateGraph

from src.graph.node.multi_modal.multi_modal_node import multi_modal_node
from src.graph.state import State


def multi_modal_agent():
    builder = StateGraph(State)

    builder.add_node("multi_modal_node", multi_modal_node)
    builder.add_edge(START, "multi_modal_node")
    builder.add_edge("multi_modal_node", END)

    multi_modal_graph = builder.compile()

    return multi_modal_graph
