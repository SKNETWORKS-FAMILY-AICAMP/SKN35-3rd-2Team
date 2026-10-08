"""
사용자 질문 재작성 (Query Rewrite)

사용자 질문은 대개 한국어이고, 앞 대화에 기대거나("그럼 그건 어떻게 고쳐?"), 에러 로그가 통째로 붙어 있습니다.
문서는 영어이므로 그대로 검색하면 잘 안 맞습니다. 여기서는 질문을 검색하기 좋은 형태로 바꿉니다.

  입력: "아까 그 에러 또 나요. GraphRecursionError: Recursion limit of 25 reached ... 어떻게 늘려요?"
        + 대화 기록(선택)
  출력 (RewrittenQuery)
    standalone_question : 대화 기록 없이도 이해되는 한국어 질문   → 답변 생성·되묻기에 사용
    search_query        : 영어 검색어 (에러 이름·API 이름 그대로) → 검색에 사용
    tech                : langchain / langgraph / mcp / unknown   → retriever 의 tech 필터 후보
    error_keywords      : ["GraphRecursionError", "recursion_limit"] → 키워드(BM25) 검색 보강

multi_query 와 차이
  query_rewrite : 질문 1개 → "가장 좋은" 검색어 1개 (+ 기술·에러 정보 추출)
  multi_query   : 질문 1개 → 다른 각도의 검색어 여러 개 (검색 범위 넓히기)
  보통 rewrite 로 정리한 뒤 필요하면 multi_query 로 넓힙니다.

API 키가 없거나 LLM 호출이 실패하면, 정규식으로 에러 이름·기술 이름만 뽑는 규칙 기반으로 대신합니다.

사용 예
  from src.rag.query_rewrite import rewrite_query
  rq = rewrite_query("StateGraph compile 하면 에러나요", history=[("user", "LangGraph 쓰는 중이에요")])
  rq.search_query, rq.tech, rq.error_keywords

  python -m src.rag.query_rewrite "MCP 서버에 연결하면 -32601 오류가 나요"
"""

import re
from functools import lru_cache
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

Tech = Literal["langchain", "langgraph", "mcp", "unknown"]


class RewrittenQuery(BaseModel):
    standalone_question: str = Field(
        description="Korean question that is understandable without the chat history")
    search_query: str = Field(
        description="Concise ENGLISH search query for the official docs; keep exact error names, "
                    "error codes, class/function/package names")
    tech: Tech = Field(description="Main technology the question is about")
    error_keywords: list[str] = Field(
        default_factory=list,
        description="Exact error class names, error codes and API names found in the question")


PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You rewrite developer questions for searching the official documentation of "
     "LangChain, LangGraph and MCP (Model Context Protocol). The docs are in English.\n"
     "1. standalone_question: rewrite the latest user question in Korean so it is self-contained, "
     "resolving references to the chat history (e.g. '그거', '아까 그 에러').\n"
     "2. search_query: one concise English query (5-15 words). Keep exact identifiers such as "
     "error class names, error codes (-32601), function/class/package names. Drop greetings, "
     "long stack traces and file paths; keep only the final error line's essence.\n"
     "3. tech: langgraph if it mentions StateGraph, graph, node, checkpointer, interrupt, "
     "recursion limit; mcp for MCP servers/clients/tools/JSON-RPC; langchain for chains, agents, "
     "models, retrievers, middleware; otherwise unknown.\n"
     "4. error_keywords: exact error names / codes / API names, at most 5.\n"
     "Do not answer the question."),
    ("human", "Chat history:\n{history}\n\nLatest question:\n{question}"),
])


@lru_cache(maxsize=1)
def _chain():
    from src.const.models import get_llm
    return PROMPT | get_llm().with_structured_output(RewrittenQuery)


# ---------------------------------------------------------------------------
# 규칙 기반 대체 (LLM 실패 시)
# ---------------------------------------------------------------------------
ERROR_RE = re.compile(r"\b([A-Z][A-Za-z0-9]*(?:Error|Exception|Warning))\b")
CODE_RE = re.compile(r"(?<![\w.])-32\d{3}\b")                       # JSON-RPC 오류 코드
IDENT_RE = re.compile(r"\b[a-z_]+(?:\.[a-z_]+)+\b|\b[a-z]+_[a-z_]+\b")  # langgraph.prebuilt, recursion_limit
TECH_HINTS = {
    "langgraph": ["langgraph", "stategraph", "graph", "node", "checkpoint", "interrupt", "recursion", "그래프", "노드"],
    "mcp": ["mcp", "json-rpc", "jsonrpc", "fastmcp", "stdio", "-32", "model context protocol"],
    "langchain": ["langchain", "chain", "agent", "retriever", "embedding", "chatopenai", "middleware", "체인", "에이전트"],
}


def detect_tech(text: str) -> Tech:
    low = text.lower()
    scores = {t: sum(low.count(h) for h in hints) for t, hints in TECH_HINTS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "unknown"


def extract_error_keywords(text: str, limit: int = 5) -> list[str]:
    found = ERROR_RE.findall(text) + CODE_RE.findall(text) + IDENT_RE.findall(text)
    seen, out = set(), []
    for f in found:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out[:limit]


def _fallback(question: str) -> RewrittenQuery:
    keywords = extract_error_keywords(question)
    tech = detect_tech(question)
    # 영어 식별자만 모아 검색어로 (BM25 가 이걸로 정확히 찾음). 없으면 원래 질문.
    search = " ".join(([tech] if tech != "unknown" else []) + keywords) or question
    return RewrittenQuery(standalone_question=question, search_query=search,
                          tech=tech, error_keywords=keywords)


def _format_history(history) -> str:
    if not history:
        return "(none)"
    lines = []
    for item in history[-6:]:                        # 최근 6턴만
        if isinstance(item, (tuple, list)):
            role, content = item[0], item[1]
        else:                                        # LangChain 메시지 객체
            role, content = getattr(item, "type", "user"), getattr(item, "content", str(item))
        lines.append(f"{role}: {str(content)[:500]}")
    return "\n".join(lines)


def rewrite_query(question: str, history=None) -> RewrittenQuery:
    """history: [("user", "..."), ("assistant", "...")] 또는 LangChain 메시지 리스트."""
    question = question.strip()
    try:
        rq = _chain().invoke({"question": question, "history": _format_history(history)})
        # LLM 이 놓친 에러 이름은 규칙으로 보충
        for kw in extract_error_keywords(question):
            if kw not in rq.error_keywords:
                rq.error_keywords.append(kw)
        return rq
    except Exception as e:
        print(f"[query_rewrite] LLM 재작성 실패, 규칙 기반 사용: {e}")
        return _fallback(question)


def to_filters(rq: RewrittenQuery) -> dict | None:
    """retriever.search(filters=...) 에 넘길 필터. 기술을 모르면 None (전체 검색)."""
    return {"tech": rq.tech} if rq.tech != "unknown" else None


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "LangGraph에서 GraphRecursionError: Recursion limit of 25 reached 가 나요"
    print(rewrite_query(q).model_dump_json(indent=2))
