import re

def edit(path, pairs):
    s = open(path, encoding="utf-8").read()
    for old, new in pairs:
        assert old in s, (path, old[:70])
        s = s.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(s)

E = "src/evaluation/"

# 1) 질문 생성
edit(E + "retrieval_make_dataset_2026_10_15.py", [
    ("- 정답 있는 질문: 청크를 보고 gpt-4o-mini가 질문을 만든다. 그 청크가 곧 정답(원본 청크)이다.",
     "- 정답 있는 질문: 벡터 DB(Pinecone 인덱스)의 청크를 보고 gpt-4o-mini가 질문을 만든다. 그 청크가 곧 정답(원본 청크)이다."),
    ("- 모델 이름은 환경변수 EVAL_MODEL (없으면 gpt-4o-mini). 같은 시드면 같은 청크를 뽑는다.",
     "- 모델 이름은 환경변수 EVAL_MODEL (없으면 gpt-4o-mini). 같은 시드와 같은 인덱스면 같은 청크를 뽑는다."),
    ('CHUNKS_PATH = HERE.parents[1] / "data" / "processed" / "chunks.jsonl"\n', ""),
    ('''def load_chunks():
    rows = [json.loads(line) for line in CHUNKS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    return rows
''', '''def load_chunks():
    """벡터 DB(인덱스)의 모든 청크. 질문의 정답 청크 ID가 앱의 검색 결과 ID와 같은 기준이 된다."""
    return all_chunks(get_index())
'''),
    ("from src.const.config import OPEN_API_KEY\n", "from src.const.config import OPEN_API_KEY\nfrom src.evaluation.index_chunks_2026_10_15 import all_chunks, get_index\n"),
])

# 2) 체크리스트
edit(E + "answer_rubric_2026_10_15.py", [
    ('CHUNKS_PATH = HERE.parents[1] / "data" / "processed" / "chunks.jsonl"\n', ""),
    ("    chunks = {row[\"chunk_id\"]: row for row in read_jsonl(CHUNKS_PATH)}\n",
     "    questions = read_jsonl(QUESTIONS_PATH)\n    chunks = fetch_chunks(get_index(), [cid for q in questions if q[\"type\"] == \"answerable\" for cid in q[\"source_chunk_ids\"]])\n"),
    ("    for question in read_jsonl(QUESTIONS_PATH):\n", "    for question in questions:\n"),
    ('''            context = "\n\n".join(f"[{chunks[cid]['title']}]\n{chunks[cid]['text']}" for cid in question["source_chunk_ids"])''',
     '''            context = "\n\n".join(f"[{chunks[cid]['title']}]\n{chunks[cid]['text']}" for cid in question["source_chunk_ids"] if cid in chunks)
            if not context:  # 인덱스에서 원본 청크를 찾지 못한 질문은 근거 글이 없어 체크리스트를 만들지 않는다
                print(question["id"], "원본 청크가 없어 건너뜀", flush=True)
                continue'''),
    ("from src.const.config import OPEN_API_KEY\n", "from src.const.config import OPEN_API_KEY\nfrom src.evaluation.index_chunks_2026_10_15 import fetch_chunks, get_index\n"),
])

# 4) 검수 파일
edit(E + "review_sheets_2026_10_15.py", [
    ('CHUNKS_PATH = HERE.parents[1] / "data" / "processed" / "chunks.jsonl"\n', ""),
    ("    chunks = {row[\"chunk_id\"]: row for row in read_jsonl(CHUNKS_PATH)}\n",
     "    ids = [cid for q in read_jsonl(HERE / \"retrieval_questions_2026-10-15.jsonl\") for cid in q[\"source_chunk_ids\"]]\n    chunks = fetch_chunks(get_index(), ids)\n"),
    ("import json\nimport random\nfrom pathlib import Path\n", "import json\nimport random\nfrom pathlib import Path\n\nfrom src.evaluation.index_chunks_2026_10_15 import fetch_chunks, get_index\n"),
    ("""            lines += [f"**근거 문서** ({chunk_id}): {clip(chunks[chunk_id]['text'])}", ""]""",
     """            lines += [f"**근거 문서** ({chunk_id}): {clip(chunks.get(chunk_id, {}).get('text'))}", ""]"""),
])
print("ok")
