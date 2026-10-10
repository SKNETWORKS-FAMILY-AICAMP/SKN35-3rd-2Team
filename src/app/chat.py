"""Figma chat UI; model and DB contracts stay in chat_service."""
from copy import deepcopy
from datetime import datetime, timezone
from html import escape
from uuid import uuid4

import streamlit as st

from src import db

from src.const.config import OPEN_MODEL
from src.app.chat_service import chat_result, run_chat, run_db_chat, text_content
from src.prompt.chat_prompt import CHAT_SYSTEM_PROMPT


# Figma's small SVG assets are embedded below when installing this UI, so only
# chat.py changes and no temporary asset URLs or new asset files are needed.
FIGMA_ICONS = {'terminal': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiB2aWV3Qm94PSIwIDAgMjAgMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJ0ZXJtaW5hbCI+CjxwYXRoIGlkPSJWZWN0b3IiIGQ9Ik0xMCAxNS44MzRIMTYuNjY2TTMuMzM0IDE0LjE2NzFMOC4zMzM1IDkuMTY2NTdMMy4zMzQgNC4xNjYiIHN0cm9rZS13aWR0aD0iMS43IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZT0id2hpdGUiLz4KPC9nPgo8L3N2Zz4K', 'panel': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiB2aWV3Qm94PSIwIDAgMTggMTgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJwYW5lbC1sZWZ0Ij4KPHBhdGggaWQ9IlZlY3RvciIgZD0iTTYuNzUgMi4yNVYxNS43NU02Ljc1IDIuMjVIMy43NUMyLjkyMTU3IDIuMjUgMi4yNSAyLjkyMTU3IDIuMjUgMy43NVYxNC4yNUMyLjI1IDE1LjA3ODQgMi45MjE1NyAxNS43NSAzLjc1IDE1Ljc1SDYuNzVNNi43NSAyLjI1SDE0LjI1QzE1LjA3ODQgMi4yNSAxNS43NSAyLjkyMTU3IDE1Ljc1IDMuNzVWMTQuMjVDMTUuNzUgMTUuMDc4NCAxNS4wNzg0IDE1Ljc1IDE0LjI1IDE1Ljc1SDYuNzUiIHN0cm9rZS13aWR0aD0iMS43IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZT0iIzY0NzQ4QiIvPgo8L2c+Cjwvc3ZnPgo=', 'workflow': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiB2aWV3Qm94PSIwIDAgMTggMTgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJ3b3JrZmxvdyI+CjxwYXRoIGlkPSJWZWN0b3IiIGQ9Ik01LjI1IDguMjVWMTEuMjVDNS4yNSAxMS42NDc4IDUuNDA4MDQgMTIuMDI5NCA1LjY4OTM0IDEyLjMxMDdDNS45NzA2NCAxMi41OTIgNi4zNTIxOCAxMi43NSA2Ljc1IDEyLjc1SDkuNzVNNS4yNSA4LjI1SDYuNzVDNy41Nzg0MyA4LjI1IDguMjUgNy41Nzg0MyA4LjI1IDYuNzVWMy43NUM4LjI1IDIuOTIxNTcgNy41Nzg0MyAyLjI1IDYuNzUgMi4yNUgzLjc1QzIuOTIxNTcgMi4yNSAyLjI1IDIuOTIxNTcgMi4yNSAzLjc1VjYuNzVDMi4yNSA3LjU3ODQzIDIuOTIxNTcgOC4yNSAzLjc1IDguMjVINS4yNVpNOS43NSAxMi43NVYxNC4yNUM5Ljc1IDE1LjA3ODQgMTAuNDIxNiAxNS43NSAxMS4yNSAxNS43NUgxNC4yNUMxNS4wNzg0IDE1Ljc1IDE1Ljc1IDE1LjA3ODQgMTUuNzUgMTQuMjVWMTEuMjVDMTUuNzUgMTAuNDIxNiAxNS4wNzg0IDkuNzUgMTQuMjUgOS43NUgxMS4yNUMxMC40MjE2IDkuNzUgOS43NSAxMC40MjE2IDkuNzUgMTEuMjVWMTIuNzVaIiBzdHJva2Utd2lkdGg9IjEuNyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2U9IiM2NDc0OEIiLz4KPC9nPgo8L3N2Zz4K', 'code': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiB2aWV3Qm94PSIwIDAgMTggMTgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJjb2RlLXhtbCI+CjxwYXRoIGlkPSJWZWN0b3IiIGQ9Ik0xMy41MDA0IDExLjk5OTdMMTYuNTAwNiA5TDEzLjUwMDQgNi4wMDAzTTQuNDk5NjQgNi4wMDAzTDEuNDk5NCA5TDQuNDk5NjQgMTEuOTk5N00xMC44NzUxIDMuMDAwNkw3LjEyNDg1IDE0Ljk5OTQiIHN0cm9rZS13aWR0aD0iMS43IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZT0iIzY0NzQ4QiIvPgo8L2c+Cjwvc3ZnPgo=', 'plug': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiB2aWV3Qm94PSIwIDAgMTggMTgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJwbHVnIj4KPHBhdGggaWQ9IlZlY3RvciIgZD0iTTkgMTYuNTAwNlYxMi43NTAzTTkgMTIuNzUwM0gxMC41QzExLjI5NTYgMTIuNzUwMyAxMi4wNTg3IDEyLjQzNDIgMTIuNjIxMyAxMS44NzE1QzEzLjE4MzkgMTEuMzA4OSAxMy41IDEwLjU0NTggMTMuNSA5Ljc1MDA2VjYuNzQ5ODJDMTMuNSA2LjU1MDg5IDEzLjQyMSA2LjM2MDExIDEzLjI4MDMgNi4yMTk0NUMxMy4xMzk3IDYuMDc4NzggMTIuOTQ4OSA1Ljk5OTc2IDEyLjc1IDUuOTk5NzZIMTEuMjVNOSAxMi43NTAzSDcuNUM2LjcwNDM1IDEyLjc1MDMgNS45NDEyOSAxMi40MzQyIDUuMzc4NjggMTEuODcxNUM0LjgxNjA3IDExLjMwODkgNC41IDEwLjU0NTggNC41IDkuNzUwMDZWNi43NDk4MkM0LjUgNi41NTA4OSA0LjU3OTAyIDYuMzYwMTEgNC43MTk2NyA2LjIxOTQ1QzQuODYwMzIgNi4wNzg3OCA1LjA1MTA5IDUuOTk5NzYgNS4yNSA1Ljk5OTc2SDYuNzVNMTEuMjUgNS45OTk3NlYxLjQ5OTRNMTEuMjUgNS45OTk3Nkg2Ljc1TTYuNzUgNS45OTk3NlYxLjQ5OTQiIHN0cm9rZS13aWR0aD0iMS43IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZT0iIzY0NzQ4QiIvPgo8L2c+Cjwvc3ZnPgo=', 'assistant': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2IiB2aWV3Qm94PSIwIDAgMTYgMTYiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJ0ZXJtaW5hbCI+CjxwYXRoIGlkPSJWZWN0b3IiIGQ9Ik04IDEyLjY2NzJIMTMuMzMyOE0yLjY2NzIgMTEuMzMzN0w2LjY2NjggNy4zMzMyNkwyLjY2NzIgMy4zMzI4IiBzdHJva2Utd2lkdGg9IjEuNyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2U9IiM0RjQ2RTUiLz4KPC9nPgo8L3N2Zz4K'}

