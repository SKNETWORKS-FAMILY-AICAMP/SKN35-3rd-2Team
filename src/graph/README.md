# 채팅 UI ↔ LangGraph 입력·출력 규약

작성일: 2026-10-09
대상: C:\sk-encoa\SKN35-3rd-2Team
상태: 일반 답변 그래프와 UI 연결 구현 완료. 모의 모델·검색을 사용한 그래프·화면 테스트 20개 통과. 실제 API 답변 품질 평가는 별도 진행한다.

## 1. 현재 구현과 연결 목표

현재 UI의 `generate_answer(messages, mode)`는 모델을 직접 호출하고 문자열을 반환한다.
`workflow()`는 컴파일된 그래프를 만들며, `graph.invoke()`의 반환값은 전체 State다.
일반·최종 답변 노드는 `messages`에 AIMessage를 추가하지만 `State.answer`는 채우지 않는다.

UI와 그래프 사이의 `src/graph/chat_service.py`에 `run_chat(messages)` 어댑터를 구현했다.
어댑터가 State를 만들고 그래프를 호출한 뒤 화면용 결과로 정리한다.
텍스트 일반 답변과 RAG를 연결했다. RAG는 기존 Pinecone 인덱스를 검색한 뒤 최종 답변으로 연결한다. MCP·이미지는 구현 후 확장한다.

## 2. UI가 전달할 입력

`messages`: 오래된 순서로 정렬한 `[{"role": ..., "content": ...}]`.

- role: `user`, `assistant`; DB 요약이 있으면 첫 항목에 `system`도 허용한다.
- content: 문자열. 현재 단계에서는 이미지 블록을 받지 않는다.
- 마지막 메시지는 이번 질문인 `user` 메시지여야 하고 내용이 비어 있으면 안 된다.
- 현재 질문은 한 번만 들어간다. 문자열이 같다는 이유로 메시지를 제거하지 않는다.

```python
messages = [
    {"role": "user", "content": "지금부터 LangGraph를 공부할게"},
    {"role": "assistant", "content": "좋아요. 궁금한 점을 물어보세요."},
    {"role": "user", "content": "이 프레임워크에서 State는 뭐야?"},
]
```

UI의 현재 방식은 `st.session_state.messages + [user_message]`를 전달하면 된다.
DB를 붙인 뒤에는 질문 저장 후 `get_history_context()`가 돌려준 이력을 전달한다.
이 이력에는 이미 현재 질문이 포함되므로 다시 붙이지 않는다. DB 이력은 마스킹·길이 제한이 적용될 수 있어 원래 입력과 완전히 같다고 가정하지 않는다.

사용자 ID·대화 ID·사용자 메시지 ID는 호출하는 쪽에서 관리한다. 그래프가 DB에 접속하거나 소유자 권한을 판단하지 않는다.

## 3. 어댑터가 생성할 그래프 State

| 필드 | 전달값 | 의미 |
|---|---|---|
| messages | 입력 메시지 전체 | 현재 질문까지 포함한 대화 문맥 |
| original_question | 마지막 user 메시지의 content | 이번 답변의 대상 질문 |
| image | None | 이미지 연결 전 |
| image_analysis | 빈 문자열 | 이번 질문의 이미지 분석 결과 초기화 |
| retrieved_docs | 빈 리스트 | 이번 질문의 검색 결과 초기화 |
| mcp_results | 빈 리스트 | 이번 질문의 외부 도구 결과 초기화 |
| answer | 빈 문자열 | 최종 답변 초기화 |

```python
state_input = {
    "messages": messages,
    "original_question": messages[-1]["content"],
    "image": None,
    "image_analysis": "",
    "retrieved_docs": [],
    "mcp_results": [],
    "answer": "",
}
```

`route`, `reason`은 Supervisor가 결정한다. UI가 지정하지 않는다.
선택 필드는 노드에서도 `state.get(...)`으로 읽어 직접 그래프를 호출해도 누락 때문에 실패하지 않게 한다.

## 4. 대화 이력과 체크포인터

이번 연결은 **호출하는 쪽이 매번 필요한 전체 이력을 전달**하는 방식으로 한다.
그래프의 `MessagesState`는 메시지를 누적하므로 전체 이력을 동일한 체크포인터 thread에 계속 넣으면 중복될 수 있다.

권장 구현: `workflow()`에서 체크포인터 없이 컴파일하고 UI/DB가 이력을 관리한다.
기존 `InMemorySaver`를 유지해야 한다면 호출마다 새 요청 UUID를 thread_id로 사용한다.
이 경우 thread_id는 DB conversation_id와 별개다. 기존 예제의 고정 `user_001`을 UI에서 공유하지 않는다.
두 방식을 섞지 않는다. 새 질문에서는 검색·이미지·도구 결과도 새로 시작한다.

## 5. UI가 받을 출력

어댑터는 아래 필드를 항상 반환한다. 전체 State나 AIMessage를 UI 반환값으로 쓰지 않는다.

| 필드 | 형식 | 규칙 |
|---|---|---|
| status | `success`, `unsupported`, `error` | 처리 완료 / 아직 없는 기능 / 실행 실패 |
| answer | 문자열 | success일 때 비어 있지 않은 최종 답변. 그 외에는 빈 문자열 |
| sources | dict 리스트 | 일반 답변이면 `[]`. 답변에서 [n]으로 인용한 검색 문서만 포함 |
| image_analysis | 문자열 또는 None | 분석하지 않았으면 None |
| error | dict 또는 None | success이면 None. 나머지는 code와 사용자 안내 message |

