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
