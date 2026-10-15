"""
2차(답변) 평가: 수집한 답변을 체크리스트로 채점한다.

    python -m src.evaluation.answer_eval_2026_10_15 --tag baseline

- 입력: answers_2026-10-15_<tag>.jsonl (답변), answer_rubric_2026-10-15.jsonl (체크리스트)
- 채점 모델은 gpt-4o-mini (환경변수 EVAL_MODEL). 앱 모델과 같아서 후하게 줄 수 있으므로 사람이 10%를 검수한다.

지표
  1) Faithfulness: 답변의 "출처가 필요한 사실 주장" 중 답변 모델에 실제로 전달된 근거(검색 문서, 도구 결과)로
     뒷받침되는 비율. 판정 모델이 근거 문장을 그대로 베껴 와야 하고, 그 문장이 근거에 없으면 "근거 없음"으로 바꾼다.
     검증할 주장이 없는 답변은 N/A (1점으로 세지 않는다).
  2) 항목 충족률(Correctness): 체크리스트의 must_include 항목을 의미 기준으로 충족(1) / 일부(0.5) / 미충족(0)으로 판정한 평균.
     must_not 항목에 걸리면 "금지 위반"으로 따로 센다 (충족률에서 빼지 않고 보고한다).
  3) 답변 관련성: 질문에 직접 답했는가 (직접 / 일부 / 벗어남).
- 같은 질문 3회의 평균과 흔들림(최고-최저)을 같이 본다. 3회 중 일부만 통과하는 질문은 "불안정"이다.
- 코드가 있는 답변을 실제로 실행해 보는 검사는 이 스크립트가 하지 않는다 (코드 실행은 별도 확인, 결과에 "미실행"으로 적는다).
- 사람 검수 표본: answer_review_sample_2026-10-15_<tag>.md (10%, 시드 고정).
- 결과: answer_results_2026-10-15_<tag>.jsonl / .md
"""

import argparse
import json
import os
import random
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.const.config import OPEN_API_KEY
from src.evaluation.grounding_eval_2026_10_15 import EXTRACT_PROMPT, MAX_CLAIMS, SNIPPET_CLIP, Claims, Support, judge_claim

HERE = Path(__file__).resolve().parent
SEED = 20261015
SAMPLE_RATE = 0.10
UNSTABLE_SPREAD = 0.34  # 같은 질문 3회의 충족률 차이가 이 이상이면 불안정으로 센다


class ItemVerdict(BaseModel):
    index: int = Field(description="항목 번호 (1부터)")
    verdict: Literal["met", "partial", "not"] = Field(description="의미상 충족=met, 일부만=partial, 없음=not")
    evidence: str = Field(description="판단 근거가 되는 답변 속 표현 또는 이유 한 문장")


class RubricJudgement(BaseModel):
    items: list[ItemVerdict] = Field(description="must_include 항목마다 하나씩")
    violations: list[str] = Field(description="답변이 걸린 must_not 항목 번호와 이유. 없으면 빈 목록")
    relevance: Literal["direct", "partial", "off"] = Field(description="질문에 직접 답했으면 direct, 일부만이면 partial, 벗어났으면 off")


RUBRIC_PROMPT = """개발 질문에 대한 답변을 체크리스트로 채점한다.

- 표현이 달라도 **의미가 같으면** 충족(met)이다. 문장이 같은지는 보지 않는다.
- 항목의 일부만 다루면 partial, 전혀 다루지 않으면 not이다.
- must_not 항목에 해당하는 내용이 답변에 있으면 violations에 "번호: 이유"로 적는다. 해당하지 않으면 빈 목록이다.
- relevance는 답변이 질문의 요구에 직접 답했는지로 판단한다.

[질문]
{question}

[답변]
{answer}

[must_include 항목]
{include}

[must_not 항목]
{exclude}"""

SCORE = {"met": 1.0, "partial": 0.5, "not": 0.0}


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def numbered(items):
    return "\n".join(f"{number}. {item}" for number, item in enumerate(items, start=1)) or "(없음)"


