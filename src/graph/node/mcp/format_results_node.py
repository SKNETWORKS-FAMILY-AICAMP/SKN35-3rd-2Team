"""
5단계: 결과를 State.mcp_results 형태로 정리한다. (모든 경로가 마지막에 여기로 온다)

State.mcp_outcome / mcp_failures / mcp_error  -->  [이 노드]  -->  State.mcp_results (기존 항목 뒤에 한 건 추가)

항목 모양 (answer 노드가 읽는다)
    {
      "status": "success" | "failed" | "no_tool",
      "tool": 도구 이름, "server": 서버 이름, "arguments": 인자,
      "content": 도구가 돌려준 글 (성공한 경우),
      "error": 실패 이유 (실패한 경우), "attempts": 도구를 고른 횟수,
      "called_at": 정리한 시각(UTC, ISO 형식),
      "note": 사용 방법 안내
    }

- "failed"인 결과로는 최신 정보를 단정하면 안 된다 (평가표 E09). note에 그 안내가 들어간다.
- 도구가 돌려준 글은 길이를 줄이고 비밀값을 가린다.
"""

from datetime import datetime, timezone

from src.const import mcp_config as cfg
from src.db.masking import mask_secrets


def _clean(text: str) -> str:
    if len(text) > cfg.MAX_RESULT_CHARS:
        text = text[: cfg.MAX_RESULT_CHARS] + cfg.CLIP_SUFFIX
    return mask_secrets(text)


def failed_record(error: str, *, tool: str | None = None, arguments: dict | None = None, attempts: int = 0) -> dict:
    """"실패" 결과 한 건. 이 노드와, 예상 못 한 오류를 잡아서 실패로 바꾸는 mcp_node(src/agent/mcp_agent.py)가 같이 쓴다."""
    return {
        "status": cfg.STATUS_FAILED,
        "tool": tool,
        "server": None,
        "arguments": arguments,
        "content": "",
        "error": _clean(error),
        "attempts": attempts,
        "called_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": cfg.FAILED_NOTE,
    }


def format_results_node(state):
    results = list(state.get("mcp_results") or [])
    failures = state.get("mcp_failures") or []
    outcome = state.get("mcp_outcome")
    error = state.get("mcp_error")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    attempts = state.get("mcp_attempts", 0)

    if outcome:
        record = {
            "status": cfg.STATUS_SUCCESS,
            "tool": outcome["tool"],
            "server": outcome["server"],
            "arguments": outcome["arguments"],
            "content": _clean(outcome["text"]),
            "error": None,
            "attempts": attempts,
            "called_at": now,
            "note": cfg.RETRIED_NOTE.format(count=len(failures)) if failures else "",
        }
    elif failures or (error and error["kind"] != "no_tool"):
        last = failures[-1] if failures else None
        record = failed_record(
            last["message"] if last else error["message"],
            tool=last["tool"] if last else None,
            arguments=last["arguments"] if last else None,
            attempts=attempts,
        )
    else:
        record = {
            "status": cfg.STATUS_NO_TOOL,
            "tool": None,
            "server": None,
            "arguments": None,
            "content": "",
            "error": None,
            "attempts": attempts,
            "called_at": now,
            "note": cfg.NO_TOOL_NOTE,
        }

    return {"mcp_results": [*results, record]}
