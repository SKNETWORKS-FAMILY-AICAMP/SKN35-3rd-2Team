"""
MCP 작업(src/agent/mcp_agent.py)이 쓰는 상태.

rag 에이전트의 RAGState와 같은 방식이다. RAGState는 src/graph/state.py(다른 팀원 파일)에 있어서,
이 상태는 MCP 폴더에 두었다. 나중에 state.py로 옮기고 싶으면 그 파일 담당자와 정하면 된다.

부모 State와 이름이 같은 항목(messages, original_question, mcp_results)은 MCP 작업이 끝나면 부모로 돌아간다.
나머지 항목은 이 작업 안에서만 쓰는 값이다.
"""

from typing import NotRequired

from langgraph.graph import MessagesState


class MCPState(MessagesState):
    original_question: str
    mcp_results: NotRequired[list]  # 결과. 부모 State.mcp_results로 돌아간다 (기존 항목 뒤에 이어 붙인다)

    mcp_tools: NotRequired[list[dict]]  # 쓸 수 있는 도구: {"server", "name", "display_name", "description", "input_schema"}
    mcp_call: NotRequired[dict | None]  # 지금 부르려는 도구: {"display_name", "arguments"} (+ 검사 뒤 "server", "name")
    mcp_attempts: NotRequired[int]  # 도구를 고른 횟수
    mcp_failures: NotRequired[list[dict]]  # 실패 기록: {"tool", "arguments", "kind", "message"} (다시 고를 때 모델에게 보여 준다)
    mcp_error: NotRequired[dict | None]  # 마지막 오류: {"kind", "message", "retryable"}. 없으면 None
    mcp_outcome: NotRequired[dict | None]  # 성공한 호출: {"tool", "server", "arguments", "text"}
