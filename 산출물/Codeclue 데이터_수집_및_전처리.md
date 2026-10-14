# CodeClue 데이터 수집 및 전처리

## 1. 데이터 개요

### 1-1. 데이터 출처

사용자가 LangChain / LangGraph / MCP 로 개발하다 겪는 오류를 해결하도록, 세 기술의 **공식 문서 원본(.mdx)** 을 수집하여 RAG 검색 데이터로 사용한다. 웹페이지를 크롤링하는 대신 문서 사이트가 빌드되는 **GitHub 원본 저장소**의 `.mdx` 를 그대로 받는다.

| 데이터 | 출처 (GitHub 원본) | 문서 사이트 (출처 링크) | 형식 | 사용 여부 |
|--------|------|------|------|-----------|
| LangChain | `langchain-ai/docs` → `src/oss/langchain/` | `docs.langchain.com/oss/python/langchain/` | MDX | ✅ 사용 |
| LangGraph | `langchain-ai/docs` → `src/oss/langgraph/` | `docs.langchain.com/oss/python/langgraph/` | MDX | ✅ 사용 |
| MCP | `modelcontextprotocol/modelcontextprotocol` → `docs/docs/2026-07-28/`, `docs/specification/2026-07-28/` (최신 버전만) | `modelcontextprotocol.io/` | MDX | ✅ 사용 |
| 코드 예제 (snippets) | `langchain-ai/docs` → `src/snippets/` | (본문에 삽입되어 함께 사용) | MDX | ✅ 사용 (LangChain·LangGraph 본문에 합침) |

- 저장소·경로 근거: `collect_docs.py` 의 `collect_langchain()` / `collect_langgraph()` / `collect_mcp()`, `mdx_to_document.py` 의 `GITHUB_SOURCES`, `WEB_SOURCES`, `collect_snippets.py` 의 `REPOSITORY = "langchain-ai/docs"`
- **Python 문서만 사용**한다. 문서 안의 JavaScript/TypeScript 블록과 예제는 전처리에서 제거한다.

### 1-2. 청킹 전략

| 데이터 | 청킹 전략 | 청킹 단위 |
|--------|-----------|-----------|
| LangChain / LangGraph / MCP 공통 | **Markdown 구조 기반 청킹** (제목 경계 우선, 코드 블록 보존) | 최대 1,000자, 긴 문단만 overlap 150자 |