STYLE = """
<style>
:root {--ui-bg:#F8FAFC;--ui-panel:#F1F5F9;--ui-border:#E2E8F0;
 --ui-ink:#1E293B;--ui-muted:#64748B;--ui-accent:#4F46E5;}
[data-testid="stAppViewContainer"], [data-testid="stMain"] {background:var(--ui-bg);color:var(--ui-ink);}
[data-testid="stSidebar"] {background:var(--ui-panel);border-right:1px solid var(--ui-border);}
[data-testid="stSidebar"] p {color:var(--ui-ink);}
[data-testid="stMainBlockContainer"] {max-width:904px;padding:4rem 2rem 340px;}
[data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {gap:12px;}
.stApp, .stApp input, .stApp textarea, .stApp button {font-family:Pretendard,"Noto Sans KR","Malgun Gothic",sans-serif;}
.stApp h1,.stApp h2,.stApp h3 {color:var(--ui-ink);letter-spacing:-.035em;}
.stApp [data-testid="stCaptionContainer"] {color:var(--ui-muted);}
.stApp [data-testid="stButton"] button, .stApp [data-testid="stDownloadButton"] button {border:1px solid var(--ui-border);border-radius:12px;background:white;color:var(--ui-ink);}
.stApp [data-testid="stButton"] button[kind="primary"] {background:var(--ui-accent);color:white;border-color:var(--ui-accent);}
.stApp [data-testid="stButton"] button:hover {border-color:var(--ui-accent);}
.stApp [data-testid="stTextInput"] input,.stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div {background:white;color:var(--ui-ink);border-color:var(--ui-border);border-radius:12px;}
.stApp [data-testid="stExpander"] {background:white;border:1px solid var(--ui-border);border-radius:12px;}
.stApp [data-testid="stVerticalBlockBorderWrapper"] {border-color:var(--ui-border);border-radius:16px;}
.ui-brand {display:flex;align-items:center;gap:10px;font-weight:700;font-size:18px;color:var(--ui-ink);}
.ui-logo {background:var(--ui-accent);width:32px;height:32px;border-radius:12px;display:flex;align-items:center;justify-content:center;}
.ui-header {display:flex;justify-content:space-between;align-items:center;gap:12px;padding:4px 0 18px;border-bottom:1px solid var(--ui-border);color:var(--ui-ink);}
.ui-header-title {display:flex;align-items:center;gap:12px;font-weight:500;min-width:0;overflow-wrap:anywhere;}
.ui-header span {font-size:12px;color:var(--ui-muted);white-space:nowrap;}
.ui-welcome {text-align:center;margin:8px 0 16px;}
.ui-welcome h1 {font-size:32px;font-weight:700;line-height:1.4;margin:0 0 16px;}
.ui-welcome p {color:var(--ui-muted);font-size:16px;line-height:1.5;}
.ui-tags {display:flex;gap:8px;justify-content:center;margin-top:16px;}
.ui-tag {background:#EEF2FF;color:var(--ui-accent);padding:4px 10px;border-radius:12px;font-size:12px;}
.ui-tech {display:flex;justify-content:space-between;align-items:center;color:var(--ui-accent);font-size:12px;margin-bottom:8px;}
.ui-user {display:flex;justify-content:flex-end;margin:12px 0 24px;}
.ui-user pre {font:inherit;white-space:pre-wrap;overflow-wrap:anywhere;max-width:90%;margin:0;background:var(--ui-panel);color:var(--ui-ink);padding:12px 20px;border-radius:16px;line-height:1.6;}
.ui-assistant {display:flex;align-items:center;gap:8px;font-weight:700;font-size:14px;margin-bottom:12px;color:var(--ui-ink);}
.ui-assistant-icon {background:#EEF2FF;border-radius:8px;width:24px;height:24px;display:flex;align-items:center;justify-content:center;}
.ui-assistant span {font-size:12px;font-weight:400;color:var(--ui-muted);}
.st-key-composer [data-testid="stChatInput"] {background:white;border:1px solid var(--ui-border);border-radius:24px;}
.st-key-composer [data-testid="stChatInput"] textarea {background:white;color:var(--ui-ink);}
.st-key-composer [data-testid="stChatInputSubmitButton"] {background:var(--ui-accent);color:white;border-radius:12px;}
.st-key-composer [data-testid="stVerticalBlock"] {gap:8px;}
.st-key-example_0 [data-testid="stVerticalBlock"],.st-key-example_1 [data-testid="stVerticalBlock"],.st-key-example_2 [data-testid="stVerticalBlock"] {gap:8px;}
[data-testid="stSidebar"] button[kind="primary"] p {color:white;}
[data-testid="stBottomBlockContainer"] {max-width:904px;margin:auto;padding:8px 2rem 16px;}
[data-testid="stBottom"] {background:var(--ui-bg);}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li {line-height:1.65;overflow-wrap:anywhere;}
.stApp pre {overflow-x:auto;}
.st-key-example_0,.st-key-example_1,.st-key-example_2 {background:white;border-radius:16px;gap:8px!important;}
.st-key-composer [data-testid="stChatInput"] > div {background:white;}
[data-testid="stSelectbox"] [role="group"] {background:white;color:var(--ui-ink);border-color:var(--ui-border);border-radius:12px;}
.st-key-preview_body h3 {font-size:20px;}
@media(max-width:640px) {
 [data-testid="stMainBlockContainer"],[data-testid="stBottomBlockContainer"] {padding-left:16px;padding-right:16px;}
 .ui-welcome {margin-top:36px;}.ui-welcome h1 {font-size:26px;}.ui-user pre {max-width:100%;}
}

.st-key-composer_box {position:relative;background:#FFFFFF;border:1px solid var(--ui-border);
 border-radius:24px;padding:12px 16px!important;gap:4px!important;}
.st-key-composer_box [data-testid="stChatInput"] {position:static!important;background:transparent!important;
 border:none!important;border-radius:0!important;min-height:43px!important;}
.st-key-composer_box [data-testid="stChatInput"] > div {position:static!important;background:transparent!important;
 border:none!important;box-shadow:none!important;}
.st-key-composer_box [data-testid="stChatInput"] textarea {background:transparent!important;}
.st-key-composer_box [data-testid="stChatInputSubmitButton"] {position:absolute!important;right:16px;bottom:12px;
 width:36px;height:36px;border-radius:12px;}
.ui-composer-tools {display:flex;justify-content:space-between;align-items:center;min-height:36px;
 padding-right:52px;gap:12px;font-size:12px;color:var(--ui-muted);}
.ui-attachment-icon {font-size:18px;margin-right:6px;vertical-align:middle;}
.ui-shortcut {white-space:nowrap;}
.st-key-composer > [data-testid="stExpander"] {background:transparent;border:none;}
@media(max-width:480px) {.ui-shortcut {font-size:10px;}.ui-composer-tools {gap:4px;font-size:11px;}}


.st-key-composer_box [data-testid="stChatInput"] * {position:static!important;}
.st-key-composer_box [data-testid="stChatInputSubmitButton"] {position:absolute!important;right:16px;bottom:12px;}
.st-key-composer_tools {padding-right:52px;gap:8px!important;align-items:center;min-height:36px;}
.st-key-composer_tools [data-testid="stButton"] button {border:none!important;background:transparent!important;
 padding:0!important;min-height:36px;color:var(--ui-muted);}
.st-key-composer_tools [data-testid="stButton"] button p {font-size:12px;}
.st-key-composer_tools [data-testid="stCaptionContainer"] {font-size:12px;white-space:nowrap;}
.st-key-composer [data-testid="stExpander"]:not(.st-key-composer_box *) {background:transparent;border:none;}
@media(max-width:480px) {.st-key-composer_tools [data-testid="stCaptionContainer"] {font-size:10px;}}

.st-key-composer_box [data-testid="stElementContainer"]:has([data-testid="stChatInput"]) {position:static!important;}

/* Compact initial height; long input can still grow within a bounded area. */
.st-key-composer_box {padding:6px 12px!important;border-radius:18px;gap:0!important;}
.st-key-composer_box [data-testid="stChatInput"] {min-height:28px!important;height:auto!important;}
.st-key-composer_box [data-testid="stChatInput"] > div {min-height:28px!important;}
.st-key-composer_box [data-testid="stChatInput"] textarea {min-height:28px!important;height:28px;
 max-height:120px!important;padding-top:2px!important;padding-bottom:2px!important;line-height:24px;}
.st-key-composer_tools {min-height:24px!important;height:24px;gap:0!important;padding-right:44px;}
.st-key-composer_tools [data-testid="stButton"] button {min-height:24px!important;height:24px;padding:0!important;}
.st-key-composer_tools [data-testid="stButton"] button p {font-size:11px;}
.st-key-composer_tools [data-testid="stCaptionContainer"] {font-size:11px;}
.st-key-composer_box [data-testid="stChatInputSubmitButton"] {width:30px;height:30px;right:12px;bottom:6px;border-radius:10px;}

.st-key-composer_box {height:68px!important;min-height:68px!important;overflow:hidden;}
.st-key-composer_box [data-testid="stChatInput"] {height:30px!important;min-height:30px!important;}
.st-key-composer_box [data-testid="stChatInput"] div {padding-top:0!important;padding-bottom:0!important;min-height:0!important;}
.st-key-composer_box [data-testid="stChatInput"] textarea {height:28px!important;max-height:28px!important;overflow-y:auto!important;}
.st-key-composer_tools {position:absolute!important;left:12px;right:52px;bottom:3px;padding-right:0!important;width:auto!important;justify-content:space-between!important;}
</style>
"""

