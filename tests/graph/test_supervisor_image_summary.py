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
