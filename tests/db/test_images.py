"""이미지 첨부 저장 확인 (메모리 SQLite). 합성 이미지는 Pillow로 만든다 (Pillow는 프로젝트 의존성)."""

import io
import os
import secrets

import pytest

PIL = pytest.importorskip("PIL")
from PIL import Image  # noqa: E402
from sqlalchemy import inspect  # noqa: E402

from src.db import (  # noqa: E402
    add_image,
    add_message,
    create_conversation,
    create_user,
    delete_conversation,
    delete_image,
    get_image,
    init_db,
    list_images,
    list_messages,
    make_engine,
    make_session_factory,
    session_scope,
    set_image_analysis,
    shrink_image,
)
from src.db.images import inspect_image, make_thumbnail, sha256_hex, sniff_mime  # noqa: E402
from src.db.models import MessageAttachment  # noqa: E402

NV = "nvapi" + "-" + "A1b2C3d4" * 4


def img_bytes(fmt="PNG", size=(120, 80), color=(30, 120, 200), mode="RGB") -> bytes:
    buf = io.BytesIO()
    Image.new(mode, size, color).save(buf, fmt)
    return buf.getvalue()


def noise_png(size=(900, 700)) -> bytes:
    """압축이 거의 안 되는 무작위 이미지 (용량 줄이기 시험용)."""
    buf = io.BytesIO()
    Image.frombytes("RGB", size, os.urandom(size[0] * size[1] * 3)).save(buf, "PNG")
    return buf.getvalue()


@pytest.fixture()
def session():
    engine = make_engine("sqlite://")
    init_db(engine)
    with session_scope(make_session_factory(engine)) as s:
        yield s


@pytest.fixture()
def turn(session):
    """사용자 한 명, 대화 하나, 사용자 메시지 하나."""
    user = create_user(session, "img_user", "pw-" + secrets.token_urlsafe(12))
    conv = create_conversation(session, user.id)
    msg = add_message(session, conv.id, user.id, "user", "오류 화면입니다", input_type="image")
    return user, conv, msg


# ---------------------------------------------------------------- 형식 판별
@pytest.mark.parametrize("fmt, mime", [("PNG", "image/png"), ("JPEG", "image/jpeg"), ("WEBP", "image/webp")])
def test_sniff_mime_from_real_bytes(fmt, mime):
    assert sniff_mime(img_bytes(fmt)) == mime


@pytest.mark.parametrize("data", [b"", b"plain text pretending to be .png", b"GIF89a....", b"%PDF-1.7 ...", b"<svg></svg>"])
def test_sniff_rejects_other_formats(data):
    assert sniff_mime(data) is None


def test_inspect_reports_size_and_rejects_broken_files():
    assert inspect_image(img_bytes(size=(120, 80))) == (120, 80)
    broken = img_bytes()[:40]  # 앞부분은 PNG인데 뒤가 잘린 파일
    with pytest.raises(ValueError):
        inspect_image(broken)


# ---------------------------------------------------------------- 저장 / 조회
def test_add_image_stores_metadata_thumbnail_and_hash(session, turn):
    user, conv, msg = turn
    data = img_bytes("PNG", (1200, 800))
    att = add_image(session, msg.id, user.id, data, analysis_text=f"NVIDIA_API_KEY={NV} 오류")
    assert att.mime_type == "image/png" and att.size_bytes == len(data)
    assert (att.width, att.height) == (1200, 800)
    assert att.sha256 == sha256_hex(data) and att.position == 0
    assert att.thumb_data and sniff_mime(att.thumb_data) == "image/jpeg"
    assert len(att.thumb_data) < len(data) or len(att.thumb_data) < 30_000
    thumb = Image.open(io.BytesIO(att.thumb_data))
    assert max(thumb.size) <= 256
    assert NV not in att.analysis_text and "[MASKED" in att.analysis_text  # 분석 텍스트는 마스킹


