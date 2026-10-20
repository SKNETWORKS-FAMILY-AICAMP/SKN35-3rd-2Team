"""재정렬 방식 선택(onnx/torch)과 ONNX 재정렬기의 점수 계산을 확인한다. 큰 모델은 불러오지 않는다."""

import numpy as np
import pytest

from src.const import models
from src.rag import rerank_onnx
from src.rag.rerank_onnx import DATA_FILE, MODEL_FILE, TOKENIZER_FILE, OnnxReranker, onnx_model_ready


def make_model_dir(tmp_path):
    for name in (MODEL_FILE, DATA_FILE, TOKENIZER_FILE):
        (tmp_path / name).write_bytes(b"x")
    return tmp_path


# ---------------------------------------------------------------- 파일 확인
def test_model_not_ready_when_files_missing(tmp_path):
    assert onnx_model_ready(tmp_path) is False
    (tmp_path / MODEL_FILE).write_bytes(b"x")
    assert onnx_model_ready(tmp_path) is False  # 일부만 있으면 준비 안 됨


def test_model_ready_when_all_files_exist(tmp_path):
    assert onnx_model_ready(make_model_dir(tmp_path)) is True


def test_missing_model_gives_clear_error(tmp_path):
    with pytest.raises(FileNotFoundError) as error:
        OnnxReranker(tmp_path)
    assert "export_reranker_onnx" in str(error.value) and "RERANK_BACKEND=torch" in str(error.value)


# ---------------------------------------------------------------- 방식 선택
def test_backend_forced_to_torch_even_if_onnx_exists(tmp_path, monkeypatch):
    monkeypatch.setattr(models, "RERANK_BACKEND", "torch")
    monkeypatch.setattr(models, "RERANK_ONNX_DIR", make_model_dir(tmp_path))
    assert models.rerank_backend() == "torch"


def test_backend_forced_to_onnx(monkeypatch, tmp_path):
    monkeypatch.setattr(models, "RERANK_BACKEND", "onnx")
    monkeypatch.setattr(models, "RERANK_ONNX_DIR", tmp_path)  # 파일이 없어도 onnx를 고른다 (만들 때 분명한 오류가 나게 한다)
    assert models.rerank_backend() == "onnx"


def test_auto_uses_onnx_when_model_files_exist(tmp_path, monkeypatch):
    monkeypatch.setattr(models, "RERANK_BACKEND", "auto")
    monkeypatch.setattr(models, "RERANK_ONNX_DIR", make_model_dir(tmp_path))
    assert models.rerank_backend() == "onnx"


def test_auto_falls_back_to_torch_when_model_files_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(models, "RERANK_BACKEND", "auto")
    monkeypatch.setattr(models, "RERANK_ONNX_DIR", tmp_path)
    assert models.rerank_backend() == "torch"


def test_auto_falls_back_to_torch_when_onnxruntime_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(models, "RERANK_BACKEND", "auto")
    monkeypatch.setattr(models, "RERANK_ONNX_DIR", make_model_dir(tmp_path))
    monkeypatch.setattr(rerank_onnx, "onnx_model_ready", lambda directory: False)
    assert models.rerank_backend() == "torch"


# ---------------------------------------------------------------- 점수 계산 (가짜 세션과 토크나이저)
class FakeEncoding:
    def __init__(self, length):
        self.ids = [1] * length
        self.attention_mask = [1] * length


class FakeTokenizer:
    def __init__(self):
        self.seen = []

    def encode_batch(self, pairs):
        self.seen.append(list(pairs))
        return [FakeEncoding(3) for _ in pairs]


class FakeSession:
    """logits를 질문마다 정해진 값으로 돌려준다."""

    def __init__(self, logits):
        self.logits = list(logits)
        self.batches = []

    def run(self, names, feed):
        size = feed["input_ids"].shape[0]
        self.batches.append(size)
        values = [self.logits.pop(0) for _ in range(size)]
        return [np.array(values, dtype=np.float32).reshape(size, 1)]


def make_reranker(logits, batch_size=8):
    reranker = OnnxReranker.__new__(OnnxReranker)
    reranker._np = np
    reranker.batch_size = batch_size
    reranker.session = FakeSession(logits)
    reranker.tokenizer = FakeTokenizer()
    return reranker


def test_scores_are_sigmoid_of_logits():
    scores = make_reranker([0.0, 2.0, -2.0]).predict([("q", "a"), ("q", "b"), ("q", "c")])
    assert np.allclose(scores, [0.5, 1 / (1 + np.exp(-2.0)), 1 / (1 + np.exp(2.0))])
    assert scores[1] > scores[0] > scores[2]  # 클수록 관련 있음


def test_pairs_are_batched_in_order():
    reranker = make_reranker(list(range(5)), batch_size=2)
    scores = reranker.predict([("q", str(i)) for i in range(5)])
    assert reranker.session.batches == [2, 2, 1]
    assert [text for batch in reranker.tokenizer.seen for _, text in batch] == ["0", "1", "2", "3", "4"]
    assert list(scores) == sorted(scores)  # 입력 순서대로 점수가 이어진다


def test_empty_pairs_return_empty_array_without_calling_model():
    reranker = make_reranker([])
    assert len(reranker.predict([])) == 0 and reranker.session.batches == []


def test_works_with_rerank_function(monkeypatch):
    """rerank()가 쓰는 방식(점수 배열을 문서와 함께 정렬)과 맞는지 확인한다."""
    import importlib
    import sys

    from langchain_core.documents import Document

    # rerank 모듈은 불러올 때 재정렬 모델을 만든다. 큰 모델을 불러오지 않게 가짜로 바꿔 끼운 상태에서 새로 불러온다.
    monkeypatch.setattr(models, "create_rerank", lambda: make_reranker([-3.0, 4.0, 0.5]))
    previous = sys.modules.pop("src.rag.rerank", None)
    try:
        rerank_module = importlib.import_module("src.rag.rerank")
        docs = [Document(page_content=text) for text in ("낮음", "높음", "중간")]
        ranked = rerank_module.rerank(docs, "질문", top_n=2)
    finally:
        sys.modules.pop("src.rag.rerank", None)
        if previous is not None:
            sys.modules["src.rag.rerank"] = previous
    assert [d.page_content for d in ranked] == ["높음", "중간"]
    assert ranked[0].metadata["rerank_score"] > ranked[1].metadata["rerank_score"]
