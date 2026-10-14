"""
이미지 입력 노드: 사용자가 올린 이미지(최대 3장)를 읽어서 항목이 있는 글로 옮긴다.

    State.image  -->  [이 노드]  -->  State.image_analysis (문자열 하나)

이 파일에는 전체 흐름만 있고, 각 단계의 일은 src/multi_modal/ 의 파일이 한다 (rag 노드와 src/rag/ 의 관계와 같다).

    1) validate_images.py  이미지 검사 (장수, 크기, 형식, 깨짐)
    2) resize_images.py    큰 이미지 줄이기
    3) encode_images.py    모델에 보낼 형태(base64)로 바꾸기
    4) read_images.py      모델에 이미지를 한 번에 보내서 읽기
    5) build_analysis.py   항목이 있는 글로 정리, 비밀값 가리기

- Supervisor가 route="multi_modal"을 고르면 실행되고, 끝나면 다시 Supervisor로 돌아간다 (supervisor_prompt 참고).
- 이미지는 "원본 바이트"로 받는다. 화면에 다시 보여 주는 용도의 저장은 이 노드가 아니라 그래프 밖(UI의 record_user_turn)이 한다.
  이 노드는 DB를 모른다.
- 어떤 단계가 실패해도 예외를 던지지 않는다. 실패했다는 안내가 image_analysis에 들어가고 그래프는 계속 진행된다.
- 설정값은 src/const/multi_modal_config.py, 프롬프트는 src/prompt/multi_modal_prompt.py에 있다.
"""

from src.const import multi_modal_config as cfg
from src.db.masking import mask_secrets
from src.multi_modal.build_analysis import build_analysis
from src.multi_modal.encode_images import encode_images
from src.multi_modal.read_images import read_images
from src.multi_modal.resize_images import resize_images
from src.multi_modal.validate_images import validate_images


def _question_text(state: dict) -> str:
    """이미지를 읽을 때 참고할 사용자의 질문 (없으면 빈 문자열)."""
    question = state.get("original_question")
    if isinstance(question, str) and question.strip():
        return question
    messages = state.get("messages") or []
    if not messages:
        return ""
    last = messages[-1]
    content = last.get("content") if isinstance(last, dict) else getattr(last, "content", "")
    return content if isinstance(content, str) else ""


def _question_with_image(state: dict, analysis: str) -> str:
    """질문 글 뒤에 이미지에서 읽은 내용을 붙인다. 이후 RAG(검색어)와 MCP(도구 선택)가 이 글을 질문으로 쓴다.

    이미지만 올려서 질문이 "이미지를 확인해 주세요"뿐이어도, 읽은 오류 문구로 검색할 수 있게 하려는 것이다.
    """
    question = _question_text(state)
    if cfg.IMAGE_CONTEXT_MARKER in question:
        return question
    text = analysis if len(analysis) <= cfg.QUESTION_IMAGE_MAX_CHARS else analysis[: cfg.QUESTION_IMAGE_MAX_CHARS] + cfg.QUESTION_CLIP_SUFFIX
    return question + "\n\n" + cfg.IMAGE_CONTEXT_MARKER + "\n" + text


def multi_modal_node(state):
    # completed_routes에 "multi_modal"을 더해 돌려준다 (rag_node, mcp_node와 같다).
    # Supervisor는 이 목록을 보고 이미 끝낸 route를 다시 고르지 않는다.
    completed = [*(state.get("completed_routes") or []), "multi_modal"]

    # 1) 이미지 검사: 읽을 수 있는 이미지만 남긴다
    images, notes = validate_images(state.get("image"))
    if not images:
        return {"image_analysis": build_analysis(None, notes), "completed_routes": completed}

    # 2) 큰 이미지 줄이기
    images, resize_notes = resize_images(images)
    notes += resize_notes

    try:
        # 3) 모델에 보낼 형태로 바꾸기
        parts = encode_images(images)

        # 4) 이미지를 한 번에 읽기
        raw_text = read_images(parts, _question_text(state))
    except Exception as exc:  # 네트워크, 한도, 키 오류 등으로 그래프 전체가 죽지 않게 한다
        notes.append(f"이미지 분석에 실패했습니다: {type(exc).__name__}: {mask_secrets(str(exc))[:300]}")
        return {"image_analysis": build_analysis(None, notes), "completed_routes": completed}

    # 5) 항목이 있는 글로 정리하고, 읽은 내용을 질문에 붙인다 (읽기에 성공한 경우에만)
    analysis = build_analysis(raw_text, notes)
    return {
        "image_analysis": analysis,
        "original_question": _question_with_image(state, analysis),
        "completed_routes": completed,
    }
