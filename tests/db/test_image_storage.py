"""이미지를 DB가 아니라 서버 파일로 저장하는 부분 시험 (메모리 SQLite + 임시 저장 폴더, 루트 conftest.py가 폴더를 정해 준다)."""

import io
import secrets
from pathlib import Path

import pytest

PIL = pytest.importorskip("PIL")
from PIL import Image  # noqa: E402
from sqlalchemy import text  # noqa: E402

from src.db import (  # noqa: E402
    add_image,
    add_message,
    create_conversation,
    create_user,
    delete_conversation,
    delete_image,
    get_image,
    image_bytes,
    init_db,
    list_images,
    make_engine,
    make_session_factory,
    session_scope,
    thumbnail_bytes,
)
from src.db import storage  # noqa: E402
from src.db.models import MessageAttachment  # noqa: E402


def png(size=(200, 120), color=(30, 120, 200)) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", size, color).save(buffer, "PNG")
    return buffer.getvalue()


@pytest.fixture()
def session():
    engine = make_engine("sqlite://")
    init_db(engine)
    with session_scope(make_session_factory(engine)) as s:
        yield s


@pytest.fixture()
def turn(session):
    user = create_user(session, "file_user", "pw-" + secrets.token_urlsafe(12))
    conv = create_conversation(session, user.id)
    msg = add_message(session, conv.id, user.id, "user", "오류 화면입니다", input_type="image")
    return user, conv, msg


def test_image_is_written_as_files_and_db_keeps_only_paths(session, turn):
    user, _, msg = turn
    data = png()
    att = add_image(session, msg.id, user.id, data)
    assert att.data is None and att.thumb_data is None
    assert att.file_path.startswith(f"{msg.id}/0_") and att.file_path.endswith(".png")
    assert att.thumb_path.endswith("_thumb.jpg")
    assert (storage.storage_root() / att.file_path).read_bytes() == data
    assert (storage.storage_root() / att.thumb_path).is_file()
    assert image_bytes(att) == data
    assert thumbnail_bytes(att)[:3] == b"\xff\xd8\xff"  # JPEG


def test_file_names_do_not_use_anything_the_user_typed(session, turn):
    user, _, msg = turn
    att = add_image(session, msg.id, user.id, png())
    assert Path(att.file_path).parent.name == str(msg.id)
    assert ".." not in att.file_path and "\\" not in att.file_path


def test_second_image_gets_next_position(session, turn):
    user, _, msg = turn
    first = add_image(session, msg.id, user.id, png(color=(1, 2, 3)))
    second = add_image(session, msg.id, user.id, png(color=(9, 8, 7)))
    assert first.file_path != second.file_path
    assert second.file_path.startswith(f"{msg.id}/1_")


def test_delete_image_removes_its_files(session, turn):
    user, _, msg = turn
    att = add_image(session, msg.id, user.id, png())
    original, thumb = storage.storage_root() / att.file_path, storage.storage_root() / att.thumb_path
    assert original.exists() and thumb.exists()
    assert delete_image(session, att.id, user.id) is True
    assert not original.exists() and not thumb.exists()


def test_delete_conversation_removes_all_image_files(session, turn):
    user, conv, msg = turn
    a = add_image(session, msg.id, user.id, png(color=(1, 1, 1)))
    b = add_image(session, msg.id, user.id, png(color=(2, 2, 2)))
    paths = [storage.storage_root() / p for att in (a, b) for p in (att.file_path, att.thumb_path)]
    assert all(p.exists() for p in paths)
    assert delete_conversation(session, conv.id, user.id) is True
    assert not any(p.exists() for p in paths)


def test_other_users_delete_does_not_touch_the_files(session, turn):
    user, _, msg = turn
    other = create_user(session, "other_user", "pw-" + secrets.token_urlsafe(12))
    att = add_image(session, msg.id, user.id, png())
    path = storage.storage_root() / att.file_path
    assert delete_image(session, att.id, other.id) is False
    assert path.exists()


def test_failed_db_write_removes_the_files_it_just_wrote(session, turn, monkeypatch):
    user, _, msg = turn

    def broken_flush(*args, **kwargs):
        raise RuntimeError("db down")

    monkeypatch.setattr(session, "flush", broken_flush)
    with pytest.raises(RuntimeError):
        add_image(session, msg.id, user.id, png())
    root = storage.storage_root()
    assert not list(root.rglob("*.png")) and not list(root.rglob("*_thumb.jpg"))


def test_reading_refuses_paths_outside_the_storage_folder():
    for bad in ("../outside.png", "../../etc/passwd", "/etc/passwd", "a/../../b.png"):
        with pytest.raises(ValueError):
            storage.read_file(bad)


def test_missing_thumbnail_file_gives_none_not_an_error(session, turn):
    user, _, msg = turn
    att = add_image(session, msg.id, user.id, png())
    (storage.storage_root() / att.thumb_path).unlink()
    assert thumbnail_bytes(att) is None  # 화면이 멈추지 않는다
    (storage.storage_root() / att.file_path).unlink()
    with pytest.raises(FileNotFoundError):
        image_bytes(att)


def test_rows_saved_the_old_way_in_the_db_can_still_be_read(session, turn):
    user, _, msg = turn
    data, thumb = png(), png(size=(20, 12))
    legacy = MessageAttachment(
        message_id=msg.id, position=0, mime_type="image/png", size_bytes=len(data),
        sha256="0" * 64, data=data, thumb_data=thumb,
    )
    session.add(legacy)
    session.flush()
    assert image_bytes(legacy) == data and thumbnail_bytes(legacy) == thumb
    assert get_image(session, legacy.id, user.id) is legacy
    assert list_images(session, msg.id, user.id) == [legacy]


def test_storage_folder_can_be_changed_by_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("IMAGE_STORAGE_DIR", str(tmp_path / "elsewhere"))
    assert storage.storage_root() == (tmp_path / "elsewhere").resolve()
    storage.write_file("1/0_abc.png", b"x")
    assert (tmp_path / "elsewhere" / "1" / "0_abc.png").read_bytes() == b"x"


def test_move_images_to_files_tool_moves_old_rows_and_is_safe_to_repeat(session, turn, monkeypatch):
    user, _, msg = turn
    data, thumb = png(), png(size=(20, 12))
    legacy = MessageAttachment(
        message_id=msg.id, position=0, mime_type="image/png", size_bytes=len(data),
        sha256="ab" * 32, data=data, thumb_data=thumb,
    )
    session.add(legacy)
    session.flush()

    import src.db.move_images_to_files as tool
    from contextlib import contextmanager

    @contextmanager
    def same_session():
        yield session
        session.flush()  # 진짜 db_session은 끝날 때 저장(commit)한다

    monkeypatch.setattr(tool, "db_session", same_session)
    tool.main()
    session.expire_all()
    moved = session.get(MessageAttachment, legacy.id)
    assert moved.data is None and moved.thumb_data is None
    assert image_bytes(moved) == data and thumbnail_bytes(moved) == thumb
    tool.main()  # 한 번 더 실행해도 그대로
    assert image_bytes(session.get(MessageAttachment, legacy.id)) == data
    assert session.execute(text("select count(*) from message_attachments")).scalar() == 1
