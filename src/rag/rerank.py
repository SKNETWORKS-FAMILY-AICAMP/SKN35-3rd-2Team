"""
검색 결과 재정렬 (Cross-Encoder Rerank)

1차 검색(벡터+BM25)은 빠르지만 대충 고릅니다. Cross-Encoder 는 (질문, 청크) 쌍을 함께 읽고
관련도를 다시 매기므로 더 정확합니다. 그래서 1차로 20개 정도 뽑고 → 재정렬로 상위 5개를 고릅니다.

모델: src/const/models.py 의 RERANK_MODEL (기본 BAAI/bge-reranker-v2-m3) (다국어, 한국어 질문 ↔ 영어 문서 OK, 로컬 무료)
  pip install sentence-transformers      (첫 실행 때 모델 약 2GB 다운로드, GPU 없으면 다소 느림)

사용 예
  from src.rag.rerank import rerank
  top = rerank("MCP 서버에서 -32601 오류", docs, top_n=5)   # → [(Document, score), ...]
"""

from langchain_core.documents import Document



def rerank(query: str, docs: list[Document], top_n: int = 5, batch_size: int = 16) -> list[tuple[Document, float]]:
    if not docs:
        return []
    try:
        from src.const.models import get_reranker
        model = get_reranker()
    except ImportError:
        print("[rerank] sentence-transformers 가 없어 재정렬을 건너뜁니다 (pip install sentence-transformers)")
        return [(d, 0.0) for d in docs[:top_n]]

    scores = model.predict([(query, d.page_content) for d in docs], batch_size=batch_size)
    ranked = sorted(zip(docs, (float(s) for s in scores)), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]
