from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from src.graph.chat_service import run_chat


def test_input_history_and_initial_state():
    history = [{"role": "user", "content": "첫 질문"},
               {"role": "assistant", "content": "첫 답변"},
               {"role": "user", "content": "후속 질문"}]
    graph = Mock()
    graph.invoke.return_value = {"messages": [AIMessage(content="후속 답변")]}
    result = run_chat(history, graph=graph)
    state = graph.invoke.call_args.args[0]
    assert state["messages"] == history and len(state["messages"]) == 3
    assert state["original_question"] == "후속 질문"
    assert state["retrieved_docs"] == [] and state["image_analysis"] == ""
    assert result["answer"] == "후속 답변" and result["sources"] == []


@pytest.mark.parametrize("messages", [[], None, [{}], [{"role": "user", "content": " "}],
    [{"role": "assistant", "content": "답변"}], [{"role": "user", "content": []}]])
def test_invalid_input_never_calls_graph(messages):
    graph = Mock()
    assert run_chat(messages, graph=graph)["error"]["code"] == "INVALID_INPUT"
    graph.invoke.assert_not_called()


@pytest.mark.parametrize("route", ["mcp", "multimodal"])
def test_unsupported_route(route):
    graph = Mock()
    graph.invoke.return_value = {"route": route, "messages": [HumanMessage(content="質問")]}
    result = run_chat([{"role": "user", "content": "質問"}], graph=graph)
    assert result["status"] == "unsupported" and result["answer"] == ""


@pytest.mark.parametrize("reply", [HumanMessage(content="入力"), AIMessage(content=" ")])
def test_input_or_empty_message_is_not_an_answer(reply):
    graph = Mock()
    graph.invoke.return_value = {"messages": [reply]}
    assert run_chat([{"role": "user", "content": "入力"}], graph=graph)["status"] == "error"


def test_error_details_are_not_returned():
    graph = Mock()
    graph.invoke.side_effect = RuntimeError("secret-api-key")
    result = run_chat([{"role": "user", "content": "入力"}], graph=graph)
    assert result["status"] == "error" and "secret-api-key" not in str(result)


def test_real_graph_routes_and_does_not_accumulate_history(monkeypatch):
    from src.graph.node import supervisor_node as supervisor
    from src.graph.node.general import general_node as general
    from src.graph.node.answer import answer_node as answer
    from src.graph.workflow import workflow

    route = ["general"]
    router = Mock()
    router.with_structured_output.return_value.invoke.side_effect = lambda _: SimpleNamespace(route=route[0], reason="test")
    responder = Mock()
    responder.invoke.return_value = AIMessage(content="테스트 답변")
    monkeypatch.setattr(supervisor, "create_openai_model", lambda **_: router)
    monkeypatch.setattr(general, "create_openai_model", lambda **_: responder)
    monkeypatch.setattr(answer, "create_openai_model", lambda **_: responder)
    graph = workflow()
    history = [{"role": "user", "content": "첫 질문"}]
    assert run_chat(history, graph=graph)["status"] == "success"
    history += [{"role": "assistant", "content": "테스트 답변"}, {"role": "user", "content": "후속 질문"}]
    assert run_chat(history, graph=graph)["status"] == "success"
    assert len(responder.invoke.call_args.args[0]) == 4  # system plus exactly three history items
    assert run_chat([{"role": "user", "content": "새 대화"}], graph=graph)["status"] == "success"
    assert len(responder.invoke.call_args.args[0]) == 2
    for value in ("mcp", "multimodal"):
        route[0] = value
        assert run_chat(history, graph=graph)["status"] == "unsupported"
    route[0] = "answer"
    assert run_chat(history, graph=graph)["status"] == "success"
    # Direct graph callers may omit optional State keys.
    assert graph.invoke({"messages": history, "original_question": "후속 질문"})["messages"][-1].content == "테스트 답변"
