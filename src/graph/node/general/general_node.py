from src.const.models import create_openai_model
from src.graph.state import State
from src.prompt.general_prompt import GENERAL_SYSTEM_PROMPT



def general_node(state: State):
    model = create_openai_model(timeout=60)
    response = model.invoke(
        [
            {
                "role": "system",
                "content": GENERAL_SYSTEM_PROMPT,
            },
            *state["messages"],
        ]
    )

    return {"messages": [response]}
