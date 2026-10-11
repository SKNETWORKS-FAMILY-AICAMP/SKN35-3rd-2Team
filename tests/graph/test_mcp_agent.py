"""
MCP 에이전트(src/agent/mcp_agent.py)와 노드 시험. 모델과 서버는 가짜로 바꿔 끼운다 (진짜 서버 시험은 tests/mcp_integration).
실행: uv run pytest tests/graph/test_mcp_agent.py -q
"""

import pytest

from src.agent.mcp_agent import mcp_agent, route_on_error
from src.const import mcp_config as cfg
from src.graph.node.mcp import call_tool_node as call_module
from src.graph.node.mcp import list_tools_node as list_module
from src.graph.node.mcp import select_tool_node as select_module
from src.graph.node.mcp.list_tools_node import assign_display_names

REPEAT_SCHEMA = {
    "type": "object",
    "properties": {"text": {"type": "string"}, "times": {"type": "integer"}},
    "required": ["text", "times"],
}
TOOLS = [
    {"server": "dev_helper", "name": "repeat_text", "description": "글을 반복한다", "input_schema": REPEAT_SCHEMA},
    {"server": "dev_helper", "name": "get_utc_time", "description": "시각", "input_schema": {"type": "object", "properties": {}}},
]
OK = {"text": "hi hi hi", "is_error": False}
TOO_MANY = {"text": "Error executing tool repeat_text: times는 1에서 5 사이여야 합니다 (받은 값: 10).", "is_error": True}


def pick(name="repeat_text", **args):
    return {"name": name, "args": args}


class FakeModel:
    """script: 호출마다 하나씩 꺼내 쓴다. dict면 도구 호출, None이면 도구를 고르지 않음, 예외면 던진다."""

    def __init__(self, script):
        self.script = list(script)
        self.seen: list[list[dict]] = []

    def bind_tools(self, tools, **kwargs):
        self.tools = tools
        return self

    def invoke(self, messages):
        self.seen.append(messages)
        step = self.script.pop(0)
        if isinstance(step, Exception):
            raise step

        class Reply:
            tool_calls = [step] if step else []

        return Reply()


class FakeServer:
    """call_tool 대역: script를 하나씩 꺼내 쓴다. 예외면 던진다."""

    def __init__(self, script):
        self.script = list(script)
        self.calls = []

    def __call__(self, server, name, arguments, *a, **kw):
        self.calls.append((server.name, name, arguments))
        step = self.script.pop(0)
        if isinstance(step, Exception):
            raise step
        return step


@pytest.fixture
def env(monkeypatch):
    list_module._CACHE.clear()
    state = {"list_calls": 0}

    def fake_list(server, *a, **kw):
        state["list_calls"] += 1
        return [dict(t) for t in TOOLS]

    monkeypatch.setattr(list_module, "list_tools", fake_list)

    def setup(model_script, server_script=()):
        model, server = FakeModel(model_script), FakeServer(server_script)
        monkeypatch.setattr(select_module, "create_openai_model", lambda **kw: model)
        monkeypatch.setattr(call_module, "call_tool", server)
        return model, server

    setup.state = state
    return setup


def run(question="hi를 3번 반복해줘", **extra):
    return mcp_agent().invoke({"messages": [], "original_question": question, **extra})


def last(result):
    return result["mcp_results"][-1]


# ---------------------------------------------------------------- 흐름
def test_success_on_first_try(env):
    model, server = env([pick(text="hi", times=3)], [OK])
    record = last(run())
    assert record["status"] == cfg.STATUS_SUCCESS and record["content"] == "hi hi hi"
    assert record["tool"] == "repeat_text" and record["server"] == "dev_helper"
    assert record["arguments"] == {"text": "hi", "times": 3} and record["attempts"] == 1
    assert record["called_at"].endswith("+00:00") and record["error"] is None
    assert len(model.seen) == 1 and len(server.calls) == 1


def test_model_is_given_tool_definitions_from_schema(env):
    model, _ = env([pick(text="hi", times=3)], [OK])
    run()
    fn = model.tools[0]["function"]
    assert fn["name"] == "repeat_text" and fn["parameters"] == REPEAT_SCHEMA
    assert "사용자의 질문: hi를 3번 반복해줘" in model.seen[0][1]["content"]


def test_tool_error_then_retry_with_failure_reason(env):
    model, server = env([pick(text="hi", times=10), pick(text="hi", times=5)], [TOO_MANY, OK])
    record = last(run("hi를 10번 반복해줘"))
    assert record["status"] == cfg.STATUS_SUCCESS and record["attempts"] == 2
    assert len(server.calls) == 2
    assert "바꿔 다시 호출한 결과" in record["note"] and record["arguments"]["times"] == 5  # 요청(10)과 다르게 불렀음을 알린다
    retry_prompt = model.seen[1][1]["content"]
    assert "앞선 시도가 실패했다" in retry_prompt and "times는 1에서 5 사이" in retry_prompt  # 실패 이유를 모델에게 보여 준다
    assert "앞선 시도가 실패했다" not in model.seen[0][1]["content"]


def test_gives_up_after_max_attempts(env):
    model, server = env([pick(text="hi", times=10 + i) for i in range(cfg.MAX_ATTEMPTS)], [TOO_MANY] * cfg.MAX_ATTEMPTS)
    record = last(run())
    assert record["status"] == cfg.STATUS_FAILED and record["note"] == cfg.FAILED_NOTE
    assert "times는 1에서 5 사이" in record["error"] and record["attempts"] == cfg.MAX_ATTEMPTS
    assert len(model.seen) == len(server.calls) == cfg.MAX_ATTEMPTS  # 더 시도하지 않는다


