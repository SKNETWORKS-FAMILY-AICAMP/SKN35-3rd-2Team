"""
3차(출처 검증) 평가: 답변에 표시된 출처가 정말 근거인지 확인한다.

    python -m src.evaluation.grounding_eval_2026_10_15 --tag baseline [--no-links]

- 입력: answers_2026-10-15_<tag>.jsonl (answer_collect_2026_10_15가 모은 답변과 출처)
- 우리 앱의 답변 본문에는 [1] 같은 인용 번호가 없고 출처 목록이 따로 표시된다. 그래서 "답변의 각 주장이
  화면에 표시된 출처 중 하나로 뒷받침되는가"를 본다.

확인하는 것
  1) 링크 유효성: 출처 URL이 열리는가 (코드로 확인. 200~399면 유효). URL이 없는 출처는 따로 센다.
  2) 주장-출처 일치: 답변에서 확인 가능한 주장을 뽑고(gpt-4o-mini), 주장마다 출처에서 근거 문장을 그대로 베껴 오게 한다.
     베껴 온 문장이 실제 출처 글에 없으면 "근거 없음"으로 바꾼다 (판정 모델이 지어낸 근거를 걸러 내려는 것이다).
  3) 필요한 인용 누락: 출처가 필요한 주장인데 어떤 출처로도 뒷받침되지 않은 주장 수. 0건이 목표다.
  4) 정답 없는 질문(no_answer)에 출처를 표시했는지: 근거가 없는 질문에 관련 없는 출처를 보여 주면 사용자가 속는다.
  - 버전 적합성은 질문에 패키지 버전이 있는 경우만 판정하는데, 지금 질문 목록에는 버전이 없어 이번에는 "해당 없음"이다.
- 주장이 하나도 없는 답변(되묻기, 거절 등)은 N/A이다. 답변을 못 받은 실행은 평가하지 않고 개수만 센다.
- 결과: grounding_results_2026-10-15_<tag>.jsonl, grounding_results_2026-10-15_<tag>.md. 사람 검수 10%는 별도로 기록한다.
"""

import argparse
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.const.config import OPEN_API_KEY

HERE = Path(__file__).resolve().parent
MAX_CLAIMS = 8
SNIPPET_CLIP = 3000
LINK_TIMEOUT = 10


class Claim(BaseModel):
    text: str = Field(description="답변에서 뽑은 확인 가능한 주장 한 문장")
    needs_source: bool = Field(description="출처가 있어야 믿을 수 있는 사실 주장이면 true, 일반적인 조언이나 예의 문장이면 false")


class Claims(BaseModel):
    claims: list[Claim] = Field(description=f"최대 {MAX_CLAIMS}개")


class Support(BaseModel):
    supported: bool = Field(description="출처 중 하나가 이 주장을 뒷받침하면 true")
    source_number: int = Field(description="뒷받침하는 출처 번호. 없으면 0")
    quote: str = Field(description="그 출처 글에서 근거가 되는 문장을 한 글자도 바꾸지 말고 그대로 베낀 것. 없으면 빈 문자열")


EXTRACT_PROMPT = f"""아래 답변에서 사실로 주장하는 문장을 최대 {MAX_CLAIMS}개 뽑는다. 답변의 핵심 주장부터 고른다.

- API, 클래스, 함수, 설정 이름이나 동작을 단정하는 문장은 needs_source=true이다.
- 인사, 되묻는 말, 일반적인 조언, "~할 수 있습니다" 수준의 안내는 needs_source=false이다.
- 코드 블록은 주장으로 뽑지 않는다.
- 주장이 하나도 없으면 빈 목록을 돌려준다.

[답변]
{{answer}}"""

SUPPORT_PROMPT = """주장 하나와 출처 목록이 있다. 출처 중 이 주장을 **직접 뒷받침하는** 것이 있는지 판정한다.

- 출처의 글에 그 내용이 실제로 쓰여 있어야 한다. 비슷한 주제를 다룰 뿐이면 supported=false이다.
- supported=true이면 근거가 되는 문장을 출처 글에서 한 글자도 바꾸지 말고 그대로 quote에 베낀다.
- 출처 글에서 근거를 찾을 수 없으면 supported=false, source_number=0, quote는 빈 문자열이다.

[주장]
{claim}

[출처 목록]
{sources}"""


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def normalize(text):
    return re.sub(r"\s+", " ", text or "").strip().lower()


def check_link(url):
    """출처 URL이 열리는지. (유효 여부, 상태 설명)"""
    try:
        response = requests.get(url, timeout=LINK_TIMEOUT, allow_redirects=True, stream=True, headers={"User-Agent": "Mozilla/5.0"})
        response.close()
        return 200 <= response.status_code < 400, str(response.status_code)
    except Exception as exc:
        return False, type(exc).__name__


def make_models():
    name = os.getenv("EVAL_MODEL") or "gpt-4o-mini"
    base = ChatOpenAI(api_key=OPEN_API_KEY, model=name, temperature=0.0, timeout=120)
    return base.with_structured_output(Claims), base.with_structured_output(Support), name


def format_sources(sources):
    return "\n\n".join(f"[출처 {number}] {source.get('title') or ''}\n{(source.get('snippet') or '')[:SNIPPET_CLIP]}" for number, source in enumerate(sources, start=1))


