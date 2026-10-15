"""
1차(검색) 평가 지표 계산: Hit@k, Recall@k, MRR, nDCG@k.

기존 평가 파일(evaluation_*.md, test_*_connection.py 등)과 섞이지 않게 새 파일로 따로 둔다.
모델을 쓰지 않는 순수 계산이다. 정답은 "청크 ID 집합", 검색 결과는 "순위가 있는 청크 ID 목록"이다.

- 같은 청크가 여러 번 나와도 한 번만 센다 (처음 나온 순위만 쓴다).
- 관련 있음/없음 2단계(이진)로 계산한다. nDCG도 이진 관련도로 계산한다.
- 정답이 하나도 없는 질문은 계산하지 않는다 (호출하는 쪽이 분모에서 뺀다).
"""

import math

KS = (1, 3, 5)


def _unique(ranked_ids):
    return list(dict.fromkeys(ranked_ids))


def hit_at_k(ranked_ids, gold_ids, k):
    """상위 k개 안에 정답이 하나라도 있으면 1, 없으면 0."""
    return int(bool(set(_unique(ranked_ids)[:k]) & set(gold_ids)))


def recall_at_k(ranked_ids, gold_ids, k):
    """상위 k개 안에 든 정답 수 / 전체 정답 수."""
    gold = set(gold_ids)
    if not gold:
        raise ValueError("정답이 없는 질문은 Recall을 계산하지 않는다.")
    return len(set(_unique(ranked_ids)[:k]) & gold) / len(gold)


def reciprocal_rank(ranked_ids, gold_ids, k=max(KS)):
    """첫 정답의 순위의 역수 (1위면 1, 3위면 1/3). 상위 k개 안에 없으면 0."""
    gold = set(gold_ids)
    for rank, chunk_id in enumerate(_unique(ranked_ids)[:k], start=1):
        if chunk_id in gold:
            return 1 / rank
    return 0.0


def ndcg_at_k(ranked_ids, gold_ids, k):
    """이진 관련도 nDCG@k. 정답이 위에 있을수록 1에 가깝다."""
    gold = set(gold_ids)
    if not gold:
        raise ValueError("정답이 없는 질문은 nDCG를 계산하지 않는다.")
    dcg = sum(1 / math.log2(rank + 1) for rank, chunk_id in enumerate(_unique(ranked_ids)[:k], start=1) if chunk_id in gold)
    ideal = sum(1 / math.log2(rank + 1) for rank in range(1, min(len(gold), k) + 1))
    return dcg / ideal


def question_metrics(ranked_ids, gold_ids, ks=KS):
    """질문 하나의 모든 지표. {"hit@1": .., "recall@1": .., ..., "mrr": .., "ndcg@1": ..}"""
    result = {}
    for k in ks:
        result[f"hit@{k}"] = hit_at_k(ranked_ids, gold_ids, k)
        result[f"recall@{k}"] = recall_at_k(ranked_ids, gold_ids, k)
        result[f"ndcg@{k}"] = ndcg_at_k(ranked_ids, gold_ids, k)
    result["mrr"] = reciprocal_rank(ranked_ids, gold_ids, max(ks))
    return result


def average(per_question):
    """질문별 지표 목록의 평균. 평가 가능한 질문 수(n)도 함께 돌려준다. 비어 있으면 {"n": 0}."""
    if not per_question:
        return {"n": 0}
    keys = per_question[0].keys()
    summary = {key: sum(item[key] for item in per_question) / len(per_question) for key in keys}
    summary["n"] = len(per_question)
    return summary
