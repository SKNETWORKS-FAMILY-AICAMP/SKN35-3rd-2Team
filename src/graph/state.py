from typing import Any, TypedDict


class State(TypedDict, total=False):
    question: str
    image: Any

    image_analysis: str

    retrieved_docs: list
    mcp_results: list

    route: str
    reason: str

    answer: str
