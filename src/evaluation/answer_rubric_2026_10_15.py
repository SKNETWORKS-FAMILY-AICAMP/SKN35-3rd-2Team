"""
2차(답변) 평가용 체크리스트(루브릭)를 질문마다 만든다.

    python -m src.evaluation.answer_rubric_2026_10_15

- 정답 문장이 아니라 "답에 꼭 들어가야 할 항목(must_include)"과 "있으면 안 되는 것(must_not)"을 만든다.
  표현이 달라도 의미가 같으면 충족으로 보려는 것이다 (채점할 때 문장이 같은지는 보지 않는다).
- 정답 있는 질문: 질문을 만든 원본 청크(들)의 내용을 근거로 만든다. 글에 없는 내용은 항목으로 만들지 않는다.
- 정답 없는 질문(모르는 내부 라이브러리, 정보 부족, 범위 밖): 사람이 코드에 적은 규칙으로 만든다 (아래 NO_ANSWER_RUBRIC).
- 결과: answer_rubric_2026-10-15.jsonl. 이미 있으면 덮어쓰지 않는다 (--force로만). 사람이 10%를 골라 검수한다.
- 모델 이름은 환경변수 EVAL_MODEL (없으면 gpt-4o-mini).
"""

import argparse
import json
import os
from pathlib import Path

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.const.config import OPEN_API_KEY

HERE = Path(__file__).resolve().parent
CHUNKS_PATH = HERE.parents[1] / "data" / "processed" / "chunks.jsonl"
QUESTIONS_PATH = HERE / "retrieval_questions_2026-10-15.jsonl"
OUTPUT_PATH = HERE / "answer_rubric_2026-10-15.jsonl"

# 정답이 없는 질문의 규칙은 유형별로 사람이 정한다.
NO_ANSWER_RUBRIC = {
    "internal": {
        "must_include": ["질문에 나온 내부 라이브러리, 오류 코드, 함수에 대한 자료를 확인할 수 없다고 밝힌다", "로그, 문서, 코드 같은 추가 자료를 요청한다"],
        "must_not": ["그 라이브러리나 오류 코드가 실제로 있는 것처럼 원인이나 의미를 단정한다", "근거 없는 해결 명령어나 설정을 만들어 낸다"],
    },
    "vague": {
        "must_include": ["오류 메시지 전문, 실행 명령, 사용 중인 언어나 라이브러리와 버전 같은 필요한 정보를 구체적으로 되묻는다"],
        "must_not": ["정보 없이 원인을 임의로 정한다", "앱 재설치나 기기 재부팅 같은 일반적인 추측 해결책을 늘어놓는다"],
    },
    "out_of_scope": {
        "must_include": ["LangChain, LangGraph, MCP 관련 도우미라서 이 질문은 범위 밖이라는 점을 밝히거나, 확인할 수 있는 자료가 없다고 말한다"],
        "must_not": ["출처나 근거 없이 그 분야의 상세한 사실을 단정적으로 설명한다"],
    },
}


class Rubric(BaseModel):
    must_include: list[str] = Field(description="답에 꼭 들어가야 할 핵심 항목 3~5개. 각각 한 문장")
    must_not: list[str] = Field(description="있으면 안 되는 것 0~3개 (글에 없는 API를 지어내거나 조건을 어기는 등)")


PROMPT = """개발 질문과 그 답의 근거가 되는 공식 문서 내용이 있다. 이 문서 내용에 근거해, 좋은 답이 갖춰야 할 체크리스트를 만든다.

규칙:
- must_include: 답에 꼭 들어가야 할 핵심 항목 3~5개. 질문이 요구하는 조건을 하나씩 나눠서 쓴다. 각 항목은 "~를 설명한다", "~를 안내한다"처럼 한 문장이고, 특정 문장을 그대로 쓰라는 뜻이 아니라 의미로 판단할 수 있어야 한다.
- must_not: 있으면 안 되는 것 0~3개. 문서와 어긋나는 내용이나 질문의 조건을 어기는 답이다.
- 문서 내용에 없는 것은 항목으로 만들지 않는다.

[질문]
{question}

[근거 문서 내용]
{context}"""


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if OUTPUT_PATH.exists() and not args.force:
        raise SystemExit(f"{OUTPUT_PATH.name}이(가) 이미 있습니다. 덮어쓰려면 --force를 붙이세요.")

    chunks = {row["chunk_id"]: row for row in read_jsonl(CHUNKS_PATH)}
    name = os.getenv("EVAL_MODEL") or "gpt-4o-mini"
    llm = ChatOpenAI(api_key=OPEN_API_KEY, model=name, temperature=0.0, timeout=120).with_structured_output(Rubric)

    records = []
    for question in read_jsonl(QUESTIONS_PATH):
        if question["type"] == "answerable":
            context = "\n\n".join(f"[{chunks[cid]['title']}]\n{chunks[cid]['text']}" for cid in question["source_chunk_ids"])
            rubric = llm.invoke(PROMPT.format(question=question["question"], context=context))
            record = {"must_include": rubric.must_include, "must_not": rubric.must_not, "made_by": name}
        else:
            record = {**NO_ANSWER_RUBRIC[question["kind"]], "made_by": "human"}
        records.append({"id": question["id"], "type": question["type"], "question": question["question"], **record})
        print(question["id"], len(record["must_include"]), len(record["must_not"]), flush=True)
    OUTPUT_PATH.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
    print("저장:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
