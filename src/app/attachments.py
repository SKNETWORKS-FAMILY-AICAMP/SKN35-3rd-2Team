"""
입력창에 올린 글 파일(.py, .md, .txt, .log, .ipynb 등)을 질문 뒤에 붙일 글로 바꾼다.

- 글 파일은 텍스트로 읽고, 시각 자료(오류 화면, 구조도)는 기존 이미지 읽기를 쓴다 (두 갈래).
- PDF, 워드 같은 편집 문서는 아직 지원하지 않는다 (향후 계획).
- 읽은 글은 질문 뒤에 이런 모양으로 붙는다. 질문이 그대로 그래프(Supervisor, RAG, 답변)와 DB로 가기 때문에 다른 곳은 바꿀 필요가 없다.

      [첨부 파일: app.py]
      ```python
      (파일 내용)
      ```

- 파일 내용 안에 ``` 가 있으면(예: .md) 울타리를 더 길게 해서 안 깨지게 한다.
- 한 번에 3개, 파일당 300KB까지 받고, 글자가 많으면 앞의 10,000자만 쓴다 (모델 비용과 속도 때문).
- 모델과 DB로 가기 전에 API 키 같은 비밀값은 가린다 (src/db/masking.py, 알려진 패턴만).
- 화면은 저장된 질문 글에서 첨부 블록을 다시 찾아 접는 영역으로 보여 준다 (split_attachment_blocks).
"""

import json
import re

from src.db.masking import mask_secrets

IMAGE_EXTENSIONS = ("png", "jpg", "jpeg", "webp")
TEXT_EXTENSIONS = ("py", "md", "txt", "log", "json", "yaml", "yml", "toml", "ini", "cfg", "csv", "sql", "sh", "js", "ts", "ipynb")
# .env는 일부러 뺐다: API 키와 비밀번호가 들어 있는 파일이라 올리면 안 된다.

MAX_DOCUMENTS = 3
MAX_FILE_BYTES = 300_000
MAX_FILE_CHARS = 10_000
MAX_OUTPUT_CHARS = 2_000  # 노트북의 출력 한 건 (오류 메시지는 대부분 이 안에 들어온다)

FILE_ONLY_QUESTION = "첨부한 파일의 내용을 확인해 주세요. 오류나 문제가 보이면 원인과 해결 방법을 알려 주세요."
ATTACHMENT_ONLY_QUESTION = "첨부한 이미지와 파일의 내용을 확인해 주세요. 오류나 문제가 보이면 원인과 해결 방법을 알려 주세요."

_LANGUAGE = {"py": "python", "md": "markdown", "yml": "yaml", "js": "javascript", "ts": "typescript", "sh": "bash", "ipynb": "python"}
_ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
_BLOCK = re.compile(
    r"\[첨부 파일: (?P<name>[^\]\n]+)\]\n(?P<fence>`{3,})[^\n]*\n(?P<body>.*?)\n(?P=fence)(?=\n|$)", re.DOTALL
)


def extension(name):
    name = name or ""
    return name.rsplit(".", 1)[-1].lower() if "." in name else ""


def is_text_file(name):
    return extension(name) in TEXT_EXTENSIONS


def is_image_file(name):
    """이미지인지. 이름을 모르면(대역 파일 등) 이미지로 본다."""
    return not name or extension(name) in IMAGE_EXTENSIONS


