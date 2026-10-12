"""
도구 선택 정확도 시험 세트: 질문마다 "모델이 어떤 도구를 골라야 하는지"를 고정해 둔다.

- 도구의 이름과 설명을 고치거나 프롬프트를 바꾼 뒤, 이 세트로 선택이 망가지지 않았는지 확인한다 (test_tool_selection.py).
- expected: 가장 알맞은 도구. None이면 "도구를 쓰지 않아야 하는 질문"이다.
- ok_tools: expected 말고도 정답으로 인정하는 도구 (질문이 모호해서 둘 이상이 합리적인 경우).
- args: 고른 도구의 인자가 맞는지 확인하는 조건 (선택이 맞을 때만 확인한다). 조건 모양은 아래 eq, contains, contains_all.
- image_analysis: 이미지로 올린 화면에서 멀티모달 노드가 읽은 글을 흉내 낸 것 (질문에는 오류 문구가 없는 경우).
"""

from dataclasses import dataclass, field


def eq(value):
    return ("eq", value)


def contains(text):
    return ("contains", text)


def contains_all(*texts):
    return ("contains_all", texts)


@dataclass(frozen=True)
class Case:
    id: str
    question: str
    expected: str | None
    category: str
    ok_tools: tuple[str, ...] = ()
    args: dict = field(default_factory=dict)
    image_analysis: str = ""


def args_match(arguments: dict, conditions: dict) -> list[str]:
    """어긋난 인자 조건의 목록 (비어 있으면 모두 맞음)."""
    problems = []
    for name, (kind, expected) in conditions.items():
        actual = arguments.get(name)
        text = " ".join(map(str, actual)) if isinstance(actual, list) else str(actual)
        if kind == "eq" and actual != expected:
            problems.append(f"{name}: {actual!r} != {expected!r}")
        elif kind == "contains" and expected.lower() not in text.lower():
            problems.append(f"{name}: {actual!r}에 {expected!r}이 없음")
        elif kind == "contains_all" and not all(t.lower() in text.lower() for t in expected):
            problems.append(f"{name}: {actual!r}에 {expected!r}이 모두 있지는 않음")
    return problems


ERROR_SCREEN = (
    "[화면 설명]\n터미널 오류 화면\n[오류 메시지]\nlanggraph.errors.GraphRecursionError: Recursion limit of 25 reached without hitting a stop condition.\n"
    "[코드]\n없음\n[환경 정보]\nlanggraph==0.6.4, Python 3.12.1\n[읽기 불확실]\n없음"
)
VERSIONS_SCREEN = "[화면 설명]\npip list 화면\n[오류 메시지]\n없음\n[코드]\n없음\n[환경 정보]\nlangchain==1.4.0\nlanggraph==0.2.0\nPython 3.12.1\n[읽기 불확실]\n없음"
IMPORT_SCREEN = (
    "[화면 설명]\n터미널 오류 화면\n[오류 메시지]\nImportError: cannot import name 'create_react_agent' from 'langgraph.prebuilt'\n"
    "[코드]\nfrom langgraph.prebuilt import create_react_agent\n[환경 정보]\n없음\n[읽기 불확실]\n없음"
)
DIAGRAM_SCREEN = "[화면 설명]\n사각형 두 개가 선으로 연결된 그림\n[오류 메시지]\n없음\n[코드]\n없음\n[환경 정보]\n없음\n[읽기 불확실]\n없음"

V, C, S, I, Y, N = (
    "get_latest_version",
    "check_version_compat",
    "search_github_issues",
    "get_github_issue",
    "check_symbol_exists",
    None,
)

