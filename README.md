.
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