문서 1개(`.mdx` 1개) = Document 1개로 만든 뒤, 제목(`#`)·코드 블록(```` ``` ````)·문단 경계를 지키며 청크로 나눈다. 세 기술 모두 같은 Markdown 형식으로 정리되므로 같은 전략을 쓴다. (상세: 5장)

### 1-3. 데이터 수량

| 구분 | Document (`documents.jsonl` 행 수) | 본문 글자 수 합계 | 코드 블록 수 | 청크 수 | 청크 비율 |
|------|----------:|----------:|----------:|----------:|:---:|
| LangChain | **55** | 947,518 | 1,067 | **1,307** | 33.4% |
| LangGraph | **38** | 698,872 | 706 | **993** | 25.3% |
| MCP | **53** | 1,152,585 | 493 | **1,618** | 41.3% |
| **합계** | **146** | 2,798,975 | 2,266 | **3,918** | 100% |

- 청크 수 3,918 은 `bm25_params.json` 의 `n_docs = 3918`(BM25 를 학습한 청크 수)과 일치한다. 전체 build 는 같은 청크로 BM25 를 학습하고 업로드하였으며, Pinecone 에 올라간 청크도 3,918개이다.
- **원본 파일은 148개**(LangChain 57, LangGraph 38, MCP 53)이고, 모두 `.mdx` 다. `mdx_to_document` 실행 결과 LangChain 의 `academy.mdx`, `retrieval.mdx` 2개가 정리 후 본문 30자 미만(`본문 없음, 건너뜀`)으로 빠져 **Document 는 146개**가 되었다. LangGraph·MCP 는 대상 전부 변환되었다.
- 코드 예제(snippets)는 **148개**다. `collect_snippets` 실행 결과 `수집 대상 예제 개수: 148`, 저장 위치 `data/raw/snippets` 로 출력되었고, `[n/148]` 다운로드 줄이 없어 148개 모두 이미 받아 둔 상태였다. LangChain·LangGraph 문서가 import 하는 Python 예제 경로 수이며(JS/TS 제외), 별도 Document 가 아니라 본문에 삽입된다.

**문서 유형별 분포**

| 기술 | documentation | error | specification | tutorial | 합계 |
|---|---:|---:|---:|---:|---:|
| LangChain | 48 (청크 1,294) | 7 (청크 13) | — | — | 55 |
| LangGraph | 32 (청크 978) | 6 (청크 15) | — | — | 38 |
| MCP | 20 (청크 529) | — | 30 (청크 939) | 3 (청크 150) | 53 |

**Document 길이 (글자 수)**: 최소 672 (`langchain/errors/OUTPUT_PARSING_FAILURE.mdx`), 기술별 중앙값 10,138~10,865, 최대 385,884 (`mcp/specification/2026-07-28/schema.mdx`).

**청크 길이 (글자 수)**: 최소 58, 중앙값 801, 평균 741, 최대 1,083. 1,000자를 넘는 청크(591개)는 청크 앞에 문서 제목을 붙인 만큼이다(1,200자 초과 0개).


---

## 2. 전처리 실행

### 2-1. 실행 순서

모든 명령은 **프로젝트 루트**에서 `python -m ...` 형태로 실행한다. (`src` 를 패키지로 찾기 위해)

```bash
python collect_docs.py                           # 0. GitHub 공식 문서 .md/.mdx → data/raw/<tech>
python -m src.preprocessing.collect_snippets     # 1. LangChain 문서가 import 하는 코드 예제 수집
python -m src.preprocessing.mdx_to_document      # 2. .mdx 정리 → data/processed/<tech>/documents.jsonl
python -m src.rag.loader                         # 3. (확인용) Document 개수
python -m src.rag.splitter                       # 4. (확인용) 청크 → data/processed/chunks.jsonl
python -m src.vectorstore.build                  # 5. 청크 → BM25 학습 → Pinecone Hybrid 업로드
```

**실행 흐름**

```
collect_docs.py        → data/raw/{langchain,langgraph,mcp}/**/*.mdx
collect_snippets.py    → data/raw/snippets/**
mdx_to_document.py     → data/processed/<tech>/documents.jsonl  (+ <tech>_merged.md 확인용)
loader.py              → Document 리스트
splitter.py            → 청크 (코드 블록 보존)
retriever.build_pinecone → data/processed/bm25_params.json + Pinecone 인덱스
```

- `loader.py` 는 `documents.jsonl` 이 없으면 그 자리에서 `convert_framework()`(2번 전처리)를 먼저 실행한다.

### 2-2. 데이터 디렉토리 구조

```
data/
├── raw/
│   ├── langchain/        # LangChain 공식 문서 .mdx (collect_docs.py)
│   ├── langgraph/        # LangGraph 공식 문서 .mdx
│   ├── mcp/              # MCP 문서·스펙 .mdx
│   └── snippets/         # LangChain 문서가 import 하는 코드 예제 (collect_snippets.py)
└── processed/
    ├── langchain/
    │   ├── documents.jsonl        # 문서별 Document (1줄 = 문서 1개) → loader 가 읽음
    │   └── langchain_merged.md    # 전체 문서를 이어 붙인 확인용 파일
    ├── langgraph/                 # 같은 구조
    ├── mcp/                       # 같은 구조
    ├── chunks.jsonl               # splitter 결과 (확인·평가용)
    └── bm25_params.json           # BM25 학습 결과 (검색에 필요, 팀원과 공유)
```

경로는 모두 `src/const/config.py` 에서 `PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent` 기준으로 만든다. 실행 위치와 무관하게 같은 경로를 쓰기 위해서다.

---

## 3. 데이터 수집

### 3-1. 공식 문서 수집 (`collect_docs.py`)

문서 사이트를 크롤링하지 않고, **GitHub API 로 문서 저장소의 파일 목록을 받아 원본 `.md` / `.mdx` 를 그대로 내려받는다.** HTML → Markdown 변환이 없으므로 코드 블록과 문서 구조가 원본 그대로 남는다.

| 항목 | LangChain | LangGraph | MCP |
|------|------|------|------|
| **저장소** | `langchain-ai/docs` (main) | `langchain-ai/docs` (main) | `modelcontextprotocol/modelcontextprotocol` (main) |
| **수집 경로** | `src/oss/langchain/` | `src/oss/langgraph/` | `docs/docs/2026-07-28/`, `docs/specification/2026-07-28/` |
| **저장 경로** | `data/raw/langchain/...` | `data/raw/langgraph/...` | `data/raw/mcp/docs/2026-07-28/...`, `data/raw/mcp/specification/2026-07-28/...` |
| **원본 파일 (수집 대상)** | 57 | 38 | 53 |
| **Document (변환 완료)** | 55 (`academy.mdx`, `retrieval.mdx` 제외) | 38 | 53 (docs 23 + specification 30) |

- MCP 는 코드에 `latest_version = "2026-07-28"` 로 **최신 버전만** 지정해, 이전 날짜 버전의 문서·스펙이 섞이지 않게 했다. 저장할 때 맨 앞 `docs/` 를 떼어 `data/raw/mcp/{docs,specification}/2026-07-28/` 로 둔다.
- 저장 경로는 저장소 폴더 구조를 그대로 유지한다. (LangChain 은 `errors/`, `mcp/`, `middleware/`, `multi-agent/`, `test/` 하위 폴더 포함)

**수집 흐름**

```
GitHub Tree API  https://api.github.com/repos/{저장소}/git/trees/main?recursive=1
    ↓
type == "blob" (파일) 이고, 수집 경로로 시작하고, .md / .mdx 인 것만
    ↓
should_exclude() 로 제외 대상 거르기
    ↓
https://raw.githubusercontent.com/{저장소}/main/{경로} 에서 원문 다운로드
  (requests.Session 재사용, User-Agent "official-docs-crawler/1.0", timeout 30초)
    ↓
data/raw/<framework>/<상대경로> 에 UTF-8 로 저장
  (실패한 파일은 [실패] 출력 후 다음 파일 계속)
```

**제외 기준** (`collect_docs.py` 와 `mdx_to_document.py` 의 `should_exclude()` 가 같은 규칙으로 두 번 거른다)

| 제외 대상 | 규칙 | 이유 |
|---|---|---|
| `frontend` 폴더 | 경로에 `frontend` 디렉터리 포함 | 프런트엔드(JS) 관련 문서 |
| changelog | 파일명 `changelog-js.mdx`, `changelog-py.mdx` | 변경 이력 나열로 오류 해결과 거리가 멂 |
| 버전 문서 | 파일명에 `version` 포함 | 버전별 중복 문서 |

> 참고: MCP 스펙의 `specification/2026-07-28/changelog.mdx` 는 파일명이 위 규칙에 걸리지 않아 수집·적재되어 있다. 버전 간 변경 사항 질문에 쓰일 수 있어 그대로 두었다.
>
> `collect_docs.py` 는 `PROJECT_ROOT = Path(__file__).resolve().parent.parent` 이므로 프로젝트 루트 바로 아래 폴더(예: `src/` 또는 `scripts/`)에 두고 실행해야 `data/raw` 가 루트에 생긴다. 이 파일은 `src/const/config.py` 를 쓰지 않고 경로를 직접 계산한다.
>
> `part-a/collect/collect_docs.py` 는 문서 사이트를 크롤링해 `data/raw/docs/<site>/*.md` 로 저장하는 별도 실험 버전으로, 최종 파이프라인에서는 쓰지 않았다.

### 3-2. 코드 예제 수집 (`src/preprocessing/collect_snippets.py`)

**문제**: LangChain 문서는 코드 예제를 본문에 쓰지 않고 별도 파일(snippets)에서 불러온다.

```mdx
import AgentsIntroPy from '/snippets/code-samples/agents-intro-py.mdx';
...
<AgentsIntroPy />          ← 화면에서는 여기에 코드가 보이지만, .mdx 원본에는 태그만 있음
```

코드 예제가 빠지면 "오류를 어떻게 고치나요?"라는 질문에 정작 고치는 코드가 검색되지 않는다. 그래서 문서가 실제로 import 하는 예제만 골라 따로 받는다.

| 항목 | 내용 |
|------|------|
| **출처** | `https://raw.githubusercontent.com/langchain-ai/docs/main/src/snippets/<경로>` |
| **대상** | `data/raw/langchain`, `data/raw/langgraph` 의 `.mdx` 가 import 하는 Python 예제 |
| **제외** | `-js.mdx`, `-ts.mdx` (JavaScript/TypeScript 예제) |
| **저장 경로** | `data/raw/snippets/<경로>` |
| **수량** | 148개 (`수집 대상 예제 개수: 148`) |

**수집 흐름**

```
data/raw/{langchain,langgraph}/**/*.mdx 전체 읽기
    ↓
정규식으로 import 경로 추출   ^import\s+\w+\s+from\s+['"]/snippets/([^'"]+)['"]   (re.M)
    ↓
-js.mdx / -ts.mdx 제외, 중복 제거(set) 후 정렬
    ↓
이미 받은 파일은 건너뜀 → 없는 것만 GitHub raw 에서 다운로드 (requests.Session 재사용, timeout 30초)
    ↓
data/raw/snippets/<경로> 저장 (실패한 파일은 [실패] 로 출력하고 계속 진행)
```

---

## 4. 전처리 — `.mdx` → Document (`src/preprocessing/mdx_to_document.py`)

### 4-1. 왜 전처리가 필요한가

`.mdx` 는 Markdown + JSX(React 컴포넌트)다. 그대로 임베딩하면 `<Tabs>`, `import ...`, `{/* */}` 같은 **화면용 코드가 검색 품질을 떨어뜨리고**, JavaScript 예제가 섞여 Python 사용자에게 엉뚱한 답이 나온다. 반대로 정리를 과하게 하면 코드 예제 안의 `import`, `<Tag>` 까지 지워진다. 그래서 **코드 블록은 건드리지 않고 그 바깥 글만 정리**하는 것이 핵심이다.

### 4-2. 파싱 흐름

```
data/raw/<tech> 의 .md / .mdx 파일 목록 (정렬, should_exclude 로 제외)
    ↓
read_file             UTF-8 로 읽기, \r\n → \n
    ↓
split_frontmatter     맨 위 --- title / description --- 분리
    ↓
resolve_snippets      <AgentsIntroPy /> 자리에 data/raw/snippets 의 실제 코드 삽입
    ↓
keep_python_blocks    :::python 블록은 남기고 :::js / :::ts 블록은 통째로 삭제
    ↓
split_code_blocks     코드 블록(```)과 일반 글을 분리 → 일반 글에만 clean_prose 적용
    ↓
clean_prose           JSX 주석·import·HTML 태그·컴포넌트 정리, HTML 엔티티 복원
    ↓
dedent_blocks         컴포넌트 안쪽 들여쓰기 제거 (목록 아래 들여쓰기는 유지)
    ↓
공백 정규화            공백만 있는 줄 → 빈 줄, 빈 줄 3개 이상 → 2개
    ↓
30자 미만 본문은 버림 → 제목·설명을 본문 맨 앞에 붙여 Document 생성
    ↓
data/processed/<tech>/documents.jsonl  +  <tech>_merged.md 저장
```

### 4-3. 노이즈 제거 대상

| 대상 | 처리 | 예시 |
|---|---|---|
| JSX 주석 | 삭제 | `{/* 내부 메모 */}` |
| `import` / `export` 줄 | 삭제 (snippet 은 먼저 코드로 치환) | `import X from '...'` |
| 이미지 태그 | 삭제 | `<img src="a.png" />` |
| 레이아웃 HTML | 줄바꿈으로 | `<div>`, `<span>`, `<br>`, `<p>` |
| 문서 사이트 전용 링크 | 이름만 남김 | ``@[`create_agent`]`` → `` `create_agent` `` |
| 안내 상자 컴포넌트 | 굵은 머리글로 | `<Note>`, `<Warning>`, `<Tip>` … → `**Note:**` |
| Docusaurus 안내 상자 | 굵은 머리글로, 닫는 `:::` 삭제 | `:::warning 주의` → `**Warning:** 주의` |
| `<Card>` | Markdown 링크 목록으로 | `<Card title="Models" href="/oss/..." />` → `- [Models](/oss/...)` |
| 제목이 있는 컴포넌트 | `title` 속성만 굵은 소제목으로 | `<Tab title="pip">` → `**pip**` (Tab, Step, Accordion, Expandable, Update, ParamField, ResponseField) |
| 그 밖의 컴포넌트 | 태그만 삭제, 안쪽 내용은 유지 | `<Tabs>`, `<CodeGroup>`, `<CardGroup>`, `<Steps>` |
| React Fragment, JSX 공백 | 삭제 / 공백으로 | `<>`, `</>`, `{' '}` |
| HTML 엔티티 | 원래 글자로 | `&lt;` → `<`, `&amp;` → `&` |
| JS/TS 언어 블록과 예제 | 통째로 삭제 | `:::js ... :::`, `-js.mdx` snippet |

대문자로 시작하는 태그만 JSX 컴포넌트로 본다(`COMPONENT_RE = <(/?)([A-Z][\w.]*)...>`). 그래서 소문자 HTML 태그와 구분된다.

### 4-4. 변환 예시 (설명서 4-3, 코드로 실행한 결과)

**입력 (.mdx)**

````mdx
---
title: Agents
description: "Build a LangChain agent"
---
import AgentsIntroPy from '/snippets/code-samples/agents-intro-py.mdx';
import AgentsIntroJs from '/snippets/code-samples/agents-intro-js.mdx';

{/* 내부 메모 */}
Use @[`create_agent`] to build an agent.

<Note>
  Agents call tools in a loop.
</Note>

:::python
<AgentsIntroPy />
:::
:::js
<AgentsIntroJs />
:::

<Card title="Models" href="/oss/langchain/models" />
````

**출력 (clean_mdx 결과)**

````markdown
Use `create_agent` to build an agent.

**Note:**

Agents call tools in a loop.

```python
from langchain.agents import create_agent
agent = create_agent("gpt-4o-mini", tools=[])
```

- [Models](/oss/langchain/models)
````

frontmatter 는 `{'title': 'Agents', 'description': 'Build a LangChain agent'}` 로 분리되어 메타데이터와 본문 맨 앞 제목에 쓰인다.

### 4-5. Document 구조

`documents.jsonl` 한 줄 = 문서 1개이며, 형식은 `{"text": 본문, ...메타데이터}` 이다. 아래는 실제 `data/processed/langgraph/documents.jsonl` 의 `GRAPH_RECURSION_LIMIT.mdx` 행이다. (`text` 는 앞부분만, 전체 912자)

```json
{
  "text": "# GRAPH_RECURSION_LIMIT\n\nYour LangGraph `StateGraph` reached the maximum number of steps before hitting a stop condition.\nThis is often due to an infinite loop caused by code like the example below:\n\n```python\nfrom typing import TypedDict\n\nfrom langgraph.graph import StateGraph\n...",
  "technology": "langgraph",
  "document_type": "error",
  "source": "data/raw/langgraph/errors/GRAPH_RECURSION_LIMIT.mdx",
  "file_name": "GRAPH_RECURSION_LIMIT.mdx",
  "title": "GRAPH_RECURSION_LIMIT",
  "description": "",
  "source_url": "https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT",
  "github_url": "https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/errors/GRAPH_RECURSION_LIMIT.mdx",
  "parent_id": "langgraph-errors-graph_recursion_limit",
  "format": "markdown"
}
```

### 4-6. 메타데이터 설계

검색 결과에 **출처를 보여 주고**, **기술별로 필터링**하기 위해 붙인다. 키 이름은 팀 `loader_1.py` 의 키(technology, document_type, source, file_name)를 따르고 필요한 것을 더했다.

| 키 | 만드는 방법 | 예시 | 용도 |
|---|---|---|---|
| `technology` | 원본 폴더 이름 | `langgraph` | 기술별 필터 (`{"technology": "langgraph"}`) |
| `document_type` | 경로에 `errors` / `specification` / `tutorials` / `examples` 가 있으면 각각 `error` / `specification` / `tutorial` / `example`, 없으면 `documentation` | `error` | 에러 문서만 찾기 등 |
| `source` | 프로젝트 루트 기준 상대경로 | `data/raw/langgraph/errors/...mdx` | 원본 위치 (팀원 PC 마다 같음) |
| `file_name` | 파일 이름 | `GRAPH_RECURSION_LIMIT.mdx` | 표시용 |
| `title` | frontmatter `title` → 본문 첫 `# 제목` → 파일 이름 순 | `GRAPH_RECURSION_LIMIT` | 답변의 출처 제목 |
| `description` | frontmatter `description` (없으면 `""`) | | 본문 맨 앞에 함께 붙여 검색에 활용 |
| `source_url` | 문서 사이트 주소 + 확장자 뗀 경로, `index` 는 폴더 주소로 | `https://docs.langchain.com/oss/python/langgraph/errors/...` | **답변에 다는 출처 링크** (C 파트 출처 점검) |
| `github_url` | GitHub 원본 주소 + 상대경로 | `https://github.com/langchain-ai/docs/blob/main/...` | 원문 확인 |
| `parent_id` | `<tech>/<경로>` 에서 확장자 제거, 영숫자·`_` 외 문자는 `-`, 소문자 | `langgraph-errors-graph_recursion_limit` | 문서 고유 ID |
| `format` | 고정값 | `markdown` | splitter 가 Markdown 전용 분할을 쓸지 판단 |
| `chunk_index`, `chunk_id` | splitter 에서 추가 | `2`, `langgraph-errors-graph_recursion_limit-002` | 청크 순서, **Pinecone 벡터 ID** |

### 4-7. 결과 저장

- `save_documents()`: `data/processed/<tech>/documents.jsonl` — loader 가 읽는 파일
- `save_merged()`: `data/processed/<tech>/<tech>_merged.md` — 문서 사이에 `---` 와 `> 출처: 경로 | URL` 을 넣어 하나로 이어 붙인 **사람이 읽는 확인용** 파일. 검색 입력으로는 쓰지 않는다.

---

## 5. 청크 분할 (`src/rag/loader.py`, `src/rag/splitter.py`)

### 5-1. 문서 읽기 (`loader.py`)

| 함수 | 동작 |
|---|---|
| `load_documents(technologies=None)` | 세 기술의 `data/processed/<tech>` 를 돌며 `load_mdx_documents` 호출. 일부 기술만 지정 가능 |
| `load_mdx_documents(root_dir, technology)` | `documents.jsonl` 을 한 줄씩 읽어 `text` → `page_content`, 나머지 → `metadata`. 파일이 없으면 전처리를 자동 실행 |
| `_detect_document_type(path)` | jsonl 에 `document_type` 이 없을 때만 경로로 판단 (전처리와 같은 규칙) |

### 5-2. 청킹 전략 — Markdown 구조 기반 청킹

공식 문서는 `## 소제목` 단위로 주제가 나뉘고, 오류 해결 답변에는 **코드 예제가 온전히** 들어 있어야 한다. 고정 길이로 자르면 코드 블록 중간이 잘려 ```` ``` ```` 짝이 깨지고 코드가 일반 글처럼 임베딩된다. 그래서 제목·코드 블록 경계를 지키며 자른다.

| 설정 | 값 | 위치 |
|---|---|---|
| `CHUNK_SIZE` | 1000자 (영어 1,000자 ≈ 250 토큰) | `config.py` (`.env` 로 변경 가능) |
| `CHUNK_OVERLAP` | 150자 (긴 일반 문단을 자를 때만 적용) | `config.py` |
| `MIN_CHUNK_CHARS` | 50자 미만 청크 버림 | `splitter.py` |

**분할 흐름 (`split_documents`)**

```
Document (format="markdown")
    ↓
_markdown_blocks      줄 단위로 heading(#) / code(``` ~ ```) / text(빈 줄로 구분된 문단) 블록화
                      코드 블록은 한 덩어리로 묶음
    ↓
split_markdown        블록을 순서대로 청크에 담음
  - 담으면 1000자를 넘으면 새 청크 시작
  - 새 소제목이 나오고 현재 청크가 300자(30%)를 넘었으면 새 청크 시작 → 주제 경계에서 자름
  - 청크가 소제목 중간에서 시작하면 그 소제목을 맨 앞에 다시 붙임 → 문맥 유지
  - 1000자보다 긴 코드 블록: _split_long_code 가 줄 단위로 나누고 조각마다 ``` 를 다시 열고 닫음
  - 1000자보다 긴 일반 문단: RecursiveCharacterTextSplitter (\n\n → \n → ". " → "。" → " " 순, overlap 150)
    ↓
후처리
  - 50자 미만 청크 버림
  - 같은 기술 안에서 내용이 같은 청크는 sha256 해시로 한 번만 남김
  - 문서 제목을 청크 맨 앞에 붙임 (이미 "# 제목" 으로 시작하면 생략)
  - chunk_index, chunk_id = "<parent_id>-000" 부여
```

`format` 이 `markdown` 이 아닌 문서는 `RecursiveCharacterTextSplitter` 만으로 자른다. (현재 전처리 결과는 모두 `markdown`)

**효과 (전체 데이터 146개 문서로 실측)**

| 방식 | 청크 수 | 코드 블록이 중간에서 잘린 청크 (```` ``` ```` 개수가 홀수) |
|---|---:|---:|
| `RecursiveCharacterTextSplitter` 만 (1000 / 150) | 3,559 | **958개 (26.9%)** |
| 현재 방식 (`split_documents`) | 3,918 | **0개** |

- 홀수 개수만 센 값이라, 코드 한가운데서 시작해 펜스가 아예 없는 조각까지 치면 기존 방식의 깨진 청크는 더 많다.
- 현재 방식의 청크 3,918개 중 1,926개(49.2%)가 코드 블록을 포함한다. 오류 해결 질문에 코드 예제가 함께 검색될 수 있다는 뜻이다.
- 청크 수가 늘어난 이유는 소제목 경계에서 먼저 끊기 때문이다.

---

## 6. 임베딩 및 적재 전략

### 6-1. 임베딩 모델

| 항목 | 내용 |
|------|------|
| **Dense 임베딩** | OpenAI `text-embedding-3-small` (1536차원) — `OPEN_EMBEDDING`, `EMBEDDING_DIM` |
| **Sparse 임베딩** | BM25 (`pinecone_text.sparse.BM25Encoder`, 우리 청크로 학습) |
| **설정 위치** | `src/const/config.py`, `.env` |
| **적용 DB** | Pinecone 서버리스 인덱스 (aws `us-east-1`, `metric="dotproduct"`, 기본 이름 `skn35-rag`) |

### 6-2. 임베딩 입력 텍스트

| 대상 | page_content 구성 | 근거 |
|------|------------------|------|
| 청크 | `{문서 제목}\n{청크 본문}` (본문 안의 코드 블록 포함) | 짧은 청크도 어떤 문서인지 알 수 있게 제목을 함께 임베딩 |
| 문서 본문 | `# {title}\n\n{description}\n\n{정리된 Markdown}` | frontmatter 의 제목·설명을 본문 앞에 붙여 검색에 반영 |

### 6-3. 적재 (`build_pinecone`)

```
load_documents → split_documents
    ↓
청크가 없으면 중단 (공용 인덱스를 비우지 않도록)
    ↓
create_pinecone_index   없으면 생성, 있으면 metric·차원 검사 (다르면 오류 안내)
    ↓
전체 구축이면 기존 벡터 전부 삭제 (없어진 문서의 청크가 남지 않게)
    ↓
BM25 학습 → data/processed/bm25_params.json 저장
  (일부 기술만 올릴 때는 기존 bm25_params.json 유지)
    ↓
PineconeHybridSearchRetriever.add_texts
  id = chunk_id, 메타데이터 = _clean_metadata(청크 metadata)
  → 한 레코드에 Dense + Sparse 벡터를 함께 저장
```

**BM25 학습 결과 (`data/processed/bm25_params.json`)**

| 항목 | 값 | 의미 |
|---|---|---|
| `n_docs` | 3,918 | 학습에 쓴 청크 수 (= 업로드한 청크 수) |
| `avgdl` | 79.08 | 청크 평균 길이 (토큰화 후 단어 수) |
| `k1`, `b` | 1.2, 0.75 | BM25 기본 보정값 |
| `lower_case`, `remove_punctuation`, `remove_stopwords`, `stem` | 모두 `true` | 소문자화, 구두점·불용어 제거, 어간 추출 |
| `language` | `english` | 영어 기준 토큰화 |

- 검색 기본값: Hybrid 가중치 `alpha = 0.7` (점수 = 0.7 × Dense + 0.3 × Sparse), `top_k = 5`, 재정렬·다중 검색어 후보 `FETCH_K = 20`
- Pinecone 메타데이터는 문자열·숫자·불리언·리스트만 허용하므로 `_clean_metadata()` 가 `None` → `""`, 그 밖의 타입 → 문자열로 바꾼다.

---

## 7. 전처리 품질 관리

### 7-1. 중복성(Duplication) 관리

데이터셋 전체에 대한 별도 중복 검사는 없고, 각 단계에서 다음 기준으로 처리한다.

| 단계 | 중복 제거 기준 | 코드 위치 |
|---|---|---|
| 코드 예제 수집 | import 경로를 `set` 으로 모음, 이미 받은 파일은 건너뜀 | `preprocessing/collect_snippets.py` |
| 청크 생성 | 같은 기술 안에서 `sha256(technology + 청크 내용)` 이 같으면 한 번만 | `rag/splitter.py` |
| Pinecone 적재 | 벡터 ID = `chunk_id` → 다시 올려도 덮어씀(중복 레코드 없음). 전체 구축은 기존 벡터 삭제 후 업로드 | `rag/retriever.py` |
| 다중 검색어 결과 | RRF 통합 시 `chunk_id` 기준으로 같은 청크를 하나로 | `rag/rrf.py` |
| 생성된 검색어 | 소문자 기준 중복 검색어 제거 | `rag/multi_query.py`, `rag/query_rewrite.py` |

### 7-2. 결측치(Missing Value) 처리

| 처리 대상 | 방식 | 코드 위치 |
|---|---|---|
| 본문이 거의 없는 문서 (목차·링크 전용 페이지 등) | 정리 후 30자 미만이면 Document 를 만들지 않음. 실제로 LangChain `academy.mdx`, `retrieval.mdx` 2개가 빠짐 | `mdx_to_document.py` (`MIN_CONTENT_CHARS`) |
| 제목 없음 | frontmatter `title` → 본문 첫 H1 → 파일 이름 순으로 대체 | `mdx_to_document.py` (`make_document`) |
| 설명 없음 | `description = ""` | `mdx_to_document.py` |
| snippet 파일 없음 | 해당 컴포넌트 태그만 지우고 진행 (collect_snippets 선행 권장) | `mdx_to_document.py` (`resolve_snippets`) |
| jsonl 에 메타데이터 키 없음 | `technology`, `document_type`, `file_name` 을 `setdefault` 로 채움 | `rag/loader.py` |
| 메타데이터 `None` | `""` 로 변환 (Pinecone 제약) | `rag/retriever.py` (`_clean_metadata`) |
| 너무 짧은 청크 | 50자 미만 버림 | `rag/splitter.py` |
| 읽기 실패 문자 | `errors="replace"` 로 읽고 계속 진행, 변환 실패 파일은 `[실패]` 출력 후 건너뜀 | `mdx_to_document.py` |

### 7-3. 편향성(Bias) 고려 사항

별도의 편향성 분석 도구는 쓰지 않는다. 데이터 특성상 다음 불균형이 있으므로 검색·답변 시 고려한다.

- **기술별 청크 수 불균형**: 문서 수는 LangChain 55 / LangGraph 38 / MCP 53 으로 비슷하지만, 청크는 MCP 1,618(41.3%) / LangChain 1,307(33.4%) / LangGraph 993(25.3%)로 MCP 가 가장 많다. 필터 없이 검색하면 MCP 문서가 과대 대표될 수 있다. → `technology` 메타데이터 필터로 질문 기술만 검색할 수 있게 설계했다.
- **문서 하나에 청크 집중**: MCP 스펙의 `schema.mdx` 하나가 385,884자, **청크 473개(전체의 12.1%)** 다. 다음으로 많은 문서(`build-server.mdx` 119개, `use-graph-api.mdx` 110개)의 4배에 가깝다. 스키마 정의(타입 나열) 위주라 일반 질문에도 자주 걸릴 수 있으므로 rerank 와 `document_type` 필터로 보완한다.
- **언어 불균형 (한국어 질문 ↔ 영어 문서)**: 문서는 영어, 질문은 주로 한국어다. BM25 는 영어 단어 기준이라 한국어 질문은 Sparse 점수가 거의 0이 된다. → `query_rewrite` 로 영어 검색어를 만들어 함께 검색하고, 다국어 Cross-Encoder(`BAAI/bge-reranker-v2-m3`)로 재정렬한다.
- **언어(프로그래밍) 범위**: Python 문서만 남기고 JS/TS 를 제거했으므로 JavaScript 사용자의 질문에는 답하기 어렵다. (의도된 범위 제한)
- **문서 유형 불균형**: 오류 해결 서비스인데 `error` 유형은 13개 문서, **청크 28개(0.7%)** 뿐이다(LangChain 7, LangGraph 6, MCP 0). 대부분의 오류 질문은 `documentation` / `specification` 청크에서 답을 찾게 되므로, `error` 필터만으로 검색하지 않도록 한다.
- **설명(description) 결측**: 146개 중 92개(63.0%)가 frontmatter `description` 이 비어 있다. 제목은 146개 모두 채워져 있다.
- **완화 장치**: Dense + Sparse Hybrid 검색, 다중 검색어 + RRF, Cross-Encoder 재정렬로 문서 수에만 의존하지 않도록 했다.

---

## 8. 적용 기술 검토

### 8-1. 형태소 분석

본 프로젝트는 KoNLPy 등 한국어 형태소 분석기를 사용하지 않는다.

1. **문서가 영어**: 검색 대상이 영어 공식 문서라 한국어 형태소 분석이 적용될 텍스트가 없다.
2. **BM25 자체 토큰화**: `BM25Encoder` 가 영어 기준으로 소문자화 → 구두점 제거 → 불용어 제거 → 어간 추출(Snowball, 예: errors → error) → 단어 해시(murmurhash) 를 수행한다. (처음 실행할 때 nltk 데이터 `punkt_tab`, `stopwords` 를 자동으로 받는다)
3. **한국어 질문 처리**: 한국어 질문은 형태소 분석 대신 LLM(`query_rewrite`)이 영어 검색어와 에러 키워드로 바꾸고, Dense 임베딩과 다국어 재정렬 모델이 의미를 맞춘다.

### 8-2. Graph DB

A 파트의 수집·전처리·적재는 Neo4j 등 그래프 데이터베이스를 사용하지 않는다. 프로젝트에서 "graph" 는 **LangGraph**(B 파트의 RAG 파이프라인 오케스트레이션)와 검색 대상 문서인 LangGraph 를 뜻한다. 청킹 전략은 Vector DB(Pinecone) 입력만 고려해 설계했으며, Knowledge Graph 구축은 향후 과제로 남긴다.

### 8-3. MDX → PDF 변환을 하지 않은 이유

초기에는 `.mdx` 를 기술별로 합쳐 PDF 로 만든 뒤(`merge_mdx.py` → `md_to_pdf.py` → `data/pdf/<tech>.pdf`) 읽는 방식을 검토했으나, 최종 파이프라인에서는 `.mdx` 를 Markdown 으로 정리해 바로 쓴다.

| 항목 | PDF 경로 | 현재 경로 (MDX → Markdown → jsonl) |
|---|---|---|
| 코드 블록 | PDF 에서 다시 텍스트를 뽑을 때 들여쓰기·줄바꿈이 깨질 수 있음 | ```` ``` ```` 블록을 그대로 보존, 청크에서도 자르지 않음 |
| 문서 경계·메타데이터 | 기술별 PDF 1개로 합쳐져 문서별 `source_url`, `title` 을 다시 찾아야 함 | 문서 1개 = Document 1개, 메타데이터가 처음부터 붙어 있음 |
| 구조 정보 | 페이지 단위로 바뀌어 `#` 제목 구조가 사라짐 | 제목 경계 기반 청킹 가능 |
| 의존성 | `markdown`, `playwright` + Chromium 설치 필요 | 표준 라이브러리 + LangChain 만 사용 |
| 사람이 확인 | PDF 열람 | `<tech>_merged.md` 로 같은 목적 달성 |
