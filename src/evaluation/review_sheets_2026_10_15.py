"""
사람 검수용 표본 파일을 만든다 (체크리스트 10%, 정답표 10%).

    python -m src.evaluation.review_sheets_2026_10_15

- answer_review_rubric_2026-10-15.md : 체크리스트(있어야 할 항목, 있으면 안 되는 것)가 질문과 근거 문서에 맞는지 확인
- retrieval_review_gold_2026-10-15.md: 정답표(어떤 청크를 정답으로 봤는지)와 모델의 판정 이유가 맞는지 확인
- 시드를 고정해서 항상 같은 표본이 뽑힌다. 정답 없는 질문은 사람이 쓴 규칙이라 표본에서 뺀다.
- 틀린 것은 체크 표시를 하고 고칠 내용을 적는다. 이 파일은 결과를 바꾸지 않는다 (읽기만 한다).
"""

import json
import random
from pathlib import Path

from src.evaluation.index_chunks_2026_10_15 import fetch_chunks, get_index

HERE = Path(__file__).resolve().parent
SEED = 20261015
RATE = 0.10
TEXT_CLIP = 700


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def clip(text):
    text = " ".join((text or "").split())
    return text if len(text) <= TEXT_CLIP else text[:TEXT_CLIP] + " …"


def pick(records):
    return random.Random(SEED).sample(records, max(1, round(len(records) * RATE)))


def rubric_sheet(chunks):
    rubrics = [r for r in read_jsonl(HERE / "answer_rubric_2026-10-15.jsonl") if r["type"] == "answerable"]
    questions = {r["id"]: r for r in read_jsonl(HERE / "retrieval_questions_2026-10-15.jsonl")}
    lines = ["# 체크리스트 검수 표본 (정답 있는 질문의 10%)", "", "확인할 것: 항목이 질문의 요구와 근거 문서에 맞는가? 문서에 없는 내용을 요구하지 않는가? 너무 좁거나 넓지 않은가?", ""]
    for record in pick(rubrics):
        source_ids = questions[record["id"]]["source_chunk_ids"]
        lines += [f"## {record['id']}", "", f"**질문**: {record['question']}", ""]
        for chunk_id in source_ids:
            lines += [f"**근거 문서** ({chunk_id}): {clip(chunks.get(chunk_id, {}).get('text'))}", ""]
        lines += ["**꼭 들어가야 할 항목**"] + [f"- [ ] {item}" for item in record["must_include"]]
        lines += ["", "**있으면 안 되는 것**"] + ([f"- [ ] {item}" for item in record["must_not"]] or ["- (없음)"])
        lines += ["", "수정할 내용: ", ""]
    return "\n".join(lines)


def gold_sheet(chunks):
    golds = [g for g in read_jsonl(HERE / "retrieval_gold_2026-10-15.jsonl") if g.get("labels") and "text" in g["labels"][0]]
    questions = {r["id"]: r for r in read_jsonl(HERE / "retrieval_questions_2026-10-15.jsonl")}
    lines = ["# 정답표 검수 표본 (정답 있는 질문의 10%, 인덱스 기준 정답표)", "", "확인할 것: 모델이 \"정답\"으로 인정한 청크가 정말 질문의 답에 직접 필요한가? \"아님\"으로 한 청크 중 사실은 필요한 것이 없는가? 내용은 Pinecone 인덱스에 저장된 실제 글이다.", ""]
    for gold in pick(golds):
        question = questions[gold["id"]]
        lines += [f"## {gold['id']}", "", f"**질문**: {question['question']}", "", f"정답으로 확정된 청크: {', '.join(gold['gold_chunk_ids'])}", ""]
        for label in gold["labels"]:
            who = "원본에 해당하는 인덱스 청크" if label["by"] == "source" else "모델 판정"
            verdict = "정답" if label["relevant"] else "정답 아님"
            rank = f"검색 {label['rank']}위" if label["rank"] else "검색 상위 5개 밖"
            lines += [f"### {rank}: {label['chunk_id']} → {verdict} [{who}]", "", f"- 이유: {label['reason']}", f"- 내용: {clip(label.get('text'))}", "- [ ] 판정이 틀렸다 (고칠 값: )", ""]
    return "\n".join(lines)


def main():
    ids = [cid for q in read_jsonl(HERE / "retrieval_questions_2026-10-15.jsonl") for cid in q["source_chunk_ids"]]
    chunks = fetch_chunks(get_index(), ids)
    (HERE / "answer_review_rubric_2026-10-15.md").write_text(rubric_sheet(chunks), encoding="utf-8")
    (HERE / "retrieval_review_gold_2026-10-15.md").write_text(gold_sheet(chunks), encoding="utf-8")
    print("저장 완료")


if __name__ == "__main__":
    main()
