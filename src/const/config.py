import os
from pathlib import Path

from dotenv import load_dotenv


# ======================== File 경로 ========================

# 프로젝트 루트 절대경로
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# 실행 위치와 관계없이 프로젝트 루트의 .env를 읽습니다.
load_dotenv(PROJECT_ROOT / ".env")

# data 폴더 절대경로
DATA_PATH = PROJECT_ROOT / "data"

# data/raw 폴더 절대경로
RAW_PATH = DATA_PATH / "raw"

# data/raw/langchain 폴더 절대경로
RAW_LANGCHAIN_PATH = RAW_PATH / "langchain"

# data/raw/langgraph 폴더 절대경로
RAW_LANGGRAPH_PATH = RAW_PATH / "langgraph"

# data/raw/mcp 폴더 절대경로
RAW_MCP_PATH = RAW_PATH / "mcp"


# ======================== ENV ========================

# NVIDIA API KEY
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

# NVIDIA MODEL NAME
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL")

# NVIDIA EMBEDDING MODEL NAME
NVIDIA_EMBEDDING_MODEL = os.getenv("NVIDIA_EMBEDDING")

# NVIDIA RERANK API KEY
NVIDIA_RERANK_API_KEY = os.getenv("NVIDIA_RERANK_API_KEY")

# NVIDIA RERANK MODEL NAME
NVIDIA_RERANK_MODEL = os.getenv("NVIDIA_RERANK_MODEL")

# OPENAI API KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL") or "gpt-4.1-mini"

# 기존 팀 코드의 변수명도 유지합니다.
OPEN_API_KEY = os.getenv("OPEN_API_KEY") or OPENAI_API_KEY

# OPENAI EMBEDDING MODEL NAME
OPEN_EMBEDDING_MODEL = os.getenv("OPEN_EMBEDDING")

# PINECONE API KEY
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# PINECONE INDEX NAME
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
