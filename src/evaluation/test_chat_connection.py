"""UI contract checks, with no external API calls or team implementation changes."""
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import Mock
import sys

import pytest
from langchain_core.messages import AIMessage, HumanMessage
from streamlit.testing.v1 import AppTest

from src.app.chat_service import chat_result, run_chat

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("messages", [[], None, [{}], [{"role": "user", "content": " "}],
    [{"role": "assistant", "content": "답변"}], [{"role": "user", "content": []}]])
def test_invalid_input(messages):
    graph = Mock()
    assert run_chat(messages, graph=graph)["error"]["code"] == "INVALID_INPUT"
    graph.invoke.assert_not_called()


@pytest.mark.parametrize("reply", [HumanMessage(content="질문"), AIMessage(content=" ")])
def test_invalid_reply(reply):
    graph = Mock()
    graph.invoke.return_value = {"messages": [reply]}
    assert run_chat([{"role": "user", "content": "질문"}], graph=graph)["status"] == "error"


def test_safe_error():
    graph = Mock()
    graph.invoke.side_effect = RuntimeError("secret-api-key")
    result = run_chat([{"role": "user", "content": "질문"}], graph=graph)
    assert result["status"] == "error" and "secret-api-key" not in str(result)


def test_graph_history_and_connected_routes(monkeypatch):
    # Replace the existing model factory only in memory, before importing dev nodes.
    from src.const import models
    class FakeModel:
        route = "general"
        seen = []
        def with_structured_output(self, schema):
            return SimpleNamespace(invoke=lambda _: SimpleNamespace(route=self.route, reason="test"))
        def invoke(self, messages):
            self.seen.append(messages)
            return AIMessage(content="테스트 답변")
    fake = FakeModel()
    monkeypatch.setattr(models, "create_openai_model", lambda **_: fake)
    module_names = ["src.graph.workflow", "src.agent.general_agent", "src.agent.answer_agent",
        "src.graph.node.supervisor_node", "src.graph.node.general.general_node",
        "src.graph.node.answer.answer_node"]
    for name in module_names:
        monkeypatch.delitem(sys.modules, name, raising=False)
    # Keep this connection test offline: workflow now imports the RAG agent.
    rag_module = ModuleType("src.agent.rag_agent")
    rag_module.rag_node = lambda state: {"retrieved_docs": [], "completed_routes": ["rag"]}
    monkeypatch.setitem(sys.modules, "src.agent.rag_agent", rag_module)
    from importlib import import_module
    workflow_module = import_module("src.graph.workflow")
    # Newly connected tool/image routes must stay offline in this contract test.
    monkeypatch.setattr(workflow_module, "mcp_node", lambda state: {
        "mcp_results": [], "completed_routes": ["mcp"]})
    monkeypatch.setattr(workflow_module, "multi_modal_node", lambda state: {
        "image_analysis": "test OCR", "completed_routes": ["multi_modal"]})
    monkeypatch.setattr(workflow_module, "supervisor_node", lambda state: {
        "route": "answer" if fake.route in (state.get("completed_routes") or []) else fake.route,
        "reason": "test"})
    graph = workflow_module.workflow()
    history = [{"role": "user", "content": "첫 질문"}]
    assert run_chat(history, graph=graph)["answer"] == "테스트 답변"
    history += [{"role": "assistant", "content": "테스트 답변"},
                {"role": "user", "content": "후속 질문"}]
    assert run_chat(history, graph=graph)["status"] == "success"
    assert len(fake.seen[-1]) == 4  # system + complete history once
    assert run_chat([{"role": "user", "content": "새 대화"}], graph=graph)["status"] == "success"
    assert len(fake.seen[-1]) == 2
    fake.route = "answer"
    assert run_chat(history, graph=graph)["status"] == "success"
    for route in ("mcp", "multi_modal"):
        fake.route = route
        assert run_chat(history, graph=graph)["status"] == "success"


def test_ui_history_reset_modes_and_errors(monkeypatch):
    from src.app import chat
    calls = []
    def respond(messages, **kwargs):
        calls.append(messages)
        question = messages[-1]["content"]
        if question == "미지원":
            return chat_result(status="unsupported", code="UNSUPPORTED_ROUTE", message="준비 중")
        if question == "실패":
            return chat_result(status="error", code="GRAPH_ERROR", message="실패 안내")
        return chat_result("테스트 답변")
    # AppTest has no browser JavaScript; storage restoration is tested separately.
    monkeypatch.setattr(chat, "restore_login", lambda: None)
    monkeypatch.setattr(chat, "run_chat", respond)
    app = AppTest.from_file(str(ROOT / "main.py"), default_timeout=15).run()
    assert not app.exception
    app.chat_input[0].set_value("첫 질문").run()
    app.chat_input[0].set_value("후속 질문").run()
    assert not app.exception and len(calls[-1]) == 3
    assert len(app.session_state["messages"]) == 4
    app.button[0].click().run()
    assert app.session_state["messages"] == []
    app.chat_input[0].set_value("미지원").run()
    assert app.info and app.session_state["messages"] == []
    app.chat_input[0].set_value("실패").run()
    assert app.error and app.session_state["messages"] == []
    app.button[0].click().run()
    app.session_state["answer_mode"] = "연습 모드"
    app.run()
    app.chat_input[0].set_value("연습").run()
    assert len(app.session_state["messages"]) == 2
    app.button[0].click().run()
    app.session_state["answer_mode"] = "OpenAI AI 답변"
    app.run()
    assert not app.exception and app.session_state["messages"] == []
