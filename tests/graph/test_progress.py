"""화면에 알려 줄 큰 단계(src/graph/progress.py) 시험. 화면이나 서비스 연결부 없이 단계 규칙만 확인한다."""

import sys
import types

from src.graph import progress
from src.graph.progress import BY_ROUTE, LOADING, NEXT, START, StageReporter, stage_for


def test_supervisor_route_decides_the_next_stage():
    for route in ("multi_modal", "rag", "mcp", "general", "answer"):
        assert stage_for("supervisor", {"route": route}) == BY_ROUTE[route]
    assert stage_for("supervisor", {"route": "unknown"}) is None
    assert stage_for("supervisor", {}) is None and stage_for("supervisor", None) is None


def test_general_and_answer_share_the_answer_stage():
    assert BY_ROUTE["general"] == BY_ROUTE["answer"] and BY_ROUTE["answer"].startswith("ANSWER")


def test_specialized_nodes_hand_back_to_supervisor():
    for node in ("rag", "mcp", "multi_modal"):
        assert stage_for(node, {}) == NEXT
    assert stage_for("answer", {"answer": "x"}) is None
    assert stage_for("general", {}) is None and stage_for("reset_turn_state", {}) is None


def test_stage_names_start_with_the_step_names_the_team_uses():
    assert BY_ROUTE["multi_modal"].startswith("MULTI_MODAL") and BY_ROUTE["rag"].startswith("RAG")
    assert BY_ROUTE["mcp"].startswith("MCP") and START.startswith("SUPERVISOR") and NEXT.startswith("SUPERVISOR")


def feed(reporter, steps):
    for node, update in steps:
        reporter.node_finished(node, update)


def test_reporter_follows_an_image_question():
    stages = []
    reporter = StageReporter(stages.append)
    reporter.start()
    feed(reporter, [
        ("reset_turn_state", {}), ("supervisor", {"route": "multi_modal"}), ("multi_modal", {}),
        ("supervisor", {"route": "rag"}), ("rag", {}), ("supervisor", {"route": "answer"}), ("answer", {}),
    ])
    assert stages == [START, BY_ROUTE["multi_modal"], NEXT, BY_ROUTE["rag"], NEXT, BY_ROUTE["answer"]]


def test_reporter_does_not_repeat_the_same_stage():
    stages = []
    reporter = StageReporter(stages.append)
    reporter.start()
    reporter.start()
    feed(reporter, [("supervisor", {"route": "general"}), ("supervisor", {"route": "general"})])
    assert stages == [START, BY_ROUTE["general"]]


def test_reporter_without_a_callback_does_nothing():
    reporter = StageReporter(None)
    reporter.loading_if_first_run()
    reporter.start()
    feed(reporter, [("supervisor", {"route": "rag"})])  # 예외 없이 지나간다


def test_loading_stage_only_before_the_graph_is_first_loaded(monkeypatch):
    stages = []
    monkeypatch.delitem(sys.modules, "src.graph.workflow", raising=False)
    StageReporter(stages.append).loading_if_first_run()
    assert stages == [LOADING]

    stages.clear()
    monkeypatch.setitem(sys.modules, "src.graph.workflow", types.ModuleType("src.graph.workflow"))
    StageReporter(stages.append).loading_if_first_run()
    assert stages == []


def test_module_does_not_import_the_ui_or_service_layer():
    """이 파일은 화면과 서비스 연결부를 몰라야 한다 (다른 담당 파일에 의존하지 않는다)."""
    source = open(progress.__file__, encoding="utf-8").read()
    assert "import streamlit" not in source and "from src.app" not in source and "import src.app" not in source
