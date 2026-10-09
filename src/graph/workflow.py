from langgraph.graph import END, START, StateGraph

from src.agent.answer_agent import answer_agent
from src.agent.general_agent import general_agent
from src.graph.node.supervisor_node import supervisor_node
from src.graph.node.rag_node import rag_node
from src.graph.state import State


def route_from_supervisor(state):
    print("route_from_supervisor 진입", end="\n\n")
    return state["route"]


def route_from_rag(state):
    return END if state.get("rag_error") else "answer"


def workflow():

    # general = general_agent()
    # answer = answer_agent()

    builder = StateGraph(State)

    builder.add_node("supervisor", supervisor_node)
    builder.add_node("general", general_agent())
    builder.add_node("answer", answer_agent())
    builder.add_node("rag", rag_node)
    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {"general": "general", "answer": "answer",
         "rag": "rag", "mcp": END, "multimodal": END},
    )

    builder.add_conditional_edges("rag", route_from_rag, {"answer": "answer", END: END})
    builder.add_edge("general", END)
    builder.add_edge("answer", END)

    # UI/DB supplies the full history on each call; do not accumulate it again.
    graph = builder.compile()

    return graph


if __name__ == "__main__":
    graph = workflow()

    result = graph.invoke(
        {
            "messages": [{"role": "user", "content": "코딩 잘하는 법 알려줘."}],
            "original_question": "코딩 잘하는 법 알려줘.",
        },
    )

    print("최종 답변 : ", result)
