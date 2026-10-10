"""Exercise existing DB functions via an isolated in-memory SQLite database."""
from contextlib import contextmanager
from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_core.messages import AIMessage

from src.app import chat_service
from src.db import create_user, list_messages, HistoryConfig, get_history_context
from src.db.models import Base


@pytest.fixture
def local_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)
    @contextmanager
    def session_scope():
        with factory() as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
    import src.db
    monkeypatch.setattr(src.db, "db_session", session_scope)
    with session_scope() as session:
        uid = create_user(session, "tester01", "test-pass-123").id
        other = create_user(session, "tester02", "test-pass-456").id
    yield session_scope, uid, other
    engine.dispose()


def test_bounded_db_history_new_graph_same_conversation(local_db, monkeypatch):
    sessions, uid, _ = local_db
    import src.db
    monkeypatch.setattr(src.db, "get_history_context", lambda session, cid, user:
        get_history_context(session, cid, user, config=HistoryConfig(max_turns=2, max_tokens=100)))
    graphs = []
    def fresh_graph():
        graph = Mock()
        graph.invoke.return_value = {"messages": [AIMessage(content="DB 테스트 답변")]}
        graphs.append(graph)
        return graph
    monkeypatch.setattr(chat_service, "get_graph", fresh_graph)
    cid = None
    for question in ("첫 오류", "두 번째 오류", "세 번째 오류"):
        result = chat_service.run_db_chat(question, user_id=uid, conversation_id=cid)
        assert result["status"] == "success"
        cid = result["conversation_id"]
        state = graphs[-1].invoke.call_args.args[0]
        assert state["messages"][-1]["content"] == question
        assert sum(m["content"] == question for m in state["messages"]) == 1
        assert len(state["messages"]) <= 4
        assert graphs[-1].invoke.call_args.kwargs["config"]["configurable"]["thread_id"] == str(cid)
    assert len(graphs) == 3 and len({id(g) for g in graphs}) == 3
    with sessions() as session:
        rows = list_messages(session, cid, uid)
        assert [m.role for m in rows] == ["user", "assistant"] * 3
    new = chat_service.run_db_chat("새 채팅", user_id=uid)
    assert new["conversation_id"] != cid
    assert len(graphs[-1].invoke.call_args.args[0]["messages"]) == 1


def test_other_user_cannot_write_or_call_graph(local_db, monkeypatch):
    _, uid, other = local_db
    graph = Mock()
    graph.invoke.return_value = {"messages": [AIMessage(content="reply")]}
    factory = Mock(return_value=graph)
    monkeypatch.setattr(chat_service, "get_graph", factory)
    result = chat_service.run_db_chat("첫 질문", user_id=uid)
    factory.reset_mock()
    rejected = chat_service.run_db_chat("다른 사람 질문", user_id=other, conversation_id=result["conversation_id"])
    assert rejected["error"]["code"] == "CONVERSATION_ACCESS_DENIED"
    factory.assert_not_called()


def test_failed_graph_keeps_question_without_saving_error_answer(local_db, monkeypatch):
    sessions, uid, _ = local_db
    graph = Mock()
    graph.invoke.side_effect = RuntimeError("private-db-or-api-detail")
    monkeypatch.setattr(chat_service, "get_graph", lambda: graph)
    result = chat_service.run_db_chat("실패 질문", user_id=uid)
    assert result["status"] == "error" and result["conversation_id"]
    assert "private-db-or-api-detail" not in str(result)
    with sessions() as session:
        rows = list_messages(session, result["conversation_id"], uid)
        assert len(rows) == 1 and rows[0].role == "user"


@pytest.mark.parametrize("uid,cid", [(None, None), (True, None), (0, None), (1, -1), (1, "123")])
def test_invalid_identity_rejected_before_db(uid, cid):
    assert chat_service.run_db_chat("질문", user_id=uid, conversation_id=cid)["error"]["code"] == "INVALID_INPUT"