EXAMPLES = (
    ("LangGraph", "LangGraph State 전달 오류", "Node의 변경 사항이 다음 Node에 전달되지 않아요.", "workflow"),
    ("LangChain", "LangChain API 변경", "기존 코드에서 import 오류가 발생해요.", "code"),
    ("MCP", "MCP 서버 연결 오류", "서버를 실행했는데 클라이언트가 연결되지 않아요.", "plug"),
)


def icon(name, size=18):
    uri = FIGMA_ICONS.get(name)
    return f'<img src="{uri}" alt="" width="{size}" height="{size}">' if uri else ""


@st.cache_resource
def get_model():
    from src.const.config import NVIDIA_API_KEY, NVIDIA_MODEL
    from src.const.models import create_nvidia_model
    if not NVIDIA_API_KEY or not NVIDIA_MODEL:
        raise ValueError("NVIDIA 설정이 필요합니다.")
    return create_nvidia_model(timeout=60)


def generate_answer(messages, mode, *, user_id=None, conversation_id=None):
    if mode == "연습 모드":
        return chat_result(
            f"입력한 질문: {messages[-1]['content']}\n\n"
            "질문을 정상적으로 받았습니다. 화면 동작을 확인하는 연습 모드입니다."
        )
    if mode == "OpenAI AI 답변":
        if user_id is not None:
            return run_db_chat(messages[-1]["content"], user_id=user_id, conversation_id=conversation_id)
        return run_chat(messages)
    if mode != "NVIDIA AI 답변":
        return chat_result(status="error", code="INVALID_MODE", message="답변 모드를 확인해 주세요.")
    try:
        response = get_model().invoke(
            [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
            + [{"role": m["role"], "content": m["content"]} for m in messages]
        )
        answer = text_content(response.content)
        if not answer:
            raise ValueError("빈 응답")
        return chat_result(answer)
    except Exception:
        return chat_result(status="error", code="MODEL_ERROR", message=
            "답변을 받지 못했습니다. NVIDIA 설정과 인터넷 연결을 확인해 주세요.")


def render_sources(sources):
    if not sources:
        return
    with st.expander("참고 근거", icon=":material/library_books:"):
        for index, source in enumerate(sources, 1):
            with st.container(border=True):
                st.markdown(f"**[{index}] {source.get('title') or '참고 문서'}**")
                types = {"docs": "공식 문서", "documentation": "공식 문서",
                         "repository": "공식 저장소", "issue": "GitHub Issue · 의견", "example": "공식 예제"}
                metadata = [source.get("tech"), types.get(source.get("doc_type"), source.get("doc_type")),
                            f"버전 {source['version']}" if source.get("version") else None,
                            source.get("updated_at")]
                st.caption(" · ".join(str(value) for value in metadata if value) or "자료 유형 미확인")
                url = source.get("url", "")
                if isinstance(url, str) and url.startswith(("https://", "http://")):
                    st.link_button("원문 보기", url, icon=":material/open_in_new:")
                else:
                    st.caption("원문 링크 미등록")


def reset_conversation():
    st.session_state.messages = []
    st.session_state.conversation_id = None
    st.session_state.ui_thread = str(uuid4())
    st.session_state.ui_failure = None
    st.session_state.chat_input = ""


def clear_account_view():
    """Remove the previous account's view and draft before switching identity."""
    reset_conversation()
    st.session_state.ui_history = {}
    st.session_state.ui_db_notice = None
    for key in list(st.session_state):
        if key.startswith(("env_", "feedback_", "auth_")):
            del st.session_state[key]
    st.session_state.history_search = ""


def logout():
    clear_account_view()
    st.session_state.pop("user_id", None)
    st.session_state.pop("username", None)
    st.session_state.ui_owner = None
    st.session_state.ui_auth_open = False


def load_saved_conversation(conversation_id):
    """Read only the authenticated owner's messages; detach all ORM values."""
    owner = st.session_state.get("user_id")
    if owner is None:
        return False
    try:
        with db.db_session() as session:
            rows = db.list_messages(session, conversation_id, owner)
            messages = [{"role": row.role, "content": row.content or "",
                         "sources": [{name: getattr(source, name) for name in
                                      ("url", "title", "tech", "version", "doc_type", "snippet", "score", "is_grounded")}
                                     for source in sorted(row.sources, key=lambda source: source.rank)]}
                        for row in rows]
        st.session_state.messages = messages
        st.session_state.conversation_id = conversation_id
        st.session_state.ui_thread = f"db_{conversation_id}"
        st.session_state.ui_failure = None
        st.session_state.ui_db_notice = None
        return True
    except Exception:
        st.session_state.ui_db_notice = "대화를 불러오지 못했습니다. DB 연결과 접근 권한을 확인해 주세요."
        return False


def render_saved_history(query):
    try:
        with db.db_session() as session:
            items = [{"id": row.id, "title": row.title or "새 대화"}
                     for row in db.list_conversations(session, st.session_state.user_id, limit=100)]
    except Exception:
        st.warning("대화 목록을 불러오지 못했습니다. DB 연결 상태를 확인해 주세요.")
        return
    visible = [item for item in items if query.casefold() in item["title"].casefold()]
    st.caption("저장된 대화 · 최근 100개")
    if not visible:
        st.caption("아직 저장된 대화가 없어요." if not query else "검색 결과가 없어요.")
    for item in visible:
        if st.button(item["title"], key=f"saved_history_{item['id']}",
                     icon=":material/chat_bubble_outline:", width="stretch"):
            if load_saved_conversation(item["id"]):
                st.session_state.answer_mode = "OpenAI AI 답변"
                st.session_state.previous_mode = "OpenAI AI 답변"
                st.session_state.ui_preview = "실제 채팅"
                st.session_state.chat_input = ""
                st.rerun()


def render_authentication():
    if st.session_state.get("user_id") is not None:
        st.markdown(f"**{escape(st.session_state.get('username', '사용자'))}**")
        st.caption("OpenAI 대화는 계정에 저장됩니다. 연습·NVIDIA 모드는 현재 접속에서만 유지됩니다.")
        st.button("로그아웃", key="logout", icon=":material/logout:",
                  width="stretch", on_click=logout)
        return
    st.markdown("**게스트**")
    st.caption("로그인하면 저장된 대화를 다시 열어 이어서 질문할 수 있습니다. 게스트 대화는 계정으로 이전되지 않습니다.")
    if st.button("로그인 / 회원가입", key="login_open", icon=":material/login:", width="stretch"):
        st.session_state.ui_auth_open = not st.session_state.get("ui_auth_open", False)
    if not st.session_state.get("ui_auth_open"):
        return
    with st.expander("계정 로그인", expanded=True):
        action = st.radio("계정 메뉴", ["로그인", "회원가입"], key="auth_action", horizontal=True)
        st.caption("아이디: 영문 소문자·숫자·밑줄 3~30자 / 비밀번호: 8자 이상")
        with st.form("account_form", clear_on_submit=True):
            username = st.text_input("아이디", key="auth_username", max_chars=30)
            password = st.text_input("비밀번호", type="password", key="auth_password")
            confirmation = st.text_input("비밀번호 확인", type="password", key="auth_confirmation") if action == "회원가입" else None
            submitted = st.form_submit_button(action, type="primary", width="stretch")
        if submitted:
            if not username.strip() or not password:
                st.error("아이디와 비밀번호를 입력해 주세요.")
                return
            if action == "회원가입" and password != confirmation:
                st.error("비밀번호 확인이 일치하지 않습니다.")
                return
            try:
                with db.db_session() as session:
                    if action == "회원가입":
                        db.create_user(session, username, password, is_admin=False)
                        identity = None
                    else:
                        user = db.authenticate(session, username, password)
                        identity = {"id": user.id, "username": user.username} if user else None
            except db.UsernameTakenError:
                st.error("이미 사용 중인 아이디입니다.")
                return
            except ValueError:
                st.error("아이디 형식과 비밀번호 길이를 확인해 주세요.")
                return
            except Exception:
                st.error("계정 정보를 확인하지 못했습니다. DB 연결과 테이블 준비 상태를 확인해 주세요.")
                return
            if action == "회원가입":
                st.success("회원가입이 완료되었습니다. 로그인 메뉴에서 로그인해 주세요.")
            elif identity is None:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
            else:
                # Widget keys are cleared by the form; preserve no password in identity.
                reset_conversation()
                st.session_state.ui_history = {}
                for key in list(st.session_state):
                    if key.startswith(("env_", "feedback_")):
                        del st.session_state[key]
                st.session_state.user_id = identity["id"]
                st.session_state.username = identity["username"]
                st.session_state.ui_owner = identity["id"]
                st.session_state.ui_db_notice = None
                st.session_state.ui_auth_open = False
                st.rerun()
        st.caption("로그인은 현재 브라우저 접속 동안 유지됩니다. 새로고침 후에는 다시 로그인할 수 있습니다.")


def remember_conversation(mode):
    if not st.session_state.messages or (mode == "OpenAI AI 답변" and st.session_state.get("user_id") is not None):
        return
    thread = st.session_state.ui_thread
    existing = st.session_state.ui_history.get(thread, {})
    st.session_state.ui_history[thread] = {
        "title": st.session_state.messages[0].get("display_content", st.session_state.messages[0]["content"])[:34],
        "messages": deepcopy(st.session_state.messages), "mode": mode,
        "conversation_id": st.session_state.get("conversation_id"),
        "updated": datetime.now(timezone.utc),
    }
    # Bound temporary conversations; account history is read from the DB.
    if not existing and len(st.session_state.ui_history) > 30:
        oldest = min(st.session_state.ui_history, key=lambda key: st.session_state.ui_history[key]["updated"])
        del st.session_state.ui_history[oldest]


def render_sidebar():
    with st.sidebar:
        st.html(f'<div class="ui-brand"><div class="ui-logo">{icon("terminal",20)}</div>AI 개발 도우미</div>')
        st.caption("LLM/RAG 개발 오류 분석 및 해결 도우미")
        st.button("새 대화", icon=":material/add:", type="primary", width="stretch",
                  key="new_chat", on_click=reset_conversation)
        query = st.text_input("대화 검색", placeholder="대화 검색", key="history_search", label_visibility="collapsed")
        if st.session_state.get("user_id") is not None:
            render_saved_history(query)
        st.caption("현재 접속의 임시 대화" if st.session_state.get("user_id") is not None else "현재 접속의 대화")
        items = sorted(st.session_state.ui_history.items(), key=lambda item: item[1]["updated"], reverse=True)
        visible = [(key, item) for key, item in items if query.casefold() in item["title"].casefold()]
        if not visible:
            st.caption("아직 대화가 없어요." if not query else "검색 결과가 없어요.")
        for key, item in visible:
            if st.button(item["title"], key=f"history_{key}", icon=":material/chat_bubble_outline:", width="stretch"):
                st.session_state.messages = deepcopy(item["messages"])
                st.session_state.conversation_id = item["conversation_id"]
                st.session_state.ui_thread = key
                st.session_state.ui_failure = None
                st.session_state.answer_mode = item["mode"]
                st.session_state.previous_mode = item["mode"]
                st.rerun()
        st.space(24)
        with st.expander("대화 설정", icon=":material/tune:"):
            mode = st.selectbox("답변 모드", ["OpenAI AI 답변", "연습 모드", "NVIDIA AI 답변"], key="answer_mode")
            if mode == "OpenAI AI 답변":
                st.caption(f"모델: {OPEN_MODEL}")
            if st.session_state.get("previous_mode", mode) != mode:
                reset_conversation()
            st.session_state.previous_mode = mode
            st.caption("모드를 바꾸면 새 대화를 시작합니다.")
        with st.expander("디자인 미리보기", icon=":material/visibility:"):
            st.selectbox("시안 화면", ["실제 채팅", "오류 분석 예시", "추가 정보 요청 예시"], key="ui_preview")
            st.caption("예시 화면은 API를 호출하거나 대화를 저장하지 않습니다.")
        with st.expander("현재 사용할 수 있는 기능"):
            st.markdown("- 일반 질문과 후속 질문\n- 연습 모드: API 호출 없이 화면 확인\n- 문서 검색·외부 조회·이미지 분석: 준비 중")
        st.space(24)
        render_authentication()
        return mode


def render_welcome():
    st.html('''<section class="ui-welcome"><h1>개발 중 막힌 문제를 함께 해결해요.</h1>
    <p>LangChain · LangGraph · MCP의 개발 오류를 함께 살펴봅니다.</p>
    <div class="ui-tags"><span class="ui-tag">LangChain</span><span class="ui-tag">LangGraph</span><span class="ui-tag">MCP</span></div></section>''')
    st.caption("이런 질문으로 시작해 보세요")
    for index, (column, example) in enumerate(zip(st.columns(3), EXAMPLES)):
        tech, title, question, name = example
        with column, st.container(border=True, key=f"example_{index}"):
            st.html(f'<div class="ui-tech">{tech}{icon(name)}</div>')
            st.markdown(f"**{title}**")
            st.caption(question)
            if st.button("질문 입력", key=f"example_select_{index}", icon=":material/north_east:", width="stretch"):
                st.session_state.chat_input = f"{tech}에서 {question} 어떤 부분을 확인해야 하나요?"
    st.caption("관련 코드와 개발 환경을 함께 알려주시면 원인을 좁히는 데 도움이 됩니다.", text_alignment="center")


def render_message(message, index):
    if message["role"] == "user":
        text = message.get("display_content", message["content"])
        st.html(f'<div class="ui-user"><pre>{escape(text)}</pre></div>')
        return
    with st.container(key=f"reply_{index}"):
        st.html(f'<div class="ui-assistant"><div class="ui-assistant-icon">{icon("assistant",16)}</div>AI 개발 도우미</div>')
        st.markdown(message["content"])
        render_sources(message.get("sources", []))
        with st.container(horizontal=True):
            with st.popover("답변 복사", icon=":material/content_copy:"):
                st.caption("오른쪽 위 복사 버튼으로 전체 답변을 복사하세요.")
                st.code(message["content"], language=None, wrap_lines=True)
            st.feedback("thumbs", key=f"feedback_{st.session_state.ui_thread}_{index}")
        st.caption("도움 됨 / 도움 안 됨 · 피드백은 현재 접속에서만 유지됩니다.")


def render_preview(kind):
    with st.container(key="preview_body"):
        render_preview_body(kind)


def render_preview_body(kind):
    st.caption("디자인 확인용 예시입니다. 실제 AI 응답·검색·검증 결과가 아닙니다.")
    question = "LangGraph에서 Node가 반환한 State가 다음 Node에 전달되지 않아요." if kind == "오류 분석 예시" else "MCP 서버가 연결되지 않아요."
    render_message({"role": "user", "content": question}, 0)
    st.html(f'<div class="ui-assistant"><div class="ui-assistant-icon">{icon("assistant",16)}</div>AI 개발 도우미 <span>예시 응답</span></div>')
    if kind == "오류 분석 예시":
        st.markdown("**문제 원인**　:gray-badge[근거 부족] :gray-badge[버전 미확인]")
        st.markdown("현재 정보만으로 원인을 확정할 수 없어요. Node 반환값, State schema, 다음 Node로 이어지는 edge를 함께 확인해 주세요. [1]")
        st.markdown("**해결 단계**\n\n1. Node가 변경한 키를 반환하는지 확인해 주세요. [1]\n2. State 정의·연결 구조와 설치된 SDK 버전을 확인해 주세요. [2]")
        st.markdown("**수정 전/후 코드**")
        st.caption("반환 방식만 보여주는 예시 코드이며 실제 해결 코드가 아닙니다.")
        before, after = st.columns(2)
        with before:
            st.caption("수정 전 · Python")
            st.code('def node(state):\n    state["message"] = "hello"\n    # 업데이트 반환 없음', language="python")
        with after:
            st.caption("수정 후 · Python")
            st.code('def node(state):\n    return {"message": "hello"}', language="python")
        st.markdown("**주의사항**\n\nState 키·reducer·SDK 버전에 따라 다를 수 있어요. 실제 코드와 버전을 함께 알려 주세요.")
        with st.expander("참고 근거 · 예시 자료", icon=":material/library_books:"):
            for title, label in [("[1] State 업데이트 반환 방식", "공식 문서 표시 예시"), ("[2] Node 간 State 전달 관련 논의", "GitHub Issue · 의견 표시 예시")]:
                with st.container(border=True):
                    st.markdown(f"**{title}**")
                    st.caption(f"LangGraph · {label} · 원문 링크 미등록")
            st.caption("실제 자료가 제공되지 않았으므로 URL·버전·날짜는 표시하지 않습니다.")
    else:
        with st.container(border=True):
            st.subheader("연결 상황을 조금 더 알려 주세요.")
            st.markdown("연결 오류는 실행 환경과 연결 방식에 따라 원인이 달라질 수 있어요. 확인 가능한 내용을 보내주세요.")
            rows = [("전체 오류 메시지", "Traceback 또는 로그를 처음부터 끝까지 보내 주세요."),
                    ("실행 명령 / 연결 설정", "서버 실행 명령과 클라이언트의 연결 설정이 필요해요."),
                    ("SDK 이름과 버전", "사용 중인 MCP SDK와 설치된 버전을 알려 주세요."),
                    ("연결 방식", "stdio 또는 HTTP 계열 연결 방식을 알려 주세요."),
                    ("운영체제", "Windows, macOS, Linux 등 실행 환경을 알려 주세요.")]
            for title, description in rows:
                st.markdown(f"**{title}**")
                st.caption(description)
            st.caption("API key, 토큰, 비밀번호 등 민감한 정보는 지우고 보내 주세요.")
        st.caption("MCP 서버 오류 상담과 외부 자료를 조회하는 MCP 도구 실행은 별개입니다.")


def render_composer(preview):
    with st.bottom:
        with st.container(key="composer"):
            with st.expander("개발 환경 추가 · 선택", icon=":material/tune:"):
                left, right = st.columns(2)
                with left:
                    st.selectbox("사용 기술", ["선택 안 함", "LangChain", "LangGraph", "MCP"], key="env_tech")
                    st.selectbox("실행 환경", ["선택 안 함", "Python", "Node.js", "기타"], key="env_runtime")
                with right:
                    st.text_input("라이브러리 / SDK 버전", placeholder="사용 중인 실제 버전 입력", key="env_sdk")
                    st.text_input("실행 환경 버전", placeholder="사용 중인 실제 버전 입력", key="env_version")
                st.selectbox("운영체제", ["선택 안 함", "Windows", "macOS", "Linux", "기타"], key="env_os")
                st.caption("선택한 환경은 다음 질문에 함께 전달됩니다. 입력 전에는 버전을 가정하지 않습니다.")
            with st.container(key="composer_box"):
                prompt = st.chat_input("에러 메시지와 관련 코드를 입력해 주세요.", key="chat_input",
                                       submit_mode="disable", height=43, disabled=preview)
                with st.container(key="composer_tools", horizontal=True, horizontal_alignment="distribute"):
                    st.button("이미지 첨부 · 준비 중", key="attachment_pending",
                              icon=":material/add_photo_alternate:", disabled=True)
                    st.caption("Shift + Enter 줄바꿈")
            st.caption("실제 코드와 공식 원문을 확인해 주세요. API 키·비밀번호는 입력하지 마세요.")
    return prompt


def environment_question(prompt):
    fields = [("기술", "env_tech"), ("라이브러리/SDK 버전", "env_sdk"), ("실행 환경", "env_runtime"),
              ("실행 환경 버전", "env_version"), ("운영체제", "env_os")]
    values = [f"{label}: {st.session_state.get(key)}" for label, key in fields
              if st.session_state.get(key) and st.session_state.get(key) != "선택 안 함"]
    return prompt + ("\n\n[사용자가 제공한 개발 환경]\n" + "\n".join(values) if values else "")


def send_question(prompt, mode, *, prepared=None):
    user_message = prepared or {"role": "user", "content": environment_question(prompt), "display_content": prompt}
    with st.spinner("입력을 확인하는 중…" if mode == "연습 모드" else "답변을 작성하고 있어요…", show_time=True):
        result = generate_answer(st.session_state.messages + [user_message], mode,
                                 user_id=st.session_state.get("user_id"),
                                 conversation_id=st.session_state.get("conversation_id"))
    if result.get("conversation_id") is not None:
        st.session_state.conversation_id = result["conversation_id"]
    persisted = False
    if mode == "OpenAI AI 답변" and st.session_state.get("user_id") is not None and result.get("conversation_id") is not None:
        persisted = load_saved_conversation(result["conversation_id"])
    if result["status"] == "success":
        if not persisted:
            st.session_state.messages.extend([user_message, {"role": "assistant", "content": result["answer"], "sources": result["sources"]}])
        st.session_state.ui_failure = None
        remember_conversation(mode)
    else:
        st.session_state.ui_failure = {"message": user_message, "result": result, "saved_in_history": persisted}
    st.rerun()


def render_chat():
    defaults = {"messages": [], "ui_history": {}, "ui_thread": str(uuid4()), "ui_failure": None,
                "answer_mode": "OpenAI AI 답변", "ui_preview": "실제 채팅"}
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)
    owner = st.session_state.get("user_id")
    if st.session_state.get("ui_owner", owner) != owner:
        reset_conversation()
        st.session_state.ui_history = {}
    st.session_state.ui_owner = owner
    st.html(STYLE)
    mode = render_sidebar()
    if st.session_state.get("ui_db_notice"):
        st.warning(st.session_state.ui_db_notice)
    preview = st.session_state.ui_preview != "실제 채팅"
    title = st.session_state.ui_preview if preview else (
        st.session_state.messages[0].get("display_content", st.session_state.messages[0]["content"])[:42]
        if st.session_state.messages else "새 대화")
    st.html(f'<div class="ui-header"><div class="ui-header-title">{icon("panel")}{escape(title)}</div><span>{"UI 예시" if preview else "개발 오류 상담"}</span></div>')
    if preview:
        render_preview(st.session_state.ui_preview)
    else:
        if mode == "연습 모드":
            st.caption("연습 모드 · 실제 AI 답변이 아닙니다.")
        else:
            st.caption("현재 일반 답변을 제공합니다. 공식 문서 검색·외부 조회·이미지 분석은 준비 중입니다.")
        if not st.session_state.messages and not st.session_state.ui_failure:
            render_welcome()
        for index, message in enumerate(st.session_state.messages):
            render_message(message, index)
        failure = st.session_state.ui_failure
        if failure:
            if not failure.get("saved_in_history"):
                render_message(failure["message"], len(st.session_state.messages))
            result = failure["result"]
            if result["status"] == "unsupported":
                st.info(result["error"]["message"])
            else:
                st.error(result["error"]["message"])
                if owner is None or mode != "OpenAI AI 답변":
                    if st.button("재시도", key="retry", icon=":material/refresh:"):
                        send_question("", mode, prepared=failure["message"])
                else:
                    st.caption("질문이 DB에 저장됐을 수 있습니다. 중복 저장 방지를 위해 같은 질문의 자동 재시도는 제공하지 않습니다.")
            st.caption("입력 내용은 위에 유지됩니다. 실패 안내는 AI 답변으로 저장하지 않습니다.")
    prompt = render_composer(preview)
    if prompt and prompt.strip() and not preview:
        send_question(prompt.strip(), mode)
