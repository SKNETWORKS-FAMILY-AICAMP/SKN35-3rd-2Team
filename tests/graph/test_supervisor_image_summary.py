import os

os.environ.setdefault("OPENAI_API_KEY", "test-key-not-real")

from src.graph.node.supervisor_node import image_summary  # noqa: E402


def test_summary_has_only_presence_and_count_not_bytes():
    blob = b"\x89PNG" + b"x" * 5000
    summary = image_summary({"image": [blob, blob]})
    assert summary == {"has_image": True, "image_count": 2}
    assert "PNG" not in str(summary)


def test_summary_without_image():
    assert image_summary({}) == {"has_image": False, "image_count": 0}
    assert image_summary({"image": None}) == {"has_image": False, "image_count": 0}
    assert image_summary({"image": b"one"}) == {"has_image": True, "image_count": 1}


def test_long_question_is_clipped_for_the_supervisor_only():
    from src.graph.node.supervisor_node import QUESTION_MAX_CHARS, _clip

    long = "가" * (QUESTION_MAX_CHARS + 500)
    clipped = _clip(long)
    assert len(clipped) < len(long) and clipped.endswith("(이하 생략)")
    assert _clip("짧은 질문") == "짧은 질문"
