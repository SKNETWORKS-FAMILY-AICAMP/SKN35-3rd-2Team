"""실행: python -m streamlit run main.py"""

from pathlib import Path

import streamlit as st

from src.app.chat import render_chat


def main():
    st.set_page_config(
        page_title="CodeClue",
        page_icon=str(Path(__file__).resolve().parent / "assets" / "codeclue-favicon.png"),
        layout="wide",
        initial_sidebar_state="expanded",
    )
    render_chat()


if __name__ == "__main__":
    main()
