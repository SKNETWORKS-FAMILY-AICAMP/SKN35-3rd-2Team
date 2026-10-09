"""
1단계: 폴더별 .mdx 병합  (→ 정리된 Markdown 파일 1개씩)

data/raw 아래의 최상위 폴더(langchain, langgraph, mcp ...) 마다
그 폴더와 모든 하위 폴더의 .mdx 를 하나의 .md 로 합칩니다.
PDF 변환은 2단계 md_to_pdf.py 가 따로 합니다.

  data/raw/langchain/**/*.mdx  →  data/merged/langchain.md
  data/raw/langgraph/**/*.mdx  →  data/merged/langgraph.md
  data/raw/mcp/**/*.mdx        →  data/merged/mcp.md

합치는 순서 (폴더 트리를 위에서부터 읽는 순서)
  1. 해당 폴더 바로 안의 파일들 (파일 이름 자연 정렬: 2-a 가 10-b 보다 먼저)
  2. 그다음 하위 폴더를 이름순으로, 각 하위 폴더 안에서도 같은 규칙을 반복

합치면서 하는 일 (MDX → 일반 Markdown)
  - frontmatter(--- ... ---) 의 title 을 장 제목으로 쓰고 제거
  - import / export 줄, {/* JSX 주석 */} 제거
  - <Note>, <Warning>, :::tip 같은 안내 상자 → <div class="callout ..."> 상자
  - <Tabs>/<Tab title>, <Steps>/<Step title>, <Accordion title>, <Card title href> → 굵은 소제목
  - 그 밖의 대문자 JSX 컴포넌트 → 태그만 지우고 안쪽 내용 유지
  - 컴포넌트 안 들여쓰기 제거 (안 하면 본문이 코드 블록으로 보임)
  - 상대 경로 이미지 → 절대 경로
  - 코드 블록(```) 안은 절대 건드리지 않음
  - 파일 하나 = 장(H1) 하나, 본문 안의 H1 은 H2 로 내림
  - 하위 폴더가 바뀔 때마다 "폴더 구분 페이지" 를 넣어 PDF 목차에서 묶이게 함

사용 예
  python merge_mdx.py                                  # data/raw → data/merged (폴더 전부)
  python merge_mdx.py --raw data/raw --out data/merged
  python merge_mdx.py --only langchain mcp             # 일부 폴더만
  python merge_mdx.py --ext .mdx .md                   # .md 도 같이 합치기

요구 사항
  Python 3.10 이상, 외부 라이브러리 없음 (표준 라이브러리만 사용)
"""

# ---------------------------------------------------------------------------
# 표준 라이브러리
# ---------------------------------------------------------------------------
import argparse                     # 명령줄 옵션 처리
import html                         # 속성값 이스케이프
import re                           # 정규식: MDX 문법 정리
import textwrap                     # 들여쓰기 제거(dedent)
from pathlib import Path            # 파일 경로 처리 (Windows / Mac / Linux 호환)

# 안내 상자로 바꿀 컴포넌트 이름 → 상자 머리글
CALLOUTS = {
    "note": "참고", "info": "정보", "tip": "팁", "check": "확인",
    "warning": "주의", "caution": "주의", "danger": "위험", "important": "중요",
    "callout": "참고", "admonition": "참고",
}

# 태그는 지우되 title/label 속성을 굵은 소제목으로 남길 컴포넌트
TITLED = {"tab", "tabitem", "step", "accordion", "card", "expandable", "update", "details"}

# 2단계(md_to_pdf.py)가 이 표시를 보고 페이지를 나눔
PAGE_BREAK = '\n\n<div class="page-break"></div>\n\n'


# ---------------------------------------------------------------------------
# 1. 파일 순서: 폴더 트리를 위에서부터 (파일 먼저, 그다음 하위 폴더)
# ---------------------------------------------------------------------------
def natural_key(name: str):
    """'10-intro' 가 '2-setup' 보다 뒤에 오도록 숫자는 숫자로 비교."""
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", name.lower())]


def walk_files(folder: Path, exts: tuple[str, ...]) -> list[Path]:
    files = sorted((f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in exts),
                   key=lambda f: natural_key(f.name))
    subdirs = sorted((d for d in folder.iterdir() if d.is_dir()), key=lambda d: natural_key(d.name))
    for d in subdirs:
        files.extend(walk_files(d, exts))
    return files


# ---------------------------------------------------------------------------
# 2. frontmatter (PyYAML 없이 'key: value' 만 간단히)
# ---------------------------------------------------------------------------
FRONTMATTER_RE = re.compile(r"\A﻿?---\s*\n(.*?)\n---\s*\n", re.S)


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text.lstrip("﻿")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip("'\"")
    return meta, text[m.end():]


