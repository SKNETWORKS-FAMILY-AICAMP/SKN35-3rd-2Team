```
├── README.md
├── data
│ ├── processed
│ │ ├── langchain # 전처리된 LangChain 문서
│ │ ├── langgraph # 전처리된 LangGraph 문서
│ │ └── mcp # 전처리된 MCP 문서
│ └── raw
│ ├── langchain # LangChain 원본 문서
│ ├── langgraph # LangGraph 원본 문서
│ └── mcp # MCP 원본 문서
├── main.py
├── pyproject.toml
├── src
│ ├── app # 애플리케이션 및 사용자 인터페이스
│ ├── const
│ │ ├── config.py # 환경변수 및 프로젝트 설정
│ │ └── models.py # LLM / Embedding / Reranker 모델 설정
│ ├── db # 관계형 DB 연결 및 데이터 처리
│ ├── evaluation # RAG 및 답변 품질 평가
│ ├── graph
│ │ ├── node # LangGraph에서 실행되는 개별 노드
│ │ ├── state.py # LangGraph State 정의
│ │ ├── supervisor.py # 작업 분기 및 라우팅 판단
│ │ └── workflow.py # LangGraph 전체 워크플로우 구성
│ ├── mcp_integration
│ │ ├── client # MCP Server 연결 및 Tool 호출
│ │ └── server # MCP Server 및 Tool 구현
│ ├── preprocessing # 문서 전처리 및 데이터 정제
│ ├── prompt # LLM 프롬프트 관리
│ ├── rag
│ │ ├── context_compressor.py # 검색 결과 Context 압축
│ │ ├── loader.py # 문서 로딩
│ │ ├── multi_query.py # Multi-Query 생성
│ │ ├── query_rewrite.py # 사용자 질문 재작성
│ │ ├── rerank.py # 검색 결과 재정렬
│ │ ├── retriever.py # 문서 검색
│ │ ├── rrf.py # 검색 결과 RRF 통합
│ │ └── splitter.py # 문서 Chunk 분할
│ └── vectorstore # Vector DB 저장 및 검색 관리
└── uv.lock
```

# 첫 채팅 화면 실행하기

## 1. 실행

프로젝트 폴더의 PowerShell에서 실행합니다.

```powershell
cd C:\sk-encoa\SKN35-3rd-2Team
.\.venv\Scripts\python.exe -m streamlit run .\main.py
```

터미널에 표시된 Local URL을 브라우저에서 여세요. 보통 http://localhost:8501 입니다. 서버를 종료하려면 터미널에서 Ctrl+C를 누릅니다.

## 2. API 없이 화면부터 확인

왼쪽에서 선택한 '연습 모드'에서 '안녕하세요'를 입력하세요. 입력한 질문과 확인 응답이 보이면 기본 화면이 동작한 것입니다. 두 번째 질문도 입력해 대화가 누적되는지 확인한 뒤 '대화 초기화'를 누르세요.

연습 응답은 AI 답변이 아니므로 평가 점수를 매기지 않습니다.

## 3. 실제 AI 답변 확인

기본값인 'OpenAI AI 답변'은 .env의 OPENAI_API_KEY를 사용합니다. 팀 그래프와 채팅 화면은 OPEN_MODEL을 사용합니다(기본값: gpt-4o-mini). 팀 LangGraph의 Supervisor가 대화와 질문을 받아 일반 답변 또는 최종 답변으로 연결합니다. 그래프 모델은 OPEN_MODEL을 사용합니다(기본값: gpt-4o-mini). NVIDIA를 사용하려면 왼쪽에서 'NVIDIA AI 답변'을 선택하세요. 프로젝트 .env에 NVIDIA_API_KEY와 NVIDIA_MODEL이 설정되어 있어야 합니다. 기존 src/const/models.py의 생성 함수를 사용합니다. 질문을 보낼 때 외부 모델 API가 호출됩니다.

우선 평가표 E10, 이어서 E11을 실행하고 답변을 기록하세요. 일반 답변과 RAG 문서 검색을 연결했습니다. MCP·이미지 입력은 아직 연결 전입니다.

## 4. 코드 이해하기

- st.chat_input: 사용자가 질문을 입력하는 칸입니다.
- st.chat_message: 사용자와 AI의 메시지를 표시합니다.
- st.session_state.messages: 같은 접속에서 대화를 기억합니다. DB 저장은 아니므로 접속이 새로 만들어지면 사라질 수 있습니다.
- generate_answer: 답변을 만드는 함수입니다. 현재는 연습 응답, OpenAI 팀 그래프 또는 NVIDIA 직접 호출을 하고, OpenAI 모드는 팀의 LangGraph를 호출하고 status·answer·sources 형식으로 결과를 반환합니다.
- st.spinner: 실제 답변을 기다리는 동안 처리 상태를 표시합니다.

API 요청이 실패하면 안내 메시지가 나오며 실패한 질문은 대화 기록에 추가하지 않습니다. 설정을 수정했다면 Ctrl+C로 서버를 종료하고 다시 실행하세요.

## 5. 팀과 다음에 합의할 것

백엔드 함수의 질문·대화 기록 입력 형식과 답변·출처·상태 반환 형식을 합의하세요. 현재 일반 답변 그래프가 연결되었습니다. RAG는 Pinecone 문서를 검색한 뒤 근거와 함께 답변합니다. MCP/이미지는 준비 중 안내를 표시합니다.


## 파일별 역할

- main.py: 실행 진입점으로 채팅 화면을 호출합니다.
- src/app/chat.py: 질문 입력, 대화 표시, 응답 처리를 담당합니다.
- src/const/config.py: 프로젝트 루트의 .env와 모델 설정을 읽습니다.
- src/const/models.py: OpenAI 클라이언트와 NVIDIA 모델을 생성합니다.
- src/prompt/chat_prompt.py: 일반 답변 프롬프트를 관리합니다.
- src/evaluation/evaluation_questions.md: 평가 질문과 실행 기록을 관리합니다.


## 그래프 연결 확인

OpenAI 모드는 `src/graph/chat_service.py`의 `run_chat()`을 통해 팀 그래프를 실행합니다. 전체 이력을 호출마다 전달하며 그래프 체크포인터는 사용하지 않습니다. RAG 분기는 문서 검색 후 최종 답변으로 연결됩니다. MCP·이미지 분기는 준비 중 안내를 반환합니다. DB 저장은 아직 연결 전입니다.

입력·출력 규약은 `src/graph/README.md`에 정리했습니다. 연결 테스트는 `python -m pytest tests/graph -q`로 실행합니다. 실제 API 없이 모의 응답으로 입력·분기·문맥 전달·초기화·오류 표시를 검증합니다. 실제 답변 품질은 gpt-4o-mini로 E10·E11을 재평가해야 합니다.


## RAG 연결 확인

서버를 재시작한 뒤 OpenAI 모드에서 '공식 문서를 검색해서 LangGraph의 State를 설명해줘'를 입력합니다. 답변의 [1] 표기와 '참고한 문서' 링크를 확인하세요. Pinecone API 키, 기존 인덱스, data/processed/bm25_params.json이 필요합니다. 채팅 중 인덱스를 생성·초기화하지 않습니다. 결과가 없으면 근거 부족을 안내하고, 검색 실패는 오류로 표시합니다. 다중 검색과 로컬 재정렬은 이번 연결에서 사용하지 않습니다. 문서 번호를 인용한 검색 결과만 출처로 표시하며, 인용의 정확성은 직접 문서와 대조해야 합니다.
