"""
문서 로딩: data/pdf/*.pdf → LangChain Document 목록

입력 PDF (md_to_pdf.py 결과, 경로는 src/const/config.py 의 PDF_FILES)
  data/pdf/langchain.pdf
  data/pdf/langgraph.pdf
  data/pdf/mcp.pdf
tech 값은 PDF 파일 이름(langchain/langgraph/mcp)입니다.
이 PDF 들은 아래 구조라서, 페이지를 그냥 자르지 않고 "원래 문서(.mdx) 단위" 로 다시 묶을 수 있습니다.

  1쪽         표지
  2~n쪽       목차
  (폴더 구분 페이지)   예: "langchain / errors"
  문서 첫 쪽  [문서 제목]
              [langchain/errors/INVALID_PROMPT.mdx]   ← 원본 경로 줄 (문서 시작 표시)
              본문 ...
  각 쪽 맨 아래 "3 / 16" 같은 쪽 번호

그래서 로더는
  - 표지·목차·폴더 구분 페이지와 쪽 번호 줄을 버리고
  - "원본 경로 줄" 이 나올 때마다 새 문서를 시작해서
  - 문서 1개 = Document 1개 로 돌려줍니다 (여러 쪽에 걸친 문서는 이어 붙임)

Document.metadata
  tech        : langchain / langgraph / mcp   (PDF 파일 이름)
  title       : 문서 제목
  doc_path    : langchain/errors/INVALID_PROMPT.mdx  (원본 경로, 출처 표시용)
  source      : langchain.pdf
  page_start  : 시작 쪽 (1부터)
  page_end    : 끝 쪽
  doc_type    : official_doc
  parent_id   : langchain-errors-invalid_prompt   (문서 고유 ID, 청크들의 부모)

사용 예
  from src.rag.loader import load_documents
  docs = load_documents()                        # data/pdf 의 PDF 3개
  docs = load_documents(techs=["mcp"])           # mcp.pdf 만

  python -m src.rag.loader                           # 몇 개 읽혔는지 확인
"""

import re
from pathlib import Path

import pymupdf                                      # pip install pymupdf  (PDF 텍스트 추출, 빠르고 한글 OK)
from langchain_core.documents import Document

from src.const.config import PDF_FILES, TECHS

PAGE_NUMBER_RE = re.compile(r"^\s*\d+\s*/\s*\d+\s*$")             # "3 / 16"
SOURCE_LINE_RE = re.compile(r"^[\w.\-]+(?:/[\w.\- ]+)*\.mdx?$")   # "langchain/errors/x.mdx"


def make_parent_id(doc_path: str) -> str:
    """'langchain/errors/INVALID_PROMPT.mdx' → 'langchain-errors-invalid_prompt'"""
    stem = re.sub(r"\.mdx?$", "", doc_path)
    return re.sub(r"[^\w]+", "-", stem).strip("-").lower()


def _page_lines(page) -> list[str]:
    lines = [l.rstrip() for l in page.get_text().splitlines()]
    return [l for l in lines if l.strip() and not PAGE_NUMBER_RE.match(l)]


def tech_of(pdf_path: Path) -> str:
    """data/processed/mcp/mcp.pdf → 'mcp'. 기술 폴더 밖에 있으면 파일 이름으로."""
    for part in reversed(pdf_path.parent.parts):
        if part.lower() in TECHS:
            return part.lower()
    return pdf_path.stem.lower()


def load_pdf(pdf_path: Path, tech: str | None = None) -> list[Document]:
    """PDF 1개 → 원래 문서 단위 Document 목록."""
    tech = tech or tech_of(pdf_path)
    pdf = pymupdf.open(pdf_path)
    docs: list[Document] = []
    cur: dict | None = None                         # 지금 모으는 중인 문서

    def close_current():
        if cur and "\n".join(cur["lines"]).strip():
            docs.append(Document(
                page_content="\n".join(cur["lines"]).strip(),
                metadata={
                    "tech": tech,
                    "title": cur["title"],
                    "doc_path": cur["doc_path"],
                    "source": pdf_path.name,
                    "page_start": cur["page_start"],
                    "page_end": cur["page_end"],
                    "doc_type": "official_doc",
                    "parent_id": make_parent_id(cur["doc_path"]),
                },
            ))

    for page_no, page in enumerate(pdf, start=1):
        lines = _page_lines(page)
        # 이 페이지에서 "원본 경로 줄" 위치 찾기 (문서 시작 표시)
        src_idx = next((i for i, l in enumerate(lines) if i > 0 and SOURCE_LINE_RE.match(l.strip())), None)

        if src_idx is None:
            if cur is None or len(lines) <= 1:
                continue                            # 표지·목차·폴더 구분 페이지 → 버림
            cur["lines"].extend(lines)              # 앞 문서가 다음 쪽으로 이어짐
            cur["page_end"] = page_no
            continue

        if cur is not None and src_idx > 1:         # 제목 줄 앞에 남은 내용은 앞 문서 꼬리
            cur["lines"].extend(lines[: src_idx - 1])
        close_current()
        cur = {
            "title": lines[src_idx - 1].strip(),
            "doc_path": lines[src_idx].strip(),
            "lines": [],
            "page_start": page_no,
            "page_end": page_no,
        }
        cur["lines"].extend(lines[src_idx + 1:])

    close_current()
    pdf.close()
    return docs


def load_documents(techs: list[str] | None = None, pdf_files: dict | None = None) -> list[Document]:
    """data/pdf/langchain.pdf, langgraph.pdf, mcp.pdf 를 읽음. techs=["mcp"] 처럼 일부만 고를 수 있음.
    pdf_files={"langchain": "다른/경로.pdf", ...} 로 경로를 바꿀 수도 있음."""
    files = {t: Path(p) for t, p in (pdf_files or PDF_FILES).items()}
    if techs:
        files = {t: p for t, p in files.items() if t in {x.lower() for x in techs}}
    docs = []
    for tech, path in files.items():
        if not path.exists():
            print(f"[loader] 없음, 건너뜀: {path}")
            continue
        loaded = load_pdf(path, tech=tech)
        print(f"[loader] {path.name}: 문서 {len(loaded)}개")
        docs.extend(loaded)
    if not docs:
        raise FileNotFoundError(
            "읽을 PDF 가 없습니다. 다음 위치에 PDF 를 두세요: " + ", ".join(str(p) for p in files.values()))
    return docs


if __name__ == "__main__":
    all_docs = load_documents()
    print(f"총 {len(all_docs)}개 문서")
    if all_docs:
        d = all_docs[0]
        print("예시 메타데이터:", d.metadata)
        print("예시 본문:", d.page_content[:300])
