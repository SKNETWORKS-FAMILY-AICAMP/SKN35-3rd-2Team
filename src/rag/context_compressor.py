from langchain_core.documents import Document

from src.const.models import create_openai_model
from src.prompt.context_compressor_prompt import CONTEXT_COMPRESSOR_SYSTEM_PROMPT

model = create_openai_model()


def context_compressor(question, documents):
    compressed_documents = []

    for document in documents:
        response = model.invoke(
            [
                {"role": "system", "content": CONTEXT_COMPRESSOR_SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ]
        )

        content = response.content

        print("content : ", content)

        if content:
            compressed_documents.append(
                Document(page_content=content, metadata=document.metadata)
            )

    return compressed_documents
