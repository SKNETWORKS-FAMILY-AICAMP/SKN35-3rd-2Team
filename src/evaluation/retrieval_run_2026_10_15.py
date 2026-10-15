"""
1차(검색) 평가에서 질문 하나의 "검색 순위"를 받아 온다.

RAG 하위 그래프를 그대로 돌리되, 평가에는 filter와 압축을 거치기 전의 것이 필요하므로
마지막 rerank 직후의 문서 목록(상위 5개)을 가져온다 (재시도가 있었다면 마지막 재정렬 결과).
앱 코드는 고치지 않고 읽기만 한다.
"""

from src.agent.rag_agent import rag_agent


def ranked_candidates(question: str) -> list[dict]:
    """질문 하나를 RAG에 넣어 마지막 rerank 직후의 [{chunk_id, rerank_score, title}, ...]를 순위순으로 돌려준다."""
    graph = rag_agent()
    last = None
    for event in graph.stream(
        {"messages": [{"role": "user", "content": question}], "original_question": question, "retry_count": 0},
        stream_mode="updates",
    ):
        for node_name, update in event.items():
            if node_name == "rerank" and isinstance(update, dict):
                last = update.get("documents")
    if last is None:
        raise RuntimeError("rerank 결과를 받지 못했습니다.")
    return [
        {
            "chunk_id": document.metadata.get("chunk_id"),
            "rerank_score": document.metadata.get("rerank_score"),
            "title": document.metadata.get("title"),
            "text": document.page_content,
        }
        for document in last
    ]
