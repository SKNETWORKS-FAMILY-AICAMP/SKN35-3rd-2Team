from src.const.models import create_nvidia_model
from src.prompt.answer_prompt import ANSWER_SYSTEM_PROMPT

model = create_nvidia_model()


def answer_node(state):
    response = model.invoke(
        [
            {
                "role": "system",
                "content": ANSWER_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": str(
                    {
                        "original_question": state["original_question"],
                        "messages": state["messages"],
                        "image_analysis": state["image_analysis"],
                        "retrieved_docs": state["retrieved_docs"],
                        "mcp_results": state["mcp_results"],
                    }
                ),
            },
        ]
    )

    return {
        "messages": [response],
    }
