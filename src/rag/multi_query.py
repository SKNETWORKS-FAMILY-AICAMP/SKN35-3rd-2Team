"""
Multi-Query 생성

질문 하나를 여러 표현으로 바꿔 각각 검색한 뒤 RRF 로 합치면, 표현 차이 때문에 놓치는 문서가 줄어듭니다.
이 프로젝트는 "한국어 질문 ↔ 영어 문서" 이므로 영어 번역 질문을 꼭 포함시킵니다.

  "LangGraph에서 재귀 한도 오류가 나요"
   → ["LangGraph에서 재귀 한도 오류가 나요",                (원래 질문)
      "GraphRecursionError recursion limit LangGraph",      (영어 키워드)
      "How to increase recursion_limit in LangGraph",        (영어 해결 방법)
      "LangGraph graph loops forever until recursion limit"] (다른 관점)

사용 예
  from src.rag.multi_query import generate_queries
  queries = generate_queries("MCP 서버 연결이 안 돼요", n=3)
"""

from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You help search English technical documentation for LangChain, LangGraph and MCP.\n"
     "Rewrite the user's question into {n} different search queries in ENGLISH.\n"
     "- Keep exact error names, codes, class/function names and package names unchanged.\n"
     "- Make one query keyword-style (error name + library), one a 'how to fix' question, "
     "and the others from different angles (cause, related API, version change).\n"
     "- Do not answer the question."),
    ("human", "{question}"),
])


class Queries(BaseModel):
    queries: list[str] = Field(description="English search queries")


@lru_cache(maxsize=1)
def _chain():
    from src.const.models import create_openai_model
    return PROMPT | create_openai_model().with_structured_output(Queries)


def generate_queries(question: str, n: int = 3, include_original: bool = True) -> list[str]:
    try:
        result = _chain().invoke({"question": question, "n": n})
        generated = [q.strip() for q in result.queries if q.strip()][:n]
    except Exception as e:                       # API 키 없음·네트워크 오류 → 원래 질문만으로 계속
        print(f"[multi_query] 생성 실패, 원래 질문만 사용: {e}")
        generated = []
    queries = ([question] if include_original else []) + generated
    seen, unique = set(), []
    for q in queries:
        if q.lower() not in seen:
            seen.add(q.lower())
            unique.append(q)
    return unique
