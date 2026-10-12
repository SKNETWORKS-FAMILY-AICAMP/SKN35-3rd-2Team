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


def chat_result(answer="", *, status="success", code=None, message=None, sources=None, image_analysis=None):
    return {
        "status": status, "answer": answer, "sources": sources or [],
        "image_analysis": image_analysis,
        "error": {"code": code, "message": message} if code else None,
    }


# 이미지만 올리고 질문을 쓰지 않았을 때 그래프에 넘기는 질문
IMAGE_ONLY_QUESTION = "첨부한 이미지를 확인하고 문제의 원인과 해결 방법을 알려 주세요."


def prepare_images(images):
    """첨부 이미지를 DB 한도에 맞춘다: 장수와 형식을 확인하고, 한 장이 크기 한도보다 크면 줄여서 쓴다.

    문제가 있으면 사용자에게 그대로 보여 줄 수 있는 문장으로 ValueError를 낸다.
    """
    items = [bytes(data) for data in (images or []) if data]
    if not items:
        return []
    from src.db.images import max_image_bytes, max_images_per_message, shrink_image, sniff_mime

    if len(items) > max_images_per_message():
        raise ValueError(f"이미지는 한 번에 {max_images_per_message()}장까지 첨부할 수 있어요.")
    prepared = []
    for number, data in enumerate(items, 1):
        if sniff_mime(data) is None:
            raise ValueError(f"이미지 {number}은(는) png, jpeg, webp 형식이 아니에요.")
        if len(data) > max_image_bytes():
            try:
                data, _ = shrink_image(data)
            except (ValueError, RuntimeError) as error:
                raise ValueError(f"이미지 {number}을(를) {max_image_bytes() // 1_000_000}MB 이하로 줄이지 못했어요. 더 작은 이미지를 올려 주세요.") from error
        prepared.append(data)
    return prepared


def get_graph():
    # Keep dev's checkpointer unchanged. Each request owns its graph and checkpoints.
    from src.graph.workflow import workflow
    return workflow()


def unsupported_result():
    return chat_result(status="unsupported", code="UNSUPPORTED_ROUTE", message=
        "문서 검색·외부 조회·이미지 분석은 준비 중입니다. 현재는 일반 질문에 답변합니다.")


def result_sources(result):
    """그래프 결과(RAG 문서, MCP 결과)에서 화면과 DB가 같이 쓰는 출처 목록을 만든다.

    출처를 만들지 못해도(예: DB 패키지가 없는 환경) 답변은 그대로 낸다.
    """
    try:
        from src.db import build_sources

        return build_sources(result.get("retrieved_docs"), result.get("mcp_results"))
    except Exception:
        return []


def run_chat(messages, *, conversation_id=None, graph=None, images=None):
    """Send full bounded history to a fresh graph, using the DB conversation ID.

    Without a DB conversation, temporary UI requests keep their own UUID.
    An injected graph is for tests only; DB calls always construct a fresh graph.
    images: 첨부 이미지(바이트 목록). 그래프의 State.image로 넘어가고, Supervisor가 multimodal을 골라 읽는다.
    """
    try:
        images = prepare_images(images)
    except ValueError as error:
        return chat_result(status="error", code="INVALID_IMAGE", message=str(error))
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
        "image": images or None, "image_analysis": "", "retrieved_docs": [],
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
        analysis = text_content(result.get("image_analysis")) if images else ""
        return chat_result(answer, sources=result_sources(result), image_analysis=analysis or None)
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


def run_db_chat(question, *, user_id, conversation_id=None, images=None):
    """Save the question, fetch bounded DB history once, run a fresh graph, save reply.

    user_id must come from authenticated session state, never from a chat input.
    A returned conversation_id lets the UI continue the same conversation even
    if the model failed after the user's question was saved.
    images: 첨부 이미지(바이트 목록). 질문과 함께 DB에 저장하고(원본과 썸네일), 그래프로 넘겨 읽은 글(image_analysis)을 답변과 함께 저장한다.
    """
    try:
        images = prepare_images(images)
    except ValueError as error:
        return chat_result(status="error", code="INVALID_IMAGE", message=str(error))
    if not isinstance(question, str) or (not question.strip() and not images) or type(user_id) is not int or user_id <= 0 or (
        conversation_id is not None and (type(conversation_id) is not int or conversation_id <= 0)
    ):
        return chat_result(status="error", code="INVALID_INPUT", message="질문과 로그인 정보를 확인해 주세요.")
    current_id = conversation_id
    try:
        from src.db import db_session, get_history_context, record_user_turn, record_assistant_turn
        with db_session() as session:
            turn = record_user_turn(session, user_id, question, conversation_id=conversation_id, images=images or None)
            history = get_history_context(session, turn.conversation_id, user_id)
        current_id = turn.conversation_id
        if images and history and history[-1]["role"] == "user" and not history[-1]["content"].strip():
            history[-1] = {**history[-1], "content": IMAGE_ONLY_QUESTION}  # 이미지만 올린 질문
        # history already includes the current question; do not append it again.
        result = run_chat(history, conversation_id=current_id, images=images)
        result["conversation_id"] = current_id
        if result["status"] == "success":
            with db_session() as session:
                record_assistant_turn(session, user_id, current_id, result["answer"],
                    user_message_id=turn.message_id, sources=result["sources"],
                    image_analysis=result.get("image_analysis") or None)
        return result
    except PermissionError:
        result = chat_result(status="error", code="CONVERSATION_ACCESS_DENIED",
            message="대화가 없거나 접근할 수 없습니다.")
    except ValueError as error:
        # 이미지 오류(장수, 크기, 형식 등)는 그대로 알려 준다. 그 밖의 입력 오류는 기존 안내를 쓴다.
        result = chat_result(status="error", code="INVALID_INPUT",
            message=str(error) if images else "질문 길이와 입력 정보를 확인해 주세요.")
    except Exception:
        result = chat_result(status="error", code="DB_ERROR",
            message="대화를 읽거나 저장하지 못했습니다. DB 연결 상태를 확인해 주세요.")
    result["conversation_id"] = current_id
    return result
