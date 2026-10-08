# LangChain, LangGraph, MCP의 최신 공식 문서 중
# RAG에 필요한 핵심 개발 문서만 수집하여 Markdown 파일로 저장한다.

from pathlib import Path

import requests

# ============================================================
# 기본 설정
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"

HEADERS = {
    "User-Agent": "official-docs-crawler/1.0",
}


# ============================================================
# HTTP Session
# ============================================================

session = requests.Session()

session.headers.update(HEADERS)


# ============================================================
# 제외 규칙
# ============================================================

# 디렉터리 단위로 제외할 경로
EXCLUDED_DIRECTORIES = {
    "frontend",
}

# 파일명 단위로 제외할 파일
EXCLUDED_FILENAMES = {
    "changelog-js.mdx",
    "changelog-py.mdx",
}

# 파일명에 특정 문자열이 포함되면 제외
EXCLUDED_FILENAME_KEYWORDS = {
    "version",
}


def should_exclude(path: str) -> bool:
    """
    수집 대상에서 제외해야 하는 파일인지 확인한다.

    제외 기준:
    1. frontend 디렉터리에 있는 문서
    2. changelog 파일
    3. 파일명에 version이 포함된 문서
    """

    path_obj = Path(path)

    # --------------------------------------------------------
    # 디렉터리 제외
    # --------------------------------------------------------

    for part in path_obj.parts:
        if part in EXCLUDED_DIRECTORIES:
            return True

    # --------------------------------------------------------
    # 파일명 제외
    # --------------------------------------------------------

    filename = path_obj.name.lower()

    if filename in EXCLUDED_FILENAMES:
        return True

    # --------------------------------------------------------
    # 파일명 키워드 제외
    # --------------------------------------------------------

    for keyword in EXCLUDED_FILENAME_KEYWORDS:
        if keyword in filename:
            return True

    return False


# ============================================================
# 공통 함수
# ============================================================


def download(url: str) -> str:
    """URL에서 텍스트를 다운로드한다."""

    response = session.get(
        url,
        timeout=30,
    )

    response.raise_for_status()

    return response.text


def save_file(
    framework: str,
    relative_path: str,
    content: str,
) -> None:
    """data/raw/{framework} 아래에 파일을 저장한다."""

    file_path = RAW_DIR / framework / relative_path

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    print(f"저장: {file_path}")


