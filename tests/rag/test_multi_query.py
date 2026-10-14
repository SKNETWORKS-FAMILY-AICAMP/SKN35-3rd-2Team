"""RAG 멀티 쿼리 응답 해석 시험. 모델이 약속한 모양과 조금 다르게 답해도 그래프가 죽지 않아야 한다 (모델은 가짜로 바꾼다)."""

import os
from types import SimpleNamespace

import pytest

os.environ.setdefault("OPENAI_API_KEY", "test-key-not-real")

import src.rag.multi_query as mq  # noqa: E402


def fake_model(content):
    return SimpleNamespace(invoke=lambda messages: SimpleNamespace(content=content))


@pytest.mark.parametrize("content", [
    '{"queries": [{"query": "a error", "target_lib": null}, {"query": "how to fix a", "target_lib": "langgraph"}]}',
    '[{"query": "a error", "target_lib": null}, {"query": "how to fix a", "target_lib": null}]',
    '["a error", "how to fix a"]',
    '```json\n[{"query": "a error"}, {"query": "how to fix a"}]\n```',
    '{"queries": ["a error", "how to fix a"]}',
])
def test_every_known_shape_gives_the_same_queries(content):
    assert mq.parse_queries(content) == ["a error", "how to fix a"]


@pytest.mark.parametrize("content", ["", "not json", "{}", '{"queries": "x"}', "[]", '[{"q": "x"}]', '[{"query": "  "}]', "null", "123"])
def test_unreadable_answers_give_none(content):
    assert mq.parse_queries(content) is None


def test_bare_list_answer_no_longer_crashes(monkeypatch):
    """이전에는 queries로 감싸지 않은 목록이 오면 ValueError로 그래프 전체가 죽었다."""
    monkeypatch.setattr(mq, "model", fake_model('[{"query": "TypeError unsupported type list", "target_lib": null}]'))
    assert mq.multi_query("원래 질문") == ["TypeError unsupported type list"]


def test_unreadable_answer_falls_back_to_the_original_question(monkeypatch):
    monkeypatch.setattr(mq, "model", fake_model("죄송하지만 JSON으로 답할 수 없습니다"))
    assert mq.multi_query("  원래 질문  ") == ["원래 질문"]


def test_duplicates_are_removed_and_at_most_three_are_kept(monkeypatch):
    monkeypatch.setattr(mq, "model", fake_model('["a", "a", "b", "c", "d"]'))
    assert mq.multi_query("q") == ["a", "b", "c"]
