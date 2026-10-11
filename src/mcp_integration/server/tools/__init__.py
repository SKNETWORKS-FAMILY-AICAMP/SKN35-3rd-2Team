"""
서버에 등록할 도구 모음. 도구 파일마다 register(mcp) 함수가 있고, 여기서 한꺼번에 등록한다.
"""

from src.mcp_integration.server.tools import example_tool

# 새 도구 파일을 만들면 여기에 추가한다. (example_tool은 구조 시험용이라 실제 도구가 정해지면 지워도 된다)
TOOL_MODULES = (example_tool,)


def register_all(mcp) -> None:
    for module in TOOL_MODULES:
        module.register(mcp)
