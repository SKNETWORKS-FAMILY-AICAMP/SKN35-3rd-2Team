"""
1차(검색) 평가용 질문 50개를 만든다: 정답 있는 질문 40개 + 정답 없는 질문 10개.

    python -m src.evaluation.retrieval_make_dataset_2026_10_15

- 정답 있는 질문: 청크를 보고 gpt-4o-mini가 질문을 만든다. 그 청크가 곧 정답(원본 청크)이다.
  40개 중 28개는 청크 1개, 12개는 같은 문서의 이웃 청크 2개를 함께 읽어야 답할 수 있는 질문(복수 근거)이다.
  기술(langchain, langgraph, mcp)별로 고르게 뽑고, 튜닝용 20개와 최종용 20개로 나눈다 (기술별 비율이 같게).
- 정답 없는 질문: 사람이 읽고 검토할 수 있게 코드에 직접 적어 두었다 (모르는 내부 라이브러리, 정보 부족, 범위 밖).
- 모델 이름은 환경변수 EVAL_MODEL (없으면 gpt-4o-mini). 같은 시드면 같은 청크를 뽑는다.
- 결과: retrieval_questions_2026-10-15.jsonl (이 폴더). 이미 있으면 덮어쓰지 않는다 (--force로만 덮어쓴다).
"""

import argparse
import json
import os
import random
from collections import defaultdict
from pathlib import Path

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.const.config import OPEN_API_KEY

HERE = Path(__file__).resolve().parent
CHUNKS_PATH = HERE.parents[1] / "data" / "processed" / "chunks.jsonl"
OUTPUT_PATH = HERE / "retrieval_questions_2026-10-15.jsonl"

SEED = 20261015
SINGLE = 28  # 청크 1개로 답하는 질문 수
MULTI = 12  # 같은 문서의 이웃 청크 2개가 필요한 질문 수
MIN_CHARS = 500  # 너무 짧은 청크(제목만 있는 등)는 질문을 만들기 어려워 제외한다
MAX_CHARS = 2500

NO_ANSWER = [
    # 모르는 내부 라이브러리 / 오류 코드 (문서에 없다)
    ("internal", "사내 라이브러리 NovaFlowKit에서 NF-2207 오류가 나요. 원인과 해결 명령어를 알려 주세요."),
    ("internal", "내부용 프레임워크 DeepHarbor의 HarborRetryPolicy 설정은 어떻게 하나요?"),
    ("internal", "우리 팀 전용 SDK AtlasAgentSDK에서 ATLAS-5013 에러가 나는 이유가 뭔가요?"),
    ("internal", "비공개 패키지 corp_langtools의 sync_memory() 함수 사용법을 알려 주세요."),
    # 정보 부족 (오류 메시지도 환경도 없다)
    ("vague", "앱 실행이 안 돼요. 해결해 주세요."),
    ("vague", "아까 그 오류가 또 나요. 어떻게 해야 하죠?"),
    ("vague", "코드가 이상하게 동작해요."),
    # 범위 밖 (LangChain, LangGraph, MCP와 무관하다)
    ("out_of_scope", "Django ORM에서 select_related와 prefetch_related의 차이가 뭔가요?"),
    ("out_of_scope", "React에서 useEffect 안의 비동기 함수는 어떻게 정리하나요?"),
    ("out_of_scope", "PostgreSQL 인덱스가 사용되지 않는 이유를 어떻게 확인하나요?"),
]


class GeneratedQuestion(BaseModel):
    question: str = Field(description="개발자가 실제로 물어볼 법한 한국어 질문 한 개")


SINGLE_PROMPT = """아래는 {tech} 공식 문서의 일부다. 이 글을 근거로 답할 수 있는, 개발자가 실제로 물어볼 법한 질문을 한국어로 한 개 만든다.

조건:
- 이 글만으로 답할 수 있어야 한다. 글에 없는 내용을 묻지 않는다.
- 글의 문장을 그대로 베끼지 않고 자연스러운 말로 바꾼다.
- "이 문서", "위 글", "아래 내용" 같은 지시어를 쓰지 않는다. 질문만 읽어도 무엇을 묻는지 알 수 있어야 한다.
- 영어 용어, 함수와 클래스 이름은 그대로 써도 된다.
- 설명, 번호, 따옴표 없이 질문만 쓴다.

[문서 제목] {title}
[글]
{text}"""

MULTI_PROMPT = """아래는 {tech} 공식 문서에서 이어진 두 부분이다. 두 부분을 모두 읽어야 완전하게 답할 수 있는, 개발자가 실제로 물어볼 법한 질문을 한국어로 한 개 만든다.

조건:
- 두 부분의 내용이 모두 필요해야 한다. 한쪽만으로 답이 끝나면 안 된다.
- 글에 없는 내용을 묻지 않는다.
- 글의 문장을 그대로 베끼지 않고 자연스러운 말로 바꾼다.
- "이 문서", "위 글", "첫 번째 부분" 같은 지시어를 쓰지 않는다.
- 설명, 번호, 따옴표 없이 질문만 쓴다.

[문서 제목] {title}
[부분 1]
{text1}

[부분 2]
{text2}"""


