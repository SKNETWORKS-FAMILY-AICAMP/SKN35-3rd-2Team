"""UI-facing text contract; no DB access and no per-user graph memory."""
from functools import lru_cache

from langchain_core.messages import AIMessage


def text_content(content):
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return "\n".join(
            block if isinstance(block, str) else block.get("text", "")
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


@lru_cache(maxsize=1)
def get_graph():
    from src.graph.workflow import workflow
    return workflow()


def run_chat(messages, *, graph=None):
    """messages includes the current question exactly once, as its last item."""
    if not isinstance(messages, list) or not messages or any(
        not isinstance(m, dict) or m.get("role") not in ("system", "user", "assistant")
        or not isinstance(m.get("content"), str) for m in messages
    ) or messages[-1]["role"] != "user" or not messages[-1]["content"].strip():
        return chat_result(status="error", code="INVALID_INPUT", message="질문을 입력해 주세요.")
    state = {
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
        "original_question": messages[-1]["content"],
        "image": None, "image_analysis": "", "retrieved_docs": [],
        "mcp_results": [], "answer": "", "sources": [], "rag_error": "",
    }
    try:
        result = (graph if graph is not None else get_graph()).invoke(state)
        if result.get("rag_error"):
            return chat_result(status="error", code="RAG_ERROR", message=result["rag_error"])
        route = result.get("route")
        unsupported = {
            "mcp": "외부 정보 조회 기능은 아직 연결 중입니다.",
            "multimodal": "이미지 분석 기능은 아직 연결 중입니다.",
        }
        if route in unsupported:
            return chat_result(status="unsupported", code="UNSUPPORTED_ROUTE", message=unsupported[route])
        replies = result.get("messages", [])
        if not replies or not isinstance(replies[-1], AIMessage):
            return chat_result(status="error", code="EMPTY_RESPONSE", message="AI 답변을 받지 못했습니다.")
        answer = text_content(result.get("answer")) or text_content(replies[-1].content)
        if not answer:
            return chat_result(status="error", code="EMPTY_RESPONSE", message="AI 답변이 비어 있습니다.")
        return chat_result(answer, sources=result.get("sources", []))
    except Exception as error:
        name = type(error).__name__
        notices = {
            "AuthenticationError": "OpenAI 인증에 실패했습니다. API 키를 확인해 주세요.",
            "RateLimitError": "OpenAI 사용 한도 또는 요청 제한에 도달했습니다.",
            "NotFoundError": "설정된 OpenAI 모델을 사용할 수 없습니다.",
            "APITimeoutError": "답변 대기 시간이 초과되었습니다. 다시 시도해 주세요.",
        }
        return chat_result(status="error", code="GRAPH_ERROR", message=notices.get(
            name, "답변을 받지 못했습니다. OpenAI 설정과 인터넷 연결을 확인해 주세요."
        ))
