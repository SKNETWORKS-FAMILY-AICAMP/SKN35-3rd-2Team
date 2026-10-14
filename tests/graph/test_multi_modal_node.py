"""
이미지 입력 노드(src/graph/node/multi_modal)와 단계 함수(src/multi_modal) 시험. 실제 모델은 부르지 않고 가짜 모델로 바꿔 끼운다.
실행: uv run pytest tests/graph -q
"""

import io

import pytest
from PIL import Image

from src.const import db_config as limits
from src.const import multi_modal_config as cfg
from src.multi_modal import read_images as read_images_module
from src.multi_modal.build_analysis import build_analysis
from src.multi_modal.encode_images import encode_images
from src.agent.multi_modal_agent import multi_modal_node
from src.multi_modal.resize_images import resize_images
from src.multi_modal.validate_images import ImageItem, sniff_mime, validate_images


def make_image(fmt="PNG", size=(120, 80), color=(200, 30, 30)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", size, color).save(buf, fmt)
    return buf.getvalue()


SAMPLE_OUTPUT = """[화면 설명]
터미널 화면
[오류 메시지]
ModuleNotFoundError: No module named 'requests'
[코드]
import requests
    print(requests.get)
[환경 정보]
Python 3.12
[읽기 불확실]
없음"""


class FakeModel:
    def __init__(self, text=SAMPLE_OUTPUT, error=None):
        self.text, self.error, self.calls = text, error, []

    def invoke(self, messages, **kwargs):
        self.calls.append((messages, kwargs))
        if self.error:
            raise self.error

        class Reply:
            content = self.text

        return Reply()


@pytest.fixture
def fake_model(monkeypatch):
    model = FakeModel()
    monkeypatch.setattr(read_images_module, "create_openai_model", lambda **kwargs: model)
    return model


# ---------------------------------------------------------------- 1) 검사
def test_validate_accepts_bytes_dict_and_list():
    one = make_image()
    assert len(validate_images(one)[0]) == 1
    assert len(validate_images({"data": one, "name": "a.png"})[0]) == 1
    items, notes = validate_images([one, {"data": make_image("JPEG")}])
    assert [i.number for i in items] == [1, 2] and not notes
    assert [i.mime for i in items] == ["image/png", "image/jpeg"]
    assert (items[0].width, items[0].height) == (120, 80)


def test_validate_none_and_unknown_type():
    assert validate_images(None) == ([], [])
    items, notes = validate_images(12345)
    assert items == [] and "State.image" in notes[0]


def test_validate_rejects_by_real_bytes_not_name():
    items, notes = validate_images({"data": b"GIF89a....", "name": "fake.png"})
    assert items == [] and "png, jpeg, webp" in notes[0]


def test_validate_rejects_broken_empty_and_oversize():
    broken = make_image()[:40]
    items, notes = validate_images([broken, b"", make_image()])
    assert [i.number for i in items] == [3]  # 번호는 올린 순서 그대로
    assert len(notes) == 2
    big = b"\x89PNG\r\n\x1a\n" + b"0" * (limits.DEFAULT_IMAGE_MAX_BYTES + 1)
    assert "넘습니다" in validate_images(big)[1][0]


def test_validate_limits_count():
    imgs = [make_image() for _ in range(limits.DEFAULT_IMAGE_MAX_PER_MESSAGE + 2)]
    items, notes = validate_images(imgs)
    assert len(items) == limits.DEFAULT_IMAGE_MAX_PER_MESSAGE
    assert "앞의" in notes[0]


def test_sniff_mime_formats():
    assert sniff_mime(make_image("PNG")) == "image/png"
    assert sniff_mime(make_image("JPEG")) == "image/jpeg"
    assert sniff_mime(make_image("WEBP")) == "image/webp"
    assert sniff_mime(b"not an image") is None


# ---------------------------------------------------------------- 2) 줄이기
def test_resize_keeps_small_image_untouched():
    item = validate_images(make_image(size=(300, 200)))[0][0]
    out, notes = resize_images([item])
    assert out[0] is item and notes == []


def test_resize_shrinks_big_image_and_keeps_aspect():
    big = make_image(size=(cfg.RESIZE_MAX_EDGE * 2, cfg.RESIZE_MAX_EDGE))
    item = validate_images(big)[0][0]
    out, notes = resize_images([item])
    assert max(out[0].width, out[0].height) == cfg.RESIZE_MAX_EDGE
    assert (out[0].width, out[0].height) == (cfg.RESIZE_MAX_EDGE, cfg.RESIZE_MAX_EDGE // 2)
    assert out[0].number == item.number and out[0].mime == "image/png"
    assert "줄여" in notes[0]


def test_resize_webp_becomes_png_and_jpeg_stays_jpeg():
    size = (cfg.RESIZE_MAX_EDGE + 400, 300)
    webp = validate_images(make_image("WEBP", size=size))[0][0]
    jpeg = validate_images(make_image("JPEG", size=size))[0][0]
    out, _ = resize_images([webp, jpeg])
    assert [i.mime for i in out] == ["image/png", "image/jpeg"]
    assert all(sniff_mime(i.data) == i.mime for i in out)


def test_resize_failure_keeps_original_and_notes():
    item = ImageItem(1, b"broken", "image/png", cfg.RESIZE_MAX_EDGE + 1, 10)
    out, notes = resize_images([item])
    assert out == [item] and "줄이지 못해" in notes[0]


# ---------------------------------------------------------------- 3) 변환
def test_encode_builds_labeled_data_urls():
    items = validate_images([make_image(), make_image("JPEG")])[0]
    parts = encode_images(items)
    assert [p["type"] for p in parts] == ["text", "image_url", "text", "image_url"]
    assert parts[0]["text"] == "[이미지 1]" and parts[2]["text"] == "[이미지 2]"
    assert parts[1]["image_url"]["url"].startswith("data:image/png;base64,")
    assert parts[3]["image_url"]["url"].startswith("data:image/jpeg;base64,")
    assert parts[1]["image_url"]["detail"] == cfg.IMAGE_DETAIL


# ---------------------------------------------------------------- 5) 정리
def test_build_orders_sections_and_fills_empty():
    text = build_analysis("[오류 메시지]\nTypeError: x\n[화면 설명]\n터미널", [])
    positions = [text.index(h) for h in cfg.SECTION_HEADINGS]
    assert positions == sorted(positions)  # 항상 정해진 순서
    assert "TypeError: x" in text
    assert text.count(cfg.EMPTY_SECTION_TEXT) == 4  # 코드, 환경 정보, 화면 속 글자, 읽기 불확실


def test_build_keeps_code_indentation_and_markdown_headings():
    text = build_analysis("**[코드]**\ndef f():\n    return 1\n## [환경 정보] Python 3.12", [])
    assert "def f():\n    return 1" in text
    assert "[환경 정보]\nPython 3.12" in text


def test_build_without_format_keeps_raw_and_notes_it():
    text = build_analysis("그냥 설명입니다", [])
    assert "그냥 설명입니다" in text and "항목 형식이 아니어서" in text
    assert "[화면 설명]" not in text  # 항목을 지어내지 않는다


def test_build_masks_secrets():
    key = "sk-" + "a1B2c3D4e5F6g7H8i9J0k1L2"
    text = build_analysis(f"[코드]\nOPENAI_API_KEY={key}\nclient = OpenAI(api_key='{key}')", [])
    assert key not in text and "[MASKED" in text


def test_build_none_cases():
    assert build_analysis(None, []) == cfg.NO_IMAGE_NOTICE
    assert build_analysis(None, ["문제가 있었습니다"]) == "※ 문제가 있었습니다"
    assert cfg.EMPTY_RESULT_NOTICE in build_analysis("   ", [])


def test_build_prepends_notes_and_clips():
    assert build_analysis(SAMPLE_OUTPUT, ["일부만 읽음"]).startswith("※ 일부만 읽음\n\n[화면 설명]")
    # 공백 없이 이어진 긴 글자열은 mask_secrets가 매우 느려지는 알려진 문제가 있어서(src/db/masking.py), 단어로 채운다
    long = build_analysis("[코드]\n" + "ab " * (limits.IMAGE_ANALYSIS_MAX_CHARS // 3 + 50), [])
    assert long.endswith(limits.CLIP_SUFFIX)


# ---------------------------------------------------------------- 노드 전체
def test_node_full_pipeline_with_fake_model(fake_model):
    state = {"original_question": "이 오류 어떻게 해결해?", "image": [make_image(), make_image("JPEG")]}
    result = multi_modal_node(state)
    assert set(result) == {"image_analysis", "original_question", "completed_routes"} and result["completed_routes"] == ["multi_modal"]
    assert "ModuleNotFoundError" in result["image_analysis"]

    assert len(fake_model.calls) == 1  # 이미지가 여러 장이어도 모델은 한 번만 부른다
    messages, kwargs = fake_model.calls[0]
    assert kwargs["max_tokens"] == cfg.VISION_MAX_OUTPUT_TOKENS
    user_parts = messages[1]["content"]
    assert user_parts[0]["text"] == "사용자의 질문: 이 오류 어떻게 해결해?"
    assert sum(p["type"] == "image_url" for p in user_parts) == 2
    assert "답하지 않는다" in messages[0]["content"]


def test_node_uses_last_message_when_no_original_question(fake_model):
    multi_modal_node({"image": make_image(), "messages": [{"role": "user", "content": "마지막 질문"}]})
    assert "마지막 질문" in fake_model.calls[0][0][1]["content"][0]["text"]


def test_node_image_only_question(fake_model):
    multi_modal_node({"image": make_image()})
    assert "이미지만 올림" in fake_model.calls[0][0][1]["content"][0]["text"]


def test_node_no_image_does_not_call_model(fake_model):
    assert multi_modal_node({"original_question": "q"}) == {"image_analysis": cfg.NO_IMAGE_NOTICE, "completed_routes": ["multi_modal"]}
    assert fake_model.calls == []


def test_node_all_images_invalid_does_not_call_model(fake_model):
    result = multi_modal_node({"image": [b"junk", b""]})
    assert "건너뛰었습니다" in result["image_analysis"] and fake_model.calls == []


def test_node_model_failure_is_reported_not_raised(monkeypatch):
    model = FakeModel(error=RuntimeError("boom api_key=sk-" + "Z" * 30))
    monkeypatch.setattr(read_images_module, "create_openai_model", lambda **kwargs: model)
    result = multi_modal_node({"image": make_image()})["image_analysis"]
    assert "이미지 분석에 실패했습니다" in result and "RuntimeError" in result
    assert "Z" * 30 not in result  # 오류 문구에 섞인 키도 가린다


def test_node_missing_key_is_reported_not_raised(monkeypatch):
    def no_key(**kwargs):
        raise ValueError("OPENAI_API_KEY 설정이 필요합니다.")

    monkeypatch.setattr(read_images_module, "create_openai_model", no_key)
    assert "설정이 필요합니다" in multi_modal_node({"image": make_image()})["image_analysis"]


def test_node_notes_about_skipped_and_resized(fake_model):
    big = make_image(size=(cfg.RESIZE_MAX_EDGE + 500, 400))
    result = multi_modal_node({"image": [b"junk", big]})["image_analysis"]
    assert result.startswith("※ 이미지 1은(는) 읽을 수 없어")
    assert "이미지 2은(는) 크기가 커서" in result
    sent = fake_model.calls[0][0][1]["content"]
    assert "[이미지 2]" in [p.get("text") for p in sent] and "[이미지 1]" not in [p.get("text") for p in sent]


# ---------------------------------------------------------------- completed_routes (Supervisor가 끝난 route를 알게 한다)
def test_node_adds_multi_modal_to_the_completed_routes_in_every_case(fake_model, monkeypatch):
    ok = multi_modal_node({"original_question": "q", "image": make_image(), "completed_routes": ["rag"]})
    assert ok["completed_routes"] == ["rag", "multi_modal"]  # 앞선 route는 그대로 둔다
    assert multi_modal_node({"original_question": "q"})["completed_routes"] == ["multi_modal"]  # 이미지가 없을 때
    assert multi_modal_node({"original_question": "q", "image": [b"junk"]})["completed_routes"] == ["multi_modal"]  # 모두 건너뛴 경우
    monkeypatch.setattr(read_images_module, "create_openai_model", lambda **kwargs: FakeModel(error=RuntimeError("boom")))
    assert multi_modal_node({"original_question": "q", "image": make_image()})["completed_routes"] == ["multi_modal"]  # 모델 호출이 실패한 경우


# ---------------------------------------------------------------- 읽은 내용을 질문에 붙이기
def test_read_content_is_attached_to_the_question(fake_model):
    state = {"original_question": "이미지를 확인해 주세요", "image": [make_image()]}
    question = multi_modal_node(state)["original_question"]
    assert question.startswith("이미지를 확인해 주세요\n\n" + cfg.IMAGE_CONTEXT_MARKER + "\n")
    assert "ModuleNotFoundError" in question  # 검색어와 도구 선택이 실제 오류 문구를 볼 수 있다


def test_question_is_not_attached_twice(fake_model):
    state = {"original_question": "q\n\n" + cfg.IMAGE_CONTEXT_MARKER + "\n이미 붙어 있음", "image": [make_image()]}
    assert multi_modal_node(state)["original_question"] == state["original_question"]


def test_attached_content_is_clipped(fake_model, monkeypatch):
    monkeypatch.setattr(cfg, "QUESTION_IMAGE_MAX_CHARS", 20)
    question = multi_modal_node({"original_question": "q", "image": [make_image()]})["original_question"]
    assert question.endswith(cfg.QUESTION_CLIP_SUFFIX)
    assert len(question) < 120


def test_question_is_left_alone_when_nothing_was_read(fake_model):
    assert "original_question" not in multi_modal_node({"original_question": "q"})  # 이미지 없음
    assert "original_question" not in multi_modal_node({"original_question": "q", "image": [b"junk"]})  # 읽을 이미지 없음


# ---------------------------------------------------------------- 구조도·표처럼 오류가 없는 이미지
def test_screen_text_section_is_kept_between_environment_and_uncertain():
    assert cfg.SECTION_HEADINGS.index("[화면 속 글자]") == cfg.SECTION_HEADINGS.index("[환경 정보]") + 1
    assert cfg.SECTION_HEADINGS[-1] == "[읽기 불확실]"


def test_diagram_text_without_errors_or_code_is_not_lost():
    raw = "[화면 설명]\n흐름도\n[화면 속 글자]\nSupervisor\n질의 분석 · 동적 라우팅\nMCP 도구 실행"
    text = build_analysis(raw, [])
    assert "Supervisor" in text and "MCP 도구 실행" in text
    assert text.index("[화면 속 글자]") < text.index("[읽기 불확실]")


def test_prompt_asks_for_diagram_structure_and_all_visible_text():
    from src.prompt.multi_modal_prompt import MULTI_MODAL_SYSTEM_PROMPT as prompt

    assert "[화면 속 글자]" in prompt and "구조도" in prompt and "화살표" in prompt


# ---------------------------------------------------------------- 하위 그래프 (단계마다 노드)
def _visited(state):
    from src.agent.multi_modal_agent import multi_modal_agent

    order = []
    for event in multi_modal_agent().stream(state, stream_mode="updates"):
        order.extend(event)
    return order


def test_graph_visits_all_five_nodes_in_order(fake_model):
    assert _visited({"original_question": "q", "image": [make_image()]}) == [
        "validate_images", "resize_images", "encode_images", "read_images", "build_analysis"]


def test_graph_skips_to_build_analysis_when_no_readable_image(fake_model):
    assert _visited({"original_question": "q", "image": [b"junk"]}) == ["validate_images", "build_analysis"]
    assert fake_model.calls == []


def test_graph_goes_straight_to_build_analysis_when_encoding_fails(fake_model, monkeypatch):
    from src.graph.node.multi_modal import encode_images_node as module

    def boom(images):
        raise RuntimeError("encode boom")

    monkeypatch.setattr(module, "encode_images", boom)
    assert _visited({"original_question": "q", "image": [make_image()]}) == [
        "validate_images", "resize_images", "encode_images", "build_analysis"]
    assert fake_model.calls == []
    assert "이미지 분석에 실패했습니다" in multi_modal_node({"original_question": "q", "image": [make_image()]})["image_analysis"]


def test_main_state_does_not_receive_image_bytes_or_base64(fake_model):
    result = multi_modal_node({"original_question": "q", "image": [make_image()]})
    assert set(result) == {"image_analysis", "original_question", "completed_routes"}
