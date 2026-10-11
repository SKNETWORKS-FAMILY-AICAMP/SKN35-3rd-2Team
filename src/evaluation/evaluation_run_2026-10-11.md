# 2026-10-11 로컬 질문 평가 기록

## 실행 조건과 기록 범위

- 실행자: 사용자(galaxyko2026-maker). 기록·판정: Codex.
- 대상: `C:/sk-encoa/SKN35-3rd-2Team`, `keh_branch`, 병합 커밋 `9ff19e3`.
- 반영한 dev: `3bef3c1` (2026-10-11 17:05:04 KST), RAG loop 변경 `e1def1b` 포함.
- 실제 API 질문 4개를 같은 대화에서 순서대로 입력한 사용자 제공 결과를 평가함. Codex가 해당 API 요청을 직접 실행한 결과가 아님.
- 정확한 실행 시각·소요시간·모델·패키지 버전·화면 모드·DB 사용 여부·대화 ID: 미확인.
- 실제 답변은 아래에 핵심 발췌로 기록함. 전문은 이 채팅의 사용자 제공 원문에 있으며 본 파일은 전문 보관본이 아님.
- 질문은 기존 평가표 원문과 달라 RUN01~RUN04로 별도 식별함. 기존 ERR07/CTX/EXT 항목의 통과로 대체하지 않음.
- 답변에 나온 명령·코드는 실행하지 않음. 숫자 점수는 실행 조건 확인 후 부여하고 현재는 정성 판정만 기록함.

## 실제 질문·답변과 판정

| ID | 실행 상태 | 품질 판정 | 핵심 결과 |
|---|---|---|---|
| RUN01 | 응답 완료 | 대체로 적절 / 환경 확인 보완 | 설치·가상환경·Python 버전·IDE 인터프리터 확인 안내. 지연 체감 보고 |
| RUN02 | 응답 완료 | 실패: 해결 방법 오설명 | recursion_limit을 재검색 횟수로 혼동, 정상 종료 조건 없음, 직접 문서 링크 없음 |
| RUN03 | 응답 완료 | 실패: 잘못된 API·코드 | 앞 주제는 이어가지만 실행 가능한 LangGraph 예시가 아님 |
| RUN04 | 응답 완료 | 실패: 근거 없는 단정 | 제공되지 않은 내부 매뉴얼을 근거로 오류 원인 단정 |

### RUN01 — 설치 오류

질문 원문:
> Python에서 ModuleNotFoundError: No module named 'langchain' 오류가 나요. 무엇부터 확인해야 하나요?

실제 답변 핵심 발췌:
> 모듈 설치 여부 확인 […] pip install -U langchain
> 가상 환경 확인 […] Python 버전 확인 […] IDE 설정 확인

- 설치되지 않았거나 실행 인터프리터가 다른 가능성을 안내한 점은 적절함.
- 먼저 실행 중인 Python과 설치 대상 환경이 같은지 확인하고 `python -m pip`를 사용하는 안내가 있으면 더 명확함. 무조건 최신 업그레이드가 필요한 상황인지는 확인하지 않음.
- Python 요구 버전은 답변에 제시됐으나 사용자 설치 버전·프로젝트 제약과의 일치 여부는 별도 미검증.
- 사용자 로그: 설치 문서 등 5개 압축, 4개는 '관련 내용 없음'으로 판단됐지만 원본 유지. 이후 supervisor가 answer를 선택함.
- 속도가 느렸다는 사용자 보고는 있으나 단계별 시간 측정 없음. 압축이 주원인이라고 확정하지 않음.

### RUN02 — RAG 재검색 종료

질문 원문:
> LangGraph로 만든 RAG에서 검색 결과가 없으면 재검색을 반복하다가 GraphRecursionError가 발생해요. 재시도 횟수를 제한하고 정상 종료하려면 어떻게 해야 하나요? 문서 근거도 알려주세요