def load_chunks():
    rows = [json.loads(line) for line in CHUNKS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    return rows


def usable(row):
    return MIN_CHARS <= len(row["text"]) <= MAX_CHARS


def pick(rows, rng):
    """기술별로 고르게, 문서를 겹치지 않게 뽑는다. [(종류, [청크...]), ...] 순서가 섞인 40개."""
    by_doc = defaultdict(list)
    for row in rows:
        by_doc[row["parent_id"]].append(row)
    for chunks in by_doc.values():
        chunks.sort(key=lambda r: int(r["chunk_index"]))

    techs = sorted({row["tech"] for row in rows})
    singles_pool = {tech: [] for tech in techs}
    multis_pool = {tech: [] for tech in techs}
    for chunks in by_doc.values():
        tech = chunks[0]["tech"]
        for index, chunk in enumerate(chunks):
            if usable(chunk):
                singles_pool[tech].append(chunk)
            if index + 1 < len(chunks) and usable(chunk) and usable(chunks[index + 1]):
                multis_pool[tech].append((chunk, chunks[index + 1]))

    def spread(total):
        base, extra = divmod(total, len(techs))
        return {tech: base + (1 if i < extra else 0) for i, tech in enumerate(techs)}

    used_docs = set()
    picked = []
    for kind, pool, total in (("multi", multis_pool, MULTI), ("single", singles_pool, SINGLE)):
        for tech, count in spread(total).items():
            candidates = pool[tech][:]
            rng.shuffle(candidates)
            taken = 0
            for item in candidates:
                chunks = list(item) if kind == "multi" else [item]
                if chunks[0]["parent_id"] in used_docs:
                    continue
                used_docs.add(chunks[0]["parent_id"])
                picked.append((kind, chunks))
                taken += 1
                if taken == count:
                    break
            if taken < count:
                raise RuntimeError(f"{tech}에서 {kind} 청크를 {count}개 뽑지 못했습니다 ({taken}개).")
    rng.shuffle(picked)
    return picked


def split_labels(picked):
    """기술별로 같은 비율이 되게 튜닝용/최종용을 번갈아 나누고, 전체가 정확히 반반이 되게 한다.

    질문 수가 홀수인 기술은 번갈아 가며 튜닝용 또는 최종용으로 시작해서 한쪽이 하나 더 많아지게 한다.
    """
    techs = [chunks[0]["tech"] for _, chunks in picked]
    totals = defaultdict(int)
    for tech in techs:
        totals[tech] += 1
    start = {}
    flip = 0
    for tech in sorted(totals):
        if totals[tech] % 2:
            start[tech] = "tune" if flip % 2 == 0 else "final"
            flip += 1
        else:
            start[tech] = "tune"
    counter = defaultdict(int)
    labels = []
    for tech in techs:
        first, second = ("tune", "final") if start[tech] == "tune" else ("final", "tune")
        labels.append(first if counter[tech] % 2 == 0 else second)
        counter[tech] += 1
    return labels


def make_model():
    model = os.getenv("EVAL_MODEL") or "gpt-4o-mini"
    return ChatOpenAI(api_key=OPEN_API_KEY, model=model, temperature=0.0, timeout=120).with_structured_output(GeneratedQuestion), model


def generate(llm, kind, chunks):
    first = chunks[0]
    if kind == "single":
        prompt = SINGLE_PROMPT.format(tech=first["tech"], title=first["title"], text=first["text"])
    else:
        prompt = MULTI_PROMPT.format(tech=first["tech"], title=first["title"], text1=chunks[0]["text"], text2=chunks[1]["text"])
    return llm.invoke(prompt).question.strip()


def build(rows, llm, model_name):
    rng = random.Random(SEED)
    picked = pick(rows, rng)
    labels = split_labels(picked)
    records = []
    for number, ((kind, chunks), split) in enumerate(zip(picked, labels), start=1):
        question = generate(llm, kind, chunks)
        records.append(
            {
                "id": f"R{number:02d}",
                "type": "answerable",
                "split": split,
                "kind": kind,
                "tech": chunks[0]["tech"],
                "question": question,
                "source_chunk_ids": [chunk["chunk_id"] for chunk in chunks],
                "generated_by": model_name,
            }
        )
        print(records[-1]["id"], split, kind, chunks[0]["tech"], question)
    for offset, (category, question) in enumerate(NO_ANSWER, start=1):
        records.append(
            {
                "id": f"N{offset:02d}",
                "type": "no_answer",
                "split": "tune" if offset % 2 else "final",
                "kind": category,
                "tech": None,
                "question": question,
                "source_chunk_ids": [],
                "generated_by": "human",
            }
        )
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="이미 있는 질문 파일을 덮어쓴다")
    args = parser.parse_args()
    if OUTPUT_PATH.exists() and not args.force:
        raise SystemExit(f"{OUTPUT_PATH.name}이(가) 이미 있습니다. 덮어쓰려면 --force를 붙이세요.")
    llm, model_name = make_model()
    records = build(load_chunks(), llm, model_name)
    OUTPUT_PATH.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
    print(f"저장: {OUTPUT_PATH} ({len(records)}개)")


if __name__ == "__main__":
    main()
