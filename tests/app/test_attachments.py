"""입력창에 올린 글 파일(.py, .md, .ipynb 등)을 질문에 붙이는 부분 시험."""

import json
from types import SimpleNamespace

import pytest

from src.app import attachments as at
from src.app.chat import composer_documents, default_question, split_composer_value


def file(name, data):
    return SimpleNamespace(name=name, getvalue=lambda: data)


# ---------------------------------------------------------------- 형식 구분
def test_extensions_split_into_images_and_text():
    assert at.is_image_file("a.PNG") and at.is_image_file("shot.webp")
    assert at.is_text_file("app.py") and at.is_text_file("README.MD") and at.is_text_file("note.ipynb")
    assert not at.is_text_file("a.pdf") and not at.is_text_file("a.docx") and not at.is_text_file("secrets.env")
    assert at.is_image_file(None)  # 이름을 모르는 대역 파일은 이미지로 본다 (기존 시험과 호환)


def test_composer_splits_files_by_kind():
    value = SimpleNamespace(text="질문", files=[file("a.png", b"img"), file("main.py", b"print(1)"), file("n.md", b"# t")])
    text, images, notice = split_composer_value(value)
    assert text == "질문" and images == [b"img"] and notice is None
    assert composer_documents(value) == [("main.py", b"print(1)"), ("n.md", b"# t")]
    assert composer_documents("글만") == [] and composer_documents(None) == []


# ---------------------------------------------------------------- 읽기
def test_utf8_and_korean_windows_encoding_are_read():
    assert at.decode_text("한글 ok".encode("utf-8")) == "한글 ok"
    assert at.decode_text("한글 ok".encode("utf-8-sig")) == "한글 ok"
    assert at.decode_text("한글 ok".encode("cp949")) == "한글 ok"


def test_binary_file_is_rejected():
    with pytest.raises(ValueError, match="텍스트 파일이 아니에요"):
        at.decode_text(b"\x89PNG\x00\x00binary")


def test_context_block_has_name_language_and_content():
    context, notices = at.build_context([("app.py", b"print('hi')")])
    assert notices == []
    assert context == "\n\n[첨부 파일: app.py]\n```python\nprint('hi')\n```"


def test_fence_is_longer_when_the_file_contains_backticks():
    body = "# 제목\n```python\nprint(1)\n```\n"
    context, _ = at.build_context([("guide.md", body.encode())])
    assert "````markdown" in context
    clean, files = at.split_attachment_blocks("질문" + context)
    assert clean == "질문" and files == [("guide.md", body)]  # 파일 내용이 한 글자도 안 바뀐다


def test_secrets_are_masked_before_the_text_goes_anywhere():
    key = "sk-" + "A1b2C3d4" * 6
    context, _ = at.build_context([("cfg.py", f"API_KEY = '{key}'".encode())])
    assert key not in context and "[MASKED" in context


def test_long_file_is_clipped_and_reported():
    context, notices = at.build_context([("big.log", ("line of log\n" * 2000).encode())])
    assert len(context) < at.MAX_FILE_CHARS + 200
    assert notices and "big.log" in notices[0] and "10,000자" in notices[0]


def test_oversize_empty_and_broken_files_give_notices_not_errors():
    big = b"x" * (at.MAX_FILE_BYTES + 1)
    context, notices = at.build_context([("big.txt", big), ("empty.py", b"  \n"), ("bin.py", b"\x00\x01")])
    assert context == "" and len(notices) == 3
    assert "300KB" in notices[0] and "비어" in notices[1] and "텍스트 파일이 아니에요" in notices[2]


def test_only_three_documents_are_used():
    docs = [(f"f{i}.py", b"x = 1") for i in range(5)]
    context, notices = at.build_context(docs)
    assert context.count("[첨부 파일:") == 3 and "3개까지" in notices[-1]


def test_file_name_cannot_break_the_block_format():
    context, _ = at.build_context([("a]\n[첨부 파일: b.py", b"x = 1")])
    clean, files = at.split_attachment_blocks(context)
    assert len(files) == 1 and "\n" not in files[0][0] and "]" not in files[0][0]


def test_split_returns_text_unchanged_without_blocks():
    assert at.split_attachment_blocks("그냥 질문") == ("그냥 질문", [])
    assert at.split_attachment_blocks("") == ("", [])


# ---------------------------------------------------------------- 노트북
def notebook(cells, **extra):
    return json.dumps({"nbformat": 4, "nbformat_minor": 5, "metadata": {"kernelspec": {"language": "python"}}, "cells": cells, **extra})


def test_notebook_keeps_code_markdown_and_error_output_but_drops_images():
    nb = notebook([
        {"cell_type": "markdown", "source": ["# 실험\n", "설명"]},
        {"cell_type": "code", "source": "import langgraph\nprint(langgraph.__version__)", "outputs": [
            {"output_type": "stream", "name": "stdout", "text": ["0.6.4\n"]},
            {"output_type": "display_data", "data": {"image/png": "AAAA" * 5000, "text/plain": "<Figure size 640x480>"}},
        ]},
        {"cell_type": "code", "source": "graph.invoke({})", "outputs": [
            {"output_type": "error", "ename": "GraphRecursionError", "evalue": "Recursion limit of 25 reached",
             "traceback": ["\x1b[0;31m---------------\x1b[0m", "GraphRecursionError: Recursion limit of 25 reached"]},
        ]},
    ])
    text = at.notebook_to_text(nb)
    assert "# [셀 1 · 마크다운]" in text and "import langgraph" in text and "0.6.4" in text
    assert "GraphRecursionError: Recursion limit of 25 reached" in text
    assert "\x1b[" not in text  # 색상 제어 문자는 뺀다
    assert "AAAA" not in text   # 그림(base64)은 버린다
    assert len(text) < 1000


def test_notebook_goes_through_the_same_attachment_path():
    nb = notebook([{"cell_type": "code", "source": "1/0", "outputs": [{"output_type": "error", "ename": "ZeroDivisionError", "evalue": "division by zero", "traceback": []}]}])
    context, notices = at.build_context([("lab.ipynb", nb.encode())])
    assert notices == [] and "ZeroDivisionError: division by zero" in context and "```python" in context


@pytest.mark.parametrize("raw, message", [("not json", "형식이 올바르지"), ('{"worksheets": []}', "nbformat 4"), ("[]", "nbformat 4")])
def test_broken_or_old_notebooks_are_reported(raw, message):
    context, notices = at.build_context([("x.ipynb", raw.encode())])
    assert context == "" and message in notices[0]


# ---------------------------------------------------------------- 기본 질문
def test_default_question_depends_on_what_was_attached():
    assert default_question([b"i"], False) != at.FILE_ONLY_QUESTION
    assert default_question([], True) == at.FILE_ONLY_QUESTION
    assert default_question([b"i"], True) == at.ATTACHMENT_ONLY_QUESTION
    assert "문제가 있다" not in at.FILE_ONLY_QUESTION  # 문제가 있다고 단정하지 않는다