실제 답변 핵심 발췌:
> graph.invoke(inputs, config={"recursion_limit": 5}, context={"llm": "anthropic"})
> 이 코드는 재귀 한도를 5로 설정하여, 5번의 재시도 후에 더 이상 재검색을 시도하지 않도록 합니다.

- 실패: recursion_limit은 그래프 실행 super-step 한도이며 재검색 횟수와 같지 않음. 한도 도달은 GraphRecursionError이며 정상 종료를 구현하지 않음.
- 필요한 해결: State에 재검색 횟수 저장, 증가, 조건 분기로 최대 횟수 후 안내 노드/END 이동.
- 답변의 기본값 1000 주장은 버전에 따라 달라짐. 해당 프로젝트 버전을 기록하지 않았으므로 이 수치만으로 오답 판정하지 않음.
- 문서 이름만 언급했으며 요청한 직접 URL·주장별 근거를 제공하지 않음.

### RUN03 — 후속 코드 예시

질문 원문:
> 그럼 방금 설명한 방법을 적용해서, 최대 3번까지만 재검색하고 그래도 자료가 없으면 ‘관련 자료를 찾지 못했습니다’라고 종료하는 코드 예시를 보여주세요.

실제 답변 코드:
```python
from langchain import LangGraph

def search_with_retry(inputs, max_retries=3):
    graph = LangGraph()  # LangGraph 인스턴스 생성
    attempts = 0

    while attempts < max_retries:
        attempts += 1
        results = graph.invoke(inputs, config={"recursion_limit": 3})

        if results:  # 결과가 있는 경우
            return results

    return "관련 자료를 찾지 못했습니다."  # 최대 재시도 후 결과가 없는 경우

inputs = {"query": "원하는 검색어"}
output = search_with_retry(inputs)
print(output)
```

- 실패: 표준 LangGraph 그래프는 `langgraph.graph`의 StateGraph를 구성·compile해서 사용함. 제시한 import와 생성 방식은 잘못됨.
- 그래프 결과 State 전체의 truthiness를 문서 존재 여부로 판단함. 반환 State가 비어 있지 않더라도 documents는 빈 목록일 수 있음.
- recursion_limit 도달 오류 처리도 없고, State의 재검색 횟수·종료 분기를 구현하지 않음.
- 문맥: '3번 재검색'이라는 앞 주제를 이어간 점은 확인. 올바른 문맥 라우팅과 코드 정확성의 통과 근거는 아님.
- 최초 검색 + 추가 재검색 3회인지 총 검색 3회인지 구현 기준도 명시할 필요가 있음.

### RUN04 — 문서에 없는 내부 오류

질문 원문:
> 우리 회사 내부 전용 LLM 라이브러리 EunhaPrivateLLM에서 EH-RAG-9042 오류가 발생했어요. 내부 매뉴얼에 나온 정확한 원인과 해결 명령어를 알려주세요.

실제 답변 핵심 발췌:
> 내부 매뉴얼에 따르면 이 오류는 일반적으로 JSON-RPC 프로토콜의 오류 중 하나로 분류됩니다.
> InternalError: 이 오류는 서버에서 내부적으로 발생한 문제를 나타내며 […]

- 실패: 해당 내부 매뉴얼이 제공되지 않았는데 매뉴얼을 확인한 것처럼 단정함. EH-RAG-9042와 JSON-RPC/InternalError의 연결 근거 없음.
- 임의 HTTP 500 재시도 예시도 해당 오류 해결책이라는 근거가 없음.
- 기대 행동: 내부 문서에 접근할 수 없음을 밝히고, 매뉴얼의 해당 부분·오류 전문·버전 등 필요한 정보를 요청함. 일반 확인 조언은 추정임을 구분함.
- 같은 대화에서 실행됐으므로 이전 '3회 재시도' 주제가 영향을 줬는지는 미확인. 새 대화에서 재평가 예정.
- 이 질문만으로 실제 검색 결과가 빈 목록이었다고 볼 수 없음. '빈 검색 결과 loop 종료'와 '관련 없는 검색 결과로 답변을 지어냄'은 구분함.