```python
# 정상 반환 예시 (실제 실행 결과가 아님)
{
    "status": "success",
    "answer": "State는 그래프의 노드들이 읽고 갱신하는 공유 상태입니다.",
    "sources": [],
    "image_analysis": None,
    "error": None,
}

# 미구현 분기 예시
{
    "status": "unsupported",
    "answer": "",
    "sources": [],
    "image_analysis": None,
    "error": {"code": "UNSUPPORTED_ROUTE", "message": "문서 검색 기능은 아직 연결 중입니다."},
}
```

현재 노드는 `answer`를 채우지 않으므로 첫 연결에서는 최종 반환 messages의 마지막 항목이 AIMessage인지 확인한 뒤 그 content를 답변으로 변환한다.
문자열 또는 텍스트 블록만 추출하고, assistant 메시지가 없거나 텍스트가 비면 error로 처리한다. 사용자 입력이나 도구 메시지를 답변으로 표시하지 않는다.
이후 일반·최종 답변 노드가 `answer`도 채우게 바꾸면 어댑터는 해당 값을 사용한다.
예외 원문은 UI 반환값에 넣지 않는다. 미구현 route는 실행 오류와 구분해 안내한다.

success일 때만 assistant 메시지를 화면 이력과 DB에 추가한다.
DB 연결 이후에는 질문을 먼저 저장하므로 실패해도 사용자 메시지가 DB에 남는다. 실패 안내를 AI 답변으로 저장하지 않는다.

## 6. 출처 형식: 기존 DB와 동일하게

```python
{
    "url": "실제로 검색된 문서의 URL",
    "title": "문서 제목",
    "tech": "langgraph",
    "version": None,
    "doc_type": "documentation",
    "snippet": "실제 근거 발췌문",
    "score": 0.9,
}
```

| 검색 Document | 출력 source |
|---|---|
| metadata.source_url | url |
| metadata.title | title |
| metadata.technology | tech |
| metadata.version | version |
| metadata.document_type | doc_type |
| page_content의 근거 발췌 | snippet |
| metadata.score | score |

없는 버전·점수는 None으로 둔다. URL이 없는 문서는 URL을 지어내지 않고 DB에 저장할 sources에서 제외한다.
검색 후보 전체가 답변을 뒷받침한다고 가정하지 않는다. sources는 답변에 사용한 문서를 전달하며 근거 검증 여부를 임의로 설정하지 않는다.

## 7. 구현 범위와 확인 기준

1. 그래프 분기를 현재 지원 기능으로 제한하거나 미구현 route를 unsupported로 처리한다.
2. 선택 State 필드 누락을 보완하고 체크포인터 정책을 적용한다.
3. 입력 검증·State 생성·답변 추출·실패 변환을 담당하는 어댑터를 작성한다.
4. UI의 실제 답변 경로에서 어댑터를 호출한다.
5. E10, E11을 gpt-4o-mini로 재평가한다.

확인 기준: 일반 질문 정상 응답, 두 번째 질문 문맥 유지, 현재 질문 중복 없음, 대화 초기화 후 이전 문맥 없음, 미구현 분기 안내, API 실패·빈 응답 처리.

모델명 통일만으로 조건이 같아지지는 않는다. 평가 기록에는 모델, 프롬프트, temperature, 대화 이력, 검색 사용 여부도 기록한다. 현재 팀 그래프 모델은 temperature=0.0이고 UI의 직접 OpenAI 호출은 temperature를 지정하지 않는다.

## 구현 확인

- `workflow()`는 체크포인터 없이 컴파일한다.
- MCP·이미지 route는 END로 종료한 뒤 어댑터가 unsupported로 반환한다. RAG route는 검색 후 answer로 연결한다.
- Supervisor에는 후속 질문 판단을 위해 전체 대화 이력을 전달한다.
- 선택 State 필드 누락을 보완했다.
- OpenAI UI는 OPEN_MODEL을 표시하고 팀 그래프를 호출한다.
- 연습 모드와 NVIDIA 직접 호출은 유지했다.
- 테스트: `python -m pytest tests/graph -v -p no:cacheprovider`, 20개 통과.
- E10·E11 실제 API 품질 재평가는 아직 수행하지 않았다.

## RAG 연결 (2026-10-09)

- `rag_node`는 `PineconeHybridRetriever`를 직접 사용한다. 인덱스 자동 생성·초기화 함수는 호출하지 않는다.
- 최근 대화(현재 질문 제외)를 사용한 Query Rewrite와 Hybrid 검색으로 상위 5개를 조회한다. 답변에 넣을 본문은 총 6000자로 제한한다.
- 검색 실패 시 RAG_ERROR로 반환하고 답변 모델은 호출하지 않는다. 결과가 없으면 근거 부족을 안내한다.
- 답변은 문서 번호 [n]을 인용하도록 요청한다. 제공 문서에서 실제 URL을 찾아 `sources`로 변환하며, 인용되지 않은 후보나 잘못된 번호는 출처로 표시하지 않는다. 인용 정확성은 별도 검증 대상이다.
- UI는 참고 문서 링크를 보여주고 화면을 다시 실행해도 링크를 유지한다.
- 로컬 사전 확인: OpenAI 키 있음, BM25 파일 있음, Pinecone 키 없음. 실제 Pinecone 검색과 답변 품질은 미검증이다. 키를 저장소나 채팅에 올리지 말고 로컬 .env에 설정한다.
