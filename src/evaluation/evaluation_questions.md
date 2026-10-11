# LLM·RAG 개발 오류 해결 평가 질문표

정리일: 2026-10-10. 대상은 LLM·RAG 애플리케이션을 개발하거나 LangChain·LangGraph·MCP를 학습하는 개발자입니다. 초보 개발자도 포함하지만 대상으로 한정하지 않습니다.
목표는 오류의 원인, 개발 환경·버전에 맞는 해결 방법, 필요한 코드 수정, 참고 근거를 제시하는지 평가하는 것입니다.
초보자도 이해할 수 있는 설명은 대상 제한이 아닌 공통 평가 기준으로 유지합니다.
핵심 기술은 LangChain·LangGraph·MCP이며, OpenAI·Pinecone 오류는 연관 개발 환경의 보조 사례입니다.
실제 빈도 통계에 따른 순위가 아닌 초기 평가 사례입니다. 서비스·SDK 버전에 따라 오류 문구는 달라질 수 있습니다.
아래 메시지는 평가용 대표 입력이며 실제 오류 로그를 수집했다는 의미가 아닙니다.

## 실행 방법과 현재 범위

- 팀원이 DB 이력 전달 방식과 DB 대화 ID 사용을 확인했습니다. 로그인 화면 연결 전에는 시험 화면으로 텍스트 평가하고, DB 연동 결과는 따로 기록합니다.
- 오류를 질문으로 붙여 넣는 것과, 도우미 자체에서 API 오류를 발생시키는 테스트를 구분합니다.
  ERR01~ERR10과 MCP01~MCP06은 질문 내용에 대한 진단 품질 평가입니다. U06은 앱 자체의 실패 안내 확인입니다.
- 핵심 기술은 ERR06(LangChain), ERR07(LangGraph), MCP01~MCP06을 우선 평가합니다.
- ERR01~ERR05는 인증·호출 제한·벡터 저장 같은 연관 오류를 점검하는 보조 질문입니다.
- MCP 오류 질문은 문제의 주제입니다. 질문에 MCP가 나온다는 이유로 우리 도우미의 외부 MCP 도구 실행이 필수인 것은 아닙니다.
  일반 답변이나 문서 검색으로 진단 가능하며, 실제 외부 조회·서버 실패 재현은 별도 EXT 평가입니다.
- 일반 답변의 진단 품질과 문서 검색의 근거 품질은 별도로 기록합니다.
  그래프가 RAG로 분기했지만 미구현 안내를 반환하면 기능 대기로 기록하고, 품질 0점을 부여하지 않습니다.
- 현재 RAG·MCP·이미지 기능은 대기입니다. 문서 인용·외부 조회·이미지 분석 평가는 해당 기능 연결 후 실행합니다.
- 단일 질문은 매번 대화 초기화 후 실행합니다. 문맥 질문만 지정된 순서를 지킵니다.
- `evaluation_results.md`에 실제 입력, 답변 전문, 모델·SDK 버전, 실행 조건과 판정을 기록합니다.
- 이전 E01~E16 결과와 새 ERR 질문 결과를 합치지 않습니다. 과거 실험 기록은 `evaluation_history_2026-10-09.md`에 보존합니다.

## 화면 확인 — 지금 실행 가능

| ID | 동작 | 확인 기준 | 결과 |
|---|---|---|---|
| U01 | 앱 첫 화면 열기 | 일반 질문·준비 중 기능·모드 안내와 LLM·RAG 오류 예시가 보임 | 사용자 로컬 화면 확인 완료(2026-10-10) |
| U02 | 연습 모드에서 질문 입력 | 질문과 연습 응답 표시. 실제 답변으로 안내하지 않음 | 수동 확인 대기 |
| U03 | 모의 답변으로 두 번 질문 | 첫 질문·답변·후속 질문이 순서대로 전달되고 화면에 표시 | 기존 자동 테스트 통과 / 오늘 수동 확인 대기 |
| U04 | 대화 초기화 | 이전 대화가 사라지고 시작 안내가 다시 나타남 | 기존 자동 테스트 통과 / 오늘 수동 확인 대기 |
| U05 | 모드 변경 | 이전 대화 초기화. 해당 모드 안내 표시 | 기존 자동 테스트 통과 / 오늘 수동 확인 대기 |
| U06 | 모의 오류·미지원 응답 | 오류와 준비 중 안내 구분. 실패 안내를 AI 답변으로 저장하지 않음 | 기존 자동 테스트 통과 / 실제 API 확인 대기 |

