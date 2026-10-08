# collect_docs.py 로 data/raw 에 저장한 공식 문서(.mdx / .md)를
# RAG 파이프라인(splitter → vectorstore)에서 바로 쓸 수 있는 LangChain Document 로 변환한다.
#
#   data/raw/langchain/**/*.mdx  →  Document(page_content=정리된 Markdown, metadata={...})
#   data/raw/langgraph/**/*.mdx
#   data/raw/mcp/**/*.mdx
#
# 결과 저장 (프레임워크별)
#   data/processed/{framework}/documents.jsonl      문서별 Document (1줄 = 문서 1개) → src/rag/loader.py 가 읽음
#   data/processed/{framework}/{framework}_merged.md 모든 문서를 하나로 병합한 파일 → 사람이 읽기·확인용
#
# 실행 (프로젝트 루트에서)
#   python -m src.preprocessing.mdx_to_document
#
# 전체 흐름 (PDF 변환 없음)
#   data/raw/**/*.mdx ─(이 파일)→ data/processed/{framework}/documents.jsonl
#                     ─(src/rag/loader.py)→ Document ─(splitter)→ 청크 ─(retriever.build_pinecone)→ Pinecone
#
# 코드에서 사용
#   from src.preprocessing.mdx_to_document import load_merged_documents
#   merged = load_merged_documents()                    # 프레임워크별 병합 Document 3개

import html
import json
import re
import textwrap
from pathlib import Path

from langchain_core.documents import Document

from src.const.config import PROCESSED_PATHS, PROJECT_ROOT, RAW_PATHS, RAW_SNIPPETS_PATH

# ============================================================
# 기본 설정
# ============================================================

FRAMEWORKS = [
    "langchain",
    "langgraph",
    "mcp",
]

# 변환 결과 파일 이름 (data/processed/{framework}/documents.jsonl) → src/rag/loader.py 가 읽음
DOCUMENTS_FILE_NAME = "documents.jsonl"

# 본문이 이보다 짧으면 (목차만 있는 index 등) 버린다
MIN_CONTENT_CHARS = 30

# 공식 문서 코드 예제(snippets)가 저장된 위치 (collect_snippets.py 로 수집)
SNIPPETS_DIR = RAW_SNIPPETS_PATH

# 문서 원본 GitHub 위치 (collect_docs.py 와 같은 저장소·경로)
GITHUB_SOURCES = {
    "langchain": "https://github.com/langchain-ai/docs/blob/main/src/oss/langchain/",
    "langgraph": "https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/",
    "mcp": "https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/",
}

# 문서 사이트 주소 규칙 (파일 경로에서 확장자를 뗀 값을 뒤에 붙임)
#   langchain/agents.mdx                        → https://docs.langchain.com/oss/python/langchain/agents
#   mcp/specification/2026-07-28/basic/index.mdx → https://modelcontextprotocol.io/specification/2026-07-28/basic
WEB_SOURCES = {
    "langchain": "https://docs.langchain.com/oss/python/langchain/",
    "langgraph": "https://docs.langchain.com/oss/python/langgraph/",
    "mcp": "https://modelcontextprotocol.io/",
}


# ============================================================
# 제외 규칙 (collect_docs.py 와 같은 기준)
# ============================================================

EXCLUDED_DIRECTORIES = {
    "frontend",
}

EXCLUDED_FILENAMES = {
    "changelog-js.mdx",
    "changelog-py.mdx",
}

EXCLUDED_FILENAME_KEYWORDS = {
    "version",
}


def should_exclude(path: str) -> bool:
    """
    변환 대상에서 제외해야 하는 파일인지 확인한다.

    제외 기준:
    1. frontend 디렉터리에 있는 문서
    2. changelog 파일
    3. 파일명에 version이 포함된 문서
    """

    path_obj = Path(path)

    for part in path_obj.parts:
        if part in EXCLUDED_DIRECTORIES:
            return True

    filename = path_obj.name.lower()

    if filename in EXCLUDED_FILENAMES:
        return True

    for keyword in EXCLUDED_FILENAME_KEYWORDS:
        if keyword in filename:
            return True

    return False


# ============================================================
# 공통 함수
# ============================================================