def test_max_three_images_per_message_and_positions(session, turn):
    user, conv, msg = turn
    atts = [add_image(session, msg.id, user.id, img_bytes(size=(50 + i, 50))) for i in range(3)]
    assert [a.position for a in atts] == [0, 1, 2]
    with pytest.raises(ValueError, match="3장"):
        add_image(session, msg.id, user.id, img_bytes())
    # 한 장을 지우면 다시 붙일 수 있고, 순번은 이어서 증가한다
    assert delete_image(session, atts[0].id, user.id) is True
    again = add_image(session, msg.id, user.id, img_bytes())
    assert again.position == 3
    assert [a.position for a in list_images(session, msg.id, user.id)] == [1, 2, 3]


def test_per_message_limit_is_configurable(session, turn, monkeypatch):
    user, conv, msg = turn
    monkeypatch.setenv("IMAGE_MAX_PER_MESSAGE", "1")
    add_image(session, msg.id, user.id, img_bytes())
    with pytest.raises(ValueError, match="1장"):
        add_image(session, msg.id, user.id, img_bytes())


def test_size_limit_is_enforced(session, turn, monkeypatch):
    user, conv, msg = turn
    data = img_bytes(size=(300, 300))
    monkeypatch.setenv("IMAGE_MAX_BYTES", str(len(data) - 1))
    with pytest.raises(ValueError, match="바이트 이하"):
        add_image(session, msg.id, user.id, data)
    monkeypatch.setenv("IMAGE_MAX_BYTES", str(len(data)))
    assert add_image(session, msg.id, user.id, data).size_bytes == len(data)  # 딱 맞으면 허용


@pytest.mark.parametrize("data", [b"", b"not an image at all", b"GIF89a" + b"0" * 50, b"\x89PNG\r\n\x1a\n" + b"junk"])
def test_invalid_or_unsupported_data_is_rejected(session, turn, data):
    user, conv, msg = turn
    with pytest.raises(ValueError):
        add_image(session, msg.id, user.id, data)


@pytest.mark.parametrize("fmt", ["GIF", "BMP", "TIFF"])
def test_valid_but_unsupported_formats_are_rejected(session, turn, fmt):
    """파일 자체는 멀쩡한 이미지여도 허용하지 않는 형식(gif, bmp, tiff)은 형식 검사가 막아야 한다.
    (깨진 파일은 Pillow 검사가 막아 주므로, 이 사례가 형식 검사를 따로 확인해 준다.)"""
    user, conv, msg = turn
    with pytest.raises(ValueError, match="png, jpeg, webp"):
        add_image(session, msg.id, user.id, img_bytes(fmt))


def test_images_only_on_user_messages(session, turn):
    user, conv, msg = turn
    answer = add_message(session, conv.id, user.id, "assistant", "답변")
    with pytest.raises(ValueError, match="사용자"):
        add_image(session, answer.id, user.id, img_bytes())


def test_ownership_isolation(session, turn):
    user, conv, msg = turn
    other = create_user(session, "other_user", "pw-" + secrets.token_urlsafe(12))
    att = add_image(session, msg.id, user.id, img_bytes())
    with pytest.raises(PermissionError):
        add_image(session, msg.id, other.id, img_bytes())
    with pytest.raises(PermissionError):
        list_images(session, msg.id, other.id)
    with pytest.raises(PermissionError):
        set_image_analysis(session, att.id, other.id, "남의 이미지")
    assert get_image(session, att.id, other.id) is None
    assert delete_image(session, att.id, other.id) is False
    assert get_image(session, att.id, user.id) is not None  # 본인은 그대로 볼 수 있다


def test_get_image_returns_original_bytes_but_list_does_not_load_them(session, turn):
    user, conv, msg = turn
    data = img_bytes("JPEG", (400, 300))
    att = add_image(session, msg.id, user.id, data)
    session.flush()
    session.expire_all()  # 방금 넣은 객체의 캐시를 비워 DB에서 새로 읽게 한다

    listed = list_images(session, msg.id, user.id)[0]
    assert "data" in inspect(listed).unloaded          # 목록에서는 원본을 읽지 않았다
    assert listed.thumb_data                           # 미리보기는 바로 쓸 수 있다
    full = get_image(session, att.id, user.id)
    assert full.data == data                           # 필요할 때 원본을 그대로 돌려준다


