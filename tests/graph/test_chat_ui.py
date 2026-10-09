from pathlib import Path

from streamlit.testing.v1 import AppTest

from src.app import chat
from src.graph.chat_service import chat_result

ROOT = Path(__file__).resolve().parents[2]


def test_graph_ui_history_reset_and_failure(monkeypatch):
    calls = []
    def respond(messages):
        calls.append(messages)
        if messages[-1]["content"] == "未対応":
            return chat_result(status="unsupported", code="UNSUPPORTED_ROUTE", message="準備中")
        if messages[-1]["content"] == "失敗":
            return chat_result(status="error", code="GRAPH_ERROR", message="失敗しました")
        return chat_result("테스트 답변")
    monkeypatch.setattr(chat, "run_chat", respond)
    app = AppTest.from_file(str(ROOT / "main.py"), default_timeout=15).run()
    assert not app.exception
    app.chat_input[0].set_value("첫 질문").run()
    app.chat_input[0].set_value("후속 질문").run()
    assert not app.exception and len(calls[-1]) == 3
    assert len(app.session_state["messages"]) == 4
    app.button[0].click().run()
    assert app.session_state["messages"] == []
    app.chat_input[0].set_value("未対応").run()
    assert app.session_state["messages"] == [] and app.info
    app.chat_input[0].set_value("失敗").run()
    assert app.session_state["messages"] == [] and app.error
    app.selectbox[0].select("연습 모드").run()
    app.chat_input[0].set_value("연습").run()
    assert len(app.session_state["messages"]) == 2
    app.selectbox[0].select("OpenAI AI 답변").run()
    assert not app.exception and app.session_state["messages"] == []
