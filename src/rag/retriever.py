import time

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pinecone import Pinecone, ServerlessSpec

from src.const.config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from src.rag.loader import load_documents
from src.rag.splitter import split_documents

DENSE_MODEL = "llama-text-embed-v2"
SPARSE_MODEL = "pinecone-sparse-english-v0"

DENSE_DIMENSION = 1024

CLOUD = "aws"
REGION = "us-east-1"

TOP_K = 5
ALPHA = 0.7


def get_pinecone_client():
    return Pinecone(api_key=PINECONE_API_KEY)


def create_pinecone_index():
    pc = get_pinecone_client()

    existing_indexes = [index.name for index in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Pinecone Index 생성 중: {PINECONE_INDEX_NAME}")

        pc.create_index(
            name=PINECONE_INDEX_NAME,
            vector_type="dense",
            dimension=DENSE_DIMENSION,
            metric="dotproduct",
            spec=ServerlessSpec(
                cloud=CLOUD,
                region=REGION,
            ),
        )

        print(f"Pinecone Index 생성 완료: {PINECONE_INDEX_NAME}")

    else:
        print(f"Pinecone Index 이미 존재: {PINECONE_INDEX_NAME}")

    return pc.Index(PINECONE_INDEX_NAME)


def create_dense_embeddings(
    pc,
    texts: list[str],
    batch_size: int = 20,
    sleep_seconds: float = 2.0,
):
    all_embeddings = []

    total = len(texts)

    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        batch = texts[start:end]

        print(f"Dense Embedding: {start + 1}~{end}/{total}")

        result = pc.inference.embed(
            model=DENSE_MODEL,
            inputs=batch,
            parameters={
                "input_type": "passage",
                "truncate": "END",
            },
        )

        all_embeddings.extend(result.data)

        time.sleep(sleep_seconds)

    return all_embeddings


def create_sparse_embeddings(
    pc,
    texts: list[str],
    batch_size: int = 20,
    sleep_seconds: float = 2.0,
):
    all_embeddings = []

    total = len(texts)

    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        batch = texts[start:end]

        print(f"Sparse Embedding: {start + 1}~{end}/{total}")

        result = pc.inference.embed(
            model=SPARSE_MODEL,
            inputs=batch,
            parameters={
                "input_type": "passage",
            },
        )

        all_embeddings.extend(result.data)

        time.sleep(sleep_seconds)

    return all_embeddings


def create_vectors(
    pc,
    documents: list[Document],
    dense_alpha: float = 0.7,
):
    texts = [doc.page_content for doc in documents]

    dense_embeddings = create_dense_embeddings(
        pc,
        texts,
        batch_size=20,
        sleep_seconds=2.0,
    )

    sparse_embeddings = create_sparse_embeddings(
        pc,
        texts,
        batch_size=20,
        sleep_seconds=2.0,
    )

    vectors = []

    for i, document in enumerate(documents):
        dense_embedding = dense_embeddings[i]
        sparse_embedding = sparse_embeddings[i]

        vector = {
            "id": f"doc-{i}",
            "values": [value * dense_alpha for value in dense_embedding.values],
            "sparse_values": {
                "indices": sparse_embedding.sparse_indices,
                "values": [
                    value * (1 - dense_alpha)
                    for value in sparse_embedding.sparse_values
                ],
            },
            "metadata": document.metadata
            | {
                "text": document.page_content,
            },
        }

        vectors.append(vector)

    return vectors


def upsert_documents(
    index,
    vectors,
    batch_size: int = 50,
):
    total = len(vectors)

    print(f"Pinecone Upsert 시작: {total}개")

    for start in range(
        0,
        total,
        batch_size,
    ):
        end = start + batch_size

        batch = vectors[start:end]

        index.upsert(vectors=batch)

        print(f"Upsert 완료: {min(end, total)}/{total}")

    print("Pinecone Upsert 완료")


def create_query_embeddings(
    pc,
    query: str,
):
    dense_result = pc.inference.embed(
        model=DENSE_MODEL,
        inputs=[query],
        parameters={
            "input_type": "query",
            "truncate": "END",
        },
    )

    sparse_result = pc.inference.embed(
        model=SPARSE_MODEL,
        inputs=[query],
        parameters={
            "input_type": "query",
        },
    )

    dense = dense_result.data[0]
    sparse = sparse_result.data[0]

    return dense, sparse


def hybrid_search(
    query: str,
    top_k: int = TOP_K,
):
    pc = get_pinecone_client()

    index = pc.Index(PINECONE_INDEX_NAME)
    print(index.describe_index_stats())

    dense, sparse = create_query_embeddings(
        pc,
        query,
    )

    # Dense / Sparse 가중치 적용
    dense_values = [value * ALPHA for value in dense.values]

    sparse_values = [value * (1 - ALPHA) for value in sparse.sparse_values]

    results = index.query(
        vector=dense_values,
        sparse_vector={
            "indices": sparse.sparse_indices,
            "values": sparse_values,
        },
        top_k=top_k,
        include_metadata=True,
    )

    return results


def convert_to_documents(results):
    documents = []

    for match in results.matches:
        metadata = match.metadata or {}

        text = metadata.get(
            "text",
            "",
        )

        document_metadata = {
            key: value for key, value in metadata.items() if key != "text"
        }

        document_metadata["score"] = match.score
        document_metadata["id"] = match.id

        document = Document(
            page_content=text,
            metadata=document_metadata,
        )

        documents.append(document)

    return documents


class PineconeHybridRetriever(BaseRetriever):
    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager=None,
    ) -> list[Document]:

        results = hybrid_search(
            query=query,
            top_k=TOP_K,
        )

        documents = convert_to_documents(results)

        return documents


def build_pinecone():
    print("Pinecone Hybrid Index 구축")

    documents = load_documents()

    print(f"전체 Document 개수: {len(documents)}")

    chunks = split_documents(documents)

    print(f"전체 Chunk 개수: {len(chunks)}")

    pc = get_pinecone_client()

    index = create_pinecone_index()

    vectors = create_vectors(
        pc,
        chunks,
    )

    upsert_documents(
        index,
        vectors,
    )
    print("Pinecone Hybrid Index 구축 완료")

    return index


def create_hybrid_retriever():
    pc = get_pinecone_client()

    existing_indexes = [index.name for index in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing_indexes:
        print("Pinecone Index가 없습니다.")

        build_pinecone()

    else:
        print(f"Pinecone Index 사용: {PINECONE_INDEX_NAME}")

    retriever = PineconeHybridRetriever()

    return retriever


if __name__ == "__main__":
    retriever = create_hybrid_retriever()

    query = "LangGraph에서 GRAPH_RECURSION_LIMIT 에러가 발생하는 이유는?"

    documents = retriever.invoke(query)

    print("검색 결과")

    for i, document in enumerate(
        documents,
        start=1,
    ):
        print()
        print(f"[{i}]")
        print(
            "score:",
            document.metadata.get("score"),
        )
        print(
            "technology:",
            document.metadata.get("technology"),
        )
        print(
            "document_type:",
            document.metadata.get("document_type"),
        )
        print(
            "source:",
            document.metadata.get("source"),
        )
        print(document.page_content[:500])
