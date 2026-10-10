"""실행: python -m streamlit run main.py"""
import streamlit as st

from src.app.chat import render_chat


def main():
    st.set_page_config(
        page_title="AI 개발 도우미 | LLM/RAG 오류 해결",
        page_icon=":material/code:",
        layout="wide",
        initial_sidebar_state="auto",
    )
    render_chat()


if __name__ == "__main__":
    main()