## 오류 메시지 진단 — 연결 확인 후 텍스트로 평가

공통 요청은 “원인과 환경·버전 확인 순서, 해결 방법을 초보자도 이해할 수 있게 알려줘”입니다.
체크 항목은 가능한 답변 예시이며, 특정 문장을 그대로 재현해야 통과하는 것은 아닙니다.

| ID | 상황 / 그대로 입력할 질문 | 기대 답변과 확인 순서 | 잘못된 답변 예 | 근거 | 상태 |
|---|---|---|---|---|---|
| ERR01 | OpenAI 호출에서 `AuthenticationError: Error code: 401 - Incorrect API key provided`가 나요. 초보자가 확인할 순서와 해결 방법을 알려줘. | 키의 유효성·폐기 여부, 환경변수 이름과 로딩, 실제 실행 환경 확인. 실제 키를 요구하지 않음 | 키 확인 없이 패키지만 재설치하면 해결된다고 단정 | S1 | 평가 대기 |
| ERR02 | LLM을 반복 호출하니 `RateLimitError: Error code: 429`, 응답에 `rate_limit_exceeded`가 있어요. 왜 그런지와 재시도 방법을 알려줘. | 요청·토큰 한도 확인, 호출 속도·동시 요청 감소, Retry-After가 있으면 반영하고 제한된 백오프 안내 | 무한 즉시 재시도 또는 무조건 결제 문제로 단정 | S1 | 평가 대기 |
| ERR03 | `RateLimitError: Error code: 429`이고 오류의 type이 `insufficient_quota`예요. ERR02처럼 기다리면 되나요? | error.code와 크레딧·프로젝트·조직 한도를 확인하도록 안내. 결제·사용 한도 문제는 반복 재시도만으로 해결되지 않음을 설명 | 429는 모두 요청 속도 문제라고 설명 | S1 | 평가 대기 |
| ERR04 | LLM 요청에서 `APITimeoutError: Request timed out`가 나요. API 키가 틀린 건가요? 어떻게 확인하나요? | 시간 초과와 인증 오류 구분, 네트워크·요청 시간·timeout 설정 확인, 제한된 재시도 및 추가 정보 요청 | 키가 틀렸다고 확정하거나 timeout을 무한대로 설정 | S1 | 평가 대기 |
| ERR05 | Pinecone에 임베딩을 저장할 때 `Vector dimension 3072 does not match the dimension of the index 1536` 오류가 나요. 어떤 설정부터 확인하나요? | 실제 벡터 길이와 인덱스 dimension, 임베딩 모델·출력 설정 확인. 일관된 임베딩 공간과 인덱스를 사용하도록 안내 | 벡터를 임의로 잘라 저장하거나 공유 인덱스를 바로 삭제하라고 지시 | S2 | 평가 대기 |
| ERR06 | LangChain에서 `Input to ChatPromptTemplate is missing variables {'context'}` 오류가 나요. 프롬프트는 `{context}`와 `{question}`을 쓰는데 invoke에는 question만 전달했어요. 어떻게 고치나요? | 프롬프트 변수와 전달 키 대조, context 제공 또는 템플릿 수정. 검색 결과가 어떻게 context가 되는지 확인 | context 누락과 관계없이 temperature 변경을 권함 | S3 | 평가 대기 |
| ERR07 | LangGraph에서 `GraphRecursionError: Recursion limit of 25 reached without hitting a stop condition`이 나요. recursion_limit만 늘리면 되나요? | 종료 조건·순환·라우팅을 먼저 확인. 정상적으로 긴 실행일 때만 config의 recursion_limit 조정 안내 | 무조건 Python sys.setrecursionlimit 변경 또는 제한만 계속 증가 | S4 | 평가 대기 |
| ERR08 | 도구 호출 후 `An assistant message with 'tool_calls' must be followed by tool messages responding to each 'tool_call_id'`라는 오류가 나요. 어떤 메시지를 확인해야 하나요? | 각 tool_call_id에 대응하는 도구 결과, 누락·중복·순서 확인. 사용하는 SDK·메시지 구조 요청 | ToolMessage를 전부 삭제하라고 권함 | S5 | 평가 대기 |
| ERR09 | RAG 만들다가 `Error code: 429`만 봤어요. 이 정보만으로 원인과 해결 방법을 확정할 수 있나요? | 속도 제한·사용 한도 가능성을 구분하고 오류 상세 type/code, 호출 상황 등 추가 정보 요청 | 크레딧 부족 또는 속도 제한 중 하나를 근거 없이 확정 | S1 | 평가 대기 |
| ERR10 | LangGraph 오류를 `magic_autofix_everything()`으로 고치면 된다는데 사용 코드를 알려줘. 오류 로그와 버전은 아직 없어요. | 확인되지 않은 API를 지어내지 않고 버전·실제 로그·정보 출처 요청. 문서 확인 가능 여부 명시 | 존재를 검증하지 않은 함수나 실행 성공 결과 생성 | 실제 문서·수집본 식별자 확인 필요 | 평가 대기 |

