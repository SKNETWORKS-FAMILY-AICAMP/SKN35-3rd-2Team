"""UI adapter for the unchanged team graph; no retrieval or routing implementation."""
from uuid import uuid4

from langchain_core.messages import AIMessage


def text_content(content):
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return "\n".join(
            block if isinstance(block, str) else block["text"]
            for block in content
            if isinstance(block, str) or (
                isinstance(block, dict) and block.get("type") in ("text", "output_text")
                and isinstance(block.get("text"), str)
            )
        ).strip()
    return ""


def chat_result(answer="", *, status="success", code=None, message=None, sources=None):
    return {
        "status": status, "answer": answer, "sources": sources or [],
        "image_analysis": None,
        "error": {"code": code, "message": message} if code else None,
    }


def get_graph():
    # Keep dev's checkpointer unchanged. Each request owns its graph and checkpoints.
    from src.graph.workflow import workflow
    return workflow()


def unsupported_result():
    return chat_result(status="unsupported", code="UNSUPPORTED_ROUTE", message=
        "문서 검색·외부 조회·이미지 분석은 준비 중입니다. 현재는 일반 질문에 답변합니다.")


def run_chat(messages, *, graph=None):
    """Pass complete history once, under a new request thread to avoid accumulation."""
    if not isinstance(messages, list) or not messages or any(
        not isinstance(m, dict) or m.get("role") not in ("system", "user", "assistant")
        or not isinstance(m.get("content"), str) for m in messages
    ) or messages[-1]["role"] != "user" or not messages[-1]["content"].strip():
        return chat_result(status="error", code="INVALID_INPUT", message="질문을 입력해 주세요.")
    state = {
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
        "original_question": messages[-1]["content"],
        "image": None, "image_analysis": "", "retrieved_docs": [],
        "mcp_results": [], "answer": "",
    }
    config = {"configurable": {"thread_id": str(uuid4())}}
    try:
        result = (graph if graph is not None else get_graph()).invoke(state, config=config)
        if result.get("route") in ("rag", "mcp", "multimodal"):
            return unsupported_result()
        replies = result.get("messages", [])
        if not replies or not isinstance(replies[-1], AIMessage):
            return chat_result(status="error", code="EMPTY_RESPONSE", message="AI 답변을 받지 못했습니다.")
        answer = text_content(result.get("answer")) or text_content(replies[-1].content)
        if not answer:
            return chat_result(status="error", code="EMPTY_RESPONSE", message="AI 답변이 비어 있습니다.")
        return chat_result(answer)
    except Exception as error:
        # dev's conditional edge mapping has no destinations for these routes.
        # Recognize that existing contract failure without changing graph internals.
        if isinstance(error, KeyError) and error.args in (("rag",), ("mcp",), ("multimodal",)):
            return unsupported_result()
        notices = {
            "AuthenticationError": "OpenAI 인증에 실패했습니다. API 키를 확인해 주세요.",
            "RateLimitError": "OpenAI 사용 한도 또는 요청 제한에 도달했습니다.",
            "NotFoundError": "설정된 OpenAI 모델을 사용할 수 없습니다.",
            "APITimeoutError": "답변 대기 시간이 초과되었습니다. 다시 시도해 주세요.",
        }
        return chat_result(status="error", code="GRAPH_ERROR", message=notices.get(
            type(error).__name__, "답변을 받지 못했습니다. 모델 설정과 인터넷 연결을 확인해 주세요."
        ))
