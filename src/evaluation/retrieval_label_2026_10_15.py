"""
1차(검색) 평가의 정답표를 만든다.

    python -m src.evaluation.retrieval_label_2026_10_15

- 입력: retrieval_questions_2026-10-15.jsonl (질문과 원본 청크 ID. 모두 벡터 DB(인덱스)의 청크 ID다)
- 정답 = 질문을 만든 원본 청크(항상 정답) + 검색 후보(상위 5개) 중 gpt-4o-mini가 "근거가 맞다"고 판정한 청크.
  관련 있음/없음 2단계로 판정한다. 같은 주제를 다룰 뿐 질문의 답에 직접 필요하지 않으면 "없음"이다.
- 판정 이유(reason)와 청크 글(앞부분)도 저장한다. 사람이 10%를 골라 이 이유를 보고 검수한다.
- 인덱스에서 원본 청크를 찾지 못한 질문은 원본 없이 모델이 판정한 청크만 정답이 된다 (source_found_in_index=false).
- 정답이 없는 질문(type=no_answer)은 정답표를 만들지 않는다 (검색 지표의 분모에서 빠진다).
- 이미 판정한 질문은 건너뛴다 (중간에 끊겨도 이어서 할 수 있다). 처음부터 다시 하려면 결과 파일을 지운다.
  사람이 고친 판정(by="human")은 결과 파일에만 있으므로 지우기 전에 백업한다.
- 결과: retrieval_gold_2026-10-15.jsonl (이 폴더). 모델 이름은 환경변수 EVAL_MODEL (없으면 gpt-4o-mini).
"""

import json
import os
from pathlib import Path

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.const.config import OPEN_API_KEY
from src.evaluation.index_chunks_2026_10_15 import fetch_chunks, get_index
from src.evaluation.retrieval_run_2026_10_15 import ranked_candidates

HERE = Path(__file__).resolve().parent
QUESTIONS_PATH = HERE / "retrieval_questions_2026-10-15.jsonl"
GOLD_PATH = HERE / "retrieval_gold_2026-10-15.jsonl"
CLIP_CHARS = 2000
SHOW_CHARS = 900  # 사람이 검수할 때 볼 수 있게 정답표에 남기는 글의 길이


class Judgement(BaseModel):
    relevant: bool = Field(description="이 글이 질문에 답하는 데 직접 필요한 내용을 담고 있으면 true")
    reason: str = Field(description="판단 이유 한 문장")


PROMPT = """개발 질문과 공식 문서의 한 부분이 있다. 이 글이 질문에 답하는 데 **직접 필요한 내용**을 담고 있는지 판정한다.

기준:
- true: 이 글을 읽으면 질문의 답(또는 답의 중요한 부분)을 알 수 있다.
- false: 같은 주제나 같은 라이브러리를 다룰 뿐, 질문의 답에는 필요하지 않다. 배경지식 수준이면 false다.
- 질문에 쓰인 단어가 글에 있다는 이유만으로 true로 하지 않는다.

[질문]
{question}

[글]
{text}"""


def make_judge():
    model = os.getenv("EVAL_MODEL") or "gpt-4o-mini"
    return ChatOpenAI(api_key=OPEN_API_KEY, model=model, temperature=0.0, timeout=120).with_structured_output(Judgement), model


def read_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def label_one(judge, index, record):
    candidates = ranked_candidates(record["question"])
    sources = fetch_chunks(index, record["source_chunk_ids"])
    source_ids = [cid for cid in record["source_chunk_ids"] if cid in sources]
    labels = [
        {"rank": None, "chunk_id": cid, "relevant": True, "reason": "질문을 만든 원본 청크", "by": "source", "text": sources[cid]["text"][:SHOW_CHARS]}
        for cid in source_ids
    ]
    for rank, candidate in enumerate(candidates, start=1):
        chunk_id = candidate["chunk_id"]
        if chunk_id in source_ids:
            for label in labels:
                if label["chunk_id"] == chunk_id:
                    label["rank"] = rank
            continue
        verdict = judge.invoke(PROMPT.format(question=record["question"], text=candidate["text"][:CLIP_CHARS]))
        labels.append({"rank": rank, "chunk_id": chunk_id, "relevant": verdict.relevant, "reason": verdict.reason, "by": "model", "text": candidate["text"][:SHOW_CHARS]})
    gold = list(dict.fromkeys(source_ids + [item["chunk_id"] for item in labels if item["relevant"]]))
    return {
        "id": record["id"],
        "gold_chunk_ids": gold,
        "source_chunk_ids": source_ids,
        "source_found_in_index": bool(source_ids),
        "candidate_chunk_ids": [candidate["chunk_id"] for candidate in candidates],
        "labels": sorted(labels, key=lambda item: (item["rank"] is None, item["rank"] or 0)),
    }


def main():
    questions = [r for r in read_jsonl(QUESTIONS_PATH) if r["type"] == "answerable"]
    if not questions:
        raise SystemExit(f"{QUESTIONS_PATH.name}이(가) 없습니다. 먼저 retrieval_make_dataset_2026_10_15를 실행하세요.")
    done = {r["id"] for r in read_jsonl(GOLD_PATH)}
    judge, model_name = make_judge()
    index = get_index()
    with GOLD_PATH.open("a", encoding="utf-8") as out:
        for record in questions:
            if record["id"] in done:
                continue
            try:
                gold = label_one(judge, index, record)
            except Exception as exc:  # 한 질문이 실패해도 나머지는 계속한다. 실패한 질문은 다음 실행 때 다시 시도한다.
                print(record["id"], "실패:", type(exc).__name__, str(exc)[:200], flush=True)
                continue
            gold["judged_by"] = model_name
            out.write(json.dumps(gold, ensure_ascii=False) + "\n")
            out.flush()
            print(record["id"], "정답", len(gold["gold_chunk_ids"]), "개 (원본", len(gold["source_chunk_ids"]), "+ 추가", len(gold["gold_chunk_ids"]) - len(gold["source_chunk_ids"]), ")", flush=True)
    print("저장:", GOLD_PATH)


if __name__ == "__main__":
    main()
