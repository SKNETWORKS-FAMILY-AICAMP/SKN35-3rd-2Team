"""
2단계: 병합된 Markdown → PDF 변환

1단계 merge_mdx.py 가 만든 data/merged/*.md 를 각각 PDF 로 바꿉니다.

  data/merged/langchain.md  →  data/pdf/langchain.pdf
  data/merged/langgraph.md  →  data/pdf/langgraph.pdf
  data/merged/mcp.md        →  data/pdf/mcp.pdf

변환 방식
  Markdown → HTML (python-markdown) → PDF (헤드리스 Chromium, playwright)
  - 표지 + 클릭되는 목차 + 문서마다 새 페이지 + 쪽 번호 + PDF 책갈피
  - 한글 폰트: Noto Sans KR → 맑은 고딕 → Apple SD Gothic Neo → 나눔고딕 순으로 자동 사용

설치 (한 번만)
  pip install markdown playwright
  python -m playwright install chromium

사용 예
  python md_to_pdf.py                                   # data/merged/*.md → data/pdf/*.pdf
  python md_to_pdf.py --src data/merged --out data/pdf
  python md_to_pdf.py --src data/merged/mcp.md          # 파일 하나만
  python md_to_pdf.py --keep-html                       # 중간 HTML 도 저장 (모양 확인용)

요구 사항
  Python 3.10 이상
"""

# ---------------------------------------------------------------------------
# 표준 라이브러리
# ---------------------------------------------------------------------------
import argparse                     # 명령줄 옵션 처리
import html                         # 제목 이스케이프
import re                           # 제목·파일 수 읽기
from pathlib import Path            # 파일 경로 처리

# ---------------------------------------------------------------------------
# 외부 라이브러리 (pip install markdown playwright)
# ---------------------------------------------------------------------------
import markdown                     # Markdown → HTML
from playwright.sync_api import sync_playwright   # HTML → PDF (Chromium)

FONT_STACK = ('"Noto Sans KR", "Malgun Gothic", "맑은 고딕", "Apple SD Gothic Neo", '
              '"NanumGothic", "WenQuanYi Zen Hei", sans-serif')
MONO_STACK = ('"D2Coding", "Consolas", "Menlo", "DejaVu Sans Mono", '
              '"Malgun Gothic", "Apple SD Gothic Neo", "WenQuanYi Zen Hei Mono", monospace')

CSS = f"""
@page {{ size: A4; }}
body {{ font-family: {FONT_STACK}; font-size: 10.5pt; line-height: 1.6; color: #222;
        word-break: keep-all; overflow-wrap: anywhere; }}
h1 {{ font-size: 20pt; border-bottom: 2px solid #333; padding-bottom: 4px; }}
h2 {{ font-size: 15pt; border-bottom: 1px solid #ccc; padding-bottom: 2px; }}
h3 {{ font-size: 12.5pt; }}
h1, h2, h3, h4 {{ break-after: avoid; }}
pre, code {{ font-family: {MONO_STACK}; font-size: 9pt; }}
code {{ background: #f3f3f3; padding: 1px 3px; border-radius: 3px; }}
pre {{ background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 4px; padding: 8px 10px;
       white-space: pre-wrap; word-break: break-all; }}
pre code {{ background: none; padding: 0; }}
table {{ border-collapse: collapse; width: 100%; font-size: 9.5pt; }}
th, td {{ border: 1px solid #ccc; padding: 4px 6px; vertical-align: top; }}
th {{ background: #f0f0f0; }}
tr, img, blockquote {{ break-inside: avoid; }}
img {{ max-width: 100%; }}
blockquote {{ border-left: 4px solid #ccc; margin: 0; padding: 2px 12px; color: #555; }}
.callout {{ border-left: 4px solid #4a90d9; background: #eef5fc; padding: 6px 12px;
            margin: 10px 0; border-radius: 3px; }}
.callout.warning, .callout.caution, .callout.danger, .callout.important {{
            border-color: #d9534f; background: #fdf0ef; }}
.callout.tip, .callout.check {{ border-color: #3c9a5f; background: #eef8f1; }}
.callout-label {{ font-weight: bold; margin: 0 0 2px 0; }}
.page-break {{ break-after: page; }}
.folder-title {{ font-size: 22pt; font-weight: bold; color: #4a90d9; text-align: center;
                 padding-top: 35vh; break-after: page; }}
.cover {{ text-align: center; padding-top: 35vh; }}
.cover h1 {{ border: none; font-size: 28pt; }}
.toc ul {{ list-style: none; padding-left: 1.2em; }}
.toc > ul {{ padding-left: 0; }}
.toc a {{ color: #222; text-decoration: none; }}
.source {{ color: #888; font-size: 8.5pt; margin-top: -6px; }}
"""