def read_file(file_path: Path) -> str:
    """파일을 읽는다. (Windows 줄바꿈 정리)"""

    return file_path.read_text(
        encoding="utf-8",
        errors="replace",
    ).replace("\r\n", "\n")


def get_raw_files(framework: str) -> list[Path]:
    """data/raw/{framework} 아래의 .mdx / .md 파일 목록을 가져온다."""

    framework_dir = RAW_PATHS[framework]

    if not framework_dir.exists():
        print(f"[건너뜀] 폴더 없음: {framework_dir}")
        return []

    files = []

    for file_path in sorted(framework_dir.rglob("*")):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in (".md", ".mdx"):
            continue

        relative_path = file_path.relative_to(framework_dir)

        if should_exclude(str(relative_path)):
            continue

        files.append(file_path)

    return files


FRONTMATTER_RE = re.compile(r"\A﻿?---\s*\n(.*?)\n---\s*\n", re.S)


def split_frontmatter(text: str) -> tuple[dict, str]:
    """
    문서 맨 위의 frontmatter(--- ... ---)를 분리한다.

    ---
    title: Agents
    description: "Build a LangChain agent ..."
    ---
    """

    match = FRONTMATTER_RE.match(text)

    if not match:
        return {}, text.lstrip("﻿")

    meta = {}

    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip("'\"")

    return meta, text[match.end():]


# ============================================================
# MDX → Markdown 정리
# ============================================================

FENCE_RE = re.compile(r"^\s*(```+|~~~+)")

SNIPPET_IMPORT_RE = re.compile(r"^import\s+(\w+)\s+from\s+['\"](/snippets/[^'\"]+)['\"];?\s*$", re.M)

ATTR_RE = re.compile(r'(\w+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|\{\s*["\'`]([^"\'`]*)["\'`]\s*\})')

# 대문자로 시작하는 JSX 컴포넌트 태그 (여는/닫는/자기 닫힘, 속성이 여러 줄이어도 잡음)
COMPONENT_RE = re.compile(r"<(/?)([A-Z][\w.]*)((?:\s+[^<>]*?)?)\s*(/?)>", re.S)

# 안내 상자 → "**Note:**" 처럼 굵은 머리글
CALLOUTS = {
    "note": "Note",
    "info": "Info",
    "tip": "Tip",
    "check": "Check",
    "warning": "Warning",
    "danger": "Danger",
    "caution": "Caution",
    "callout": "Note",
}

# 태그는 지우되 title 속성을 굵은 소제목으로 남길 컴포넌트
TITLED = {
    "tab",
    "step",
    "accordion",
    "expandable",
    "update",
    "paramfield",
    "responsefield",
}


def split_code_blocks(text: str) -> list[tuple[bool, str]]:
    """코드 블록(```)은 건드리면 안 되므로 [(코드인가?, 내용)] 조각으로 나눈다."""

    chunks, buf, in_code, fence = [], [], False, ""

    for line in text.splitlines(keepends=True):
        match = FENCE_RE.match(line)

        if not in_code and match:
            if buf:
                chunks.append((False, "".join(buf)))
            buf, in_code, fence = [line], True, match.group(1)[0] * 3

        elif in_code and line.strip().startswith(fence) and line.strip().strip(fence[0]) == "":
            buf.append(line)
            chunks.append((True, "".join(buf)))
            buf, in_code = [], False

        else:
            buf.append(line)

    if buf:
        chunks.append((in_code, "".join(buf)))

    return chunks


def resolve_snippets(text: str) -> str:
    """
    LangChain 문서는 코드 예제를 별도 파일(snippets)에서 불러온다.

      import AgentsIntroPy from '/snippets/code-samples/agents-intro-py.mdx';
      ...
      <AgentsIntroPy />

    data/raw/snippets/ 에 그 파일이 있으면 <AgentsIntroPy /> 자리에 코드를 그대로 넣는다.
    (없으면 태그만 지워짐 → collect_snippets.py 로 먼저 수집 권장)
    JavaScript 예제(-js)는 Python 문서만 쓰므로 넣지 않는다.
    """

    snippets = {}

    for name, snippet_path in SNIPPET_IMPORT_RE.findall(text):
        if snippet_path.endswith(("-js.mdx", "-ts.mdx")):
            snippets[name] = ""
            continue

        file_path = SNIPPETS_DIR / snippet_path.removeprefix("/snippets/")

        if file_path.exists():
            _, body = split_frontmatter(read_file(file_path))
            snippets[name] = "\n" + textwrap.dedent(body).strip() + "\n"
        else:
            snippets[name] = ""

    for name, body in snippets.items():
        text = re.sub(rf"<{name}\s*/>", lambda _m, b=body: b, text)

    return text


