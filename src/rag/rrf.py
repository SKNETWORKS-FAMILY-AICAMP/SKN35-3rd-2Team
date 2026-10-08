"""
검색 결과 RRF(Reciprocal Rank Fusion) 통합

여러 검색 결과 목록(벡터 검색, BM25, Multi-Query 의 질문별 결과 …)을 하나로 합칩니다.
점수 크기가 서로 다른 검색기도 "순위" 만 보고 합치므로 정규화가 필요 없습니다.

  RRF 점수(문서) = Σ  weight_i / (k + 순위_i)      (순위는 1부터, k 기본 60)

여러 목록에서 공통으로 위에 나온 문서일수록 점수가 높아집니다.

사용 예
  from src.rag.rrf import reciprocal_rank_fusion
  fused = reciprocal_rank_fusion([vector_docs, bm25_docs], weights=[0.6, 0.4], top_n=10)
  # → [(Document, rrf_score), ...]
"""

from langchain_core.documents import Document


def _doc_key(doc: Document) -> str:
    return doc.metadata.get("chunk_id") or doc.page_content[:200]


def reciprocal_rank_fusion(result_lists: list[list[Document]], k: int = 60,
                           weights: list[float] | None = None,
                           top_n: int | None = None) -> list[tuple[Document, float]]:
    if weights is None:
        weights = [1.0] * len(result_lists)
    if len(weights) != len(result_lists):
        raise ValueError("weights 개수와 result_lists 개수가 달라요")

    scores: dict[str, float] = {}
    docs: dict[str, Document] = {}
    for results, w in zip(result_lists, weights):
        for rank, doc in enumerate(results, start=1):
            key = _doc_key(doc)
            scores[key] = scores.get(key, 0.0) + w / (k + rank)
            docs.setdefault(key, doc)

    fused = sorted(((docs[key], s) for key, s in scores.items()), key=lambda x: x[1], reverse=True)
    return fused[:top_n] if top_n else fused