def context_as_sources(row):
    """답변 모델에 실제로 전달된 근거를 judge_claim이 읽는 출처 모양으로 바꾼다."""
    sources = [{"title": doc.get("title") or doc.get("chunk_id") or "", "snippet": doc.get("text") or ""} for doc in row.get("context_docs") or []]
    if row.get("mcp_results") and row["mcp_results"] != "[]":
        sources.append({"title": "MCP 도구 결과", "snippet": row["mcp_results"]})
    return sources


def make_models():
    name = os.getenv("EVAL_MODEL") or "gpt-4o-mini"
    base = ChatOpenAI(api_key=OPEN_API_KEY, model=name, temperature=0.0, timeout=120)
    return base.with_structured_output(Claims), base.with_structured_output(Support), base.with_structured_output(RubricJudgement), name


def evaluate(row, rubric, models):
    extract_model, support_model, rubric_model, _ = models
    sources = context_as_sources(row)
    claims = [c for c in extract_model.invoke(EXTRACT_PROMPT.format(answer=row["answer"])).claims[:MAX_CLAIMS] if c.needs_source]
    if sources:
        judged = [judge_claim(support_model, claim, sources) for claim in claims]
    else:
        judged = [{"claim": c.text, "supported": False, "quote": "", "note": "답변에 전달된 근거가 없음"} for c in claims]
    faithfulness = (sum(1 for c in judged if c["supported"]) / len(judged)) if judged else None  # 검증할 주장이 없으면 N/A

    verdict = rubric_model.invoke(
        RUBRIC_PROMPT.format(question=row["question"], answer=row["answer"], include=numbered(rubric["must_include"]), exclude=numbered(rubric["must_not"]))
    )
    by_index = {item.index: item for item in verdict.items}
    scores = [SCORE[by_index[number].verdict] if number in by_index else 0.0 for number in range(1, len(rubric["must_include"]) + 1)]
    return {
        "id": row["id"],
        "repeat": row["repeat"],
        "type": row["type"],
        "split": row["split"],
        "route": row.get("completed_routes", []) + [row.get("last_route")],
        "had_context": bool(sources),
        "claims": judged,
        "faithfulness": faithfulness,
        "items": [{"index": i.index, "verdict": i.verdict, "evidence": i.evidence} for i in verdict.items],
        "fulfillment": sum(scores) / len(scores) if scores else None,
        "violations": verdict.violations,
        "relevance": verdict.relevance,
    }


def mean(values):
    values = [v for v in values if v is not None]
    return (sum(values) / len(values)) if values else None


def fmt(value):
    return "N/A" if value is None else f"{value:.3f}"


def summarize(results, rows_by_key, skipped):
    def group(predicate):
        part = [r for r in results if predicate(r)]
        with_claims = [r for r in part if r["faithfulness"] is not None]
        return {
            "n": len(part),
            "faith": mean([r["faithfulness"] for r in part]),
            "faith_n": len(with_claims),
            "fulfill": mean([r["fulfillment"] for r in part]),
            "violation": sum(1 for r in part if r["violations"]),
            "direct": sum(1 for r in part if r["relevance"] == "direct"),
        }

    rows = [
        ("전체", lambda r: True),
        ("정답 있는 질문", lambda r: r["type"] == "answerable"),
        ("정답 없는 질문", lambda r: r["type"] == "no_answer"),
        ("tune", lambda r: r["split"] == "tune"),
        ("final", lambda r: r["split"] == "final"),
        ("근거를 받은 답변", lambda r: r["had_context"]),
        ("근거 없이 답한 답변", lambda r: not r["had_context"]),
    ]
    lines = ["| 구분 | 답변 수 | Faithfulness | (평가 가능 수) | 항목 충족률 | 금지 위반 답변 수 | 관련성 direct |", "|---|---|---|---|---|---|---|"]
    for label, predicate in rows:
        g = group(predicate)
        lines.append(f"| {label} | {g['n']} | {fmt(g['faith'])} | {g['faith_n']} | {fmt(g['fulfill'])} | {g['violation']} | {g['direct']}/{g['n']} |")

    per_question = {}
    for r in results:
        per_question.setdefault(r["id"], []).append(r)
    spreads = {qid: (max(x["fulfillment"] for x in v) - min(x["fulfillment"] for x in v)) for qid, v in per_question.items() if len(v) > 1 and all(x["fulfillment"] is not None for x in v)}
    unstable = sorted(qid for qid, spread in spreads.items() if spread >= UNSTABLE_SPREAD)
    return (
        "## 지표\n\n" + "\n".join(lines) + "\n\n## 집계\n\n"
        f"- 채점한 답변: {len(results)}개, 답변을 못 받아 제외한 실행: {skipped}개\n"
        f"- Faithfulness는 출처가 필요한 사실 주장이 있는 답변만 평균 (주장이 없으면 N/A). 근거 없이 답한 답변은 주장이 모두 \"근거 없음\"으로 계산된다.\n"
        f"- 불안정한 질문(3회 항목 충족률 차이 {UNSTABLE_SPREAD} 이상): {len(unstable)}개 {unstable}\n"
        "- 코드 실행 검사: 이 스크립트는 하지 않음 (코드가 있는 답변은 별도로 실행해 확인해야 하며, 지금은 미실행)\n"
    )


