"""실행: python -m streamlit run main.py"""

from pathlib import Path

import streamlit as st

from src.app.chat import render_chat
from src.app.chat_service import warm_up


def main():
    warm_up()  # 첫 질문의 준비 시간을 미리 끝내 둔다 (백그라운드, 한 번만 실행)
    st.set_page_config(
        page_title="CodeClue",
        page_icon=str(Path(__file__).resolve().parent / "assets" / "codeclue-favicon.png"),
        layout="wide",
        initial_sidebar_state="expanded",
    )
    render_chat()


if __name__ == "__main__":
    main()
