"""
2차(답변), 3차(출처) 평가에 쓸 답변을 모은다. 질문마다 실제 앱 그래프를 돌려서 답변, 출처, 답변에 실제로 전달된 근거를 저장한다.

    python -m src.evaluation.answer_collect_2026_10_15 [--tag 이름] [--repeats 3] [--split tune|final|all]

- 입력: retrieval_questions_2026-10-15.jsonl (정답 있는 40개 + 정답 없는 10개)
- 질문마다 repeats번(기본 3번) 새 대화로 실행한다. 같은 질문도 답이 달라지기 때문이다.
- 저장하는 것: 답변, 화면에 표시되는 출처(sources), 답변 모델에 전달된 검색 문서(context_docs), 도구 결과(mcp_results), 소요 시간, 실패 여부.
- 답변을 못 받았거나 오류로 끝난 실행도 "failed"로 남긴다 (성공률에 포함하려는 것이다).
- 이미 모은 (질문, 회차)는 건너뛴다. 중간에 끊겨도 같은 --tag로 다시 실행하면 이어서 한다.
- 결과: answers_2026-10-15_<tag>.jsonl (이 폴더). 앱 코드는 읽기만 한다.
"""

import argparse
import json
import time
from pathlib import Path

from langchain_core.messages import AIMessage

from src.app import chat_service as cs

HERE = Path(__file__).resolve().parent
QUESTIONS_PATH = HERE / "retrieval_questions_2026-10-15.jsonl"
CLIP_DOC_CHARS = 4000
CLIP_MCP_CHARS = 4000


def read_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_once(question):
    """새 대화 하나로 그래프를 돌린다. (결과 딕셔너리, 실패 사유 또는 None)."""
    state = {
        "messages": [{"role": "user", "content": question}],
        "original_question": question,
        "image": None,
        "image_analysis": "",
        "retrieved_docs": [],
        "mcp_results": [],
        "answer": "",
    }
    result = cs.get_graph().invoke(state, config={"configurable": {"thread_id": f"eval-{time.time_ns()}"}})
    answer = cs.text_content(result.get("answer"))
    if not answer.strip():  # general 노드는 answer 키 없이 messages로만 답을 돌려준다 (run_chat과 같게 마지막 메시지를 읽는다)
        replies = result.get("messages") or []
        answer = cs.text_content(replies[-1].content) if replies and isinstance(replies[-1], AIMessage) else ""
    result["answer"] = answer
    if not answer.strip():
        return result, "답변이 비어 있습니다."
    return result, None


def summarize(result):
    docs = [
        {
            "chunk_id": doc.metadata.get("chunk_id"),
            "title": doc.metadata.get("title"),
            "text": doc.page_content[:CLIP_DOC_CHARS],
        }
        for doc in result.get("retrieved_docs") or []
        if hasattr(doc, "page_content")
    ]
    return docs, str(result.get("mcp_results") or "")[:CLIP_MCP_CHARS]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="baseline")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--split", choices=["tune", "final", "all"], default="all")
    parser.add_argument("--limit", type=int, default=0, help="앞의 몇 개 질문만 실행한다 (시험용)")
    args = parser.parse_args()

    out_path = HERE / f"answers_2026-10-15_{args.tag}.jsonl"
    done = {(r["id"], r["repeat"]) for r in read_jsonl(out_path)}
    questions = [r for r in read_jsonl(QUESTIONS_PATH) if args.split == "all" or r["split"] == args.split]
    if args.limit:
        questions = questions[: args.limit]

    with out_path.open("a", encoding="utf-8") as out:
        for repeat in range(1, args.repeats + 1):
            for record in questions:
                if (record["id"], repeat) in done:
                    continue
                started = time.time()
                row = {"id": record["id"], "repeat": repeat, "type": record["type"], "split": record["split"], "question": record["question"]}
                try:
                    result, problem = run_once(record["question"])
                    docs, mcp_text = summarize(result)
                    row.update(
                        status="failed" if problem else "ok",
                        problem=problem,
                        answer=result.get("answer") or "",
                        completed_routes=result.get("completed_routes") or [],
                        last_route=result.get("route"),
                        sources=cs.result_sources(result),
                        context_docs=docs,
                        mcp_results=mcp_text,
                    )
                except Exception as exc:
                    row.update(status="failed", problem=f"{type(exc).__name__}: {str(exc)[:200]}", answer="", sources=[], context_docs=[], mcp_results="")
                row["seconds"] = round(time.time() - started, 1)
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                out.flush()
                print(record["id"], repeat, row["status"], row["seconds"], flush=True)
    print("저장:", out_path)


if __name__ == "__main__":
    main()
