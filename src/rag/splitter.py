"""
문서 Chunk 분할: Document(문서 1개) → Document(청크 여러 개)

- RecursiveCharacterTextSplitter 로 문단 → 줄 → 문장 → 단어 순서로 자연스럽게 자름
- 청크마다 "문서 제목" 을 맨 앞에 붙임 → 짧은 청크도 무슨 문서인지 알 수 있어 검색 정확도↑
- 너무 짧은 청크(기본 50자 미만)와 내용이 똑같은 중복 청크는 버림
- 청크 메타데이터: 원본 문서 메타데이터 + chunk_id, chunk_index
    chunk_id 예: langchain-errors-invalid_prompt-002   (팀 공유 스키마의 chunk_id)

사용 예
  from src.rag.loader import load_documents
  from src.rag.splitter import split_documents, save_chunks
  chunks = split_documents(load_documents())
  save_chunks(chunks)          # data/processed/chunks.jsonl
"""

import hashlib
import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.const.config import CHUNK_OVERLAP, CHUNK_SIZE, CHUNKS_PATH

MIN_CHUNK_CHARS = 50


def split_documents(docs: list[Document], chunk_size: int = CHUNK_SIZE,
                    chunk_overlap: int = CHUNK_OVERLAP) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", "。", " ", ""],
    )
    chunks: list[Document] = []
    seen_hashes: set[str] = set()

    for doc in docs:
        title = doc.metadata.get("title", "")
        parts = splitter.split_text(doc.page_content)
        index = 0
        for part in parts:
            if len(part.strip()) < MIN_CHUNK_CHARS:
                continue
            digest = hashlib.sha256((doc.metadata.get("tech", "") + part.strip()).encode("utf-8")).hexdigest()
            if digest in seen_hashes:                 # 같은 기술 문서 안에 똑같은 문단 → 한 번만
                continue
            seen_hashes.add(digest)

            text = part if part.startswith(title) else f"{title}\n{part}"
            meta = dict(doc.metadata)
            meta["chunk_index"] = index
            meta["chunk_id"] = f"{meta.get('parent_id', 'doc')}-{index:03d}"
            chunks.append(Document(page_content=text, metadata=meta))
            index += 1

    print(f"[splitter] 문서 {len(docs)}개 → 청크 {len(chunks)}개 "
          f"(chunk_size={chunk_size}, overlap={chunk_overlap})")
    return chunks


def save_chunks(chunks: list[Document], path: Path = CHUNKS_PATH) -> Path:
    """청크를 jsonl 로 저장 (한 줄 = 청크 1개). BM25 검색, get_chunk(), 평가(C 파트)에서 사용."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps({"text": c.page_content, **c.metadata}, ensure_ascii=False) + "\n")
    print(f"[splitter] 저장: {path}")
    return path


def load_chunks(path: Path = CHUNKS_PATH) -> list[Document]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} 가 없습니다. 먼저 python -m src.vectorstore.build 를 실행하세요.")
    chunks = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                text = row.pop("text")
                chunks.append(Document(page_content=text, metadata=row))
    return chunks


if __name__ == "__main__":
    from src.rag.loader import load_documents
    cs = split_documents(load_documents())
    save_chunks(cs)                      # data/processed/chunks.jsonl (Pinecone 업로드는 python -m src.vectorstore.build)
    if cs:
        print("예시:", cs[0].metadata["chunk_id"], "|", cs[0].page_content[:200])
