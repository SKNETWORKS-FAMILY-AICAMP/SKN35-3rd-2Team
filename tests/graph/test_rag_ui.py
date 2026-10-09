from pathlib import Path

from streamlit.testing.v1 import AppTest

from src.app import chat
from src.graph.chat_service import chat_result


def test_sources_remain_visible_after_rerun_and_are_not_sent_as_messages(monkeypatch):
    source = {"url": "https://docs.langchain.com/oss/python/langgraph/graph-api", "title": "Graph API"}
    calls = []
    def respond(messages):
        calls.append(messages)
        return chat_result("State 설명 [1]", sources=[source])
    monkeypatch.setattr(chat, "run_chat", respond)
    app = AppTest.from_file(str(Path(__file__).resolve().parents[2] / "main.py"), default_timeout=15).run()
    app.chat_input[0].set_value("State 설명").run()
    assert not app.exception and len(app.get("link_button")) == 1
    assert app.session_state["messages"][-1]["sources"] == [source]
    app.run()
    assert len(app.get("link_button")) == 1
    app.button[0].click().run()
    assert app.session_state["messages"] == [] and len(app.get("link_button")) == 0
