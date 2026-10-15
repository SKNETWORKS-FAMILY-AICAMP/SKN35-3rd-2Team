"""
1차(검색) 평가 실행: 질문마다 RAG의 검색 순위를 받아 정답표와 비교해 Hit@k, Recall@k, MRR, nDCG@k를 낸다.

    python -m src.evaluation.retrieval_eval_2026_10_15 [--tag 이름] [--split tune|final|all]

- 입력: retrieval_questions_2026-10-15.jsonl, retrieval_gold_2026-10-15.jsonl
- 정답이 없는 질문(no_answer)은 분모에서 빼고, 개수와 "상위 문서 점수"만 따로 적는다.
- 검색이 실패해 순위를 못 받은 질문은 "측정 불가"로 적고 평균에서 뺀다 (개수는 보고한다). 검색은 했는데 정답을 놓친 것은 0점이다.
- 결과: retrieval_results_<실행 날짜>_<tag>.jsonl (질문별), retrieval_results_<실행 날짜>_<tag>.md (요약표).
  같은 이름이 있으면 덮어쓰지 않는다. 개선 전후 비교는 tag를 바꿔서 나란히 둔다.
- 앱 코드는 읽기만 하고, 평가하는 동안 모델, 프롬프트, 검색 설정을 바꾸지 않는다 (아래 환경 기록에 남는다).
"""

import argparse
import json
import subprocess
import time
from datetime import date
from pathlib import Path

from src.const import rag_config
from src.const.config import OPEN_MODEL, RERANK_MODEL
from src.evaluation.retrieval_metrics_2026_10_15 import KS, average, question_metrics
from src.evaluation.retrieval_run_2026_10_15 import ranked_candidates

HERE = Path(__file__).resolve().parent
QUESTIONS_PATH = HERE / "retrieval_questions_2026-10-15.jsonl"
GOLD_PATH = HERE / "retrieval_gold_2026-10-15.jsonl"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def git_state():
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE.parents[1], check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "src", "data"], capture_output=True, text=True, cwd=HERE.parents[1], check=True).stdout.strip()
        return commit, "미커밋 변경 있음" if dirty else "미커밋 변경 없음"
    except Exception:
        return "알 수 없음", "알 수 없음"


def run_question(record, gold_by_id):
    started = time.time()
    try:
        candidates = ranked_candidates(record["question"])
    except Exception as exc:
        return {"id": record["id"], "status": "failed", "error": f"{type(exc).__name__}: {str(exc)[:200]}", "seconds": round(time.time() - started, 1)}
    ranked_ids = [item["chunk_id"] for item in candidates]
    result = {
        "id": record["id"],
        "status": "ok",
        "ranked_chunk_ids": ranked_ids,
        "rerank_scores": [item["rerank_score"] for item in candidates],
        "seconds": round(time.time() - started, 1),
    }
    if record["type"] == "answerable":
        result["gold_chunk_ids"] = gold_by_id[record["id"]]["gold_chunk_ids"]
        result["metrics"] = question_metrics(ranked_ids, result["gold_chunk_ids"])
    return result


