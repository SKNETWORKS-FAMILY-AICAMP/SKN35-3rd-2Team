"""Chat UI; OpenAI requests go through the team's LangGraph."""
import streamlit as st

from src.const.config import OPEN_MODEL
from src.app.chat_service import chat_result, run_chat, run_db_chat, text_content
from src.prompt.chat_prompt import CHAT_SYSTEM_PROMPT


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
    if sources:
        with st.expander("참고한 문서"):
            for source in sources:
                st.link_button(source.get("title") or source["url"], source["url"])


def render_chat():
    st.session_state.setdefault("messages", [])
    st.title("AI 개발 도우미")
    st.caption("개발하다 궁금한 점을 질문하고, 답변을 확인하세요.")
    with st.expander("현재 사용할 수 있는 기능"):
        st.markdown(
            "- **일반 질문**: 질문과 답변을 주고받습니다.\n"
            "- **문서 검색 · 외부 조회 · 이미지 분석**: 준비 중입니다.\n"
            "- **연습 모드**: AI 호출 없이 화면 동작을 확인합니다."
        )
    with st.sidebar:
        st.header("대화 설정")
        mode = st.selectbox("답변 모드", ["OpenAI AI 답변", "연습 모드", "NVIDIA AI 답변"])
        if mode == "OpenAI AI 답변":
            st.caption(f"모델: {OPEN_MODEL}")
        if st.session_state.get("previous_mode", mode) != mode:
            st.session_state.messages = []
            st.session_state.conversation_id = None
        st.session_state.previous_mode = mode
        if st.button("대화 초기화", icon=":material/delete:"):
            st.session_state.messages = []
            st.session_state.conversation_id = None
        st.caption("모드를 바꾸면 대화가 초기화됩니다. 대화는 현재 접속에서만 유지됩니다.")
        if st.session_state.get("user_id") is None:
            st.caption("로그인 화면은 준비 중입니다. 현재 대화는 DB에 저장하지 않습니다.")
        else:
            st.caption("OpenAI 모드의 질문과 답변은 현재 사용자의 대화에 저장됩니다.")
    if mode == "연습 모드":
        st.info("연습 모드: API 호출 없이 질문 입력과 대화 표시를 확인합니다.")
    elif mode == "NVIDIA AI 답변":
        st.info("NVIDIA 모델로 일반 답변을 제공합니다.")
    else:
        st.info("일반 질문에 답변합니다. 문서 검색·외부 조회·이미지 분석은 준비 중입니다.")
    if not st.session_state.messages:
        with st.container(border=True):
            st.markdown("**어떤 점이 궁금하신가요?**")
            st.markdown(
                "LLM 호출 중 `RateLimitError: Error code: 429`가 발생했어요. 원인과 해결 방법을 알려줘.\n\n"
                "Pinecone에 임베딩을 저장할 때 `Vector dimension 3072 does not match the dimension of the index 1536` 오류가 나요. 어떻게 해결하나요?"
            )
            st.caption("비밀번호나 API 키 같은 민감한 정보는 입력하지 마세요.")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            render_sources(message.get("sources", []))
    if prompt := st.chat_input("질문을 입력해 주세요", submit_mode="disable"):
        if prompt.strip():
            user_message = {"role": "user", "content": prompt.strip()}
            with st.chat_message("user"):
                st.markdown(user_message["content"])
            with st.chat_message("assistant"):
                with st.spinner("입력을 확인하는 중…" if mode == "연습 모드" else "AI 답변 생성 중…"):
                    result = generate_answer(
                        st.session_state.messages + [user_message], mode,
                        user_id=st.session_state.get("user_id"),
                        conversation_id=st.session_state.get("conversation_id"),
                    )
                if result.get("conversation_id") is not None:
                    st.session_state.conversation_id = result["conversation_id"]
                if result["status"] == "success":
                    st.markdown(result["answer"])
                    render_sources(result["sources"])
                    st.session_state.messages.extend([
                        user_message, {"role": "assistant", "content": result["answer"], "sources": result["sources"]},
                    ])
                    st.rerun()
                elif result["status"] == "unsupported":
                    st.info(result["error"]["message"])
                else:
                    st.error(result["error"]["message"])
