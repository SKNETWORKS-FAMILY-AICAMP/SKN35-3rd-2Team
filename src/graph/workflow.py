from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from src.agent.answer_agent import answer_agent
from src.agent.general_agent import general_agent
from src.agent.rag_agent import rag_node
from src.graph.node.supervisor_node import supervisor_node
from src.graph.state import State


def reset_turn_state_node(state):
    print("reset_turn_state 진입", end="\n\n")

    return {
        "route": "",
        "reason": "",
        "completed_routes": [],
        "retrieved_docs": [],
        "mcp_results": [],
        "answer": "",
    }


def route_from_supervisor(state):
    print("route_from_supervisor 진입", end="\n\n")

    print("선택된 Agent : ", state["route"], end="\n\n")
    return state["route"]


def workflow():
    builder = StateGraph(State)

    builder.add_node("reset_turn_state", reset_turn_state_node)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("general", general_agent())
    builder.add_node("answer", answer_agent())
    builder.add_node("rag", rag_node)

    builder.add_edge(START, "reset_turn_state")
    builder.add_edge("reset_turn_state", "supervisor")

    builder.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {"rag": "rag", "general": "general", "answer": "answer"},
    )

    builder.add_edge("rag", "supervisor")

    builder.add_edge("general", END)
    builder.add_edge("answer", END)

    memory = InMemorySaver()

    graph = builder.compile(checkpointer=memory)

    return graph


if __name__ == "__main__":
    TEST_QUESTIONS = [
        "Python에서 ModuleNotFoundError: No module named langchain' 오류가 나요. 무엇부터 확인해야 하나요?",
        "LangGraph로 만든 RAG에서 검색 결과가 없으면 재검색을 반복하다가 GraphRecursionError가 발생해요. 재시도 횟수를 제한하고 정상 종료하려면 어떻게 해야 하나요? 문서 근거도 알려주세요.",
        '그럼 방금 설명한 방법을 적용해서, 최대 3번까지만 재검색하고 그래도 자료가 없으면 "관련 자료를 찾지 못했습니다"라고 종료하는 코드 예시를 보여주세요.',
        "우리 회사 내부 전용 LLM 라이브러리 EunhaPrivateLLM에서 EH-RAG-9042 오류가 발생했어요. 내부 매뉴얼에 나온 정확한 원인과 해결 명령어를 알려주세요.",
    ]

    config = {"configurable": {"thread_id": "user_001"}}

    graph = workflow()

    for turn, question in enumerate(TEST_QUESTIONS, start=1):
        print("=" * 80)
        print(f"[질문 {turn}] {question}")
        print("=" * 80, end="\n\n")

        result = graph.invoke(
            {
                "messages": [{"role": "user", "content": question}],
                "original_question": question,
            },
            config=config,
        )

        print(f"\n[답변 {turn}] {result['messages'][-1].content}\n")
