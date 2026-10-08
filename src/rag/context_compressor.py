"""
검색 결과 Context 압축

검색된 청크를 그대로 LLM 에 넣으면 질문과 상관없는 문장이 많아 토큰이 낭비되고 답변이 흐려집니다.
여기서는 청크마다 "질문과 관련된 부분만" 남기고, 관련 없는 청크는 버립니다.

방법 2가지
  method="llm"        LLM 이 청크에서 관련 문장만 그대로 뽑아냄 (정확, API 비용 있음)
  method="embedding"  청크를 문장으로 나눠 질문과 임베딩 유사도가 높은 문장만 남김 (빠름, 저렴)
공통
  max_chars  압축 후 전체 글자 수 상한 (넘으면 아래 순위 청크부터 자름)

사용 예
  from src.rag.context_compressor import compress_documents, format_context
  small = compress_documents(question, docs, method="llm")
  context = format_context(small)      # LLM 프롬프트에 넣을 문자열 ([1] 제목 (출처) ...)
"""

import re
from functools import lru_cache

import numpy as np
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate


NO_OUTPUT = "NO_RELEVANT_CONTENT"

EXTRACT_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Extract ONLY the parts of the document that help answer the question, copied verbatim "
     "(keep code, error messages and commands exactly). Do not summarize or add anything. "
     f"If nothing is relevant, reply exactly {NO_OUTPUT}."),
    ("human", "Question: {question}\n\nDocument:\n{document}"),
])


@lru_cache(maxsize=1)
def _extract_chain():
    from langchain_core.output_parsers import StrOutputParser
    from src.const.models import get_llm
    return EXTRACT_PROMPT | get_llm() | StrOutputParser()


def _compress_llm(question: str, docs: list[Document]) -> list[Document]:
    inputs = [{"question": question, "document": d.page_content} for d in docs]
    outputs = _extract_chain().batch(inputs, config={"max_concurrency": 5})   # 여러 청크 동시 처리
    out = []
    for doc, text in zip(docs, outputs):
        text = text.strip()
        if not text or NO_OUTPUT in text:
            continue
        out.append(Document(page_content=text, metadata={**doc.metadata, "compressed": True}))
    return out


def _split_sentences(text: str) -> list[str]:
    # 빈 줄·줄바꿈·문장 끝(. ? !) 기준. 코드 줄은 줄 단위로 남음
    parts = re.split(r"\n+|(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if len(p.strip()) > 2]


def _compress_embedding(question: str, docs: list[Document], threshold: float,
                        keep_neighbors: int = 1) -> list[Document]:
    from src.const.models import get_embeddings
    emb = get_embeddings()
    q = np.array(emb.embed_query(question))
    out = []
    for doc in docs:
        sents = _split_sentences(doc.page_content)
        if not sents:
            continue
        vecs = np.array(emb.embed_documents(sents))
        sims = vecs @ q / (np.linalg.norm(vecs, axis=1) * np.linalg.norm(q) + 1e-10)
        keep = set()
        for i in np.where(sims >= threshold)[0]:
            # 앞뒤 문장도 조금 남겨서 문맥이 끊기지 않게
            keep.update(range(max(0, i - keep_neighbors), min(len(sents), i + keep_neighbors + 1)))
        if keep:
            text = "\n".join(sents[i] for i in sorted(keep))
            out.append(Document(page_content=text, metadata={**doc.metadata, "compressed": True}))
    return out


def compress_documents(question: str, docs: list[Document], method: str = "llm",
                       threshold: float = 0.45, max_chars: int = 6000) -> list[Document]:
    if not docs:
        return []
    try:
        if method == "llm":
            compressed = _compress_llm(question, docs)
        elif method == "embedding":
            compressed = _compress_embedding(question, docs, threshold)
        else:
            raise ValueError("method 는 'llm' 또는 'embedding'")
    except Exception as e:                         # API 오류 시 원문 그대로 (서비스가 멈추지 않게)
        print(f"[context_compressor] 압축 실패, 원문 사용: {e}")
        compressed = list(docs)

    # 전체 길이 상한: 순위가 높은 청크부터 채움
    result, total = [], 0
    for d in compressed:
        if total + len(d.page_content) > max_chars:
            remain = max_chars - total
            if remain > 200:
                result.append(Document(page_content=d.page_content[:remain], metadata=d.metadata))
            break
        result.append(d)
        total += len(d.page_content)
    return result


def format_context(docs: list[Document]) -> str:
    """LLM 프롬프트용 문자열. 답변에서 [1], [2] 로 출처를 달 수 있게 번호를 붙임."""
    blocks = []
    for i, d in enumerate(docs, start=1):
        m = d.metadata
        src = m.get("source_url") or f"{m.get('doc_path', '')} ({m.get('source', '')} p.{m.get('page_start', '?')})"
        blocks.append(f"[{i}] {m.get('title', '')} | {m.get('tech', '')} | {src}\n{d.page_content}")
    return "\n\n---\n\n".join(blocks)