def keep_python_blocks(text: str) -> str:
    """
    LangChain 문서의 언어별 블록 처리

      :::python      → 안쪽 내용만 남김
      ...
      :::
      :::js          → 통째로 버림 (Python 문서만 사용)
      ...
      :::
    """

    out, mode, in_code, fence = [], None, False, ""

    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        match = FENCE_RE.match(line)

        if in_code:
            if stripped.startswith(fence) and stripped.strip(fence[0]) == "":
                in_code = False
            if mode != "drop":
                out.append(line)
            continue

        if match:
            in_code, fence = True, match.group(1)[0] * 3
            if mode != "drop":
                out.append(line)
            continue

        if stripped in (":::python", ":::py"):
            mode = "keep"
            continue

        if stripped in (":::js", ":::ts", ":::javascript", ":::typescript"):
            mode = "drop"
            continue

        if stripped == ":::" and mode is not None:
            mode = None
            continue

        if mode != "drop":
            out.append(line)

    return "".join(out)


def attrs_of(attr_text: str) -> dict:
    return {
        m.group(1): next(g for g in m.groups()[1:] if g is not None)
        for m in ATTR_RE.finditer(attr_text or "")
    }


def replace_component(match: re.Match) -> str:
    closing, name, attr_text = match.group(1), match.group(2), match.group(3)

    lower = name.lower()
    attrs = attrs_of(attr_text)
    title = attrs.get("title") or attrs.get("label") or attrs.get("name") or ""

    if lower in CALLOUTS:
        return "\n\n" if closing else f"\n\n**{CALLOUTS[lower]}:**\n\n"

    if lower == "card":
        if closing:
            return "\n\n"
        href = attrs.get("href")
        return f"\n\n- [{title}]({href})\n\n" if title and href else (f"\n\n- **{title}**\n\n" if title else "\n\n")

    if lower in TITLED:
        if closing or not title:
            return "\n\n"
        return f"\n\n**{title}**\n\n"

    return "\n\n"                     # 나머지(Tabs, CodeGroup, CardGroup, Steps ...): 태그만 지움


def clean_prose(text: str) -> str:
    """코드 블록 바깥 부분만 정리한다."""

    text = re.sub(r"\{/\*.*?\*/\}", "", text, flags=re.S)                    # {/* JSX 주석 */}
    text = re.sub(r"^(import|export)\s[^\n]*\n?", "", text, flags=re.M)       # import / export 줄
    text = re.sub(r"<img\b[^>]*?/?>", "", text, flags=re.S)                  # 이미지 태그
    text = re.sub(r"</?(?:div|span|br|p)\b[^>]*>", "\n", text)                # 레이아웃용 HTML
    text = re.sub(r"@\[([^\]]+)\](?:\[[^\]]*\])?", r"\1", text)               # @[`create_agent`] → `create_agent`

    # Docusaurus 식 안내 상자 :::note → **Note:**
    text = re.sub(
        r"^[ \t]*:::(note|tip|info|warning|caution|danger)[ \t]*(.*)$",
        lambda m: f"\n**{m.group(1).capitalize()}:** {m.group(2)}\n",
        text,
        flags=re.M | re.I,
    )
    text = re.sub(r"^[ \t]*:::[ \t]*$", "", text, flags=re.M)

    text = COMPONENT_RE.sub(replace_component, text)                          # JSX 컴포넌트
    text = re.sub(r"</?>", "", text)                                          # <> </>
    text = re.sub(r"\{\s*['\"]\s*['\"]\s*\}", " ", text)                      # {' '}

    return html.unescape(text)


