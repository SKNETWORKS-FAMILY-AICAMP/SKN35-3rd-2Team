"""검색기를 불러와도 쓰지 않는 무거운 라이브러리(torch, transformers)를 끌어오지 않는지 확인한다."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(code):
    result = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    assert result.returncode == 0, result.stderr[-500:]
    return result.stdout.strip().splitlines()[-1]


def test_retriever_does_not_import_torch_or_transformers():
    code = "import sys, src.rag.retriever; print(json.dumps({'torch': 'torch' in sys.modules, 'transformers': 'transformers' in sys.modules}))"
    loaded = json.loads(run("import json;" + code))
    assert loaded == {"torch": False, "transformers": False}


def test_bm25_encoder_still_works_and_splade_is_blocked():
    code = (
        "import json, src.rag.retriever as r;"
        "from src.const.config import BM25_PATH;"
        "enc = r.BM25Encoder().load(str(BM25_PATH));"
        "vector = enc.encode_queries('GraphRecursionError recursion limit');"
        "from pinecone_text.sparse import SpladeEncoder;"
        "blocked = False\n"
        "try:\n"
        "    SpladeEncoder()\n"
        "except ImportError:\n"
        "    blocked = True\n"
        "print(json.dumps({'indices': len(vector['indices']), 'blocked': blocked}))"
    )
    result = json.loads(run(code))
    assert result["indices"] > 0 and result["blocked"] is True