def judge_claim(support_model, claim, sources):
    verdict = support_model.invoke(SUPPORT_PROMPT.format(claim=claim.text, sources=format_sources(sources)))
    supported, number, quote = verdict.supported, verdict.source_number, verdict.quote
    note = None
    if supported:
        valid_number = 1 <= number <= len(sources)
        quote_found = valid_number and normalize(quote) and normalize(quote) in normalize(sources[number - 1].get("snippet"))
        if not quote_found:
            supported, note = False, "판정 모델이 가져온 근거 문장이 출처에 없어 근거 없음으로 바꿈"
    return {"claim": claim.text, "needs_source": claim.needs_source, "supported": supported, "source_number": number if supported else 0, "quote": quote if supported else "", "note": note}


def evaluate_answer(row, extract_model, support_model, link_cache):
    sources = row.get("sources") or []
    links = []
    for source in sources:
        url = source.get("url")
        if not url:
            links.append({"url": None, "valid": None, "status": "URL 없음"})
            continue
        if url not in link_cache:
            link_cache[url] = check_link(url) if link_cache.get("__check__", True) else (None, "확인 안 함")
        valid, status = link_cache[url]
        links.append({"url": url, "valid": valid, "status": status})

    result = {"id": row["id"], "repeat": row["repeat"], "type": row["type"], "source_count": len(sources), "links": links, "claims": []}
    claims = extract_model.invoke(EXTRACT_PROMPT.format(answer=row["answer"])).claims[:MAX_CLAIMS]
    if not sources:
        result["claims"] = [{"claim": c.text, "needs_source": c.needs_source, "supported": False, "source_number": 0, "quote": "", "note": "표시된 출처가 없음"} for c in claims]
    else:
        result["claims"] = [judge_claim(support_model, claim, sources) for claim in claims]
    needing = [c for c in result["claims"] if c["needs_source"]]
    result["missing_citations"] = sum(1 for c in needing if not c["supported"])
    result["support_rate"] = (sum(1 for c in result["claims"] if c["supported"]) / len(result["claims"])) if result["claims"] else None  # 주장이 없으면 N/A
    return result


def summarize(results, skipped_failed):
    answerable = [r for r in results if r["type"] == "answerable"]
    no_answer = [r for r in results if r["type"] == "no_answer"]
    link_items = [link for r in results for link in r["links"]]
    checked = [link for link in link_items if link["valid"] is not None]
    rated = [r for r in answerable if r["support_rate"] is not None]
    lines = [
        "## 요약",
        "",
        f"- 평가한 답변: {len(results)}개 (정답 있는 질문 {len(answerable)}개, 정답 없는 질문 {len(no_answer)}개), 답변을 못 받아 제외한 실행: {skipped_failed}개",
        f"- 링크 유효성: {sum(1 for l in checked if l['valid'])}/{len(checked)} ({(sum(1 for l in checked if l['valid']) / len(checked)):.3f})" if checked else "- 링크 유효성: 확인한 링크 없음",
        f"- URL이 없는 출처: {sum(1 for l in link_items if l['valid'] is None and l['status'] == 'URL 없음')}개",
        f"- 주장-출처 일치율(정답 있는 질문, 주장이 있는 답변 {len(rated)}개 평균): " + (f"{sum(r['support_rate'] for r in rated) / len(rated):.3f}" if rated else "N/A"),
        f"- 주장이 없어 N/A인 답변: {sum(1 for r in answerable if r['support_rate'] is None)}개",
        f"- 필요한 인용 누락(출처가 필요한데 뒷받침 안 된 주장): 총 {sum(r['missing_citations'] for r in answerable)}건, 누락이 1건 이상인 답변 {sum(1 for r in answerable if r['missing_citations'])}개",
        f"- 정답 없는 질문 중 출처를 표시한 답변: {sum(1 for r in no_answer if r['source_count'])}/{len(no_answer)}개 (근거가 없는 질문에 출처를 보이면 사용자가 속을 수 있다)",
        "- 버전 적합성: 질문 목록에 패키지 버전이 없어 해당 없음",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="baseline")
    parser.add_argument("--no-links", action="store_true", help="링크 요청을 보내지 않는다 (오프라인 시험용)")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    answers_path = HERE / f"answers_2026-10-15_{args.tag}.jsonl"
    if not answers_path.exists():
        raise SystemExit(f"{answers_path.name}이(가) 없습니다. 먼저 answer_collect_2026_10_15를 실행하세요.")
    rows = read_jsonl(answers_path)
    ok_rows = [r for r in rows if r["status"] == "ok"]
    skipped_failed = len(rows) - len(ok_rows)

    stem = f"grounding_results_2026-10-15_{args.tag}"
    jsonl_path, md_path = HERE / f"{stem}.jsonl", HERE / f"{stem}.md"
    if jsonl_path.exists() or md_path.exists():
        raise SystemExit(f"{stem} 결과가 이미 있습니다. --tag를 바꿔 주세요.")

    extract_model, support_model, model_name = make_models()
    link_cache = {"__check__": not args.no_links}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda row: evaluate_answer(row, extract_model, support_model, link_cache), ok_rows))
    jsonl_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in results) + "\n", encoding="utf-8")
    md_path.write_text(f"# 3차(출처 검증) 평가 결과: {args.tag}\n\n- 채점 모델: {model_name}, 답변 파일: {answers_path.name}\n\n" + summarize(results, skipped_failed) + "\n", encoding="utf-8")
    print("저장:", md_path)


if __name__ == "__main__":
    main()
