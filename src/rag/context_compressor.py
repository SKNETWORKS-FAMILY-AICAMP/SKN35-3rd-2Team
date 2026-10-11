from langchain_core.documents import Document

from src.const.models import create_openai_model
from src.prompt.context_compressor_prompt import CONTEXT_COMPRESSOR_SYSTEM_PROMPT

model = create_openai_model()


def context_compressor(
    question: str,
    documents: list[Document],
) -> list[Document]:
    compressed_documents = []

    for document in documents:
        title = document.metadata.get("title", "제목 없음")
        source_url = document.metadata.get("source_url", "")

        document_content = (
            f"문서 제목: {title}\n"
            f"문서 출처: {source_url}\n\n"
            f"문서 본문:\n{document.page_content}"
        )

        print(f"\n압축 대상 문서: {title}")
        print(f"질문: {question}")
        print(f"원본 문서 길이: {len(document.page_content)}")

        try:
            response = model.invoke(
                [
                    {
                        "role": "system",
                        "content": CONTEXT_COMPRESSOR_SYSTEM_PROMPT(document_content),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"질문: {question}\n\n"
                            "위 문서 본문에서 질문과 관련된 내용을 추출하세요. "
                            "문서에 관련 정보가 있으면 반드시 해당 원문을 반환하세요. "
                            "관련 내용이 전혀 없을 때만 '관련 내용 없음'을 반환하세요."
                        ),
                    },
                ]
            )

            content = response.content

            if not isinstance(content, str):
                content = str(content)

            content = content.strip()

            print(f"압축 결과: {content[:500]}")

            if content and content != "관련 내용 없음":
                compressed_documents.append(
                    Document(
                        page_content=content,
                        metadata=document.metadata.copy(),
                    )
                )
            else:
                print(f"원본 문서 유지: {title}")
                compressed_documents.append(document)

        except Exception as e:
            print(f"압축 실패: {title} / {type(e).__name__}: {e}")
            print("원본 문서를 유지합니다.")
            compressed_documents.append(document)

    print(f"\n압축 전 문서 수: {len(documents)}")
    print(f"압축 후 문서 수: {len(compressed_documents)}")

    return compressed_documents
