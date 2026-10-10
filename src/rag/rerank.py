from const.models import create_rerank

reranker = create_rerank()


def rerank(documents, question, top_n=5):
    results = reranker.compress_documents(documents, question)

    return results[:top_n]
