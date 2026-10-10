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


def run_chat(messages, *, conversation_id=None, graph=None):
    """Send full bounded history to a fresh graph, using the DB conversation ID.

    Without a DB conversation, temporary UI requests keep their own UUID.
    An injected graph is for tests only; DB calls always construct a fresh graph.
    """
    if conversation_id is not None and (
        type(conversation_id) is not int or conversation_id <= 0
    ):
        return chat_result(status="error", code="INVALID_INPUT", message="대화 정보를 확인해 주세요.")
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
    config = {"configurable": {"thread_id": str(conversation_id) if conversation_id is not None else str(uuid4())}}
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


def run_db_chat(question, *, user_id, conversation_id=None):
    """Save the question, fetch bounded DB history once, run a fresh graph, save reply.

    user_id must come from authenticated session state, never from a chat input.
    A returned conversation_id lets the UI continue the same conversation even
    if the model failed after the user's question was saved.
    """
    if not isinstance(question, str) or not question.strip() or type(user_id) is not int or user_id <= 0 or (
        conversation_id is not None and (type(conversation_id) is not int or conversation_id <= 0)
    ):
        return chat_result(status="error", code="INVALID_INPUT", message="질문과 로그인 정보를 확인해 주세요.")
    current_id = conversation_id
    try:
        from src.db import db_session, get_history_context, record_user_turn, record_assistant_turn
        with db_session() as session:
            turn = record_user_turn(session, user_id, question, conversation_id=conversation_id)
            history = get_history_context(session, turn.conversation_id, user_id)
        current_id = turn.conversation_id
        # history already includes the current question; do not append it again.
        result = run_chat(history, conversation_id=current_id)
        result["conversation_id"] = current_id
        if result["status"] == "success":
            with db_session() as session:
                record_assistant_turn(session, user_id, current_id, result["answer"],
                    user_message_id=turn.message_id, sources=result["sources"])
        return result
    except PermissionError:
        result = chat_result(status="error", code="CONVERSATION_ACCESS_DENIED",
            message="대화가 없거나 접근할 수 없습니다.")
    except ValueError:
        result = chat_result(status="error", code="INVALID_INPUT",
            message="질문 길이와 입력 정보를 확인해 주세요.")
    except Exception:
        result = chat_result(status="error", code="DB_ERROR",
            message="대화를 읽거나 저장하지 못했습니다. DB 연결 상태를 확인해 주세요.")
    result["conversation_id"] = current_id
    return result
