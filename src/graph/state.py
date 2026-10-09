from typing import Any, NotRequired

from langgraph.graph import MessagesState


class State(MessagesState):
    original_question: str

    image: NotRequired[Any]
    image_analysis: NotRequired[str]

    retrieved_docs: NotRequired[list]
    mcp_results: NotRequired[list]

    route: NotRequired[str]
    reason: NotRequired[str]

    answer: NotRequired[str]
    sources: NotRequired[list[dict]]
    rag_error: NotRequired[str]
