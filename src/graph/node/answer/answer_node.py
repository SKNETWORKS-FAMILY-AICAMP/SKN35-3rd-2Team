from src.const.models import create_openai_model
from src.prompt.answer_prompt import ANSWER_SYSTEM_PROMPT

model = create_openai_model()


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
                        "original_question": state.get("original_question", ""),
                        "messages": state.get("messages", []),
                        "image_analysis": state.get("image_analysis"),
                        "retrieved_docs": state.get("retrieved_docs", []),
                        "mcp_results": state.get("mcp_results"),
                    }
                ),
            },
        ]
    )

    return {
        "messages": [response],
        "answer": response.content,
    }