def test_invalid_arguments_are_caught_before_calling(env):
    model, server = env([pick(text="hi"), pick(text="hi", times="세 번"), pick(text="hi", times=3)], [OK])
    record = last(run())
    assert record["status"] == cfg.STATUS_SUCCESS and record["attempts"] == 3
    assert len(server.calls) == 1  # 잘못된 인자 두 번은 서버를 부르지 않고 걸러졌다
    assert "times" in model.seen[1][1]["content"]  # 빠진 인자 이름이 실패 이유에 있다


def test_unknown_tool_then_corrected(env):
    model, server = env([pick("repeat_txt", text="hi", times=3), pick(text="hi", times=3)], [OK])
    record = last(run())
    assert record["status"] == cfg.STATUS_SUCCESS and len(server.calls) == 1
    assert "repeat_text" in model.seen[1][1]["content"]  # 쓸 수 있는 도구 이름을 알려 준다


def test_same_failed_call_is_not_repeated(env):
    same = pick(text="hi", times=10)
    model, server = env([same, same, pick(text="hi", times=5)], [TOO_MANY, OK])
    record = last(run())
    assert record["status"] == cfg.STATUS_SUCCESS and record["attempts"] == 3
    assert len(server.calls) == 2  # 같은 호출을 두 번째로 부르지 않았다
    assert "이미 실패한 호출" in model.seen[2][1]["content"]


# ---------------------------------------------------------------- 다시 시도하지 않는 경우
def test_connection_failure_is_not_retried(env):
    model, server = env([pick(text="hi", times=3)], [RuntimeError("server crashed")])
    record = last(run())
    assert record["status"] == cfg.STATUS_FAILED and "server crashed" in record["error"]
    assert len(model.seen) == 1 and len(server.calls) == 1


def test_timeout_is_not_retried(env):
    model, server = env([pick(text="hi", times=3)], [TimeoutError()])
    record = last(run())
    assert record["status"] == cfg.STATUS_FAILED and "초 안에 끝나지 않았습니다" in record["error"]
    assert len(model.seen) == 1


def test_model_error_is_not_retried(env):
    model, server = env([RuntimeError("rate limited")])
    record = last(run())
    assert record["status"] == cfg.STATUS_FAILED and "rate limited" in record["error"]
    assert server.calls == []


def test_no_tool_chosen_from_the_start(env):
    model, server = env([None])
    record = last(run("오늘 날씨 알려줘"))
    assert record["status"] == cfg.STATUS_NO_TOOL and record["note"] == cfg.NO_TOOL_NOTE
    assert server.calls == []


def test_gives_up_when_model_chooses_no_tool_after_failure(env):
    model, server = env([pick(text="hi", times=10), None], [TOO_MANY])
    record = last(run())
    assert record["status"] == cfg.STATUS_FAILED  # 맞는 도구가 없다는 뜻이 아니라, 실패한 것이다
    assert "times는 1에서 5 사이" in record["error"] and len(server.calls) == 1


def test_no_tools_available_skips_the_model(env, monkeypatch):
    model, server = env([])

    def broken(server, *a, **kw):
        raise OSError("cannot start server")

    monkeypatch.setattr(list_module, "list_tools", broken)
    record = last(run())
    assert record["status"] == cfg.STATUS_FAILED and "cannot start server" in record["error"]
    assert model.seen == []


# ---------------------------------------------------------------- 결과 정리와 그 밖의 동작
def test_results_are_appended_not_replaced(env):
    env([pick(text="hi", times=3)], [OK])
    previous = {"status": "success", "tool": "earlier"}
    result = run(mcp_results=[previous])
    assert result["mcp_results"][0] == previous and len(result["mcp_results"]) == 2


def test_result_is_clipped_and_secrets_masked(env):
    key = "sk-" + "a1B2c3D4e5F6g7H8i9J0k1L2"
    long_text = f"OPENAI_API_KEY={key} " + "단어 " * cfg.MAX_RESULT_CHARS
    env([pick(text="hi", times=3)], [{"text": long_text, "is_error": False}])
    content = last(run())["content"]
    assert key not in content and "[MASKED" in content
    assert content.endswith(cfg.CLIP_SUFFIX) and len(content) < cfg.MAX_RESULT_CHARS + 200


def test_tool_list_is_cached_between_runs(env):
    env([pick(text="hi", times=3), pick(text="hi", times=3)], [OK, OK])
    run()
    run()
    assert env.state["list_calls"] == 1


def test_display_names_resolve_collisions():
    tools = [
        {"server": "a", "name": "search"},
        {"server": "b", "name": "search"},
        {"server": "a", "name": "other"},
        {"server": "a", "name": "한글 이름!"},
    ]
    names = [t["display_name"] for t in assign_display_names(tools)]
    assert names == ["a__search", "b__search", "other", "______"]  # 모델이 받을 수 없는 글자(한글, 공백, !)는 _로 바뀐다


def test_route_on_error_rules():
    retryable = {"kind": "tool_error", "message": "x", "retryable": True}
    fatal = {"kind": "timeout", "message": "x", "retryable": False}
    assert route_on_error({"mcp_error": retryable, "mcp_attempts": 1}) == "select_tool"
    assert route_on_error({"mcp_error": retryable, "mcp_attempts": cfg.MAX_ATTEMPTS}) == "format_results"
    assert route_on_error({"mcp_error": fatal, "mcp_attempts": 1}) == "format_results"