FOOTER = ('<div style="width:100%;font-size:8px;color:#888;text-align:center;">'
          '<span class="pageNumber"></span> / <span class="totalPages"></span></div>')


def md_to_html(md_text: str, title: str, toc_depth: int) -> str:
    md = markdown.Markdown(
        extensions=["extra", "toc", "sane_lists"],   # extra = 표·코드블록·md_in_html(상자 안 Markdown)
        extension_configs={"toc": {"toc_depth": f"1-{toc_depth}"}},
    )
    body = md.convert(md_text)
    m = re.search(r"files:\s*(\d+)", md_text)        # merge_mdx.py 가 남긴 파일 수
    count = f"<p>{m.group(1)}개 문서</p>" if m else ""
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>{CSS}</style></head><body>
<section class="cover"><h1>{html.escape(title)}</h1>{count}</section>
<div class="page-break"></div>
<section class="toc"><h2>목차</h2>{md.toc}</section>
<div class="page-break"></div>
{body}
</body></html>"""


def convert(md_files: list[Path], out_dir: Path, toc_depth: int, keep_html: bool, chromium: str | None):
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:                      # 브라우저는 한 번만 띄우고 파일마다 재사용
        browser = p.chromium.launch(executable_path=chromium) if chromium else p.chromium.launch()
        for md_path in md_files:
            text = md_path.read_text(encoding="utf-8")
            m = re.search(r"<!-- title:\s*(.+?)\s*-->", text)
            title = m.group(1) if m else md_path.stem

            html_path = out_dir / f"{md_path.stem}.html"
            pdf_path = out_dir / f"{md_path.stem}.pdf"
            # Chromium 이 이미지(file://)를 읽을 수 있도록 HTML 을 파일로 저장한 뒤 엶
            html_path.write_text(md_to_html(text, title, toc_depth), encoding="utf-8")

            page = browser.new_page()
            page.goto(html_path.resolve().as_uri(), wait_until="networkidle", timeout=180_000)
            page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,                # 코드 블록·상자 배경색
                display_header_footer=True,
                header_template="<span></span>",
                footer_template=FOOTER,               # 쪽 번호
                margin={"top": "18mm", "bottom": "20mm", "left": "16mm", "right": "16mm"},
                outline=True,                         # 제목 → PDF 책갈피
                tagged=True,
            )
            page.close()
            if not keep_html:
                html_path.unlink()
            print(f"[완료] {md_path} → {pdf_path}")
        browser.close()


def main():
    ap = argparse.ArgumentParser(description="병합된 .md 를 PDF 로 변환")
    ap.add_argument("--src", type=Path, default=Path("data/merged"), help=".md 파일 또는 폴더 (기본 data/merged)")
    ap.add_argument("--out", type=Path, default=Path("data/pdf"), help="PDF 저장 폴더 (기본 data/pdf)")
    ap.add_argument("--toc-depth", type=int, default=2, help="목차에 넣을 제목 깊이 (기본 2)")
    ap.add_argument("--keep-html", action="store_true", help="중간 HTML 도 저장")
    ap.add_argument("--chromium", help="Chromium 실행 파일 경로 (보통 필요 없음)")
    args = ap.parse_args()

    if args.src.is_dir():
        md_files = sorted(args.src.glob("*.md"))
    elif args.src.is_file():
        md_files = [args.src]
    else:
        raise SystemExit(f"없음: {args.src}")
    if not md_files:
        raise SystemExit(f"{args.src} 에 .md 파일이 없습니다. 먼저 merge_mdx.py 를 실행하세요.")

    convert(md_files, args.out, args.toc_depth, args.keep_html, args.chromium)


if __name__ == "__main__":
    main()