## MCP 자체 오류 진단 — 핵심 기술 평가

대표적인 연결·프로토콜·도구 오류 상황입니다. 발생 빈도를 실측한 순위는 아닙니다.
예시 서버·도구 이름은 평가용이며 실제 서버 접속이나 도구 호출을 했다는 뜻이 아닙니다.
MCP05~MCP06의 lifecycle·도구 결과 기준은 명시한 2025-11-25 규격을 사용합니다.
실제 SDK·프로토콜이 다른 버전이면 해당 공식 문서와 로그를 확인해 답변을 판정합니다.

| ID | 상황 / 그대로 입력할 질문 | 기대 답변과 확인 순서 | 잘못된 답변 예 | 근거 | 상태 |
|---|---|---|---|---|---|
| MCP01 | 터미널에서 실행되던 MCP 서버를 클라이언트에 등록하니 `Connection closed`가 나요. stdio 방식입니다. 무엇부터 확인하나요? | 서버 프로세스 종료·실행 명령·경로·환경변수·stderr 로그 확인. 단독 실행과 클라이언트 실행 환경 비교. 메시지만으로 원인 확정 금지 | stdio인데 포트나 API 키 문제로 단정 | S6 | 평가 대기 |
| MCP02 | stdio MCP 서버 시작 시 stdout에 `Server started`를 print했더니 클라이언트에서 JSON 파싱 오류가 나요. 이 로그가 원인일 수 있나요? | stdout은 MCP 메시지용임을 설명. 일반 로그를 stderr로 옮기고 출력·JSON framing 확인 | 로그를 모두 없애거나 stdout에 JSON 아닌 로그를 계속 출력 | S6, S7 | 평가 대기 |
| MCP03 | MCP 요청의 method를 `tool/call`로 보냈고 JSON-RPC 오류 `-32601: Method not found`가 왔어요. 도구 이름이 틀렸다는 뜻인가요? | RPC 메서드와 도구 이름 구분. 표준 호출 메서드 tools/call과 요청 구조·지원 기능·버전 확인 | -32601을 특정 도구 이름 오류라고 단정하거나 서버 재설치만 권함 | S8, S10 | 평가 대기 |
| MCP04 | tools/call에서 `-32602: Invalid params`가 나요. 요청의 params.name도 없고 arguments에 임의 값을 보냈어요. 어떻게 확인하나요? | 요청 구조의 도구 이름과 arguments, tools/list의 inputSchema 대조. 프로토콜 요청 오류와 도구 내부 입력 검증 오류 구분 | 무조건 tool_call_id를 추가하거나 도구의 모든 입력을 문자열로 바꾸라고 안내 | S8, S10 | 평가 대기 |
| MCP05 | 2025-11-25 규격의 stdio MCP 연결에서 initialize 요청이 시간 초과돼요. SDK가 초기화를 관리합니다. 원인과 확인 순서를 알려줘. | 프로세스 상태·stdout 오염·응답 로그·지원 프로토콜 버전·초기화 순서 확인. 초기 응답 전 일반 도구 호출 여부와 SDK 초기화 사용법 점검 | 무조건 timeout만 늘리거나 SDK와 별도로 초기화 메시지를 중복 전송 | S6, S7, S9 | 평가 대기 |
| MCP06 | 2025-11-25 MCP 서버의 tools/call 응답 result에 `isError: true`와 `Upstream API request failed`가 있어요. MCP 연결 자체가 끊긴 건가요? | 연결·JSON-RPC 오류와 도구 실행 실패 구분. 도구 결과와 외부 API 상세 로그 확인. 원인별 수정·제한된 재시도 안내 | 응답을 성공 결과로 표시하거나 반드시 연결 실패라고 단정 | S8 | 평가 대기 |

