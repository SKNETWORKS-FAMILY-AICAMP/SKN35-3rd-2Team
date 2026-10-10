from src.const.models import create_openai_model
from src.prompt.multi_query_prompt import MULTI_QUERY_PROMPT

model = create_openai_model()


def multi_query(question):
    response = model.invoke(
        [
            {"role": "system", "content": MULTI_QUERY_PROMPT},
            {"role": "user", "content": question},
        ]
    )

    queries = [
        query.strip() for query in response.content.splitlines() if query.strip()
    ]

    return queries[:3]