def decode_text(data):
    """바이트를 글로 바꾼다 (UTF-8 먼저, 안 되면 한글 윈도우 인코딩). 바이너리면 ValueError."""
    if b"\x00" in data:
        raise ValueError("텍스트 파일이 아니에요.")
    for encoding in ("utf-8-sig", "cp949"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("글자를 읽을 수 없어요 (UTF-8 또는 한글 인코딩이 아니에요).")


def _join(source):
    return "".join(source) if isinstance(source, list) else (source if isinstance(source, str) else "")


def _clip(text, limit):
    return text if len(text) <= limit else text[:limit] + f"\n…(이하 {len(text) - limit}자 생략)"


def _outputs(outputs):
    parts = []
    for output in outputs if isinstance(outputs, list) else []:
        if not isinstance(output, dict):
            continue
        kind = output.get("output_type")
        if kind == "stream":
            text = _join(output.get("text"))
        elif kind == "error":
            trace = "\n".join(_ANSI.sub("", line) for line in output.get("traceback") or [] if isinstance(line, str))
            text = f"{output.get('ename', '')}: {output.get('evalue', '')}\n{trace}".strip()
        elif kind in ("execute_result", "display_data"):
            data = output.get("data") if isinstance(output.get("data"), dict) else {}
            text = _join(data.get("text/plain"))
            if not text and any(key.startswith("image/") for key in data):
                text = "(그림 출력은 생략했어요)"
        else:
            continue
        text = _ANSI.sub("", text).strip()
        if text:
            parts.append(_clip(text, MAX_OUTPUT_CHARS))
    return "\n".join(parts)


def notebook_to_text(raw):
    """Jupyter 노트북(.ipynb, nbformat 4)에서 셀의 코드, 글, 출력만 뽑는다. 그림(base64)과 메타데이터는 버린다."""
    try:
        notebook = json.loads(raw)
    except ValueError as error:
        raise ValueError("노트북(.ipynb) 형식이 올바르지 않아요.") from error
    cells = notebook.get("cells") if isinstance(notebook, dict) else None
    if not isinstance(cells, list):
        raise ValueError("지원하지 않는 노트북 형식이에요 (nbformat 4만 지원해요).")
    parts = []
    for number, cell in enumerate(cells, 1):
        if not isinstance(cell, dict):
            continue
        kind = cell.get("cell_type")
        label = {"code": "코드", "markdown": "마크다운"}.get(kind, "원문")
        source = _join(cell.get("source")).rstrip()
        if source.strip():
            parts.append(f"# [셀 {number} · {label}]\n{source}")
        if kind == "code":
            output = _outputs(cell.get("outputs"))
            if output:
                parts.append(f"# [셀 {number} · 출력]\n{output}")
    return "\n\n".join(parts)


def read_document(name, data):
    """파일 하나를 (글, 안내)로 바꾼다. 읽을 수 없으면 ValueError (사용자에게 그대로 보여 줄 수 있는 문장)."""
    if len(data) > MAX_FILE_BYTES:
        raise ValueError(f"{MAX_FILE_BYTES // 1000}KB를 넘어서 사용하지 않았어요.")
    text = decode_text(data)
    if extension(name) == "ipynb":
        text = notebook_to_text(text)
    if not text.strip():
        raise ValueError("내용이 비어 있어요.")
    notice = None
    if len(text) > MAX_FILE_CHARS:
        notice = f"글자가 많아 앞의 {MAX_FILE_CHARS:,}자만 사용했어요."
        text = text[:MAX_FILE_CHARS]
    return mask_secrets(text), notice


def _fence(text):
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


def _safe_name(name):
    name = (name or "파일").replace("\\", "/").rsplit("/", 1)[-1]
    return re.sub(r"[\]\[\r\n]", "_", name)[:80] or "파일"


def build_context(documents):
    """[(이름, 바이트)]를 질문 뒤에 붙일 글로 만든다. 돌려주는 값: (붙일 글, 사용자에게 보일 안내 목록)."""
    notices, blocks = [], []
    for name, data in documents[:MAX_DOCUMENTS]:
        label = _safe_name(name)
        try:
            text, notice = read_document(name, data)
        except ValueError as error:
            notices.append(f"{label}: {error}")
            continue
        if notice:
            notices.append(f"{label}: {notice}")
        fence = _fence(text)
        blocks.append(f"[첨부 파일: {label}]\n{fence}{_LANGUAGE.get(extension(name), extension(name))}\n{text}\n{fence}")
    if len(documents) > MAX_DOCUMENTS:
        notices.append(f"글 파일은 한 번에 {MAX_DOCUMENTS}개까지 보낼 수 있어서 앞의 {MAX_DOCUMENTS}개만 사용했어요.")
    return ("\n\n" + "\n\n".join(blocks)) if blocks else "", notices


def split_attachment_blocks(text):
    """질문 글에서 첨부 블록을 찾아 (블록을 뺀 글, [(파일 이름, 내용)])로 나눈다. 화면에서 접는 영역으로 보여 주려는 것."""
    files = [(m.group("name"), m.group("body")) for m in _BLOCK.finditer(text or "")]
    return _BLOCK.sub("", text or "").rstrip(), files
