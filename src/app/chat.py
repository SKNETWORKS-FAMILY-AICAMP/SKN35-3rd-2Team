"""Figma chat UI; model and DB contracts stay in chat_service."""
from copy import deepcopy
from datetime import datetime, timezone, timedelta
from html import escape
from uuid import uuid4
from time import perf_counter

import streamlit as st

from src.app.ui_components import example_cards, copy_answer

from src import db
from src.app.browser_auth import forget_login, remember_login, restore_login

from src.const.config import OPEN_MODEL
from src.app.chat_service import (IMAGE_ONLY_QUESTION, LEGACY_IMAGE_ONLY_QUESTION, chat_result, run_chat, run_db_chat,
                                   text_content)
from src.app.attachments import (ATTACHMENT_ONLY_QUESTION, FILE_ONLY_QUESTION, IMAGE_EXTENSIONS, TEXT_EXTENSIONS,
                                 build_context, is_image_file, is_text_file, split_attachment_blocks)
from src.prompt.chat_prompt import CHAT_SYSTEM_PROMPT


# Figma's small SVG assets are embedded below when installing this UI, so only
# chat.py changes and no temporary asset URLs or new asset files are needed.
FIGMA_ICONS = {'terminal': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiB2aWV3Qm94PSIwIDAgMjAgMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJ0ZXJtaW5hbCI+CjxwYXRoIGlkPSJWZWN0b3IiIGQ9Ik0xMCAxNS44MzRIMTYuNjY2TTMuMzM0IDE0LjE2NzFMOC4zMzM1IDkuMTY2NTdMMy4zMzQgNC4xNjYiIHN0cm9rZS13aWR0aD0iMS43IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZT0id2hpdGUiLz4KPC9nPgo8L3N2Zz4K', 'panel': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiB2aWV3Qm94PSIwIDAgMTggMTgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJwYW5lbC1sZWZ0Ij4KPHBhdGggaWQ9IlZlY3RvciIgZD0iTTYuNzUgMi4yNVYxNS43NU02Ljc1IDIuMjVIMy43NUMyLjkyMTU3IDIuMjUgMi4yNSAyLjkyMTU3IDIuMjUgMy43NVYxNC4yNUMyLjI1IDE1LjA3ODQgMi45MjE1NyAxNS43NSAzLjc1IDE1Ljc1SDYuNzVNNi43NSAyLjI1SDE0LjI1QzE1LjA3ODQgMi4yNSAxNS43NSAyLjkyMTU3IDE1Ljc1IDMuNzVWMTQuMjVDMTUuNzUgMTUuMDc4NCAxNS4wNzg0IDE1Ljc1IDE0LjI1IDE1Ljc1SDYuNzUiIHN0cm9rZS13aWR0aD0iMS43IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZT0iIzY0NzQ4QiIvPgo8L2c+Cjwvc3ZnPgo=', 'workflow': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiB2aWV3Qm94PSIwIDAgMTggMTgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJ3b3JrZmxvdyI+CjxwYXRoIGlkPSJWZWN0b3IiIGQ9Ik01LjI1IDguMjVWMTEuMjVDNS4yNSAxMS42NDc4IDUuNDA4MDQgMTIuMDI5NCA1LjY4OTM0IDEyLjMxMDdDNS45NzA2NCAxMi41OTIgNi4zNTIxOCAxMi43NSA2Ljc1IDEyLjc1SDkuNzVNNS4yNSA4LjI1SDYuNzVDNy41Nzg0MyA4LjI1IDguMjUgNy41Nzg0MyA4LjI1IDYuNzVWMy43NUM4LjI1IDIuOTIxNTcgNy41Nzg0MyAyLjI1IDYuNzUgMi4yNUgzLjc1QzIuOTIxNTcgMi4yNSAyLjI1IDIuOTIxNTcgMi4yNSAzLjc1VjYuNzVDMi4yNSA3LjU3ODQzIDIuOTIxNTcgOC4yNSAzLjc1IDguMjVINS4yNVpNOS43NSAxMi43NVYxNC4yNUM5Ljc1IDE1LjA3ODQgMTAuNDIxNiAxNS43NSAxMS4yNSAxNS43NUgxNC4yNUMxNS4wNzg0IDE1Ljc1IDE1Ljc1IDE1LjA3ODQgMTUuNzUgMTQuMjVWMTEuMjVDMTUuNzUgMTAuNDIxNiAxNS4wNzg0IDkuNzUgMTQuMjUgOS43NUgxMS4yNUMxMC40MjE2IDkuNzUgOS43NSAxMC40MjE2IDkuNzUgMTEuMjVWMTIuNzVaIiBzdHJva2Utd2lkdGg9IjEuNyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2U9IiM2NDc0OEIiLz4KPC9nPgo8L3N2Zz4K', 'code': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiB2aWV3Qm94PSIwIDAgMTggMTgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJjb2RlLXhtbCI+CjxwYXRoIGlkPSJWZWN0b3IiIGQ9Ik0xMy41MDA0IDExLjk5OTdMMTYuNTAwNiA5TDEzLjUwMDQgNi4wMDAzTTQuNDk5NjQgNi4wMDAzTDEuNDk5NCA5TDQuNDk5NjQgMTEuOTk5N00xMC44NzUxIDMuMDAwNkw3LjEyNDg1IDE0Ljk5OTQiIHN0cm9rZS13aWR0aD0iMS43IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZT0iIzY0NzQ4QiIvPgo8L2c+Cjwvc3ZnPgo=', 'plug': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiB2aWV3Qm94PSIwIDAgMTggMTgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJwbHVnIj4KPHBhdGggaWQ9IlZlY3RvciIgZD0iTTkgMTYuNTAwNlYxMi43NTAzTTkgMTIuNzUwM0gxMC41QzExLjI5NTYgMTIuNzUwMyAxMi4wNTg3IDEyLjQzNDIgMTIuNjIxMyAxMS44NzE1QzEzLjE4MzkgMTEuMzA4OSAxMy41IDEwLjU0NTggMTMuNSA5Ljc1MDA2VjYuNzQ5ODJDMTMuNSA2LjU1MDg5IDEzLjQyMSA2LjM2MDExIDEzLjI4MDMgNi4yMTk0NUMxMy4xMzk3IDYuMDc4NzggMTIuOTQ4OSA1Ljk5OTc2IDEyLjc1IDUuOTk5NzZIMTEuMjVNOSAxMi43NTAzSDcuNUM2LjcwNDM1IDEyLjc1MDMgNS45NDEyOSAxMi40MzQyIDUuMzc4NjggMTEuODcxNUM0LjgxNjA3IDExLjMwODkgNC41IDEwLjU0NTggNC41IDkuNzUwMDZWNi43NDk4MkM0LjUgNi41NTA4OSA0LjU3OTAyIDYuMzYwMTEgNC43MTk2NyA2LjIxOTQ1QzQuODYwMzIgNi4wNzg3OCA1LjA1MTA5IDUuOTk5NzYgNS4yNSA1Ljk5OTc2SDYuNzVNMTEuMjUgNS45OTk3NlYxLjQ5OTRNMTEuMjUgNS45OTk3Nkg2Ljc1TTYuNzUgNS45OTk3NlYxLjQ5OTQiIHN0cm9rZS13aWR0aD0iMS43IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZT0iIzY0NzQ4QiIvPgo8L2c+Cjwvc3ZnPgo=', 'assistant': 'data:image/svg+xml;base64,PHN2ZyBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgc3R5bGU9ImRpc3BsYXk6IGJsb2NrOyIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2IiB2aWV3Qm94PSIwIDAgMTYgMTYiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGlkPSJ0ZXJtaW5hbCI+CjxwYXRoIGlkPSJWZWN0b3IiIGQ9Ik04IDEyLjY2NzJIMTMuMzMyOE0yLjY2NzIgMTEuMzMzN0w2LjY2NjggNy4zMzMyNkwyLjY2NzIgMy4zMzI4IiBzdHJva2Utd2lkdGg9IjEuNyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2U9IiM0RjQ2RTUiLz4KPC9nPgo8L3N2Zz4K'}

STYLE = """
<style>
:root {--ui-bg:#F8FAFC;--ui-panel:#F1F5F9;--ui-border:#E2E8F0;
 --ui-ink:#1E293B;--ui-muted:#64748B;--ui-accent:#4F46E5;--ui-radius:16px;--ui-focus:rgba(79,70,229,.12);}
[data-testid="stAppViewContainer"], [data-testid="stMain"] {background:var(--ui-bg);color:var(--ui-ink);}
[data-testid="stSidebar"] {background:var(--ui-panel);border-right:1px solid var(--ui-border);}
[data-testid="stSidebar"] p {color:var(--ui-ink);}
[data-testid="stMainBlockContainer"] {max-width:904px;padding:1rem 2rem 220px;}
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
.ui-brand {border:0;background:transparent;padding:0;cursor:pointer;text-align:left;font:inherit;display:flex;align-items:center;gap:10px;font-weight:700;font-size:18px;color:var(--ui-ink);}
.ui-logo {object-fit:contain;background:transparent;width:32px;height:32px;border-radius:12px;display:flex;align-items:center;justify-content:center;}
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
.st-key-composer [data-testid="stChatInput"] {
 background:var(--ui-bg);border:1px solid #DCE2E9;border-radius:28px;
 box-shadow:0 2px 8px rgba(15,23,42,.06),0 8px 24px rgba(15,23,42,.04);
 transition:border-color .15s ease,box-shadow .15s ease;}
.st-key-composer [data-testid="stChatInput"]:focus-within {
 border-color:var(--ui-accent)!important;
 box-shadow:0 0 0 3px var(--ui-focus),0 4px 16px rgba(15,23,42,.05);}
.st-key-composer [data-testid="stChatInput"] {
 --primary-color:var(--ui-accent);}
.st-key-composer [data-testid="stChatInput"] div:focus-within,
.st-key-composer [data-testid="stChatInput"] textarea:focus {
 border-color:var(--ui-accent)!important;outline-color:var(--ui-accent)!important;}
.st-key-composer [data-testid="stChatInput"] textarea {background:transparent!important;color:var(--ui-ink);}
.st-key-composer [data-testid="stChatInputSubmitButton"] {background:var(--ui-accent);color:white;border-radius:12px;}
.st-key-composer [data-testid="stVerticalBlock"] {gap:8px;}
.st-key-example_0 [data-testid="stVerticalBlock"],.st-key-example_1 [data-testid="stVerticalBlock"],.st-key-example_2 [data-testid="stVerticalBlock"] {gap:8px;}
[data-testid="stSidebar"] button[kind="primary"] p {color:white;}
[data-testid="stBottomBlockContainer"] {max-width:904px;margin:auto;padding:8px 2rem 16px;}
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"] {background:var(--ui-bg)!important;}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li {line-height:1.65;overflow-wrap:anywhere;}
.stApp pre {overflow-x:auto;}
.st-key-example_0,.st-key-example_1,.st-key-example_2 {background:white;border-radius:16px;gap:8px!important;}
.st-key-composer [data-testid="stChatInput"] > div {
 background:transparent!important;border:none!important;border-radius:inherit!important;}
.st-key-composer [data-testid="stChatInput"] > div:focus-within {border:none!important;}
[data-testid="stSelectbox"] [role="group"] {background:white;color:var(--ui-ink);border-color:var(--ui-border);border-radius:12px;}
.st-key-preview_body h3 {font-size:20px;}
@media(max-width:640px) {
 [data-testid="stMainBlockContainer"],[data-testid="stBottomBlockContainer"] {padding-left:16px;padding-right:16px;}
 .ui-welcome {margin-top:36px;}.ui-welcome h1 {font-size:26px;}.ui-user pre {max-width:100%;}
}

/* Keep native chat input layout and hit targets intact. */
.st-key-composer_box {padding:0!important;gap:8px!important;}
.st-key-composer_box [data-testid="stChatInput"] {border-radius:28px;}
.st-key-composer_box [data-testid="stChatInput"] textarea {
 line-height:24px!important;max-height:192px!important;overflow-y:auto!important;}
.st-key-composer_box textarea {text-align:left!important;}
.st-key-composer_box textarea::placeholder {text-align:left;}
.st-key-composer_tools {gap:8px!important;}
[data-testid="stHeader"] {background:var(--ui-bg);}
[data-testid="stMainBlockContainer"] {margin-inline:auto;padding-bottom:220px;}
[data-testid="stBottomBlockContainer"] {margin-inline:auto;}

.ui-sidebar-description {white-space:nowrap;font-size:12px;line-height:1.5;letter-spacing:-0.3px;color:var(--ui-muted);}
/* Keep account controls visible; only the conversation list scrolls. */
[data-testid="stSidebarContent"] {overflow:hidden!important;}
[data-testid="stSidebarUserContent"] {padding:0 20px 12px!important;}
.st-key-sidebar_shell {height:calc(100dvh - 76px);min-height:0;gap:14px!important;}
.st-key-sidebar_header,.st-key-sidebar_footer {flex:0 0 auto;}
.st-key-sidebar_history {flex:1 1 0!important;min-height:0!important;overflow-y:auto;overflow-x:hidden;
 scrollbar-width:thin;padding-right:4px;}
.st-key-sidebar_footer {border-top:1px solid var(--ui-border);padding-top:10px;max-height:55dvh;overflow-y:auto;}
.st-key-sidebar_history [data-testid="stButton"] button {background:transparent;border-color:transparent;
 text-align:left;justify-content:flex-start;padding:8px 10px;min-height:40px;}
.st-key-sidebar_history [data-testid="stButton"] button:hover {background:#E2E8F0;border-color:transparent;}
.st-key-sidebar_history [data-testid="stButton"] button > div {justify-content:flex-start!important;flex:1;min-width:0;}
.st-key-sidebar_history [data-testid="stButton"] button [data-testid="stMarkdownContainer"] {flex:1;min-width:0;text-align:left!important;}
.st-key-sidebar_history [data-testid="stButton"] button p {text-align:left!important;white-space:nowrap;
 overflow:hidden;text-overflow:ellipsis;display:block;}
.st-key-sidebar_header [data-testid="stButton"] button {min-height:40px;height:40px;}
.st-key-sidebar_header [data-testid="stTextInput"] input {background:var(--ui-panel);}
.st-key-sidebar_footer [data-testid="stVerticalBlock"] {gap:8px;}
.st-key-sidebar_footer [data-testid="stCaptionContainer"] {font-size:11px;}

.st-key-sidebar_shell {height:calc(100dvh - 88px)!important;min-height:calc(100dvh - 88px)!important;flex:none!important;}
.st-key-sidebar_shell > [data-testid="stLayoutWrapper"] {flex:0 0 auto!important;min-height:0;}
.st-key-sidebar_shell > [data-testid="stLayoutWrapper"]:has(> .st-key-sidebar_history) {flex:1 1 0!important;overflow:hidden;}
.st-key-sidebar_history {height:100%!important;flex:1 1 auto!important;}

/* Compact sidebar width and preserve room for saved conversations. */
[data-testid="stSidebar"][aria-expanded="true"] {width:260px!important;min-width:260px!important;max-width:260px!important;}
[data-testid="stSidebarUserContent"] {padding:0 12px 12px!important;}
.st-key-sidebar_shell > [data-testid="stLayoutWrapper"]:has(> .st-key-sidebar_history) {min-height:100px!important;}
.st-key-sidebar_shell > [data-testid="stLayoutWrapper"]:has(> .st-key-sidebar_footer) {margin-top:auto;}
.st-key-sidebar_history {min-height:100px!important;}
.st-key-sidebar_header [data-testid="stButton"] button,
.st-key-sidebar_footer [data-testid="stButton"] button,
.st-key-sidebar_footer [data-testid="stPopover"] > button {min-height:40px!important;height:40px!important;}

.st-key-sidebar_header [data-testid="stTextInput"] [data-baseweb="input"],
.st-key-sidebar_header [data-testid="stTextInput"] input {background:#FFFFFF!important;}
.st-key-sidebar_header [data-testid="stTextInput"] [data-baseweb="input"] {
 border:1px solid var(--ui-border)!important;border-radius:12px;}
.st-key-sidebar_footer {max-height:none;overflow:visible;}


/* Dialogs render outside .stApp, so use the same accent explicitly. */
[data-testid="stDialog"] {--primary-color:#4F46E5;}
[data-testid="stDialog"] button[kind="primaryFormSubmit"] {
 background:#4F46E5!important;border-color:#4F46E5!important;color:white!important;}
[data-testid="stDialog"] button[kind="primaryFormSubmit"]:hover {
 background:#4338CA!important;border-color:#4338CA!important;}
[data-testid="stDialog"] button[kind="primaryFormSubmit"]:focus-visible {
 outline:2px solid #4F46E5;outline-offset:2px;}
/* Draw only the checked radio indicator; keep the label background clear. */
[data-testid="stDialog"] [data-testid="stRadio"] label:has(input:checked) {
 position:relative;background:transparent!important;}
[data-testid="stDialog"] [data-testid="stRadio"] label:has(input:checked)::before {
 content:"";position:absolute;left:0;top:50%;transform:translateY(-50%);
 width:20px;height:20px;border-radius:50%;background:#4F46E5;
 z-index:1;pointer-events:none;}
[data-testid="stDialog"] [data-testid="stRadio"] label:has(input:checked)::after {
 content:"";position:absolute;left:7px;top:50%;transform:translateY(-50%);
 width:6px;height:6px;border-radius:50%;background:white;
 z-index:2;pointer-events:none;}
[data-testid="stDialog"] [data-baseweb="input"]:focus-within {
 border-color:#4F46E5!important;}


/* Upload affordance and its native tooltip. */
.st-key-composer [data-testid="stChatInputFileUploadButton"] button {
 width:36px!important;height:36px!important;border-radius:50%!important;
 transition:background-color .15s ease;color:#475569!important;}
.st-key-composer [data-testid="stChatInputFileUploadButton"] button:not(:disabled):hover,
.st-key-composer [data-testid="stChatInputFileUploadButton"] button:focus-visible {
 background:#E5E7EB!important;}
.codeclue-upload-tooltip {
 background:#1E293B!important;color:#FFFFFF!important;
 padding:10px 14px!important;border-radius:10px!important;
 font-size:13px!important;line-height:1.5!important;
 box-shadow:0 4px 12px rgba(15,23,42,.18)!important;}

/* Requested toolbar removal includes its reserved height. */
[data-testid="stHeader"] {height:0!important;min-height:0!important;background:transparent!important;overflow:visible!important;}
[data-testid="stToolbar"] {height:0!important;min-height:0!important;overflow:visible!important;pointer-events:none;}
[data-testid="stToolbar"] > div > div:last-child:not(:first-child) {display:none!important;}
[data-testid="stMainMenu"], [data-testid="stDecoration"], [data-testid="stToolbarActions"], [data-testid="stAppDeployButton"] {display:none!important;}
[data-testid="stExpandSidebarButton"] {
 position:fixed!important;top:8px!important;left:8px!important;
 display:flex!important;visibility:visible!important;opacity:1!important;
 pointer-events:auto!important;z-index:1000001!important;}
[data-testid="stMainBlockContainer"] {padding-top:1rem!important;}
[data-testid="stSidebarCollapsedControl"] {
 position:fixed!important;top:8px!important;left:8px!important;
 width:40px!important;height:40px!important;overflow:visible!important;
 visibility:visible!important;opacity:1!important;z-index:1000001!important;}
[data-testid="stSidebarCollapsedControl"] button {visibility:visible!important;opacity:1!important;}
.st-key-sidebar_header [data-testid="stTextInput"] input {text-align:left;}
.st-key-composer [data-testid="stChatInput"] textarea,
.st-key-composer [data-testid="stChatInput"] [data-baseweb="textarea"] {background:var(--ui-bg)!important;}
.ui-draft-code {padding:12px;max-height:192px;overflow:auto;}
.ui-draft-code pre {white-space:pre-wrap;background:var(--ui-panel);padding:12px;border-radius:8px;}
/* Native code blocks keep their copy action visible, including while streaming. */
[data-testid="stCode"] {
 background:#F0F0F0;border:1px solid #E2E2E2;border-radius:20px;
 padding-top:42px;overflow:hidden;}
[data-testid="stCode"]::before {
 content:attr(data-code-language);position:absolute;top:14px;left:20px;
 font-size:13px;font-weight:500;color:var(--ui-ink);}
[data-testid="stCode"] pre {background:transparent!important;border-radius:0!important;padding:16px 20px!important;}
[data-testid="stCode"] > div:last-child:has(button) {
 opacity:1!important;visibility:visible!important;pointer-events:auto!important;
 transition:none!important;top:0!important;right:0!important;padding:8px 12px!important;}
[class*="st-key-user_message_"] {background:var(--ui-panel);border-radius:16px;padding:12px 20px;margin-left:auto;
 width:fit-content!important;max-width:100%!important;min-width:0;box-sizing:border-box;}
/* Show the loading spinner only beside elapsed time. */
.st-key-generation_progress [data-testid="stExpanderIconSpinner"],
.st-key-generation_progress [data-testid="stSpinner"],
.st-key-generation_progress [data-testid="stStatusWidget"] {display:none!important;}
/* The submit hint overlaps typed text in the narrow sidebar search field. */
.st-key-history_search [data-testid="InputInstructions"],
.st-key-history_search [data-testid="stInputInstructions"] {display:none!important;}
/* Interaction states share the same design tokens. */
.st-key-composer [data-testid="stChatInput"] {background:white;}
.st-key-composer [data-testid="stChatInput"] textarea,
.st-key-composer [data-testid="stChatInput"] [data-baseweb="textarea"] {background:transparent!important;}
.st-key-composer [data-testid="stChatInputSubmitButton"]:disabled {opacity:.4;}
.st-key-sidebar_history button[kind="primary"] {background:#EEF2FF!important;border-color:#C7D2FE!important;}
.st-key-sidebar_history button[kind="primary"] p {color:var(--ui-accent)!important;font-weight:600;}
.st-key-sidebar_footer {padding:14px 4px 4px;}
@media (prefers-reduced-motion:reduce) { .st-key-composer * {transition:none!important;} }
</style>
"""


UPLOAD_TOOLTIP = r"""
<script>
(() => {
  if (window.codeclueCopyHandler) {
    document.removeEventListener("click", window.codeclueCopyHandler);
    delete window.codeclueCopyHandler;
  }
  if (window.codeclueDraftHandler) document.removeEventListener("input", window.codeclueDraftHandler);
  window.codeclueDraftHandler = event => {
    const textarea = event.target;
    if (!textarea.matches('.st-key-composer textarea')) return;
    const host = textarea.closest('[data-testid="stChatInput"]');
    let preview = host.querySelector('.ui-draft-code');
    const fences = [...textarea.value.matchAll(/```([^\n`]*)\n([\s\S]*?)(?:```|$)/g)];
    if (!fences.length) { if (preview) preview.remove(); return; }
    if (!preview) {
      preview = document.createElement('div');
      preview.className = 'ui-draft-code';
      preview.setAttribute('aria-label', '입력 코드 미리보기');
      host.appendChild(preview);
    }
    preview.replaceChildren();
    for (const match of fences) {
      const label = document.createElement('small');
      label.textContent = match[1] || '코드';
      const pre = document.createElement('pre');
      pre.textContent = match[2];
      preview.append(label, pre);
    }
  };
  document.addEventListener("input", window.codeclueDraftHandler);
  if (window.codeclueBrandHandler) document.removeEventListener("click", window.codeclueBrandHandler);
  window.codeclueBrandHandler = event => {
    if (event.target.closest('.ui-brand')) {
      document.querySelector('.st-key-new_chat button')?.click();
    }
  };
  document.addEventListener("click", window.codeclueBrandHandler);
  // Streamlit exposes no upload-tooltip parameter. Update only its native tooltip.
  const label = "Upload images or code files (PNG, JPG, WEBP, PY, MD, TXT, LOG, IPYNB). Up to 3 images and 3 text files.";
  const update = () => {
    document.querySelectorAll('[data-testid="stCode"]').forEach(block => {
      const code = block.querySelector('code');
      const languageClass = code && [...code.classList].find(name => name.startsWith('language-'));
      const language = languageClass ? languageClass.slice(9) : '';
      const shell = /^(?:\s*\$\s*)?(?:pip(?:3)?\s|python(?:3)?\s+-m\s+pip\s|npm\s|uv\s|conda\s)/m.test(code ? code.textContent : '');
      const label = /^(bash|sh|shell|console|shell-session)$/.test(language) || (!language && shell)
        ? 'Bash' : language ? language.charAt(0).toUpperCase() + language.slice(1) : '코드';
      if (block.dataset.codeLanguage !== label) block.dataset.codeLanguage = label;
    });
    document.querySelectorAll('[role="tooltip"], [data-testid="stTooltipContent"]').forEach(el => {
      if (el.textContent.trim().startsWith("Upload or drag")) {
        el.classList.add("codeclue-upload-tooltip");
        if (el.textContent.trim() !== label) el.textContent = label;
      }
    });
  };
  if (window.codeclueUploadTooltipObserver) window.codeclueUploadTooltipObserver.disconnect();
  window.codeclueUploadTooltipObserver = new MutationObserver(update);
  window.codeclueUploadTooltipObserver.observe(document.body, {childList:true, subtree:true, characterData:true});
  update();
})();
</script>
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


IMAGE_TYPES = ["png", "jpg", "jpeg", "webp"]
MAX_UPLOAD_MB = 10  # 올릴 때 한도. 2MB를 넘는 이미지는 서비스에서 자동으로 줄인다.
DEFAULT_IMAGE_TEXT = IMAGE_ONLY_QUESTION


def split_composer_value(value, *, limit=3):
    """chat_input 값(None, 문자열, 또는 text/files를 가진 값)을 (글, 이미지 바이트 목록, 안내)로 나눈다."""
    if value is None:
        return "", [], None
    if isinstance(value, str):
        return value, [], None
    text = getattr(value, "text", None)
    files = getattr(value, "files", None)
    if text is None and isinstance(value, dict):
        text, files = value.get("text"), value.get("files")
    images = [file.getvalue() for file in (files or []) if is_image_file(getattr(file, "name", None))]
    notice = None
    if len(images) > limit:
        images = images[:limit]
        notice = f"이미지는 한 번에 {limit}장까지 보낼 수 있어서 앞의 {limit}장만 사용했어요."
    return text or "", images, notice


def composer_documents(value):
    """chat_input 값에서 글 파일(.py, .md, .ipynb 등)을 [(이름, 바이트)]로 꺼낸다. 이미지는 split_composer_value가 맡는다."""
    files = getattr(value, "files", None)
    if files is None and isinstance(value, dict):
        files = value.get("files")
    return [(file.name, file.getvalue()) for file in (files or []) if is_text_file(getattr(file, "name", None))]


def default_question(images, has_documents):
    """글 없이 파일만 올렸을 때 대신 넣는 질문 (문제가 있다고 단정하지 않는 문장)."""
    if images and has_documents:
        return ATTACHMENT_ONLY_QUESTION
    return FILE_ONLY_QUESTION if has_documents else DEFAULT_IMAGE_TEXT


def generate_answer(messages, mode, *, user_id=None, conversation_id=None, images=None, on_token=None, on_stage=None):
    if images and mode != "OpenAI AI 답변":
        return chat_result(status="error", code="IMAGE_UNSUPPORTED",
                           message="이미지 분석은 'OpenAI AI 답변' 모드에서만 사용할 수 있어요.")
    if mode == "연습 모드":
        return chat_result(
            f"입력한 질문: {messages[-1]['content']}\n\n"
            "질문을 정상적으로 받았습니다. 화면 동작을 확인하는 연습 모드입니다."
        )
    if mode == "OpenAI AI 답변":
        if user_id is not None:
            return run_db_chat(messages[-1]["content"], user_id=user_id, conversation_id=conversation_id,
                               images=images, on_token=on_token, on_stage=on_stage)
        return run_chat(messages, images=images, on_token=on_token, on_stage=on_stage)
    if mode != "NVIDIA AI 답변":
        return chat_result(status="error", code="INVALID_MODE", message="답변 모드를 확인해 주세요.")
    try:
        response_stream = get_model().stream(
            [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
            + [{"role": m["role"], "content": m["content"]} for m in messages]
        )
        answer = ""
        for chunk in response_stream:
            token = chunk.content if isinstance(chunk.content, str) else text_content(chunk.content)
            answer += token
            if on_token and token:
                on_token(token)
        if not answer:
            raise ValueError("빈 응답")
        return chat_result(answer)
    except Exception:
        return chat_result(status="error", code="MODEL_ERROR", message=
            "답변을 받지 못했습니다. NVIDIA 설정과 인터넷 연결을 확인해 주세요.")


def render_sources(sources):
    if not sources:
        return
    with st.expander("참고 자료", icon=":material/library_books:"):
        st.caption("답변 생성에 전달된 검색 문서입니다. 각 문서가 답변을 뒷받침하는지는 별도 확인이 필요합니다.")
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
    st.session_state.pop("ui_scroll_to_latest", None)
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
    forget_login()
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
                         "images": [b for b in (db.thumbnail_bytes(a) for a in row.attachments) if b],
                         "image_analysis": row.image_analysis,
                         "sources": [{name: getattr(source, name) for name in
                                      ("url", "title", "tech", "version", "doc_type", "snippet", "score", "is_grounded")}
                                     for source in sorted(row.sources, key=lambda source: source.rank)]}
                        for row in rows]
        st.session_state.messages = messages
        st.session_state.ui_scroll_to_latest = True
        st.session_state.conversation_id = conversation_id
        st.session_state.ui_thread = f"db_{conversation_id}"
        st.session_state.ui_failure = None
        st.session_state.ui_db_notice = None
        return True
    except Exception:
        st.session_state.ui_db_notice = "대화를 불러오지 못했습니다. DB 연결과 접근 권한을 확인해 주세요."
        return False


def history_period(updated):
    if updated.tzinfo is None:
        updated = updated.replace(tzinfo=timezone.utc)
    local = timezone(timedelta(hours=9))
    age = (datetime.now(local).date() - updated.astimezone(local).date()).days
    return "오늘" if age <= 0 else "지난 7일" if age < 7 else "이전 대화"


def render_saved_history(query):
    try:
        with db.db_session() as session:
            items = [{"id": row.id, "title": row.title or "새 대화", "updated": row.updated_at}
                     for row in db.list_conversations(session, st.session_state.user_id, limit=100)]
    except Exception:
        st.warning("대화 목록을 불러오지 못했습니다. DB 연결 상태를 확인해 주세요.")
        return
    visible = [item for item in items if query.casefold() in item["title"].casefold()]
    if not visible:
        st.caption("아직 저장된 대화가 없어요." if not query else "검색 결과가 없어요.", text_alignment="center")
    period = None
    for item in visible:
        current = history_period(item["updated"])
        if current != period:
            st.caption(current)
            period = current
        if st.button(item["title"], key=f"saved_history_{item['id']}",
                     icon=":material/chat_bubble_outline:", width="stretch",
                     type="primary" if st.session_state.get("conversation_id") == item["id"] else "secondary"):
            if load_saved_conversation(item["id"]):
                st.session_state.answer_mode = "OpenAI AI 답변"
                st.session_state.previous_mode = "OpenAI AI 답변"
                st.session_state.ui_preview = "실제 채팅"
                st.session_state.chat_input = ""
                st.rerun()


def render_authentication():
    if st.session_state.get("user_id") is not None:
        st.markdown(f"**{escape(st.session_state.get('username', '사용자'))}**")
        st.caption("OpenAI 대화는 계정에 저장됩니다.")
        st.button("로그아웃", key="logout", icon=":material/logout:",
                  width="stretch", on_click=logout)
        return
    st.markdown("**게스트**")
    st.caption("로그인하고 이전 대화를 이어가세요.")
    if st.button("로그인/ 회원가입", key="login_open", icon=":material/login:", width="stretch"):
        st.session_state.ui_auth_open = True
        st.session_state.auth_action = "로그인"


def close_auth_dialog():
    st.session_state.ui_auth_open = False
    st.session_state.pop("auth_missing_fields", None)


@st.dialog("로그인", width="small", on_dismiss=close_auth_dialog)
def render_auth_dialog():
    render_auth_form("로그인")


@st.dialog("회원가입", width="small", on_dismiss=close_auth_dialog)
def render_signup_dialog():
    render_auth_form("회원가입")


def switch_auth(action):
    st.session_state.auth_action = action
    st.session_state.pop("auth_missing_fields", None)
    for key in ("auth_username", "auth_password", "auth_confirmation"):
        st.session_state.pop(key, None)
    st.rerun(scope="app")


def validate_auth_fields():
    st.session_state.auth_missing_fields = {
        "auth_username": not st.session_state.get("auth_username", "").strip(),
        "auth_password": not st.session_state.get("auth_password", ""),
    }


def render_auth_form(action):
    if st.session_state.pop("auth_registered", False):
        st.success("회원가입이 완료되었습니다. 로그인해 주세요.")
    guidance = "아이디: 영문 소문자·숫자·밑줄 3~30자 / 비밀번호: 8자 이상"
    guidance_slot = st.empty()
    if action == "회원가입":
        guidance_slot.caption(guidance)
    missing = st.session_state.get("auth_missing_fields", {})
    error_placeholders = {
        "auth_username": "아이디를 입력하세요.",
        "auth_password": "비밀번호를 입력하세요.",
    }
    selectors = ",".join(
        f".st-key-{key} input::placeholder"
        for key in error_placeholders if missing.get(key)
    )
    if selectors:
        st.html(f"<style>{selectors} {{color:#dc2626!important;opacity:1!important;}}</style>")
    with st.form("account_form", clear_on_submit=False):
        username = st.text_input("아이디", key="auth_username", max_chars=30,
                                 placeholder=error_placeholders["auth_username"] if missing.get("auth_username") else None)
        password = st.text_input("비밀번호", type="password", key="auth_password",
                                 placeholder=error_placeholders["auth_password"] if missing.get("auth_password") else None)
        confirmation = st.text_input("비밀번호 확인", type="password", key="auth_confirmation") if action == "회원가입" else None
        submitted = st.form_submit_button(action, type="primary", width="stretch",
                                           on_click=validate_auth_fields)
    # Render the footer before validation so every error keeps navigation visible.
    st.button("회원가입" if action == "로그인" else "로그인으로 돌아가기",
              key="auth_switch", width="stretch", on_click=switch_auth,
              args=("회원가입" if action == "로그인" else "로그인",))
    st.caption("새로고침해도 로그인 상태가 유지됩니다.  \n로그아웃하거나 브라우저 탭을 닫으면 로그인이 종료됩니다. (최대 24시간)",
               text_alignment="center" if action == "로그인" else "left")
    if submitted:
        if not username.strip() or not password:
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
            st.session_state.auth_registered = True
            switch_auth("로그인")
            st.rerun()
        elif identity is None:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
        else:
            try:
                remember_login(identity)
            except Exception:
                st.error("로그인 상태를 저장하지 못했습니다. 잠시 후 다시 시도해 주세요.")
                return
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
    with st.sidebar, st.container(key="sidebar_shell"):
        with st.container(key="sidebar_header"):
            st.html('<button type="button" class="ui-brand" aria-label="CodeClue 새 대화"><img class="ui-logo" src="data:image/png;base64,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" alt="CodeClue">CodeClue</button>')
            st.html('<div class="ui-sidebar-description">LLM/RAG 개발 오류 분석 및 해결 도우미</div>')
            st.button("새 대화", icon=":material/add:", type="primary", width="stretch",
                      key="new_chat", on_click=reset_conversation)
            query = st.text_input("대화 검색", placeholder="대화 검색", key="history_search", label_visibility="collapsed")
        with st.container(key="sidebar_history"):
            owner = st.session_state.get("user_id")
            if owner is not None:
                render_saved_history(query)
            items = sorted(st.session_state.ui_history.items(), key=lambda item: item[1]["updated"], reverse=True)
            visible = [(key, item) for key, item in items if query.casefold() in item["title"].casefold()]
            if owner is not None and visible:
                st.caption("현재 접속의 임시 대화")
            if owner is None and not visible:
                st.caption("아직 대화가 없어요." if not query else "검색 결과가 없어요.", text_alignment="center")
            period = None
            for key, item in visible:
                current = history_period(item["updated"])
                if current != period:
                    st.caption(current)
                    period = current
                if st.button(item["title"], key=f"history_{key}", icon=":material/chat_bubble_outline:", width="stretch",
                             type="primary" if st.session_state.get("ui_thread") == key else "secondary"):
                    st.session_state.messages = deepcopy(item["messages"])
                    st.session_state.ui_scroll_to_latest = True
                    st.session_state.conversation_id = item["conversation_id"]
                    st.session_state.ui_thread = key
                    st.session_state.ui_failure = None
                    st.session_state.answer_mode = item["mode"]
                    st.session_state.previous_mode = item["mode"]
                    st.rerun()
        with st.container(key="sidebar_footer"):
            render_authentication()
    return st.session_state.answer_mode


def render_welcome():
    with st.container(key="welcome_intro"):
        render_welcome_body()



def select_example_question(question):
    # Callbacks run before chat_input is instantiated on the next rerun.
    st.session_state.chat_input = question


def render_welcome_body():
    st.html('''<section class="ui-welcome"><h1>개발 중 막힌 문제를 함께 해결해요.</h1>
    <p>LangChain · LangGraph · MCP의 개발 오류를 함께 살펴봅니다.</p>
    <div class="ui-tags"><span class="ui-tag">LangChain</span><span class="ui-tag">LangGraph</span><span class="ui-tag">MCP</span></div></section>''')
    st.caption("이런 질문으로 시작해 보세요")
    def choose_example():
        selected = st.session_state["welcome_cards"].get("selected")
        if isinstance(selected, int) and 0 <= selected < len(EXAMPLES):
            tech, _, question, _ = EXAMPLES[selected]
            select_example_question(f"{tech}에서 {question} 어떤 부분을 확인해야 하나요?")
    example_cards(EXAMPLES, on_selected_change=choose_example)
    st.caption("관련 코드와 개발 환경을 함께 알려주시면 원인을 좁히는 데 도움이 됩니다.", text_alignment="center")



def render_message(message, index):
    if message["role"] == "user":
        st.html(f'<div id="user-turn-{index}" style="scroll-margin-top:24px"></div>')
        text = message.get("display_content", message["content"])
        clean_content, attached_files = split_attachment_blocks(message["content"])
        if "display_content" not in message:
            text = clean_content  # 저장된 대화에서 불러온 질문: 파일 내용은 뺀다
        if (message.get("images") or attached_files) and text in (
                DEFAULT_IMAGE_TEXT, LEGACY_IMAGE_ONLY_QUESTION, FILE_ONLY_QUESTION, ATTACHMENT_ONLY_QUESTION):
            text = ""
        if message.get("images"):
            with st.container(key=f"user_images_row_{index}", horizontal=True,
                              horizontal_alignment="right", width="stretch"):
                for data in message["images"]:
                    try:
                        st.image(data, width=180, alt="첨부한 오류 화면")
                    except Exception:
                        st.caption("이미지를 표시할 수 없어요.")
        if text:
            with st.container(key=f"user_text_row_{index}", horizontal=True,
                              horizontal_alignment="right", width="stretch"):
                with st.container(key=f"user_message_{index}", width="content"):
                    st.markdown(text)
        for file_name, file_body in attached_files:
            with st.expander(f"첨부 파일 · {file_name}", icon=":material/description:"):
                st.code(file_body, language=None, wrap_lines=True)
        if message.get("image_analysis"):
            with st.expander("이미지에서 읽은 내용", icon=":material/image_search:"):
                st.text(message["image_analysis"])
                st.caption("읽은 내용이 틀렸다면 바로잡아서 다시 질문해 주세요.")
        return
    with st.container(key=f"reply_{index}"):
        st.html(f'<div class="ui-assistant"><div class="ui-assistant-icon">{icon("assistant",16)}</div>CodeClue</div>')
        st.markdown(message["content"])
        render_sources(message.get("sources", []))
        elapsed = message.get("elapsed_seconds")
        if elapsed is None:
            timing_key = (st.session_state.get("user_id"), st.session_state.get("conversation_id"), index)
            elapsed = st.session_state.get("ui_answer_timings", {}).get(timing_key)
        if elapsed is not None:
            st.caption(f"생성 소요시간 · {elapsed:.1f}초")
        copy_answer(message["content"], key=f"copy_answer_{index}")



def render_preview(kind):
    with st.container(key="preview_body"):
        render_preview_body(kind)


def render_preview_body(kind):
    st.caption("디자인 확인용 예시입니다. 실제 AI 응답·검색·검증 결과가 아닙니다.")
    question = "LangGraph에서 Node가 반환한 State가 다음 Node에 전달되지 않아요." if kind == "오류 분석 예시" else "MCP 서버가 연결되지 않아요."
    render_message({"role": "user", "content": question}, 0)
    st.html(f'<div class="ui-assistant"><div class="ui-assistant-icon">{icon("assistant",16)}</div>CodeClue <span>예시 응답</span></div>')
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
            with st.container(key="composer_box"):
                prompt = st.chat_input("에러 메시지와 관련 코드를 입력해 주세요.", key="chat_input",
                                       submit_mode="disable", height="content", disabled=preview,
                                       accept_file="multiple", file_type=[*IMAGE_EXTENSIONS, *TEXT_EXTENSIONS], max_upload_size=MAX_UPLOAD_MB)
            st.caption("API 키·비밀번호는 입력하지 마세요.", text_alignment="center")
    return prompt


def environment_question(prompt):
    fields = [("기술", "env_tech"), ("라이브러리/SDK 버전", "env_sdk"), ("실행 환경", "env_runtime"),
              ("실행 환경 버전", "env_version"), ("운영체제", "env_os")]
    values = [f"{label}: {st.session_state.get(key)}" for label, key in fields
              if st.session_state.get(key) and st.session_state.get(key) != "선택 안 함"]
    return prompt + ("\n\n[사용자가 제공한 개발 환경]\n" + "\n".join(values) if values else "")


def graph_messages(messages):
    """로그인하지 않은 대화는 DB 이력이 없으므로, 이전에 읽은 이미지 내용을 질문 글에 붙여서 다음 질문에도 AI가 기억하게 한다."""
    return [{**m, "content": m["content"] + "\n\n[첨부 이미지에서 읽은 내용] " + m["image_analysis"]}
            if m["role"] == "user" and m.get("image_analysis") else m for m in messages]


def send_question(prompt, mode, *, prepared=None, images=None, context=""):
    """context: 입력창에 올린 글 파일을 질문 뒤에 붙일 글로 바꾼 것 (attachments.build_context). 화면에는 질문만 보이고 파일은 접는 영역으로 보인다."""
    if prepared is not None:
        images = prepared.get("images")
    question = prompt or default_question(images, bool(context))
    user_message = prepared or {"role": "user", "content": environment_question(question) + context,
                                "display_content": question, "images": images or []}
    with st.container(key="generation_progress"):
        progress = st.status("입력을 확인하는 중…" if mode == "연습 모드" else "질문을 분석하고 있어요…", expanded=False, type="compact")
    answer_slot = st.empty()
    streamed = []
    def show_token(token):
        streamed.append(token)
        answer_slot.markdown("".join(streamed) + "▌")
    started_at = perf_counter()
    with st.spinner("경과 시간", show_time=True):
        result = generate_answer(graph_messages(st.session_state.messages) + [user_message], mode,
                                 user_id=st.session_state.get("user_id"),
                                 conversation_id=st.session_state.get("conversation_id"),
                                 images=images or None, on_token=show_token,
                                 on_stage=lambda label: progress.update(label=label))
        if result["status"] == "success":
            progress.update(label="답변 완성", state="complete")
    elapsed_seconds = perf_counter() - started_at
    if result["status"] != "success":
        progress.empty()
    if result["status"] == "success":
        answer_slot.markdown(result["answer"])
    else:
        answer_slot.empty()
    if result.get("conversation_id") is not None:
        st.session_state.conversation_id = result["conversation_id"]
    persisted = False
    if mode == "OpenAI AI 답변" and st.session_state.get("user_id") is not None and result.get("conversation_id") is not None:
        persisted = load_saved_conversation(result["conversation_id"])
    if result["status"] == "success":
        if not persisted:
            user_message = {**user_message, "image_analysis": result.get("image_analysis")}  # 로그인 안 해도 읽은 내용을 보여 준다
            st.session_state.messages.extend([user_message, {"role": "assistant", "content": result["answer"], "sources": result["sources"], "elapsed_seconds": elapsed_seconds}])
        if persisted and st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
            index = len(st.session_state.messages) - 1
            st.session_state.messages[index]["elapsed_seconds"] = elapsed_seconds
            timing_key = (st.session_state.get("user_id"), st.session_state.get("conversation_id"), index)
            st.session_state.setdefault("ui_answer_timings", {})[timing_key] = elapsed_seconds
        st.session_state.ui_failure = None
        remember_conversation(mode)
    else:
        st.session_state.ui_failure = {"message": user_message, "result": result, "saved_in_history": persisted}
    st.rerun()



def scroll_to_latest_question():
    if not st.session_state.pop("ui_scroll_to_latest", False):
        return
    indices = [index for index, message in enumerate(st.session_state.messages)
               if message["role"] == "user"]
    if not indices:
        return
    target = indices[-1]
    # Leave room below a short final answer so the question can reach the top.
    st.html(f"""
    <div style="height:100dvh" aria-hidden="true"></div>
    <script>
    (() => {{
      const main = document.querySelector('[data-testid="stMain"]');
      if (!main) return;
      let attempts = 0;
      let previousTop = null;
      let stableFrames = 0;
      const position = () => {{
        const anchor = document.getElementById('user-turn-{target}');
        if (anchor) {{
          const top = main.scrollTop + anchor.getBoundingClientRect().top
            - main.getBoundingClientRect().top - 24;
          stableFrames = previousTop !== null && Math.abs(top - previousTop) < 1
            ? stableFrames + 1 : 0;
          previousTop = top;
          main.scrollTo({{top, behavior: 'instant'}});
        }}
        if (++attempts < 60 && stableFrames < 6) requestAnimationFrame(position);
      }};
      requestAnimationFrame(position);
    }})();
    </script>
    """, unsafe_allow_javascript=True)


def render_chat():
    restore_login()
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
    st.html(UPLOAD_TOOLTIP, unsafe_allow_javascript=True)
    mode = render_sidebar()
    if st.session_state.get("ui_auth_open") and st.session_state.get("user_id") is None:
        if st.session_state.get("auth_action") == "회원가입":
            render_signup_dialog()
        else:
            render_auth_dialog()
    if st.session_state.get("ui_db_notice"):
        st.warning(st.session_state.ui_db_notice)
    preview = st.session_state.ui_preview != "실제 채팅"
    title = st.session_state.ui_preview if preview else (
        st.session_state.messages[0].get("display_content", st.session_state.messages[0]["content"])[:42]
        if st.session_state.messages else "새 대화")
    st.html(f'<div class="ui-header"><div class="ui-header-title">{icon("panel")}{escape(title)}</div><span>{"UI 예시" if preview else "개발 오류 상담"}</span></div>')
    body = st.empty()
    value = render_composer(preview)
    prompt, images, notice = split_composer_value(value)
    prompt = prompt.strip()
    context, document_notices = build_context(composer_documents(value))
    submitting = bool(prompt or images or context) and not preview
    with body.container():
        for message in [notice, *document_notices]:
            if message:
                st.warning(message)
        if preview:
            render_preview(st.session_state.ui_preview)
        else:
            if mode == "연습 모드":
                st.caption("연습 모드 · 실제 AI 답변이 아닙니다.")
            else:
                st.caption("일반 질문, 공식 문서 검색, 외부 조회, 이미지 분석, 글 파일(py, md, ipynb 등) 읽기를 제공합니다. 참고 자료가 반환되면 답변 아래에서 확인할 수 있습니다.")
            # Keep the welcome in its own stable placeholder. Clearing this slot
            # removes all previous cards before any blocking model work begins.
            welcome_slot = st.empty()
            if not st.session_state.messages and not st.session_state.ui_failure and not submitting:
                with welcome_slot.container():
                    render_welcome()
            else:
                welcome_slot.empty()
            for index, message in enumerate(st.session_state.messages):
                render_message(message, index)
            scroll_to_latest_question()
            failure = st.session_state.ui_failure
            if failure and not submitting:
                if not failure.get("saved_in_history"):
                    render_message(failure["message"], len(st.session_state.messages))
                result = failure["result"]
                failure_index = len(st.session_state.messages) + (0 if failure.get("saved_in_history") else 1)
                render_message({"role": "assistant", "content": result["error"]["message"], "sources": []}, failure_index)
                if result["status"] != "unsupported":
                    if owner is None or mode != "OpenAI AI 답변":
                        if st.button("재시도", key="retry", icon=":material/refresh:"):
                            send_question("", mode, prepared=failure["message"])
                    else:
                        st.caption("질문이 DB에 저장됐을 수 있습니다. 중복 저장 방지를 위해 같은 질문의 자동 재시도는 제공하지 않습니다.")
                st.caption("입력 내용은 위에 유지됩니다. 실패 안내는 AI 답변으로 저장하지 않습니다.")
            if submitting:
                render_message({"role": "user", "content": (prompt or default_question(images, bool(context))) + context,
                                "images": images}, len(st.session_state.messages))
                send_question(prompt, mode, images=images, context=context)