def dedent_blocks(text: str) -> str:
    """
    컴포넌트 안쪽 내용은 보통 2~4칸 들여쓰기 되어 있다.
    그대로 두면 Markdown 에서 코드 블록으로 오해하므로 빈 줄로 나뉜 덩어리마다 들여쓰기를 걷어낸다.
    (목록 아래 들여쓴 내용은 목록의 일부이므로 유지)
    """

    out, block = [], []

    def flush():
        if not block:
            return
        previous = next((line for line in reversed(out) if line.strip()), "")
        if re.match(r"^\s*([-*+]|\d+[.)])\s", previous) and block[0].startswith((" ", "\t")):
            out.extend(block)
        else:
            out.extend(textwrap.dedent("\n".join(block)).split("\n"))
        block.clear()

    for line in text.split("\n"):
        if line.strip() == "":
            flush()
            out.append(line)
        else:
            block.append(line)

    flush()

    return "\n".join(out)


def clean_mdx(text: str) -> str:
    """MDX 본문 → 일반 Markdown (코드 블록은 그대로 보존)."""

    text = resolve_snippets(text)
    text = keep_python_blocks(text)

    text = "".join(
        chunk if is_code else clean_prose(chunk)
        for is_code, chunk in split_code_blocks(text)
    )

    text = dedent_blocks(text)
    text = re.sub(r"^[ \t]+$", "", text, flags=re.M)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ============================================================
# Document 만들기
# ============================================================


def make_parent_id(doc_path: str) -> str:
    """'langchain/errors/INVALID_PROMPT_INPUT.mdx' → 'langchain-errors-invalid_prompt_input'"""

    stem = re.sub(r"\.mdx?$", "", doc_path)

    return re.sub(r"[^\w]+", "-", stem).strip("-").lower()


def make_source_url(framework: str, relative_path: str) -> str:
    """문서 사이트 주소 (index.mdx 는 폴더 주소)"""

    path = re.sub(r"\.mdx?$", "", relative_path.replace("\\", "/"))
    path = re.sub(r"(^|/)index$", "", path)

    return WEB_SOURCES[framework] + path


def detect_document_type(relative_path: Path) -> str:
    """경로로 문서 유형 판단 (팀 loader 의 _detect_document_type 과 같은 규칙)"""

    parts = Path(relative_path).parts

    if "errors" in parts:
        return "error"

    if "specification" in parts:
        return "specification"

    if "tutorials" in parts:
        return "tutorial"

    if "examples" in parts:
        return "example"

    return "documentation"


def relative_source(file_path: Path) -> str:
    """프로젝트 루트 기준 경로 (팀원마다 절대경로가 달라서 상대경로로 저장)"""

    try:
        return file_path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return file_path.as_posix()


def make_document(
    framework: str,
    file_path: Path,
) -> Document | None:
    """
    .mdx 파일 1개 → Document 1개 (본문이 너무 짧으면 None)

    metadata
      technology    : langchain / langgraph / mcp
      document_type : error / specification / tutorial / example / documentation
      source        : data/raw/langchain/errors/INVALID_PROMPT_INPUT.mdx  (프로젝트 루트 기준)
      file_name     : INVALID_PROMPT_INPUT.mdx
      title, description, source_url(문서 사이트), github_url, parent_id, format="markdown"
    """

    relative_path = file_path.relative_to(RAW_PATHS[framework]).as_posix()

    frontmatter, body = split_frontmatter(read_file(file_path))

    text = clean_mdx(body)

    if len(text) < MIN_CONTENT_CHARS:
        return None

    # 제목: frontmatter title → 본문 첫 H1 → 파일 이름
    h1 = re.match(r"^#\s+(.+)$", text, re.M)
    title = frontmatter.get("title") or (h1.group(1).strip() if h1 else file_path.stem)
    description = frontmatter.get("description", "")

    # 제목과 설명을 본문 맨 앞에 붙여 검색이 잘 되게 한다
    if not (h1 and h1.group(1).strip() == title):
        header = f"# {title}\n\n" + (f"{description}\n\n" if description else "")
        text = header + text

    return Document(
        page_content=text,
        metadata={
            "technology": framework,
            "document_type": detect_document_type(Path(relative_path)),
            "source": relative_source(file_path),
            "file_name": file_path.name,
            "title": title,
            "description": description,
            "source_url": make_source_url(framework, relative_path),
            "github_url": GITHUB_SOURCES[framework] + relative_path,
            "parent_id": make_parent_id(f"{framework}/{relative_path}"),
            "format": "markdown",
        },
    )