def review_sample(results, rows_by_key, rubrics):
    rng = random.Random(SEED)
    picked = rng.sample(results, max(1, round(len(results) * SAMPLE_RATE)))
    parts = ["# 2차(답변) 평가 사람 검수 표본 (10%)", "", "각 항목의 모델 판정이 맞는지 확인하고 틀린 것에 표시하세요.", ""]
    for r in picked:
        row = rows_by_key[(r["id"], r["repeat"])]
        rubric = rubrics[r["id"]]
        parts += [f"## {r['id']} (회차 {r['repeat']}, {r['type']})", "", f"**질문**: {row['question']}", "", "**답변**", "", row["answer"], "", "**항목 판정**"]
        parts += [f"- [ ] {item['index']}. {rubric['must_include'][item['index'] - 1]} → {item['verdict']} ({item['evidence']})" for item in r["items"] if 1 <= item["index"] <= len(rubric["must_include"])]
        parts += [f"- 금지 위반: {r['violations'] or '없음'}", f"- 관련성: {r['relevance']}, Faithfulness: {fmt(r['faithfulness'])}", ""]
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="baseline")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    answers_path = HERE / f"answers_2026-10-15_{args.tag}.jsonl"
    rubric_path = HERE / "answer_rubric_2026-10-15.jsonl"
    if not answers_path.exists() or not rubric_path.exists():
        raise SystemExit("answers_2026-10-15_<tag>.jsonl과 answer_rubric_2026-10-15.jsonl이 모두 필요합니다.")
    rows = read_jsonl(answers_path)
    rubrics = {r["id"]: r for r in read_jsonl(rubric_path)}
    ok_rows = [r for r in rows if r["status"] == "ok"]
    rows_by_key = {(r["id"], r["repeat"]): r for r in ok_rows}

    stem = f"answer_results_2026-10-15_{args.tag}"
    jsonl_path, md_path = HERE / f"{stem}.jsonl", HERE / f"{stem}.md"
    if jsonl_path.exists() or md_path.exists():
        raise SystemExit(f"{stem} 결과가 이미 있습니다. --tag를 바꿔 주세요.")

    models = make_models()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda row: evaluate(row, rubrics[row["id"]], models), ok_rows))
    jsonl_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in results) + "\n", encoding="utf-8")
    md_path.write_text(
        f"# 2차(답변) 평가 결과: {args.tag}\n\n- 채점 모델: {models[3]}, 답변 파일: {answers_path.name}, 체크리스트: {rubric_path.name}\n\n" + summarize(results, rows_by_key, len(rows) - len(ok_rows)),
        encoding="utf-8",
    )
    (HERE / f"answer_review_sample_2026-10-15_{args.tag}.md").write_text(review_sample(results, rows_by_key, rubrics), encoding="utf-8")
    print("저장:", md_path)


if __name__ == "__main__":
    main()