def get_github_tree(
    repository: str,
    branch: str = "main",
) -> list[dict]:
    """GitHub repository의 전체 파일 트리를 가져온다."""

    url = f"https://api.github.com/repos/{repository}/git/trees/{branch}?recursive=1"

    response = session.get(
        url,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["tree"]


# ============================================================
# LangChain
# ============================================================


def collect_langchain() -> None:
    """
    LangChain 공식 documentation repository에서
    RAG에 필요한 LangChain 문서만 수집한다.
    """

    print()
    print("=" * 60)
    print("LANGCHAIN")
    print("=" * 60)

    repository = "langchain-ai/docs"
    branch = "main"

    directory = "src/oss/langchain"

    tree = get_github_tree(
        repository=repository,
        branch=branch,
    )

    files = []

    for item in tree:
        path = item.get("path", "")

        if item.get("type") != "blob":
            continue

        if not path.startswith(directory + "/"):
            continue

        if not path.endswith(
            (
                ".md",
                ".mdx",
            )
        ):
            continue

        # 불필요한 문서 제외
        relative_path = Path(path).relative_to(directory)

        if should_exclude(str(relative_path)):
            continue

        files.append(path)

    print(f"수집 대상 문서 개수: {len(files)}")

    for index, path in enumerate(
        files,
        start=1,
    ):
        try:
            raw_url = f"https://raw.githubusercontent.com/{repository}/{branch}/{path}"

            content = download(raw_url)

            relative_path = Path(path).relative_to(directory)

            print(f"[{index}/{len(files)}] {relative_path}")

            save_file(
                framework="langchain",
                relative_path=str(relative_path),
                content=content,
            )

        except Exception as e:
            print(f"[실패] {path}")
            print(f"       {e}")


# ============================================================
# LangGraph
# ============================================================


def collect_langgraph() -> None:
    """
    LangGraph 공식 documentation repository에서
    RAG에 필요한 LangGraph 문서만 수집한다.
    """

    print()
    print("=" * 60)
    print("LANGGRAPH")
    print("=" * 60)

    repository = "langchain-ai/docs"
    branch = "main"

    directory = "src/oss/langgraph"

    tree = get_github_tree(
        repository=repository,
        branch=branch,
    )

    files = []

    for item in tree:
        path = item.get("path", "")

        if item.get("type") != "blob":
            continue

        if not path.startswith(directory + "/"):
            continue

        if not path.endswith(
            (
                ".md",
                ".mdx",
            )
        ):
            continue

        # 불필요한 문서 제외
        relative_path = Path(path).relative_to(directory)

        if should_exclude(str(relative_path)):
            continue

        files.append(path)

    print(f"수집 대상 문서 개수: {len(files)}")

    for index, path in enumerate(
        files,
        start=1,
    ):
        try:
            raw_url = f"https://raw.githubusercontent.com/{repository}/{branch}/{path}"

            content = download(raw_url)

            relative_path = Path(path).relative_to(directory)

            print(f"[{index}/{len(files)}] {relative_path}")

            save_file(
                framework="langgraph",
                relative_path=str(relative_path),
                content=content,
            )

        except Exception as e:
            print(f"[실패] {path}")
            print(f"       {e}")


# ============================================================
# MCP
# ============================================================


def collect_mcp() -> None:
    """
    MCP 공식 repository에서
    최신 Documentation과 Specification만 수집한다.

    현재 최신 MCP 버전:
    2026-07-28
    """

    print()
    print("=" * 60)
    print("MCP")
    print("=" * 60)

    repository = "modelcontextprotocol/modelcontextprotocol"

    branch = "main"

    latest_version = "2026-07-28"

    tree = get_github_tree(
        repository=repository,
        branch=branch,
    )

    files = []

    # --------------------------------------------------------
    # 최신 MCP Documentation
    # --------------------------------------------------------

    docs_prefix = f"docs/docs/{latest_version}/"

    # --------------------------------------------------------
    # 최신 MCP Specification
    # --------------------------------------------------------

    specification_prefix = f"docs/specification/{latest_version}/"

    for item in tree:
        path = item.get("path", "")

        if item.get("type") != "blob":
            continue

        if not path.endswith(
            (
                ".md",
                ".mdx",
            )
        ):
            continue

        # 최신 Documentation
        if path.startswith(docs_prefix):
            relative_path = Path(path).relative_to("docs")

            if should_exclude(str(relative_path)):
                continue

            files.append(path)

            continue

        # 최신 Specification
        if path.startswith(specification_prefix):
            relative_path = Path(path).relative_to("docs")

            if should_exclude(str(relative_path)):
                continue

            files.append(path)

            continue

    print(f"수집 대상 문서 개수: {len(files)}")

    for index, path in enumerate(
        files,
        start=1,
    ):
        try:
            raw_url = f"https://raw.githubusercontent.com/{repository}/{branch}/{path}"

            content = download(raw_url)

            # ------------------------------------------------
            # 저장 경로 정리
            #
            # docs/docs/2026-07-28/...
            #       ↓
            # data/raw/mcp/docs/2026-07-28/...
            #
            # docs/specification/2026-07-28/...
            #       ↓
            # data/raw/mcp/specification/2026-07-28/...
            #
            # 첫 번째 docs/ 제거
            # ------------------------------------------------

            relative_path = Path(path).relative_to("docs")

            print(f"[{index}/{len(files)}] {relative_path}")

            save_file(
                framework="mcp",
                relative_path=str(relative_path),
                content=content,
            )

        except Exception as e:
            print(f"[실패] {path}")
            print(f"       {e}")


# ============================================================
# Main
# ============================================================


def main() -> None:

    print("=" * 60)
    print("공식 문서 수집 시작")
    print("=" * 60)

    # LangChain
    collect_langchain()

    # LangGraph
    collect_langgraph()

    # MCP
    collect_mcp()

    print()
    print("=" * 60)
    print("공식 문서 수집 완료")
    print("=" * 60)

    print()
    print(f"저장 위치: {RAW_DIR}")


if __name__ == "__main__":
    main()
