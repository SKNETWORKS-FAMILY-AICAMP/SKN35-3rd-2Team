"""
MCP 에이전트: 질문에 맞는 MCP 도구를 골라 부르고, 결과를 State.mcp_results에 담는다.

이 파일 하나에 전체 흐름이 보이도록 했다 (rag_agent.py와 같은 방식). 각 단계의 일은 src/graph/node/mcp/ 의 노드가 한다.

    START
      │
      ▼
    list_tools ──(도구 없음)──────────────────────────────────────┐
      │                                                           │
      ▼                                                           │
    select_tool ◀──────────────┐   모델이 도구와 인자를 고른다     │
      │                        │   (도구를 안 골랐으면 바로 정리로)  │
      ▼                        │                                   │
    validate_call ──(오류)──▶ route_on_error ─(다시 고를 수 있음)──┘ ← select_tool로 되돌아감
      │                        ▲                                   │
      ▼                        │                                   │
    call_tool ───(오류)────────┘                                   │
      │                                                           │
      ▼                                                           ▼
    format_results ◀──────────(다시 고를 수 없음 / 횟수 초과 / 도구 안 고름)
      │
      ▼
     END

다시 고르는 조건 (route_on_error)
- 오류가 "고칠 수 있는 종류"이고 (없는 도구, 잘못된 인자, 이미 실패한 호출 반복, 도구 자체의 실패),
- 지금까지 고른 횟수가 MAX_ATTEMPTS(src/const/mcp_config.py)보다 적을 때만 select_tool로 되돌아간다.
- 서버를 못 띄움, 시간 초과, 모델 호출 실패는 도구를 바꿔도 소용없으므로 바로 정리로 간다.
- 결과가 비어 있는 경우는 다시 고르지 않는다.
"""

from langgraph.graph import END, START, StateGraph

from src.const import mcp_config as cfg
from src.graph.node.mcp.call_tool_node import call_tool_node
from src.graph.node.mcp.format_results_node import format_results_node
from src.graph.node.mcp.list_tools_node import list_tools_node
from src.graph.node.mcp.mcp_state import MCPState
from src.graph.node.mcp.select_tool_node import select_tool_node
from src.graph.node.mcp.validate_call_node import validate_call_node


def route_after_list_tools(state: MCPState):
    return "format_results" if state.get("mcp_error") else "select_tool"


def route_after_select_tool(state: MCPState):
    # 모델 호출이 실패했거나 도구를 고르지 않았으면 더 갈 곳이 없다
    if state.get("mcp_error") or state.get("mcp_call") is None:
        return "format_results"
    return "validate_call"


def route_on_error(state: MCPState):
    error = state["mcp_error"]
    if error["retryable"] and state.get("mcp_attempts", 0) < cfg.MAX_ATTEMPTS:
        return "select_tool"
    return "format_results"


def route_after_validate_call(state: MCPState):
    return route_on_error(state) if state.get("mcp_error") else "call_tool"


def route_after_call_tool(state: MCPState):
    return route_on_error(state) if state.get("mcp_error") else "format_results"


def mcp_agent():
    builder = StateGraph(MCPState)

    builder.add_node("list_tools", list_tools_node)
    builder.add_node("select_tool", select_tool_node)
    builder.add_node("validate_call", validate_call_node)
    builder.add_node("call_tool", call_tool_node)
    builder.add_node("format_results", format_results_node)

    builder.add_edge(START, "list_tools")
    builder.add_conditional_edges(
        "list_tools", route_after_list_tools, {"select_tool": "select_tool", "format_results": "format_results"}
    )
    builder.add_conditional_edges(
        "select_tool", route_after_select_tool, {"validate_call": "validate_call", "format_results": "format_results"}
    )
    builder.add_conditional_edges(
        "validate_call",
        route_after_validate_call,
        {"call_tool": "call_tool", "select_tool": "select_tool", "format_results": "format_results"},
    )
    builder.add_conditional_edges(
        "call_tool", route_after_call_tool, {"select_tool": "select_tool", "format_results": "format_results"}
    )
    builder.add_edge("format_results", END)

    return builder.compile()
