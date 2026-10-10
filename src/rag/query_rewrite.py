from src.const.models import create_openai_model
from src.prompt.query_rewrite_prompt import QUERY_REWRITE_PROMPT

model = create_openai_model()


def query_rewrite(original_question):
    response = model.invoke(
        [
            {"role": "system", "content": QUERY_REWRITE_PROMPT},
            {"role": "user", "content": original_question},
        ]
    )

    return response.content