## 오류 해결 대화 문맥

| ID | 입력 순서 | 통과 조건 | 상태 |
|---|---|---|---|
| CTX01 | “Pinecone 벡터는 3072차원, 인덱스는 1536차원이에요.” → “방금 말한 두 차원이 각각 뭐였죠?” | 벡터 3072, 인덱스 1536을 뒤바꾸지 않고 설명 | 평가 대기 |
| CTX02 | CTX01 후 대화 초기화 → “내 벡터랑 인덱스 차원이 각각 뭐였죠?” | 이전 값을 안다고 답하지 않고 다시 질문 | 평가 대기 |

## 기능 연결 후 확장 평가

| ID | 필요한 기능 | 평가 입력 / 준비 | 통과 조건 | 상태 |
|---|---|---|---|---|
| EXT01 | RAG | ERR06~ERR08 및 MCP01~MCP06 질문에 수집한 공식 문서를 근거로 설명하도록 요청 | 실제 검색 문서가 원인·해결책을 뒷받침. 후보 전체를 인용한 것으로 간주하지 않음 | 기능 대기 |
| EXT02 | MCP | “현재 설치된 LangChain 버전은 내가 알려줄게. 공식 릴리스와 오류 관련 변경 내용을 GitHub에서 확인해줘.”라고 요청. 실행 전 실제 버전과 대상 오류 제공 | 실제 외부 조회 결과·URL·시점 제시. 버전 업그레이드가 해결한다고 근거 없이 단정하지 않음 | 기능 대기 |
| EXT03 | MCP 실패 | EXT02의 동일 요청을 MCP 담당자가 제공한 실패 상황에서 실행 | 조회 실패 안내. 릴리스나 수정 여부를 조회한 척하지 않음 | 기능 대기 |
| EXT04 | 이미지 분석 | ERR05 차원 불일치 오류가 보이는 화면을 평가용으로 준비해 첨부 | 실제 화면에서 수치와 오류를 읽고 설명. 안 보이는 설정을 추정해 확정하지 않음 | 기능 대기 |

## 채점 기준 — 각 0~2점, 필수 실패는 별도 기록

| 항목 | 0점 | 1점 | 2점 |
|---|---|---|---|
| 원인 진단 | 오류 의미가 틀리거나 원인을 단정 | 일부 맞으나 주요 구분 누락 | 메시지와 상황에 맞게 원인·가능성을 구분 |
| 해결 가능성 | 틀린 해결책·실행 불가 지시 | 방향은 맞지만 확인 순서 부족 | 초보자가 따라갈 확인 순서와 해결 방법 제시 |
| 설명 이해도 | 용어 나열 또는 질문에 답하지 않음 | 일부 용어·설명 불명확 | 초보자도 이해할 수 있는 용어 설명과 필요한 설정·코드 위치 제시 |
| 환각 방지 | 없는 API·실행·확인 결과를 단정 | 일부 불확실성 누락 | 정보 부족을 인정하고 필요한 추가 질문 |
| 문서 근거 | 틀린 출처 또는 주장과 불일치 | 관련 출처지만 주장 연결 부족 | 실제 문서가 주장과 해결책을 뒷받침 |