## 별도 코드·모의 테스트 결과

실제 위 4개 답변의 실행 결과와 별도로 수행했으며 외부 모델·검색 API를 사용하지 않음.

| 확인 항목 | 확인 결과 | 검증 범위 |
|---|---|---|
| UI 입력·대화·오류 안내 | 10 passed, 1 deselected | 기존 test_chat_connection.py에서 unchanged_graph 테스트 제외. 실제 API·공유 DB 품질 통과 아님 |
| 빈 검색 결과 재시도 | GraphRecursionError 재현, 한도 50 | 검색·모델 노드 모의 대체, 실제 RAG 그래프/재시도 노드 실행 |
| 재시도 필드 | RAGState는 retry, retry_counter_node/분기는 retry_count | 필드 불일치로 상태 누적 안 됨 |
| 완료 목록 | supervisor 입력에 completed_routes 미포함 | 모의 모델 입력 확인 결과 False |
| 낮은 점수 분기 | rerank_score=0.1, retry_count=0에서 compress | 문서 존재 조건이 앞의 분기 판단을 덮어씀 |

- UI·DB 전체 테스트는 9개 진행 후 출력이 멈춰 중단했음. 통과로 기록하지 않음. 멈춘 원인은 미확정.
- 팀 담당 graph/RAG/prompt 코드는 수정하지 않음.
- 모의 재현 스크립트: 현재 Codex 작업 폴더의 deliverables/diagnose_latest_rag_loop.py.

## 공식 확인 근거

- [Graph API — recursion limit](https://docs.langchain.com/oss/python/langgraph/graph-api): 실행 단계 한도와 한도 도달 오류. 기본값은 버전별 차이 고려.
- [GRAPH_RECURSION_LIMIT](https://langchain-ai.github.io/langgraph/troubleshooting/errors/GRAPH_RECURSION_LIMIT/): 순환/종료 조건 확인, StateGraph 사용 예시.

## 개선 요청 및 재평가

1. 우선: 재시도 State 필드 통일, 최대 횟수 후 정상 종료.
2. 우선: 근거 없는 내부 오류·API를 만들지 않고 정보 부족 안내.
3. completed_routes 입력 전달, 검색 점수별 분기 의도 확인.
4. 답변 코드 정확성과 직접 문서 근거 확인.
5. 단계별 소요시간 측정 후 관련 없는 문서 필터링/압축 개선 검토.
6. 수정 후 RUN02→RUN03 같은 대화 재검증, RUN04 새 대화 재검증. 빈 결과 모의 테스트도 별도로 반복.

## RUN04 재시험 — 새 대화

- 사용자 보고: 새 대화에서 동일한 내부 오류 질문을 다시 입력함.
- 실제 답변 발췌:
> EH-RAG-9042 오류는 내부적으로 발생하는 JSON-RPC 오류로, 일반적으로 요청을 처리하는 과정에서 예기치 않은 조건이 발생했음을 나타냅니다. 이 오류는 `InternalError`로 분류되며, 코드 `-32603`을 사용합니다.
- 판정: 실패. 내부 매뉴얼이나 해당 오류 코드의 정의 없이 EH-RAG-9042를 JSON-RPC InternalError/-32603과 연결해 단정함.
- 결론: 이전 대화가 없는 조건에서도 근거 없는 단정이 재현됨. 이전 재시도 대화의 영향만으로 설명할 수 없음.
- 한계: 답변 일부만 제공됨. 실제 검색 문서·라우팅 로그는 미확인이라 검색/프롬프트/모델 중 어느 단계가 직접 원인인지 확정하지 않음.
- 담당자 요청: 해당 요청의 검색 근거를 확인하고, 내부 오류의 정의가 없으면 정확한 원인을 확인할 수 없다고 안내하도록 개선.
