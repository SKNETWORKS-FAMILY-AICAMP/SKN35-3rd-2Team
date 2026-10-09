from typing import Literal

from pydantic import BaseModel, Field

from src.const.models import create_openai_model
from src.prompt.supervisor_prompt import SUPERVISOR_SYSTEM_PROMPT



class RouteDecision(BaseModel):
    route: Literal[
        "general",
        "rag",
        "mcp",
        "multimodal",
        "answer",
    ] = Field(description="현재 상태를 바탕으로 다음에 수행할 작업을 선택합니다.")

    reason: str = Field(description="선택한 작업이 필요한 이유를 간단하게 설명합니다.")


def supervisor_node(state):
    model = create_openai_model(timeout=60)
    print("supervisor 진입", end="\n\n")
    supervisor = model.with_structured_output(RouteDecision)

    decision = supervisor.invoke(
        [
            {
                "role": "system",
                "content": SUPERVISOR_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": str(
                    {
                        "messages": [{"role": m.type, "content": m.content} for m in state["messages"]],
                        "image": state.get("image"),
                        "image_analysis": state.get("image_analysis"),
                        "retrieved_docs": state.get("retrieved_docs"),
                        "mcp_results": state.get("mcp_results"),
                    }
                ),
            },
        ]
    )

    return {
        "route": decision.route,
        "reason": decision.reason,
    }