CASES: tuple[Case, ...] = (
    # ---- 최신 버전 조회
    Case("ver-1", "langgraph 최신 버전이 뭐야?", V, "최신 버전", args={"package": eq("langgraph")}),
    Case("ver-2", "langchain 최신 버전 알려줘", V, "최신 버전", args={"package": eq("langchain")}),
    Case("ver-3", "mcp 파이썬 SDK는 최신 버전이 언제 나왔어?", V, "최신 버전", args={"package": eq("mcp")}),
    Case("ver-4", "langgraph 레포 최신 릴리스 알려줘", V, "최신 버전", args={"package": eq("langgraph")}),  # 평가표 E08 유형
    Case("ver-5", "langchain-openai 마지막 버전이 뭐야?", V, "최신 버전", args={"package": eq("langchain-openai")}),
    Case("ver-6", "pydantic 최신 버전은?", V, "최신 버전", args={"package": eq("pydantic")}),
    # ---- 호환성 점검
    Case("compat-1", "langchain 1.4.0이랑 langgraph 0.2.0 같이 써도 돼? 파이썬은 3.12야", C, "호환성",
         args={"packages": contains_all("langchain==1.4.0", "langgraph==0.2.0"), "python_version": contains("3.12")}),
    Case("compat-2", "langgraph 1.2.14랑 langchain-core 0.3 호환돼?", C, "호환성", args={"packages": contains_all("langgraph==1.2.14")}),
    Case("compat-3", "mcp 2.3.0 쓰는데 파이썬 3.9에서도 돼?", C, "호환성", args={"packages": contains_all("mcp==2.3.0"), "python_version": contains("3.9")}),
    Case("compat-4", "업그레이드하고 나서 ImportError가 나요. langchain==1.4.0, langgraph==0.3.5 쓰고 있어요", C, "호환성",
         ok_tools=(S,), args={"packages": contains_all("langchain==1.4.0", "langgraph==0.3.5")}),
    Case("compat-5", "pip install langgraph==9.9.9 했더니 No matching distribution found가 나와요", V, "호환성", ok_tools=(C, S)),
    # ---- 이슈 검색
    Case("search-1", "GraphRecursionError 관련 GitHub 이슈 찾아줘", S, "이슈 검색", args={"query": contains("GraphRecursionError")}),
    Case("search-2", "mcp 서버 연결하면 -32601 오류가 나요", S, "이슈 검색", args={"query": contains("32601")}),
    Case("search-3", "GraphRecursionError 해결된 이슈 있어?", S, "이슈 검색", args={"query": contains("GraphRecursionError"), "state": eq("closed")}),
    Case("search-4", "ModuleNotFoundError: No module named 'langgraph.prebuilt' 이 오류 어떻게 해결해?", S, "이슈 검색", ok_tools=(Y,)),
    Case("search-5", "langchain에서 create_react_agent가 deprecated 됐다는 이슈 있어?", S, "이슈 검색"),
    Case("search-6", "아직 안 닫힌 langgraph checkpointer 버그 이슈 보여줘", S, "이슈 검색", args={"state": eq("open")}),
    # ---- 이슈 상세
    Case("issue-1", "langgraph 이슈 9163번 내용이랑 댓글 알려줘", I, "이슈 상세", args={"repo": eq("langchain-ai/langgraph"), "number": eq(9163)}),
    Case("issue-2", "python-sdk 이슈 12번 읽어줘", I, "이슈 상세", args={"repo": eq("modelcontextprotocol/python-sdk"), "number": eq(12)}),
    Case("issue-3", "langchain-ai/langchain 이슈 #30001 해결됐는지 알려줘", I, "이슈 상세", args={"repo": eq("langchain-ai/langchain"), "number": eq(30001)}),
    Case("issue-4", "https://github.com/langchain-ai/langchain/pull/12345 이 PR 내용 알려줘", I, "이슈 상세", args={"repo": eq("langchain-ai/langchain"), "number": eq(12345)}),  # 이슈 도구가 PR도 읽는다
    # ---- 심볼 존재 확인
    Case("symbol-1", "langgraph.graph.magic_autofix_everything 함수 사용법 알려줘", Y, "심볼 확인", args={"symbol": contains("magic_autofix_everything")}),  # 평가표 E07 유형
    Case("symbol-2", "langchain create_agent 함수 시그니처 알려줘", Y, "심볼 확인", args={"symbol": contains("create_agent")}),
    Case("symbol-3", "from langgraph.prebuilt import create_react_agent 이거 아직 되나요?", Y, "심볼 확인", ok_tools=(S,), args={"symbol": contains("create_react_agent")}),
    Case("symbol-4", "mcp.Client 클래스가 있어?", Y, "심볼 확인", args={"symbol": contains("mcp.Client")}),
    Case("symbol-5", "langgraph에 StateGraph.compile_all 메서드 있나요?", Y, "심볼 확인", args={"symbol": contains("compile_all")}),
    # ---- 도구를 쓰지 않아야 하는 질문
    Case("none-1", "오늘 점심 뭐 먹을까?", N, "도구 불필요"),
    Case("none-2", "langchain 1.0으로 올리면 뭐가 바뀌었어?", N, "도구 불필요"),  # 변경 내용은 이 도구들이 모른다
    Case("none-3", "저번에 말한 거 이어서 설명해줘", N, "도구 불필요"),
    Case("none-4", "StateGraph에서 Node가 하는 일을 설명해줘", N, "도구 불필요"),  # 개념 설명은 문서 검색의 일
    Case("none-5", "파이썬 리스트와 튜플의 차이를 알려줘", N, "도구 불필요"),
    Case("none-6", "안녕하세요", N, "도구 불필요"),
    # ---- 이미지에서 읽은 글이 함께 오는 경우 (질문에는 오류 문구나 버전이 없다)
    Case("image-1", "이 오류 해결해줘", S, "이미지", image_analysis=ERROR_SCREEN, args={"query": contains("GraphRecursionError")}),
    Case("image-2", "내 환경 버전들 문제 없어?", C, "이미지", image_analysis=VERSIONS_SCREEN, args={"packages": contains_all("langchain==1.4.0", "langgraph==0.2.0")}),
    Case("image-3", "이거 왜 안 돼?", Y, "이미지", ok_tools=(S,), image_analysis=IMPORT_SCREEN, args={"symbol": contains("create_react_agent")}),
    Case("image-4", "이 그림 설명해줘", N, "이미지", image_analysis=DIAGRAM_SCREEN),
)


