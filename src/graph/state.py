from typing import Any, NotRequired

from langchain_core.documents import Document
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


class RAGState(MessagesState):
    original_question: str
    rewritten_question: NotRequired[str]
    documents: NotRequired[list[Document]]
    context: NotRequired[str]
    multi_questions: NotRequired[list[str]]
    multi_questions_documents: NotRequired[list[list[Document]]]
