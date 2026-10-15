# 체크리스트 검수 표본 (정답 있는 질문의 10%)

확인할 것: 항목이 질문의 요구와 근거 문서에 맞는가? 문서에 없는 내용을 요구하지 않는가? 너무 좁거나 넓지 않은가?

## R14

**질문**: 결과 응답에 반드시 포함되어야 하는 필드는 무엇인가요?

**근거 문서** (mcp-specification-2026-07-28-basic-index-004): Overview ##### ResultType The `resultType` field in a result indicates the type of the result being returned. MCP supports polymorphic result types, allowing servers to return different structures based on the outcome of the request. The `resultType` field is a string that clients can use to determine how to parse and handle the `result` object.

**근거 문서** (mcp-specification-2026-07-28-basic-index-005): Overview ##### ResultType - A `resultType` of `"complete"` indicates the request completed successfully and the result contains the final content. - A `resultType` of `"input_required"` indicates the request is incomplete and more information is needed to process the request. The result contains an [`InputRequiredResult`](/specification/2026-07-28/basic/patterns/mrtr#inputrequiredresult) object with additional information needed. - Extensions **MAY** add additional `ResultType` values. The set of supported `ResultType` values **MUST** be created from the set defined in the core protocol and include any additional values of supported extensions that are advertised via capabilities. - A `resul …

**꼭 들어가야 할 항목**
- [ ] 결과 응답에는 반드시 result 필드가 포함되어야 함을 설명한다.
- [ ] result 필드에는 resultType 필드가 포함되어야 함을 설명한다.
- [ ] resultType 필드는 결과의 유형을 나타내는 문자열임을 안내한다.

**있으면 안 되는 것**
- [ ] 결과 응답에 result 필드가 포함되지 않아도 된다고 주장한다.
- [ ] resultType 필드가 필요 없다고 언급한다.
- [ ] 클라이언트가 인식하지 못하는 resultType 값도 유효하다고 설명한다.

수정할 내용: 

## R13

**질문**: 클라이언트가 메타데이터 문서를 사용할 때, 서버가 클라이언트 ID와 리디렉션 URI를 어떻게 검증하는지 구체적으로 설명해 줄 수 있나요?

**근거 문서** (mcp-specification-2026-07-28-basic-authorization-client-registration-005): Client Registration ### Implementation Requirements - **SHOULD** fetch metadata documents when encountering URL-formatted client_ids - **MUST** validate that the fetched document's `client_id` matches the URL exactly - **SHOULD** cache metadata respecting HTTP cache headers - **MUST** validate redirect URIs presented in an authorization request against those in the metadata document - **MUST** validate the document structure is valid JSON and contains required fields - **SHOULD** follow the security considerations in [Section 6 of Client ID Metadata Document](https://www.ietf.org/archive/id/draft-ietf-oauth-client-id-metadata-document-00.html#section-6) and in [Client ID Metadata Document Se …

**근거 문서** (mcp-specification-2026-07-28-basic-authorization-client-registration-007): Client Registration ### Client ID Metadata Documents Flow The following diagram illustrates the complete flow when using Client ID Metadata Documents: ```mermaid sequenceDiagram participant User participant Client as MCP Client participant Server as Authorization Server participant Metadata as Metadata Endpoint<br/>(Client's HTTPS URL) participant Resource as MCP Server Note over Client,Metadata: Client hosts metadata at<br/>https://app.example.com/oauth/metadata.json User->>Client: Initiates connection to MCP Server Client->>Server: Authorization Request<br/>client_id=https://app.example.com/oauth/metadata.json<br/>redirect_uri=http://localhost:3000/callback Server->>User: Authentication pr …