def save_documents(
    framework: str,
    documents: list[Document],
) -> Path:
    """data/processed/{framework}/documents.jsonl 에 저장한다."""

    file_path = PROCESSED_PATHS[framework] / DOCUMENTS_FILE_NAME

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with file_path.open("w", encoding="utf-8") as f:
        for document in documents:
            f.write(json.dumps({"text": document.page_content, **document.metadata}, ensure_ascii=False) + "\n")

    print(f"저장: {file_path}")

    return file_path


def merge_documents(
    framework: str,
    documents: list[Document],
) -> Document:
    """
    한 프레임워크의 문서들을 Document 1개로 병합한다.

    문서 사이에는 구분선(---)과 출처를 넣는다.

      # Agents
      > 출처: langchain/agents.mdx | https://docs.langchain.com/oss/python/langchain/agents
      ...본문...

      ---

      # Models
      ...
    """

    sections = []

    for document in documents:
        meta = document.metadata
        source_line = f"> 출처: {meta['source']} | {meta['source_url']}"

        body = document.page_content
        if body.startswith("# "):
            first_line, _, rest = body.partition("\n")
            body = f"{first_line}\n{source_line}\n{rest}"
        else:
            body = f"{source_line}\n\n{body}"

        sections.append(body)

    return Document(
        page_content="\n\n---\n\n".join(sections),
        metadata={
            "technology": framework,
            "document_type": "documentation",
            "source": f"data/raw/{framework}",
            "title": f"{framework} 공식 문서 (병합)",
            "parent_id": f"{framework}-merged",
            "format": "markdown",
            "doc_count": len(documents),
        },
    )


def save_merged(
    framework: str,
    merged: Document,
) -> Path:
    """data/processed/{framework}/{framework}_merged.md 에 병합 문서를 저장한다."""

    file_path = PROCESSED_PATHS[framework] / f"{framework}_merged.md"

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path.write_text(
        merged.page_content,
        encoding="utf-8",
    )

    print(f"저장: {file_path}  (문서 {merged.metadata['doc_count']}개 병합)")

    return file_path


def load_merged_documents(frameworks: list[str] | None = None) -> list[Document]:
    """프레임워크별 병합 Document 목록 (langchain 1개, langgraph 1개, mcp 1개)"""

    merged = []

    for framework in frameworks or FRAMEWORKS:
        documents = load_framework(framework)
        if documents:
            merged.append(merge_documents(framework, documents))

    return merged


def load_framework(framework: str) -> list[Document]:
    """data/raw/{framework} 의 모든 문서를 Document 로 변환한다."""

    print()
    print("=" * 60)
    print(framework.upper())
    print("=" * 60)

    files = get_raw_files(framework)

    print(f"변환 대상 문서 개수: {len(files)}")

    documents = []

    for index, file_path in enumerate(
        files,
        start=1,
    ):
        try:
            document = make_document(framework, file_path)

            if document is None:
                print(f"[{index}/{len(files)}] (본문 없음, 건너뜀) {file_path.name}")
                continue

            documents.append(document)

        except Exception as e:
            print(f"[실패] {file_path}")
            print(f"       {e}")

    print(f"변환 완료: {len(documents)}개")

    return documents


def convert_framework(framework: str) -> list[Document]:
    """변환 + 저장 (documents.jsonl, {framework}_merged.md). loader 가 결과 파일이 없을 때도 호출."""

    documents = load_framework(framework)

    if documents:
        save_documents(framework, documents)                           # 문서별 → loader 가 읽음
        save_merged(framework, merge_documents(framework, documents))  # 병합본 → 사람이 확인용

    return documents


# ============================================================
# LangChain / LangGraph / MCP
# ============================================================


def load_langchain() -> list[Document]:
    return load_framework("langchain")


def load_langgraph() -> list[Document]:
    return load_framework("langgraph")


def load_mcp() -> list[Document]:
    return load_framework("mcp")


# ============================================================
# Main
# ============================================================


def main() -> None:

    print("=" * 60)
    print(".mdx → Document 변환 시작")
    print("=" * 60)

    total = 0

    for framework in FRAMEWORKS:
        total += len(convert_framework(framework))

    print()
    print("=" * 60)
    print(f".mdx → Document 변환 완료: 총 {total}개")
    print("다음 단계: python -m src.vectorstore.build")
    print("=" * 60)


if __name__ == "__main__":
    main()
