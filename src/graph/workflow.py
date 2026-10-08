from langgraph.graph import StateGraph

from graph.node.supervisor_node import supervisor_node
from src.graph.state import START, State


def supervisor_route(state):
    return state["route"]


builder = StateGraph(State)

builder.add_node("supervisor_node", supervisor_node)

builder.add_edge(START, "supervisor_node")