# 어려운 질문 (정확도 기준에는 넣지 않고 보고만 한다): 모호하거나, 도구가 없는 편이 맞거나, 주소나 PR처럼 형식이 다른 경우.
# 여기서 틀리는 것은 "아직 못 하는 것"의 목록이다. 고쳐지면 CASES로 옮긴다.
HARD_CASES: tuple[Case, ...] = (
    Case("hard-1", "langgraph 1.2.14 릴리스 노트 알려줘", N, "어려움", ok_tools=(V,)),  # 도구는 노트 내용을 모른다 (링크만)
    Case("hard-2", "mcp 서버를 처음부터 만드는 방법 알려줘", N, "어려움"),
    Case("hard-3", "내가 쓰는 langgraph가 최신인지 확인해줘. 지금 0.6.4야", V, "어려움", args={"package": eq("langgraph")}),
    Case("hard-4", "langgraph랑 langchain 둘 다 최신으로 올리면 서로 호환돼?", V, "어려움", ok_tools=(C,)),  # 버전을 모르는 상태
    Case("hard-5", "recursion_limit을 올려도 GraphRecursionError가 계속 나요", S, "어려움", args={"query": contains("GraphRecursionError")}),
    Case("hard-6", "이 이슈 읽어줘 https://github.com/langchain-ai/langgraph/issues/9163", I, "어려움", args={"repo": eq("langchain-ai/langgraph"), "number": eq(9163)}),
    Case("hard-8", "LangGraph 1.0에서 없어진 함수 목록 알려줘", N, "어려움"),
    Case("hard-9", "mcp.server.fastmcp.FastMCP가 2.x에도 있나요?", Y, "어려움", args={"symbol": contains("FastMCP")}),
    Case("hard-10", "pip로 langgraph 설치가 안 돼요. 파이썬은 3.8이에요", V, "어려움", ok_tools=(C,)),  # 지원 Python 버전 확인이 답
)
