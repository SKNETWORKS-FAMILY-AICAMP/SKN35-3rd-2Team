"""채팅 화면과 사용자 입력 처리. main.py에서 render_chat()을 호출합니다."""
import streamlit as st

from src.const.config import OPENAI_MODEL
from src.prompt.chat_prompt import CHAT_SYSTEM_PROMPT


@st.cache_resource
def get_openai_client():
    from src.const.models import create_openai_client
    return create_openai_client(timeout=60)


@st.cache_resource
def get_model():
    from src.const.config import NVIDIA_API_KEY, NVIDIA_MODEL
    from src.const.models import create_nvidia_model
    if not NVIDIA_API_KEY or not NVIDIA_MODEL:
        raise ValueError("NVIDIA 설정이 필요합니다.")
    return create_nvidia_model(timeout=60)


def generate_answer(messages, mode):
    """나중에 이 함수를 팀의 LangGraph 호출로 교체합니다."""
    if mode == "연습 모드":
        return (
            f"입력한 질문: {messages[-1]['content']}\n\n"
            "질문을 정상적으로 받았습니다. 지금은 화면 동작을 확인하는 연습 모드입니다. "
            "실제 AI 답변은 왼쪽에서 OpenAI 또는 NVIDIA 모드를 선택하면 받을 수 있습니다."
        )
    if mode == "OpenAI AI 답변":
        model_name = OPENAI_MODEL
        response = get_openai_client().responses.create(
            model=model_name,
            instructions=CHAT_SYSTEM_PROMPT,
            input=messages,
            max_output_tokens=1000,
            store=False,
        )
        if not response.output_text.strip():
            raise ValueError("빈 응답입니다.")
        return response.output_text
    response = get_model().invoke(
        [{"role": "system", "content": CHAT_SYSTEM_PROMPT}] + messages
    )
    # 텍스트 블록 형태의 응답도 표시할 수 있게 정규화합니다.
    content = response.content
    if isinstance(content, str):
        answer = content
    else:
        answer = "\n".join(
            block if isinstance(block, str) else block.get("text", "")
            for block in content
            if isinstance(block, (str, dict))
        )
    if not answer.strip():
        raise ValueError("빈 응답입니다.")
    return answer



def render_chat():
    # Streamlit은 입력할 때마다 파일 전체를 다시 실행합니다.
    # session_state에 저장하면 같은 접속 안에서 대화를 유지할 수 있습니다.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("AI 개발 도우미")
    st.caption("LangChain · LangGraph · MCP 개발 질문을 입력해 보세요.")

    with st.sidebar:
        st.header("대화 설정")
        mode = st.selectbox("답변 모드", ["OpenAI AI 답변", "연습 모드", "NVIDIA AI 답변"])
        if mode == "OpenAI AI 답변":
            st.caption(f"모델: {OPENAI_MODEL}")
        if st.session_state.get("previous_mode", mode) != mode:
            st.session_state.messages = []
        st.session_state.previous_mode = mode
        if st.button("대화 초기화", icon=":material/delete:"):
            st.session_state.messages = []
        st.caption("모드를 바꾸면 대화가 초기화됩니다. 대화는 현재 접속에서만 유지됩니다.")

    if mode == "연습 모드":
        st.info("연습 모드: API 호출 없이 질문 입력과 대화 표시를 확인합니다.")
    elif mode == "NVIDIA AI 답변":
        st.info("NVIDIA 모델로 답변합니다. 문서 검색과 외부 정보 조회는 아직 연결 전입니다.")
    else:
        st.info("OpenAI 모델로 답변합니다. 문서 검색과 외부 정보 조회는 아직 연결 전입니다.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("예: LangGraph의 State는 무엇인가요?", submit_mode="disable"):
        if prompt.strip():
            user_message = {"role": "user", "content": prompt.strip()}
            with st.chat_message("user"):
                st.markdown(user_message["content"])
            with st.chat_message("assistant"):
                try:
                    with st.spinner("입력을 확인하는 중…" if mode == "연습 모드" else "AI 답변 생성 중…"):
                        answer = generate_answer(st.session_state.messages + [user_message], mode)
                    st.markdown(answer)
                except Exception as error:
                    # 외부 오류 메시지에 인증 정보가 들어갈 수 있어 그대로 노출하지 않습니다.
                    error_name = type(error).__name__
                    if mode == "OpenAI AI 답변":
                        if error_name == "AuthenticationError":
                            message = "OpenAI 인증에 실패했습니다. OPENAI_API_KEY가 유효한지 확인해 주세요."
                        elif error_name == "RateLimitError":
                            message = "OpenAI 사용 한도 또는 요청 제한에 도달했습니다. API 잔액과 사용 한도를 확인해 주세요."
                        elif error_name == "NotFoundError":
                            message = "설정된 OpenAI 모델을 사용할 수 없습니다. OPENAI_MODEL과 모델 접근 권한을 확인해 주세요."
                        else:
                            message = "답변을 받지 못했습니다. OPENAI_API_KEY, OPENAI_MODEL과 인터넷 연결을 확인해 주세요."
                    else:
                        message = "답변을 받지 못했습니다. NVIDIA_API_KEY, NVIDIA_MODEL과 인터넷 연결을 확인해 주세요."
                    st.error(message)
                else:
                    st.session_state.messages.extend([
                        user_message,
                        {"role": "assistant", "content": answer},
                    ])