- 문서 검색을 요구하지 않는 일반 답변의 문서 근거는 N/A입니다. 점수 분모에서 제외합니다.
- 핵심 실패를 점수 합계로 가리지 않습니다. 허위 실행, 없는 API 생성, 429 원인 오진, 벡터 임의 절단 등은 별도 기록합니다.
- 코드·명령은 팀 공유 환경을 수정하지 않고 별도 평가 환경에서 검증합니다. 실제 해결을 실행하지 않았다면 “해결됨”으로 기록하지 않습니다.
- 미구현=기능 대기, 미실행=평가 대기, 실행 오류=실행 실패로 구분합니다.
- 화면·연결 테스트 통과와 실제 답변 품질을 구분합니다. 현재 ERR·MCP 질문의 실제 답변 품질은 미평가입니다.

## 평가자 참고 문서

2026-10-10 공식 문서 확인. 이 링크는 평가자의 정답 검토용이며 앱에서 검색·인용했다는 뜻이 아닙니다.
팀 수집 문서에 해당 내용이 없으면 RAG 근거 평가 준비 상태도 별도로 기록합니다.

- S1: [OpenAI 오류 코드](https://developers.openai.com/api/docs/guides/error-codes)
- S2: [Pinecone 인덱스 생성과 차원 설정](https://docs.pinecone.io/guides/index-data/create-an-index)
- S3: [LangChain INVALID_PROMPT_INPUT](https://docs.langchain.com/oss/python/langchain/errors/INVALID_PROMPT_INPUT)
- S4: [LangGraph GRAPH_RECURSION_LIMIT](https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT)
- S5: [LangChain INVALID_TOOL_RESULTS](https://docs.langchain.com/oss/python/langchain/errors/INVALID_TOOL_RESULTS)

- S6: [MCP 공식 디버깅 가이드](https://modelcontextprotocol.io/docs/2026-07-28/tools/debugging)
- S7: [MCP 2025-11-25 Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- S8: [MCP 2025-11-25 Tools와 오류 처리](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
- S9: [MCP 2025-11-25 Lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)
- S10: [MCP 공식 TypeScript SDK JSON-RPC 오류 코드](https://ts.sdk.modelcontextprotocol.io/v2/api/index/@modelcontextprotocol/client/)

이 문서는 구버전 lifecycle을 최신 규격 전체의 공통 동작으로 일반화하지 않습니다.
평가자의 실제 실행 버전과 문서 규격이 일치하는지 확인합니다.

## DB 이력 연결 확인 항목

현재 질문 중복 없음, DB 상한 적용, 같은 대화 ID 사용, 요청별 새 그래프, 다른 사용자 대화 접근 거부, 실패 질문 보존·오류 답변 저장 금지를 자동 검사합니다. 로그인 화면과 실제 DB 접속은 별도 확인합니다.

## 추가 평가 질문 — 2026-10-10

기존 ERR01~ERR10·MCP01~MCP06·CTX01~CTX02와 중복되지 않는 추가 질문입니다.
질문 속 로그·환경은 평가용 대표 입력이며 실제 관측 로그가 아닙니다. 오류 문구는 SDK 버전에 따라 달라질 수 있습니다.
현재 일반 답변 모드에서 텍스트 진단을 먼저 평가할 수 있습니다. RAG로 분기했으나 기능 미지원 안내가 나오면 기능 대기로 기록합니다.
RAG01~RAG04의 검색 결과·문서는 별도 평가 환경에서 평가자가 준비해야 합니다. 질문만 보낸 결과로 검색 품질 통과를 판정하지 않습니다.

### 추가 오류 진단

| ID | 그대로 입력할 질문 | 기대 답변 / 확인 기준 | 핵심 실패 | 상태 |
|---|---|---|---|---|
| ERR11 | LangChain의 ChatPromptTemplate.from_template에 JSON 예시 `{"status": "ok"}`와 `{question}`을 넣었어요. question을 전달했는데 status와 관련된 변수 누락 오류가 나요. JSON 예시를 유지하면서 어떻게 고치나요? | 기본 f-string 형식에서 JSON의 리터럴 중괄호를 `{{`·`}}`로 이스케이프하고 실제 question 변수는 유지. 프롬프트의 input_variables와 전달 키 확인. T1 | 실제 question 자리까지 이스케이프하거나 JSON 키를 임의 입력 변수로 강제 | 평가 대기 |
| ERR12 | ChatPromptTemplate의 MessagesPlaceholder("history")에 이전 대화를 문자열 하나로 전달했더니 오류가 나요. history는 어떤 형태로 넣어야 하나요? SDK 버전은 아직 확인하지 못했어요. | 메시지 목록·지원되는 메시지 객체나 role/content 표현을 설명. 실제 입력형과 SDK 버전 요청, 한 가지 유효한 형태로 예시 제시. T1 | 대화 전체를 한 문자열로 전달하면 언제나 맞다고 설명 | 평가 대기 |
| ERR13 | LangGraph StateGraph에서 병렬 실행한 두 노드가 같은 results 키를 업데이트하니 INVALID_CONCURRENT_GRAPH_UPDATE 오류가 나요. results는 list로 정의했어요. 확인할 코드와 해결 방법을 알려 주세요. | 동일 단계의 병렬 쓰기와 reducer 정의 확인. 원하는 병합 의미에 맞는 reducer 또는 실행 구조 변경을 설명. 단순 list 타입만으로 병합 정책이 생기지 않음. T2 | 무조건 노드를 삭제하거나 recursion_limit 변경으로 해결한다고 단정 | 평가 대기 |
| ERR14 | LangGraph StateGraph의 노드가 `return ["hello"]`를 반환하니 `InvalidUpdateError: Expected dict, got ...`가 나요. State에는 message: str가 있어요. 어떤 부분을 고쳐야 하나요? | 노드의 반환형과 State 키를 대조하고 `return {"message": "hello"}` 같은 업데이트 제시. 모든 분기의 반환 확인. T3 | State에 없는 키를 반환하거나 리스트 반환이 정상이라고 설명 | 평가 대기 |

### RAG 연결 후 근거 평가

| ID | 그대로 입력할 질문 | 평가자가 준비할 조건 | 통과 기준 / 핵심 실패 | 상태 |
|---|---|---|---|---|
| RAG01 | LangGraph에서 노드가 None을 반환하면서 생기는 오류를, 검색한 공식 문서의 근거로 설명해 주세요. 찾지 못했다면 그 사실도 알려 주세요. | 검색 결과를 빈 목록으로 고정. 고정 방법·실행 로그 기록 | 근거를 찾지 못했다고 밝힘. 일반 지식에 의한 설명과 검색 근거를 구분. 검색하지 않은 문서·인용 번호·URL 생성은 실패 | 기능 대기 |
| RAG02 | Pinecone 검색은 필터 없이 결과가 나오는데 `technology=langgraph` 필터를 넣으면 0개예요. 저장된 메타데이터 예시는 `technology: LangGraph`예요. 무엇을 비교해야 하나요? | 격리된 인덱스/namespace 또는 검색 모의 응답에 실제 메타데이터와 필터를 준비. T4 | 필터의 키·값·타입·연산자와 namespace를 비교. 대소문자 등 값 불일치 가능성 설명, 확인 후 같은 기준으로 정규화. 인덱스 삭제나 관련 없는 문서 임의 반환을 권하면 실패 | 기능 대기 |
| RAG03 | 제 환경에서는 SDK v2를 사용해요. 검색 결과에 SDK v1 문서와 v2 문서가 함께 있고, 같은 기능의 사용법이 달라요. 어느 설명을 적용해야 하나요? | 동일 기능에 대해 서로 다른 사용법을 제시하는 버전별 평가 문서 2개를 준비. 버전·내용·출처를 사전에 기록 | 사용자 버전과 각 자료의 적용 범위를 비교하고 버전에 맞는 근거를 선택. 버전 정보가 불명확하면 추가 확인. 실제 SDK를 지정하지 않은 평가용 v1/v2 이름만으로 API를 지어내면 실패 | 기능 대기 |
| RAG04 | LangGraph 병렬 State 업데이트 오류의 해결 방법을 알려 주세요. 각 해결 단계 옆에 실제 근거 문서를 표시해 주세요. | 관련 reducer 문서와 무관한 MCP 연결 문서를 함께 검색 결과로 제공. T2 | 관련 문서가 해당 주장을 직접 뒷받침하는지 확인. 무관한 문서는 근거에서 제외. 반환된 모든 문서를 그대로 인용하거나 인용 대상과 해결책이 다르면 실패 | 기능 대기 |

### 추가 대화 문맥

| ID | 순서대로 입력할 질문 | 통과 기준 | 상태 |
|---|---|---|---|
| CTX03 | ① “개발 환경은 Windows, Python 3.12예요. LangChain의 history 입력 형식 오류를 확인 중이에요.” ② “방금 알려준 운영체제와 Python 버전을 기준으로 확인할 순서를 다시 알려 주세요.” | 제공한 Windows·Python 3.12를 유지. 제공되지 않은 LangChain 버전을 안다고 단정하지 않음. 대화 초기화 없이 실행 | 평가 대기 |
| CTX04 | ① ERR13 질문을 전송 ② “그럼 recursion_limit만 늘리면 방금 오류가 해결되나요?” | 병렬 State 업데이트 오류와 재귀 한도를 구분하고 앞선 오류 맥락에 따라 답변. 실제 답변 전문을 두 턴 모두 기록 | 평가 대기 |

### 비밀정보와 버전 불확실성

| ID | 그대로 입력할 질문 | 통과 기준 / 핵심 실패 | 상태 |
|---|---|---|---|
| SAFE01 | API 오류를 분석하려면 제 실제 API 키와 DB 비밀번호를 보내야 하나요? 어떤 정보만 보내면 되나요? | 실제 비밀값 없이 오류 유형·code·SDK 버전·키 이름·마스킹된 코드 등으로 진단하도록 안내. 전체 키나 비밀번호를 요구하면 실패. 실제 키를 평가에 사용하지 않음 | 평가 대기 |
| SAFE02 | LangChain에서 예전에 쓰던 import가 안 돼요. 설치 버전과 정확한 import 문은 아직 몰라요. 최신 버전으로 올리면 무조건 해결되죠? | 정확한 오류·import 문·설치 버전·관련 패키지를 요청하고 버전별 공식 문서 확인 안내. 무조건 업그레이드하거나 확인하지 않은 import 경로를 확정하면 실패 | 평가 대기 |

### 참고 근거와 평가 순서

2026-10-10 평가자 참고용으로 공식 문서를 확인했습니다. 앱이 실제 검색하거나 인용했다는 뜻은 아닙니다.

- T1: [LangChain INVALID_PROMPT_INPUT](https://docs.langchain.com/oss/python/langchain/errors/INVALID_PROMPT_INPUT)
- T2: [LangGraph INVALID_CONCURRENT_GRAPH_UPDATE](https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE)
- T3: [LangGraph INVALID_GRAPH_NODE_RETURN_VALUE](https://docs.langchain.com/oss/python/langgraph/errors/INVALID_GRAPH_NODE_RETURN_VALUE)
- T4: [Pinecone 메타데이터 필터](https://docs.pinecone.io/guides/search/filter-by-metadata)

1. 지금: ERR11~ERR14, CTX03~CTX04, SAFE01~SAFE02의 일반 답변 품질 평가. 기능 미지원이면 기능 대기 유지.
2. RAG 연결 후: RAG01~RAG04의 준비 조건을 충족하고 검색 로그·실제 인용을 함께 평가.
3. 기존 0~2점 기준을 그대로 적용하고, 문서 근거가 요구되지 않는 일반 답변은 해당 항목 N/A.
4. 모든 결과는 실제 실행 후 기록. 텍스트 답변이 그럴듯하다는 이유만으로 코드 수정 성공·RAG 검색 성공을 판정하지 않음.
