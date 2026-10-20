"""앱을 켤 때 미리 불러오기(웜업)와 "모델을 불러오는 중" 단계 알림을 확인한다. 큰 모델은 불러오지 않는다."""

import threading
from unittest.mock import Mock

import pytest
from langchain_core.messages import AIMessage

from src.app import chat_service as cs
from src.graph.progress import LOADING, START


@pytest.fixture(autouse=True)
def reset_warm_state(monkeypatch):
    monkeypatch.setattr(cs, "_warm_started", False)
    monkeypatch.delenv(cs.NO_WARM_UP_ENV, raising=False)


# ---------------------------------------------------------------- 웜업
def test_warm_up_runs_the_steps_once(monkeypatch):
    steps = Mock()
    monkeypatch.setattr(cs, "_warm_up_steps", steps)
    assert cs.warm_up(background=False) is True
    assert cs.warm_up(background=False) is False  # Streamlit이 main.py를 다시 실행해도 한 번만
    steps.assert_called_once()


def test_warm_up_in_background_does_not_block(monkeypatch):
    started, release = threading.Event(), threading.Event()

    def slow_steps():
        started.set()
        release.wait(5)

    monkeypatch.setattr(cs, "_warm_up_steps", slow_steps)
    assert cs.warm_up(background=True) is True  # 단계가 끝나기 전에 돌아온다
    assert started.wait(2)
    release.set()


def test_warm_up_failure_is_swallowed(monkeypatch, capsys):
    monkeypatch.setattr(cs, "_warm_up_steps", Mock(side_effect=RuntimeError("pinecone down")))
    assert cs.warm_up(background=False) is True  # 예외가 밖으로 나가지 않는다
    assert "웜업 실패" in capsys.readouterr().err


def test_warm_up_can_be_switched_off_by_environment(monkeypatch):
    steps = Mock()
    monkeypatch.setattr(cs, "_warm_up_steps", steps)
    monkeypatch.setenv(cs.NO_WARM_UP_ENV, "1")
    assert cs.warm_up(background=False) is False
    steps.assert_not_called()


def test_warm_up_steps_build_graph_and_retriever(monkeypatch):
    calls = []
    monkeypatch.setattr(cs, "get_graph", lambda: calls.append("graph"))
    import src.rag.retriever as retriever_module

    monkeypatch.setattr(retriever_module, "create_hybrid_retriever", lambda **kwargs: calls.append(("retriever", kwargs)))
    cs._warm_up_steps()
    assert calls[0] == "graph" and calls[1][0] == "retriever"
    assert calls[1][1] == {"filters": None, "use_query_rewrite": False, "use_multi_query": False, "use_rerank": False}  # 검색 노드와 같은 설정


# ---------------------------------------------------------------- "모델을 불러오는 중" 알림
class FakeEngine:
    def stream(self, state, config=None, stream_mode=None):
        yield "updates", {"answer": {"route": "end", "answer": "답", "messages": [AIMessage(content="답")]}}


def ask(monkeypatch):
    monkeypatch.setattr(cs, "get_graph", lambda: FakeEngine())
    stages = []
    result = cs.run_chat([{"role": "user", "content": "질문"}], on_stage=stages.append)
    assert result["status"] == "success"
    return stages


def test_loading_stage_is_announced_until_the_graph_is_ready(monkeypatch):
    monkeypatch.setattr(cs, "_GRAPH_READY", threading.Event())  # 아직 준비 안 됨 (웜업 중이거나 첫 질문)
    assert ask(monkeypatch)[:2] == [LOADING, START]


def test_loading_stage_is_not_announced_once_ready(monkeypatch):
    ready = threading.Event()
    ready.set()
    monkeypatch.setattr(cs, "_GRAPH_READY", ready)
    assert ask(monkeypatch)[0] == START


def test_get_graph_marks_ready(monkeypatch):
    import sys
    import types

    fake = types.ModuleType("src.graph.workflow")
    fake.workflow = lambda: "graph"
    monkeypatch.setitem(sys.modules, "src.graph.workflow", fake)
    ready = threading.Event()
    monkeypatch.setattr(cs, "_GRAPH_READY", ready)
    assert cs.get_graph() == "graph" and ready.is_set()