# ---------------------------------------------------------------------------
# 3. MDX → 일반 Markdown
# ---------------------------------------------------------------------------
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
ATTR_RE = re.compile(r'(\w+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|\{\s*["\'`]([^"\'`]*)["\'`]\s*\})')
# 대문자로 시작하는 JSX 컴포넌트 태그 (여는/닫는/자기 닫힘, 속성이 여러 줄이어도 잡음)
COMPONENT_RE = re.compile(r"<(/?)([A-Z][\w.]*)((?:\s+[^<>]*?)?)\s*(/?)>", re.S)


def attrs_of(attr_text: str) -> dict:
    return {m.group(1): next(g for g in m.groups()[1:] if g is not None)
            for m in ATTR_RE.finditer(attr_text or "")}


def split_code_blocks(text: str) -> list[tuple[bool, str]]:
    """코드 블록은 건드리면 안 되므로 [(코드인가?, 내용)] 조각으로 나눔."""
    chunks, buf, in_code, fence = [], [], False, ""
    for line in text.splitlines(keepends=True):
        m = FENCE_RE.match(line)
        if not in_code and m:
            if buf:
                chunks.append((False, "".join(buf)))
            buf, in_code, fence = [line], True, m.group(1)[0] * 3
        elif in_code and line.strip().startswith(fence) and line.strip().strip(fence[0]) == "":
            buf.append(line)
            chunks.append((True, "".join(buf)))
            buf, in_code = [], False
        else:
            buf.append(line)
    if buf:
        chunks.append((in_code, "".join(buf)))
    return chunks


def replace_component(m: re.Match) -> str:
    closing, name, attr_text = m.group(1), m.group(2), m.group(3)
    low = name.lower()
    attrs = attrs_of(attr_text)
    title = attrs.get("title") or attrs.get("label") or attrs.get("name") or ""

    if low in CALLOUTS:
        if closing:
            return "\n\n</div>\n\n"
        label = title or CALLOUTS[low]
        kind = attrs.get("type", low).lower()
        return (f'\n\n<div class="callout {html.escape(kind)}" markdown="1">\n\n'
                f'<p class="callout-label">{html.escape(label)}</p>\n\n')
    if low in TITLED:
        if closing:
            return "\n\n"
        href = attrs.get("href")
        head = f"[{title}]({href})" if (title and href) else title
        return f"\n\n**{head}**\n\n" if head else "\n\n"
    if low == "br":
        return "  \n"
    return "\n\n"                         # 나머지: 태그만 지우고 안쪽 내용 유지


def clean_prose(text: str) -> str:
    """코드 블록 바깥 부분만 정리."""
    text = re.sub(r"\{/\*.*?\*/\}", "", text, flags=re.S)          # {/* JSX 주석 */}
    # import / export (여러 줄 export 는 괄호가 닫힐 때까지 제거)
    out, skipping, depth = [], False, 0
    for line in text.splitlines(keepends=True):
        if not skipping and re.match(r"^(import\s.+from\s|import\s+['\"]|export\s)", line):
            depth = line.count("{") - line.count("}") + line.count("(") - line.count(")")
            skipping = depth > 0
            continue
        if skipping:
            depth += line.count("{") - line.count("}") + line.count("(") - line.count(")")
            skipping = depth > 0
            continue
        out.append(line)
    text = "".join(out)

    def admon(m):                                                  # Docusaurus  :::note 제목
        kind = m.group(1).lower()
        label = (m.group(2) or "").strip() or CALLOUTS.get(kind, kind)
        return (f'\n<div class="callout {kind}" markdown="1">\n\n'
                f'<p class="callout-label">{html.escape(label)}</p>\n\n')
    text = re.sub(r"^[ \t]*:::(\w+)[ \t]*(.*)$", admon, text, flags=re.M)
    text = re.sub(r"^[ \t]*:::[ \t]*$", "\n</div>\n", text, flags=re.M)

    text = COMPONENT_RE.sub(replace_component, text)               # JSX 컴포넌트
    text = re.sub(r"</?>", "", text)                               # <> </> 프래그먼트
    text = re.sub(r"\{\s*['\"]\s*['\"]\s*\}", " ", text)           # {' '}
    text = text.replace("className=", "class=")
    return text


def dedent_blocks(text: str) -> str:
    """빈 줄로 나뉜 덩어리마다 들여쓰기 제거. 단, 목록 아래 들여쓴 내용은 목록의 일부이므로 유지."""
    out, block = [], []

    def flush():
        if not block:
            return
        prev = next((l for l in reversed(out) if l.strip()), "")
        if re.match(r"^\s*([-*+]|\d+[.)])\s", prev) and block[0].startswith((" ", "\t")):
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


