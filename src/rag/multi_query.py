import json

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

    try:
        result = json.loads(response.content)
        queries = [
            item["query"].strip()
            for item in result["queries"]
            if isinstance(item.get("query"), str) and item["query"].strip()
        ]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise ValueError(
            f"멀티 쿼리 응답의 JSON 형식이 올바르지 않습니다: {response.content}"
        ) from e

    queries = list(dict.fromkeys(queries))[:3]

    print("queries:", queries)

    return queries