def table(rows):
    header = "| 구분 | 평가 가능 수 | " + " | ".join(f"Hit@{k}" for k in KS) + " | " + " | ".join(f"Recall@{k}" for k in KS) + " | MRR | " + " | ".join(f"nDCG@{k}" for k in KS) + " |"
    divider = "|" + "---|" * (2 + 3 * len(KS) + 1)
    lines = [header, divider]
    for label, summary in rows:
        if summary["n"] == 0:
            lines.append(f"| {label} | 0 |" + " - |" * (3 * len(KS) + 1))
            continue
        cells = [f"{summary[f'hit@{k}']:.3f}" for k in KS] + [f"{summary[f'recall@{k}']:.3f}" for k in KS] + [f"{summary['mrr']:.3f}"] + [f"{summary[f'ndcg@{k}']:.3f}" for k in KS]
        lines.append(f"| {label} | {summary['n']} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_report(tag, split, questions, results):
    by_id = {record["id"]: record for record in questions}
    ok = [r for r in results if r["status"] == "ok"]
    failed = [r for r in results if r["status"] == "failed"]
    scored = [r for r in ok if "metrics" in r]

    def subset(predicate):
        return average([r["metrics"] for r in scored if predicate(by_id[r["id"]])])

    rows = [("전체", average([r["metrics"] for r in scored]))]
    for name in ("tune", "final"):
        rows.append((f"{name}", subset(lambda rec, name=name: rec["split"] == name)))
    for tech in sorted({by_id[r["id"]]["tech"] for r in scored}):
        rows.append((f"기술: {tech}", subset(lambda rec, tech=tech: rec["tech"] == tech)))
    for kind in ("single", "multi"):
        rows.append((f"근거 {'1개' if kind == 'single' else '2개(복수)'}", subset(lambda rec, kind=kind: rec["kind"] == kind)))

    no_answer = [r for r in ok if by_id[r["id"]]["type"] == "no_answer"]
    top_scores = [r["rerank_scores"][0] for r in no_answer if r["rerank_scores"]]
    commit, dirty = git_state()
    lines = [
        f"# 1차(검색) 평가 결과: {tag}",
        "",
        f"- 실행 날짜: {date.today().isoformat()}, 범위: {split}",
        f"- 커밋: {commit} ({dirty})",
        f"- 앱 채팅 모델: {OPEN_MODEL}, 재정렬 모델: {RERANK_MODEL}, 재정렬 통과 점수: {rag_config.RERANK_SCORE_THRESHOLD}, 재시도 최대: {rag_config.MAX_RETRY}",
        "- 검색 순위: 마지막 rerank 직후 상위 5개 (필터, 압축 이전). K는 1, 3, 5",
        "- 정답표: gpt-4o-mini 판정 + 원본 청크 (retrieval_gold_2026-10-15.jsonl). 사람 검수 10%는 별도 기록",
        "",
        "## 지표 (정답 있는 질문만)",
        "",
        table(rows),
        "",
        "## 집계",
        "",
        f"- 실행 시도: {len(results)}개, 검색 성공: {len(ok)}개, 측정 불가(실패): {len(failed)}개",
        f"- 검색 지표 평가 가능: {len(scored)}개 (정답 있는 질문 중 검색 성공)",
        f"- 정답 없는 질문: {len(no_answer)}개는 지표 분모에서 제외. 1위 재정렬 점수 평균: " + (f"{sum(top_scores) / len(top_scores):.3f}" if top_scores else "-"),
        f"- 검색 시간 중앙값: " + (f"{sorted(r['seconds'] for r in results)[len(results) // 2]}초" if results else "-"),
    ]
    if failed:
        lines += ["", "## 측정 불가 질문", ""] + [f"- {r['id']}: {r['error']}" for r in failed]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="baseline", help="결과 파일 이름에 붙는 이름 (개선 전후 비교용)")
    parser.add_argument("--split", choices=["tune", "final", "all"], default="all")
    args = parser.parse_args()

    questions = read_jsonl(QUESTIONS_PATH)
    gold_by_id = {row["id"]: row for row in read_jsonl(GOLD_PATH)}
    questions = [r for r in questions if args.split == "all" or r["split"] == args.split]
    missing = [r["id"] for r in questions if r["type"] == "answerable" and r["id"] not in gold_by_id]
    if missing:
        raise SystemExit(f"정답표가 없는 질문이 있습니다: {missing}. 먼저 retrieval_label_2026_10_15를 실행하세요.")

    stem = f"retrieval_results_{date.today().isoformat()}_{args.tag}"
    jsonl_path, md_path = HERE / f"{stem}.jsonl", HERE / f"{stem}.md"
    if jsonl_path.exists() or md_path.exists():
        raise SystemExit(f"{stem} 결과가 이미 있습니다. --tag를 바꿔 주세요.")

    results = []
    with jsonl_path.open("w", encoding="utf-8") as out:
        for record in questions:
            result = run_question(record, gold_by_id)
            results.append(result)
            out.write(json.dumps(result, ensure_ascii=False) + "\n")
            out.flush()
            print(record["id"], result["status"], result.get("metrics", {}).get("hit@5", "-"), flush=True)
    md_path.write_text(build_report(args.tag, args.split, questions, results), encoding="utf-8")
    print("저장:", md_path)


if __name__ == "__main__":
    main()