def fix_image_paths(text: str, base: Path) -> str:
    """상대 경로 이미지를 절대 경로(file://)로 → 합친 파일 위치가 달라도 이미지가 보임."""
    def md_img(m):
        alt, src = m.group(1), m.group(2).strip()
        if re.match(r"^(https?:|data:|file:|/)", src):
            return m.group(0)
        p = (base / src.split(" ")[0]).resolve()
        return f"![{alt}]({p.as_uri()})" if p.exists() else m.group(0)

    def html_img(m):
        src = m.group(2)
        if re.match(r"^(https?:|data:|file:|/)", src):
            return m.group(0)
        p = (base / src).resolve()
        return f"{m.group(1)}{p.as_uri()}{m.group(3)}" if p.exists() else m.group(0)

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", md_img, text)
    return re.sub(r'(<img[^>]*?src=["\'])([^"\']+)(["\'])', html_img, text)


def mdx_to_markdown(path: Path) -> tuple[str, str]:
    """파일 하나 → (제목, 정리된 Markdown)."""
    raw = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    meta, body = split_frontmatter(raw)

    body = "".join(chunk if is_code else clean_prose(chunk)
                   for is_code, chunk in split_code_blocks(body))
    body = dedent_blocks(body)
    body = fix_image_paths(body, path.parent)
    body = re.sub(r"^[ \t]+$", "", body, flags=re.M)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()

    # 제목: frontmatter title → 본문 첫 H1 → 파일 이름
    h1 = re.match(r"^#\s+(.+)$", body, re.M)
    title = meta.get("title") or (h1.group(1).strip() if h1 else path.stem)
    if h1:
        body = body[h1.end():].lstrip()
    # 본문 안의 다른 H1 → H2 (코드 블록 제외)
    body = "".join(chunk if is_code else re.sub(r"^# ", "## ", chunk, flags=re.M)
                   for is_code, chunk in split_code_blocks(body))
    return title, body


# ---------------------------------------------------------------------------
# 4. 한 폴더(langchain 등) → .md 1개
# ---------------------------------------------------------------------------
def merge_folder(folder: Path, out_path: Path, exts: tuple[str, ...]) -> int:
    files = walk_files(folder, exts)
    if not files:
        print(f"[건너뜀] {folder}: {'/'.join(exts)} 파일 없음")
        return 0

    sections, current_dir = [], None
    for f in files:
        rel = f.relative_to(folder)
        sub = rel.parent.as_posix()                       # 예: "errors", "docs/2026-07-28/learn"
        divider = ""
        if sub != current_dir:                            # 하위 폴더가 바뀌면 구분 페이지
            current_dir = sub
            label = folder.name if sub == "." else f"{folder.name} / {sub}"
            divider = f'<div class="folder-title">{html.escape(label)}</div>\n\n'
        title, body = mdx_to_markdown(f)
        sections.append(f"{divider}# {title}\n\n"
                        f'<p class="source">{html.escape(folder.name + "/" + rel.as_posix())}</p>\n\n'
                        f"{body}\n")

    header = (f"<!-- merged by merge_mdx.py | source: {folder.as_posix()} | files: {len(files)} -->\n"
              f"<!-- title: {folder.name} -->\n\n")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(header + PAGE_BREAK.join(sections), encoding="utf-8")
    print(f"[완료] {folder.name}: {len(files)}개 파일 → {out_path}")
    return len(files)


def main():
    ap = argparse.ArgumentParser(description="data/raw 의 폴더별 .mdx 를 .md 하나씩으로 병합")
    ap.add_argument("--raw", type=Path, default=Path("data/raw"), help="원본 루트 폴더 (기본 data/raw)")
    ap.add_argument("--out", type=Path, default=Path("data/merged"), help="병합 결과 폴더 (기본 data/merged)")
    ap.add_argument("--only", nargs="+", help="이 폴더들만 (예: --only langchain mcp)")
    ap.add_argument("--ext", nargs="+", default=[".mdx"], help="합칠 확장자 (기본 .mdx)")
    args = ap.parse_args()

    if not args.raw.is_dir():
        raise SystemExit(f"폴더가 없습니다: {args.raw}")
    exts = tuple(e if e.startswith(".") else "." + e for e in (x.lower() for x in args.ext))
    targets = sorted((d for d in args.raw.iterdir() if d.is_dir()), key=lambda d: natural_key(d.name))
    if args.only:
        targets = [d for d in targets if d.name in args.only]

    total = 0
    for folder in targets:
        total += merge_folder(folder, args.out / f"{folder.name}.md", exts)
    print(f"총 {total}개 파일 병합")


if __name__ == "__main__":
    main()
