"""
벡터 DB 만들기: data/processed/<tech>/*.pdf → 청크 → data/processed/chunks.jsonl + Pinecone 업로드

실행 (프로젝트 루트에서)
  python -m src.vectorstore.build
  python -m src.vectorstore.build --tech mcp        # 일부만 (테스트용, 이때 Pinecone namespace 는 mcp 만 남음)
"""

import argparse

from src.rag.loader import load_documents
from src.rag.splitter import save_chunks, split_documents
from src.vectorstore.pinecone_store import build_vectorstore


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tech", nargs="+", help="langchain / langgraph / mcp 중 일부만")
    args = ap.parse_args()

    docs = load_documents(techs=args.tech)
    chunks = split_documents(docs)
    save_chunks(chunks)
    build_vectorstore(chunks)
    print(f"[완료] 문서 {len(docs)}개, 청크 {len(chunks)}개 → Pinecone 업로드")


if __name__ == "__main__":
    main()
