"""
구조 시험용 도구 (실제 도구가 정해지면 이 파일은 지워도 된다).

도구 파일을 쓰는 방법의 본보기이기도 하다.
- 함수의 타입 표시와 docstring이 모델에게 보이는 도구 설명과 입력 규칙이 된다. 설명은 모델이 읽으므로 구체적으로 쓴다.
- 사용자가 고칠 수 있는 오류(잘못된 인자 등)는 ToolError로 던진다. 이 메시지는 클라이언트와 모델에게 전달되어 다시 시도할 때 쓰인다.
  그 밖의 예외는 서버 안의 오류로 보고 "Error executing tool ..."만 전달된다 (내부 내용이 새지 않게 하려는 것).
"""

from datetime import datetime, timezone

from mcp.server.mcpserver.exceptions import ToolError

MAX_REPEAT = 5


def register(mcp) -> None:
    @mcp.tool()
    async def get_utc_time() -> str:
        """서버의 현재 시각(UTC)을 ISO 형식으로 알려 준다."""
        return datetime.now(timezone.utc).isoformat(timespec="seconds")

    @mcp.tool()
    async def repeat_text(text: str, times: int) -> str:
        """글을 times번 반복해서 공백으로 이어 붙인다. times는 1에서 5 사이여야 한다.

        Args:
            text: 반복할 글
            times: 반복 횟수 (1~5)
        """
        if not 1 <= times <= MAX_REPEAT:
            raise ToolError(f"times는 1에서 {MAX_REPEAT} 사이여야 합니다 (받은 값: {times}).")
        return " ".join([text] * times)
