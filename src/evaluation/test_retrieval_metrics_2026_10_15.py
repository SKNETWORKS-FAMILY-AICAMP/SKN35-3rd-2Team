import math

import pytest

from src.evaluation.retrieval_metrics_2026_10_15 import (
    average,
    hit_at_k,
    ndcg_at_k,
    question_metrics,
    recall_at_k,
    reciprocal_rank,
)

RANKED = ["A", "B", "C", "D", "E"]


def test_hit_at_k_example_from_the_plan():
    gold = {"C", "E"}
    assert [hit_at_k(RANKED, gold, k) for k in (1, 3, 5)] == [0, 1, 1]


def test_recall_at_k_example_from_the_plan():
    # 정답 3개 중 상위 5개에 2개 -> Recall@5 = 2/3
    assert recall_at_k(RANKED, {"C", "E", "Z"}, 5) == pytest.approx(2 / 3)
    assert recall_at_k(RANKED, {"C", "E", "Z"}, 1) == 0
    assert recall_at_k(RANKED, {"C", "E", "Z"}, 3) == pytest.approx(1 / 3)


def test_duplicates_are_counted_once():
    assert recall_at_k(["A", "A", "A", "C"], {"A", "C"}, 3) == 1.0  # 중복 A는 한 번, C는 2위로 밀린다
    assert hit_at_k(["A", "A", "B"], {"B"}, 2) == 1


def test_reciprocal_rank():
    assert reciprocal_rank(RANKED, {"A"}) == 1
    assert reciprocal_rank(RANKED, {"C"}) == pytest.approx(1 / 3)
    assert reciprocal_rank(RANKED, {"Z"}) == 0
    assert reciprocal_rank(RANKED, {"E", "C"}) == pytest.approx(1 / 3)  # 첫 정답 기준


def test_ndcg_perfect_and_worst_and_between():
    assert ndcg_at_k(["A", "B"], {"A", "B"}, 5) == pytest.approx(1.0)
    assert ndcg_at_k(RANKED, {"Z"}, 5) == 0
    one_at_rank3 = ndcg_at_k(RANKED, {"C"}, 5)
    assert one_at_rank3 == pytest.approx((1 / math.log2(4)) / 1.0)
    assert 0 < one_at_rank3 < ndcg_at_k(["C"], {"C"}, 5)


def test_ndcg_ideal_uses_min_of_gold_and_k():
    # 정답이 5개여도 k=1이면 이상적인 DCG는 1개분이다
    assert ndcg_at_k(["A"], {"A", "B", "C", "D", "E"}, 1) == pytest.approx(1.0)


def test_empty_gold_is_rejected():
    with pytest.raises(ValueError):
        recall_at_k(RANKED, set(), 5)
    with pytest.raises(ValueError):
        ndcg_at_k(RANKED, set(), 5)


def test_fewer_results_than_k_are_evaluated_as_they_are():
    assert hit_at_k(["A"], {"A"}, 5) == 1
    assert recall_at_k(["A"], {"A", "B"}, 5) == 0.5


def test_question_metrics_keys_and_average():
    metrics = question_metrics(RANKED, {"C"})
    assert set(metrics) == {"hit@1", "recall@1", "ndcg@1", "hit@3", "recall@3", "ndcg@3", "hit@5", "recall@5", "ndcg@5", "mrr"}
    other = question_metrics(RANKED, {"A"})
    summary = average([metrics, other])
    assert summary["n"] == 2
    assert summary["hit@1"] == 0.5 and summary["mrr"] == pytest.approx((1 / 3 + 1) / 2)
    assert average([]) == {"n": 0}
