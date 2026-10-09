"""
이미지 입력 노드(src/graph/node/multimodal) 시험. 실제 모델은 부르지 않고 가짜 모델로 바꿔 끼운다.
실행: uv run pytest tests/graph -q
"""

import io

import pytest
from PIL import Image

from src.const import db_config as limits
from src.const import multimodal_config as cfg
from src.graph.node.multimodal import read_images as read_images_module
from src.graph.node.multimodal.build_analysis import build_analysis
from src.graph.node.multimodal.encode_images import encode_images
from src.graph.node.multimodal.multimodal_node import multimodal_node
from src.graph.node.multimodal.resize_images import resize_images
from src.graph.node.multimodal.validate_images import ImageItem, sniff_mime, validate_images


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
    assert text.count(cfg.EMPTY_SECTION_TEXT) == 3  # 코드, 환경 정보, 읽기 불확실


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
    result = multimodal_node(state)
    assert list(result) == ["image_analysis"]
    assert "ModuleNotFoundError" in result["image_analysis"]

    assert len(fake_model.calls) == 1  # 이미지가 여러 장이어도 모델은 한 번만 부른다
    messages, kwargs = fake_model.calls[0]
    assert kwargs["max_tokens"] == cfg.VISION_MAX_OUTPUT_TOKENS
    user_parts = messages[1]["content"]
    assert user_parts[0]["text"] == "사용자의 질문: 이 오류 어떻게 해결해?"
    assert sum(p["type"] == "image_url" for p in user_parts) == 2
    assert "답하지 않는다" in messages[0]["content"]


def test_node_uses_last_message_when_no_original_question(fake_model):
    multimodal_node({"image": make_image(), "messages": [{"role": "user", "content": "마지막 질문"}]})
    assert "마지막 질문" in fake_model.calls[0][0][1]["content"][0]["text"]


def test_node_image_only_question(fake_model):
    multimodal_node({"image": make_image()})
    assert "이미지만 올림" in fake_model.calls[0][0][1]["content"][0]["text"]


def test_node_no_image_does_not_call_model(fake_model):
    assert multimodal_node({"original_question": "q"}) == {"image_analysis": cfg.NO_IMAGE_NOTICE}
    assert fake_model.calls == []


def test_node_all_images_invalid_does_not_call_model(fake_model):
    result = multimodal_node({"image": [b"junk", b""]})
    assert "건너뛰었습니다" in result["image_analysis"] and fake_model.calls == []


def test_node_model_failure_is_reported_not_raised(monkeypatch):
    model = FakeModel(error=RuntimeError("boom api_key=sk-" + "Z" * 30))
    monkeypatch.setattr(read_images_module, "create_openai_model", lambda **kwargs: model)
    result = multimodal_node({"image": make_image()})["image_analysis"]
    assert "이미지 분석에 실패했습니다" in result and "RuntimeError" in result
    assert "Z" * 30 not in result  # 오류 문구에 섞인 키도 가린다


def test_node_missing_key_is_reported_not_raised(monkeypatch):
    def no_key(**kwargs):
        raise ValueError("OPENAI_API_KEY 설정이 필요합니다.")

    monkeypatch.setattr(read_images_module, "create_openai_model", no_key)
    assert "설정이 필요합니다" in multimodal_node({"image": make_image()})["image_analysis"]


def test_node_notes_about_skipped_and_resized(fake_model):
    big = make_image(size=(cfg.RESIZE_MAX_EDGE + 500, 400))
    result = multimodal_node({"image": [b"junk", big]})["image_analysis"]
    assert result.startswith("※ 이미지 1은(는) 읽을 수 없어")
    assert "이미지 2은(는) 크기가 커서" in result
    sent = fake_model.calls[0][0][1]["content"]
    assert "[이미지 2]" in [p.get("text") for p in sent] and "[이미지 1]" not in [p.get("text") for p in sent]
