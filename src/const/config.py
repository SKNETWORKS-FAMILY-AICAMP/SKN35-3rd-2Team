"""
환경변수 및 프로젝트 설정

.env (프로젝트 루트, Git 에 올리지 않기) 예시
  OPENAI_API_KEY=sk-...
  PINECONE_API_KEY=pcsk_...
  PINECONE_INDEX_NAME=skn35-3rd-2team-rag
  PINECONE_NAMESPACE=docs
  EMBEDDING_PROVIDER=openai          # openai | hf (BAAI/bge-m3)
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# 프로젝트 루트 = src/ 의 한 단계 위 (README.md, data/, main.py 가 있는 곳)
# → 어느 폴더에서 실행해도 경로가 틀어지지 않음
PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2]))
load_dotenv(PROJECT_ROOT / ".env")

# ---------------------------------------------------------------------------
# 데이터 경로
# ---------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"                     # raw/{langchain,langgraph,mcp}  원본 문서
PROCESSED_DIR = DATA_DIR / "processed"         # processed/{langchain,langgraph,mcp}  전처리된 문서, chunks.jsonl
PDF_DIR = DATA_DIR / "pdf"                     # 입력 PDF 폴더 (md_to_pdf.py 출력)
TECHS = ["langchain", "langgraph", "mcp"]
# 입력 PDF: data/pdf/langchain.pdf, data/pdf/langgraph.pdf, data/pdf/mcp.pdf
PDF_FILES = {tech: PDF_DIR / f"{tech}.pdf" for tech in TECHS}
CHUNKS_PATH = PROCESSED_DIR / "chunks.jsonl"   # 청크 사본 (BM25 키워드 검색, get_chunk 용)

# ---------------------------------------------------------------------------
# Pinecone
# ---------------------------------------------------------------------------
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "skn35-3rd-2team-rag")    # 소문자·숫자·하이픈만
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "docs")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")            # 무료(Starter) 플랜은 aws/us-east-1

# ---------------------------------------------------------------------------
# 청크
# ---------------------------------------------------------------------------
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))        # 글자 수 (영어 1,000자 ≈ 250 토큰)
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
