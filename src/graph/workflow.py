from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from src.agent.answer_agent import answer_agent
from src.agent.general_agent import general_agent
from src.agent.rag_agent import rag_agent
from src.graph.node.supervisor_node import supervisor_node
from src.graph.state import State


def route_from_supervisor(state):
    print("route_from_supervisor 진입", end="\n\n")

    print("선택된 Agent : ", state["route"], end="\n\n")
    return state["route"]


def workflow():
    builder = StateGraph(State)

    builder.add_node("supervisor", supervisor_node)
    builder.add_node("general", general_agent())
    builder.add_node("answer", answer_agent())
    builder.add_node("rag", rag_agent())
    builder.add_edge(START, "supervisor")

    builder.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {"rag": "rag", "general": "general", "answer": "answer"},
    )

    builder.add_edge("general", END)
    builder.add_edge("answer", END)
    builder.add_edge("rag", END)
    memory = InMemorySaver()

    graph = builder.compile(checkpointer=memory)

    return graph


if __name__ == "__main__":
    config = {"configurable": {"thread_id": "user_001"}}

    graph = workflow()

    result = graph.invoke(
        {
            "messages": [{"role": "user", "content": "코딩 잘하는 법 알려줘."}],
            "original_question": "코딩 잘하는 법 알려줘.",
        },
        config=config,
    )

    print("최종 답변 : ", result)
