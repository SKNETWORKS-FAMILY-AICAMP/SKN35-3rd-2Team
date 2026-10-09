"""
이미지 입력 노드: 사용자가 올린 이미지(최대 3장)를 읽어서 항목이 있는 글로 옮긴다.

    State.image  -->  [이 노드]  -->  State.image_analysis (문자열 하나)

이 파일에는 전체 흐름만 있고, 각 단계의 일은 같은 폴더의 파일이 한다.

    1) validate_images.py  이미지 검사 (장수, 크기, 형식, 깨짐)
    2) resize_images.py    큰 이미지 줄이기
    3) encode_images.py    모델에 보낼 형태(base64)로 바꾸기
    4) read_images.py      모델에 이미지를 한 번에 보내서 읽기
    5) build_analysis.py   항목이 있는 글로 정리, 비밀값 가리기

- Supervisor가 route="multimodal"을 고르면 실행되고, 끝나면 다시 Supervisor로 돌아간다 (supervisor_prompt 참고).
- 이미지는 "원본 바이트"로 받는다. 화면에 다시 보여 주는 용도의 저장은 이 노드가 아니라 그래프 밖(UI의 record_user_turn)이 한다.
  이 노드는 DB를 모른다.
- 어떤 단계가 실패해도 예외를 던지지 않는다. 실패했다는 안내가 image_analysis에 들어가고 그래프는 계속 진행된다.
- 설정값은 src/const/multimodal_config.py, 프롬프트는 src/prompt/multimodal_prompt.py에 있다.
"""

from src.db.masking import mask_secrets
from src.graph.node.multimodal.build_analysis import build_analysis
from src.graph.node.multimodal.encode_images import encode_images
from src.graph.node.multimodal.read_images import read_images
from src.graph.node.multimodal.resize_images import resize_images
from src.graph.node.multimodal.validate_images import validate_images


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


def multimodal_node(state):
    # 1) 이미지 검사: 읽을 수 있는 이미지만 남긴다
    images, notes = validate_images(state.get("image"))
    if not images:
        return {"image_analysis": build_analysis(None, notes)}

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
        return {"image_analysis": build_analysis(None, notes)}

    # 5) 항목이 있는 글로 정리
    return {"image_analysis": build_analysis(raw_text, notes)}
