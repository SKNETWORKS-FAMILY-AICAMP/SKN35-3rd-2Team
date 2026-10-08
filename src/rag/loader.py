# MDX 파일을 LangChain Document 객체로 변환하는 모듈

from pathlib import Path

from langchain_core.documents import Document

from src.const.config import (
    RAW_LANGCHAIN_PATH,
    RAW_LANGGRAPH_PATH,
    RAW_MCP_PATH,
)


def _detect_document_type(file_path: Path) -> str:
    """
    파일 경로를 기반으로 문서 유형을 간단하게 판단한다.

    현재는 전처리를 하지 않기 때문에
    최소한의 metadata만 생성한다.
    """

    parts = file_path.parts

    if "errors" in parts:
        return "error"

    if "specification" in parts:
        return "specification"

    if "tutorials" in parts:
        return "tutorial"

    if "examples" in parts:
        return "example"

    if "docs" in parts:
        return "documentation"

    return "documentation"


def load_mdx_documents(
    root_dir: str,
    technology: str,
) -> list[Document]:
    """
    root_dir 아래의 모든 MDX 파일을 찾아
    LangChain Document 객체로 변환한다.

    Args:
        root_dir: MDX 파일이 저장된 루트 디렉터리
        technology: langchain / langgraph / mcp

    Returns:
        Document 리스트
    """

    root_path = Path(root_dir)

    if not root_path.exists():
        raise FileNotFoundError(f"디렉터리를 찾을 수 없습니다: {root_path}")

    documents = []

    mdx_files = sorted(root_path.rglob("*.mdx"))

    for file_path in mdx_files:
        text = file_path.read_text(encoding="utf-8")

        document_type = _detect_document_type(file_path)

        document = Document(
            page_content=text,
            metadata={
                "technology": technology,
                "document_type": document_type,
                "source": str(file_path),
                "file_name": file_path.name,
            },
        )

        documents.append(document)

    return documents


def load_documents():
    data_dict = {
        "langchain": RAW_LANGCHAIN_PATH,
        "langgraph": RAW_LANGGRAPH_PATH,
        "mcp": RAW_MCP_PATH,
    }

    documents = []

    for technology, path in data_dict.items():
        loaded_documents = load_mdx_documents(
            root_dir=path,
            technology=technology,
        )

        print(f"{technology} Document 개수: {len(loaded_documents)}")

        documents.extend(loaded_documents)

    print(f"전체 Document 개수: {len(documents)}")

    return documents
