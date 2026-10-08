# LangChain / LangGraph 문서가 import 하는 코드 예제(snippets)를 수집한다.
#
# langchain-ai/docs 저장소는 코드 예제를 문서 본문이 아닌 별도 파일에 둔다.
#
#   import AgentsIntroPy from '/snippets/code-samples/agents-intro-py.mdx';
#   <AgentsIntroPy />
#
# collect_docs.py 는 문서만 받으므로 이 예제들이 빠진다.
# 이 스크립트는 data/raw/{langchain,langgraph} 문서가 실제로 import 하는 Python 예제만 골라
# data/raw/snippets/... 에 저장한다. 그 뒤 mdx_to_document.py 가 예제 코드를 본문에 끼워 넣는다.
#
# 실행 (collect_docs.py 다음, 프로젝트 루트에서)
#   python -m src.preprocessing.collect_snippets

import re

import requests

from src.const.config import RAW_PATHS, RAW_SNIPPETS_PATH

# ============================================================
# 기본 설정
# ============================================================

REPOSITORY = "langchain-ai/docs"

BRANCH = "main"

SNIPPETS_DIR = RAW_SNIPPETS_PATH

HEADERS = {
    "User-Agent": "official-docs-crawler/1.0",
}

session = requests.Session()

session.headers.update(HEADERS)

SNIPPET_IMPORT_RE = re.compile(r"""^import\s+\w+\s+from\s+['"]/snippets/([^'"]+)['"]""", re.M)


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


def find_snippet_paths() -> list[str]:
    """data/raw/langchain, langgraph 문서가 import 하는 Python 예제 경로를 모은다."""

    paths = set()

    for framework in ("langchain", "langgraph"):
        for file_path in RAW_PATHS[framework].rglob("*.mdx"):
            text = file_path.read_text(encoding="utf-8", errors="replace")

            for snippet_path in SNIPPET_IMPORT_RE.findall(text):
                if snippet_path.endswith(("-js.mdx", "-ts.mdx")):
                    continue
                paths.add(snippet_path)

    return sorted(paths)


def collect_snippets() -> None:

    print("=" * 60)
    print("SNIPPETS")
    print("=" * 60)

    paths = find_snippet_paths()

    print(f"수집 대상 예제 개수: {len(paths)}")

    for index, snippet_path in enumerate(
        paths,
        start=1,
    ):
        file_path = SNIPPETS_DIR / snippet_path

        if file_path.exists():
            continue

        try:
            raw_url = f"https://raw.githubusercontent.com/{REPOSITORY}/{BRANCH}/src/snippets/{snippet_path}"

            content = download(raw_url)

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_path.write_text(
                content,
                encoding="utf-8",
            )

            print(f"[{index}/{len(paths)}] {snippet_path}")

        except Exception as e:
            print(f"[실패] {snippet_path}")
            print(f"       {e}")

    print(f"저장 위치: {SNIPPETS_DIR}")


if __name__ == "__main__":
    collect_snippets()