**꼭 들어가야 할 항목**
- [ ] 클라이언트 ID가 URL 형식일 때 서버가 메타데이터 문서를 가져오는 과정을 설명한다.
- [ ] 가져온 문서의 client_id가 해당 URL과 정확히 일치하는지 검증해야 한다(MUST)고 설명한다.
- [ ] 서버가 인가 요청의 리디렉션 URI를 메타데이터 문서에 있는 목록과 비교하여 검증하는 절차를 설명한다.
- [ ] 메타데이터 문서가 유효한 JSON 구조이고 필수 필드를 포함하는지 확인한다고 안내한다.

**있으면 안 되는 것**
- [ ] client_id 일치 검증을 선택 사항이라고 설명한다.
- [ ] 리디렉션 URI 검증이 필요 없다고 잘못 설명한다.
- [ ] 메타데이터 문서의 구조가 유효하지 않아도 된다고 언급한다.

수정할 내용: 

## R29

**질문**: 여러 팀이 각자의 구성 요소를 독립적으로 유지 관리할 수 있는지 여부는 어떻게 확인할 수 있나요?

**근거 문서** (langchain-multi-agent-index-005): Multi-agent ### Choosing a pattern - **Distributed development**: Can different teams maintain components independently? - **Parallelization**: Can multiple agents execute concurrently? - **Multi-hop**: Does the pattern support calling multiple subagents in series? - **Direct user interaction**: Can subagents converse directly with the user? **Tip:** You can mix patterns! For example, a **subagents** architecture can invoke tools that invoke custom workflows or router agents. Subagents can even use the **skills** pattern to load context on-demand. The possibilities are endless!

**꼭 들어가야 할 항목**
- [ ] 패턴 비교 기준 중 '분산 개발(Distributed development)' 항목이 이 질문에 해당함을 설명한다.
- [ ] 분산 개발의 정의(서로 다른 팀이 구성 요소를 독립적으로 유지 관리할 수 있는가)를 설명한다.
- [ ] 패턴별 평가(비교표)를 보고 판단할 수 있음을 안내한다.

**있으면 안 되는 것**
- [ ] 분산 개발 기준을 사용자 직접 대화나 병렬화 기준과 혼동한다.
- [ ] 각 팀의 독립적인 유지 관리가 불가능하다고 단정짓는다.
- [ ] 서브 에이전트의 역할을 잘못 설명한다.

수정할 내용: 

## R31

**질문**: 도구 호출 중에 서버가 클라이언트에게 입력을 요청할 수 있는 방법은 무엇인가?

**근거 문서** (langchain-mcp-tools-016): Tools ## Server requests during tool execution Most tools finish without asking the client for anything mid-call. When a server needs input, `MCPAdapter` surfaces [elicitation](https://modelcontextprotocol.io/specification/draft/client/elicitation) as a LangGraph `interrupt`. ### Elicitation [Elicitation](https://modelcontextprotocol.io/specification/draft/client/elicitation) lets an MCP server request input during a tool call. The adapter pauses the run with a LangGraph interrupt. Your application presents the request to the user and resumes the run with their answer. Attach a [checkpointer](/oss/langchain/short-term-memory) to the agent and use the same `thread_id` when invoking and resumi …

**꼭 들어가야 할 항목**
- [ ] 도구 호출 중 서버가 클라이언트에게 입력을 요청하는 방법이 Elicitation임을 설명한다.
- [ ] 어댑터가 LangGraph interrupt로 실행을 일시 중지하고, 애플리케이션이 사용자에게 요청을 보여 준 뒤 답으로 실행을 재개함을 설명한다.
- [ ] interrupt로 일시 중지한 뒤 재개하려면 체크포인터를 붙이고 같은 thread_id를 써야 함을 설명한다.
- [ ] InputRequiredResult(다중 왕복 요청)로 추가 입력을 요청할 수 있음을 설명한다.

**있으면 안 되는 것**
- [ ] 도구 호출 중에 클라이언트의 입력을 항상 요구한다고 잘못 설명한다.
- [ ] 사람 승인 미들웨어(HITL, approve 결정)를 서버의 입력 요청 방식으로 설명한다.

수정할 내용: 