def test_very_long_analysis_text_is_clipped_not_rejected(session, turn):
    """분석 텍스트가 너무 길면 한 행이 DB 한도(TiDB 6MiB)를 넘을 수 있어서 잘라서 저장한다."""
    from src.db.images import MAX_ANALYSIS_CHARS

    user, conv, msg = turn
    att = add_image(session, msg.id, user.id, img_bytes(), analysis_text="가" * (MAX_ANALYSIS_CHARS + 5_000))
    assert len(att.analysis_text) < MAX_ANALYSIS_CHARS + 50 and att.analysis_text.endswith("(이하 생략)")
    set_image_analysis(session, att.id, user.id, "나" * (MAX_ANALYSIS_CHARS * 2))
    assert len(get_image(session, att.id, user.id).analysis_text) < MAX_ANALYSIS_CHARS + 50
    short = add_image(session, msg.id, user.id, img_bytes(), analysis_text="짧은 텍스트")
    assert short.analysis_text == "짧은 텍스트"  # 짧은 건 그대로


def test_set_image_analysis_later(session, turn):
    user, conv, msg = turn
    att = add_image(session, msg.id, user.id, img_bytes())
    assert att.analysis_text is None
    set_image_analysis(session, att.id, user.id, "ModuleNotFoundError: No module named 'langgraph.prebuilt'")
    assert "ModuleNotFoundError" in get_image(session, att.id, user.id).analysis_text


# ---------------------------------------------------------------- 대화 내역 표시 / 삭제
def test_list_messages_in_order_with_attachments(session, turn):
    user, conv, msg = turn
    add_image(session, msg.id, user.id, img_bytes())
    add_message(session, conv.id, user.id, "assistant", "원인은 ...")
    add_message(session, conv.id, user.id, "user", "그럼 어떻게 고쳐요?")
    msgs = list_messages(session, conv.id, user.id)
    assert [m.role for m in msgs] == ["user", "assistant", "user"]
    assert [len(m.attachments) for m in msgs] == [1, 0, 0]
    assert [m.role for m in list_messages(session, conv.id, user.id, limit=2)] == ["assistant", "user"]
    other = create_user(session, "someone_else", "pw-" + secrets.token_urlsafe(12))
    with pytest.raises(PermissionError):
        list_messages(session, conv.id, other.id)


def test_deleting_conversation_removes_images(session, turn):
    user, conv, msg = turn
    add_image(session, msg.id, user.id, img_bytes())
    add_image(session, msg.id, user.id, img_bytes())
    assert session.query(MessageAttachment).count() == 2
    delete_conversation(session, conv.id, user.id)
    session.flush()
    assert session.query(MessageAttachment).count() == 0


# ---------------------------------------------------------------- 썸네일 / 용량 줄이기
def test_thumbnail_handles_transparency_and_returns_none_for_garbage():
    rgba = img_bytes("PNG", (300, 300), (255, 0, 0, 0), mode="RGBA")  # 완전 투명
    assert sniff_mime(make_thumbnail(rgba)) == "image/jpeg"
    assert make_thumbnail(b"garbage") is None


def test_shrink_image_reduces_large_images_under_the_limit():
    big = noise_png((1400, 1000))
    limit = 400_000
    assert len(big) > limit
    out, mime = shrink_image(big, max_bytes=limit)
    assert len(out) <= limit and mime in ("image/png", "image/jpeg")
    assert sniff_mime(out) == mime
    w, h = inspect_image(out)
    assert max(w, h) <= 1600


def test_shrink_image_keeps_small_screenshots_as_png():
    small = img_bytes("PNG", (800, 600))
    out, mime = shrink_image(small, max_bytes=2_000_000)
    assert mime == "image/png" and len(out) <= 2_000_000


def test_shrink_image_rejects_broken_input():
    with pytest.raises(ValueError):
        shrink_image(b"not an image", max_bytes=100_000)
