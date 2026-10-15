"""
평가 스크립트가 청크를 읽는 공통 통로: 벡터 DB(Pinecone 인덱스)에서 직접 읽는다.

앱이 실제로 검색하는 것과 같은 청크(ID, 글)이므로, 평가의 정답 근거 ID가 검색 결과의 ID와 항상 같은 기준이 된다.
앱 코드는 고치지 않고, 읽기만 한다.
"""

from pinecone import Pinecone

from src.const import config as app_config

BATCH = 100


def get_index():
    return Pinecone(api_key=app_config.PINECONE_API_KEY).Index(app_config.PINECONE_INDEX_NAME)


def normalize(chunk_id, metadata):
    """인덱스 메타데이터를 평가 스크립트가 쓰는 모양으로 맞춘다."""
    metadata = metadata or {}
    return {
        "chunk_id": chunk_id,
        "tech": metadata.get("technology"),
        "title": metadata.get("title") or "",
        "parent_id": metadata.get("parent_id"),
        "chunk_index": int(float(metadata.get("chunk_index") or 0)),
        "text": metadata.get("text") or "",
    }


def fetch_chunks(index, chunk_ids):
    """청크 ID 목록의 청크를 {ID: 청크}로 읽는다. 인덱스에 없는 ID는 빠진다."""
    ids = list(dict.fromkeys(chunk_ids))
    found = {}
    for start in range(0, len(ids), BATCH):
        for chunk_id, vector in index.fetch(ids=ids[start : start + BATCH]).vectors.items():
            found[chunk_id] = normalize(chunk_id, vector.metadata)
    return found


def all_chunks(index):
    """인덱스의 모든 청크 [청크, ...] (문서와 청크 번호 순서)."""
    ids = [chunk_id for page in index.list() for chunk_id in page]
    chunks = list(fetch_chunks(index, ids).values())
    return sorted(chunks, key=lambda chunk: (chunk["parent_id"] or "", chunk["chunk_index"]))
