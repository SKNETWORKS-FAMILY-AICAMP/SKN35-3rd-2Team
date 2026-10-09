# Agents
> 출처: data/raw/langchain/agents.mdx | https://docs.langchain.com/oss/python/langchain/agents

Build a LangChain agent: a model calling tools in a loop until a task is complete, shaped by a harness of prompt, tools, and middleware.

An agent is a model calling tools in a loop until a given task is complete.

A harness is everything around that loop: the prompt, the tools, and any middleware that shapes the model's behavior.

**Note:**

**Agent = Model + Harness**

The job of a harness: get the model the right context at the right time for the given task.

`create_agent` is a highly configurable harness. At its simplest, you can create one with:

```python Google
from langchain.agents import create_agent

agent = create_agent(model="google_genai:gemini-3.6-flash", tools=tools)
```

```python OpenAI
from langchain.agents import create_agent

agent = create_agent(model="openai:gpt-5.5", tools=tools)
```

```python Anthropic
from langchain.agents import create_agent

agent = create_agent(model="anthropic:claude-sonnet-5", tools=tools)
```

```python OpenRouter
from langchain.agents import create_agent

agent = create_agent(model="openrouter:z-ai/glm-5.2", tools=tools)
```

```python Fireworks
from langchain.agents import create_agent

agent = create_agent(model="fireworks:accounts/fireworks/models/glm-5p2", tools=tools)
```

```python Baseten
from langchain.agents import create_agent

agent = create_agent(model="baseten:zai-org/GLM-5.2", tools=tools)
```

```python Ollama
from langchain.agents import create_agent

agent = create_agent(model="ollama:north-mini-code-1.0", tools=tools)
```

Building on that, you can configure the basics directly with the `model=`, `tools=`, and `system_prompt=` parameters. For more advanced capabilities, extend the harness with [middleware](#configure-the-harness).

**Tip:**

[Deep Agents](/oss/deepagents/overview) builds on `create_agent` and comes with commonly useful capabilities already assembled, such as planning, file system tools, subagents, and memory. Use `create_agent` when you need to configure the harness yourself.

## Core components

### Model

Pass a model identifier string (`"provider:model"`) or an initialized model instance to select the model for your agent. See [Models](/oss/langchain/models) for parameters, provider setup, and dynamic model selection.

```python Google
from langchain.agents import create_agent

agent = create_agent(model="google_genai:gemini-3.6-flash", tools=tools)
```

```python OpenAI
from langchain.agents import create_agent

agent = create_agent(model="openai:gpt-5.5", tools=tools)
```

```python Anthropic
from langchain.agents import create_agent

agent = create_agent(model="anthropic:claude-sonnet-5", tools=tools)
```

```python OpenRouter
from langchain.agents import create_agent

agent = create_agent(model="openrouter:z-ai/glm-5.2", tools=tools)
```

```python Fireworks
from langchain.agents import create_agent

agent = create_agent(model="fireworks:accounts/fireworks/models/glm-5p2", tools=tools)
```

```python Baseten
from langchain.agents import create_agent

agent = create_agent(model="baseten:zai-org/GLM-5.2", tools=tools)
```

```python Ollama
from langchain.agents import create_agent

agent = create_agent(model="ollama:north-mini-code-1.0", tools=tools)
```

### Tools

To provide the agent with tools, pass any Python callable, LangChain tool, or tool dict. See [Tools](/oss/langchain/tools) for tool definition, context access, and dynamic tool selection.

```python Google
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(model="google_genai:gemini-3.6-flash", tools=[search])
```

```python OpenAI
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(model="openai:gpt-5.5", tools=[search])
```

```python Anthropic
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(model="anthropic:claude-sonnet-5", tools=[search])
```

```python OpenRouter
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(model="openrouter:z-ai/glm-5.2", tools=[search])
```

```python Fireworks
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(model="fireworks:accounts/fireworks/models/glm-5p2", tools=[search])
```

```python Baseten
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(model="baseten:zai-org/GLM-5.2", tools=[search])
```

```python Ollama
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(model="ollama:north-mini-code-1.0", tools=[search])
```

### System prompt

Shape how the agent approaches tasks. The system prompt parameter accepts a string or `SystemMessage`. For dynamic prompts at runtime, use [middleware](/oss/langchain/middleware).

```python Google
agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=tools,
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)
```

```python OpenAI
agent = create_agent(
    model="openai:gpt-5.5",
    tools=tools,
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)
```

```python Anthropic
agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=tools,
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)
```

```python OpenRouter
agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=tools,
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)
```

```python Fireworks
agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=tools,
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)
```

```python Baseten
agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=tools,
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)
```

```python Ollama
agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=tools,
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)
```

### Structured output

Return a validated schema from the agent using `response_format=`. See [Structured output](/oss/langchain/structured-output) for strategies and examples.

```python Google
from pydantic import BaseModel
from langchain.agents import create_agent

class Answer(BaseModel):
    summary: str
    confidence: float

agent = create_agent(model="google_genai:gemini-3.6-flash", tools=tools, response_format=Answer)
result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends"}]})
result["structured_response"]  # Answer(summary=..., confidence=...)
```

```python OpenAI
from pydantic import BaseModel
from langchain.agents import create_agent

class Answer(BaseModel):
    summary: str
    confidence: float

agent = create_agent(model="openai:gpt-5.5", tools=tools, response_format=Answer)
result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends"}]})
result["structured_response"]  # Answer(summary=..., confidence=...)
```

```python Anthropic
from pydantic import BaseModel
from langchain.agents import create_agent

class Answer(BaseModel):
    summary: str
    confidence: float

agent = create_agent(model="anthropic:claude-sonnet-5", tools=tools, response_format=Answer)
result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends"}]})
result["structured_response"]  # Answer(summary=..., confidence=...)
```

```python OpenRouter
from pydantic import BaseModel
from langchain.agents import create_agent

class Answer(BaseModel):
    summary: str
    confidence: float

agent = create_agent(model="openrouter:z-ai/glm-5.2", tools=tools, response_format=Answer)
result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends"}]})
result["structured_response"]  # Answer(summary=..., confidence=...)
```

```python Fireworks
from pydantic import BaseModel
from langchain.agents import create_agent

class Answer(BaseModel):
    summary: str
    confidence: float

agent = create_agent(model="fireworks:accounts/fireworks/models/glm-5p2", tools=tools, response_format=Answer)
result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends"}]})
result["structured_response"]  # Answer(summary=..., confidence=...)
```

```python Baseten
from pydantic import BaseModel
from langchain.agents import create_agent

class Answer(BaseModel):
    summary: str
    confidence: float

agent = create_agent(model="baseten:zai-org/GLM-5.2", tools=tools, response_format=Answer)
result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends"}]})
result["structured_response"]  # Answer(summary=..., confidence=...)
```

```python Ollama
from pydantic import BaseModel
from langchain.agents import create_agent

class Answer(BaseModel):
    summary: str
    confidence: float

agent = create_agent(model="ollama:north-mini-code-1.0", tools=tools, response_format=Answer)
result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends"}]})
result["structured_response"]  # Answer(summary=..., confidence=...)
```

### Agent state

Every agent manages its execution context through `AgentState`, a typed dictionary that holds the current conversation history and any custom fields your tools and middleware need.

The built-in field is:

| Field | Type | Description |
|-------|------|-------------|
| `messages` | `list[BaseMessage]` | The full conversation history for the current thread. Append-only: new messages are added, never replaced. |

`AgentState` is also the type signature for every node-style middleware hook (`before_model`, `after_model`, and similar). Hooks receive the current state and can return a dict of updates to merge back into it.

To add custom fields (for example, a `user_id` or a counter), subclass `AgentState` and pass the subclass to `create_agent` via `state_schema=`:

```python Google
from langchain.agents import AgentState, create_agent

class MyState(AgentState):
    user_id: str
    call_count: int

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[],
    state_schema=MyState,  # [!code highlight]
)
```

```python OpenAI
from langchain.agents import AgentState, create_agent

class MyState(AgentState):
    user_id: str
    call_count: int

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[],
    state_schema=MyState,  # [!code highlight]
)
```

```python Anthropic
from langchain.agents import AgentState, create_agent

class MyState(AgentState):
    user_id: str
    call_count: int

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[],
    state_schema=MyState,  # [!code highlight]
)
```

```python OpenRouter
from langchain.agents import AgentState, create_agent

class MyState(AgentState):
    user_id: str
    call_count: int

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[],
    state_schema=MyState,  # [!code highlight]
)
```

```python Fireworks
from langchain.agents import AgentState, create_agent

class MyState(AgentState):
    user_id: str
    call_count: int

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[],
    state_schema=MyState,  # [!code highlight]
)
```

```python Baseten
from langchain.agents import AgentState, create_agent

class MyState(AgentState):
    user_id: str
    call_count: int

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[],
    state_schema=MyState,  # [!code highlight]
)
```

```python Ollama
from langchain.agents import AgentState, create_agent

class MyState(AgentState):
    user_id: str
    call_count: int

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[],
    state_schema=MyState,  # [!code highlight]
)
```

For full details, examples, and middleware-level state schemas, see [Short-term memory](/oss/langchain/short-term-memory#customizing-agent-memory) and [Custom middleware](/oss/langchain/middleware/custom#state-updates).

## Invocation

**Tip:**

Trace each step of this loop, debug tool calls, and evaluate agent outputs with [LangSmith](https://smith.langchain.com). Follow the [tracing quickstart](/langsmith/trace-with-langchain) to get set up. We recommend you also set up [LangSmith Engine](/langsmith/engine) which monitors your traces, detects issues, and proposes fixes.

You can invoke an agent with a message. Behind the scenes that passes an update to the agent's [`State`](/oss/langgraph/graph-api#state). All agents include a [sequence of messages](/oss/langgraph/use-graph-api#messagesstate) in their state; to invoke the agent, pass a new message along with a `thread_id` so the agent can persist and resume conversation history:

```python Google
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": str(uuid7())}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config=config,
)

# A follow-up turn on the same conversation: reuse the same thread_id to keep history
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What about tomorrow?"}]},
    config=config,
)
```

```python OpenAI
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": str(uuid7())}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config=config,
)

# A follow-up turn on the same conversation: reuse the same thread_id to keep history
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What about tomorrow?"}]},
    config=config,
)
```

```python Anthropic
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": str(uuid7())}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config=config,
)

# A follow-up turn on the same conversation: reuse the same thread_id to keep history
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What about tomorrow?"}]},
    config=config,
)
```

```python OpenRouter
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": str(uuid7())}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config=config,
)

# A follow-up turn on the same conversation: reuse the same thread_id to keep history
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What about tomorrow?"}]},
    config=config,
)
```

```python Fireworks
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": str(uuid7())}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config=config,
)

# A follow-up turn on the same conversation: reuse the same thread_id to keep history
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What about tomorrow?"}]},
    config=config,
)
```

```python Baseten
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": str(uuid7())}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config=config,
)

# A follow-up turn on the same conversation: reuse the same thread_id to keep history
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What about tomorrow?"}]},
    config=config,
)
```

```python Ollama
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": str(uuid7())}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config=config,
)

# A follow-up turn on the same conversation: reuse the same thread_id to keep history
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What about tomorrow?"}]},
    config=config,
)
```

- [View example trace](https://smith.langchain.com/public/5ddee370-d49e-4c80-ae12-691aa17c1aa8/r)

  Open a public LangSmith run for this example.

**Note:**

Persisting conversation history with `thread_id` requires the agent to be configured with a [checkpointer](/oss/langchain/long-term-memory). When deployed on [LangSmith](/langsmith/deployment), a checkpointer is provisioned automatically. Locally, pass one explicitly, for example `create_agent(..., checkpointer=InMemorySaver())`.

If you also need to pass per-run configuration (such as a user ID, API keys, or feature flags) to tools and middleware, pass it as `context` alongside `config`. Define the shape of that data with `context_schema` and access it through `runtime.context`:

```python Google
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

@dataclass
class Context:
    user_id: str

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[],
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config={"configurable": {"thread_id": str(uuid7())}},
    context=Context(user_id="user-123"),
)
```

```python OpenAI
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

@dataclass
class Context:
    user_id: str

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[],
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config={"configurable": {"thread_id": str(uuid7())}},
    context=Context(user_id="user-123"),
)
```

```python Anthropic
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

@dataclass
class Context:
    user_id: str

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[],
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config={"configurable": {"thread_id": str(uuid7())}},
    context=Context(user_id="user-123"),
)
```

```python OpenRouter
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

@dataclass
class Context:
    user_id: str

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[],
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config={"configurable": {"thread_id": str(uuid7())}},
    context=Context(user_id="user-123"),
)
```

```python Fireworks
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

@dataclass
class Context:
    user_id: str

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[],
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config={"configurable": {"thread_id": str(uuid7())}},
    context=Context(user_id="user-123"),
)
```

```python Baseten
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

@dataclass
class Context:
    user_id: str

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[],
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config={"configurable": {"thread_id": str(uuid7())}},
    context=Context(user_id="user-123"),
)
```

```python Ollama
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

@dataclass
class Context:
    user_id: str

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[],
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config={"configurable": {"thread_id": str(uuid7())}},
    context=Context(user_id="user-123"),
)
```

- [View example trace](https://smith.langchain.com/public/5a94648f-0a0b-46f3-a80c-bd1670e35930/r)

  Open a public LangSmith run for this example.

`thread_id` scopes the *conversation* (message history, checkpoints), while `context` carries *per-run* data your tools and middleware read at invocation time. Both are commonly passed together. See [tool context](/oss/langchain/tools#context) and [Runtime](/oss/langchain/runtime) for more.

## Streaming

`invoke` returns the final response at the end of a run. If an agent executes multiple tool calls, users often need progress updates before completion. Use streaming to surface intermediate messages and tool activity as they happen.

```python
from langchain.messages import AIMessage, HumanMessage

stream = agent.stream_events(
    {"messages": [{"role": "user", "content": "Search for AI news and summarize the findings"}]},
    version="v3",
)
for snapshot in stream.values:
    # Each snapshot contains the full state at that point
    latest_message = snapshot["messages"][-1]
    if latest_message.content:
        if isinstance(latest_message, HumanMessage):
            print(f"User: {latest_message.content}")
        elif isinstance(latest_message, AIMessage):
            print(f"Agent: {latest_message.content}")
    elif latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
```

- [View example trace](https://smith.langchain.com/public/7331dcc8-fbc7-4d2e-91fa-f32b4a6f410d/r)

  Open a public LangSmith run for this example.

**Tip:**

For streaming modes, event types, and UI patterns, see [Streaming](/oss/langchain/streaming).

## Configure the harness

`create_agent` is highly extensible. Middleware is the primitive for customization: each piece handles one concern, hooks into the agent loop at the right moment, and composes freely with any other. Take exactly what your use case needs and skip the rest.

Common patterns are prebuilt as first-class middleware. You can build anything else as [custom middleware](/oss/langchain/middleware/custom).

As agents take on complex work, they need support across a few key areas. The middleware ecosystem provides:

- [Execution environment](#execution-environment)

    Tools, filesystem, sandboxes, and code execution

- [Context management](#context-management)

    Summarization, memory, skills, and prompt caching

- [Planning and delegation](#planning-and-delegation)

    Todo lists and subagents for parallel, isolated work

- [Fault tolerance](#fault-tolerance)

    Retries, fallbacks, and call limits

- [Guardrails](#guardrails)

    PII detection and content controls

- [Steering](#steering)

    Human-in-the-loop approval before high-impact actions

**Tip:**

`create_deep_agent` pre-assembles this stack for long-running coding and research tasks (filesystem, summarization, subagents, and prompt caching included by default). See [Deep Agents](/oss/deepagents/harness) for the full prebuilt harness.

### Execution environment

Agents are especially useful when they can take action rather than just generate text. The execution environment gives the agent a workspace: tools it can call, a filesystem for reading and writing files across turns, and code execution for running scripts or shell commands.

```python Google
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[search],
    middleware=[FilesystemMiddleware(backend=StateBackend())],
)
```

```python OpenAI
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[search],
    middleware=[FilesystemMiddleware(backend=StateBackend())],
)
```

```python Anthropic
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[search],
    middleware=[FilesystemMiddleware(backend=StateBackend())],
)
```

```python OpenRouter
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[search],
    middleware=[FilesystemMiddleware(backend=StateBackend())],
)
```

```python Fireworks
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[search],
    middleware=[FilesystemMiddleware(backend=StateBackend())],
)
```

```python Baseten
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[search],
    middleware=[FilesystemMiddleware(backend=StateBackend())],
)
```

```python Ollama
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[search],
    middleware=[FilesystemMiddleware(backend=StateBackend())],
)
```

See `FilesystemMiddleware`, [Sandboxes](/oss/deepagents/sandboxes), [Interpreters](/oss/deepagents/interpreters).

**Note:**

This example imports from the `deepagents` package. Install it with:

```bash pip
pip install deepagents
```

```bash uv
uv add deepagents
```

### Context management

Every model call has a fixed context window. As an agent runs, that window fills with accumulating history, tool results, and intermediate steps. Summarization compresses history before overflow hits; memory loads persistent instructions at startup so knowledge carries across sessions; skills surface domain knowledge on demand rather than loading everything upfront.

```python Google
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware, SummarizationMiddleware

backend = StateBackend()
model = "google_genai:gemini-3.6-flash"

agent = create_agent(
    model=model,
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        MemoryMiddleware(backend=backend, sources=["./AGENTS.md"]),
        SkillsMiddleware(backend=backend, sources=["./skills/"]),
    ],
)
```

```python OpenAI
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware, SummarizationMiddleware

backend = StateBackend()
model = "openai:gpt-5.5"

agent = create_agent(
    model=model,
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        MemoryMiddleware(backend=backend, sources=["./AGENTS.md"]),
        SkillsMiddleware(backend=backend, sources=["./skills/"]),
    ],
)
```

```python Anthropic
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware, SummarizationMiddleware

backend = StateBackend()
model = "anthropic:claude-sonnet-5"

agent = create_agent(
    model=model,
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        MemoryMiddleware(backend=backend, sources=["./AGENTS.md"]),
        SkillsMiddleware(backend=backend, sources=["./skills/"]),
    ],
)
```

```python OpenRouter
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware, SummarizationMiddleware

backend = StateBackend()
model = "openrouter:z-ai/glm-5.2"

agent = create_agent(
    model=model,
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        MemoryMiddleware(backend=backend, sources=["./AGENTS.md"]),
        SkillsMiddleware(backend=backend, sources=["./skills/"]),
    ],
)
```

```python Fireworks
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware, SummarizationMiddleware

backend = StateBackend()
model = "fireworks:accounts/fireworks/models/glm-5p2"

agent = create_agent(
    model=model,
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        MemoryMiddleware(backend=backend, sources=["./AGENTS.md"]),
        SkillsMiddleware(backend=backend, sources=["./skills/"]),
    ],
)
```

```python Baseten
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware, SummarizationMiddleware

backend = StateBackend()
model = "baseten:zai-org/GLM-5.2"

agent = create_agent(
    model=model,
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        MemoryMiddleware(backend=backend, sources=["./AGENTS.md"]),
        SkillsMiddleware(backend=backend, sources=["./skills/"]),
    ],
)
```

```python Ollama
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware, SummarizationMiddleware

backend = StateBackend()
model = "ollama:north-mini-code-1.0"

agent = create_agent(
    model=model,
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        MemoryMiddleware(backend=backend, sources=["./AGENTS.md"]),
        SkillsMiddleware(backend=backend, sources=["./skills/"]),
    ],
)
```

See `SummarizationMiddleware`, `MemoryMiddleware`, [Skills](/oss/langchain/multi-agent/skills), [Context engineering](/oss/deepagents/context-engineering).

**Note:**

This example imports from the `deepagents` package. Install it with:

```bash pip
pip install deepagents
```

```bash uv
uv add deepagents
```

### Planning and delegation

Complex tasks often exceed what one context window can handle. Delegation lets the main agent break work into pieces, hand them to subagents that each run in their own isolated context, and stay focused on coordination rather than execution. Work can run in parallel; the main agent's context stays clean.

```python Google
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

backend = StateBackend()

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        TodoListMiddleware(),
        SubAgentMiddleware(
            backend=backend,
            subagents=[
                {
                    "name": "researcher",
                    "description": "Searches and returns a structured summary.",
                    "system_prompt": "Use the search tool to research the question and summarize key points.",
                    "tools": [search],
                    "model": "anthropic:claude-sonnet-4-6",
                    "middleware": [],
                }
            ],
        ),
    ],
)
```

```python OpenAI
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

backend = StateBackend()

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        TodoListMiddleware(),
        SubAgentMiddleware(
            backend=backend,
            subagents=[
                {
                    "name": "researcher",
                    "description": "Searches and returns a structured summary.",
                    "system_prompt": "Use the search tool to research the question and summarize key points.",
                    "tools": [search],
                    "model": "anthropic:claude-sonnet-4-6",
                    "middleware": [],
                }
            ],
        ),
    ],
)
```

```python Anthropic
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

backend = StateBackend()

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        TodoListMiddleware(),
        SubAgentMiddleware(
            backend=backend,
            subagents=[
                {
                    "name": "researcher",
                    "description": "Searches and returns a structured summary.",
                    "system_prompt": "Use the search tool to research the question and summarize key points.",
                    "tools": [search],
                    "model": "anthropic:claude-sonnet-4-6",
                    "middleware": [],
                }
            ],
        ),
    ],
)
```

```python OpenRouter
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

backend = StateBackend()

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        TodoListMiddleware(),
        SubAgentMiddleware(
            backend=backend,
            subagents=[
                {
                    "name": "researcher",
                    "description": "Searches and returns a structured summary.",
                    "system_prompt": "Use the search tool to research the question and summarize key points.",
                    "tools": [search],
                    "model": "anthropic:claude-sonnet-4-6",
                    "middleware": [],
                }
            ],
        ),
    ],
)
```

```python Fireworks
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

backend = StateBackend()

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        TodoListMiddleware(),
        SubAgentMiddleware(
            backend=backend,
            subagents=[
                {
                    "name": "researcher",
                    "description": "Searches and returns a structured summary.",
                    "system_prompt": "Use the search tool to research the question and summarize key points.",
                    "tools": [search],
                    "model": "anthropic:claude-sonnet-4-6",
                    "middleware": [],
                }
            ],
        ),
    ],
)
```

```python Baseten
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

backend = StateBackend()

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        TodoListMiddleware(),
        SubAgentMiddleware(
            backend=backend,
            subagents=[
                {
                    "name": "researcher",
                    "description": "Searches and returns a structured summary.",
                    "system_prompt": "Use the search tool to research the question and summarize key points.",
                    "tools": [search],
                    "model": "anthropic:claude-sonnet-4-6",
                    "middleware": [],
                }
            ],
        ),
    ],
)
```

```python Ollama
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

backend = StateBackend()

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[search],
    middleware=[
        FilesystemMiddleware(backend=backend),
        TodoListMiddleware(),
        SubAgentMiddleware(
            backend=backend,
            subagents=[
                {
                    "name": "researcher",
                    "description": "Searches and returns a structured summary.",
                    "system_prompt": "Use the search tool to research the question and summarize key points.",
                    "tools": [search],
                    "model": "anthropic:claude-sonnet-4-6",
                    "middleware": [],
                }
            ],
        ),
    ],
)
```

See [Subagents](/oss/langchain/multi-agent/subagents).

**Note:**

This example imports from the `deepagents` package. Install it with:

```bash pip
pip install deepagents
```

```bash uv
uv add deepagents
```

### Name your agent

Optionally use an identifier for the agent. This is especially useful when embedding the agent as a subgraph in [multi-agent](/oss/langchain/multi-agent) systems.

```python Google
agent = create_agent(model="google_genai:gemini-3.6-flash", tools=tools, name="research_assistant")
```

```python OpenAI
agent = create_agent(model="openai:gpt-5.5", tools=tools, name="research_assistant")
```

```python Anthropic
agent = create_agent(model="anthropic:claude-sonnet-5", tools=tools, name="research_assistant")
```

```python OpenRouter
agent = create_agent(model="openrouter:z-ai/glm-5.2", tools=tools, name="research_assistant")
```

```python Fireworks
agent = create_agent(model="fireworks:accounts/fireworks/models/glm-5p2", tools=tools, name="research_assistant")
```

```python Baseten
agent = create_agent(model="baseten:zai-org/GLM-5.2", tools=tools, name="research_assistant")
```

```python Ollama
agent = create_agent(model="ollama:north-mini-code-1.0", tools=tools, name="research_assistant")
```

### Fault tolerance

Agents in production encounter failures that rarely appear in development: rate limits, model timeouts, transient API errors. Fault tolerance middleware handles these at the infrastructure level so your tools and business logic don't need try/catch around every call.

```python Google
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[search],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(max_retries=2),
    ],
)
```

```python OpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[search],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(max_retries=2),
    ],
)
```

```python Anthropic
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[search],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(max_retries=2),
    ],
)
```

```python OpenRouter
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[search],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(max_retries=2),
    ],
)
```

```python Fireworks
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[search],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(max_retries=2),
    ],
)
```

```python Baseten
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[search],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(max_retries=2),
    ],
)
```

```python Ollama
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[search],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(max_retries=2),
    ],
)
```

See `ModelRetryMiddleware`, `ToolRetryMiddleware`, [Prebuilt middleware](/oss/langchain/middleware/built-in).

### Guardrails

Some policies can't live in a prompt—they need to be enforced deterministically regardless of what the model does. Guardrails intercept data as it flows through the agent loop, applying compliance rules or content policies before tool results reach the model's context.

```python Google
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[search],
    middleware=[PIIMiddleware("email")],
)
```

```python OpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[search],
    middleware=[PIIMiddleware("email")],
)
```

```python Anthropic
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[search],
    middleware=[PIIMiddleware("email")],
)
```

```python OpenRouter
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[search],
    middleware=[PIIMiddleware("email")],
)
```

```python Fireworks
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[search],
    middleware=[PIIMiddleware("email")],
)
```

```python Baseten
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[search],
    middleware=[PIIMiddleware("email")],
)
```

```python Ollama
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[search],
    middleware=[PIIMiddleware("email")],
)
```

See `PIIMiddleware`, [Prebuilt middleware](/oss/langchain/middleware/built-in).

### Steering

Full autonomy isn't always appropriate. Steering lets you place humans at specific decision points—before destructive writes, expensive API calls, or anything requiring judgment—without restructuring your agent. The agent pauses and waits; a human approves, edits, or rejects; execution continues.

```python Google
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[search],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"write_file": True})],
)
```

```python OpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[search],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"write_file": True})],
)
```

```python Anthropic
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[search],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"write_file": True})],
)
```

```python OpenRouter
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[search],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"write_file": True})],
)
```

```python Fireworks
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[search],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"write_file": True})],
)
```

```python Baseten
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[search],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"write_file": True})],
)
```

```python Ollama
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[search],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"write_file": True})],
)
```

See `HumanInTheLoopMiddleware`, [Human-in-the-loop](/oss/langchain/human-in-the-loop).

### Middleware resources

- [Middleware overview](/oss/langchain/middleware/overview)

    How the middleware stack works and when hooks fire

- [Prebuilt middleware](/oss/langchain/middleware/built-in)

    Full reference with configuration examples

- [Custom middleware](/oss/langchain/middleware/custom)

    Write your own hooks for business logic, PII scrubbing, and more

---

# Component architecture
> 출처: data/raw/langchain/component-architecture.mdx | https://docs.langchain.com/oss/python/langchain/component-architecture

LangChain's power comes from how its components work together to create sophisticated AI applications. This page provides diagrams showcasing the relationships between different components.

## Core component ecosystem

The diagram below shows how LangChain's major components connect to form complete AI applications:

```mermaid
graph TD
    %% Input processing
    subgraph "📥 Input processing"
        A[Text input] --> B[Document loaders]
        B --> C[Text splitters]
        C --> D[Documents]
    end

%% Embedding & storage
subgraph "🔢 Embedding & storage"
    D --> E[Embedding models]
    E --> F[Vectors]
    F --> G[(Vector stores)]
end

%% Retrieval
subgraph "🔍 Retrieval"
    H[User Query] --> I[Embedding models]
    I --> J[Query vector]
    J --> K[Retrievers]
    K --> G
    G --> L[Relevant context]
end

%% Generation
subgraph "🤖 Generation"
    M[Chat models] --> N[Tools]
    N --> O[Tool results]
    O --> M
    L --> M
    M --> P[AI response]
end

%% Orchestration
subgraph "🎯 Orchestration"
    Q[Agents] --> M
    Q --> N
    Q --> K
    Q --> R[Memory]
end

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

    class A,H trigger
    class B,C,E,I,K,M,N,Q process
    class D,F,J,L,O,P,R neutral
    class G output
```

### How components connect

Each component layer builds on the previous ones:

1. **Input processing** – Transform raw data into structured documents
2. **Embedding & storage** – Convert text into searchable vector representations
3. **Retrieval** – Find relevant information based on user queries
4. **Generation** – Use AI models to create responses, optionally with tools
5. **Orchestration** – Coordinate everything through agents and memory systems

## Component categories

LangChain organizes components into these main categories:

| Category | Purpose | Key Components | Use Cases |
|----------|---------|---------------|-----------|
| **[Models](/oss/langchain/models)** | AI reasoning and generation | Chat models, LLMs, Embedding models | Text generation, reasoning, semantic understanding |
| **[Tools](/oss/langchain/tools)** | External capabilities | APIs, databases, etc. | Web search, data access, computations |
| **[Agents](/oss/langchain/agents)** | Orchestration and reasoning | ReAct agents, tool calling agents | Nondeterministic workflows, decision making |
| **[Memory](/oss/langchain/short-term-memory)** | Context preservation | Message history, custom state | Conversations, stateful interactions |
| **[Retrievers](/oss/integrations/retrievers)** | Information access | Vector retrievers, web retrievers | RAG, knowledge base search |
| **[Document processing](/oss/integrations/document_loaders)** | Data ingestion | Loaders, splitters, transformers | PDF processing, web scraping |
| **[Vector Stores](/oss/integrations/vectorstores)** | Semantic search | Chroma, Pinecone, FAISS | Similarity search, embeddings storage |

## Common patterns

### RAG (Retrieval-Augmented generation)
```mermaid
graph LR
    A[User question] --> B[Retriever]
    B --> C[Relevant docs]
    C --> D[Chat model]
    A --> D
    D --> E[Informed response]

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

    class A trigger
    class B,D process
    class C,E neutral
```

### Agent with tools
```mermaid
graph LR
    A[User request] --> B[Agent]
    B --> C{Need tool?}
    C -->|Yes| D[Call tool]
    D --> E[Tool result]
    E --> B
    C -->|No| F[Final answer]

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
classDef decision fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

    class A trigger
    class B,D process
    class C decision
    class E,F neutral
```

### Multi-agent system
```mermaid
graph LR
    A[Complex Task] --> B[Supervisor agent]
    B --> C[Specialist agent 1]
    B --> D[Specialist agent 2]
    C --> E[Results]
    D --> E
    E --> B
    B --> F[Coordinated response]

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

    class A trigger
    class B,C,D process
    class E,F neutral
```

## Learn more

- [Creating agents](/oss/langchain/agents)
- [Working with tools](/oss/langchain/tools)
- [Browse integrations](/oss/integrations/providers/overview)

---

# Context engineering in agents
> 출처: data/raw/langchain/context-engineering.mdx | https://docs.langchain.com/oss/python/langchain/context-engineering

## Overview

The hard part of building agents (or any LLM application) is making them reliable enough. While they may work for a prototype, they often fail in real-world use cases.

### Why do agents fail?

When agents fail, it's usually because the LLM call inside the agent took the wrong action / didn't do what we expected. LLMs fail for one of two reasons:

1. The underlying LLM is not capable enough
2. The "right" context was not passed to the LLM

More often than not - it's actually the second reason that causes agents to not be reliable.

**Context engineering** is providing the right information and tools in the right format so the LLM can accomplish a task. This is the number one job of AI Engineers. This lack of "right" context is the number one blocker for more reliable agents, and LangChain's agent abstractions are uniquely designed to facilitate context engineering.

**Tip:**

New to context engineering? Start with the [conceptual overview](/oss/concepts/context) to understand the different types of context and when to use them.

### The agent loop

A typical agent loop consists of two main steps:

1. **Model call** - calls the LLM with a prompt and available tools, returns either a response or a request to execute tools
2. **Tool execution** - executes the tools that the LLM requested, returns tool results

This loop continues until the LLM decides to finish.

### What you can control

To build reliable agents, you need to control what happens at each step of the agent loop, as well as what happens between steps.

| Context Type | What You Control | Transient or Persistent |
|--------------|------------------|-------------------------|
| **[Model Context](#model-context)** | What goes into model calls (instructions, message history, tools, response format) | Transient |
| **[Tool Context](#tool-context)** | What tools can access and produce (reads/writes to state, store, runtime context) | Persistent |
| **[Life-cycle Context](#life-cycle-context)** | What happens between model and tool calls (summarization, guardrails, logging, etc.) | Persistent |

- **Transient context**

    What the LLM sees for a single call. You can modify messages, tools, or prompts without changing what's saved in state.

- **Persistent context**

    What gets saved in state across turns. Life-cycle hooks and tool writes modify this permanently.

### Data sources

Throughout this process, your agent accesses (reads / writes) different sources of data:

| Data Source | Also Known As | Scope | Examples |
|-------------|---------------|-------|----------|
| **Runtime Context** | Static configuration | Conversation-scoped | User ID, API keys, database connections, permissions, environment settings |
| **State** | Short-term memory | Conversation-scoped | Current messages, uploaded files, authentication status, tool results |
| **Store** | Long-term memory | Cross-conversation | User preferences, extracted insights, memories, historical data |

### How it works

LangChain [middleware](/oss/langchain/middleware) is the mechanism under the hood that makes context engineering practical for developers using LangChain.

Middleware allows you to hook into any step in the agent lifecycle and:

* Update context
* Jump to a different step in the agent lifecycle

Throughout this guide, you'll see frequent use of the middleware API as a means to the context engineering end.

## Model context

Control what goes into each model call - instructions, available tools, which model to use, and output format. These decisions directly impact reliability and cost.

- [System Prompt](#system-prompt)

        Base instructions from the developer to the LLM.

- [Messages](#messages)

        The full list of messages (conversation history) sent to the LLM.

- [Tools](#tools)

        Utilities the agent has access to for taking actions.

- [Model](#model)

        The actual model (including configuration) to be called.

- [Response Format](#response-format)

        Schema specification for the model's final response.

All of these types of model context can draw from **state** (short-term memory), **store** (long-term memory), or **runtime context** (static configuration).

### System Prompt

The system prompt sets the LLM's behavior and capabilities. Different users, contexts, or conversation stages need different instructions. Successful agents draw on memories, preferences, and configuration to provide the right instructions for the current state of the conversation.

**State**

Access message count or conversation context from state:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest

@dynamic_prompt
def state_aware_prompt(request: ModelRequest) -> str:
    # request.messages is a shortcut for request.state["messages"]
    message_count = len(request.messages)

base = "You are a helpful assistant."

if message_count > 10:
    base += "\nThis is a long conversation - be extra concise."

return base

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[state_aware_prompt]
)
```

**Store**

Access user preferences from long-term memory:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

@dynamic_prompt
def store_aware_prompt(request: ModelRequest) -> str:
    user_id = request.runtime.context.user_id

# Read from Store: get user preferences
store = request.runtime.store
user_prefs = store.get(("preferences",), user_id)

base = "You are a helpful assistant."

if user_prefs:
    style = user_prefs.value.get("communication_style", "balanced")
    base += f"\nUser prefers {style} responses."

return base

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[store_aware_prompt],
    context_schema=Context,
    store=InMemoryStore()
)
```

**Runtime Context**

Access user ID or configuration from Runtime Context:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest

@dataclass
class Context:
    user_role: str
    deployment_env: str

@dynamic_prompt
def context_aware_prompt(request: ModelRequest) -> str:
    # Read from Runtime Context: user role and environment
    user_role = request.runtime.context.user_role
    env = request.runtime.context.deployment_env

base = "You are a helpful assistant."

if user_role == "admin":
    base += "\nYou have admin access. You can perform all operations."
elif user_role == "viewer":
    base += "\nYou have read-only access. Guide users to read operations only."

if env == "production":
    base += "\nBe extra careful with any data modifications."

return base

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[context_aware_prompt],
    context_schema=Context
)
```

### Messages

Messages make up the prompt that is sent to the LLM.
It's critical to manage the content of messages to ensure that the LLM has the right information to respond well.

**State**

Inject uploaded file context from State when relevant to current query:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@wrap_model_call
def inject_file_context(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Inject context about files user has uploaded this session."""
    # Read from State: get uploaded files metadata
    uploaded_files = request.state.get("uploaded_files", [])  # [!code highlight]

if uploaded_files:
    # Build context about available files
    file_descriptions = []
    for file in uploaded_files:
        file_descriptions.append(
            f"- {file['name']} ({file['type']}): {file['summary']}"
        )

            file_context = f"""Files you have access to in this conversation:
{chr(10).join(file_descriptions)}

Reference these files when answering questions."""

# Inject file context before recent messages
messages = [  # [!code highlight]
    *request.messages,
    {"role": "user", "content": file_context},
]
request = request.override(messages=messages)  # [!code highlight]

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[inject_file_context]
)
```

**Store**

Inject user's email writing style from Store to guide drafting:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

@wrap_model_call
def inject_writing_style(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Inject user's email writing style from Store."""
    user_id = request.runtime.context.user_id  # [!code highlight]

# Read from Store: get user's writing style examples
store = request.runtime.store  # [!code highlight]
writing_style = store.get(("writing_style",), user_id)  # [!code highlight]

        if writing_style:
            style = writing_style.value
            # Build style guide from stored examples
            style_context = f"""Your writing style:
- Tone: {style.get('tone', 'professional')}
- Typical greeting: "{style.get('greeting', 'Hi')}"
- Typical sign-off: "{style.get('sign_off', 'Best')}"
- Example email you've written:
{style.get('example_email', '')}"""

# Append at end - models pay more attention to final messages
messages = [
    *request.messages,
    {"role": "user", "content": style_context}
]
request = request.override(messages=messages)  # [!code highlight]

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[inject_writing_style],
    context_schema=Context,
    store=InMemoryStore()
)
```

**Runtime Context**

Inject compliance rules from Runtime Context based on user's jurisdiction:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@dataclass
class Context:
    user_jurisdiction: str
    industry: str
    compliance_frameworks: list[str]

@wrap_model_call
def inject_compliance_rules(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Inject compliance constraints from Runtime Context."""
    # Read from Runtime Context: get compliance requirements
    jurisdiction = request.runtime.context.user_jurisdiction  # [!code highlight]
    industry = request.runtime.context.industry  # [!code highlight]
    frameworks = request.runtime.context.compliance_frameworks  # [!code highlight]

# Build compliance constraints
rules = []
if "GDPR" in frameworks:
    rules.append("- Must obtain explicit consent before processing personal data")
    rules.append("- Users have right to data deletion")
if "HIPAA" in frameworks:
    rules.append("- Cannot share patient health information without authorization")
    rules.append("- Must use secure, encrypted communication")
if industry == "finance":
    rules.append("- Cannot provide financial advice without proper disclaimers")

        if rules:
            compliance_context = f"""Compliance requirements for {jurisdiction}:
{chr(10).join(rules)}"""

# Append at end - models pay more attention to final messages
messages = [
    *request.messages,
    {"role": "user", "content": compliance_context}
]
request = request.override(messages=messages)  # [!code highlight]

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[inject_compliance_rules],
    context_schema=Context
)
```

**Note:**

**Transient vs Persistent Message Updates:**

The examples above use `wrap_model_call` to make **transient** updates - modifying what messages are sent to the model for a single call without changing what's saved in state.

For **persistent** updates that modify state, you can:

- Return a `ExtendedModelResponse` with a `Command` from `wrap_model_call` to inject state updates from the model call layer.
- Use life-cycle hooks like `before_model`, `after_model`, or `wrap_tool_call` (for tool returns) to update the conversation history. See the [middleware documentation](/oss/langchain/middleware) for more details.

See [State updates](/oss/langchain/middleware/custom#state-updates) for more information.

### Tools

Tools let the model interact with databases, APIs, and external systems. How you define and select tools directly impacts whether the model can complete tasks effectively.

#### Defining tools

Each tool needs a clear name, description, argument names, and argument descriptions. These aren't just metadata—they guide the model's reasoning about when and how to use the tool.

```python
from langchain.tools import tool

@tool(parse_docstring=True)
def search_orders(
    user_id: str,
    status: str,
    limit: int = 10
) -> str:
    """Search for user orders by status.

Use this when the user asks about order history or wants to check
order status. Always filter by the provided status.

    Args:
        user_id: Unique identifier for the user
        status: Order status: 'pending', 'shipped', or 'delivered'
        limit: Maximum number of results to return
    """
    # Implementation here
    pass
```

#### Selecting tools

Not every tool is appropriate for every situation. Too many tools may overwhelm the model (overload context) and increase errors; too few limit capabilities. Dynamic tool selection adapts the available toolset based on authentication state, user permissions, feature flags, or conversation stage.

**State**

Enable advanced tools only after certain conversation milestones:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@wrap_model_call
def state_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on conversation State."""
    # Read from State: check if user has authenticated
    state = request.state  # [!code highlight]
    is_authenticated = state.get("authenticated", False)  # [!code highlight]
    message_count = len(state["messages"])

# Only enable sensitive tools after authentication
if not is_authenticated:
    tools = [t for t in request.tools if t.name.startswith("public_")]
    request = request.override(tools=tools)  # [!code highlight]
elif message_count < 5:
    # Limit tools early in conversation
    tools = [t for t in request.tools if t.name != "advanced_search"]
    request = request.override(tools=tools)  # [!code highlight]

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[public_search, private_search, advanced_search],
    middleware=[state_based_tools]
)
```

**Store**

Filter tools based on user preferences or feature flags in Store:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

@wrap_model_call
def store_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on Store preferences."""
    user_id = request.runtime.context.user_id

# Read from Store: get user's enabled features
store = request.runtime.store
feature_flags = store.get(("features",), user_id)

if feature_flags:
    enabled_features = feature_flags.value.get("enabled_tools", [])
    # Only include tools that are enabled for this user
    tools = [t for t in request.tools if t.name in enabled_features]
    request = request.override(tools=tools)

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, analysis_tool, export_tool],
    middleware=[store_based_tools],
    context_schema=Context,
    store=InMemoryStore()
)
```

**Runtime Context**

Filter tools based on user permissions from Runtime Context:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@dataclass
class Context:
    user_role: str

@wrap_model_call
def context_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on Runtime Context permissions."""
    # Read from Runtime Context: get user role
    user_role = request.runtime.context.user_role

if user_role == "admin":
    # Admins get all tools
    pass
elif user_role == "editor":
    # Editors can't delete
    tools = [t for t in request.tools if t.name != "delete_data"]
    request = request.override(tools=tools)
else:
    # Viewers get read-only tools
    tools = [t for t in request.tools if t.name.startswith("read_")]
    request = request.override(tools=tools)

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[read_data, write_data, delete_data],
    middleware=[context_based_tools],
    context_schema=Context
)
```

See [Dynamic tools](/oss/langchain/tools#dynamic-tool-selection) for both filtering pre-registered tools and registering tools at runtime (e.g., from MCP servers).

### Model

Different models have different strengths, costs, and context windows. Select the right model for the task at hand, which
might change during an agent run.

**State**

Use different models based on conversation length from State:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.chat_models import init_chat_model
from typing import Callable

# Initialize models once outside the middleware
large_model = init_chat_model("claude-sonnet-4-6")
standard_model = init_chat_model("gpt-5.5")
efficient_model = init_chat_model("gpt-5.4-mini")

@wrap_model_call
def state_based_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Select model based on State conversation length."""
    # request.messages is a shortcut for request.state["messages"]
    message_count = len(request.messages)  # [!code highlight]

if message_count > 20:
    # Long conversation - use model with larger context window
    model = large_model
elif message_count > 10:
    # Medium conversation
    model = standard_model
else:
    # Short conversation - use efficient model
    model = efficient_model

request = request.override(model=model)  # [!code highlight]

return handler(request)

agent = create_agent(
    model="gpt-5.4-mini",
    tools=[...],
    middleware=[state_based_model]
)
```

**Store**

Use user's preferred model from Store:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.chat_models import init_chat_model
from typing import Callable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

# Initialize available models once
MODEL_MAP = {
    "gpt-5.5": init_chat_model("gpt-5.5"),
    "gpt-5.4-mini": init_chat_model("gpt-5.4-mini"),
    "claude-sonnet": init_chat_model("claude-sonnet-4-6"),
}

@wrap_model_call
def store_based_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Select model based on Store preferences."""
    user_id = request.runtime.context.user_id

# Read from Store: get user's preferred model
store = request.runtime.store
user_prefs = store.get(("preferences",), user_id)

if user_prefs:
    preferred_model = user_prefs.value.get("preferred_model")
    if preferred_model and preferred_model in MODEL_MAP:
        request = request.override(model=MODEL_MAP[preferred_model])

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[store_based_model],
    context_schema=Context,
    store=InMemoryStore()
)
```

**Runtime Context**

Select model based on cost limits or environment from Runtime Context:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.chat_models import init_chat_model
from typing import Callable

@dataclass
class Context:
    cost_tier: str
    environment: str

# Initialize models once outside the middleware
premium_model = init_chat_model("claude-sonnet-4-6")
standard_model = init_chat_model("gpt-5.5")
budget_model = init_chat_model("gpt-5.4-mini")

@wrap_model_call
def context_based_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Select model based on Runtime Context."""
    # Read from Runtime Context: cost tier and environment
    cost_tier = request.runtime.context.cost_tier
    environment = request.runtime.context.environment

if environment == "production" and cost_tier == "premium":
    # Production premium users get best model
    model = premium_model
elif cost_tier == "budget":
    # Budget tier gets efficient model
    model = budget_model
else:
    # Standard tier
    model = standard_model

request = request.override(model=model)

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[context_based_model],
    context_schema=Context
)
```

See [Dynamic model](/oss/langchain/models#dynamic-model-selection) for more examples.

### Response format

Structured output transforms unstructured text into validated, structured data. When extracting specific fields or returning data for downstream systems, free-form text isn't sufficient.

**How it works:** When you provide a schema as the response format, the model's final response is guaranteed to conform to that schema. The agent runs the model / tool calling loop until the model is done calling tools, then the final response is coerced into the provided format.

#### Defining formats

Schema definitions guide the model. Field names, types, and descriptions specify exactly what format the output should adhere to.

```python
from pydantic import BaseModel, Field

class CustomerSupportTicket(BaseModel):
    """Structured ticket information extracted from customer message."""

    category: str = Field(
        description="Issue category: 'billing', 'technical', 'account', or 'product'"
    )
    priority: str = Field(
        description="Urgency level: 'low', 'medium', 'high', or 'critical'"
    )
    summary: str = Field(
        description="One-sentence summary of the customer's issue"
    )
    customer_sentiment: str = Field(
        description="Customer's emotional tone: 'frustrated', 'neutral', or 'satisfied'"
    )
```

#### Selecting formats

Dynamic response format selection adapts schemas based on user preferences, conversation stage, or role—returning simple formats early and detailed formats as complexity increases.

**State**

Configure structured output based on conversation state:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from pydantic import BaseModel, Field
from typing import Callable

class SimpleResponse(BaseModel):
    """Simple response for early conversation."""
    answer: str = Field(description="A brief answer")

class DetailedResponse(BaseModel):
    """Detailed response for established conversation."""
    answer: str = Field(description="A detailed answer")
    reasoning: str = Field(description="Explanation of reasoning")
    confidence: float = Field(description="Confidence score 0-1")

@wrap_model_call
def state_based_output(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Select output format based on State."""
    # request.messages is a shortcut for request.state["messages"]
    message_count = len(request.messages)  # [!code highlight]

if message_count < 3:
    # Early conversation - use simple format
    request = request.override(response_format=SimpleResponse)  # [!code highlight]
else:
    # Established conversation - use detailed format
    request = request.override(response_format=DetailedResponse)  # [!code highlight]

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[state_based_output]
)
```

**Store**

Configure output format based on user preferences in Store:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from pydantic import BaseModel, Field
from typing import Callable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

class VerboseResponse(BaseModel):
    """Verbose response with details."""
    answer: str = Field(description="Detailed answer")
    sources: list[str] = Field(description="Sources used")

class ConciseResponse(BaseModel):
    """Concise response."""
    answer: str = Field(description="Brief answer")

@wrap_model_call
def store_based_output(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Select output format based on Store preferences."""
    user_id = request.runtime.context.user_id

# Read from Store: get user's preferred response style
store = request.runtime.store
user_prefs = store.get(("preferences",), user_id)

if user_prefs:
    style = user_prefs.value.get("response_style", "concise")
    if style == "verbose":
        request = request.override(response_format=VerboseResponse)
    else:
        request = request.override(response_format=ConciseResponse)

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[store_based_output],
    context_schema=Context,
    store=InMemoryStore()
)
```

**Runtime Context**

Configure output format based on Runtime Context like user role or environment:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from pydantic import BaseModel, Field
from typing import Callable

@dataclass
class Context:
    user_role: str
    environment: str

class AdminResponse(BaseModel):
    """Response with technical details for admins."""
    answer: str = Field(description="Answer")
    debug_info: dict = Field(description="Debug information")
    system_status: str = Field(description="System status")

class UserResponse(BaseModel):
    """Simple response for regular users."""
    answer: str = Field(description="Answer")

@wrap_model_call
def context_based_output(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Select output format based on Runtime Context."""
    # Read from Runtime Context: user role and environment
    user_role = request.runtime.context.user_role
    environment = request.runtime.context.environment

if user_role == "admin" and environment == "production":
    # Admins in production get detailed output
    request = request.override(response_format=AdminResponse)
else:
    # Regular users get simple output
    request = request.override(response_format=UserResponse)

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[context_based_output],
    context_schema=Context
)
```

## Tool context

Tools are special in that they both read and write context.

In the most basic case, when a tool executes, it receives the LLM's request parameters and returns a tool message back. The tool does its work and produces a result.

Tools can also fetch important information for the model that allows it to perform and complete tasks.

### Reads

Most real-world tools need more than just the LLM's parameters. They need user IDs for database queries, API keys for external services, or current session state to make decisions. Tools read from state, store, and runtime context to access this information.

**State**

Read from State to check current session information:

```python
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent

@tool
def check_authentication(
    runtime: ToolRuntime
) -> str:
    """Check if user is authenticated."""
    # Read from State: check current auth status
    current_state = runtime.state
    is_authenticated = current_state.get("authenticated", False)

if is_authenticated:
    return "User is authenticated"
else:
    return "User is not authenticated"

agent = create_agent(
    model="gpt-5.5",
    tools=[check_authentication]
)
```

**Store**

Read from Store to access persisted user preferences:

```python
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

@tool
def get_preference(
    preference_key: str,
    runtime: ToolRuntime[Context]
) -> str:
    """Get user preference from Store."""
    user_id = runtime.context.user_id

# Read from Store: get existing preferences
store = runtime.store
existing_prefs = store.get(("preferences",), user_id)

if existing_prefs:
    value = existing_prefs.value.get(preference_key)
    return f"{preference_key}: {value}" if value else f"No preference set for {preference_key}"
else:
    return "No preferences found"

agent = create_agent(
    model="gpt-5.5",
    tools=[get_preference],
    context_schema=Context,
    store=InMemoryStore()
)
```

**Runtime Context**

Read from Runtime Context for configuration like API keys and user IDs:

```python
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent

@dataclass
class Context:
    user_id: str
    api_key: str
    db_connection: str

@tool
def fetch_user_data(
    query: str,
    runtime: ToolRuntime[Context]
) -> str:
    """Fetch data using Runtime Context configuration."""
    # Read from Runtime Context: get API key and DB connection
    user_id = runtime.context.user_id
    api_key = runtime.context.api_key
    db_connection = runtime.context.db_connection

# Use configuration to fetch data
results = perform_database_query(db_connection, query, api_key)

return f"Found {len(results)} results for user {user_id}"

agent = create_agent(
    model="gpt-5.5",
    tools=[fetch_user_data],
    context_schema=Context
)

# Invoke with runtime context
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Get my data"}]},
    context=Context(
        user_id="user_123",
        api_key="sk-...",
        db_connection="postgresql://..."
    )
)
```

### Writes

Tool results can be used to help an agent complete a given task. Tools can both return results directly to the model
and update the memory of the agent to make important context available to future steps.

**State**

Write to State to track session-specific information using Command:

```python
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langgraph.types import Command

@tool
def authenticate_user(
    password: str,
    runtime: ToolRuntime
) -> Command:
    """Authenticate user and update State."""
    # Perform authentication (simplified)
    if password == "correct":
        # Write to State: mark as authenticated using Command
        return Command(
            update={"authenticated": True},
        )
    else:
        return Command(update={"authenticated": False})

agent = create_agent(
    model="gpt-5.5",
    tools=[authenticate_user]
)
```

**Store**

Write to Store to persist data across sessions:

```python
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

@tool
def save_preference(
    preference_key: str,
    preference_value: str,
    runtime: ToolRuntime[Context]
) -> str:
    """Save user preference to Store."""
    user_id = runtime.context.user_id

# Read existing preferences
store = runtime.store
existing_prefs = store.get(("preferences",), user_id)

# Merge with new preference
prefs = existing_prefs.value if existing_prefs else {}
prefs[preference_key] = preference_value

# Write to Store: save updated preferences
store.put(("preferences",), user_id, prefs)

return f"Saved preference: {preference_key} = {preference_value}"

agent = create_agent(
    model="gpt-5.5",
    tools=[save_preference],
    context_schema=Context,
    store=InMemoryStore()
)
```

See [Tools](/oss/langchain/tools) for comprehensive examples of accessing state, store, and runtime context in tools.

## Life-cycle context

Control what happens **between** the core agent steps - intercepting data flow to implement cross-cutting concerns like summarization, guardrails, and logging.

As you've seen in [Model Context](#model-context) and [Tool Context](#tool-context), [middleware](/oss/langchain/middleware) is the mechanism that makes context engineering practical. Middleware allows you to hook into any step in the agent lifecycle and either:

1. **Update context** - Modify state and store to persist changes, update conversation history, or save insights
2. **Jump in the lifecycle** - Move to different steps in the agent cycle based on context (e.g., skip tool execution if a condition is met, repeat model call with modified context)

### Example: Summarization

One of the most common life-cycle patterns is automatically condensing conversation history when it gets too long. Unlike the transient message trimming shown in [Model Context](#messages), summarization **persistently updates state** - permanently replacing old messages with a summary that's saved for all future turns.

LangChain offers built-in middleware for this:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger={"tokens": 4000},
            keep=("messages", 20),
        ),
    ],
)
```

When the conversation exceeds the token limit, `SummarizationMiddleware` automatically:
1. Summarizes older messages using a separate LLM call
2. Replaces them with a summary message in State (permanently)
3. Keeps recent messages intact for context

The summarized conversation history is permanently updated - future turns will see the summary instead of the original messages.

**Note:**

For a complete list of built-in middleware, available hooks, and how to create custom middleware, see the [Middleware documentation](/oss/langchain/middleware).

## Best practices

1. **Start simple** - Begin with static prompts and tools, add dynamics only when needed
2. **Test incrementally** - Add one context engineering feature at a time
3. **Monitor performance** - Track model calls, token usage, and latency
4. **Use built-in middleware** - Leverage [`SummarizationMiddleware`](/oss/langchain/middleware#summarization), [`LLMToolSelectorMiddleware`](/oss/langchain/middleware#llm-tool-selector), etc.
5. **Document your context strategy** - Make it clear what context is being passed and why
6. **Understand transient vs persistent**: Model context changes are transient (per-call), while life-cycle context changes persist to state

## Related resources

- [Context conceptual overview](/oss/concepts/context) - Understand context types and when to use them
- [Middleware](/oss/langchain/middleware) - Complete middleware guide
- [Tools](/oss/langchain/tools) - Tool creation and context access
- [Memory](/oss/concepts/memory) - Short-term and long-term memory patterns
- [Agents](/oss/langchain/agents) - Core agent concepts

---

# Build a data analysis agent from scratch
> 출처: data/raw/langchain/deep-agent-from-scratch.mdx | https://docs.langchain.com/oss/python/langchain/deep-agent-from-scratch

Build a data analysis agent step by step using create_agent and Deep Agents middleware.

This guide builds a data analysis agent from first principles using `create_agent` and Deep Agents middleware.

Both `create_agent` and `create_deep_agent` provide you with fine-grained control over tools, memory, and more.
The main difference between both is that Deep Agents comes with a range of commonly useful capabilities already built in, such as planning, file system tools, and subagents.
If the Deep Agents default harness does not fit your needs, this guide shows you how to start with `create_agent` and assemble the harness one piece at a time, so you can see exactly what each component adds and swap in only what your use case needs.

Follow this guide to build an agent that:

1. Accepts a CSV file for analysis
2. Writes and executes Python code in an isolated sandbox
3. Delegates visualization work to a specialized subagent
4. Loads data analysis patterns from a skills file

The final stack mirrors what `create_deep_agent` assembles by default.

## What you will learn

Each step adds one capability to the same data analysis agent:

| Step | Problem without it | What you add |
|------|-------------------|--------------|
| Minimal agent | — | Baseline loop: model + tools, no harness |
| Sandbox + filesystem | Agent cannot read CSVs or run Python | Isolated [backend](/oss/deepagents/backends) + file and execute tools |
| Summarization | Long sessions hit context limits | Automatic history compression |
| Skills | Domain rules bloat the system prompt | On-demand expertise via [progressive disclosure](/oss/langchain/multi-agent/skills-sql-assistant) |
| Subagent | Chart iteration crowds the main thread | Isolated worker + parallel delegation |

## Setup

**Install packages**

Install the packages for this tutorial:

```bash
pip install deepagents langsmith
```

**Set up LangSmith API keys**

This tutorial uses `LangSmithSandbox`, which provisions sandboxes through `SandboxClient`. That client authenticates with LangSmith using `LANGSMITH_API_KEY` from your environment, so an API key is required to run the tutorial. Setting up LangSmith also allows you to see traces of what happens when your agent runs.

1. [Sign up for a free account](https://smith.langchain.com). You can use Google, GitHub, or email.
2. [Create an API key](/langsmith/create-account-api-key) in **Settings > API Keys**.
3. Export the LangSmith API key:

```bash
export LANGSMITH_API_KEY=...
```

4. Enable tracing to inspect tool calls, middleware steps, and subagent delegation as you add each piece:

```bash
export LANGSMITH_TRACING=true
```

**Add a model provider API key**

Export the API key for the model provider you use in the code samples:

```bash Google
export GOOGLE_API_KEY=...
```

```bash OpenAI
export OPENAI_API_KEY=...
```

```bash Anthropic
export ANTHROPIC_API_KEY=...
```

```bash OpenRouter
export OPENROUTER_API_KEY=...
```

```bash Fireworks
export FIREWORKS_API_KEY=...
```

```bash Baseten
export BASETEN_API_KEY=...
```

```bash Ollama
# Local: Ollama must be running on your machine
# Cloud: Set your Ollama API key for hosted inference
export OLLAMA_API_KEY=...
```

## Build the agent

## Create the minimal agent

A data analysis agent needs more than a chat loop, but to begin with, start with the baseline: only a model and a loop.

Use `create_agent` and specify the model that you want to use:

```python Google
from langchain.agents import create_agent

agent = create_agent(model="google_genai:gemini-3.6-flash", tools=[])
```

```python OpenAI
from langchain.agents import create_agent

agent = create_agent(model="openai:gpt-5.5", tools=[])
```

```python Anthropic
from langchain.agents import create_agent

agent = create_agent(model="anthropic:claude-sonnet-5", tools=[])
```

```python OpenRouter
from langchain.agents import create_agent

agent = create_agent(model="openrouter:z-ai/glm-5.2", tools=[])
```

```python Fireworks
from langchain.agents import create_agent

agent = create_agent(model="fireworks:accounts/fireworks/models/glm-5p2", tools=[])
```

```python Baseten
from langchain.agents import create_agent

agent = create_agent(model="baseten:zai-org/GLM-5.2", tools=[])
```

```python Ollama
from langchain.agents import create_agent

agent = create_agent(model="ollama:north-mini-code-1.0", tools=[])
```

This runs, but the agent has no filesystem and no way to execute code. If you ask it to analyze a CSV, it can only guess from the prompt. The next steps add real file access and code execution.

## Add a sandbox backend

To analyze data efficiently, the agent needs to run code on files. This requires two things:

- An isolated [sandbox](/oss/deepagents/sandboxes) where the agent can place files and run code on the files without giving the agent access to your host machine.

- A [backend](/oss/deepagents/backends) which provides the file system tools to work with the sandbox (`read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`) using the `FilesystemMiddleware`:**. Because the `LangSmithSandbox` backend implements the sandbox protocol, `FilesystemMiddleware` also adds the `execute` tool, which allows the agent to run shell commands.

`LangSmithSandbox` is where files live and commands run. `FilesystemMiddleware` is what exposes that environment to the model as tools. The same middleware works with other backends if you swap the backend later.

`LangSmithSandbox` gives the agent an isolated environment with a filesystem and an `execute` tool for running shell commands. With it, the agent can install packages, write scripts, and run them without touching the host. To boot from a custom image instead of the default runtime, pass `snapshot_name` or `snapshot_id` to `create_sandbox()`; see [Sandbox snapshots](/langsmith/sandbox-snapshots).

Replace the agent from the previous step with one that includes `FilesystemMiddleware`:

```python Google
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python OpenAI
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python Anthropic
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python OpenRouter
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python Fireworks
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python Baseten
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python Ollama
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

The sandbox filesystem is separate from your laptop. You must upload the files you need to it before you invoke the agent:

```python
import csv
import io

rows = [
    ["Date", "Product", "Units", "Revenue"],
    ["2025-08-01", "Widget A", 10, 250],
    ["2025-08-02", "Widget B", 5, 125],
    ["2025-08-03", "Widget A", 7, 175],
    ["2025-08-04", "Widget C", 3, 90],
]
buf = io.StringIO()
csv.writer(buf).writerows(rows)
backend.upload_files([("/sales.csv", buf.getvalue().encode())])

upload_stream = agent.stream_events(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Read /sales.csv and summarize total revenue by product in one "
                    "sentence. Do not run shell commands."
                ),
            }
        ]
    },
    version="v3",
    config={"recursion_limit": 8},
)
for item in upload_stream.messages:
    print(item.text)
upload_stream.output
```

**Note:**

With `LangSmithSandbox`, upload paths must be absolute POSIX paths (for example, `/sales.csv`). Relative paths such as `sales.csv` are rejected with `invalid_path` and the file is not written to the sandbox.

Combine the code from the previous steps into one script and run it:

```bash
python analyze_sales.py
```

On the first run, LangSmith provisions a sandbox (this can take a few seconds). The script uploads `sales.csv`, streams the agent run, and prints assistant messages as they arrive. You should see an analysis of the sample sales data: product-level revenue, which widgets sold most, and brief trend notes. Exact wording varies by model run.

Open the run in [LangSmith](https://smith.langchain.com/) and watch the agent use filesystem tools (`read_file`, and `execute` if it runs Python in the sandbox) before it replies.

## Add context management

After step 2, every tool result stays in the message history. A real analysis session (multiple plots, failed scripts, large `read_file` output) fills the context window quickly.

`SummarizationMiddleware` compresses older turns when history grows too large, so the agent keeps working without you manually trimming messages. This matters less on the first `sales.csv` question and more on follow-ups such as "Now segment by product and plot monthly trends."

Update your agent from step 2 by adding `SummarizationMiddleware` to the middleware list:

```python Google
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "google_genai:gemini-3.6-flash"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python OpenAI
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "openai:gpt-5.5"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python Anthropic
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "anthropic:claude-sonnet-5"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python OpenRouter
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "openrouter:z-ai/glm-5.2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python Fireworks
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "fireworks:accounts/fireworks/models/glm-5p2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python Baseten
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "baseten:zai-org/GLM-5.2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python Ollama
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "ollama:north-mini-code-1.0"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

Run a multi-turn session to see summarization in action. After the initial analysis, ask follow-up questions that trigger more file reads or script runs. In LangSmith, look for a summarization step before later model calls. For more information, [Context engineering](/oss/langchain/context-engineering).

## Add skills

[Skills](/oss/langchain/multi-agent/skills-sql-assistant) provide a way to give an agent on-demand domain knowledge when needed using progressive disclosure. Skills can include multi-step workflows, rules, and conventions. By placing this information in a skill, it isn't added to the system prompt by default which ensures the tokens are only used when the information from the skill is needed for a task.

When the agent starts, it sees only lightweight metadata about each skill. When a task needs a skill, the agent loads the full skill file on demand.

Create a skill file in a skills directory:

```
skills/
  pandas-patterns/
    SKILL.md
```

```markdown
---
name: pandas-patterns
description: Common pandas and matplotlib patterns for data analysis and visualization
---

## Data loading
Use `pd.read_csv()` for CSV files. Always check `df.info()` and `df.describe()` first.

## Visualization
Use `matplotlib` for bar charts, `seaborn` for statistical plots.
Save figures with `plt.savefig("output.png", dpi=150, bbox_inches="tight")`.

## Reporting
Write a markdown summary to `report.md` alongside any generated charts.
```

This skill contains information on how the visualization should be done.

With `LangSmithSandbox`, skill paths resolve on the sandbox filesystem, not your local machine. Upload your local `skills/` directory before configuring `SkillsMiddleware`:

```python
from pathlib import Path

skills_dir = (Path(__file__).resolve().parent / "skills").resolve()
skill_files: list[tuple[str, bytes]] = []
for path in sorted(skills_dir.rglob("*")):
    if not path.is_file():
        continue
    rel = path.resolve().relative_to(skills_dir)
    skill_files.append((f"/skills/{rel.as_posix()}", path.read_bytes()))
backend.upload_files(skill_files)
```

Then create your agent with your skills by adding `SkillsMiddleware`:

```python Google
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "google_genai:gemini-3.6-flash"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python OpenAI
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "openai:gpt-5.5"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python Anthropic
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "anthropic:claude-sonnet-5"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python OpenRouter
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "openrouter:z-ai/glm-5.2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python Fireworks
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "fireworks:accounts/fireworks/models/glm-5p2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python Baseten
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "baseten:zai-org/GLM-5.2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python Ollama
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "ollama:north-mini-code-1.0"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

You can try a prompt such as "Analyze sales.csv using our pandas patterns." The agent will load the skill when it needs plotting or reporting guidance. If you ask a different question that does not need the skill, the agent will not load it.

## Add a visualization subagent

Some tasks produce large intermediate output (script drafts, failed runs, file reads) that would crowd the main agent's context if kept in one thread. A [subagent](/oss/deepagents/subagents) runs in its own context window so the supervisor sees only the final result, not every tool call along the way. That keeps the main analysis focused and leaves room for follow-up questions.

One example where using a subagent makes sense is chart generation. Plotting often means iterating on Python scripts, installing packages, and reading error output before a figure is ready. The following `visualizer` subagent can handle that work in isolation while the main agent continues planning and analysis. With `TodoListMiddleware`, the main agent can also delegate that chart work in parallel instead of blocking on each plot.

Update your agent from step 4 by adding `TodoListMiddleware` and `SubAgentMiddleware`:

```python Google
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "google_genai:gemini-3.6-flash"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python OpenAI
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "openai:gpt-5.5"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python Anthropic
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "anthropic:claude-sonnet-5"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python OpenRouter
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "openrouter:z-ai/glm-5.2"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python Fireworks
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "fireworks:accounts/fireworks/models/glm-5p2"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python Baseten
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "baseten:zai-org/GLM-5.2"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python Ollama
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "ollama:north-mini-code-1.0"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

Try a prompt such as "Analyze sales.csv, then create a bar chart of revenue by product." The main agent handles analysis and planning and delegates chart generation to the `visualizer` subagent via the `task` tool.

If you enabled tracing in [Setup](#setup), open the run in [LangSmith](https://smith.langchain.com/). You should see a `task` call to `visualizer`, a separate sub-run with its own tool loop, and a short result returned to the supervisor.

## What you built

You've built a customized agent with the following middleware:

| Middleware | What it adds |
|---|---|
| `FilesystemMiddleware` + `LangSmithSandbox` | Isolated filesystem + `execute` tool |
| `SummarizationMiddleware` | Automatic context compression |
| `SkillsMiddleware` | Domain knowledge loaded on demand |
| `TodoListMiddleware` + `SubAgentMiddleware` | Parallel visualization subagent |

This is the same foundation as `create_deep_agent`: assembled manually so you control exactly what's included.

The possibilities don't end here: see [Prebuilt middleware](/oss/langchain/middleware/built-in) for the full list of composable capabilities, and the `create_agent` reference for all configuration options.

To work with the pre-assembled version, see [Customize Deep Agents](/oss/deepagents/customization). For the full data analysis example using `create_deep_agent`, see [Data analysis](/oss/deepagents/data-analysis).

---

# Deployment
> 출처: data/raw/langchain/deploy.mdx | https://docs.langchain.com/oss/python/langchain/deploy

Deploy LangChain agents to production with LangSmith Cloud or JavaScript frameworks and hosting platforms.

When you are ready to deploy your LangChain agent to production, choose a hosting model that fits your stack. **[LangSmith Cloud](/langsmith/deploy-to-cloud)** provides fully managed infrastructure for stateful, long-running agents with persistent state and background execution.

**Tip:**

LangSmith offers multiple deployment options beyond Cloud, including [hybrid](/langsmith/hybrid), [standalone servers](/langsmith/deploy-standalone-server), and [self-hosted with control plane](/langsmith/deploy-with-control-plane). For more information, see the [LangSmith Deployment overview](/langsmith/deployment).

## LangSmith Cloud

This section walks through deploying your agent to LangSmith Cloud from a GitHub repository. LangSmith handles infrastructure, scaling, and operational concerns.

### Prerequisites

Before you begin, ensure you have the following:

- A [GitHub account](https://github.com/)
- A [LangSmith account](https://smith.langchain.com) (free to sign up)

### Deploy your agent

#### 1. Create a repository on GitHub

Your application's code must reside in a GitHub repository to be deployed on LangSmith. Both public and private repositories are supported. For this quickstart, first make sure your app is LangGraph-compatible by following the [local server setup guide](/oss/langchain/studio). Then, push your code to the repository.

#### 2. Deploy to LangSmith

**Navigate to LangSmith Deployment**

Log in to [LangSmith](https://smith.langchain.com). In the left sidebar, select **Deployments**.

**Create new deployment**

Click the **+ New Deployment** button. A pane will open where you can fill in the required fields.

**Link repository**

If you are a first time user or adding a private repository that has not been previously connected, click the **Add new account** button and follow the instructions to connect your GitHub account.

**Deploy repository**

Select your application's repository. Click **Submit** to deploy. This may take about 15 minutes to complete. You can check the status in the **Deployment details** view.

#### 3. Test your application in Studio

Once your application is deployed:

1. Select the deployment you just created to view more details.
2. Click the **Studio** button in the top right corner. Studio will open to display your graph.

#### 4. Get the API URL for your deployment

1. In the **Deployment details** view in LangGraph, click the **API URL** to copy it to your clipboard.
2. Click the `URL` to copy it to the clipboard.

#### 5. Test the API

You can now test the API:

**Python**

1. Install LangGraph Python:

```bash pip
pip install -U langgraph-sdk
```

```bash uv
uv add langgraph-sdk
```

2. Send a message to the agent:
```python
from langgraph_sdk import get_sync_client # or get_client for async

client = get_sync_client(url="your-deployment-url", api_key="your-langsmith-api-key")

for chunk in client.runs.stream(
    None,    # Threadless run
    "agent", # Name of agent. Defined in langgraph.json.
    input={
        "messages": [{
            "role": "human",
            "content": "What is LangGraph?",
        }],
    },
    stream_mode="updates",
):
    print(f"Receiving new event of type: {chunk.event}...")
    print(chunk.data)
    print("\n\n")
```

**Rest API**

```bash
curl -s --request POST \
    --url <DEPLOYMENT_URL>/runs/stream \
    --header 'Content-Type: application/json' \
    --header "X-Api-Key: <LANGSMITH API KEY> \
    --data "{
        \"assistant_id\": \"agent\", `# Name of agent. Defined in langgraph.json.`
        \"input\": {
            \"messages\": [
                {
                    \"role\": \"human\",
                    \"content\": \"What is LangGraph?\"
                }
            ]
        },
        \"stream_mode\": \"updates\"
    }"
```

**Tip:**

LangSmith offers additional hosting options, including self-hosted and hybrid. For more information, please see the [Platform setup overview](/langsmith/platform-setup).

---

# INVALID_PROMPT_INPUT
> 출처: data/raw/langchain/errors/INVALID_PROMPT_INPUT.mdx | https://docs.langchain.com/oss/python/langchain/errors/INVALID_PROMPT_INPUT

Occurs when a [prompt template](https://github.com/langchain-ai/langchain/blob/v0.3/docs/docs/concepts/prompt_templates.mdx) received missing or invalid input variables.

## Troubleshooting

To resolve this error, you can:

1. Review your prompt template for correctness. When using f-string formats, ensure proper escaping of curly braces:
   * Use `{{` for single braces in f-strings
   * Use `{{{{` for double braces in f-strings
2. When using `MessagesPlaceholder` components, confirm you're passing message arrays or message-like objects. If using shorthand tuples, wrap variable names in curly braces like `["placeholder", "{messages}"]`
3. Debug by examining actual inputs to your prompt template by using [LangSmith](/langsmith/observability) or logging to verify they match expectations
4. If sourcing prompts from LangChain [Prompt Hub](https://smith.langchain.com/prompts), isolate and test the prompt with sample inputs to ensure it functions as intended

---

# INVALID_TOOL_RESULTS
> 출처: data/raw/langchain/errors/INVALID_TOOL_RESULTS.mdx | https://docs.langchain.com/oss/python/langchain/errors/INVALID_TOOL_RESULTS

**Note:**

Currently only used in `langchainjs` (JavaScript/TypeScript).

This error occurs when passing mismatched, insufficient, or excessive `ToolMessage` objects to a model during tool calling operations.

The error stems from a fundamental requirement: an assistant message with `tool_calls` must be followed by tool messages responding to each `tool_call_id`.

When a model returns an `AIMessage` with tool calls, you must provide exactly one corresponding `ToolMessage` for each tool call, with matching `tool_call_id` values.

## Common causes

* **Insufficient responses**: If a model requests two tool executions but you only provide one response message, the model rejects the incomplete message chain
* **Duplicate responses**: Providing multiple `ToolMessage` objects for the same tool call ID results in rejection, as does having unmatched IDs
* **Orphaned tool messages**: Sending a `ToolMessage` without a preceding `AIMessage` containing tool calls violates protocol requirements

Here's an example of a problematic pattern:

```python
# Model requests two tool calls
response_message.tool_calls  # Returns 2 calls

# But only one ToolMessage provided
chat_history.append(ToolMessage(
    content=str(tool_response),
    tool_call_id=tool_call.get("id")
))

model_with_tools.invoke(chat_history)
```

## Troubleshooting

To resolve this error:

* **Count matching pairs**: Ensure one `ToolMessage` exists per tool call in the preceding `AIMessage`
* **Verify IDs**: Confirm each `ToolMessage.tool_call_id` matches an actual tool call identifier

---

# MESSAGE_COERCION_FAILURE
> 출처: data/raw/langchain/errors/MESSAGE_COERCION_FAILURE.mdx | https://docs.langchain.com/oss/python/langchain/errors/MESSAGE_COERCION_FAILURE

This error occurs when message objects don't conform to the expected format.

## Accepted message formats

LangChain modules accept `MessageLikeRepresentation`, which is defined as:

```python
from typing import Union

from langchain_core.prompts.chat import (
    BaseChatPromptTemplate,
    BaseMessage,
    BaseMessagePromptTemplate,
)

MessageLikeRepresentation = Union[
    Union[BaseMessagePromptTemplate, BaseMessage, BaseChatPromptTemplate],
    tuple[
        Union[str, type],
        Union[str, list[dict], list[object]],
    ],
    str,
]
```

These include OpenAI style message objects (`{ role: "user", content: "Hello world!" }`), tuples, and plain strings (which are converted to `HumanMessage` objects).

If a module receives a value outside of one of these formats, you will receive an error:

```python
from langchain_anthropic import ChatAnthropic

uncoercible_message = {"role": "HumanMessage", "random_field": "random value"}

model = ChatAnthropic(model="claude-sonnet-4-6")

model.invoke([uncoercible_message])
```

```text
ValueError: Message dict must contain 'role' and 'content' keys, got {'role': 'HumanMessage', 'random_field': 'random value'}
```

## Troubleshooting

To resolve this error:

1. **Ensure proper format**: All inputs to chat models must be an array of LangChain message classes or a supported message-like format
2. Verify no unintended stringification or transformation occurs to your messages
3. Examine the error's stack trace and add logging statements to inspect message objects before they're passed to the model

---

# MODEL_AUTHENTICATION
> 출처: data/raw/langchain/errors/MODEL_AUTHENTICATION.mdx | https://docs.langchain.com/oss/python/langchain/errors/MODEL_AUTHENTICATION

**Note:**

Currently only used in `langchainjs` (JavaScript/TypeScript).

Your model provider is denying you access to their service.

This error typically occurs when there's an issue with your authentication credentials or API keys.

## Troubleshooting

* Confirm that your API key or authentication credentials are accurate and valid.
* If using environment-based authentication, verify:
    - The variable name is spelled correctly
    - The variable contains an assigned value
    - Third-party packages like `dotenv` haven't interfered with loading
* If using a proxy or non-standard endpoint, make sure that your custom provider does not expect an alternative authentication scheme.
* Bypass environment variable issues by passing credentials explicitly:

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(api_key="YOUR_KEY_HERE")
```

---

# MODEL_NOT_FOUND
> 출처: data/raw/langchain/errors/MODEL_NOT_FOUND.mdx | https://docs.langchain.com/oss/python/langchain/errors/MODEL_NOT_FOUND

**Note:**

Currently only used in `langchainjs` (JavaScript/TypeScript).

The model name you have specified is not acknowledged by your provider.

## Troubleshooting

To resolve this error:

1. **Verify the model identifier**: Double check the model string you are passing in. Ensure the spelling and format are correct
2. **Check proxy/wrapper configurations**: If you are using a proxy or other alternative host with a model wrapper, confirm that the permitted model names are not restricted or altered

The error typically stems from either a typo in the model name string itself or restrictions imposed by a proxy service or model wrapper between your code and the provider's API.

---

# MODEL_RATE_LIMIT
> 출처: data/raw/langchain/errors/MODEL_RATE_LIMIT.mdx | https://docs.langchain.com/oss/python/langchain/errors/MODEL_RATE_LIMIT

**Note:**

Currently only used in `langchainjs` (JavaScript/TypeScript).

You have hit the maximum number of requests that a model provider allows over a given time period and are being temporarily blocked.

This error occurs when you exceed the maximum number of requests permitted by your model provider within a specific timeframe, resulting in temporary blocking. The restriction is generally temporary and lifts after the limit resets.

## Troubleshooting

To resolve this error, you can:

1. **Implement Rate Limiting**: Deploy a rate limiter to regulate the frequency of requests sent to the model.
    See [rate limiting](/oss/langchain/models#rate-limiting) docs.
2. **Implement Response Caching**: Use model response caching to reduce redundant requests when incoming queries are repetitive.
3. **Use Multiple Providers**: Distribute requests across multiple providers if your application architecture supports this approach
4. **Contact Your Provider**: Reach out to your model provider requesting an increase to your rate limits

---

# OUTPUT_PARSING_FAILURE
> 출처: data/raw/langchain/errors/OUTPUT_PARSING_FAILURE.mdx | https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

An [output parser](https://reference.langchain.com/python/langchain-core/output_parsers) was unable to handle model output as expected.

**Note:**

Some prebuilt constructs like legacy LangChain agents and chains may use output parsers internally, so you may see this error even if you're not visibly instantiating and using an output parser.

## Troubleshooting

- Consider using tool calling or other structured output techniques if possible without an output parser to reliably output parseable values.
- Add more precise formatting instructions to your prompt.
- If you are using a smaller or less capable model, try using a more capable one.

---

# Event streaming
> 출처: data/raw/langchain/event-streaming.mdx | https://docs.langchain.com/oss/python/langchain/event-streaming

Stream real-time updates from LangChain agent runs

LangChain agents are built on LangGraph, so they support the same streaming stack with agent-focused projections for messages, tool calls, state, and custom updates.

For most application and frontend use cases, use **Event Streaming** through `stream_events(..., version="v3")`. Event Streaming returns a run object with typed projections, so each projection can be consumed independently instead of parsing stream-mode tuples.

```py
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
)

stream = agent.stream_events({
    "messages": [{"role": "user", "content": "What is the weather in SF?"}],
}, version="v3")

for message in stream.messages:
    for delta in message.text:
        print(delta, end="", flush=True)

final_state = stream.output
```

## What you can stream

| Projection | Use |
| ---------- | --- |
| `for event in stream` | Raw protocol events with full envelope and access to every channel. |
| `stream.messages` | Model message streams, one per LLM call. |
| `message.text` | Text deltas and final text for a message. |
| `message.reasoning` | Reasoning deltas for models that expose reasoning content. |
| `message.tool_calls` | Tool-call argument chunks and finalized tool calls. |
| `message.output` | Final message object after the model call completes. |
| `stream.values` | Agent state snapshots. |
| `stream.output` | Final agent state. |
| `stream.subgraphs` | Nested graph runs (sub-agents and plain subgraphs). |
| `stream.extensions` | Custom transformer projections. |
| `stream.tool_calls` | Tool execution lifecycle, inputs, output deltas, final output, and errors. |

`stream.messages` yields `ChatModelStream` objects. Each message stream exposes `.text`, `.reasoning`, `.tool_calls`, and `.output`. Sync projections are iterable for live deltas and drainable for final values: use `str(message.text)` for final text and `message.tool_calls.get()` for finalized tool calls.

## Agent messages

Use `stream.messages` when you want model output from each LLM call.

```py
stream = agent.stream_events(input, version="v3")

for message in stream.messages:
    print(f"[{message.node}] ", end="")
    for delta in message.text:
        print(delta, end="", flush=True)

    full_message = message.output
    usage = full_message.usage_metadata
    if usage:
        print(usage)
```

`message.output` gives you the finalized AI message, including provider-specific content blocks. In TypeScript, use `message.usage` when you only need token counts or other usage metadata; in Python, read usage from `message.output.usage_metadata`.

## Reasoning content

Reasoning content uses the same shape as text content, but it is available only when the selected model emits reasoning blocks.

```py
stream = agent.stream_events(input, version="v3")

for message in stream.messages:
    for delta in message.reasoning:
        print(f"[thinking] {delta}", end="", flush=True)

    for delta in message.text:
        print(delta, end="", flush=True)
```

See the [reasoning guide](/oss/langchain/models#reasoning) and your provider's integration page for model configuration details.

## Tool calls

There are two useful tool-call projections:

- `message.tool_calls` streams tool-call argument chunks while the model is producing the tool call.
- `stream.tool_calls` streams the lifecycle of tool execution after the tool call starts.

```py
stream = agent.stream_events(input, version="v3")

for message in stream.messages:
    for chunk in message.tool_calls:
        print(f"tool call chunk: {chunk}")

finalized = message.tool_calls.get()
if finalized:
    print(f"finalized tool calls: {finalized}")

for call in stream.tool_calls:
    print(f"{call.tool_name}({call.input})")
    for delta in call.output_deltas:
        print(delta, end="", flush=True)
    print(call.output, call.error)
```

## Streaming sub-agents

When a `create_agent` call invokes another named `create_agent` (via a wrapping tool, typically), the inner agent's events flow at a nested namespace. The `name=` you pass to `create_agent` identifies that inner agent in the stream, so you can filter and label per agent.

Named sub-agents surface on the dedicated `stream.subagents` projection. Each handle exposes the inner agent's own `.messages`, `.values`, `.tool_calls`, and `.output`, plus `.name` (the `name=` you passed) and `.cause` (the tool call that dispatched the sub-agent). Because only named `create_agent` runs appear here, you don't need to filter plain subgraphs out.

```py
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

weather_agent = create_agent(
    model=init_chat_model("openai:gpt-5.5"),
    tools=[get_weather],
    name="weather_agent",
)

def call_weather(query: str) -> str:
    """Query the weather agent."""
    result = weather_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].text

supervisor = create_agent(
    model=init_chat_model("openai:gpt-5.5"),
    tools=[call_weather],
    name="supervisor",
)

stream = supervisor.stream_events(
    {"messages": [{"role": "user", "content": "What's the weather in Boston?"}]},
    version="v3",
)

for subagent in stream.subagents:
    print(f"{subagent.name}: ", end="")
    for message in subagent.messages:
        for token in message.text:
            print(token, end="", flush=True)
    print()
```

Plain `StateGraph` subgraphs invoked from a tool also surface on `stream.subgraphs` — set `name=` on `.compile(name=...)` to get a label in `subagent.graph_name`.

`stream.subagents` is the focused view of named `create_agent` sub-agents, while `stream.subgraphs` covers every nested graph. Use whichever matches your UI.

## State and final output

Use `stream.values` for state snapshots and `stream.output` for the final agent state.

```py
stream = agent.stream_events(input, version="v3")

for snapshot in stream.values:
    print(snapshot)

final_state = stream.output
```

## Multiple projections

For concurrent consumption in async code, use `astream_events` with `asyncio.gather`:

```py
import asyncio

stream = await agent.astream_events(input, version="v3")

async def consume_messages():
    async for message in stream.messages:
        print(await message.text)

async def consume_tool_calls():
    async for call in stream.tool_calls:
        print(call.tool_name, call.input)

await asyncio.gather(consume_messages(), consume_tool_calls())
```

For synchronous code, use `stream.interleave(...)` instead:

```py
stream = agent.stream_events(input, version="v3")

for name, item in stream.interleave("messages", "tool_calls", "values"):
    if name == "messages":
        print(item.text)
    elif name == "tool_calls":
        print(item.tool_name, item.input)
    elif name == "values":
        print(item)
```

To access channels that aren't exposed as typed projections, or to inspect the full event envelope, iterate raw protocol events:

```py
for event in stream:
    print(event["method"], event["params"]["namespace"], event["params"]["data"])
```

## Custom updates

Use custom stream transformers when your application needs a projection that is not built in, such as retrieval progress, artifacts, or domain-specific events.

```py
stream = agent.stream_events(
    input,
    version="v3",
    transformers=[ToolActivityTransformer],
)

for activity in stream.extensions["tool_activity"]:
    print(activity)
```

### Register transformers on middleware

**Note:**

Middleware-registered transformers require `langchain>=1.3.2`.

Middleware can declare stream transformer factories alongside its hooks and tools. The factory shape differs between languages:

Set the `transformers` attribute on an `AgentMiddleware` subclass to a sequence of factories. Each factory has the shape `Callable[[tuple[str, ...]], StreamTransformer]` and is invoked as `factory(scope)`, where `scope` is the mini-mux scope tuple (`()` for the root mux, non-empty for subgraphs). Returning a fresh transformer per call keeps each subgraph isolated.

```py
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware

class ToolActivityMiddleware(AgentMiddleware):
    transformers = (ToolActivityTransformer,)

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
    middleware=[ToolActivityMiddleware()],
)
```

At compile time, `create_agent` merges middleware-registered factories with anything passed to its own `transformers=` argument. The final order on the compiled graph is:

1. The built-in `ToolCallTransformer`.
2. Middleware-registered factories, in middleware order.
3. Caller-supplied `transformers=` from `create_agent`.

This keeps the built-in tool-call projection in front of consumer transformers and gives caller-supplied entries the final word.

The built-in `PIIMiddleware` uses this hook to redact PII from streamed wire output. With `apply_to_output=True`, its registered transformer scrubs detected PII from text deltas, tool-call args, tool outputs, and state snapshots before they leave the run, closing the window where `after_model` state-level redaction would otherwise let raw PII through to live readers of `stream_events(version="v3")`.

```py
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

agent = create_agent(
    model="gpt-5-nano",
    tools=[],
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_output=True),
    ],
)
```

See [PII detection](/oss/langchain/middleware/built-in#pii-detection) for the full configuration surface.

See [Build your own projection](/oss/langgraph/event-streaming#build-your-own-projection) for the transformer contract.

## Related

- [Streaming](/oss/langchain/streaming) covers low-level Pregel stream modes.
- [Build your own projection](/oss/langgraph/event-streaming#build-your-own-projection) covers writing application-specific projections.
- [Frontend streaming patterns](/oss/langchain/frontend/overview) shows UI use cases built on streamed state.

---

# Get help
> 출처: data/raw/langchain/get-help.mdx | https://docs.langchain.com/oss/python/langchain/get-help

Connect with the LangChain community, access learning resources, and get the support you need to build with confidence.

## Learning resources

Start your journey or deepen your knowledge with our comprehensive learning materials.

- **[Chat LangChain](https://chat.langchain.com/)**: Ask the docs anything about LangChain, powered by real-time docs
- **[API Reference](https://reference.langchain.com/python/)**: Complete documentation for all LangChain packages

## Community support

Get help from fellow developers and the LangChain team through our active community channels.

- **[Community Forum](https://forum.langchain.com/)**: Ask questions, share solutions, and discuss best practices
- **[Community Slack](https://www.langchain.com/join-community)**: Connect with other builders and get quick help

## Professional support

For enterprise needs and critical applications, access dedicated support channels.

- **[Support portal](https://support.langchain.com/)**: Submit tickets and track support requests
- **[LangSmith status](https://global.status.smith.langchain.com/gcp-us)**: Real-time status of LangSmith services and APIs

## Contribute

Help us improve LangChain for everyone. Whether you're fixing bugs, adding features, or improving documentation, we welcome your contributions.

- **[Contributing Guide](/oss/contributing/overview)**: Everything you need to know about contributing to LangChain

## Stay connected

Follow us for the latest updates, announcements, and community highlights.

- **[X (Twitter)](https://x.com/langchain)**: Daily updates and community spotlights
- **[LinkedIn](https://www.linkedin.com/company/langchain/)**: Professional network and company updates

---

# Guardrails
> 출처: data/raw/langchain/guardrails.mdx | https://docs.langchain.com/oss/python/langchain/guardrails

Implement safety checks and content filtering for your agents

Guardrails help you build safe, compliant AI applications by validating and filtering content at key points in your agent's execution. They can detect sensitive information, enforce content policies, validate outputs, and prevent unsafe behaviors before they cause problems.

Common use cases include:
- Preventing PII leakage
- Detecting and blocking prompt injection attacks
- Blocking inappropriate or harmful content
- Enforcing business rules and compliance requirements
- Validating output quality and accuracy

You can implement guardrails using [middleware](/oss/langchain/middleware) to intercept execution at strategic points - before the agent starts, after it completes, or around model and tool calls.

Guardrails can be implemented using two complementary approaches:

- **Deterministic guardrails**

        Use rule-based logic like regex patterns, keyword matching, or explicit checks. Fast, predictable, and cost-effective, but may miss nuanced violations.

- **Model-based guardrails**

        Use LLMs or classifiers to evaluate content with semantic understanding. Catch subtle issues that rules miss, but are slower and more expensive.

LangChain provides both built-in guardrails (e.g., [PII detection](#pii-detection), [human-in-the-loop](#human-in-the-loop)) and a flexible middleware system for building custom guardrails using either approach.

## Built-in guardrails

### PII detection

LangChain provides built-in middleware for detecting and handling Personally Identifiable Information (PII) in conversations. This middleware can detect common PII types like emails, credit cards, IP addresses, and more.

PII detection middleware is helpful for cases such as health care and financial applications with compliance requirements, customer service agents that need to sanitize logs, and generally any application handling sensitive user data.

The PII middleware supports multiple strategies for handling detected PII:

| Strategy | Description | Example |
|----------|-------------|---------|
| `redact` | Replace with `[REDACTED_{PII_TYPE}]` | `[REDACTED_EMAIL]` |
| `mask` | Partially obscure (e.g., last 4 digits) | `****-****-****-1234` |
| `hash` | Replace with deterministic hash | `a8f5f167...` |
| `block` | Raise exception when detected | Error thrown |

**Note:**

With `apply_to_output=True`, `PIIMiddleware` also redacts streamed wire output—text deltas, tool-call args, tool outputs, and state snapshots—via a registered stream transformer. Requires `langchain>=1.3.2`. See [Register transformers on middleware](/oss/langchain/event-streaming#register-transformers-on-middleware).

```python
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[customer_service_tool, email_tool],
    middleware=[
        # Redact emails in user input before sending to model
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True,
        ),
        # Mask credit cards in user input
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_input=True,
        ),
        # Block API keys - raise error if detected
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
            apply_to_input=True,
        ),
    ],
)

# When user provides PII, it will be handled according to the strategy
result = agent.invoke({
    "messages": [{"role": "user", "content": "My email is john.doe@example.com and card is 5105-1051-0510-5100"}]
})
```

**Built-in PII types and configuration**

**Built-in PII types:**
- `email` - Email addresses
- `credit_card` - Credit card numbers (Luhn validated)
- `ip` - IP addresses
- `mac_address` - MAC addresses
- `url` - URLs

**Configuration options:**

Parameter | Description | Default
-----------|-------------|---------
`pii_type` | Type of PII to detect (built-in or custom) | Required
`strategy` | How to handle detected PII (`"block"`, `"redact"`, `"mask"`, `"hash"`) | `"redact"`
`detector` | Custom detector function or regex pattern | `None` (uses built-in)
`apply_to_input` | Check user messages before model call | `True`
`apply_to_output` | Check AI messages after model call | `False`
`apply_to_tool_results` | Check tool result messages after execution | `False`

See the [middleware documentation](/oss/langchain/middleware#pii-detection) for complete details on PII detection capabilities.

### Human-in-the-loop

LangChain provides built-in middleware for requiring human approval before executing sensitive operations. This is one of the most effective guardrails for high-stakes decisions.

Human-in-the-loop middleware is helpful for cases such as financial transactions and transfers, deleting or modifying production data, sending communications to external parties, and any operation with significant business impact.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, send_email_tool, delete_database_tool],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                # Require approval for sensitive operations
                "send_email": True,
                "delete_database": True,
                # Auto-approve safe operations
                "search": False,
            }
        ),
    ],
    # Persist the state across interrupts
    checkpointer=InMemorySaver(),
)

# Human-in-the-loop requires a thread ID for persistence
config = {"configurable": {"thread_id": "some_id"}}

# Agent will pause and wait for approval before executing sensitive tools
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Send an email to the team"}]},
    config=config
)

result = agent.invoke(
    Command(resume={"decisions": [{"type": "approve"}]}),
    config=config  # Same thread ID to resume the paused conversation
)
```

**Tip:**

See the [human-in-the-loop documentation](/oss/langchain/human-in-the-loop) for complete details on implementing approval workflows.

## Custom guardrails

For more sophisticated guardrails, you can create custom middleware that runs before or after the agent executes. This gives you full control over validation logic, content filtering, and safety checks.

### Before agent guardrails

Use "before agent" hooks to validate requests once at the start of each invocation. This is useful for session-level checks like authentication, rate limiting, or blocking inappropriate requests before any processing begins.

```python title="Class syntax"
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime

class ContentFilterMiddleware(AgentMiddleware):
    """Deterministic guardrail: Block requests containing banned keywords."""

def __init__(self, banned_keywords: list[str]):
    super().__init__()
    self.banned_keywords = [kw.lower() for kw in banned_keywords]

@hook_config(can_jump_to=["end"])
def before_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    # Get the first user message
    if not state["messages"]:
        return None

first_message = state["messages"][0]
if first_message.type != "human":
    return None

content = first_message.content.lower()

# Check for banned keywords
for keyword in self.banned_keywords:
    if keyword in content:
        # Block execution before any processing
        return {
            "messages": [{
                "role": "assistant",
                "content": "I cannot process requests containing inappropriate content. Please rephrase your request."
            }],
            "jump_to": "end"
        }

return None

# Use the custom guardrail
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, calculator_tool],
    middleware=[
        ContentFilterMiddleware(
            banned_keywords=["hack", "exploit", "malware"]
        ),
    ],
)

# This request will be blocked before any processing
result = agent.invoke({
    "messages": [{"role": "user", "content": "How do I hack into a database?"}]
})
```

```python title="Decorator syntax"
from typing import Any

from langchain.agents.middleware import before_agent, AgentState, hook_config
from langgraph.runtime import Runtime

banned_keywords = ["hack", "exploit", "malware"]

@before_agent(can_jump_to=["end"])
def content_filter(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Deterministic guardrail: Block requests containing banned keywords."""
    # Get the first user message
    if not state["messages"]:
        return None

first_message = state["messages"][0]
if first_message.type != "human":
    return None

content = first_message.content.lower()

# Check for banned keywords
for keyword in banned_keywords:
    if keyword in content:
        # Block execution before any processing
        return {
            "messages": [{
                "role": "assistant",
                "content": "I cannot process requests containing inappropriate content. Please rephrase your request."
            }],
            "jump_to": "end"
        }

return None

# Use the custom guardrail
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, calculator_tool],
    middleware=[content_filter],
)

# This request will be blocked before any processing
result = agent.invoke({
    "messages": [{"role": "user", "content": "How do I hack into a database?"}]
})
```

### After agent guardrails

Use "after agent" hooks to validate final outputs once before returning to the user. This is useful for model-based safety checks, quality validation, or final compliance scans on the complete agent response.

```python title="Class syntax"
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime
from langchain.messages import AIMessage
from langchain.chat_models import init_chat_model
from typing import Any

class SafetyGuardrailMiddleware(AgentMiddleware):
    """Model-based guardrail: Use an LLM to evaluate response safety."""

def __init__(self):
    super().__init__()
    self.safety_model = init_chat_model("gpt-5.4-mini")

@hook_config(can_jump_to=["end"])
def after_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    # Get the final AI response
    if not state["messages"]:
        return None

last_message = state["messages"][-1]
if not isinstance(last_message, AIMessage):
    return None

# Use a model to evaluate safety
safety_prompt = f"""Evaluate if this response is safe and appropriate.
Respond with only 'SAFE' or 'UNSAFE'.

Response: {last_message.content}"""

result = self.safety_model.invoke([{"role": "user", "content": safety_prompt}])

if "UNSAFE" in result.content:
    last_message.content = "I cannot provide that response. Please rephrase your request."

return None

# Use the safety guardrail
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, calculator_tool],
    middleware=[SafetyGuardrailMiddleware()],
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "How do I make explosives?"}]
})
```

```python title="Decorator syntax"
from langchain.agents.middleware import after_agent, AgentState, hook_config
from langgraph.runtime import Runtime
from langchain.messages import AIMessage
from langchain.chat_models import init_chat_model
from typing import Any

safety_model = init_chat_model("gpt-5.4-mini")

@after_agent(can_jump_to=["end"])
def safety_guardrail(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Model-based guardrail: Use an LLM to evaluate response safety."""
    # Get the final AI response
    if not state["messages"]:
        return None

last_message = state["messages"][-1]
if not isinstance(last_message, AIMessage):
    return None

# Use a model to evaluate safety
safety_prompt = f"""Evaluate if this response is safe and appropriate.
Respond with only 'SAFE' or 'UNSAFE'.

Response: {last_message.content}"""

result = safety_model.invoke([{"role": "user", "content": safety_prompt}])

if "UNSAFE" in result.content:
    last_message.content = "I cannot provide that response. Please rephrase your request."

return None

# Use the safety guardrail
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, calculator_tool],
    middleware=[safety_guardrail],
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "How do I make explosives?"}]
})
```

### Combine multiple guardrails

You can stack multiple guardrails by adding them to the middleware array. They execute in order, allowing you to build layered protection:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware, HumanInTheLoopMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, send_email_tool],
    middleware=[
        # Layer 1: Deterministic input filter (before agent)
        ContentFilterMiddleware(banned_keywords=["hack", "exploit"]),

# Layer 2: PII protection (before and after model)
PIIMiddleware("email", strategy="redact", apply_to_input=True),
PIIMiddleware("email", strategy="redact", apply_to_output=True),

# Layer 3: Human approval for sensitive tools
HumanInTheLoopMiddleware(interrupt_on={"send_email": True}),

        # Layer 4: Model-based safety check (after agent)
        SafetyGuardrailMiddleware(),
    ],
)
```

## Additional resources

- [Middleware documentation](/oss/langchain/middleware) - Complete guide to custom middleware
- [Middleware API reference](https://reference.langchain.com/python/langchain/middleware/) - Complete guide to custom middleware
- [Human-in-the-loop](/oss/langchain/human-in-the-loop) - Add human review for sensitive operations
- [Testing agents](/oss/langchain/test/) - Strategies for testing safety mechanisms

---

# Human-in-the-loop
> 출처: data/raw/langchain/human-in-the-loop.mdx | https://docs.langchain.com/oss/python/langchain/human-in-the-loop

The Human-in-the-Loop (HITL) [middleware](/oss/langchain/middleware/built-in#human-in-the-loop) lets you add human oversight to agent tool calls.
When a model proposes an action that might require review—for example, writing to a file or executing SQL—the middleware can pause execution and wait for a decision.

It does this by checking each tool call against a configurable policy. If intervention is needed, the middleware issues an interrupt that halts execution. The graph state is saved using LangGraph's [persistence layer](/oss/langgraph/persistence), so execution can pause safely and resume later.

A human decision then determines what happens next: the action can be approved as-is (`approve`), modified before running (`edit`), rejected with feedback (`reject`), or responded to directly (`respond`) for "ask user" style tools.

## Interrupt decision types

The [middleware](/oss/langchain/middleware/built-in#human-in-the-loop) defines four built-in ways a human can respond to an interrupt:

| Decision Type | Description                                                               | Example Use Case                                    |
|---------------|---------------------------------------------------------------------------|-----------------------------------------------------|
| ✅ `approve`   | Execute the tool with the original arguments as proposed by the agent.    | Send an email draft exactly as written              |
| ✏️ `edit`     | Modify the tool arguments before execution.                               | Change the recipient before sending an email        |
| ❌ `reject`    | Skip executing this tool call entirely and return rejection feedback to the agent. | Deny file deletion and explain why         |
| 💬 `respond`  | Return the human's message directly as a synthetic tool result, skipping execution, for "ask user" style tools. | Answer an `"ask_user"` prompt with a direct reply |

The available decision types for each tool depend on the policy you configure in `interrupt_on`.
When multiple tool calls are paused at the same time, each action requires a separate decision.
Decisions must be provided in the same order as the actions appear in the interrupt request.

Use `reject` when the human is denying the requested action. Use `respond` only when the human is acting as the tool, such as answering an `ask_user` prompt. Do not use `respond` to deny side-effecting tools, because its message is treated as a successful tool result.

**Tip:**

When **editing** tool arguments, make changes conservatively. Significant modifications to the original arguments may cause the model to re-evaluate its approach and potentially execute the tool multiple times or take unexpected actions.

## Configuring interrupts

To use HITL, add the [middleware](/oss/langchain/middleware/built-in#human-in-the-loop) to the agent's `middleware` list when creating the agent.

You configure it with a mapping of tool actions to the decision types that are allowed for each action. The middleware will interrupt execution when a tool call matches an action in the mapping.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware # [!code highlight]
from langgraph.checkpoint.memory import InMemorySaver # [!code highlight]

agent = create_agent(
    model="gpt-5.5",
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware( # [!code highlight]
            interrupt_on={
                "write_file": True,  # All decisions (approve, edit, reject, respond) allowed
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},  # No editing allowed
                "read_data": False, # Safe operation, no approval needed
            },
            # Prefix for interrupt messages - combined with tool name and args to form the full message
            # e.g., "Tool execution pending approval: execute_sql with query='DELETE FROM...'"
            # Individual tools can override this by specifying a "description" in their interrupt config
            description_prefix="Tool execution pending approval",
        ),
    ],
    # Human-in-the-loop requires checkpointing to handle interrupts.
    # In production, use a persistent checkpointer like AsyncPostgresSaver or MongoDBSaver.
    checkpointer=InMemorySaver(),  # [!code highlight]
)
```

**Info:**

You must configure a checkpointer to persist the graph state across interrupts.
In production, use a persistent checkpointer like `AsyncPostgresSaver` or [`MongoDBSaver`](https://pypi.org/project/langgraph-checkpoint-mongodb/). For testing or prototyping, use `InMemorySaver`.

When invoking the agent, pass a `config` that includes the **thread ID** to associate execution with a conversation thread.
See the [LangGraph interrupts documentation](/oss/langgraph/interrupts) for details.

**Configuration options**

Mapping of tool names to approval configs. Values can be `True` (interrupt with default config), `False` (auto-approve), or an `InterruptOnConfig` object.

Prefix for action request descriptions

**`InterruptOnConfig` options:**

List of allowed decisions: `'approve'`, `'edit'`, `'reject'`, or `'respond'`

Static string or callable function for custom description

Optional predicate that receives a ToolCallRequest and returns `True` to interrupt or `False` to auto-approve. Use it to gate interrupts on a call's arguments. Requires `langchain>=1.3.3`.

## Conditional interrupts

By default, every tool call listed in `interrupt_on` pauses for review. To pause only some calls, add a `when` predicate to a tool's `InterruptOnConfig`. The predicate receives a `ToolCallRequest` and returns `True` to interrupt or `False` to auto-approve, so you can gate on the tool's arguments.

**Note:**

Conditional interrupts require `langchain>=1.3.3`.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ToolCallRequest
from langgraph.checkpoint.memory import InMemorySaver

def writes_outside_workspace(request: ToolCallRequest) -> bool:
    """Pause writes to paths outside the workspace directory."""
    path = request.tool_call["args"].get("path", "")
    return not path.startswith("/workspace/")

def is_write_query(request: ToolCallRequest) -> bool:
    """Pause SQL that isn't a read-only SELECT."""
    query = request.tool_call["args"].get("query", "")
    return not query.lstrip().upper().startswith("SELECT")

agent = create_agent(
    model="gpt-5.5",
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "write_file": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                    "when": writes_outside_workspace,
                },
                "execute_sql": {
                    "allowed_decisions": ["approve", "reject"],
                    "when": is_write_query,
                },
            },
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

When the `when` predicate returns `False`, the call runs without interrupting. When it returns `True`, or when you omit `when`, the call pauses as usual. Calls that evaluate to `False` are never added to the interrupt batch, so a reviewer only sees the actions that need a decision.

## Responding to interrupts

When you invoke the agent, it runs until it either completes or an interrupt is raised. An interrupt is triggered when a tool call matches the policy you configured in `interrupt_on`. With `version="v2"`, the result is a `GraphOutput` with an `interrupts` attribute containing the actions that require review. You can then present those actions to a reviewer and resume execution once decisions are provided.

```python
from langgraph.types import Command

# Human-in-the-loop leverages LangGraph's persistence layer.
# You must provide a thread ID to associate the execution with a conversation thread,
# so the conversation can be paused and resumed (as is needed for human review).
config = {"configurable": {"thread_id": "some_id"}} # [!code highlight]
# Run the graph until the interrupt is hit.
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Delete old records from the database",
            }
        ]
    },
    config=config, # [!code highlight]
    version="v2", # [!code highlight]
)

# result is a GraphOutput with .value and .interrupts
print(result.interrupts)  # [!code highlight]
# > (
# >    Interrupt(
# >       value={
# >          'action_requests': [
# >             {
# >                'name': 'execute_sql',
# >                'arguments': {'query': 'DELETE FROM records WHERE created_at < NOW() - INTERVAL \'30 days\';'},
# >                'description': 'Tool execution pending approval\n\nTool: execute_sql\nArgs: {...}'
# >             }
# >          ],
# >          'review_configs': [
# >             {
# >                'action_name': 'execute_sql',
# >                'allowed_decisions': ['approve', 'reject']
# >             }
# >          ]
# >       }
# >    ),
# > )

# Resume with approval decision
agent.invoke(
    Command( # [!code highlight]
        resume={"decisions": [{"type": "approve"}]}  # or "reject" [!code highlight]
    ), # [!code highlight]
    config=config, # Same thread ID to resume the paused conversation
    version="v2",
)
```

### Decision types

**✅ approve**

Use `approve` to approve the tool call as-is and execute it without changes.

```python
agent.invoke(
    Command(
        # Decisions are provided as a list, one per action under review.
        # The order of decisions must match the order of actions
        # in the interrupt request.
        resume={
            "decisions": [
                {
                    "type": "approve",
                }
            ]
        }
    ),
    config=config,  # Same thread ID to resume the paused conversation
    version="v2",
)
```

**✏️ edit**

Use `edit` to modify the tool call before execution.
Provide the edited action with the new tool name and arguments.

```python
agent.invoke(
    Command(
        # Decisions are provided as a list, one per action under review.
        # The order of decisions must match the order of actions
        # in the interrupt request.
        resume={
            "decisions": [
                {
                    "type": "edit",
                    # Edited action with tool name and args
                    "edited_action": {
                        # Tool name to call.
                        # Will usually be the same as the original action.
                        "name": "new_tool_name",
                        # Arguments to pass to the tool.
                        "args": {"key1": "new_value", "key2": "original_value"},
                    }
                }
            ]
        }
    ),
    config=config,  # Same thread ID to resume the paused conversation
    version="v2",
)
```

**Tip:**

When **editing** tool arguments, make changes conservatively. Significant modifications to the original arguments may cause the model to re-evaluate its approach and potentially execute the tool multiple times or take unexpected actions.

**❌ reject**

Use `reject` to deny the tool call and provide feedback instead of execution. The tool is not executed.

```python
agent.invoke(
    Command(
        # Decisions are provided as a list, one per action under review.
        # The order of decisions must match the order of actions
        # in the interrupt request.
        resume={
            "decisions": [
                {
                    "type": "reject",
                    # Optional: explain why the action was rejected
                    # and whether the agent should retry a different approach.
                    "message": "User rejected this action. Do not retry this tool call.",
                }
            ]
        }
    ),
    config=config,  # Same thread ID to resume the paused conversation
    version="v2",
)
```

The `message` is added to the conversation as feedback to help the agent understand why the action was rejected and what it should do instead. When you omit `message`, the middleware uses a default rejection message that tells the model the tool was not executed and not to retry the same tool call unless the user asks. For side-effecting tools, provide a domain-specific message that is explicit about whether the agent should abandon the action, ask a follow-up question, or try a safer alternative.

**💬 respond**

Use `respond` for "ask user" style tools where the tool's real implementation is the human's reply. The `message` content is returned directly as the tool result; the tool itself is not executed.

```python
agent.invoke(
    Command(
        # Decisions are provided as a list, one per action under review.
        # The order of decisions must match the order of actions
        # in the interrupt request.
        resume={
            "decisions": [
                {
                    "type": "respond",
                    # The human's reply, returned directly as the tool result
                    "message": "Blue.",
                }
            ]
        }
    ),
    config=config,  # Same thread ID to resume the paused conversation
    version="v2",
)
```

The `message` is returned to the agent as a successful `ToolMessage`. Use `respond` when the tool is intentionally a placeholder for human input, for example, an `ask_user` tool that prompts for clarification. Do not use `respond` to deny a proposed action, because it tells the model that the tool completed successfully.

---

### Multiple decisions

When multiple actions are under review, provide a decision for each action in the same order as they appear in the interrupt:

```python
{
    "decisions": [
        {"type": "approve"},
        {
            "type": "edit",
            "edited_action": {
                "name": "tool_name",
                "args": {"param": "new_value"}
            }
        },
        {
            "type": "reject",
            "message": "This action is not allowed"
        }
    ]
}
```

## Streaming with human-in-the-loop

You can stream real-time updates while the agent runs and handles interrupts using `stream_events()`. Use `stream.messages` to stream LLM tokens and `stream.values` to check agent state snapshots for interrupts.

```python
from langgraph.types import Command

config = {"configurable": {"thread_id": "some_id"}}

# Stream agent progress and LLM tokens until interrupt
stream = agent.stream_events(
    {"messages": [{"role": "user", "content": "Delete old records from the database"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for message in stream.messages:  # [!code highlight]
    for token in message.text:  # [!code highlight]
        print(token, end="", flush=True)

# Check whether the run paused for human input
if stream.interrupted:  # [!code highlight]
    print(f"\n\nInterrupt: {stream.interrupts}")  # [!code highlight]

# Resume with streaming after human decision
stream = agent.stream_events(
    Command(resume={"decisions": [{"type": "approve"}]}),
    config=config,
    version="v3",  # [!code highlight]
)
for message in stream.messages:  # [!code highlight]
    for token in message.text:
        print(token, end="", flush=True)
```

See the [Streaming](/oss/langchain/streaming) guide for more details on stream modes.

## Execution lifecycle

The middleware defines an `after_model` hook that runs after the model generates a response but before any tool calls are executed:

1. The agent invokes the model to generate a response.
2. The middleware inspects the response for tool calls.
3. If any calls require human input, the middleware builds a HITLRequest with `action_requests` and `review_configs` and calls interrupt.
4. The agent waits for human decisions.
5. Based on the `HITLResponse` decisions, the middleware executes approved or edited calls, synthesizes ToolMessage's for rejected calls, returns human replies directly as ToolMessage's for `respond` decisions, and resumes execution.

## Custom HITL logic

For more specialized workflows, you can build custom HITL logic directly using the interrupt primitive and [middleware](/oss/langchain/middleware) abstraction.

Review the [execution lifecycle](#execution-lifecycle) above to understand how to integrate interrupts into the agent's operation.

---

# Install LangChain
> 출처: data/raw/langchain/install.mdx | https://docs.langchain.com/oss/python/langchain/install

Install the LangChain package and the independent provider packages for the models and integrations you use.

To install the LangChain package:

```bash pip
pip install -U langchain
# Requires Python 3.10+
```

```bash uv
uv add langchain
# Requires Python 3.10+
```

LangChain provides integrations to hundreds of LLMs and thousands of other integrations. These live in independent provider packages.

```bash pip
# Installing the OpenAI integration
pip install -U langchain-openai

# Installing the Anthropic integration
pip install -U langchain-anthropic
```
```bash uv
# Installing the OpenAI integration
uv add langchain-openai

# Installing the Anthropic integration
uv add langchain-anthropic
```

**Tip:**

See the [Integrations tab](/oss/integrations/providers/overview) for a full list of available integrations.

Now that you have LangChain installed, you can get started by following the [Quickstart guide](/oss/langchain/quickstart).

**Tip:**

Set up [LangSmith](https://smith.langchain.com) tracing to debug your first LangChain app. Follow the [tracing quickstart](/langsmith/trace-with-langchain) to get started. We recommend you also set up [LangSmith Engine](/langsmith/engine) which monitors your traces, detects issues, and proposes fixes.

---

# Build a semantic search engine with LangChain
> 출처: data/raw/langchain/knowledge-base.mdx | https://docs.langchain.com/oss/python/langchain/knowledge-base

## Overview

Build a semantic search engine over a PDF with LangChain [embeddings](/oss/integrations/embeddings) and [vector stores](/oss/integrations/vectorstores). Use it to retrieve passages similar to a query, then plug the retriever into [retrieval-augmented generation (RAG)](/oss/deepagents/retrieval) or other LLM workflows.

This tutorial covers:

1. Create `Document` objects from a PDF.
2. Generate embeddings.
3. Load and split a PDF.
4. Index chunks in a vector store and query by similarity.
5. Wrap the store as a retriever.

The guide also includes a minimal RAG implementation on top of the search engine.

### Concepts

This tutorial focuses on text retrieval and covers the following concepts:

- `Document`
- [Text splitters](/oss/integrations/splitters)
- [Embeddings](/oss/integrations/embeddings)
- [Vector stores](/oss/integrations/vectorstores) and [retrievers](/oss/integrations/retrievers)

## Setup

### Install dependencies

This tutorial reads a PDF using the `pypdf` package:

```bash pip
pip install pypdf
```
```bash conda
conda install pypdf -c conda-forge
```
```bash uv
uv add pypdf
```

For more details, see the [Installation guide](/oss/langchain/install).

### Configure LangSmith

Many of the applications you build with LangChain will contain multiple steps with multiple invocations of LLM calls.
As these applications get more and more complex, it becomes crucial to be able to inspect what exactly is going on inside your chain or agent.
The best way to do this is with [LangSmith](https://smith.langchain.com).

After you sign up at the link above, make sure to set your environment variables to start logging traces:

```shell
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```

In a notebook, you can set them with:

```python
import getpass
import os

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass()
```

## Create documents

LangChain implements a `Document` abstraction for a unit of text and associated metadata. It has three attributes:

- `page_content`: a string representing the content.
- `metadata`: a dict containing arbitrary metadata.
- `id`: (optional) a string identifier for the document.

`metadata` can capture the source of the document, its relationship to other documents, and other information. An individual `Document` often represents a chunk of a larger document.

The following code creates sample documents:

```python
from langchain_core.documents import Document

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
]
```

## Generate embeddings

Vector search stores numeric vectors associated with text. Embed a query as a vector of the same dimension, then use similarity metrics (such as cosine similarity) to find related text.

LangChain supports embeddings from [many providers](/oss/integrations/embeddings/). Select a model to specify how text should be converted into a numeric vector:

**OpenAI**

```shell
pip install -U "langchain-openai"
```

```python
import getpass
import os

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
```

**Azure**

```shell
pip install -U "langchain-openai"
```

```python
import getpass
import os

if not os.environ.get("AZURE_OPENAI_API_KEY"):
    os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass("Enter API key for Azure: ")

from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)
```

**Google Gemini**

```shell
pip install -qU langchain-google-genai
```

```python
import getpass
import os

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
```

**Gemini Enterprise Agent Platform**

```shell
pip install -qU langchain-google-vertexai
```

```python
from langchain_google_vertexai import VertexAIEmbeddings

embeddings = VertexAIEmbeddings(model="text-embedding-005")
```

**AWS**

```shell
pip install -qU langchain-aws
```

```python
from langchain_aws import BedrockEmbeddings

embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
```

**HuggingFace**

```shell
pip install -qU langchain-huggingface
```

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    encode_kwargs={"normalize_embeddings": True},
)
```

**Ollama**

```shell
pip install -qU langchain-ollama
```

```python
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="llama3")
```

**Cohere**

```shell
pip install -qU langchain-cohere
```

```python
import getpass
import os

if not os.environ.get("COHERE_API_KEY"):
    os.environ["COHERE_API_KEY"] = getpass.getpass("Enter API key for Cohere: ")

from langchain_cohere import CohereEmbeddings

embeddings = CohereEmbeddings(model="embed-english-v3.0")
```

**MistralAI**

```shell
pip install -qU langchain-mistralai
```

```python
import getpass
import os

if not os.environ.get("MISTRALAI_API_KEY"):
    os.environ["MISTRALAI_API_KEY"] = getpass.getpass("Enter API key for MistralAI: ")

from langchain_mistralai import MistralAIEmbeddings

embeddings = MistralAIEmbeddings(model="mistral-embed")
```

**Nomic**

```shell
pip install -qU langchain-nomic
```

```python
import getpass
import os

if not os.environ.get("NOMIC_API_KEY"):
    os.environ["NOMIC_API_KEY"] = getpass.getpass("Enter API key for Nomic: ")

from langchain_nomic import NomicEmbeddings

embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5")
```

**NVIDIA**

```shell
pip install -qU langchain-nvidia-ai-endpoints
```

```python
import getpass
import os

if not os.environ.get("NVIDIA_API_KEY"):
    os.environ["NVIDIA_API_KEY"] = getpass.getpass("Enter API key for NVIDIA: ")

from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

embeddings = NVIDIAEmbeddings(model="NV-Embed-QA")
```

**Voyage AI**

```shell
pip install -qU langchain-voyageai
```

```python
import getpass
import os

if not os.environ.get("VOYAGE_API_KEY"):
    os.environ["VOYAGE_API_KEY"] = getpass.getpass("Enter API key for Voyage AI: ")

from langchain-voyageai import VoyageAIEmbeddings

embeddings = VoyageAIEmbeddings(model="voyage-3")
```

**IBM watsonx**

```shell
pip install -qU langchain-ibm
```

```python
import getpass
import os

if not os.environ.get("WATSONX_APIKEY"):
    os.environ["WATSONX_APIKEY"] = getpass.getpass("Enter API key for IBM watsonx: ")

from langchain_ibm import WatsonxEmbeddings

embeddings = WatsonxEmbeddings(
    model_id="ibm/slate-125m-english-rtrvr",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="<WATSONX PROJECT_ID>",
)
```

**Fake**

```shell
pip install -qU langchain-core
```

```python
from langchain_core.embeddings import DeterministicFakeEmbedding

embeddings = DeterministicFakeEmbedding(size=4096)
```

**Isaacus**

```shell
pip install -qU langchain-isaacus
```

```python
import getpass
import os

if not os.environ.get("ISAACUS_API_KEY"):
os.environ["ISAACUS_API_KEY"] = getpass.getpass("Enter API key for Isaacus: ")

from langchain_isaacus import IsaacusEmbeddings

embeddings = IsaacusEmbeddings(model="kanon-2-embedder")
```

```python
vector_1 = embeddings.embed_query(documents[0].page_content)
vector_2 = embeddings.embed_query(documents[1].page_content)

assert len(vector_1) == len(vector_2)
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])
```

```text wrap
Generated vectors of length 1536

[-0.008586574345827103, -0.03341241180896759, -0.008936782367527485, -0.0036674530711025, 0.010564599186182022, 0.009598285891115665, -0.028587326407432556, -0.015824200585484505, 0.0030416189692914486, -0.012899317778646946]
```

Next, store embeddings in a vector store that supports efficient similarity search.

## Select a vector store

LangChain `VectorStore` objects add text and `Document` objects to a store and query them with similarity metrics. They are often initialized with [embedding](/oss/integrations/embeddings) models that translate text into numeric vectors.

LangChain includes [integrations](/oss/integrations/vectorstores) with many vector store technologies. Some are hosted and need credentials, some run in separate infrastructure (local or third-party), and others run in-memory for lightweight workloads. Select a vector store:

**In-memory**

```shell
pip install -U "langchain-core"
```

```python
from langchain_core.vectorstores import InMemoryVectorStore

vector_store = InMemoryVectorStore(embeddings)
```

**Amazon OpenSearch**

```shell
pip install -qU  boto3
```

```python
from opensearchpy import RequestsHttpConnection

service = "es"  # must set the service as 'es'
region = "us-east-2"
credentials = boto3.Session(
    aws_access_key_id="xxxxxx", aws_secret_access_key="xxxxx"
).get_credentials()
awsauth = AWS4Auth("xxxxx", "xxxxxx", region, service, session_token=credentials.token)

vector_store = OpenSearchVectorSearch.from_documents(
    docs,
    embeddings,
    opensearch_url="host url",
    http_auth=awsauth,
    timeout=300,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    index_name="test-index",
)
```

**AstraDB**

```shell
pip install -U "langchain-astradb"
```

```python
from langchain_astradb import AstraDBVectorStore

vector_store = AstraDBVectorStore(
    embedding=embeddings,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    collection_name="astra_vector_langchain",
    token=ASTRA_DB_APPLICATION_TOKEN,
    namespace=ASTRA_DB_NAMESPACE,
)
```

**Chroma**

```shell
pip install -qU langchain-chroma
```

```python
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)
```

**Milvus**

```shell
pip install -qU langchain-milvus
```

```python
from langchain_milvus import Milvus

URI = "./milvus_example.db"

vector_store = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": URI},
    index_params={"index_type": "FLAT", "metric_type": "L2"},
)
```

**MongoDB**

```shell
pip install -qU langchain-mongodb
```

```python
from langchain_mongodb import MongoDBAtlasVectorSearch

vector_store = MongoDBAtlasVectorSearch(
    embedding=embeddings,
    collection=MONGODB_COLLECTION,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)
```

**PGVector**

```shell
pip install -qU langchain-postgres
```

```python
from langchain_postgres import PGVector

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="my_docs",
    connection="postgresql+psycopg://...",
)
```

**PGVectorStore**

```shell
pip install -qU langchain-postgres
```

```python
from langchain_postgres import PGEngine, PGVectorStore

pg_engine = PGEngine.from_connection_string(
    url="postgresql+psycopg://..."
)

vector_store = PGVectorStore.create_sync(
    engine=pg_engine,
    table_name='test_table',
    embedding_service=embeddings
)
```

**Pinecone**

```shell
pip install -qU langchain-pinecone
```

```python
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

pc = Pinecone(api_key=...)
index = pc.Index(index_name)

vector_store = PineconeVectorStore(embedding=embeddings, index=index)
```

**Qdrant**

```shell
pip install -qU langchain-qdrant
```

```python
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")

vector_size = len(embeddings.embed_query("sample text"))

if not client.collection_exists("test"):
    client.create_collection(
        collection_name="test",
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
vector_store = QdrantVectorStore(
    client=client,
    collection_name="test",
    embedding=embeddings,
)
```

## Load and split a PDF

Load content from a PDF, then split it into smaller chunks before indexing. This example uses [a sample Nike 10-K filing from 2023](https://github.com/langchain-ai/langchain/blob/v0.3/docs/docs/example_data/nke-10k-2023.pdf).

For dedicated PDF document loaders (including `PyPDFLoader` and partner packages), see [PDF document loaders](/oss/integrations/document_loaders#pdfs).

```python
import pypdf
from langchain_core.documents import Document

# Below is a minimal helper for demonstration purposes.
def load_pdf_pages(file_path: str) -> list[Document]:
    reader = pypdf.PdfReader(file_path)
    return [
        Document(
            page_content=page.extract_text() or "",
            metadata={"source": file_path, "page": i},
        )
        for i, page in enumerate(reader.pages)
    ]

file_path = "../example_data/nke-10k-2023.pdf"
docs = load_pdf_pages(file_path)
print(len(docs))
```

```text
107
```

A page is often too coarse for retrieval. Split pages further so relevant passages are not diluted by surrounding text. `RecursiveCharacterTextSplitter` recursively splits on common separators (such as newlines) until each chunk is the target size. This is the recommended text splitter for generic text use cases.

Set `add_start_index=True` so each split keeps a `start_index` metadata field for its character offset in the original document.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

print(len(all_splits))
```

```text
516
```

## Index documents

Index the chunks into the vector store:

```python
ids = vector_store.add_documents(documents=all_splits)
```

Most vector store integrations also support connecting to an existing store (for example with a client or index name). See the docs for a specific [integration](/oss/integrations/vectorstores) for details.

## Query the vector store

After you have added the documents to the `VectorStore`, you can query it:

- Synchronously and asynchronously
- By string query and by vector
- With and without similarity scores
- By similarity and maximum marginal relevance (to balance similarity with diversity)

These methods generally return a list of `Document` objects.

### Search by string

Embeddings map text to dense vectors so similar meanings are geometrically close. This means you can Retrieve relevant passages by passing a natural-language question:

```python
results = vector_store.similarity_search(
    "How many distribution centers does Nike have in the US?"
)

print(results[0])
```
```python wrap
page_content='direct to consumer operations sell products through the following number of retail stores in the United States:
U.S. RETAIL STORES NUMBER
NIKE Brand factory stores 213
NIKE Brand in-line stores (including employee-only stores) 74
Converse stores (including factory stores) 82
TOTAL 369
In the United States, NIKE has eight significant distribution centers. Refer to Item 2. Properties for further information.
2023 FORM 10-K 2' metadata={'page': 4, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 3125}
```

Async query:

```python
results = await vector_store.asimilarity_search("When was Nike incorporated?")

print(results[0])
```
```python wrap
page_content='Table of Contents
PART I
ITEM 1. BUSINESS
GENERAL
NIKE, Inc. was incorporated in 1967 under the laws of the State of Oregon. As used in this Annual Report on Form 10-K (this "Annual Report"), the terms "we," "us," "our,"
"NIKE" and the "Company" refer to NIKE, Inc. and its predecessors, subsidiaries and affiliates, collectively, unless the context indicates otherwise.
Our principal business activity is the design, development and worldwide marketing and selling of athletic footwear, apparel, equipment, accessories and services. NIKE is
the largest seller of athletic footwear and apparel in the world. We sell our products through NIKE Direct operations, which are comprised of both NIKE-owned retail stores
and sales through our digital platforms (also referred to as "NIKE Brand Digital"), to retail accounts and to a mix of independent distributors, licensees and sales' metadata={'page': 3, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 0}
```

### Return scores

You can return similarity scores with the documents. Score meaning varies by provider. In this case, the score is a distance metric that varies inversely with similarity:

```python
# Note that providers implement different scores; the score here
# is a distance metric that varies inversely with similarity.

results = vector_store.similarity_search_with_score("What was Nike's revenue in 2023?")
doc, score = results[0]
print(f"Score: {score}\n")
print(doc)
```
```python wrap
Score: 0.23699893057346344

page_content='Table of Contents
FISCAL 2023 NIKE BRAND REVENUE HIGHLIGHTS
The following tables present NIKE Brand revenues disaggregated by reportable operating segment, distribution channel and major product line:
FISCAL 2023 COMPARED TO FISCAL 2022
•NIKE, Inc. Revenues were $51.2 billion in fiscal 2023, which increased 10% and 16% compared to fiscal 2022 on a reported and currency-neutral basis, respectively.
The increase was due to higher revenues in North America, Europe, Middle East & Africa ("EMEA"), APLA and Greater China, which contributed approximately 7, 6,
2 and 1 percentage points to NIKE, Inc. Revenues, respectively.
•NIKE Brand revenues, which represented over 90% of NIKE, Inc. Revenues, increased 10% and 16% on a reported and currency-neutral basis, respectively. This
increase was primarily due to higher revenues in Men's, the Jordan Brand, Women's and Kids' which grew 17%, 35%,11% and 10%, respectively, on a wholesale
equivalent basis.' metadata={'page': 35, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 0}
```

### Search by vector

Embed the query yourself, then search with the resulting vector:

```python
embedding = embeddings.embed_query("How were Nike's margins impacted in 2023?")

results = vector_store.similarity_search_by_vector(embedding)
print(results[0])
```
```python wrap
page_content='Table of Contents
GROSS MARGIN
FISCAL 2023 COMPARED TO FISCAL 2022
For fiscal 2023, our consolidated gross profit increased 4% to $22,292 million compared to $21,479 million for fiscal 2022. Gross margin decreased 250 basis points to
43.5% for fiscal 2023 compared to 46.0% for fiscal 2022 due to the following:
*Wholesale equivalent
The decrease in gross margin for fiscal 2023 was primarily due to:
•Higher NIKE Brand product costs, on a wholesale equivalent basis, primarily due to higher input costs and elevated inbound freight and logistics costs as well as
product mix;
•Lower margin in our NIKE Direct business, driven by higher promotional activity to liquidate inventory in the current period compared to lower promotional activity in
the prior period resulting from lower available inventory supply;
•Unfavorable changes in net foreign currency exchange rates, including hedges; and
•Lower off-price margin, on a wholesale equivalent basis.
This was partially offset by:' metadata={'page': 36, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 0}
```

Learn more:

- API Reference
- [Integration-specific docs](/oss/integrations/vectorstores)

## Use retrievers

LangChain `VectorStore` objects do not subclass `Runnable`. Retrievers are Runnables, so they support standard methods such as sync and async `invoke` and `batch`.

You can also build retrievers from vector stores, and retrievers can also wrap non-vector sources (such as external APIs).

In this case, create a simple retriever without subclassing `Retriever` by wrapping `similarity_search`:

```python
from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import chain

@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query, k=1)

retriever.batch(
    [
        "How many distribution centers does Nike have in the US?",
        "When was Nike incorporated?",
    ],
)
```

```text wrap
[[Document(metadata={'page': 4, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 3125}, page_content='direct to consumer operations sell products through the following number of retail stores in the United States:\nU.S. RETAIL STORES NUMBER\nNIKE Brand factory stores 213 \nNIKE Brand in-line stores (including employee-only stores) 74 \nConverse stores (including factory stores) 82 \nTOTAL 369 \nIn the United States, NIKE has eight significant distribution centers. Refer to Item 2. Properties for further information.\n2023 FORM 10-K 2')],
 [Document(metadata={'page': 3, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 0}, page_content='Table of Contents\nPART I\nITEM 1. BUSINESS\nGENERAL\nNIKE, Inc. was incorporated in 1967 under the laws of the State of Oregon. As used in this Annual Report on Form 10-K (this "Annual Report"), the terms "we," "us," "our,"\n"NIKE" and the "Company" refer to NIKE, Inc. and its predecessors, subsidiaries and affiliates, collectively, unless the context indicates otherwise.\nOur principal business activity is the design, development and worldwide marketing and selling of athletic footwear, apparel, equipment, accessories and services. NIKE is\nthe largest seller of athletic footwear and apparel in the world. We sell our products through NIKE Direct operations, which are comprised of both NIKE-owned retail stores\nand sales through our digital platforms (also referred to as "NIKE Brand Digital"), to retail accounts and to a mix of independent distributors, licensees and sales')]]
```

Vector stores implement an `as_retriever` method that returns a [`VectorStoreRetriever`](https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStoreRetriever). These retrievers expose `search_type` and `search_kwargs` to select and parameterize the underlying store methods. Replicate the example above with:

```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)

retriever.batch(
    [
        "How many distribution centers does Nike have in the US?",
        "When was Nike incorporated?",
    ],
)
```
```text wrap
[[Document(metadata={'page': 4, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 3125}, page_content='direct to consumer operations sell products through the following number of retail stores in the United States:\nU.S. RETAIL STORES NUMBER\nNIKE Brand factory stores 213 \nNIKE Brand in-line stores (including employee-only stores) 74 \nConverse stores (including factory stores) 82 \nTOTAL 369 \nIn the United States, NIKE has eight significant distribution centers. Refer to Item 2. Properties for further information.\n2023 FORM 10-K 2')],
 [Document(metadata={'page': 3, 'source': '../example_data/nke-10k-2023.pdf', 'start_index': 0}, page_content='Table of Contents\nPART I\nITEM 1. BUSINESS\nGENERAL\nNIKE, Inc. was incorporated in 1967 under the laws of the State of Oregon. As used in this Annual Report on Form 10-K (this "Annual Report"), the terms "we," "us," "our,"\n"NIKE" and the "Company" refer to NIKE, Inc. and its predecessors, subsidiaries and affiliates, collectively, unless the context indicates otherwise.\nOur principal business activity is the design, development and worldwide marketing and selling of athletic footwear, apparel, equipment, accessories and services. NIKE is\nthe largest seller of athletic footwear and apparel in the world. We sell our products through NIKE Direct operations, which are comprised of both NIKE-owned retail stores\nand sales through our digital platforms (also referred to as "NIKE Brand Digital"), to retail accounts and to a mix of independent distributors, licensees and sales')]]
```

`VectorStoreRetriever` supports search types of `"similarity"` (default), `"mmr"` (maximum marginal relevance), and `"similarity_score_threshold"`. Use the last option to filter documents by similarity score.

You can use retrievers in more complex apps such as [retrieval-augmented generation (RAG)](/oss/deepagents/retrieval), which combine a question with retrieved context in a prompt for an LLM. To learn more about building such an application, check out the [RAG tutorial](/oss/deepagents/rag) tutorial.

## Next steps

You've now seen how to build a semantic search engine over a PDF document.

For more information see:

- [Available embedding integrations](/oss/integrations/embeddings)
- [Available vector store integrations](/oss/integrations/vectorstores)

For more on RAG:

- [Retrieval overview](/oss/deepagents/retrieval)
- [RAG with Deep Agents](/oss/deepagents/rag)
- [Evaluate a RAG application](/langsmith/evaluate-rag-tutorial)

---

# Long-term memory
> 출처: data/raw/langchain/long-term-memory.mdx | https://docs.langchain.com/oss/python/langchain/long-term-memory

Add long-term memory to LangChain agents to store and recall data across conversations and sessions

Long-term memory lets your agent store and recall information across different conversations and sessions.
Unlike [short-term memory](/oss/langchain/short-term-memory), which is scoped to a single thread, long-term memory persists across threads and can be recalled at any time.

Long-term memory is built on [LangGraph stores](/oss/langgraph/stores), which save data as JSON documents organized by namespace and key.

## Usage

To add long-term memory to an agent, create a store and pass it to `create_agent`:

**InMemoryStore**

```python
from langchain.agents import create_agent
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production use.
store = InMemoryStore()

agent: Runnable = create_agent(
    "claude-sonnet-4-6",
    tools=[],
    store=store,
)
```

- [View example trace](https://smith.langchain.com/public/2521e9f7-35c6-4a40-9b50-bedf6b66f302/r)

  Open a public LangSmith run for this example.

**PostgreSQL**

```bash pip
pip install -U langgraph-checkpoint-postgres "psycopg[binary]"
```

```bash uv
uv add langgraph-checkpoint-postgres "psycopg[binary]"
```

**Note:**

By default, `langgraph-checkpoint-postgres` installs `psycopg` (Psycopg 3) without extras. The install above adds `psycopg[binary]`, which is recommended for most users. For other options, see the [Psycopg installation docs](https://www.psycopg.org/psycopg3/docs/basic/install.html).

```python
from langchain.agents import create_agent
from langchain_core.runnables import Runnable
from langgraph.store.postgres import PostgresStore  # type: ignore[import-not-found]

DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"

with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()
    agent: Runnable = create_agent(
        "claude-sonnet-4-6",
        tools=[],
        store=store,
    )
```

- [View example trace](https://smith.langchain.com/public/d2faa3ae-94bf-4a5e-a373-abf574b7223c/r)

  Open a public LangSmith run for this example.

**Note:**

For other store backends, including Redis and MongoDB, see the [store integrations](/oss/integrations/long-term-memory) list. For a MongoDB walkthrough, see [long-term memory with MongoDB](/oss/integrations/memory/mongodb-long-term-memory).

Tools can then read from and write to the store using the `runtime.store` parameter. See [Read long-term memory in tools](#read-long-term-memory-in-tools) and [Write long-term memory from tools](#write-long-term-memory-from-tools) for examples.

**Tip:**

For a deeper dive into memory types (semantic, episodic, procedural) and strategies for writing memories, see the [Memory conceptual guide](/oss/concepts/memory#long-term-memory).

## Memory storage

LangGraph stores long-term memories as JSON documents in a [store](/oss/langgraph/stores).

Each memory is organized under a custom `namespace` (similar to a folder) and a distinct `key` (like a file name). Namespaces often include user or org IDs or other labels that makes it easier to organize information.

This structure enables hierarchical organization of memories. Cross-namespace searching is then supported through content filters.

**InMemoryStore**

```python
from collections.abc import Sequence

from langgraph.store.base import IndexConfig
from langgraph.store.memory import InMemoryStore

def embed(texts: Sequence[str]) -> list[list[float]]:
    # Replace with an actual embedding function or LangChain embeddings object
    return [[1.0, 2.0] for _ in texts]

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production use.
store = InMemoryStore(index=IndexConfig(embed=embed, dims=2))
user_id = "my-user"
application_context = "chitchat"
namespace = (user_id, application_context)
store.put(
    namespace,
    "a-memory",
    {
        "rules": [
            "User likes short, direct language",
            "User only speaks English & python",
        ],
        "my-key": "my-value",
    },
)
# get the "memory" by ID
item = store.get(namespace, "a-memory")
# search for "memories" within this namespace, filtering on content equivalence, sorted by vector similarity
items = store.search(
    namespace, filter={"my-key": "my-value"}, query="language preferences"
)
```

- [View example trace](https://smith.langchain.com/public/19bcf66b-a673-4d5c-b936-f9110546d42c/r)

  Open a public LangSmith run for this example.

**PostgreSQL**

```python
from collections.abc import Sequence

from langgraph.store.base import IndexConfig
from langgraph.store.postgres import PostgresStore  # type: ignore[import-not-found]

def embed(texts: Sequence[str]) -> list[list[float]]:
    # Replace with an actual embedding function or LangChain embeddings object
    return [[1.0, 2.0] for _ in texts]

DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"

with PostgresStore.from_conn_string(
    DB_URI,
    index=IndexConfig(embed=embed, dims=2),  # type: ignore[arg-type]
) as store:
    store.setup()
    user_id = "my-user"
    application_context = "chitchat"
    namespace = (user_id, application_context)
    store.put(
        namespace,
        "a-memory",
        {
            "rules": [
                "User likes short, direct language",
                "User only speaks English & python",
            ],
            "my-key": "my-value",
        },
    )
    item = store.get(namespace, "a-memory")
    items = store.search(
        namespace, filter={"my-key": "my-value"}, query="language preferences"
    )
```

- [View example trace](https://smith.langchain.com/public/072edfca-d661-4858-a2ff-663daff0c41e/r)

  Open a public LangSmith run for this example.

For more information about the memory store, see the [Persistence](/oss/langgraph/stores) guide.

## Read long-term memory in tools

**InMemoryStore**

```python Google
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

# Write sample data to the store using the put method
store.put(
    (
        "users",
    ),  # Namespace to group related data together (users namespace for user data)
    "user_123",  # Key within the namespace (user ID as key)
    {
        "name": "John Smith",
        "language": "English",
    },  # Data to store for the given user
)

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Look up user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    user_id = runtime.context.user_id
    # Retrieve data from store - returns StoreValue object with value and metadata
    user_info = runtime.store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

agent: Runnable = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[get_user_info],
    # Pass store to agent - enables agent to access store when running tools
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "look up user information"}]},
    context=Context(user_id="user_123"),
)
```

```python OpenAI
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

# Write sample data to the store using the put method
store.put(
    (
        "users",
    ),  # Namespace to group related data together (users namespace for user data)
    "user_123",  # Key within the namespace (user ID as key)
    {
        "name": "John Smith",
        "language": "English",
    },  # Data to store for the given user
)

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Look up user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    user_id = runtime.context.user_id
    # Retrieve data from store - returns StoreValue object with value and metadata
    user_info = runtime.store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

agent: Runnable = create_agent(
    model="openai:gpt-5.5",
    tools=[get_user_info],
    # Pass store to agent - enables agent to access store when running tools
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "look up user information"}]},
    context=Context(user_id="user_123"),
)
```

```python Anthropic
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

# Write sample data to the store using the put method
store.put(
    (
        "users",
    ),  # Namespace to group related data together (users namespace for user data)
    "user_123",  # Key within the namespace (user ID as key)
    {
        "name": "John Smith",
        "language": "English",
    },  # Data to store for the given user
)

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Look up user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    user_id = runtime.context.user_id
    # Retrieve data from store - returns StoreValue object with value and metadata
    user_info = runtime.store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

agent: Runnable = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[get_user_info],
    # Pass store to agent - enables agent to access store when running tools
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "look up user information"}]},
    context=Context(user_id="user_123"),
)
```

```python OpenRouter
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

# Write sample data to the store using the put method
store.put(
    (
        "users",
    ),  # Namespace to group related data together (users namespace for user data)
    "user_123",  # Key within the namespace (user ID as key)
    {
        "name": "John Smith",
        "language": "English",
    },  # Data to store for the given user
)

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Look up user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    user_id = runtime.context.user_id
    # Retrieve data from store - returns StoreValue object with value and metadata
    user_info = runtime.store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

agent: Runnable = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[get_user_info],
    # Pass store to agent - enables agent to access store when running tools
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "look up user information"}]},
    context=Context(user_id="user_123"),
)
```

```python Fireworks
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

# Write sample data to the store using the put method
store.put(
    (
        "users",
    ),  # Namespace to group related data together (users namespace for user data)
    "user_123",  # Key within the namespace (user ID as key)
    {
        "name": "John Smith",
        "language": "English",
    },  # Data to store for the given user
)

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Look up user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    user_id = runtime.context.user_id
    # Retrieve data from store - returns StoreValue object with value and metadata
    user_info = runtime.store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

agent: Runnable = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[get_user_info],
    # Pass store to agent - enables agent to access store when running tools
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "look up user information"}]},
    context=Context(user_id="user_123"),
)
```

```python Baseten
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

# Write sample data to the store using the put method
store.put(
    (
        "users",
    ),  # Namespace to group related data together (users namespace for user data)
    "user_123",  # Key within the namespace (user ID as key)
    {
        "name": "John Smith",
        "language": "English",
    },  # Data to store for the given user
)

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Look up user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    user_id = runtime.context.user_id
    # Retrieve data from store - returns StoreValue object with value and metadata
    user_info = runtime.store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

agent: Runnable = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[get_user_info],
    # Pass store to agent - enables agent to access store when running tools
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "look up user information"}]},
    context=Context(user_id="user_123"),
)
```

```python Ollama
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

# Write sample data to the store using the put method
store.put(
    (
        "users",
    ),  # Namespace to group related data together (users namespace for user data)
    "user_123",  # Key within the namespace (user ID as key)
    {
        "name": "John Smith",
        "language": "English",
    },  # Data to store for the given user
)

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Look up user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    user_id = runtime.context.user_id
    # Retrieve data from store - returns StoreValue object with value and metadata
    user_info = runtime.store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

agent: Runnable = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[get_user_info],
    # Pass store to agent - enables agent to access store when running tools
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "look up user information"}]},
    context=Context(user_id="user_123"),
)
```

- [View example trace](https://smith.langchain.com/public/a1a10780-0608-450e-9d0e-86dac1a9747e/r)

  Open a public LangSmith run for this example.

**PostgreSQL**

```python
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.postgres import PostgresStore  # type: ignore[import-not-found]

@dataclass
class Context:
    user_id: str

DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"

with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()
    store.put(("users",), "user_123", {"name": "John Smith", "language": "English"})

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Look up user info."""
    assert runtime.store is not None
    user_info = runtime.store.get(("users",), runtime.context.user_id)
    return str(user_info.value) if user_info else "Unknown user"

agent: Runnable = create_agent(
    "claude-sonnet-4-6",
    tools=[get_user_info],
    store=store,
    context_schema=Context,
)

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "look up user information"}]},
        context=Context(user_id="user_123"),
    )
```

- [View example trace](https://smith.langchain.com/public/af4184a4-46db-413d-a847-571c44ac1627/r)

  Open a public LangSmith run for this example.

<a id="write-long-term"></a>
## Write long-term memory from tools

**InMemoryStore**

```python Google
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore
from typing_extensions import TypedDict

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

@dataclass
class Context:
    user_id: str

# TypedDict defines the structure of user information for the LLM
class UserInfo(TypedDict):
    name: str

# Tool that allows agent to update user information (useful for chat applications)
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    store = runtime.store
    user_id = runtime.context.user_id
    # Store data in the store (namespace, key, data)
    store.put(("users",), user_id, dict(user_info))
    return "Successfully saved user info."

agent: Runnable = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[save_user_info],
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is John Smith"}]},
    # user_id passed in context to identify whose information is being updated
    context=Context(user_id="user_123"),
)

# You can access the store directly to get the value
item = store.get(("users",), "user_123")
```

```python OpenAI
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore
from typing_extensions import TypedDict

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

@dataclass
class Context:
    user_id: str

# TypedDict defines the structure of user information for the LLM
class UserInfo(TypedDict):
    name: str

# Tool that allows agent to update user information (useful for chat applications)
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    store = runtime.store
    user_id = runtime.context.user_id
    # Store data in the store (namespace, key, data)
    store.put(("users",), user_id, dict(user_info))
    return "Successfully saved user info."

agent: Runnable = create_agent(
    model="openai:gpt-5.5",
    tools=[save_user_info],
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is John Smith"}]},
    # user_id passed in context to identify whose information is being updated
    context=Context(user_id="user_123"),
)

# You can access the store directly to get the value
item = store.get(("users",), "user_123")
```

```python Anthropic
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore
from typing_extensions import TypedDict

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

@dataclass
class Context:
    user_id: str

# TypedDict defines the structure of user information for the LLM
class UserInfo(TypedDict):
    name: str

# Tool that allows agent to update user information (useful for chat applications)
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    store = runtime.store
    user_id = runtime.context.user_id
    # Store data in the store (namespace, key, data)
    store.put(("users",), user_id, dict(user_info))
    return "Successfully saved user info."

agent: Runnable = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[save_user_info],
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is John Smith"}]},
    # user_id passed in context to identify whose information is being updated
    context=Context(user_id="user_123"),
)

# You can access the store directly to get the value
item = store.get(("users",), "user_123")
```

```python OpenRouter
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore
from typing_extensions import TypedDict

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

@dataclass
class Context:
    user_id: str

# TypedDict defines the structure of user information for the LLM
class UserInfo(TypedDict):
    name: str

# Tool that allows agent to update user information (useful for chat applications)
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    store = runtime.store
    user_id = runtime.context.user_id
    # Store data in the store (namespace, key, data)
    store.put(("users",), user_id, dict(user_info))
    return "Successfully saved user info."

agent: Runnable = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[save_user_info],
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is John Smith"}]},
    # user_id passed in context to identify whose information is being updated
    context=Context(user_id="user_123"),
)

# You can access the store directly to get the value
item = store.get(("users",), "user_123")
```

```python Fireworks
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore
from typing_extensions import TypedDict

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

@dataclass
class Context:
    user_id: str

# TypedDict defines the structure of user information for the LLM
class UserInfo(TypedDict):
    name: str

# Tool that allows agent to update user information (useful for chat applications)
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    store = runtime.store
    user_id = runtime.context.user_id
    # Store data in the store (namespace, key, data)
    store.put(("users",), user_id, dict(user_info))
    return "Successfully saved user info."

agent: Runnable = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[save_user_info],
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is John Smith"}]},
    # user_id passed in context to identify whose information is being updated
    context=Context(user_id="user_123"),
)

# You can access the store directly to get the value
item = store.get(("users",), "user_123")
```

```python Baseten
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore
from typing_extensions import TypedDict

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

@dataclass
class Context:
    user_id: str

# TypedDict defines the structure of user information for the LLM
class UserInfo(TypedDict):
    name: str

# Tool that allows agent to update user information (useful for chat applications)
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    store = runtime.store
    user_id = runtime.context.user_id
    # Store data in the store (namespace, key, data)
    store.put(("users",), user_id, dict(user_info))
    return "Successfully saved user info."

agent: Runnable = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[save_user_info],
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is John Smith"}]},
    # user_id passed in context to identify whose information is being updated
    context=Context(user_id="user_123"),
)

# You can access the store directly to get the value
item = store.get(("users",), "user_123")
```

```python Ollama
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore
from typing_extensions import TypedDict

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

@dataclass
class Context:
    user_id: str

# TypedDict defines the structure of user information for the LLM
class UserInfo(TypedDict):
    name: str

# Tool that allows agent to update user information (useful for chat applications)
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user info."""
    # Access the store - same as that provided to `create_agent`
    assert runtime.store is not None
    store = runtime.store
    user_id = runtime.context.user_id
    # Store data in the store (namespace, key, data)
    store.put(("users",), user_id, dict(user_info))
    return "Successfully saved user info."

agent: Runnable = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[save_user_info],
    store=store,
    context_schema=Context,
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is John Smith"}]},
    # user_id passed in context to identify whose information is being updated
    context=Context(user_id="user_123"),
)

# You can access the store directly to get the value
item = store.get(("users",), "user_123")
```

- [View example trace](https://smith.langchain.com/public/d2799b9a-c5ad-465a-8980-ea8aa39f59dc/r)

  Open a public LangSmith run for this example.

**PostgreSQL**

```python
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.postgres import PostgresStore  # type: ignore[import-not-found]
from typing_extensions import TypedDict

@dataclass
class Context:
    user_id: str

class UserInfo(TypedDict):
    name: str

@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user info."""
    assert runtime.store is not None
    runtime.store.put(("users",), runtime.context.user_id, dict(user_info))
    return "Successfully saved user info."

DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"

with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()
    agent: Runnable = create_agent(
        "claude-sonnet-4-6",
        tools=[save_user_info],
        store=store,
        context_schema=Context,
    )

    agent.invoke(
        {"messages": [{"role": "user", "content": "My name is John Smith"}]},
        context=Context(user_id="user_123"),
    )
```

- [View example trace](https://smith.langchain.com/public/5c75411b-ff91-449b-bfce-c9c0fdacb530/r)

  Open a public LangSmith run for this example.

---

# Authentication
> 출처: data/raw/langchain/mcp/auth.mdx | https://docs.langchain.com/oss/python/langchain/mcp/auth

Authenticate MCP connections with bearer tokens, OAuth 2.1, or per-user credentials in LangChain.

Most remote MCP servers require authentication. `MCPAdapter` delegates auth to FastMCP, so any credential a `fastmcp.Client` accepts works: a static [bearer token](#bearer-token), a full [OAuth 2.1](#oauth-authentication) flow, or any [`httpx.Auth`](https://www.python-httpx.org/advanced/authentication/). Pass the credential on a prebuilt client and hand that client to the adapter. When one agent talks to several servers, use [per-server authentication](#per-server-authentication); in a deployment, use [per-user authentication](#per-user-authentication) so each run reaches the server as the caller.

**Note:**

The `langchain.mcp` namespace requires `langchain[mcp]>=1.4.0` and is in beta. The API may change.

## Bearer token

The simplest case: the server verifies a token you provisioned and adds it in the `Authorization: Bearer <token>` header. There is no discovery, browser, or refresh. Pass the token as the client's `auth`:

```python
from fastmcp.client import Client
from langchain.mcp import MCPAdapter

async def load_tools_with_bearer(url: str, token: str) -> list:
    # `auth` accepts a bearer-token string, the literal "oauth" (full OAuth 2.1
    # with dynamic client registration), or any `httpx.Auth`.
    async with MCPAdapter(Client(url, auth=token)) as adapter:
        return await adapter.list_tools()
```

The `auth` argument accepts a bearer-token string, the literal `"oauth"`, or any `httpx.Auth`. In an `MCPConfig` fleet, each server takes the same key.

## OAuth authentication

For a server that issues its own credentials, pass the literal string `"oauth"`. FastMCP runs the full OAuth 2.1 flow: discovery, [dynamic client registration](https://modelcontextprotocol.io/specification/draft/basic/authorization), the browser redirect, and the token exchange. Dynamic client registration means the client registers itself at runtime instead of you pre-provisioning a client ID:

```python
async def load_tools_with_oauth(url: str) -> list:
    # "oauth" runs discovery, dynamic client registration, the browser redirect,
    # and the token exchange. Pass `OAuth(..., token_storage=...)` to persist
    # tokens across runs instead of repeating the browser step each time.
    async with MCPAdapter(Client(url, auth="oauth")) as adapter:
        return await adapter.list_tools()
```

By default tokens are held in memory, so each run repeats the browser step. Pass a prebuilt `OAuth` provider with a token store to persist them across runs:

```python
from fastmcp.client import Client
from fastmcp.client.auth import OAuth

oauth = OAuth(mcp_url="https://example.com/mcp", token_storage=...)
client = Client("https://example.com/mcp", auth=oauth)
```

FastMCP ships providers for common identity providers (Auth0, WorkOS, Okta, and more); the flow the client runs is identical across them. See [OAuth authentication](https://gofastmcp.com/clients/auth/oauth) in the FastMCP documentation.

## Per-server authentication

When one agent talks to several servers, each server may need its own credential. Give each its own connection with a [`ClientGroup`](/oss/langchain/mcp/connections#independent-connections-with-clientgroup), and set `auth` per client, so every server authenticates independently:

```python
from fastmcp.client.group import ClientGroup

async def load_with_per_server_auth(
    billing_url: str, docs_token: str, docs_url: str
) -> list:
    # Each server carries its own credential. A `ClientGroup` keeps one
    # connection per server, so each authenticates independently.
    group = ClientGroup(
        {
            "billing": Client(billing_url, auth="oauth"),
            "docs": Client(docs_url, auth=docs_token),
        }
    )
    async with MCPAdapter(group) as adapter:
        return await adapter.list_tools()
```

## Per-user authentication

In a deployment, each run should reach the MCP server as the user who initiated it, not with one shared credential. The pattern has two halves:

1. **Authenticate the caller at the LangGraph server.** A [custom auth handler](/langsmith/auth) resolves the incoming request to a user identity, which each run reads off its runtime.
2. **Mint or exchange a credential for that user.** Inside the [graph factory](/oss/langchain/mcp/connections#scale-a-deployment), read the user's identity and build the MCP client with a per-user token, so the connection carries that user's authorization.

```python
from fastmcp.client import Client
from fastmcp.client.auth import BearerAuth

CONFIG = {
    "mcpServers": {
        "docs": { "url": "https://example.com/mcp" }
    }
}

async def make_graph(runtime):
    user = runtime.user.identity if runtime.user is not None else "anonymous"
    auth = BearerAuth(token_for(user))  # exchange for a per-user token
    async with MCPAdapter(Client(CONFIG, auth=auth)) as adapter:
        tools = await adapter.list_tools()
        return create_agent("claude-sonnet-5", tools)
```

In production, `token_for` stands in for whatever the deployment already has: an OAuth gateway that exchanges the session for a per-user token, or a `fastmcp.client.auth` provider that runs the authorization-code flow per identity. Isolate any [cached responses](/oss/langchain/mcp/connections#caching) per user, keyed off the verified identity, so one user never sees another's cached tool list.

## See also

- [FastMCP OAuth authentication](https://gofastmcp.com/clients/auth/oauth)
- [FastMCP bearer token authentication](https://gofastmcp.com/clients/auth/bearer)
- [FastMCP machine-to-machine authentication](https://gofastmcp.com/clients/auth/client-credentials)
- [FastMCP client groups](https://gofastmcp.com/clients/client-groups) — independent connections for per-server auth
- [FastMCP server authentication providers](https://gofastmcp.com/servers/auth/authentication)
- [MCP authorization specification](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [Custom authentication for a LangGraph server](/langsmith/auth)

---

# Connections
> 출처: data/raw/langchain/mcp/connections.mdx | https://docs.langchain.com/oss/python/langchain/mcp/connections

Connection lifecycle, multiple servers, deployment scaling, protocol eras, and caching for MCP in LangChain.

**Note:**

The `langchain.mcp` namespace requires `langchain[mcp]>=1.4.0` and is in beta. The API may change.

`MCPAdapter` opens an MCP connection, discovers tools, and returns LangChain tools your agent can call. How you pass servers in, and how long you keep the adapter open, depends on the shape of your app. The connection itself is FastMCP's; this page covers the LangChain patterns and links out to FastMCP for transport and client details.

Prefer the [default lifecycle](#connection-lifecycle) unless you are connecting to several servers or deploying many concurrent runs. For what a single target can be (URL, script path, in-process server), see [Transports](/oss/langchain/mcp#transports).

## Choose a pattern

Pick one row from each table. Server shape and connection lifetime are independent; any shape works with any lifetime.

**Server shape**

| If you need… | Use | Go to |
| --- | --- | --- |
| One server | A URL, `Path`, or in-process target | [Transports](/oss/langchain/mcp#transports) |
| Several servers behind one connection | An `MCPConfig` dict | [MCPConfig](#one-aggregate-connection-with-mcpconfig) |
| Several servers with separate auth, protocol eras, or pools | A [`ClientGroup`](https://gofastmcp.com/clients/client-groups) | [ClientGroup](#independent-connections-with-clientgroup) |

**Connection lifetime**

| Situation | Pattern | Go to |
| --- | --- | --- |
| Script, notebook, or most agents | Discover inside `async with`, then exit | [Connection lifecycle](#connection-lifecycle) |
| Hold one session across several tool calls in a run | Keep the adapter open around the agent call | [One session per invocation](#one-session-per-invocation) |
| Many concurrent runs in a deployment | Discover per run; reuse a [shared pool](#shared-connection-pool) and [cache](#caching) | [Scale a deployment](#scale-a-deployment) |

## Connection lifecycle

`MCPAdapter` is an async context manager. Entering it connects the underlying client; exiting it releases the connection. Discovery happens inside the context, but the tools it returns hold the client, so they stay callable after the context exits.

To discover tools and build an agent (the default pattern):

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

async def build_agent(target):
    # Discover and build the agent inside the adapter's context. The tools hold
    # the client, so the agent stays usable after the context exits.
    async with MCPAdapter(target) as adapter:
        tools = await adapter.list_tools()
        return create_agent("claude-sonnet-5", tools)
```

You do not need to keep the adapter open for the life of the agent. Prefer this pattern unless you are [holding a session open](#one-session-per-invocation) or [scaling a deployment](#scale-a-deployment).

### One session per invocation

The tools `MCPAdapter` returns are reentrant: each time a tool is invoked, it opens the client, runs the MCP call, and releases it, whether or not a connection is already held elsewhere. A single agent run therefore opens one session per tool call and closes it when the call returns, rather than holding a session open across the whole run. This keeps a long-running agent from pinning an idle connection between tool calls, and it is why the tools stay callable after the discovery context exits.

If you want a session held open across several calls, keep the adapter's context open when you call the agent. The reentrant client reuses the existing connection rather than opening a second one.

## Multiple servers

To give one agent tools from several servers, choose `MCPConfig` when a single aggregate connection is enough, or `ClientGroup` when each server needs its own connection (different [protocol eras](#protocol-eras), [per-server authentication](/oss/langchain/mcp/auth#per-server-authentication), or a [shared pool](#shared-connection-pool) configured per client).

### One aggregate connection with `MCPConfig`

Give the adapter an `MCPConfig` dict to connect to several servers behind one aggregate endpoint. FastMCP prefixes every tool with its config key, so two servers exposing the same tool name stay distinguishable in the list handed to a model:

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

CONFIG = {
    "mcpServers": {
        "weather": {"command": "python", "args": ["/path/to/weather_server.py"]},
        "calc": {"command": "python", "args": ["/path/to/calc_server.py"]},
    }
}

async def fleet_agent(config):
    async with MCPAdapter(config) as adapter:
        # Every tool is prefixed with its config key (`weather_...`, `calc_...`),
        # so two servers exposing the same tool name stay distinguishable.
        tools = await adapter.list_tools()
        return create_agent("claude-sonnet-5", tools)
```

- [View example trace](https://smith.langchain.com/public/36cdd94e-7f37-4681-afe1-dbc15b85c239/r)

  Open a public LangSmith run for this example.

Each backend is addressed independently, so a fleet can mix transports: one server over stdio, another over HTTP. An `MCPConfig` fleet shares a single negotiated [protocol era](#protocol-eras) across every backend, though: add a legacy-only server and the whole fleet drops to the legacy era.

### Independent connections with `ClientGroup`

To keep each server on its own connection, pass a [`ClientGroup`](https://gofastmcp.com/clients/client-groups). Each member keeps its own negotiated protocol era, authentication, and handlers, and the group routes each call back to the client that advertised the tool. This is what lets a legacy and a modern server run side by side, and it namespaces tools the same way so identical tool names across servers never collide:

```python
from fastmcp.client import Client
from fastmcp.client.group import ClientGroup
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

async def agent_from_group(legacy_url: str, modern_url: str):
    # One connection per server: a `ClientGroup` keeps each server on its own
    # negotiated protocol era, so a legacy and a modern server run side by side.
    # It also namespaces every tool as `{server}_{tool}`, so two servers exposing
    # the same tool name stay distinct.
    group = ClientGroup(
        {
            "weather": Client(legacy_url, mode="legacy"),
            "calc": Client(modern_url, mode="auto"),
        }
    )
    async with MCPAdapter(group) as adapter:
        tools = await adapter.list_tools()
        return create_agent("claude-sonnet-5", tools)
```

- [View example trace](https://smith.langchain.com/public/e7804f49-ac87-4afb-8c19-691900f65c7d/r)

  Open a public LangSmith run for this example.

## Scale a deployment

A deployment that serves many runs should discover per run but reuse its connections underneath, rather than reconnecting on every request. Build the agent inside a [`langgraph dev`](/oss/langgraph/local-server) graph factory so each run picks up the current tool catalog, and let a [shared connection pool](#shared-connection-pool) and [response cache](#caching) absorb the cost:

```python
SERVERS = {
    "weather": "http://localhost:8001/mcp",
    "calc": "http://localhost:8002/mcp",
}

async def make_graph():
    """Build an agent over an MCP fleet. Called once per run by `langgraph dev`."""
    config = {"mcpServers": {name: {"url": url} for name, url in SERVERS.items()}}
    # A long-lived deployment discovers per run, but reuses one HTTP connection
    # pool underneath. `cache_mode="use"` serves a cached tool list within the
    # server's TTL instead of re-listing on every run.
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools(cache_mode="use")
        return create_agent("claude-sonnet-5", tools)
```

**Note:**

In a `langgraph dev` graph factory, the annotated parameter types and the return type must be importable at runtime, not only under `TYPE_CHECKING`. `langgraph-api` classifies the factory with `typing.get_type_hints()`; if an annotation cannot resolve, it injects a config dict instead of the runtime.

For a fully worked deployment example, including per-user authentication that mints a token for each caller, see [Authentication](/oss/langchain/mcp/auth#per-user-authentication).

### Shared connection pool

By default each FastMCP client manages its own HTTP connections. Across a fleet of servers, or many concurrent runs, that means many independent pools. To share one pool, pass an `httpx_client_factory` that draws from a single transport, and lend it out without letting any one client close it:

```python
import httpx2
from fastmcp.client import Client
from fastmcp.client.group import ClientGroup
from fastmcp.client.transports import StreamableHttpTransport
from langchain.mcp import MCPAdapter

# One connection pool, shared by every server the deployment talks to.
_POOL = httpx2.AsyncHTTPTransport()

class _SharedPool(httpx2.AsyncBaseTransport):
    """Lend `_POOL` to each client without letting any client close it."""

handle_async_request = _POOL.handle_async_request

async def aclose(self) -> None: ...

def _client_factory(**kwargs: object) -> httpx2.AsyncClient:
    return httpx2.AsyncClient(transport=_SharedPool(), **kwargs)

async def load_over_shared_pool(servers: dict[str, str]) -> list:
    # Every client draws HTTP connections from the same pool, so a fleet of
    # servers does not each open its own.
    group = ClientGroup(
        {
            name: Client(
                StreamableHttpTransport(url, httpx_client_factory=_client_factory)
            )
            for name, url in servers.items()
        }
    )
    async with MCPAdapter(group) as adapter:
        return await adapter.list_tools()
```

- [View example trace](https://smith.langchain.com/public/a3c3bb95-25d4-4a2e-bf3a-41e87f3b788d/r)

  Open a public LangSmith run for this example.

Because every client borrows from `_POOL`, the deployment opens one set of HTTP connections for the whole fleet rather than one per server.

## Caching

FastMCP can cache the result of `list_tools` so repeated discovery avoids a network round trip. Caching is opt-in and honors the server's own cache hints, so it only takes effect against modern-era servers that advertise them.

`list_tools()` accepts a `cache_mode` that selects how discovery reads a configured cache:

- **`use`** (the default): serve a cached tool list when one is present and still within the server's TTL hint, otherwise fetch and store.
- **`refresh`**: fetch a fresh list from the server and repopulate the cache.
- **`bypass`**: skip the cache entirely.

```python
tools = await adapter.list_tools(cache_mode="refresh")
```

The cache and its per-principal isolation are configured on the client itself, with `Client(cache=...)`. For a shared store across a fleet of replicas, or partitioning cached responses per user, see [Response caching](https://gofastmcp.com/clients/client#response-caching) in the FastMCP documentation.

## Protocol eras

MCP changed how a client and server agree on what each supports. The **legacy** era begins every connection with an `initialize` handshake; the **modern** era (protocol version `2026-07-28` and later) discovers support by probing the server's `server/discover` endpoint. FastMCP negotiates the era per connection, so nothing on the LangChain side has to know which a given server speaks.

To hold tools from servers on different eras in one agent, give each its own connection so it keeps the best era its server supports, either through a [`ClientGroup`](#independent-connections-with-clientgroup) or one adapter per server. A prebuilt `fastmcp.Client` selects the era with its `mode` parameter:

```python
from fastmcp.client import Client

async def agent_across_eras(legacy_target, modern_target):
    # MCP has two protocol eras. FastMCP negotiates per connection, so a
    # separate adapter per server lets each keep the best era its own server
    # supports. `mode="legacy"` pins the handshake era; `mode="auto"` (the
    # default) negotiates the newest the server understands.
    legacy = Client(legacy_target, mode="legacy")
    modern = Client(modern_target, mode="auto")
    async with (
        MCPAdapter(legacy) as legacy_adapter,
        MCPAdapter(modern) as modern_adapter,
    ):
        tools = await legacy_adapter.list_tools() + await modern_adapter.list_tools()
        return create_agent("claude-sonnet-5", tools)
```

Passing both servers as a single `MCPConfig` fleet instead would negotiate one era for everything the fleet holds, dropping every server to the oldest era any member requires.

For the full negotiation rules, see [Protocol negotiation](https://gofastmcp.com/clients/client#protocol-negotiation) in the FastMCP documentation.

## See also

- [Authentication](/oss/langchain/mcp/auth): Bearer, OAuth, and per-user credentials.

- [Deploy a LangGraph server](/oss/langgraph/local-server): Graph factories for long-lived deployments.
- [FastMCP connection lifecycle](https://gofastmcp.com/clients/client#connection-lifecycle)
- [MCP configuration format](https://gofastmcp.com/integrations/mcp-json-configuration)

---

# Model Context Protocol (MCP)
> 출처: data/raw/langchain/mcp/index.mdx | https://docs.langchain.com/oss/python/langchain/mcp

Connect LangChain agents to MCP servers with MCPAdapter.

[Model Context Protocol (MCP)](https://modelcontextprotocol.io) is an open protocol that standardizes how applications provide tools and context to language models. LangChain agents call tools defined on MCP servers through `MCPAdapter`, which discovers a server's tools and adapts them into LangChain tools you can pass straight to `create_agent`.

`MCPAdapter` is built on [FastMCP](https://gofastmcp.com), which handles transport inference, protocol negotiation, connection management, and authentication. This section covers the LangChain-specific layer and links out to the FastMCP client documentation for the connection details underneath.

**Note:**

The `langchain.mcp` namespace requires `langchain[mcp]>=1.4.0` and is in beta. Importing from it raises a `LangChainBetaWarning` once per process. The API may change.

If you used MCP before v1.4.0, see [Migrate from `langchain-mcp-adapters`](/oss/migrate/langchain-mcp-adapters).

## Install

Install LangChain with the `mcp` extra, which pulls in FastMCP:

```bash pip
pip install "langchain[mcp]"
```

```bash uv
uv add "langchain[mcp]"
```

## Quickstart

Open an `MCPAdapter`, discover the server's tools with `list_tools()`, and build the agent inside the context. The tools hold the client, so the agent stays usable after the context exits:

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

async def main():
    async with MCPAdapter("https://example.com/mcp") as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        return await agent.ainvoke({"messages": [{"role": "user", "content": "..."}]})
```

- [View example trace](https://smith.langchain.com/public/dbd2bd37-78e9-48ac-8d8a-ae052e8462ca/r)

  Open a public LangSmith run for this example.

**LangChain docs MCP server**

The [LangChain docs MCP server](/use-these-docs) is a public HTTP endpoint at `https://docs.langchain.com/mcp`.

Connect an agent to it to search and read documentation without writing custom tools:

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

async def main():
    async with MCPAdapter("https://docs.langchain.com/mcp") as adapter:  # [!code highlight]
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        return await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "How do I add short-term memory to a LangChain agent?",
                    }
                ]
            }
        )
```

**Note:**

The docs MCP server is public and does not require an API key. For IDE and coding-agent setup (Claude Code, Cursor, and others), see [Use docs programmatically](/use-these-docs).

The server exposes these tools:

| Tool | Description |
|------|-------------|
| `search_docs_by_lang_chain` | Search docs for relevant guides, how-tos, and examples. |
| `query_docs_filesystem_docs_by_lang_chain` | Read or search docs through a virtual filesystem (`rg`, `head`, `cat`, and related commands). |
| `submit_feedback` | Report a problem with a documentation page. |

## Transports

`MCPAdapter` infers the transport from the target you provide. The target is the only difference between an in-process server, a local script over stdio, and a remote URL:

```python
from pathlib import Path

from langchain.mcp import MCPAdapter

# An in-process FastMCP server: no subprocess, no socket. Ideal for tests.
in_memory = MCPAdapter(server)  # a FastMCP instance

# A script path is launched over stdio, one subprocess per adapter.
stdio = MCPAdapter(Path("weather_server.py"))

# A string must be an http(s) URL, reached over streamable HTTP.
http = MCPAdapter("https://example.com/mcp")
```

A target can be any of the following:

- **An `http`/`https` URL** (`str`): reached over Streamable HTTP.
- **A script path** (`Path`): launched as a subprocess over stdio.
- **A transport object** (`StreamableTransport`): a preconfigured transport object. See [Client Transports](https://gofastmcp.com/clients/transports).
- **An in-process `FastMCP` server**: connected in memory, without a subprocess or socket.
- **An `MCPConfig` dict** (`{"mcpServers": {...}}`): several servers behind one adapter. See [Connections](/oss/langchain/mcp/connections#multiple-servers).
- **A prebuilt `fastmcp.Client`**: for full control over transport, [caching](https://gofastmcp.com/clients/client#response-caching), and [protocol negotiation](https://gofastmcp.com/clients/client#protocol-negotiation).

**Warning:**

A `str` target must be an `http` or `https` URL. FastMCP resolves a string by testing it as a filesystem path before testing it as a URL, so a string naming an existing `.py` or `.js` file would launch that file as a subprocess. Because strings are the form a target most often arrives in from configuration or from a model, `MCPAdapter` rejects strings that do not match the shape of a URL.

## Next steps

- [Tools](/oss/langchain/mcp/tools)

    Load MCP tools into agents, control their execution, and handle their outputs.

- [Connections](/oss/langchain/mcp/connections)

    Connection lifecycle, multiple servers, protocol eras, and caching.

- [Authentication](/oss/langchain/mcp/auth)

    Bearer tokens, OAuth 2.1, and per-user server auth.

---

# Tools
> 출처: data/raw/langchain/mcp/tools.mdx | https://docs.langchain.com/oss/python/langchain/mcp/tools

Load MCP tools into LangChain agents, control their execution, and handle server results and requests.

**Note:**

The `langchain.mcp` namespace requires `langchain[mcp]>=1.4.0` and is in beta. The API may change.

`MCPAdapter` bridges MCP servers and LangChain agents: it discovers the tools a server advertises and adapts them into standard LangChain tools. Pass the tools from `list_tools()` to `create_agent` as you would any other LangChain tool.

This page covers what is specific to that bridge: identifying MCP tools, controlling their execution, handling their outputs, and responding when a server needs input during a call. For the runnable discovery-and-agent example, see the [MCP quickstart](/oss/langchain/mcp).

## Use MCP tools in an agent

Discover the server's catalog with `MCPAdapter.list_tools`, then give the returned tools to `create_agent`. From the agent's perspective, they behave like LangChain tools: the model chooses a tool, LangChain invokes it, and the resulting `ToolMessage` returns to the model.

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

async def run_agent(server) -> dict:
    # Discover the server's tools, then hand them to the agent like any other
    # LangChain tools. The tools hold the client, so the agent stays usable
    # for the life of the adapter context.
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        return await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": "What is the forecast for Oslo?"}
                ]
            }
        )
```

- [View example trace](https://smith.langchain.com/public/025418ad-e7bc-43a3-b700-d1a78b3a4856/r)

  Open a public LangSmith run for this example.

For general guidance on defining, binding, and using LangChain tools, see [Tools](/oss/langchain/tools). For several MCP servers and their namespaced tool catalogs, see [Connections](/oss/langchain/mcp/connections#multiple-servers).

## Handle tool outputs

MCP tool results become `ToolMessage` objects with content the model can read, an artifact for application data, and a status indicating success or failure.

### Multimodal content

The adapter converts model-visible MCP content into LangChain [content blocks](/oss/langchain/messages#standard-content-blocks). For example, a tool that returns an MCP image block with a screenshot reaches the model as an `image` block.

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain.messages import ToolMessage

async def access_multimodal_tool_content(server) -> dict:
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Take a screenshot."}]}
        )

# An MCP result arrives as LangChain content blocks. Image and file content
# convert into standardized `image`/`file` blocks alongside `text`.
for message in result["messages"]:
    if not isinstance(message, ToolMessage):
        continue
    for block in message.content_blocks:  # [!code highlight]
        if block["type"] == "text":  # [!code highlight]
            print(f"Text: {block['text']}")  # [!code highlight]
        elif block["type"] == "image":  # [!code highlight]
            preview = block.get("base64", "")[:20]  # [!code highlight]
            print(f"Image mime type: {block.get('mime_type')}")  # [!code highlight]
            print(f"Image base64: {preview}...")  # [!code highlight]

    return result
```

- [View example trace](https://smith.langchain.com/public/b0c37c50-18d9-43d8-91fb-b933c920ebd7/r)

  Open a public LangSmith run for this example.

### Structured content

When a tool returns structured content, the adapter attaches it to the `ToolMessage` as an artifact rather than folding it into the model-visible text. Run the agent, then read the `artifact` from the `ToolMessage` instances in the result:

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain.messages import ToolMessage

async def run_agent_structured(server) -> dict:
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Look up user 42."}]}
        )

# The adapter sets `artifact` only when the tool returned structured
# content, so a non-None artifact always carries `structured_content`.
for message in result["messages"]:
    if isinstance(message, ToolMessage) and message.artifact is not None:
        structured = message.artifact["structured_content"]  # [!code highlight]
        print(f"Structured content: {structured}")  # [!code highlight]

    return result
```

- [View example trace](https://smith.langchain.com/public/52189bcc-6bd4-4d88-b8da-e5cf72a4849c/r)

  Open a public LangSmith run for this example.

The artifact is an `MCPToolArtifact`, whose `structured_content` field holds the tool result's `structuredContent`. A tool that returns no structured content leaves `artifact` as `None`.

### Errors

An MCP tool result carries an `isError` flag. When a server reports `isError=True`, the adapter converts it into a `ToolMessage` with `status="error"` carrying the server's own message, so the agent can read it and correct itself:

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain.messages import ToolMessage

async def divide_by_zero(server) -> dict:
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Use the divide tool to calculate 10 divided by 0.",
                    }
                ]
            }
        )

# A server error (isError=True) reaches the model as a failed ToolMessage,
# so the agent can read the server's own message and recover. Transport
# failures still raise, because a model cannot act on those.
for message in result["messages"]:
    if isinstance(message, ToolMessage) and message.status == "error":
        print(f"Tool reported: {message.text}")  # [!code highlight]

    return result
```

A server-reported error reaches the model as a failed tool message, but a transport or session failure raises instead.

## Tool metadata

Each adapted tool may carry its MCP provenance under an `mcp` namespace on the LangChain tool's metadata:

```python
tool.metadata
# {
#     "mcp": {
#         "tool": {
#             "annotations": {
#                 "destructive_hint": True,
#                 "read_only_hint": False,
#             },
#             "_meta": {"origin": "crm"},
#         },
#         "server": {
#             "name": "crm",
#             "version": "2.1.0",
#         },
#     },
# }
```

Every nested field is optional: a server may provide tool annotations, `_meta`, server identity, any combination of those, or none. `annotations` contains MCP hints such as `read_only_hint` and `destructive_hint`; `_meta` is opaque metadata supplied by the server; and `server` identifies the MCP implementation that advertised the tool.

Read optional metadata defensively, so a missing field returns a default rather than failing:

```python
from langchain.tools import BaseTool

def is_destructive(tool: BaseTool) -> bool:
    """Read the MCP destructive hint off the adapter's tool metadata."""
    # Chain `.get` with defaults so a tool missing any nested field returns
    # False rather than raising.
    annotations = (
        (tool.metadata or {}).get("mcp", {}).get("tool", {}).get("annotations", {})
    )
    return annotations.get("destructive_hint", False)
```

## Human-in-the-loop

Reading annotations lets you gate a tool based on what the server declares about it, rather than hardcoding tool names. The MCP annotation classifies the tool and LangChain's human-in-the-loop middleware enforces the approval policy.

Read the destructive hint from metadata once during tool discovery. Then give the human-in-the-loop configuration a `when` predicate that receives each pending tool call and returns whether the call needs approval:

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents.middleware.human_in_the_loop import InterruptOnConfig
from langchain.tools import BaseTool
from langchain.tools.tool_node import ToolCallRequest

def is_destructive(tool: BaseTool) -> bool:
    """Read the MCP destructive hint off the adapter's tool metadata."""
    annotations = (
        (tool.metadata or {}).get("mcp", {}).get("tool", {}).get("annotations", {})
    )
    return annotations.get("destructive_hint", False)

async def gate_destructive_tools(server):
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()

# Read the destructive hint from metadata once, then let a callable
# decide per call. One config covers whatever destructive tools a
# server exposes, without hardcoding tool names.
destructive = {tool.name for tool in tools if is_destructive(tool)}

def needs_approval(request: ToolCallRequest) -> bool:
    return request.tool_call["name"] in destructive

        gate = InterruptOnConfig(
            allowed_decisions=["approve", "reject"], when=needs_approval
        )
        interrupt_on: dict[str, bool | InterruptOnConfig] = {
            tool.name: gate for tool in tools
        }
        return create_agent(
            "claude-sonnet-5",
            tools,
            middleware=[HumanInTheLoopMiddleware(interrupt_on=interrupt_on)],
            checkpointer=InMemorySaver(),
        )
```

When the agent calls a tool that the predicate gates, the run pauses. Approve the call to run it, or reject it to skip the tool and tell the model:

```python
from langgraph.types import Command

# Approve the pending destructive call and resume.
resumed = await agent.ainvoke(
    Command(resume={"decisions": [{"type": "approve"}]}), config
)
```

The predicate can also inspect the call's arguments. This lets a tool run freely for safe inputs and pause only for risky ones, such as a `delete_file` call targeting a protected path.

Access the arguments through `request.tool_call["args"]`.

Combine the metadata classification and argument check to gate a tool only when its type and inputs warrant approval. For the full approval workflow, see [Human-in-the-loop](/oss/langchain/human-in-the-loop).

## Server requests during tool execution

Most tools finish without asking the client for anything mid-call. When a server needs input, `MCPAdapter` surfaces [elicitation](https://modelcontextprotocol.io/specification/draft/client/elicitation) as a LangGraph `interrupt`.

### Elicitation

[Elicitation](https://modelcontextprotocol.io/specification/draft/client/elicitation) lets an MCP server request input during a tool call. The adapter pauses the run with a LangGraph interrupt. Your application presents the request to the user and resumes the run with their answer.

Attach a [checkpointer](/oss/langchain/short-term-memory) to the agent and use the same `thread_id` when invoking and resuming it.

This example assumes the booking tool asks for one date and pauses once. Replace the sample date with the user's answer.

```python
from typing import Any

from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

async def book_with_elicitation(server) -> dict:
    # Elicitation is handled automatically: when a server needs input mid-call,
    # the adapter surfaces the question as a LangGraph `interrupt()`, so the
    # person already reviewing the agent's work answers it and the run resumes.
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()

# Resuming a paused run needs persistence, so the interrupted run has
# somewhere to wait.
agent = create_agent("claude-sonnet-5", tools, checkpointer=InMemorySaver())
config: Any = {"configurable": {"thread_id": "booking-1"}}

paused = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "Book a table for 4."}]}, config
)
[interrupt] = paused["__interrupt__"]
[question] = interrupt.value["requests"]

        # Answers are keyed by the server's own request key, so nothing has to
        # be tracked across the pause. `decline` or `cancel` would refuse.
        answer = {"action": "accept", "content": {"date": "2026-09-14"}}
        return await agent.ainvoke(
            Command(resume={"responses": {question["key"]: answer}}), config
        )
```

Elicitation is on by default. The adapter advertises the capability and drives the interrupt loop. A prebuilt client that already carries its own elicitation handler is honored instead of overridden.

Resume with `Command(resume={"responses": {key: answer}})`. The interrupt payload and answer types live in `langchain.mcp.elicitation`.

**Note:**

Resuming reruns the tool from the beginning. Any work performed before the server asks for input can repeat. Make that work safe to repeat without duplicating side effects.

Each answer uses one of these actions:

- **`accept`**: Provide form `content` matching the request's schema, or confirm completion of a URL interaction without `content`.
- **`decline`**: Refuse to provide the requested information.
- **`cancel`**: Indicate that the user canceled the interaction.

The adapter forwards the answer to the server, which decides how the tool call finishes.

Only elicitation is answered this way. A server that instead asks for [sampling](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling) or [roots](https://modelcontextprotocol.io/specification/2025-06-18/client/roots) raises an error, because the modern, sessionless protocol has no live back-channel for those requests. See [Sampling and roots](/oss/migrate/langchain-mcp-adapters#sampling-and-roots).

**Note:**

Interrupt-driven elicitation answers a server that returns its request as an `InputRequiredResult`. A server that only pushes elicitation over a legacy handshake session cannot be answered this way.

## See also

- [Content blocks](/oss/langchain/messages#standard-content-blocks)
- [Tools](/oss/langchain/tools)
- [Human-in-the-loop](/oss/langchain/human-in-the-loop)

- [FastMCP calling tools](https://gofastmcp.com/clients/tools)
- [FastMCP client elicitation](https://gofastmcp.com/clients/elicitation)
- [FastMCP server elicitation](https://gofastmcp.com/servers/elicitation)

- [MCP elicitation specification](https://modelcontextprotocol.io/specification/draft/client/elicitation)
- [MCP tool annotations](https://modelcontextprotocol.io/specification/draft/server/tools)

---

# Messages
> 출처: data/raw/langchain/messages.mdx | https://docs.langchain.com/oss/python/langchain/messages

Messages are the fundamental unit of context for models in LangChain. They represent the input and output of models, carrying both the content and metadata needed to represent the state of a conversation when interacting with an LLM.

Messages are objects that contain:

* 

 [**Role**](#message-types) - Identifies the message type (e.g. `system`, `user`)
* 

 [**Content**](#message-content) - Represents the actual content of the message (like text, images, audio, documents, etc.)
* 

 [**Metadata**](#message-metadata) - Optional fields such as response information, message IDs, and token usage

LangChain provides a standard message type that works across all model providers, ensuring consistent behavior regardless of the model being called.

## Basic usage

The simplest way to use messages is to create message objects and pass them to a model when [invoking](/oss/langchain/models#invocation).

```python
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

model = init_chat_model("gpt-5-nano")

system_msg = SystemMessage("You are a helpful assistant.")
human_msg = HumanMessage("Hello, how are you?")

# Use with chat models
messages = [system_msg, human_msg]
response = model.invoke(messages)  # Returns AIMessage
```

**Tip:**

Multi-turn [agents](/oss/langchain/agents) accumulate long message histories. [LangSmith](/langsmith/observability) records each turn, tool result, and model response so you can inspect the full conversation. Follow the [tracing quickstart](/langsmith/trace-with-langchain) to enable tracing.

We recommend you also set up [LangSmith Engine](/langsmith/engine) which monitors your traces, detects issues, and proposes fixes.

### Text prompts

Text prompts are strings - ideal for straightforward generation tasks where you don't need to retain conversation history.

```python
response = model.invoke("Write a haiku about spring")
```

**Use text prompts when:**
* You have a single, standalone request
* You don't need conversation history
* You want minimal code complexity

### Message prompts

Alternatively, you can pass in a list of messages to the model by providing a list of message objects.

```python
from langchain.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage("You are a poetry expert"),
    HumanMessage("Write a haiku about spring"),
    AIMessage("Cherry blossoms bloom...")
]
response = model.invoke(messages)
```

**Use message prompts when:**
* Managing multi-turn conversations
* Working with multimodal content (images, audio, files)
* Including system instructions

### Dictionary format

You can also specify messages directly in OpenAI chat completions format.

```python
messages = [
    {"role": "system", "content": "You are a poetry expert"},
    {"role": "user", "content": "Write a haiku about spring"},
    {"role": "assistant", "content": "Cherry blossoms bloom..."}
]
response = model.invoke(messages)
```

## Message types

- 

 [System message](#system-message) - Tells the model how to behave and provide context for interactions
- 

 [Human message](#human-message) - Represents user input and interactions with the model
- 

 [AI message](#ai-message) - Responses generated by the model, including text content, tool calls, and metadata
- 

 [Tool message](#tool-message) - Represents the outputs of [tool calls](/oss/langchain/models#tool-calling)

### System message

A `SystemMessage` represent an initial set of instructions that primes the model's behavior. You can use a system message to set the tone, define the model's role, and establish guidelines for responses.

```python Basic instructions
system_msg = SystemMessage("You are a helpful coding assistant.")

messages = [
    system_msg,
    HumanMessage("How do I create a REST API?")
]
response = model.invoke(messages)
```

```python Detailed persona
from langchain.messages import SystemMessage, HumanMessage

system_msg = SystemMessage("""
You are a senior Python developer with expertise in web frameworks.
Always provide code examples and explain your reasoning.
Be concise but thorough in your explanations.
""")

messages = [
    system_msg,
    HumanMessage("How do I create a REST API?")
]
response = model.invoke(messages)
```

---

### Human message

A `HumanMessage` represents user input and interactions. They can contain text, images, audio, files, and any other amount of multimodal [content](#message-content).

#### Text content

```python Message object
response = model.invoke([
  HumanMessage("What is machine learning?")
])
```

```python String shortcut
# Using a string is a shortcut for a single HumanMessage
response = model.invoke("What is machine learning?")
```

#### Message metadata

```python Add metadata
human_msg = HumanMessage(
    content="Hello!",
    name="alice",  # Optional: identify different users
    id="msg_123",  # Optional: unique identifier for tracing
)
```

**Note:**

The `name` field behavior varies by provider—some use it for user identification, others ignore it. To check, refer to the model provider's [reference](https://reference.langchain.com/python/integrations/).

---

### AI message

An `AIMessage` represents the output of a model invocation. They can include multimodal data, tool calls, and provider-specific metadata that you can later access.

```python
response = model.invoke("Explain AI")
print(type(response))  # <class 'langchain.messages.AIMessage'>
```

`AIMessage` objects are returned by the model when calling it, which contains all of the associated metadata in the response.

Providers weigh/contextualize types of messages differently, which means it is sometimes helpful to manually create a new `AIMessage` object and insert it into the message history as if it came from the model.

```python
from langchain.messages import AIMessage, SystemMessage, HumanMessage

# Create an AI message manually (e.g., for conversation history)
ai_msg = AIMessage("I'd be happy to help you with that question!")

# Add to conversation history
messages = [
    SystemMessage("You are a helpful assistant"),
    HumanMessage("Can you help me?"),
    ai_msg,  # Insert as if it came from the model
    HumanMessage("Great! What's 2+2?")
]

response = model.invoke(messages)
```

**Attributes**

The text content of the message.

The raw content of the message.

The standardized [content blocks](#message-content) of the message.

The tool calls made by the model.

Empty if no tools are called.

A unique identifier for the message (either automatically generated by LangChain or returned in the provider response)

The usage metadata of the message, which can contain token counts when available.

The response metadata of the message.

#### Tool calls

When models make [tool calls](/oss/langchain/models#tool-calling), they're included in the `AIMessage`:

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5-nano")

def get_weather(location: str) -> str:
    """Get the weather at a location."""
    ...

model_with_tools = model.bind_tools([get_weather])
response = model_with_tools.invoke("What's the weather in Paris?")

for tool_call in response.tool_calls:
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")
    print(f"ID: {tool_call['id']}")
```

Other structured data, such as reasoning or citations, can also appear in message [content](/oss/langchain/messages#message-content).

#### Token usage

An `AIMessage` can hold token counts and other usage metadata in its `usage_metadata` field:

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5-nano")

response = model.invoke("Hello!")
response.usage_metadata
```

```
{'input_tokens': 8,
 'output_tokens': 304,
 'total_tokens': 312,
 'input_token_details': {'audio': 0, 'cache_read': 0},
 'output_token_details': {'audio': 0, 'reasoning': 256}}
```

See `UsageMetadata` for details.

#### Streaming and chunks

During streaming, you'll receive `AIMessageChunk` objects that can be combined into a full message object:

```python
chunks = []
full_message = None
for chunk in model.stream("Hi"):
    chunks.append(chunk)
    print(chunk.text)
    full_message = chunk if full_message is None else full_message + chunk
```

**Note:**

Learn more:
- [Streaming tokens from chat models](/oss/langchain/models#stream)
- [Streaming tokens and/or steps from agents](/oss/langchain/streaming)

---

### Tool message

For models that support [tool calling](/oss/langchain/models#tool-calling), AI messages can contain tool calls. Tool messages are used to pass the results of a single tool execution back to the model.

[Tools](/oss/langchain/tools) can generate `ToolMessage` objects directly. Below, we show a simple example. Read more in the [tools guide](/oss/langchain/tools).

```python
from langchain.messages import AIMessage
from langchain.messages import ToolMessage

# After a model makes a tool call
# (Here, we demonstrate manually creating the messages for brevity)
ai_message = AIMessage(
    content=[],
    tool_calls=[{
        "name": "get_weather",
        "args": {"location": "San Francisco"},
        "id": "call_123"
    }]
)

# Execute tool and create result message
weather_result = "Sunny, 72°F"
tool_message = ToolMessage(
    content=weather_result,
    tool_call_id="call_123"  # Must match the call ID
)

# Continue conversation
messages = [
    HumanMessage("What's the weather in San Francisco?"),
    ai_message,  # Model's tool call
    tool_message,  # Tool execution result
]
response = model.invoke(messages)  # Model processes the result
```

**Attributes**

The stringified output of the tool call.

The ID of the tool call that this message is responding to. Must match the ID of the tool call in the `AIMessage`.

The name of the tool that was called.

Additional data not sent to the model but can be accessed programmatically.

**Note:**

The `artifact` field stores supplementary data that won't be sent to the model but can be accessed programmatically. This is useful for storing raw results, debugging information, or data for downstream processing without cluttering the model's context.

**Example: Using artifact for retrieval metadata**

For example, a [retrieval](/oss/deepagents/retrieval) tool could retrieve a passage from a document for reference by a model. Where message `content` contains text that the model will reference, an `artifact` can contain document identifiers or other metadata that an application can use (e.g., to render a page). See example below:

```python
from langchain.messages import ToolMessage

# Sent to model
message_content = "It was the best of times, it was the worst of times."

# Artifact available downstream
artifact = {"document_id": "doc_123", "page": 0}

tool_message = ToolMessage(
    content=message_content,
    tool_call_id="call_123",
    name="search_books",
    artifact=artifact,
)
```

See the [RAG tutorial](/oss/deepagents/rag) for an end-to-end example of building retrieval [agents](/oss/langchain/agents) with LangChain.

---

## Message content

You can think of a message's content as the payload of data that gets sent to the model. Messages have a `content` attribute that is loosely-typed, supporting strings and lists of untyped objects (e.g., dictionaries). This allows support for provider-native structures directly in LangChain chat models, such as [multimodal](#multimodal) content and other data.

Separately, LangChain provides dedicated content types for text, reasoning, citations, multi-modal data, server-side tool calls, and other message content. See [content blocks](#standard-content-blocks) below.

LangChain chat models accept message content in the `content` attribute.

This may contain either:

1. A string
2. A list of content blocks in a provider-native format
3. A list of [LangChain's standard content blocks](#standard-content-blocks)

See below for an example using [multimodal](#multimodal) inputs:

```python
from langchain.messages import HumanMessage

# String content
human_message = HumanMessage("Hello, how are you?")

# Provider-native format (e.g., OpenAI)
human_message = HumanMessage(content=[
    {"type": "text", "text": "Hello, how are you?"},
    {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
])

# List of standard content blocks
human_message = HumanMessage(content_blocks=[
    {"type": "text", "text": "Hello, how are you?"},
    {"type": "image", "url": "https://example.com/image.jpg"},
])
```

**Tip:**

Specifying `content_blocks` when initializing a message will still populate message
`content`, but provides a type-safe interface for doing so.

### Standard content blocks

LangChain provides a standard representation for message content that works across providers.

Message objects implement a `content_blocks` property that will lazily parse the `content` attribute into a standard, type-safe representation. For example, messages generated from [`ChatAnthropic`](/oss/integrations/chat/anthropic) or [`ChatOpenAI`](/oss/integrations/chat/openai) will include `thinking` or `reasoning` blocks in the format of the respective provider, but can be lazily parsed into a consistent [`ReasoningContentBlock`](#content-block-reference) representation:

**Anthropic**

```python
from langchain.messages import AIMessage

message = AIMessage(
    content=[
        {"type": "thinking", "thinking": "...", "signature": "WaUjzkyp..."},
        {"type": "text", "text": "..."},
    ],
    response_metadata={"model_provider": "anthropic"}
)
message.content_blocks
```
```
[{'type': 'reasoning',
  'reasoning': '...',
  'extras': {'signature': 'WaUjzkyp...'}},
 {'type': 'text', 'text': '...'}]
```

**OpenAI**

```python
from langchain.messages import AIMessage

message = AIMessage(
    content=[
        {
            "type": "reasoning",
            "id": "rs_abc123",
            "summary": [
                {"type": "summary_text", "text": "summary 1"},
                {"type": "summary_text", "text": "summary 2"},
            ],
        },
        {"type": "text", "text": "...", "id": "msg_abc123"},
    ],
    response_metadata={"model_provider": "openai"}
)
message.content_blocks
```
```
[{'type': 'reasoning', 'id': 'rs_abc123', 'reasoning': 'summary 1'},
 {'type': 'reasoning', 'id': 'rs_abc123', 'reasoning': 'summary 2'},
 {'type': 'text', 'text': '...', 'id': 'msg_abc123'}]
```

See the [integrations guides](/oss/integrations/providers/overview) to get started with the
inference provider of your choice.

**Note:**

**Serializing standard content**

If an application outside of LangChain needs access to the standard content block
representation, you can opt-in to storing content blocks in message content.

To do this, you can set the `LC_OUTPUT_VERSION` environment variable to `v1`. Or,
initialize any chat model with `output_version="v1"`:

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5-nano", output_version="v1")
```

### Multimodal

**Multimodality** refers to the ability to work with data that comes in different
forms, such as text, audio, images, and video. LangChain includes standard types
for these data that can be used across providers.

[Chat models](/oss/langchain/models) can accept multimodal data as input and generate
it as output. Below we show short examples of input messages featuring multimodal data.

**Note:**

Extra keys can be included top-level in the content block or nested in `"extras": {"key": value}`.

[OpenAI](/oss/integrations/chat/openai),
for example, requires a filename for PDFs. See the [provider page](/oss/integrations/providers/overview)
for your chosen model for specifics.

```python Image input
# From URL
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this image."},
        {"type": "image", "url": "https://example.com/path/to/image.jpg"},
    ]
}

# From base64 data
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this image."},
        {
            "type": "image",
            "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
            "mime_type": "image/jpeg",
        },
    ]
}

# From provider-managed File ID
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this image."},
        {"type": "image", "file_id": "file-abc123"},
    ]
}
```

```python PDF document input
# From URL
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this document."},
        {"type": "file", "url": "https://example.com/path/to/document.pdf"},
    ]
}

# From base64 data
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this document."},
        {
            "type": "file",
            "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
            "mime_type": "application/pdf",
        },
    ]
}

# From provider-managed File ID
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this document."},
        {"type": "file", "file_id": "file-abc123"},
    ]
}
```

```python Audio input
# From base64 data
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this audio."},
        {
            "type": "audio",
            "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
            "mime_type": "audio/wav",
        },
    ]
}

# From provider-managed File ID
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this audio."},
        {"type": "audio", "file_id": "file-abc123"},
    ]
}
```

```python Video input
# From base64 data
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this video."},
        {
            "type": "video",
            "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
            "mime_type": "video/mp4",
        },
    ]
}

# From provider-managed File ID
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this video."},
        {"type": "video", "file_id": "file-abc123"},
    ]
}
```

**Warning:**

Not all models support all file types. Check the model provider's [reference](https://reference.langchain.com/python/integrations/) for supported formats and size limits.

### Content block reference

Content blocks are represented (either when creating a message or accessing the `content_blocks` property) as a list of typed dictionaries. Each item in the list must adhere to one of the following block types:

**Core**

**TextContentBlock**

**Purpose:** Standard text output

Always `"text"`

The text content

List of annotations for the text

Additional provider-specific data

**Example:**
```python
{
    "type": "text",
    "text": "Hello world",
    "annotations": []
}
```

**ReasoningContentBlock**

**Purpose:** Model reasoning steps

Always `"reasoning"`

The reasoning content

Additional provider-specific data

**Example:**
```python
{
    "type": "reasoning",
    "reasoning": "The user is asking about...",
    "extras": {"signature": "abc123"},
}
```

**Multimodal**

**ImageContentBlock**

**Purpose:** Image data

Always `"image"`

URL pointing to the image location.

Base64-encoded image data.

Unique identifier for this content block (either generated by the provider or by LangChain).

Image [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml#image) (e.g., `image/jpeg`, `image/png`). Required for base64 data.

**AudioContentBlock**

**Purpose:** Audio data

Always `"audio"`

URL pointing to the audio location.

Base64-encoded audio data.

Unique identifier for this content block (either generated by the provider or by LangChain).

Audio [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml#audio) (e.g., `audio/mpeg`, `audio/wav`). Required for base64 data.

**VideoContentBlock**

**Purpose:** Video data

Always `"video"`

URL pointing to the video location.

Base64-encoded video data.

Unique identifier for this content block (either generated by the provider or by LangChain).

Video [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml#video) (e.g., `video/mp4`, `video/webm`). Required for base64 data.

**FileContentBlock**

**Purpose:** Generic files (PDF, etc)

Always `"file"`

URL pointing to the file location.

Base64-encoded file data.

Unique identifier for this content block (either generated by the provider or by LangChain).

File [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml) (e.g., `application/pdf`). Required for base64 data.

**PlainTextContentBlock**

**Purpose:** Document text (`.txt`, `.md`)

Always `"text-plain"`

The text content

[MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml) of the text (e.g., `text/plain`, `text/markdown`)

**Tool Calling**

**ToolCall**

**Purpose:** Function calls

Always `"tool_call"`

Name of the tool to call

Arguments to pass to the tool

Unique identifier for this tool call

**Example:**
```python
{
    "type": "tool_call",
    "name": "search",
    "args": {"query": "weather"},
    "id": "call_123"
}
```

**ToolCallChunk**

**Purpose:** Streaming tool call fragments

Always `"tool_call_chunk"`

Name of the tool being called

Partial tool arguments (may be incomplete JSON)

Tool call identifier

Position of this chunk in the stream

**InvalidToolCall**

**Purpose:** Malformed calls, intended to catch JSON parsing errors.

Always `"invalid_tool_call"`

Name of the tool that failed to be called

Arguments to pass to the tool

Description of what went wrong

**Server-Side Tool Execution**

**ServerToolCall**

**Purpose:** Tool call that is executed server-side.

Always `"server_tool_call"`

An identifier associated with the tool call.

The name of the tool to be called.

Partial tool arguments (may be incomplete JSON)

**ServerToolCallChunk**

**Purpose:** Streaming server-side tool call fragments

Always `"server_tool_call_chunk"`

An identifier associated with the tool call.

Name of the tool being called

Partial tool arguments (may be incomplete JSON)

Position of this chunk in the stream

**ServerToolResult**

**Purpose:** Search results

Always `"server_tool_result"`

Identifier of the corresponding server tool call.

Identifier associated with the server tool result.

Execution status of the server-side tool. `"success"` or `"error"`.

Output of the executed tool.

**Provider-Specific Blocks**

**NonStandardContentBlock**

**Purpose:** Provider-specific escape hatch

Always `"non_standard"`

Provider-specific data structure

**Usage:** For experimental or provider-unique features

Additional provider-specific content types may be found within the [reference documentation](/oss/integrations/providers/overview) of each model provider.

**Tip:**

View the canonical type definitions in the API reference.

**Info:**

Content blocks were introduced as a new property on messages in LangChain v1 to standardize content formats across providers while maintaining backward compatibility with existing code.

Content blocks are not a replacement for the `content` property, but rather a new property that can be used to access the content of a message in a standardized format.

## Serialization

You can serialize messages to plain objects for storage and deserialize back to message instances. This is useful for persisting conversation history and resuming sessions.

```python
from langchain.messages import HumanMessage
from langchain_core.load import dumpd, load

message = HumanMessage("What is the capital of France?")

# Serialize to a plain dict
serialized = dumpd(message)

# Deserialize back to a message object
restored = load(serialized)
```

- [View example trace](https://smith.langchain.com/public/2a8b01aa-e859-42a3-b658-d991cf6746dd/r)

  Open a public LangSmith run for this example.

**Warning:**

**`load()` instantiates Python objects and can trigger side effects during deserialization. Never call `load()` on data from an untrusted or unauthenticated source.**

## Use with chat models

[Chat models](/oss/langchain/models) accept a sequence of message objects as input and return an `AIMessage` as output. Interactions are often stateless, so that a simple conversational loop involves invoking a model with a growing list of messages.

Refer to the below guides to learn more:

- Built-in features for [persisting and managing conversation histories](/oss/langchain/short-term-memory)
- Strategies for managing context windows, including [trimming and summarizing messages](/oss/langchain/short-term-memory#common-patterns)

---

# Prebuilt middleware
> 출처: data/raw/langchain/middleware/built-in.mdx | https://docs.langchain.com/oss/python/langchain/middleware/built-in

Prebuilt middleware for common agent use cases

LangChain and [Deep Agents](/oss/deepagents/overview) provide prebuilt middleware for common use cases. Each middleware is production-ready and configurable for your specific needs.

## Provider-agnostic middleware

The following middleware work with any LLM provider:

| Middleware | Description |
|------------|-------------|
| [Tool error](#tool-error) | Catch tool execution exceptions and convert them to error messages for the model. |
| [Tool retry](#tool-retry) | Automatically retry failed tool calls with exponential backoff. |
| [Model retry](#model-retry) | Automatically retry failed model calls with exponential backoff. |
| [Model fallback](#model-fallback) | Automatically fallback to alternative models when primary fails. |
| [Summarization](#summarization) | Automatically summarize conversation history when approaching token limits. |
| [Human-in-the-loop](#human-in-the-loop) | Pause execution for human approval of tool calls. |
| [Model call limit](#model-call-limit) | Limit the number of model calls to prevent excessive costs. |
| [Tool call limit](#tool-call-limit) | Control tool execution by limiting call counts. |
| [PII detection](#pii-detection) | Detect and handle Personally Identifiable Information (PII). |
| [To-do list](#to-do-list) | Equip agents with task planning and tracking capabilities. |
| [LLM tool selector](#llm-tool-selector) | Use an LLM to select relevant tools before calling main model. |
| [Provider tool search](#provider-tool-search) | Defer tools behind providers' server-side tool search, surfacing them on demand. |
| [Shell tool](#shell-tool) | Expose a persistent shell session to agents for command execution. |
| [Filesystem](#filesystem-middleware) | Provide agents with a filesystem for storing context and long-term memories. |
| [Subagent](#subagent) | Add the ability to spawn subagents. |
| [Rubric grading (Beta)](#rubric-grading) | Apply LLM-as-a-judge grading so agents self-evaluate and iterate until a rubric is satisfied. |
| [File search](#file-search) | Provide Glob and Grep search tools over filesystem files. |
| [Context editing](#context-editing) | Manage conversation context by trimming or clearing tool uses. |
| [LLM tool emulator](#llm-tool-emulator) | Emulate tool execution using an LLM for testing purposes. |

### Tool error

Catch exceptions raised during tool execution and convert them into error `ToolMessage`s that the model can see and recover from, instead of halting the agent run. Tool error is useful for the following:

- Letting the model retry a failed tool call with corrected arguments.
- Surfacing controlled, sanitized error messages instead of raw exception details.
- Preventing unexpected tool exceptions from crashing the agent.

**Note:**

Tool error middleware does not automatically retry failed calls. For retries, compose with [Tool retry](#tool-retry) middleware placed *inner* (later in the `middleware` list) and configured with `on_failure="error"` so that exceptions reach the tool error middleware. See the [full example](#tool-error-full-example) below.

**API reference:** `ToolErrorMiddleware`

**Note:**

`ToolErrorMiddleware` requires `langchain>=1.3.14`.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ToolErrorMiddleware

def on_error(exc: Exception, request: ToolCallRequest) -> str | None:
    if isinstance(exc, ValueError):
        return f"`{request.tool_call['name']}` failed with {type(exc).__name__}."
    # propagate everything else

agent = create_agent(
    model="gpt-5.5",
    tools=[your_tools],
    middleware=[ToolErrorMiddleware(on_error)],
)
```

**Configuration options**

Sync handler called for each exception raised by tool execution. Return content (a `str` or list of content blocks) to convert the exception into a `ToolMessage(status="error")`. Return `None` or omit a return statement to let the exception propagate. Used on the sync path and, unless `aon_error` is given, on the async path.

Optional async handler, used on the async execution path. Falls back to `on_error` when not provided.

Optional list of tools or tool names to apply error handling to. If `None`, applies to all tools.

**Tool error full example**

The `on_error` handler receives the exception and the `ToolCallRequest` (which includes the tool call dict with name, args, and call ID). Return `None` for exceptions you do not want to handle, and they will propagate normally.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ToolErrorMiddleware, ToolRetryMiddleware

def on_error(exc: Exception, request: ToolCallRequest) -> str | None:
    # Surface ValueError to the model so it can correct the input
    if isinstance(exc, ValueError):
        return f"`{request.tool_call['name']}` failed: {type(exc).__name__}. Fix the input and retry."
    # Let all other exceptions propagate (halts the run)
    return None

# Async-only usage
async def aon_error(exc: Exception, request: ToolCallRequest) -> str | None:
    if isinstance(exc, ConnectionError):
        return f"Tool `{request.tool_call['name']}` encountered a connection error."
    return None

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, database_tool],
    middleware=[
        # Place retry inner so exceptions reach ToolErrorMiddleware after retries are exhausted
        ToolErrorMiddleware(on_error=on_error, tools=["search_tool"]),
        ToolRetryMiddleware(max_retries=3, on_failure="error"),
    ],
)

# Async-only: pass aon_error alone (do not pass on_error)
async_agent = create_agent(
    model="gpt-5.5",
    tools=[api_tool],
    middleware=[ToolErrorMiddleware(aon_error=aon_error)],
)
```

**Note:**

Prefer returning content that names the exception type over the raw exception message, which may carry sensitive or internal detail. The `on_error` handler controls disclosure: the raw exception message is never sent to the model unless you choose to include it.

### Tool retry

Automatically retry failed tool calls with configurable exponential backoff. Tool retry is useful for the following:

- Handling transient failures in external API calls.
- Improving reliability of network-dependent tools.
- Building resilient agents that gracefully handle temporary errors.

**API reference:** `ToolRetryMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, database_tool],
    middleware=[
        ToolRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
        ),
    ],
)
```

**Configuration options**

Maximum number of retry attempts after the initial call (3 total attempts with default)

Optional list of tools or tool names to apply retry logic to. If `None`, applies to all tools.

Either a tuple of exception types to retry on, or a callable that takes an exception and returns `True` if it should be retried. With `langchain>=1.3.16`, the default retries retryable [model errors](/oss/langchain/models#model-exceptions) and all unclassified exceptions, and no longer retries model errors marked non-retryable.

Behavior when all retries are exhausted. Options:
- `'continue'` (default) - Return a `ToolMessage` with error details, allowing the LLM to handle the failure
- `'error'` - Re-raise the exception, stopping agent execution
- Custom callable - Function that takes the exception and returns a string for the `ToolMessage` content

    **Deprecated values:** `'return_message'` (use `'continue'` instead) and `'raise'` (use `'error'` instead).

Multiplier for exponential backoff. Each retry waits `initial_delay * (backoff_factor ** retry_number)` seconds. Set to `0.0` for constant delay.

Initial delay in seconds before first retry

Maximum delay in seconds between retries (caps exponential backoff growth)

Whether to add random jitter (`±25%`) to delay to avoid thundering herd

**Full example**

The middleware automatically retries failed tool calls with exponential backoff.

**Key configuration:**
- `max_retries` - Number of retry attempts (default: 2)
- `backoff_factor` - Multiplier for exponential backoff (default: 2.0)
- `initial_delay` - Starting delay in seconds (default: 1.0)
- `max_delay` - Cap on delay growth (default: 60.0)
- `jitter` - Add random variation (default: True)

**Failure handling:**
- `on_failure='continue'` (default) - Return error message
- `on_failure='error'` - Re-raise exception
- Custom function - Function returning error message

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, database_tool, api_tool],
    middleware=[
        ToolRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
            max_delay=60.0,
            jitter=True,
            tools=["api_tool"],
            retry_on=(ConnectionError, TimeoutError),
            on_failure="continue",
        ),
    ],
)
```

### Model retry

Automatically retry failed model calls with configurable exponential backoff. Model retry is useful for the following:

- Handling transient failures in model API calls.
- Improving reliability of network-dependent model requests.
- Building resilient agents that gracefully handle temporary model errors.

**API reference:** `ModelRetryMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, database_tool],
    middleware=[
        ModelRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
        ),
    ],
)
```

**Configuration options**

Maximum number of retry attempts after the initial call (3 total attempts with default)

Either a tuple of exception types to retry on, or a callable that takes an exception and returns `True` if it should be retried. With `langchain>=1.3.16`, the default retries retryable [model errors](/oss/langchain/models#model-exceptions) and all unclassified exceptions, and no longer retries model errors marked non-retryable.

Behavior when all retries are exhausted. Options:
- `'continue'` (default) - Return an `AIMessage` with error details, allowing the agent to potentially handle the failure gracefully
- `'error'` - Re-raise the exception (stops agent execution)
- Custom callable - Function that takes the exception and returns a string for the `AIMessage` content

    Multiplier for exponential backoff. Each retry waits `initial_delay * (backoff_factor ** retry_number)` seconds. Set to `0.0` for constant delay.

Initial delay in seconds before first retry

Maximum delay in seconds between retries (caps exponential backoff growth)

Whether to add random jitter (`±25%`) to delay to avoid thundering herd

**Full example**

The middleware automatically retries failed model calls with exponential backoff.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware

# Basic usage with default settings (2 retries, exponential backoff)
agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool],
    middleware=[ModelRetryMiddleware()],
)

# Custom exception filtering
class TimeoutError(Exception):
    """Custom exception for timeout errors."""
    pass

class ConnectionError(Exception):
    """Custom exception for connection errors."""
    pass

# Retry specific exceptions only
retry = ModelRetryMiddleware(
    max_retries=4,
    retry_on=(TimeoutError, ConnectionError),
    backoff_factor=1.5,
)

def should_retry(error: Exception) -> bool:
    # Only retry on rate limit errors
    if isinstance(error, TimeoutError):
        return True
    # Or check for specific HTTP status codes
    if hasattr(error, "status_code"):
        return error.status_code in (429, 503)
    return False

retry_with_filter = ModelRetryMiddleware(
    max_retries=3,
    retry_on=should_retry,
)

# Return error message instead of raising
retry_continue = ModelRetryMiddleware(
    max_retries=4,
    on_failure="continue",  # Return AIMessage with error instead of raising
)

# Custom error message formatting
def format_error(error: Exception) -> str:
    return f"Model call failed: {error}. Please try again later."

retry_with_formatter = ModelRetryMiddleware(
    max_retries=4,
    on_failure=format_error,
)

# Constant backoff (no exponential growth)
constant_backoff = ModelRetryMiddleware(
    max_retries=5,
    backoff_factor=0.0,  # No exponential growth
    initial_delay=2.0,  # Always wait 2 seconds
)

# Raise exception on failure
strict_retry = ModelRetryMiddleware(
    max_retries=2,
    on_failure="error",  # Re-raise exception instead of returning message
)
```

### Model fallback

Automatically fallback to alternative models when the primary model fails. Model fallback is useful for the following:

- Building resilient agents that handle model outages.
- Cost optimization by falling back to cheaper models.
- Provider redundancy across OpenAI, Anthropic, etc.

**API reference:** `ModelFallbackMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    middleware=[
        ModelFallbackMiddleware(
            "gpt-5.4-mini",
            "claude-3-5-sonnet-20241022",
        ),
    ],
)
```

**Note:**

Watch this [video guide](https://www.youtube.com/watch?v=8rCRO0DUeIM) demonstrating Model Fallback middleware behavior.

**Configuration options**

First fallback model to try when the primary model fails. Can be a model identifier string (e.g., `'openai:gpt-5.4-mini'`) or a `BaseChatModel` instance.

Additional fallback models to try in order if previous models fail

### Summarization

Automatically summarize conversation history when approaching token limits, preserving recent messages while compressing older context. Summarization is useful for the following:
- Long-running conversations that exceed context windows.
- Multi-turn dialogues with extensive history.
- Applications where preserving full conversation context matters.

**Note:**

Summarization is text-oriented context compression. It does not resize, downsample, or otherwise compress image/audio/video payloads. Recent messages retained by `keep` still include their original multimodal blocks, while older multimodal messages that are summarized are represented only by the generated text summary. For image-heavy applications, store media in a filesystem or object store and pass URLs or file references through message history.

**API reference:** `SummarizationMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
    ],
)
```

**Configuration options**

**Tip:**

The `fraction` conditions for `trigger` and `keep` (shown below) rely on a chat model's [profile data](/oss/langchain/models#model-profiles) if using `langchain>=1.1`. If data are not available, use another condition or specify manually:

```python
from langchain.chat_models import init_chat_model

custom_profile = {
    "max_input_tokens": 100_000,
    # ...
}
model = init_chat_model("gpt-5.5", profile=custom_profile)
```

Model for generating summaries. Can be a model identifier string (e.g., `'openai:gpt-5.4-mini'`) or a `BaseChatModel` instance. See `init_chat_model` for more information.

Condition(s) for triggering summarization. Can be:

- A single `ContextSize` tuple (the specified threshold must be met)
- A single `TriggerClause` dict (all specified thresholds must be met - AND logic)
- A list mixing either form (any item must be met - OR logic)

    Supported thresholds are:

- `fraction` (float): Fraction of model's context size (0-1)
- `tokens` (int): Absolute token count
- `messages` (int): Message count

    A `ContextSize` tuple expresses exactly one threshold. A `TriggerClause` dict can include one or more thresholds, e.g. `{"tokens": 4000, "messages": 10}`, and all thresholds in the dict must be met (AND).

Each `TriggerClause` dict must specify at least one threshold. If `trigger` is not provided, summarization will not trigger automatically.

See the API reference for `ContextSize` and `TriggerClause` for more information.

How much context to preserve after summarization. Specify exactly one of:

- `fraction` (float): Fraction of model's context size to keep (0-1)
- `tokens` (int): Absolute token count to keep
- `messages` (int): Number of recent messages to keep

    See the API reference for `ContextSize` for more information.

Custom token counting function. Defaults to character-based counting.

Custom prompt template for summarization. Uses built-in template if not specified. The template should include `{messages}` placeholder where conversation history will be inserted.

Maximum number of tokens to include when generating the summary. Messages will be trimmed to fit this limit before summarization.

**Deprecated:** Use `summary_prompt` to provide the full prompt instead.

**Deprecated:** Use `trigger: ("tokens", value)` instead. Token threshold for triggering summarization.

**Deprecated:** Use `keep: ("messages", value)` instead. Recent messages to preserve.

**Full example**

The summarization middleware monitors message token counts and automatically summarizes older messages when thresholds are reached.

**Trigger conditions** control when summarization runs:
- A single threshold triggers when that threshold is met
- A trigger clause with multiple thresholds triggers only when all thresholds are met (AND logic)
- A list of trigger conditions triggers when any item is met (OR logic)
- Each threshold can use `fraction` (of model's context size), `tokens` (absolute count), or `messages` (message count)

**Keep condition** control how much context to preserve (specify exactly one):
- `fraction` - Fraction of model's context size to keep
- `tokens` - Absolute token count to keep
- `messages` - Number of recent messages to keep

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

# Single condition: trigger if tokens >= 4000
agent = create_agent(
    model="gpt-5.5",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
    ],
)

# Multiple conditions: trigger if number of tokens >= 3000 OR messages >= 6
agent2 = create_agent(
    model="gpt-5.5",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=[
                ("tokens", 3000),
                ("messages", 6),
            ],
            keep=("messages", 20),
        ),
    ],
)

# AND logic: trigger only when tokens >= 4000 AND messages >= 10
agent3 = create_agent(
    model="gpt-5.5",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger={"tokens": 4000, "messages": 10},
            keep=("messages", 20),
        ),
    ],
)

# Combine AND and OR: trigger if (tokens >= 5000 AND messages >= 3)
# OR (tokens >= 3000 AND messages >= 6)
agent4 = create_agent(
    model="gpt-5.5",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=[
                {"tokens": 5000, "messages": 3},
                {"tokens": 3000, "messages": 6},
            ],
            keep=("messages", 20),
        ),
    ],
)

# Using fractional limits
agent5 = create_agent(
    model="gpt-5.5",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=("fraction", 0.8),
            keep=("fraction", 0.3),
        ),
    ],
)
```

### Human-in-the-loop

Pause agent execution for human approval, editing, or rejection of tool calls before they execute. [Human-in-the-loop](/oss/langchain/human-in-the-loop) is useful for the following:

- High-stakes operations requiring human approval (e.g. database writes, financial transactions).
- Compliance workflows where human oversight is mandatory.
- Long-running conversations where human feedback guides the agent.

**API reference:** `HumanInTheLoopMiddleware`

**Warning:**

Human-in-the-loop middleware requires a [checkpointer](/oss/langgraph/checkpointers#checkpoints) to maintain state across interruptions.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

def your_read_email_tool(email_id: str) -> str:
    """Mock function to read an email by its ID."""
    return f"Email content for ID: {email_id}"

def your_send_email_tool(recipient: str, subject: str, body: str) -> str:
    """Mock function to send an email."""
    return f"Email sent to {recipient} with subject '{subject}'"

agent = create_agent(
    model="gpt-5.5",
    tools=[your_read_email_tool, your_send_email_tool],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "your_send_email_tool": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                },
                "your_read_email_tool": False,
            }
        ),
    ],
)
```

**Tip:**

For complete examples, configuration options, and integration patterns, see the [Human-in-the-loop documentation](/oss/langchain/human-in-the-loop).

**Note:**

Watch this [video guide](https://www.youtube.com/watch?v=SpfT6-YAVPk) demonstrating Human-in-the-loop middleware behavior.

### Model call limit

Limit the number of model calls to prevent infinite loops or excessive costs. Model call limit is useful for the following:

- Preventing runaway agents from making too many API calls.
- Enforcing cost controls on production deployments.
- Testing agent behavior within specific call budgets.

**API reference:** `ModelCallLimitMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="gpt-5.5",
    checkpointer=InMemorySaver(),  # Required for thread limiting
    tools=[],
    middleware=[
        ModelCallLimitMiddleware(
            thread_limit=10,
            run_limit=5,
            exit_behavior="end",
        ),
    ],
)
```

**Note:**

Watch this [video guide](https://www.youtube.com/watch?v=nJEER0uaNkE) demonstrating Model Call Limit middleware behavior.

**Configuration options**

Maximum model calls across all runs in a thread. Defaults to no limit.

Maximum model calls per single invocation. Defaults to no limit.

Behavior when limit is reached. Options: `'end'` (graceful termination) or `'error'` (raise exception)

### Tool call limit

Control agent execution by limiting the number of tool calls, either globally across all tools or for specific tools. Tool call limits are useful for the following:

- Preventing excessive calls to expensive external APIs.
- Limiting web searches or database queries.
- Enforcing rate limits on specific tool usage.
- Protecting against runaway agent loops.

**API reference:** `ToolCallLimitMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, database_tool],
    middleware=[
        # Global limit
        ToolCallLimitMiddleware(thread_limit=20, run_limit=10),
        # Tool-specific limit
        ToolCallLimitMiddleware(
            tool_name="search",
            thread_limit=5,
            run_limit=3,
        ),
    ],
)
```

**Note:**

Watch this [video guide](https://www.youtube.com/watch?v=6gYlaJJ8t0w) demonstrating Tool Call Limit middleware behavior.

**Configuration options**

Name of specific tool to limit. If not provided, limits apply to **all tools globally**.

Maximum tool calls across all runs in a thread (conversation). Persists across multiple invocations with the same thread ID. Requires a checkpointer to maintain state. `None` means no thread limit.

Maximum tool calls per single invocation (one user message → response cycle). Resets with each new user message. `None` means no run limit.

**Note:** At least one of `thread_limit` or `run_limit` must be specified.

Behavior when limit is reached:

- `'continue'` (default) - Block exceeded tool calls with error messages, let other tools and the model continue. The model decides when to end based on the error messages.
- `'error'` - Raise a `ToolCallLimitExceededError` exception, stopping execution immediately
- `'end'` - Stop execution immediately with a `ToolMessage` and AI message for the exceeded tool call. Only works when limiting a single tool; raises `NotImplementedError` if other tools have pending calls.

**Full example**

Specify limits with:
- **Thread limit** - Max calls across all runs in a conversation (requires checkpointer)
- **Run limit** - Max calls per single invocation (resets each turn)

Exit behaviors:
- `'continue'` (default) - Block exceeded calls with error messages, agent continues
- `'error'` - Raise exception immediately
- `'end'` - Stop with ToolMessage + AI message (single-tool scenarios only)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

global_limiter = ToolCallLimitMiddleware(thread_limit=20, run_limit=10)
search_limiter = ToolCallLimitMiddleware(tool_name="search", thread_limit=5, run_limit=3)
database_limiter = ToolCallLimitMiddleware(tool_name="query_database", thread_limit=10)
strict_limiter = ToolCallLimitMiddleware(tool_name="scrape_webpage", run_limit=2, exit_behavior="error")

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, database_tool, scraper_tool],
    middleware=[global_limiter, search_limiter, database_limiter, strict_limiter],
)
```

### PII detection

Detect and handle Personally Identifiable Information (PII) in conversations using configurable strategies. PII detection is useful for the following:

- Healthcare and financial applications with compliance requirements.
- Customer service agents that need to sanitize logs.
- Any application handling sensitive user data.

**Note:**

With `apply_to_output=True`, `PIIMiddleware` also redacts streamed wire output—text deltas, tool-call args, tool outputs, and state snapshots—via a registered stream transformer. Requires `langchain>=1.3.2`. See [Register transformers on middleware](/oss/langchain/event-streaming#register-transformers-on-middleware).

**API reference:** `PIIMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
    ],
)
```

#### Custom PII types

You can create custom PII types by providing a `detector` parameter. This allows you to detect patterns specific to your use case beyond the built-in types.

**Three ways to create custom detectors:**

1. **Regex pattern string** - Simple pattern matching
1. **Custom function** - Complex detection logic with validation

```python
import re

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMatch, PIIMiddleware

# Method 1: Regex pattern string
agent1 = create_agent(
    model="gpt-5.5",
    tools=[],
    middleware=[
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
        ),
    ],
)

# Method 2: Compiled regex pattern
agent2 = create_agent(
    model="gpt-5.5",
    tools=[],
    middleware=[
        PIIMiddleware(
            "phone_number",
            detector=re.compile(r"\+?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{4}"),
            strategy="mask",
        ),
    ],
)

# Method 3: Custom detector function
def detect_ssn(content: str) -> list[PIIMatch]:
    """Detect SSNs with validation."""
    matches: list[PIIMatch] = []
    pattern = r"\d{3}-\d{2}-\d{4}"
    for match in re.finditer(pattern, content):
        ssn = match.group(0)
        # Validate: first 3 digits shouldn't be 000, 666, or 900-999
        first_three = int(ssn[:3])
        if first_three not in [0, 666] and not (900 <= first_three <= 999):
            matches.append({
                "type": "ssn",
                "value": ssn,
                "start": match.start(),
                "end": match.end(),
            })
    return matches

agent3 = create_agent(
    model="gpt-5.5",
    tools=[],
    middleware=[
        PIIMiddleware(
            "ssn",
            detector=detect_ssn,
            strategy="hash",
        ),
    ],
)
```

**Custom detector function signature:**

The detector function must accept a string (content) and return matches:

Returns a list of `PIIMatch` objects:
```python
from langchain.agents.middleware import PIIMatch

def detector(content: str) -> list[PIIMatch]:
    return [
        {
            "type": "custom_type",
            "value": "matched_text",
            "start": 0,
            "end": 12,
        },
        # ... more matches
    ]
```

**Tip:**

For custom detectors:

- Use regex strings for simple patterns
- Use RegExp objects when you need flags (e.g., case-insensitive matching)
- Use custom functions when you need validation logic beyond pattern matching
- Custom functions give you full control over detection logic and can implement complex validation rules

**Configuration options**

Type of PII to detect. Can be a built-in type (`email`, `credit_card`, `ip`, `mac_address`, `url`) or a custom type name.

How to handle detected PII. Options:

- `'block'` - Raise exception when detected
- `'redact'` - Replace with `[REDACTED_{PII_TYPE}]`
- `'mask'` - Partially mask (e.g., `****-****-****-1234`)
- `'hash'` - Replace with deterministic hash

    Custom detector function or regex pattern. If not provided, uses built-in detector for the PII type.

Check user messages before model call

Check AI messages after model call. With `langchain>=1.3.2`, also redacts streamed wire output (text deltas, tool-call args, tool outputs, state snapshots) via a registered stream transformer. See [event streaming](/oss/langchain/event-streaming#register-transformers-on-middleware).

Check tool result messages after execution

### To-do list

Equip agents with task planning and tracking capabilities for complex multi-step tasks. To-do lists are useful for the following:

- Complex multi-step tasks requiring coordination across multiple tools.
- Long-running operations where progress visibility is important.

**Note:**

This middleware automatically provides agents with a `write_todos` tool and system prompts to guide effective task planning.

**API reference:** `TodoListMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[read_file, write_file, run_tests],
    middleware=[TodoListMiddleware()],
)
```

**Note:**

Watch this [video guide](https://www.youtube.com/watch?v=yTWocbVKQxw) demonstrating To-do List middleware behavior.

**Configuration options**

Custom system prompt for guiding todo usage. Uses built-in prompt if not specified.

Custom description for the `write_todos` tool. Uses built-in description if not specified.

### LLM tool selector

Use an LLM to intelligently select relevant tools before calling the main model. LLM tool selectors are useful for the following:

- Agents with many tools (10+) where most aren't relevant per query.
- Reducing token usage by filtering irrelevant tools.
- Improving model focus and accuracy.

This middleware uses structured output to ask an LLM which tools are most relevant for the current query. The structured output schema defines the available tool names and descriptions. Model providers often add this structured output information to the system prompt behind the scenes.

**API reference:** `LLMToolSelectorMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolSelectorMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[tool1, tool2, tool3, tool4, tool5, ...],
    middleware=[
        LLMToolSelectorMiddleware(
            model="gpt-5.4-mini",
            max_tools=3,
            always_include=["search"],
        ),
    ],
)
```

**Configuration options**

Model for tool selection. Can be a model identifier string (e.g., `'openai:gpt-5.4-mini'`) or a `BaseChatModel` instance. See `init_chat_model` for more information.

Defaults to the agent's main model.

Instructions for the selection model. Uses built-in prompt if not specified.

Maximum number of tools to select. If the model selects more, only the first max_tools will be used. No limit if not specified.

Tool names to always include regardless of selection. These do not count against the max_tools limit.

### Provider tool search

Defer selected tools behind model providers' server-side tool search, so the model discovers them on demand instead of receiving every tool schema up front. Provider tool search is useful for:

- Reducing context bloat when using many tools.
- Improving tool selection accuracy by surfacing only relevant tools.

**Note:**

Requires a model with server-side tool search support: Anthropic (Claude Sonnet 4+/Opus 4+/Haiku 4.5+) or OpenAI (gpt-5.5+). Other providers raise a `ValueError`.

**API reference:** `ProviderToolSearchMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ProviderToolSearchMiddleware

agent = create_agent(
    model="anthropic:claude-opus-4-8",
    tools=[get_weather, lookup_order],
    middleware=[
        ProviderToolSearchMiddleware(searchable_tools=["lookup_order"]),
    ],
)
```

**Configuration options**

Tools to defer behind the provider's tool search, given by name or instance. Deferred tools are withheld from the model until its search surfaces them. Tools constructed with `extras={"defer_loading": True}` are deferred regardless of this option; if `searchable_tools` is omitted, only those pre-marked tools are deferred.

**Full example**

The middleware opts-in all tools included in `searchable_tools` for deferral and search. A tool can also opt into deferral at construction time by setting `extras={"defer_loading": True}`.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ProviderToolSearchMiddleware
from langchain.tools import tool

# Marked `defer_loading` at construction, so it's deferred on its own —
# no need to list it in `searchable_tools`.
@tool(extras={"defer_loading": True})
def send_email(to: str) -> str:
    """Send an email."""
    return "sent"

agent = create_agent(
    model="anthropic:claude-opus-4-8",
    tools=[send_email],
    middleware=[ProviderToolSearchMiddleware()],
)
```

### Shell tool

Expose a persistent shell session to agents for command execution. Shell tool middleware is useful for the following:

- Agents that need to execute system commands
- Development and deployment automation tasks
- Testing and validation workflows
- File system operations and script execution

**Warning:**

**Security consideration**: Use appropriate execution policies (`HostExecutionPolicy`, `DockerExecutionPolicy`, or `CodexSandboxExecutionPolicy`) to match your deployment's security requirements.

**Note:**

**Limitation**: Persistent shell sessions do not currently work with interrupts (human-in-the-loop). We anticipate adding support for this in the future.

**API reference:** `ShellToolMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ShellToolMiddleware,
    HostExecutionPolicy,
)

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            execution_policy=HostExecutionPolicy(),
        ),
    ],
)
```

**Configuration options**

Base directory for the shell session. If omitted, a temporary directory is created when the agent starts and removed when it ends.

Optional commands executed sequentially after the session starts

Optional commands executed before the session shuts down

Execution policy controlling timeouts, output limits, and resource configuration. Options:

- `HostExecutionPolicy` - Full host access (default); best for trusted environments where the agent already runs inside a container or VM
- `DockerExecutionPolicy` - Launches a separate Docker container for each agent run, providing harder isolation
- `CodexSandboxExecutionPolicy` - Reuses the Codex CLI sandbox for additional syscall/filesystem restrictions

    Optional redaction rules to sanitize command output before returning it to the model.

**Warning:**

Redaction rules are applied post execution and do not prevent exfiltration of secrets or sensitive data when using `HostExecutionPolicy`.

Optional override for the registered shell tool description

Optional shell executable (string) or argument sequence used to launch the persistent session. Defaults to `/bin/bash`.

Optional environment variables to supply to the shell session. Values are coerced to strings before command execution.

**Full example**

The middleware provides a single persistent shell session that agents can use to execute commands sequentially.

**Execution policies:**
- `HostExecutionPolicy` (default) - Native execution with full host access
- `DockerExecutionPolicy` - Isolated Docker container execution
- `CodexSandboxExecutionPolicy` - Sandboxed execution via Codex CLI

```python
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ShellToolMiddleware,
    HostExecutionPolicy,
    DockerExecutionPolicy,
    RedactionRule,
)

# Basic shell tool with host execution
agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            execution_policy=HostExecutionPolicy(),
        ),
    ],
)

# Docker isolation with startup commands
agent_docker = create_agent(
    model="gpt-5.5",
    tools=[],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            startup_commands=["pip install requests", "export PYTHONPATH=/workspace"],
            execution_policy=DockerExecutionPolicy(
                image="python:3.11-slim",
                command_timeout=60.0,
            ),
        ),
    ],
)

# With output redaction (applied post execution)
agent_redacted = create_agent(
    model="gpt-5.5",
    tools=[],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            redaction_rules=[
                RedactionRule(pii_type="api_key", detector=r"sk-[a-zA-Z0-9]{32}"),
            ],
        ),
    ],
)
```

### Filesystem middleware

Context engineering is a main challenge in building effective agents. This is particularly difficult when using tools that return variable-length results (for example, `web_search` and RAG), as long tool results can quickly fill your context window.

`FilesystemMiddleware` from [Deep Agents](/oss/deepagents/overview) provides four tools for interacting with both short-term and long-term memory:

- `ls`: List the files in the filesystem
- `read_file`: Read an entire file or a certain number of lines from a file
- `write_file`: Write a new file to the filesystem
- `edit_file`: Edit an existing file in the filesystem

```python
from langchain.agents import create_agent
from deepagents.middleware.filesystem import FilesystemMiddleware

# FilesystemMiddleware is included by default in create_deep_agent
# You can customize it if building a custom agent
agent = create_agent(
    model="claude-sonnet-4-6",
    middleware=[
        FilesystemMiddleware(
            backend=None,  # Optional: custom backend (defaults to StateBackend)
            system_prompt="Write to the filesystem when...",  # Optional custom addition to the system prompt
            custom_tool_descriptions={
                "ls": "Use the ls tool when...",
                "read_file": "Use the read_file tool to..."
            },  # Optional: Custom descriptions for filesystem tools
            tools=["read_file", "ls", "glob", "grep"],  # Optional: Allowlist restricting which filesystem tools are exposed
        ),
    ],
)
```

#### Short-term vs. long-term filesystem

By default, these tools write to a local "filesystem" in your graph state. To enable persistent storage across threads, configure a `CompositeBackend` that routes specific paths (like `/memories/`) to a `StoreBackend`.

```python
from langchain.agents import create_agent
from deepagents.middleware import FilesystemMiddleware
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()

agent = create_agent(
    model="claude-sonnet-4-6",
    store=store,
    middleware=[
        FilesystemMiddleware(
            backend=CompositeBackend(
                default=StateBackend(),
                routes={"/memories/": StoreBackend()}
            ),
            custom_tool_descriptions={
                "ls": "Use the ls tool when...",
                "read_file": "Use the read_file tool to..."
            }  # Optional: Custom descriptions for filesystem tools
        ),
    ],
)
```

When you configure a `CompositeBackend` with a `StoreBackend` for `/memories/`, any files prefixed with **/memories/** are saved to persistent storage and survive across different threads. Files without this prefix remain in ephemeral state storage.

### Subagent

Handing off tasks to subagents isolates context, keeping the main (supervisor) agent's context window clean while still going deep on a task.

The subagents middleware from [Deep Agents](/oss/deepagents/overview) allows you to supply subagents through a `task` tool.

```python
from langchain.tools import tool
from langchain.agents import create_agent
from deepagents.middleware.subagents import SubAgentMiddleware

@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."

agent = create_agent(
    model="claude-sonnet-4-6",
    middleware=[
        SubAgentMiddleware(
            default_model="claude-sonnet-4-6",
            default_tools=[],
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent can get weather in cities.",
                    "system_prompt": "Use the get_weather tool to get the weather in a city.",
                    "tools": [get_weather],
                    "model": "gpt-5.5",
                    "middleware": [],
                }
            ],
        )
    ],
)
```

A subagent is defined with a **name**, **description**, **system prompt**, and **tools**. You can also provide a subagent with a custom **model**, or with additional **middleware**. This can be particularly useful when you want to give the subagent an additional state key to share with the main agent.

For more complex use cases, you can also provide your own prebuilt LangGraph graph as a subagent.

```python
from langchain.agents import create_agent
from deepagents.middleware.subagents import SubAgentMiddleware
from deepagents import CompiledSubAgent
from langgraph.graph import StateGraph

# Create a custom LangGraph graph
def create_weather_graph():
    workflow = StateGraph(...)
    # Build your custom graph
    return workflow.compile()

weather_graph = create_weather_graph()

# Wrap it in a CompiledSubAgent
weather_subagent = CompiledSubAgent(
    name="weather",
    description="This subagent can get weather in cities.",
    runnable=weather_graph
)

agent = create_agent(
    model="claude-sonnet-4-6",
    middleware=[
        SubAgentMiddleware(
            default_model="claude-sonnet-4-6",
            default_tools=[],
            subagents=[weather_subagent],
        )
    ],
)
```

In addition to any user-defined subagents, the main agent has access to a `general-purpose` subagent at all times. This subagent has the same instructions as the main agent and all the tools it has access to. The primary purpose of the `general-purpose` subagent is context isolation—the main agent can delegate a complex task to this subagent and get a concise answer back without bloat from intermediate tool calls.

### Rubric grading

**Note:**

`RubricMiddleware` requires `deepagents>=0.6.5`. It is in [**beta**](/oss/versioning); the API may change in the future.

Some tasks have a clear definition of "done" that an agent cannot reliably hit on the first try. `RubricMiddleware` lets you declare _what done looks like_ as a rubric and have the agent self-evaluate and iterate until the rubric is satisfied or a maximum iteration cap is hit.

**API reference:** `RubricMiddleware`

```python Google
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python OpenAI
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="openai:gpt-5.5",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Anthropic
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python OpenRouter
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Fireworks
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Baseten
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Ollama
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

For full configuration options, streaming events, and a complete code generation example, see [Grading rubrics](/oss/deepagents/rubric).

### File search

Provide Glob and Grep search tools over a filesystem. File search middleware is useful for the following:

- Code exploration and analysis
- Finding files by name patterns
- Searching code content with regex
- Large codebases where file discovery is needed

**API reference:** `FilesystemFileSearchMiddleware`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import FilesystemFileSearchMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    middleware=[
        FilesystemFileSearchMiddleware(
            root_path="/workspace",
            use_ripgrep=True,
        ),
    ],
)
```

**Configuration options**

Root directory to search. All file operations are relative to this path.

Whether to use ripgrep for search. Falls back to Python regex if ripgrep is unavailable.

Maximum file size to search in MB. Files larger than this are skipped.

**Full example**

The middleware adds two search tools to agents:

**Glob tool** - Fast file pattern matching:
- Supports patterns like `**/*.py`, `src/**/*.ts`
- Returns matching file paths sorted by modification time

**Grep tool** - Content search with regex:
- Full regex syntax support
- Filter by file patterns with `include` parameter
- Three output modes: `files_with_matches`, `content`, `count`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import FilesystemFileSearchMiddleware
from langchain.messages import HumanMessage

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    middleware=[
        FilesystemFileSearchMiddleware(
            root_path="/workspace",
            use_ripgrep=True,
            max_file_size_mb=10,
        ),
    ],
)

# Agent can now use glob_search and grep_search tools
result = agent.invoke({
    "messages": [HumanMessage("Find all Python files containing 'async def'")]
})

# The agent will use:
# 1. glob_search(pattern="**/*.py") to find Python files
# 2. grep_search(pattern="async def", include="*.py") to find async functions
```

### Context editing

Manage conversation context by clearing older tool call outputs when token limits are reached, while preserving recent results. This helps keep context windows manageable in long conversations with many tool calls. Context editing is useful for the following:

- Long conversations with many tool calls that exceed token limits
- Reducing token costs by removing older tool outputs that are no longer relevant
- Maintaining only the most recent N tool results in context

**API reference:** `ContextEditingMiddleware`, `ClearToolUsesEdit`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ContextEditingMiddleware, ClearToolUsesEdit

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    middleware=[
        ContextEditingMiddleware(
            edits=[
                ClearToolUsesEdit(
                    trigger=100000,
                    keep=3,
                ),
            ],
        ),
    ],
)
```

**Configuration options**

List of `ContextEdit` strategies to apply

Token counting method. Options: `'approximate'` or `'model'`

**`ClearToolUsesEdit` options:**

Token count that triggers the edit. When the conversation exceeds this token count, older tool outputs will be cleared.

Minimum number of tokens to reclaim when the edit runs. If set to 0, clears as much as needed.

Number of most recent tool results that must be preserved. These will never be cleared.

Whether to clear the originating tool call parameters on the AI message. When `True`, tool call arguments are replaced with empty objects.

List of tool names to exclude from clearing. These tools will never have their outputs cleared.

Placeholder text inserted for cleared tool outputs. This replaces the original tool message content.

**Full example**

The middleware applies context editing strategies when token limits are reached. The most common strategy is `ClearToolUsesEdit`, which clears older tool results while preserving recent ones.

**How it works:**
1. Monitor token count in conversation
2. When threshold is reached, clear older tool outputs
3. Keep most recent N tool results
4. Optionally preserve tool call arguments for context

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ContextEditingMiddleware, ClearToolUsesEdit

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, your_calculator_tool, database_tool],
    middleware=[
        ContextEditingMiddleware(
            edits=[
                ClearToolUsesEdit(
                    trigger=2000,
                    keep=3,
                    clear_tool_inputs=False,
                    exclude_tools=[],
                    placeholder="[cleared]",
                ),
            ],
        ),
    ],
)
```

### LLM tool emulator

Emulate tool execution using an LLM for testing purposes, replacing actual tool calls with AI-generated responses. LLM tool emulators are useful for the following:

- Testing agent behavior without executing real tools.
- Developing agents when external tools are unavailable or expensive.
- Prototyping agent workflows before implementing actual tools.

**API reference:** `LLMToolEmulator`

```python
from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolEmulator

agent = create_agent(
    model="gpt-5.5",
    tools=[get_weather, search_database, send_email],
    middleware=[
        LLMToolEmulator(),  # Emulate all tools
    ],
)
```

**Configuration options**

List of tool names (str) or BaseTool instances to emulate. If `None` (default), ALL tools will be emulated. If empty list `[]`, no tools will be emulated. If array with tool names/instances, only those tools will be emulated.

Model to use for generating emulated tool responses. Can be a model identifier string (e.g., `'google_genai:gemini-3.6-flash'`) or a `BaseChatModel` instance. Defaults to the agent's model if not specified. See `init_chat_model` for more information.

**Full example**

The middleware uses an LLM to generate plausible responses for tool calls instead of executing the actual tools.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolEmulator
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"Weather in {location}"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    return "Email sent"

# Emulate all tools (default behavior)
agent = create_agent(
    model="gpt-5.5",
    tools=[get_weather, send_email],
    middleware=[LLMToolEmulator()],
)

# Emulate specific tools only
agent2 = create_agent(
    model="gpt-5.5",
    tools=[get_weather, send_email],
    middleware=[LLMToolEmulator(tools=["get_weather"])],
)

# Use custom model for emulation
agent4 = create_agent(
    model="gpt-5.5",
    tools=[get_weather, send_email],
    middleware=[LLMToolEmulator(model="claude-sonnet-4-6")],
)
```

## Provider-specific middleware

These middleware are optimized for specific LLM providers. See each provider's documentation for full details and examples.

- [Anthropic](/oss/integrations/middleware/anthropic)

        Prompt caching, bash tool, text editor, memory, and file search middleware for Claude models.

- [AWS](/oss/integrations/middleware/aws)

        Prompt caching middleware for Amazon Bedrock models.

- [OpenAI](/oss/integrations/middleware/openai)

        Content moderation middleware for OpenAI models.

---

# Custom middleware
> 출처: data/raw/langchain/middleware/custom.mdx | https://docs.langchain.com/oss/python/langchain/middleware/custom

Build custom middleware by implementing hooks that run at specific points in the agent execution flow.

## Hooks

Middleware provides two styles of hooks to intercept agent execution:

- [Node-style hooks](#node-style-hooks)

        Run sequentially at specific execution points.

- [Wrap-style hooks](#wrap-style-hooks)

        Run around each model or tool call.

### Node-style hooks

Run sequentially at specific execution points. Use for logging, validation, and state updates.

Choose the hooks your middleware needs. You can choose between node-style hooks and wrap-style hooks.

**Node-style hooks** run at specific execution points:

| Hook | When it runs |
|------|-------------|
| `before_agent` | Before agent starts (once per invocation) |
| `before_model` | Before each model call |
| `after_model` | After each model response |
| `after_agent` | After agent completes (once per invocation) |

**Wrap-style hooks** run around each call, giving you control over execution:

| Hook | When it runs |
|------|-------------|
| `wrap_model_call` | Around each model call |
| `wrap_tool_call` | Around each tool call |

**Example:**

**Decorator**

```python
from langchain.agents.middleware import before_model, after_model, AgentState
from langchain.messages import AIMessage
from langgraph.runtime import Runtime
from typing import Any

@before_model(can_jump_to=["end"])
def check_message_limit(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    if len(state["messages"]) >= 50:
        return {
            "messages": [AIMessage("Conversation limit reached.")],
            "jump_to": "end"
        }
    return None

@after_model
def log_response(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"Model returned: {state['messages'][-1].content}")
    return None
```

**Class**

```python
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain.messages import AIMessage
from langgraph.runtime import Runtime
from typing import Any

class MessageLimitMiddleware(AgentMiddleware):
    def __init__(self, max_messages: int = 50):
        super().__init__()
        self.max_messages = max_messages

@hook_config(can_jump_to=["end"])
def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    if len(state["messages"]) >= self.max_messages:
        return {
            "messages": [AIMessage("Conversation limit reached.")],
            "jump_to": "end"
        }
    return None

    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"Model returned: {state['messages'][-1].content}")
        return None
```

### Wrap-style hooks

Intercept execution and control when the handler is called. Use for retries, caching, and transformation.

You decide if the handler is called zero times (short-circuit), once (normal flow), or multiple times (retry logic).

**Available hooks:**

- `wrap_model_call` - Around each model call
- `wrap_tool_call` - Around each tool call

**Example:**

**Decorator**

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@wrap_model_call
def retry_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    for attempt in range(3):
        try:
            return handler(request)
        except Exception as e:
            if attempt == 2:
                raise
            print(f"Retry {attempt + 1}/3 after error: {e}")
```

**Class**

```python
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from typing import Callable

class RetryMiddleware(AgentMiddleware):
    def __init__(self, max_retries: int = 3):
        super().__init__()
        self.max_retries = max_retries

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        for attempt in range(self.max_retries):
            try:
                return handler(request)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                print(f"Retry {attempt + 1}/{self.max_retries} after error: {e}")
```

## State updates

Both node-style and wrap-style hooks can update agent state. The mechanism differs:

- **Node-style hooks** (`before_agent`, `before_model`, `after_model`, `after_agent`): Return a dict directly. The dict is applied to the agent state using the graph's reducers.
- **Wrap-style hooks** (`wrap_model_call`, `wrap_tool_call`): For model calls, return `ExtendedModelResponse` with a `Command` to inject state updates alongside the model response. For tool calls, return a `Command` directly. Use these when you need to track or update state based on logic that runs during the model or tool call, such as summarization trigger points, usage metadata, or custom fields calculated from the request or response.

### Node-style hooks

Return a dict from a node-style hook to merge updates into agent state. The dict keys map to state fields.

```python
from langchain.agents.middleware import after_model, AgentState
from langgraph.runtime import Runtime
from typing import Any
from typing_extensions import NotRequired

class TrackingState(AgentState):
    model_call_count: NotRequired[int]

@after_model(state_schema=TrackingState)
def increment_after_model(state: TrackingState, runtime: Runtime) -> dict[str, Any] | None:
    return {"model_call_count": state.get("model_call_count", 0) + 1}
```

### Wrap-style hooks

Return a `ExtendedModelResponse` with a `Command` from `wrap_model_call` to inject state updates from the model call layer:

```python
from typing import Callable
from langchain.agents.middleware import (
    wrap_model_call,
    ModelRequest,
    ModelResponse,
    AgentState,
    ExtendedModelResponse
)
from langgraph.types import Command
from typing_extensions import NotRequired

class UsageTrackingState(AgentState):
    """Agent state with token usage tracking."""

last_model_call_tokens: NotRequired[int]

@wrap_model_call(state_schema=UsageTrackingState)
def track_usage(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ExtendedModelResponse:
    response = handler(request)
    return ExtendedModelResponse(
        model_response=response,
        command=Command(update={"last_model_call_tokens": 150}),
    )
```

The `Command` flows through the graph's reducers, so updates are applied correctly and messages are additive rather than replacing existing state.

#### Composition with multiple middleware

When multiple middleware layers return `ExtendedModelResponse`, their commands compose:

- **Commands are applied through reducers:** Each `Command` becomes a separate state update. For messages, this means they are additive.
- **Outer wins on conflicts:** For non-reducer state fields, commands are applied inner-first, then outer. The outermost middleware's value takes precedence on conflicting keys.
- **Retry-safe:** If the outer middleware implements logic that can result in multiple calls to `handler()` again (for example, retry logic), commands from earlier calls are discarded.

```python
from typing import Annotated, Callable

from langchain.agents.middleware import (
    AgentMiddleware,
    AgentState,
    ExtendedModelResponse,
    ModelRequest,
    ModelResponse,
)
from langchain.messages import SystemMessage
from langgraph.types import Command
from typing_extensions import NotRequired

def _last_wins(_a: str, b: str) -> str:
    """Reducer: last writer wins (outer overwrites inner)."""
    return b

class CustomMiddlewareState(AgentState):
    """Agent state: trace_layer uses last-wins (outer wins), messages use additive reducer."""

# Non-reducer field with last-wins: both middleware write; outermost value wins
trace_layer: NotRequired[Annotated[str, _last_wins]]

class OuterMiddleware(AgentMiddleware):
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ExtendedModelResponse:
        response = handler(request)
        return ExtendedModelResponse(
            model_response=response,
            command=Command(update={
                "trace_layer": "outer",
                "messages": [SystemMessage(content="[Outer ran]")],
            }),
        )

class InnerMiddleware(AgentMiddleware):
    """Adds trace_layer and message. Outer adds to same keys; trace_layer: outer wins, messages: additive."""

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ):
        response = handler(request)
        return ExtendedModelResponse(
            model_response=response,
            command=Command(update={
                "trace_layer": "inner",
                "messages": [SystemMessage(content="[Inner ran]")],
            }),
        )
```

## Create middleware

You can create middleware in two ways:

- [Decorator-based middleware](#decorator-based-middleware)

    Quick and simple for single-hook middleware. Use decorators to wrap individual functions.

- [Class-based middleware](#class-based-middleware)

    More powerful for complex middleware with multiple hooks or configuration.

### Decorator-based middleware

Quick and simple for single-hook middleware. Use decorators to wrap individual functions.

**Available decorators:**

**Node-style:**
- `@before_agent` - Runs before agent starts (once per invocation)
- `@before_model` - Runs before each model call
- `@after_model` - Runs after each model response
- `@after_agent` - Runs after agent completes (once per invocation)

**Wrap-style:**
- `@wrap_model_call` - Wraps each model call with custom logic
- `@wrap_tool_call` - Wraps each tool call with custom logic

**Convenience:**
- `@dynamic_prompt` - Generates dynamic system prompts

**Example:**

```python
from langchain.agents.middleware import (
    before_model,
    wrap_model_call,
    AgentState,
    ModelRequest,
    ModelResponse,
)
from langchain.agents import create_agent
from langgraph.runtime import Runtime
from typing import Any, Callable

@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"About to call model with {len(state['messages'])} messages")
    return None

@wrap_model_call
def retry_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    for attempt in range(3):
        try:
            return handler(request)
        except Exception as e:
            if attempt == 2:
                raise
            print(f"Retry {attempt + 1}/3 after error: {e}")

agent = create_agent(
    model="gpt-5.5",
    middleware=[log_before_model, retry_model],
    tools=[...],
)
```

**When to use decorators:**
- Single hook needed
- No complex configuration
- Quick prototyping

### Class-based middleware

More powerful for complex middleware with multiple hooks or configuration. Use classes when you need to define both sync and async implementations for the same hook, or when you want to combine multiple hooks in a single middleware.

An `AgentMiddleware` subclass can declare three class attributes that the agent factory picks up at compile time:

- `state_schema` — extend the agent state with custom fields. See [Custom state schema](#custom-state-schema).
- `tools` — register additional tools that ship with the middleware (e.g., `write_todos` on the to-do list middleware).
- `transformers` — register scope-aware stream transformer factories. See [Custom stream transformers](#custom-stream-transformers).

**Example:**

```python
from langchain.agents.middleware import (
    AgentMiddleware,
    AgentState,
    ModelRequest,
    ModelResponse,
)
from langgraph.runtime import Runtime
from typing import Any, Callable

class LoggingMiddleware(AgentMiddleware):
    def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"About to call model with {len(state['messages'])} messages")
        return None

def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"Model returned: {state['messages'][-1].content}")
    return None

async def abefore_model(
    self, state: AgentState, runtime: Runtime
) -> dict[str, Any] | None:
    # Async version of before_model
    return None

async def aafter_model(
    self, state: AgentState, runtime: Runtime
) -> dict[str, Any] | None:
    # Async version of after_model
    print(f"Model returned: {state['messages'][-1].content}")
    return None

agent = create_agent(
    model="gpt-5.5",
    middleware=[LoggingMiddleware()],
    tools=[...],
)
```

**When to use classes:**
- Defining both sync and async implementations for the same hook
- Multiple hooks needed in a single middleware
- Complex configuration required (e.g., configurable thresholds, custom models)
- Reuse across projects with init-time configuration

## Custom state schema

If your middleware needs to track state across hooks, middleware can extend the agent's state with custom properties. This enables middleware to:

- **Track state across execution**: Maintain counters, flags, or other values that persist throughout the agent's execution lifecycle
- **Share data between hooks**: Pass information from `before_model` to `after_model` or between different middleware instances
- **Implement cross-cutting concerns**: Add functionality like rate limiting, usage tracking, user context, or audit logging without modifying the core agent logic
- **Make conditional decisions**: Use accumulated state to determine whether to continue execution, jump to different nodes, or modify behavior dynamically

**Decorator**

```python
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.agents.middleware import AgentState, before_model, after_model
from typing_extensions import NotRequired
from typing import Any
from langgraph.runtime import Runtime

class CustomState(AgentState):
    model_call_count: NotRequired[int]
    user_id: NotRequired[str]

@before_model(state_schema=CustomState, can_jump_to=["end"])
def check_call_limit(state: CustomState, runtime: Runtime) -> dict[str, Any] | None:
    count = state.get("model_call_count", 0)
    if count > 10:
        return {"jump_to": "end"}
    return None

@after_model(state_schema=CustomState)
def increment_counter(state: CustomState, runtime: Runtime) -> dict[str, Any] | None:
    return {"model_call_count": state.get("model_call_count", 0) + 1}

agent = create_agent(
    model="gpt-5.5",
    middleware=[check_call_limit, increment_counter],
    tools=[],
)

# Invoke with custom state
result = agent.invoke({
    "messages": [HumanMessage("Hello")],
    "model_call_count": 0,
    "user_id": "user-123",
})
```

**Class**

```python
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.agents.middleware import AgentState, AgentMiddleware
from typing_extensions import NotRequired
from typing import Any

class CustomState(AgentState):
    model_call_count: NotRequired[int]
    user_id: NotRequired[str]

class CallCounterMiddleware(AgentMiddleware[CustomState]):
    state_schema = CustomState

def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
    count = state.get("model_call_count", 0)
    if count > 10:
        return {"jump_to": "end"}
    return None

def after_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
    return {"model_call_count": state.get("model_call_count", 0) + 1}

agent = create_agent(
    model="gpt-5.5",
    middleware=[CallCounterMiddleware()],
    tools=[],
)

# Invoke with custom state
result = agent.invoke({
    "messages": [HumanMessage("Hello")],
    "model_call_count": 0,
    "user_id": "user-123",
})
```

## Custom stream transformers

**Note:**

Middleware-registered transformers require `langchain>=1.3.2`.

Middleware can register stream transformer factories that project events from the live agent stream onto typed extension channels. This is useful for surfacing counters, side-channel artifacts, partial outputs, or wire-level redaction without coupling to the framework's built-in projections.

At compile time, middleware-registered factories merge with anything the caller passes directly to the agent factory. The [final ordering rules](/oss/langchain/event-streaming#register-transformers-on-middleware) keep the built-in `ToolCallTransformer` in front and let caller-supplied entries land last.

Set the `transformers` class attribute to a tuple of factory callables. Each factory has the shape `Callable[[tuple[str, ...]], StreamTransformer]` and is invoked as `factory(scope)`, where `scope` is the mini-mux scope tuple (`()` for the root, non-empty for subgraphs); returning a fresh transformer per call keeps each subgraph isolated.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware

class ToolActivityMiddleware(AgentMiddleware):
    transformers = (ToolActivityTransformer,)

agent = create_agent(
    model="gpt-5-nano",
    tools=[...],
    middleware=[ToolActivityMiddleware()],
)
```

See [Register transformers on middleware](/oss/langchain/event-streaming#register-transformers-on-middleware) for the full ordering rules and the PII redaction example.

## Execution order

When using multiple middleware, understand how they execute:

```python
agent = create_agent(
    model="gpt-5.5",
    middleware=[middleware1, middleware2, middleware3],
    tools=[...],
)
```

**Execution flow**

**Before hooks run in order:**
1. `middleware1.before_agent()`
2. `middleware2.before_agent()`
3. `middleware3.before_agent()`

__Agent loop starts__

4. `middleware1.before_model()`
5. `middleware2.before_model()`
6. `middleware3.before_model()`

**Wrap hooks nest like function calls:**

7. `middleware1.wrap_model_call()` → `middleware2.wrap_model_call()` → `middleware3.wrap_model_call()` → model

**After hooks run in reverse order:**

8. `middleware3.after_model()`
9. `middleware2.after_model()`
10. `middleware1.after_model()`

__Agent loop ends__

11. `middleware3.after_agent()`
12. `middleware2.after_agent()`
13. `middleware1.after_agent()`

**Key rules:**
- `before_*` hooks: First to last
- `after_*` hooks: Last to first (reverse)
- `wrap_*` hooks: Nested (first middleware wraps all others)

## Agent jumps

To exit early from middleware, return a dictionary with `jump_to`:

**Available jump targets:**
- `'end'`: Jump to the end of the agent execution (or the first `after_agent` hook)
- `'tools'`: Jump to the tools node
- `'model'`: Jump to the model node (or the first `before_model` hook)

**Decorator**

```python
from langchain.agents.middleware import after_model, hook_config, AgentState
from langchain.messages import AIMessage
from langgraph.runtime import Runtime
from typing import Any

@after_model
@hook_config(can_jump_to=["end"])
def check_for_blocked(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    last_message = state["messages"][-1]
    if "BLOCKED" in last_message.content:
        return {
            "messages": [AIMessage("I cannot respond to that request.")],
            "jump_to": "end"
        }
    return None
```

**Class**

```python
from langchain.agents.middleware import AgentMiddleware, hook_config, AgentState
from langchain.messages import AIMessage
from langgraph.runtime import Runtime
from typing import Any

class BlockedContentMiddleware(AgentMiddleware):
    @hook_config(can_jump_to=["end"])
    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        last_message = state["messages"][-1]
        if "BLOCKED" in last_message.content:
            return {
                "messages": [AIMessage("I cannot respond to that request.")],
                "jump_to": "end"
            }
        return None
```

## Configure tracing

**Note:**

Requires `langchain>=1.3.15`.

Middleware hook spans trace their inputs and outputs by default. Set a `trace_policy` to shape what they record. `TracePolicy` accepts callables such as `process_inputs` and `process_outputs` that transform the traced value; `omit_payload` drops it entirely. This can be useful as an optimization when the full message history is uninformative to the function of the middleware.

To omit the input payload from a middleware's trace:

```python
from langchain.agents.middleware import AgentMiddleware, TracePolicy, omit_payload

class MyMiddleware(AgentMiddleware):
    trace_policy = TracePolicy(process_inputs=omit_payload)
```

To apply a policy to all middleware, configure a global default:

```python
from langchain.agents.middleware import configure_trace_policy, TracePolicy, omit_payload

configure_trace_policy(TracePolicy(process_inputs=omit_payload))  # pass None to clear
```

A middleware's own `trace_policy` overrides the global default.

## Best practices

1. Keep middleware focused - each should do one thing well
2. Handle errors gracefully - don't let middleware errors crash the agent
3. **Use appropriate hook types**:
    - Node-style for sequential logic (logging, validation)
    - Wrap-style for control flow (retry, fallback, caching)
4. Clearly document any custom state properties
5. Unit test middleware independently before integrating
6. Consider execution order - place critical middleware first in the list
7. Use built-in middleware when possible

## Examples

### Dynamic prompt

Dynamically modify the system prompt at runtime to inject context, user-specific instructions, or other information before each model call. This is one of the most common middleware use cases.

Use the `system_message` field on `ModelRequest` to read and modify the system prompt. It contains a `SystemMessage` object (even if the agent was created with a string `system_prompt`).

**Decorator**

```python
from collections.abc import Callable

from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain.messages import SystemMessage

@wrap_model_call
def add_context(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    new_content = list(request.system_message.content_blocks) + [
        {"type": "text", "text": "Additional context."}
    ]
    new_system_message = SystemMessage(content=new_content)
    return handler(request.override(system_message=new_system_message))
```

**Class**

```python
from collections.abc import Callable

from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse

class ContextMiddleware(AgentMiddleware):
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        new_content = list(request.system_message.content_blocks) + [
            {"type": "text", "text": "Additional context."}
        ]
        new_system_message = SystemMessage(content=new_content)
        return handler(request.override(system_message=new_system_message))
```

**Note:**

- `ModelRequest.system_message` is always a `SystemMessage` object, even if the agent was created with `system_prompt="string"`
- Use `SystemMessage.content_blocks` to access content as a list of blocks, regardless of whether the original content was a string or list
- When modifying system messages, use `content_blocks` and append new blocks to preserve existing structure
- You can pass `SystemMessage` objects directly to `create_agent`'s `system_prompt` parameter for advanced use cases like cache control

### Dynamic model selection

**Decorator**

```python
from collections.abc import Callable

from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain.chat_models import init_chat_model

complex_model = init_chat_model("claude-sonnet-4-6")
simple_model = init_chat_model("claude-haiku-4-5-20251001")

@wrap_model_call
def dynamic_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    if len(request.messages) > 10:
        model = complex_model
    else:
        model = simple_model
    return handler(request.override(model=model))
```

**Class**

```python
from collections.abc import Callable

from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langchain.chat_models import init_chat_model

complex_model = init_chat_model("claude-sonnet-4-6")
simple_model = init_chat_model("claude-haiku-4-5-20251001")

class DynamicModelMiddleware(AgentMiddleware):
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        if len(request.messages) > 10:
            model = complex_model
        else:
            model = simple_model
        return handler(request.override(model=model))
```

### Dynamically selecting tools

Select relevant tools at runtime to improve performance and accuracy. This section covers filtering pre-registered tools. For registering tools that are discovered at runtime (e.g., from MCP servers), see [Runtime tool registration](/oss/langchain/tools#dynamic-tool-selection).

**Benefits:**
- **Shorter prompts** - Reduce complexity by exposing only relevant tools
- **Better accuracy** - Models choose correctly from fewer options
- **Permission control** - Dynamically filter tools based on user access

**Decorator**

```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@wrap_model_call
def select_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """Middleware to select relevant tools based on state/context."""
    # Select a small, relevant subset of tools based on state/context
    relevant_tools = select_relevant_tools(request.state, request.runtime)
    return handler(request.override(tools=relevant_tools))

agent = create_agent(
    model="gpt-5.5",
    tools=all_tools,  # All available tools need to be registered upfront
    middleware=[select_tools],
)
```

**Class**

```python
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from typing import Callable

class ToolSelectorMiddleware(AgentMiddleware):
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """Middleware to select relevant tools based on state/context."""
        # Select a small, relevant subset of tools based on state/context
        relevant_tools = select_relevant_tools(request.state, request.runtime)
        return handler(request.override(tools=relevant_tools))

agent = create_agent(
    model="gpt-5.5",
    tools=all_tools,  # All available tools need to be registered upfront
    middleware=[ToolSelectorMiddleware()],
)
```

### Tool call monitoring

**Decorator**

```python
from collections.abc import Callable

from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langgraph.types import Command

@wrap_tool_call
def monitor_tool(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    print(f"Executing tool: {request.tool_call['name']}")
    print(f"Arguments: {request.tool_call['args']}")
    try:
        result = handler(request)
        print("Tool completed successfully")
        return result
    except Exception as e:
        print(f"Tool failed: {e}")
        raise
```

**Class**

```python
from collections.abc import Callable

from langchain.agents.middleware import AgentMiddleware
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langgraph.types import Command

class ToolMonitoringMiddleware(AgentMiddleware):
    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        print(f"Executing tool: {request.tool_call['name']}")
        print(f"Arguments: {request.tool_call['args']}")
        try:
            result = handler(request)
            print("Tool completed successfully")
            return result
        except Exception as e:
            print(f"Tool failed: {e}")
            raise
```

### Prompt caching (Anthropic)

When working with Anthropic models, use structured content blocks with cache control directives to cache large system prompts:

**Decorator**

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.messages import SystemMessage
from typing import Callable

@wrap_model_call
def add_cached_context(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    # Always work with content blocks
    new_content = list(request.system_message.content_blocks) + [
        {
            "type": "text",
            "text": "Here is a large document to analyze:\n\n<document>...</document>",
            # content up until this point is cached
            "cache_control": {"type": "ephemeral"}
        }
    ]

    new_system_message = SystemMessage(content=new_content)
    return handler(request.override(system_message=new_system_message))
```

**Class**

```python
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langchain.messages import SystemMessage
from typing import Callable

class CachedContextMiddleware(AgentMiddleware):
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        # Always work with content blocks
        new_content = list(request.system_message.content_blocks) + [
            {
                "type": "text",
                "text": "Here is a large document to analyze:\n\n<document>...</document>",
                "cache_control": {"type": "ephemeral"}  # This content will be cached
            }
        ]

        new_system_message = SystemMessage(content=new_content)
        return handler(request.override(system_message=new_system_message))
```

**Notes:**
- `ModelRequest.system_message` is always a `SystemMessage` object, even if the agent was created with `system_prompt="string"`
- Use `SystemMessage.content_blocks` to access content as a list of blocks, regardless of whether the original content was a string or list
- When modifying system messages, use `content_blocks` and append new blocks to preserve existing structure
- You can pass `SystemMessage` objects directly to `create_agent`'s `system_prompt` parameter for advanced use cases like cache control

## Additional resources

- [Middleware API reference](https://reference.langchain.com/python/langchain/middleware/)
- [Built-in middleware](/oss/langchain/middleware/built-in)
- [Testing agents](/oss/langchain/test/)

---

# Middleware overview
> 출처: data/raw/langchain/middleware/overview.mdx | https://docs.langchain.com/oss/python/langchain/middleware/overview

Control and customize agent execution at every step

Middleware provides a way to more tightly control what happens inside the agent. Middleware is useful for the following:

- Tracking agent behavior with logging, analytics, and debugging.
- Transforming prompts, [tool selection](/oss/langchain/middleware/built-in#llm-tool-selector), and output formatting.
- Adding [retries](/oss/langchain/middleware/built-in#tool-retry), [fallbacks](/oss/langchain/middleware/built-in#model-fallback), and early termination logic.
- Applying [rate limits](/oss/langchain/middleware/built-in#model-call-limit), guardrails, and [PII detection](/oss/langchain/middleware/built-in#pii-detection).

Add middleware by passing them to `create_agent`:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[
        SummarizationMiddleware(...),
        HumanInTheLoopMiddleware(...)
    ],
)
```

## The agent loop

The core agent loop involves calling a model, letting it choose tools to execute, and then finishing when it calls no more tools:

Middleware exposes hooks before and after each of those steps:

## Use middleware inside a LangGraph workflow

Middleware is not a separate runtime: hooks run inside the compiled [LangGraph](/oss/langgraph/overview) that `create_agent` returns. You can drop the whole agent (middleware and all) into a larger StateGraph as a node or subgraph, and every middleware hook continues to run.

Reach for this pattern when the surrounding topology is more than a standard "loop until done": classifying input before routing to one of several agents, fanning out work in parallel, or stitching agent calls together with deterministic steps.

`HumanInTheLoopMiddleware` matches against each tool's `.name`.

`@tool`-decorated functions take their name from the function, so the key below is `"send_email"`.

```python
from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.graph import START, StateGraph

# Assumes read_email, send_email, classify_node, and route are defined elsewhere.
email_agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[read_email, send_email],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"send_email": True})],
)

graph = (
    StateGraph(AgentState)
    .add_node("classify", classify_node)
    .add_node("email_agent", email_agent)
    .add_edge(START, "classify")
    .add_conditional_edges("classify", route)
    .compile()
)
```

The HITL interrupt, summarization, PII redaction, retries, and any custom hooks all travel with the agent node. See [Use subgraphs](/oss/langgraph/use-subgraphs) for the full set of composition patterns, including subgraph checkpointer scoping (per-invocation versus per-thread).

## Additional resources

- [Built-in middleware](/oss/langchain/middleware/built-in)

        Explore built-in middleware for common use cases.

- [Custom middleware](/oss/langchain/middleware/custom)

        Build your own middleware with hooks and decorators.

- [Middleware API reference](https://reference.langchain.com/python/langchain/middleware/)

        Complete API reference for middleware.

- [Middleware integrations](/oss/integrations/middleware/)

        Provider-specific middleware for Anthropic, AWS, OpenAI, and more.

- [Testing agents](/oss/langchain/test/)

        Test your agents with LangSmith.

---

# Models
> 출처: data/raw/langchain/models.mdx | https://docs.langchain.com/oss/python/langchain/models

Initialize and configure chat models, the reasoning engine of LangChain agents, with support for tool calling, structured output, and multimodal inputs.

[LLMs](https://en.wikipedia.org/wiki/Large_language_model) are powerful AI tools that can interpret and generate text like humans. They're versatile enough to write content, translate languages, summarize, and answer questions without needing specialized training for each task.

In addition to text generation, many models support:

* 

 [Tool calling](#tool-calling) - calling external tools (like databases queries or API calls) and use results in their responses.
* 

 [Structured output](#structured-output) - where the model's response is constrained to follow a defined format.
* 

 [Multimodality](#multimodal) - process and return data other than text, such as images, audio, and video.
* 

 [Reasoning](#reasoning) - models perform multi-step reasoning to arrive at a conclusion.

Models are the reasoning engine of [agents](/oss/langchain/agents). They drive the agent's decision-making process, determining which tools to call, how to interpret results, and when to provide a final answer.

The quality and capabilities of the model you choose directly impact your agent's baseline reliability and performance. Different models excel at different tasks - some are better at following complex instructions, others at structured reasoning, and some support larger context windows for handling more information.

LangChain's standard model interfaces give you access to many different provider integrations, which makes it easy to experiment with and switch between models to find the best fit for your use case.

For provider-specific integration information and capabilities, see the provider's [chat model page](/oss/integrations/chat).

**Tip:**

[LangSmith](/langsmith/observability) traces each model call so you can compare providers, inspect tool routing, and debug failures. Follow the [tracing quickstart](/langsmith/trace-with-langchain) to get set up.

We recommend you also set up [LangSmith Engine](/langsmith/engine) which monitors your traces, detects issues, and proposes fixes.

## Basic usage

Models can be utilized in two ways:

1. **With agents** - Models can be dynamically specified when creating an [agent](/oss/langchain/agents#model).
2. **Standalone** - Models can be called directly (outside of the agent loop) for tasks like text generation, classification, or extraction without the need for an agent framework.

The same model interface works in both contexts, which gives you the flexibility to start simple and scale up to more complex agent-based workflows as needed.

### Initialize a model

The easiest way to get started with a standalone model in LangChain is to use `init_chat_model` to initialize one from a chat model provider of your choice (examples below):

**OpenAI**

👉 Read the [OpenAI chat model integration docs](/oss/python/integrations/chat/openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-5.5")
```
```python Model Class
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-..."

model = ChatOpenAI(model="gpt-5.5")
```

**Anthropic**

👉 Read the [Anthropic chat model integration docs](/oss/python/integrations/chat/anthropic/)

```bash pip
pip install -U "langchain[anthropic]"
```

```bash uv
uv add "langchain[anthropic]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = init_chat_model("claude-sonnet-4-6")
```
```python Model Class
import os
from langchain_anthropic import ChatAnthropic

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = ChatAnthropic(model="claude-sonnet-4-6")
```

**Azure**

👉 Read the [Azure chat model integration docs](/oss/python/integrations/chat/azure_chat_openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = init_chat_model(
    "azure_openai:gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
```
```python Model Class
import os
from langchain_openai import AzureChatOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = AzureChatOpenAI(
    model="gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
)
```

**Google Gemini**

👉 Read the [Google GenAI chat model integration docs](/oss/python/integrations/chat/google_generative_ai/)

```bash pip
pip install -U "langchain[google-genai]"
```

```bash uv
uv add "langchain[google-genai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["GOOGLE_API_KEY"] = "..."

model = init_chat_model("google_genai:gemini-3.7-flash")
```
```python Model Class
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "..."

model = ChatGoogleGenerativeAI(model="gemini-3.7-flash")
```

**AWS Bedrock**

👉 Read the [AWS Bedrock chat model integration docs](/oss/python/integrations/chat/bedrock/)

```bash pip
pip install -U "langchain[aws]"
```

```bash uv
uv add "langchain[aws]"
```

```python init_chat_model
from langchain.chat_models import init_chat_model

# Follow the steps here to configure your credentials:
# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html

model = init_chat_model(
    "us.anthropic.claude-sonnet-4-6",
    model_provider="bedrock_converse",
)
```
```python Model Class
from langchain_aws import ChatBedrock

model = ChatBedrock(model="us.anthropic.claude-sonnet-4-6")
```

**HuggingFace**

👉 Read the [HuggingFace chat model integration docs](/oss/python/integrations/chat/huggingface/)

```bash pip
pip install -U "langchain[huggingface]"
```

```bash uv
uv add "langchain[huggingface]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

model = init_chat_model(
    "microsoft/Phi-3-mini-4k-instruct",
    model_provider="huggingface",
    temperature=0.7,
    max_tokens=1024,
)
```

```python Model Class
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    temperature=0.7,
    max_length=1024,
)
model = ChatHuggingFace(llm=llm)
```

**OpenRouter**

👉 Read the [OpenRouter chat model integration docs](/oss/python/integrations/chat/openrouter/)

```bash pip
pip install -U "langchain-openrouter"
```

```bash uv
uv add "langchain-openrouter"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = init_chat_model(
    "auto",
    model_provider="openrouter",
)
```
```python Model Class
import os
from langchain_openrouter import ChatOpenRouter

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = ChatOpenRouter(model="auto")
```

```python
response = model.invoke("Why do parrots talk?")
```

See `init_chat_model` for more detail, including information on how to pass model [parameters](#parameters).

### Supported providers and models

LangChain supports all major model providers through dedicated integration packages. Each provider package implements the same standard interface, so you can swap providers without rewriting application logic. New model names work immediately — no LangChain update required — because provider packages pass model names directly to the provider's API.

Browse the [full list of supported providers](/oss/integrations/providers/overview), or see [Providers and models](/oss/concepts/providers-and-models) for a conceptual overview of how providers, packages, and model names work together in LangChain.

### Key methods

- [Invoke](#invoke)

    The model takes messages as input and outputs messages after generating a complete response.

- [Stream](#stream)

    Invoke the model, but stream the output as it is generated in real-time.

- [Batch](#batch)

    Send multiple requests to a model in a batch for more efficient processing.

**Info:**

In addition to chat models, LangChain provides support for other adjacent technologies, such as embedding models and vector stores. See the [integrations page](/oss/integrations/providers/overview) for details.

## Parameters

A chat model takes parameters that can be used to configure its behavior. The full set of supported parameters varies by model and provider, but standard ones include:

The name or identifier of the specific model you want to use with a provider. You can also specify both the model and its provider in a single argument using the '{model_provider}:{model}' format, for example, 'openai:o1'.

The key required for authenticating with the model's provider. This is usually issued when you sign up for access to the model. Often accessed by setting an 

environment variable

.

Controls the randomness of the model's output. A higher number makes responses more creative; lower ones make them more deterministic.

Limits the total number of 

tokens

in the response, effectively controlling how long the output can be.

The maximum time (in seconds) to wait for a response from the model before canceling the request.

The maximum number of attempts the system will make to resend a request if it fails due to issues like network timeouts or rate limits. Retries use exponential backoff with jitter. Network errors, rate limits (429), and server errors (5xx) are retried automatically. Client errors such as 401 (unauthorized) or 404 are not retried. For long-running [agent](/oss/deepagents/overview) tasks on unreliable networks, consider increasing this to 10–15.

Using `init_chat_model`, pass these parameters as inline 

`**kwargs`

:

```python Initialize using model parameters
model = init_chat_model(
    "claude-sonnet-4-6",
    # Kwargs passed to the model:
    temperature=0.7,
    timeout=30,
    max_tokens=1000,
    max_retries=6,  # Default; increase for unreliable networks
)
```

### Connection resilience

LangChain chat models automatically retry failed API requests with exponential backoff. By default, models retry up to **6 times** for network errors, rate limits (429), and server errors (5xx). Client errors like 401 (unauthorized) or 404 are not retried.

You can adjust `max_retries` and `timeout` when creating a model, then pass that instance to `create_agent`, `create_deep_agent`, or call it standalone:

```python
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "google_genai:gemini-3.6-flash",
    max_retries=10,  # Increase for unreliable networks (default: 6)
    timeout=120,  # Seconds; increase for slow connections
)
```

**Tip:**

For long-running agent graphs on unreliable networks, consider higher `max_retries` (for example 10–15) and a [checkpointer](/oss/langgraph/persistence) so that progress is preserved across failures.

**Info:**

Each chat model integration may have additional params used to control provider-specific functionality.

For example, `ChatOpenAI` has `use_responses_api` to dictate whether to use the OpenAI Responses or Completions API.

To find all the parameters supported by a given chat model, head to the [chat model integrations](/oss/integrations/chat) page.

---

## Invocation

A chat model must be invoked to generate an output. There are three primary invocation methods, each suited to different use cases.

### Invoke

The most straightforward way to call a model is to use `invoke()` with a single message or a list of messages.

```python Single message
response = model.invoke("Why do parrots have colorful feathers?")
print(response)
```

A list of messages can be provided to a chat model to represent conversation history. Each message has a role that models use to indicate who sent the message in the conversation.

See the [messages](/oss/langchain/messages) guide for more detail on roles, types, and content.

```python Dictionary format
conversation = [
    {"role": "system", "content": "You are a helpful assistant that translates English to French."},
    {"role": "user", "content": "Translate: I love programming."},
    {"role": "assistant", "content": "J'adore la programmation."},
    {"role": "user", "content": "Translate: I love building applications."}
]

response = model.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")
```
```python Message objects
from langchain.messages import HumanMessage, AIMessage, SystemMessage

conversation = [
    SystemMessage("You are a helpful assistant that translates English to French."),
    HumanMessage("Translate: I love programming."),
    AIMessage("J'adore la programmation."),
    HumanMessage("Translate: I love building applications.")
]

response = model.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")
```

**Info:**

If the return type of your invocation is a string, ensure that you are using a chat model as opposed to an LLM. Legacy, text-completion LLMs return strings directly. LangChain chat models are prefixed with "Chat", e.g., `ChatOpenAI`(/oss/integrations/chat/openai).

### Stream

Most models can stream their output content while it is being generated. By displaying output progressively, streaming significantly improves user experience, particularly for longer responses.

Calling `stream()` returns an 

iterator

that yields output chunks as they are produced. You can use a loop to process each chunk in real-time:

```python Basic text streaming
for chunk in model.stream("Why do parrots have colorful feathers?"):
    print(chunk.text, end="|", flush=True)
```

```python Stream tool calls, reasoning, and other content
for chunk in model.stream("What color is the sky?"):
    for block in chunk.content_blocks:
        if block["type"] == "reasoning" and (reasoning := block.get("reasoning")):
            print(f"Reasoning: {reasoning}")
        elif block["type"] == "tool_call_chunk":
            print(f"Tool call chunk: {block}")
        elif block["type"] == "text":
            print(block["text"])
        else:
            ...
```

As opposed to [`invoke()`](#invoke), which returns a single `AIMessage` after the model has finished generating its full response, `stream()` returns multiple `AIMessageChunk` objects, each containing a portion of the output text. Importantly, each chunk in a stream is designed to be gathered into a full message via summation:

```python Construct an AIMessage
full = None  # None | AIMessageChunk
for chunk in model.stream("What color is the sky?"):
    full = chunk if full is None else full + chunk
    print(full.text)

# The
# The sky
# The sky is
# The sky is typically
# The sky is typically blue
# ...

print(full.content_blocks)
# [{"type": "text", "text": "The sky is typically blue..."}]
```

The resulting message can be treated the same as a message that was generated with [`invoke()`](#invoke)—for example, it can be aggregated into a message history and passed back to the model as conversational context.

**Warning:**

Streaming only works if all steps in the program know how to process a stream of chunks. For instance, an application that isn't streaming-capable would be one that needs to store the entire output in memory before it can be processed.

**Advanced streaming topics**

**Streaming events**

LangChain chat models can also stream semantic events using `astream_events()`.

This simplifies filtering based on event types and other metadata, and will aggregate the full message in the background. See below for an example.

```python
async for event in model.astream_events("Hello"):

if event["event"] == "on_chat_model_start":
    print(f"Input: {event['data']['input']}")

elif event["event"] == "on_chat_model_stream":
    print(f"Token: {event['data']['chunk'].text}")

elif event["event"] == "on_chat_model_end":
    print(f"Full message: {event['data']['output'].text}")

    else:
        pass
```
```txt
Input: Hello
Token: Hi
Token:  there
Token: !
Token:  How
Token:  can
Token:  I
...
Full message: Hi there! How can I help today?
```

**Tip:**

See the `astream_events()` reference for event types and other details.

**"Auto-streaming" chat models**

LangChain simplifies streaming from chat models by automatically enabling streaming mode in certain cases, even when you're not explicitly calling the streaming methods. This is particularly useful when you use the non-streaming invoke method but still want to stream the entire application, including intermediate results from the chat model.

In [LangGraph agents](/oss/langchain/agents), for example, you can call `model.invoke()` within nodes, but LangChain will automatically delegate to streaming if running in a streaming mode.

#### How it works

When you `invoke()` a chat model, LangChain will automatically switch to an internal streaming mode if it detects that you are trying to stream the overall application. The result of the invocation will be the same as far as the code that was using invoke is concerned; however, while the chat model is being streamed, LangChain will take care of invoking `on_llm_new_token` events in LangChain's callback system.

Callback events allow LangGraph `stream()` and `astream_events()` to surface the chat model's output in real-time.

### Batch

Batching a collection of independent requests to a model can significantly improve performance and reduce costs, as the processing can be done in parallel:

```python Batch
responses = model.batch([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
])
for response in responses:
    print(response)
```

**Note:**

This section describes a chat model method `batch()`, which parallelizes model calls client-side.

It is **distinct** from batch APIs supported by inference providers, such as [OpenAI](https://platform.openai.com/docs/guides/batch) or [Anthropic](https://platform.claude.com/docs/en/build-with-claude/batch-processing#message-batches-api).

By default, `batch()` will only return the final output for the entire batch. If you want to receive the output for each individual input as it finishes generating, you can stream results with `batch_as_completed()`:

```python Yield batch responses upon completion
for response in model.batch_as_completed([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
]):
    print(response)
```

**Note:**

When using `batch_as_completed()`, results may arrive out of order. Each includes the input index for matching to reconstruct the original order as needed.

**Tip:**

When processing a large number of inputs using `batch()` or `batch_as_completed()`, you may want to control the maximum number of parallel calls. This can be done by setting the `max_concurrency` attribute in the `RunnableConfig` dictionary.

```python Batch with max concurrency
model.batch(
    list_of_inputs,
    config={
        'max_concurrency': 5,  # Limit to 5 parallel calls
    }
)
```

See the `RunnableConfig` reference for a full list of supported attributes.

For more details on batching, see the reference.

---

## Tool calling

Models can request to call tools that perform tasks such as fetching data from a database, searching the web, or running code. Tools are pairings of:

1. A schema, including the name of the tool, a description, and/or argument definitions (often a JSON schema)
2. A function or 

coroutine

to execute.

**Note:**

You may hear the term "function calling". We use this interchangeably with "tool calling".

Here's the basic tool calling flow between a user and a model:

```mermaid
sequenceDiagram
    participant U as User
    participant M as Model
    participant T as Tools

U->>M: "What's the weather in SF and NYC?"
M->>M: Analyze request & decide tools needed

par Parallel Tool Calls
    M->>T: get_weather("San Francisco")
    M->>T: get_weather("New York")
end

par Tool Execution
    T-->>M: SF weather data
    T-->>M: NYC weather data
end

    M->>M: Process results & generate response
    M->>U: "SF: 72°F sunny, NYC: 68°F cloudy"
```

To make tools that you have defined available for use by a model, you must bind them using `bind_tools`. In subsequent invocations, the model can choose to call any of the bound tools as needed.

Some model providers offer 

built-in tools

that can be enabled via model or invocation parameters (e.g. [`ChatOpenAI`](/oss/integrations/chat/openai), [`ChatAnthropic`](/oss/integrations/chat/anthropic)). Check the respective [provider reference](/oss/integrations/providers/overview) for details.

**Tip:**

See the [tools guide](/oss/langchain/tools) for details and other options for creating tools.

```python Binding user tools
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."

model_with_tools = model.bind_tools([get_weather])  # [!code highlight]

response = model_with_tools.invoke("What's the weather like in Boston?")
for tool_call in response.tool_calls:
    # View tool calls made by the model
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")
```

When binding user-defined tools, the model's response includes a **request** to execute a tool. When using a model separately from an [agent](/oss/langchain/agents), it is up to you to execute the requested tool and return the result back to the model for use in subsequent reasoning. When using an [agent](/oss/langchain/agents), the agent loop will handle the tool execution loop for you.

Below, we show some common ways you can use tool calling.

**Tool execution loop**

When a model returns tool calls, you need to execute the tools and pass the results back to the model. This creates a conversation loop where the model can use tool results to generate its final response. LangChain includes [agent](/oss/langchain/agents) abstractions that handle this orchestration for you.

Here's a simple example of how to do this:

```python Tool execution loop
# Bind (potentially multiple) tools to the model
tools = [get_weather]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

# Step 1: Model generates tool calls
messages = [{"role": "user", "content": "What's the weather in Boston?"}]
ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)

# Step 2: Execute tools and collect results
for tool_call in ai_msg.tool_calls:
    # Execute the tool with the generated arguments
    tool = tools_by_name[tool_call["name"]]
    tool_result = tool.invoke(tool_call)
    messages.append(tool_result)

# Step 3: Pass results back to model for final response
final_response = model_with_tools.invoke(messages)
print(final_response.text)
# "The current weather in Boston is 72°F and sunny."
```

Each `ToolMessage` returned by the tool includes a `tool_call_id` that matches the original tool call, helping the model correlate results with requests.

**Forcing tool calls**

By default, the model has the freedom to choose which bound tool to use based on the user's input. However, you might want to force choosing a tool, ensuring the model uses either a particular tool or **any** tool from a given list:

```python Force use of any tool
model_with_tools = model.bind_tools([tool_1], tool_choice="any")
```
```python Force use of specific tools
model_with_tools = model.bind_tools([tool_1], tool_choice="tool_1")
```

**Parallel tool calls**

Many models support calling multiple tools in parallel when appropriate. This allows the model to gather information from different sources simultaneously.

```python Parallel tool calls
tools = [get_weather]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

response = model_with_tools.invoke(
    "What's the weather in Boston and Tokyo?"
)

# The model may generate multiple tool calls
print(response.tool_calls)
# [
#   {'name': 'get_weather', 'args': {'location': 'Boston'}, 'id': 'call_1'},
#   {'name': 'get_weather', 'args': {'location': 'Tokyo'}, 'id': 'call_2'},
# ]

# Execute all tools (can be done in parallel with async)
results = []
for tool_call in response.tool_calls:
    tool = tools_by_name[tool_call["name"]]
    result = tool.invoke(tool_call)
    results.append(result)
```

The model intelligently determines when parallel execution is appropriate based on the independence of the requested operations.

**Tip:**

Most models supporting tool calling enable parallel tool calls by default. Some (including [OpenAI](/oss/integrations/chat/openai) and [Anthropic](/oss/integrations/chat/anthropic)) allow you to disable this feature. To do this, set `parallel_tool_calls=False`:
```python
model.bind_tools([get_weather], parallel_tool_calls=False)
```

**Streaming tool calls**

When streaming responses, tool calls are progressively built through `ToolCallChunk`. This allows you to see tool calls as they're being generated rather than waiting for the complete response.

```python Streaming tool calls
for chunk in model_with_tools.stream(
    "What's the weather in Boston and Tokyo?"
):
    # Tool call chunks arrive progressively
    for tool_chunk in chunk.tool_call_chunks:
        if name := tool_chunk.get("name"):
            print(f"Tool: {name}")
        if id_ := tool_chunk.get("id"):
            print(f"ID: {id_}")
        if args := tool_chunk.get("args"):
            print(f"Args: {args}")

# Output:
# Tool: get_weather
# ID: call_SvMlU1TVIZugrFLckFE2ceRE
# Args: {"lo
# Args: catio
# Args: n": "B
# Args: osto
# Args: n"}
# Tool: get_weather
# ID: call_QMZdy6qInx13oWKE7KhuhOLR
# Args: {"lo
# Args: catio
# Args: n": "T
# Args: okyo
# Args: "}
```

You can accumulate chunks to build complete tool calls:

```python Accumulate tool calls
gathered = None
for chunk in model_with_tools.stream("What's the weather in Boston?"):
    gathered = chunk if gathered is None else gathered + chunk
    print(gathered.tool_calls)
```

---

## Structured output

Models can be requested to provide their response in a format matching a given schema. This is useful for ensuring the output can be easily parsed and used in subsequent processing. LangChain supports multiple schema types and methods for enforcing structured output.

**Tip:**

To learn about structured output, see [Structured output](/oss/langchain/structured-output).

**Pydantic**

[Pydantic models](https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage) provide the richest feature set with field validation, descriptions, and nested structures.

```python
from pydantic import BaseModel, Field

class Movie(BaseModel):
    """A movie with details."""
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    director: str = Field(description="The director of the movie")
    rating: float = Field(description="The movie's rating out of 10")

model_with_structure = model.with_structured_output(Movie)
response = model_with_structure.invoke("Provide details about the movie Inception")
print(response)  # Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8)
```

**TypedDict**

Python's `TypedDict` provides a simpler alternative to Pydantic models, ideal when you don't need runtime validation.

```python
from typing_extensions import TypedDict, Annotated

class MovieDict(TypedDict):
    """A movie with details."""
    title: Annotated[str, ..., "The title of the movie"]
    year: Annotated[int, ..., "The year the movie was released"]
    director: Annotated[str, ..., "The director of the movie"]
    rating: Annotated[float, ..., "The movie's rating out of 10"]

model_with_structure = model.with_structured_output(MovieDict)
response = model_with_structure.invoke("Provide details about the movie Inception")
print(response)  # {'title': 'Inception', 'year': 2010, 'director': 'Christopher Nolan', 'rating': 8.8}
```

**JSON Schema**

Provide a [JSON Schema](https://json-schema.org/understanding-json-schema/about) for maximum control and interoperability.

```python
import json

json_schema = {
    "title": "Movie",
    "description": "A movie with details",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "The title of the movie"
        },
        "year": {
            "type": "integer",
            "description": "The year the movie was released"
        },
        "director": {
            "type": "string",
            "description": "The director of the movie"
        },
        "rating": {
            "type": "number",
            "description": "The movie's rating out of 10"
        }
    },
    "required": ["title", "year", "director", "rating"]
}

model_with_structure = model.with_structured_output(
    json_schema,
    method="json_schema",
)
response = model_with_structure.invoke("Provide details about the movie Inception")
print(response)  # {'title': 'Inception', 'year': 2010, ...}
```

**Note:**

**Key considerations for structured output**

- **Method parameter**: Some providers support different methods for structured output:
    - `'json_schema'`: Uses dedicated structured output features offered by the provider.
    - `'function_calling'`: Derives structured output by forcing a [tool call](#tool-calling) that follows the given schema.
    - `'json_mode'`: A precursor to `'json_schema'` offered by some providers. Generates valid JSON, but the schema must be described in the prompt.
- **Include raw**: Set `include_raw=True` to get both the parsed output and the raw AI message.
- **Validation**: Pydantic models provide automatic validation. `TypedDict` and JSON Schema require manual validation.

    See your [provider's integration page](/oss/integrations/providers/overview) for supported methods and configuration options.

**Example: Message output alongside parsed structure**

It can be useful to return the raw `AIMessage` object alongside the parsed representation to access response metadata such as [token counts](#token-usage). To do this, set `include_raw=True` when calling `with_structured_output`:

```python
from pydantic import BaseModel, Field

class Movie(BaseModel):
    """A movie with details."""
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    director: str = Field(description="The director of the movie")
    rating: float = Field(description="The movie's rating out of 10")

model_with_structure = model.with_structured_output(Movie, include_raw=True)  # [!code highlight]
response = model_with_structure.invoke("Provide details about the movie Inception")
response
# {
#     "raw": AIMessage(...),
#     "parsed": Movie(title=..., year=..., ...),
#     "parsing_error": None,
# }
```

**Example: Nested structures**

Schemas can be nested:

```python Pydantic BaseModel
from pydantic import BaseModel, Field

class Actor(BaseModel):
    name: str
    role: str

class MovieDetails(BaseModel):
    title: str
    year: int
    cast: list[Actor]
    genres: list[str]
    budget: float | None = Field(None, description="Budget in millions USD")

model_with_structure = model.with_structured_output(MovieDetails)
```

```python TypedDict
from typing_extensions import Annotated, TypedDict

class Actor(TypedDict):
    name: str
    role: str

class MovieDetails(TypedDict):
    title: str
    year: int
    cast: list[Actor]
    genres: list[str]
    budget: Annotated[float | None, ..., "Budget in millions USD"]

model_with_structure = model.with_structured_output(MovieDetails)
```

---

## Advanced topics

### Model profiles

**Info:**

Model profiles require `langchain>=1.1`.

LangChain chat models can expose a dictionary of supported features and capabilities through a `profile` attribute:

```python
model.profile
# {
#   "max_input_tokens": 400000,
#   "image_inputs": True,
#   "reasoning_output": True,
#   "tool_calling": True,
#   ...
# }
```

Refer to the full set of fields in the [API reference](https://reference.langchain.com/python/langchain-core/language_models/model_profile/ModelProfile).

Much of the model profile data is powered by the [models.dev](https://github.com/sst/models.dev) project, an open source initiative that provides model capability data. These data are augmented with additional fields for purposes of use with LangChain. These augmentations are kept aligned with the upstream project as it evolves.

Model profile data allow applications to work around model capabilities dynamically. For example:

1. [Summarization middleware](/oss/langchain/middleware/built-in#summarization) can trigger summarization based on a model's context window size.
2. [Structured output](/oss/langchain/structured-output) strategies in `create_agent` can be inferred automatically (e.g., by checking support for native structured output features).
3. Model inputs can be gated based on supported [modalities](#multimodal) and maximum input tokens.
4. [Deep Agents Code](/oss/deepagents/code) filters the [interactive model switcher](/oss/deepagents/code/providers#which-models-appear-in-the-switcher) to models whose profiles report `tool_calling` support and text I/O, and displays context window sizes and capability flags in the selector detail view.

**Updating or overwriting profile data**

Model profile data can be changed if it is missing, stale, or incorrect.

**Option 1 (quick fix)**

You can instantiate a chat model with any valid profile:

```python
custom_profile = {
    "max_input_tokens": 100_000,
    "tool_calling": True,
    "structured_output": True,
    # ...
}
model = init_chat_model("...", profile=custom_profile)
```

The `profile` is also a regular `dict` and can be updated in place. If the model instance is shared, consider using `model_copy` to avoid mutating shared state.

```python
new_profile = model.profile | {"key": "value"}
model.model_copy(update={"profile": new_profile})
```

**Option 2 (fix data upstream)**

The primary source for the data is the [models.dev](https://models.dev/) project. This data is merged with additional fields and overrides in LangChain [integration packages](/oss/integrations/providers/overview) and are shipped with those packages.

Model profile data can be updated through the following process:

1. (If needed) update the source data at [models.dev](https://models.dev/) through a pull request to its [repository on GitHub](https://github.com/sst/models.dev).
2. (If needed) update additional fields and overrides in `langchain_<package>/data/profile_augmentations.toml` through a pull request to the LangChain [integration package](/oss/integrations/providers/overview)`.
3. Use the [`langchain-model-profiles`](https://pypi.org/project/langchain-model-profiles/) CLI tool to pull the latest data from [models.dev](https://models.dev/), merge in the augmentations and update the profile data:

        ```bash pip
        pip install -U langchain-model-profiles
        ```

```bash uv
uv add langchain-model-profiles
```

```bash
langchain-profiles refresh --provider <provider> --data-dir <data_dir>
```

This command:
- Downloads the latest data for `<provider>` from models.dev
- Merges augmentations from `profile_augmentations.toml` in `<data_dir>`
- Writes merged profiles to `profiles.py` in `<data_dir>`

    For example: from [`libs/partners/anthropic`](https://github.com/langchain-ai/langchain/tree/master/libs/partners/anthropic) in the [LangChain monorepo](https://github.com/langchain-ai/langchain):

```bash
uv run --with langchain-model-profiles --provider anthropic --data-dir langchain_anthropic/data
```

**Warning:**

Model profiles are a beta feature. The format of a profile is subject to change.

### Multimodal

Certain models can process and return non-textual data such as images, audio, and video. You can pass non-textual data to a model by providing [content blocks](/oss/langchain/messages#message-content).

**Tip:**

All LangChain chat models with underlying multimodal capabilities support:

1. Data in the cross-provider standard format (see [our messages guide](/oss/langchain/messages))
2. OpenAI [chat completions](https://platform.openai.com/docs/api-reference/chat) format
3. Any format that is native to that specific provider (e.g., Anthropic models accept Anthropic native format)

See the [multimodal section](/oss/langchain/messages#multimodal) of the messages guide for details.

Some models

can return multimodal data as part of their response. If invoked to do so, the resulting `AIMessage` will have content blocks with multimodal types.

```python Multimodal output
response = model.invoke("Create a picture of a cat")
print(response.content_blocks)
# [
#     {"type": "text", "text": "Here's a picture of a cat"},
#     {"type": "image", "base64": "...", "mime_type": "image/jpeg"},
# ]
```

See the [integrations page](/oss/integrations/providers/overview) for details on specific providers.

### Reasoning

Many models are capable of performing multi-step reasoning to arrive at a conclusion. This involves breaking down complex problems into smaller, more manageable steps.

**If supported by the underlying model,** you can surface this reasoning process to better understand how the model arrived at its final answer.

```python Stream reasoning output
for chunk in model.stream("Why do parrots have colorful feathers?"):
    reasoning_steps = [r for r in chunk.content_blocks if r["type"] == "reasoning"]
    print(reasoning_steps if reasoning_steps else chunk.text)
```

```python Complete reasoning output
response = model.invoke("Why do parrots have colorful feathers?")
reasoning_steps = [b for b in response.content_blocks if b["type"] == "reasoning"]
print(" ".join(step["reasoning"] for step in reasoning_steps))
```

Depending on the model, you can sometimes specify the level of effort it should put into reasoning. Similarly, you can request that the model turn off reasoning entirely. This may take the form of categorical "tiers" of reasoning (e.g., `'low'` or `'high'`) or integer token budgets.

**Note:**

`reasoning_effort` as a standard parameter requires `langchain-core>=1.5.2`, plus the corresponding partner package version: `langchain-anthropic>=1.5.3`, `langchain-openai>=1.4.1`, `langchain-fireworks>=1.5.2`, `langchain-xai>=1.3.0`, `langchain-google-genai>=4.3.1`, or `langchain-aws>=1.7.0`.

`ChatOpenAI`, `ChatAnthropic`, `ChatFireworks`, `ChatXAI`, `ChatGoogleGenerativeAI`, and [`ChatBedrockConverse`](https://reference.langchain.com/python/langchain-aws/chat_models/bedrock_converse/ChatBedrockConverse) support a standard `reasoning_effort` parameter. Like `temperature`, it can be set at model construction or per invocation, and each provider translates it into its own API format:

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-sonnet-4-6")
response = model.invoke(
    "Why do parrots have colorful feathers?",
    reasoning_effort="high",
)
```

Supported effort levels and the provider's documented default vary by model. Check a model's [profile](#model-profiles) for the levels it supports and its default:

```python
model.profile["reasoning_effort_levels"]  # e.g. ['low', 'medium', 'high']
model.profile["reasoning_effort_default"]  # e.g. 'high'
```

Some providers also accept a native alias for `reasoning_effort` (for example, `ChatAnthropic` accepts `effort` and `ChatGoogleGenerativeAI` accepts `thinking_level`). See the [chat model integrations](/oss/integrations/chat) page for provider-specific detail.

For details, see the [integrations page](/oss/integrations/providers/overview) or [reference](https://reference.langchain.com/python/integrations/) for your respective chat model.

### Local models

LangChain supports running models locally on your own hardware. This is useful for scenarios where either data privacy is critical, you want to invoke a custom model, or when you want to avoid the costs incurred when using a cloud-based model.

[Ollama](/oss/integrations/chat/ollama) is one of the easiest ways to run chat and embedding models locally.

### Prompt caching

Many providers offer prompt caching features to reduce latency and cost on repeat processing of the same tokens. You can engage caching at three levels:

- **Implicit provider caching:** providers automatically pass on cost savings if a request hits a cache, with no configuration required. Examples: [OpenAI](/oss/integrations/chat/openai) and [Gemini](/oss/integrations/chat/google_generative_ai).
- **Provider-level explicit controls:** providers let you manually indicate cache points for greater control or to guarantee cost savings. These mirror the underlying provider/API behavior. Examples:
    - `ChatOpenAI` (via `prompt_cache_key`)
    - Anthropic content-block [`cache_control`](/oss/integrations/chat/anthropic#prompt-caching)
    - [Gemini](https://reference.langchain.com/python/langchain-google-genai).
    - AWS Bedrock [`cachePoint`](/oss/integrations/chat/bedrock#prompt-caching) blocks
- **LangChain middleware:** for agents, middleware lets LangChain optimize caching of stable system prompt and tool content. Examples:
    - Anthropic's [`AnthropicPromptCachingMiddleware`](/oss/integrations/middleware/anthropic#prompt-caching)
    - AWS Bedrock's [`BedrockPromptCachingMiddleware`](/oss/integrations/middleware/aws#prompt-caching)

**Warning:**

Prompt caching is often only engaged above a minimum input token threshold. See [provider pages](/oss/integrations/chat) for details.

Cache usage will be reflected in the [usage metadata](/oss/langchain/messages#token-usage) of the model response.

### Server-side tool use

Some providers support server-side [tool-calling](#tool-calling) loops: models can interact with web search, code interpreters, and other tools and analyze the results in a single conversational turn.

If a model invokes a tool server-side, the content of the response message will include content representing the invocation and result of the tool. Accessing the [content blocks](/oss/langchain/messages#standard-content-blocks) of the response will return the server-side tool calls and results in a provider-agnostic format:

```python Invoke with server-side tool use
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5.4-mini")

tool = {"type": "web_search"}
model_with_tools = model.bind_tools([tool])

response = model_with_tools.invoke("What was a positive news story from today?")
print(response.content_blocks)
```
```python Result expandable
[
    {
        "type": "server_tool_call",
        "name": "web_search",
        "args": {
            "query": "positive news stories today",
            "type": "search"
        },
        "id": "ws_abc123"
    },
    {
        "type": "server_tool_result",
        "tool_call_id": "ws_abc123",
        "status": "success"
    },
    {
        "type": "text",
        "text": "Here are some positive news stories from today...",
        "annotations": [
            {
                "end_index": 410,
                "start_index": 337,
                "title": "article title",
                "type": "citation",
                "url": "..."
            }
        ]
    }
]
```
This represents a single conversational turn; there are no associated [ToolMessage](/oss/langchain/messages#tool-message) objects that need to be passed in as in client-side [tool-calling](#tool-calling).

See the [integration page](/oss/integrations/chat) for your given provider for available tools and usage details.

### Model exceptions

Major integration packages raise standard exception types from `langchain_core.exceptions` for common model failures such as authentication errors, rate limits, and timeouts. These exceptions inherit from both the LangChain base type and the provider SDK's own exception type, so you can catch either one:

```python
from langchain.chat_models import init_chat_model
from langchain_core.exceptions import ModelTimeoutError

model = init_chat_model("openai:gpt-5.6-luna", timeout=0.0001)

try:
    response = model.invoke("Hello")
except ModelTimeoutError:
    print("caught")
```

Each type carries an `is_retryable` attribute that [retry middleware](/oss/langchain/middleware/built-in#model-retry) respects by default.

**Exception types**

- `ModelAuthenticationError` — missing, invalid, or expired API key (not retryable)
- `ModelPermissionDeniedError` — credentials lack permission (not retryable)
- `ModelInvalidRequestError` — provider rejects the request (not retryable)
- `ModelNotFoundError` — requested model not found (not retryable)
- `ModelRateLimitError` — provider rate limit exceeded (retryable)
- `ModelAPIError` — provider server failure (retryable)
- `ModelConnectionError` — provider cannot be reached (retryable)
- `ModelTimeoutError` — request times out (retryable)
- `ContextOverflowError` — input exceeds the model context limit (not retryable)

### Rate limiting

Many chat model providers impose a limit on the number of invocations that can be made in a given time period. If you hit a rate limit, you will typically receive a rate limit error response from the provider, and will need to wait before making more requests.

To help manage rate limits, chat model integrations accept a `rate_limiter` parameter that can be provided during initialization to control the rate at which requests are made.

**Initialize and use a rate limiter**

LangChain comes with (an optional) built-in `InMemoryRateLimiter`. This limiter is thread safe and can be shared by multiple threads in the same process.

```python Define a rate limiter
from langchain.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  # 1 request every 10s
    check_every_n_seconds=0.1,  # Check every 100ms whether allowed to make a request
    max_bucket_size=10,  # Controls the maximum burst size.
)

model = init_chat_model(
    model="gpt-5.5",
    model_provider="openai",
    rate_limiter=rate_limiter  # [!code highlight]
)
```

**Warning:**

The provided rate limiter can only limit the number of requests per unit time. It will not help if you need to also limit based on the size of the requests.

### Base URL and proxy settings

You can configure a custom base URL for providers that implement the OpenAI Chat Completions API.

**Warning:**

`model_provider="openai"` (or direct `ChatOpenAI` usage) targets the official OpenAI API specification. Provider-specific fields from routers and proxies may not be extracted or preserved.

For OpenRouter and LiteLLM, prefer the dedicated integrations:
- [OpenRouter via `ChatOpenRouter`](/oss/integrations/chat/openrouter) (`langchain-openrouter`)
- [LiteLLM via `ChatLiteLLM` / `ChatLiteLLMRouter`](/oss/integrations/chat) (`langchain-litellm`)

**Custom base URL**

Many model providers offer OpenAI-compatible APIs (e.g., [Together AI](https://www.together.ai/), [vLLM](https://github.com/vllm-project/vllm)). You can use `init_chat_model` with these providers by specifying the appropriate `base_url` parameter:

```python
model = init_chat_model(
    model="MODEL_NAME",
    model_provider="openai",
    base_url="BASE_URL",
    api_key="YOUR_API_KEY",
)
```

**Note:**

When using direct chat model class instantiation, the parameter name may vary by provider. Check the respective [reference](/oss/integrations/providers/overview) for details.

**HTTP proxy configuration**

For deployments requiring HTTP proxies, some model integrations support proxy configuration:

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-5.5",
    openai_proxy="http://proxy.example.com:8080"
)
```

**Note:**

Proxy support varies by integration. Check the specific model provider's [reference](/oss/integrations/providers/overview) for proxy configuration options.

### Log probabilities

Certain models can be configured to return token-level log probabilities representing the likelihood of a given token by setting the `logprobs` parameter when initializing the model:

```python
model = init_chat_model(
    model="gpt-5.5",
    model_provider="openai"
).bind(logprobs=True)

response = model.invoke("Why do parrots talk?")
print(response.response_metadata["logprobs"])
```

### Token usage

A number of model providers return token usage information as part of the invocation response. When available, this information will be included on the `AIMessage` objects produced by the corresponding model. For more details, see the [messages](/oss/langchain/messages) guide.

**Note:**

Some provider APIs, notably OpenAI and Azure OpenAI chat completions, require users opt-in to receiving token usage data in streaming contexts. See the [streaming usage metadata](/oss/integrations/chat/openai#streaming-usage-metadata) section of the integration guide for details.

You can track aggregate token counts across models in an application using either a callback or context manager, as shown below:

**Callback handler**

```python
from langchain.chat_models import init_chat_model
from langchain_core.callbacks import UsageMetadataCallbackHandler

model_1 = init_chat_model(model="gpt-5.4-mini")
model_2 = init_chat_model(model="claude-haiku-4-5-20251001")

callback = UsageMetadataCallbackHandler()
result_1 = model_1.invoke("Hello", config={"callbacks": [callback]})
result_2 = model_2.invoke("Hello", config={"callbacks": [callback]})
print(callback.usage_metadata)
```
```python
{
    'gpt-5.4-mini': {
        'input_tokens': 8,
        'output_tokens': 10,
        'total_tokens': 18,
        'input_token_details': {'audio': 0, 'cache_read': 0},
        'output_token_details': {'audio': 0, 'reasoning': 0}
    },
    'claude-haiku-4-5-20251001': {
        'input_tokens': 8,
        'output_tokens': 21,
        'total_tokens': 29,
        'input_token_details': {'cache_read': 0, 'cache_creation': 0}
    }
}
```

**Context manager**

```python
from langchain.chat_models import init_chat_model
from langchain_core.callbacks import get_usage_metadata_callback

model_1 = init_chat_model(model="gpt-5.4-mini")
model_2 = init_chat_model(model="claude-haiku-4-5-20251001")

with get_usage_metadata_callback() as cb:
    model_1.invoke("Hello")
    model_2.invoke("Hello")
    print(cb.usage_metadata)
```
```python
{
    'gpt-5.4-mini': {
        'input_tokens': 8,
        'output_tokens': 10,
        'total_tokens': 18,
        'input_token_details': {'audio': 0, 'cache_read': 0},
        'output_token_details': {'audio': 0, 'reasoning': 0}
    },
    'claude-haiku-4-5-20251001': {
        'input_tokens': 8,
        'output_tokens': 21,
        'total_tokens': 29,
        'input_token_details': {'cache_read': 0, 'cache_creation': 0}
    }
}
```

### Invocation config

When invoking a model, you can pass additional configuration through the `config` parameter using a `RunnableConfig` dictionary. This provides run-time control over execution behavior, callbacks, and metadata tracking.

Common configuration options include:

```python Invocation with config
response = model.invoke(
    "Tell me a joke",
    config={
        "run_name": "joke_generation",      # Custom name for this run
        "tags": ["humor", "demo"],          # Tags for categorization
        "metadata": {"user_id": "123"},     # Custom metadata
        "callbacks": [my_callback_handler], # Callback handlers
    }
)
```

These configuration values are particularly useful when:
- Debugging with [LangSmith](/langsmith/observability) tracing
- Implementing custom logging or monitoring
- Controlling resource usage in production
- Tracking invocations across complex pipelines

**Key configuration attributes**

Identifies this specific invocation in logs and traces. Not inherited by sub-calls.

Labels inherited by all sub-calls for filtering and organization in debugging tools.

Custom key-value pairs for tracking additional context, inherited by all sub-calls.

Controls the maximum number of parallel calls when using `batch()` or `batch_as_completed()`.

Handlers for monitoring and responding to events during execution.

Maximum recursion depth for chains to prevent infinite loops in complex pipelines.

**Tip:**

See full `RunnableConfig` reference for all supported attributes.

### Configurable models

You can also create a runtime-configurable model by specifying `configurable_fields`. If you don't specify a model value, then `'model'` and `'model_provider'` will be configurable by default.

```python
from langchain.chat_models import init_chat_model

configurable_model = init_chat_model(temperature=0)

configurable_model.invoke(
    "what's your name",
    config={"configurable": {"model": "gpt-5-nano"}},  # Run with GPT-5-Nano
)
configurable_model.invoke(
    "what's your name",
    config={"configurable": {"model": "claude-sonnet-4-6"}},  # Run with Claude
)
```

**Configurable model with default values**

We can create a configurable model with default model values, specify which parameters are configurable, and add prefixes to configurable params:

```python
first_model = init_chat_model(
        model="gpt-5.4-mini",
        temperature=0,
        configurable_fields=("model", "model_provider", "temperature", "max_tokens"),
        config_prefix="first",  # Useful when you have a chain with multiple models
)

first_model.invoke("what's your name")
```

```python
first_model.invoke(
    "what's your name",
    config={
        "configurable": {
            "first_model": "claude-sonnet-4-6",
            "first_temperature": 0.5,
            "first_max_tokens": 100,
        }
    },
)
```

See the `init_chat_model` reference for more details on `configurable_fields` and `config_prefix`.

**Using a configurable model declaratively**

We can call declarative operations like `bind_tools`, `with_structured_output`, `with_configurable`, etc. on a configurable model and chain a configurable model in the same way that we would a regularly instantiated chat model object.

```python
from pydantic import BaseModel, Field

class GetWeather(BaseModel):
    """Get the current weather in a given location"""

location: str = Field(description="The city and state, e.g. San Francisco, CA")

class GetPopulation(BaseModel):
    """Get the current population in a given location"""

location: str = Field(description="The city and state, e.g. San Francisco, CA")

model = init_chat_model(temperature=0)
model_with_tools = model.bind_tools([GetWeather, GetPopulation])

model_with_tools.invoke(
    "what's bigger in 2024 LA or NYC", config={"configurable": {"model": "gpt-5.4-mini"}}
).tool_calls
```
```
[
    {
        'name': 'GetPopulation',
        'args': {'location': 'Los Angeles, CA'},
        'id': 'call_Ga9m8FAArIyEjItHmztPYA22',
        'type': 'tool_call'
    },
    {
        'name': 'GetPopulation',
        'args': {'location': 'New York, NY'},
        'id': 'call_jh2dEvBaAHRaw5JUDthOs7rt',
        'type': 'tool_call'
    }
]
```
```python
model_with_tools.invoke(
    "what's bigger in 2024 LA or NYC",
    config={"configurable": {"model": "claude-sonnet-4-6"}},
).tool_calls
```
```
[
    {
        'name': 'GetPopulation',
        'args': {'location': 'Los Angeles, CA'},
        'id': 'toolu_01JMufPf4F4t2zLj7miFeqXp',
        'type': 'tool_call'
    },
    {
        'name': 'GetPopulation',
        'args': {'location': 'New York City, NY'},
        'id': 'toolu_01RQBHcE8kEEbYTuuS8WqY1u',
        'type': 'tool_call'
    }
]
```

### Dynamic model selection

Dynamic models are selected at 

runtime

based on the current 

state

and context. This enables sophisticated routing logic and cost optimization.

To use a dynamic model, create middleware using the `@wrap_model_call` decorator that modifies the model in the request:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

basic_model = ChatOpenAI(model="gpt-5.4-mini")
advanced_model = ChatOpenAI(model="gpt-5.5")

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])

if message_count > 10:
    # Use an advanced model for longer conversations
    model = advanced_model
else:
    model = basic_model

return handler(request.override(model=model))

agent = create_agent(
    model=basic_model,  # Default model
    tools=[],
    middleware=[dynamic_model_selection]
)
```

**Warning:**

Pre-bound models (models with `bind_tools` already called) are not supported when using structured output. If you need dynamic model selection with structured output, ensure the models passed to the middleware are not pre-bound.

**Tip:**

For model configuration details, see [Models](/oss/langchain/models). For dynamic model selection patterns, see [Dynamic model in middleware](/oss/langchain/middleware#dynamic-model).

---

# Custom workflow
> 출처: data/raw/langchain/multi-agent/custom-workflow.mdx | https://docs.langchain.com/oss/python/langchain/multi-agent/custom-workflow

In the **custom workflow** architecture, you define your own bespoke execution flow using [LangGraph](/oss/langgraph/overview). You have complete control over the graph structure—including sequential steps, conditional branches, loops, and parallel execution.

```mermaid
graph LR
    A([Input]) --> B{{Conditional}}
    B -->|path_a| C[Deterministic step]
    B -->|path_b| D((Agentic step))
    C --> G([Output])
    D --> G([Output])

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
classDef decision fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F

    class A,G trigger
    class C,D process
    class B decision
```

## Key characteristics

* Complete control over graph structure
* Mix deterministic logic with agentic behavior
* Support for sequential steps, conditional branches, loops, and parallel execution
* Embed other patterns as nodes in your workflow

## When to use

Use custom workflows when standard patterns (subagents, skills, etc.) don't fit your requirements, you need to mix deterministic logic with agentic behavior, or your use case requires complex routing or multi-stage processing.

Each node in your workflow can be a simple function, an LLM call, or an entire [agent](/oss/langchain/agents) with [tools](/oss/langchain/tools). You can also compose other architectures within a custom workflow—for example, embedding a multi-agent system as a single node.

For a complete example of a custom workflow, see the tutorial below.

- [Tutorial: Build a multi-source knowledge base with routing](/oss/langchain/multi-agent/router-knowledge-base)

    The [router pattern](/oss/langchain/multi-agent/router) is an example of a custom workflow. This tutorial walks through building a router that queries GitHub, Notion, and Slack in parallel, then synthesizes results.
>

## Basic implementation

The core insight is that you can call a LangChain agent directly inside any LangGraph node, combining the flexibility of custom workflows with the convenience of prebuilt agents:

```python
from langchain.agents import create_agent
from langgraph.graph import StateGraph, START, END

agent = create_agent(model="openai:gpt-5.5", tools=[...])

def agent_node(state: State) -> dict:
    """A LangGraph node that invokes a LangChain agent."""
    result = agent.invoke({
        "messages": [{"role": "user", "content": state["query"]}]
    })
    return {"answer": result["messages"][-1].content}

# Build a simple workflow
workflow = (
    StateGraph(State)
    .add_node("agent", agent_node)
    .add_edge(START, "agent")
    .add_edge("agent", END)
    .compile()
)
```

## Example: RAG pipeline

A common use case is combining [retrieval](/oss/deepagents/retrieval) with an agent. This example builds a WNBA stats assistant that retrieves from a knowledge base and can fetch live news.

**Custom RAG workflow**

The workflow demonstrates three types of nodes:

- **Model node** (Rewrite): Rewrites the user query for better retrieval using [structured output](/oss/langchain/structured-output).
- **Deterministic node** (Retrieve): Performs vector similarity search — no LLM involved.
- **Agent node** (Agent): Reasons over retrieved context and can fetch additional information via tools.

```mermaid
graph LR
    A([Query]) --> B{{Rewrite}}
    B --> C[(Retrieve)]
    C --> D((Agent))
    D --> E([Response])

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,E trigger
    class B,C,D process
```

**Tip:**

You can use LangGraph state to pass information between workflow steps. This allows each part of your workflow to read and update structured fields, making it easy to share data and context across nodes.

```python
from typing import TypedDict
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

class State(TypedDict):
    question: str
    rewritten_query: str
    documents: list[str]
    answer: str

# WNBA knowledge base with rosters, game results, and player stats
embeddings = OpenAIEmbeddings()
vector_store = InMemoryVectorStore(embeddings)
vector_store.add_texts([
    # Rosters
    "New York Liberty 2024 roster: Breanna Stewart, Sabrina Ionescu, Jonquel Jones, Courtney Vandersloot.",
    "Las Vegas Aces 2024 roster: A'ja Wilson, Kelsey Plum, Jackie Young, Chelsea Gray.",
    "Indiana Fever 2024 roster: Caitlin Clark, Aliyah Boston, Kelsey Mitchell, NaLyssa Smith.",
    # Game results
    "2024 WNBA Finals: New York Liberty defeated Minnesota Lynx 3-2 to win the championship.",
    "June 15, 2024: Indiana Fever 85, Chicago Sky 79. Caitlin Clark had 23 points and 8 assists.",
    "August 20, 2024: Las Vegas Aces 92, Phoenix Mercury 84. A'ja Wilson scored 35 points.",
    # Player stats
    "A'ja Wilson 2024 season stats: 26.9 PPG, 11.9 RPG, 2.6 BPG. Won MVP award.",
    "Caitlin Clark 2024 rookie stats: 19.2 PPG, 8.4 APG, 5.7 RPG. Won Rookie of the Year.",
    "Breanna Stewart 2024 stats: 20.4 PPG, 8.5 RPG, 3.5 APG.",
])
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

@tool
def get_latest_news(query: str) -> str:
    """Get the latest WNBA news and updates."""
    # Your news API here
    return "Latest: The WNBA announced expanded playoff format for 2025..."

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[get_latest_news],
)

model = ChatOpenAI(model="gpt-5.5")

class RewrittenQuery(BaseModel):
    query: str

def rewrite_query(state: State) -> dict:
    """Rewrite the user query for better retrieval."""
    system_prompt = """Rewrite this query to retrieve relevant WNBA information.
The knowledge base contains: team rosters, game results with scores, and player statistics (PPG, RPG, APG).
Focus on specific player names, team names, or stat categories mentioned."""
    response = model.with_structured_output(RewrittenQuery).invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": state["question"]}
    ])
    return {"rewritten_query": response.query}

def retrieve(state: State) -> dict:
    """Retrieve documents based on the rewritten query."""
    docs = retriever.invoke(state["rewritten_query"])
    return {"documents": [doc.page_content for doc in docs]}

def call_agent(state: State) -> dict:
    """Generate answer using retrieved context."""
    context = "\n\n".join(state["documents"])
    prompt = f"Context:\n{context}\n\nQuestion: {state['question']}"
    response = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    return {"answer": response["messages"][-1].content_blocks}

workflow = (
    StateGraph(State)
    .add_node("rewrite", rewrite_query)
    .add_node("retrieve", retrieve)
    .add_node("agent", call_agent)
    .add_edge(START, "rewrite")
    .add_edge("rewrite", "retrieve")
    .add_edge("retrieve", "agent")
    .add_edge("agent", END)
    .compile()
)

result = workflow.invoke({"question": "Who won the 2024 WNBA Championship?"})
print(result["answer"])
```

**Info:**

In production, use a persistent vector store such as [Valkey](/oss/integrations/vectorstores/valkey), [Databricks Vector Search](/oss/integrations/vectorstores/databricks_vector_search), or [MongoDB Atlas](/oss/integrations/vectorstores/mongodb_atlas) instead of `InMemoryVectorStore`. See [all vector stores](/oss/integrations/vectorstores).

---

# Build customer support with handoffs
> 출처: data/raw/langchain/multi-agent/handoffs-customer-support.mdx | https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs-customer-support

The [state machine pattern](/oss/langchain/multi-agent/handoffs) describes workflows where an agent's behavior changes as it moves through different states of a task. This tutorial shows how to implement a state machine by using tool calls to dynamically change a single agent's configuration—updating its available tools and instructions based on the current state. The state can be determined from multiple sources: the agent's past actions (tool calls), external state (such as API call results), or even initial user input (for example, by running a classifier to determine user intent).

In this tutorial, you'll build a customer support agent that does the following:

- Collects warranty information before proceeding.
- Classifies issues as hardware or software.
- Provides solutions or escalates to human support.
- Maintains conversation state across multiple turns.

Unlike the [subagents pattern](/oss/langchain/multi-agent/subagents-personal-assistant) where sub-agents are called as tools, the **state machine pattern** uses a single agent whose configuration changes based on workflow progress. Each "step" is just a different configuration (system prompt + tools) of the same underlying agent, selected dynamically based on state.

Here's the workflow we'll build:

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'primaryColor':'#E5F4FF','primaryTextColor':'#030710','primaryBorderColor':'#006DDD','lineColor':'#40668D','secondaryColor':'#F6FFDB','tertiaryColor':'#FDF3FF'}}}%%
flowchart TD
    %% Start
    Start([💬 Customer reports<br>an issue]) --> Warranty{Is the device<br>under warranty?}

%% Warranty check
Warranty -->|✅ Yes| IssueType{What type<br>of issue?}
Warranty -->|❌ No| OutOfWarranty{What type<br>of issue?}

%% In-Warranty branch
IssueType -->|🔩 Hardware| Repair[Provide warranty<br>repair instructions]
IssueType -->|💻 Software| Troubleshoot[Provide troubleshooting<br>steps]

%% Out-of-Warranty branch
OutOfWarranty -->|🔩 Hardware| Escalate[Escalate to human<br>for paid repair options]
OutOfWarranty -->|💻 Software| Troubleshoot

%% Troubleshooting follow-up
Troubleshoot --> Close([✅ Issue Resolved])
Repair --> Close
Escalate --> Close

%% === Styling ===
classDef startEnd fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef decisionNode fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
classDef actionNode fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
classDef escalateNode fill:#F8E8E6,stroke:#B27D75,stroke-width:2px,color:#634643

    class Start,Close startEnd
    class Warranty,IssueType,OutOfWarranty decisionNode
    class Repair,Troubleshoot actionNode
    class Escalate escalateNode
```

## Setup

### Installation

This tutorial requires the `langchain` package:

```bash pip
pip install langchain
```
```bash uv
uv add langchain
```
```bash conda
conda install langchain -c conda-forge
```

For more details, see our [Installation guide](/oss/langchain/install).

### LangSmith

Set up [LangSmith](https://smith.langchain.com) to inspect what is happening inside your agent. Then set the following environment variables:

```bash Shell
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```
```python Python
import getpass
import os

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass()
```

### Select an LLM

Select a chat model from LangChain's suite of integrations:

**OpenAI**

👉 Read the [OpenAI chat model integration docs](/oss/python/integrations/chat/openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-5.5")
```
```python Model Class
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-..."

model = ChatOpenAI(model="gpt-5.5")
```

**Anthropic**

👉 Read the [Anthropic chat model integration docs](/oss/python/integrations/chat/anthropic/)

```bash pip
pip install -U "langchain[anthropic]"
```

```bash uv
uv add "langchain[anthropic]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = init_chat_model("claude-sonnet-4-6")
```
```python Model Class
import os
from langchain_anthropic import ChatAnthropic

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = ChatAnthropic(model="claude-sonnet-4-6")
```

**Azure**

👉 Read the [Azure chat model integration docs](/oss/python/integrations/chat/azure_chat_openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = init_chat_model(
    "azure_openai:gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
```
```python Model Class
import os
from langchain_openai import AzureChatOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = AzureChatOpenAI(
    model="gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
)
```

**Google Gemini**

👉 Read the [Google GenAI chat model integration docs](/oss/python/integrations/chat/google_generative_ai/)

```bash pip
pip install -U "langchain[google-genai]"
```

```bash uv
uv add "langchain[google-genai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["GOOGLE_API_KEY"] = "..."

model = init_chat_model("google_genai:gemini-3.7-flash")
```
```python Model Class
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "..."

model = ChatGoogleGenerativeAI(model="gemini-3.7-flash")
```

**AWS Bedrock**

👉 Read the [AWS Bedrock chat model integration docs](/oss/python/integrations/chat/bedrock/)

```bash pip
pip install -U "langchain[aws]"
```

```bash uv
uv add "langchain[aws]"
```

```python init_chat_model
from langchain.chat_models import init_chat_model

# Follow the steps here to configure your credentials:
# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html

model = init_chat_model(
    "us.anthropic.claude-sonnet-4-6",
    model_provider="bedrock_converse",
)
```
```python Model Class
from langchain_aws import ChatBedrock

model = ChatBedrock(model="us.anthropic.claude-sonnet-4-6")
```

**HuggingFace**

👉 Read the [HuggingFace chat model integration docs](/oss/python/integrations/chat/huggingface/)

```bash pip
pip install -U "langchain[huggingface]"
```

```bash uv
uv add "langchain[huggingface]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

model = init_chat_model(
    "microsoft/Phi-3-mini-4k-instruct",
    model_provider="huggingface",
    temperature=0.7,
    max_tokens=1024,
)
```

```python Model Class
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    temperature=0.7,
    max_length=1024,
)
model = ChatHuggingFace(llm=llm)
```

**OpenRouter**

👉 Read the [OpenRouter chat model integration docs](/oss/python/integrations/chat/openrouter/)

```bash pip
pip install -U "langchain-openrouter"
```

```bash uv
uv add "langchain-openrouter"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = init_chat_model(
    "auto",
    model_provider="openrouter",
)
```
```python Model Class
import os
from langchain_openrouter import ChatOpenRouter

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = ChatOpenRouter(model="auto")
```

## 1. Define custom state

First, define a custom state schema that tracks which step is currently active:

```python
from langchain.agents import AgentState
from typing_extensions import NotRequired
from typing import Literal

# Define the possible workflow steps
SupportStep = Literal["warranty_collector", "issue_classifier", "resolution_specialist"]  # [!code highlight]

class SupportState(AgentState):  # [!code highlight]
    """State for customer support workflow."""
    current_step: NotRequired[SupportStep]  # [!code highlight]
    warranty_status: NotRequired[Literal["in_warranty", "out_of_warranty"]]
    issue_type: NotRequired[Literal["hardware", "software"]]
```

The `current_step` field is the core of the state machine pattern - it determines which configuration (prompt + tools) is loaded on each turn.

## 2. Create tools that manage workflow state

Create tools that update the workflow state. These tools allow the agent to record information and transition to the next step.

The key is using `Command` to update state, including the `current_step` field:

```python
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langgraph.types import Command

@tool
def record_warranty_status(
    status: Literal["in_warranty", "out_of_warranty"],
    runtime: ToolRuntime[None, SupportState],
) -> Command:  # [!code highlight]
    """Record the customer's warranty status and transition to issue classification."""
    return Command(  # [!code highlight]
        update={  # [!code highlight]
            "messages": [
                ToolMessage(
                    content=f"Warranty status recorded as: {status}",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
            "warranty_status": status,
            "current_step": "issue_classifier",  # [!code highlight]
        }
    )

@tool
def record_issue_type(
    issue_type: Literal["hardware", "software"],
    runtime: ToolRuntime[None, SupportState],
) -> Command:  # [!code highlight]
    """Record the type of issue and transition to resolution specialist."""
    return Command(  # [!code highlight]
        update={  # [!code highlight]
            "messages": [
                ToolMessage(
                    content=f"Issue type recorded as: {issue_type}",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
            "issue_type": issue_type,
            "current_step": "resolution_specialist",  # [!code highlight]
        }
    )

@tool
def escalate_to_human(reason: str) -> str:
    """Escalate the case to a human support specialist."""
    # In a real system, this would create a ticket, notify staff, etc.
    return f"Escalating to human support. Reason: {reason}"

@tool
def provide_solution(solution: str) -> str:
    """Provide a solution to the customer's issue."""
    return f"Solution provided: {solution}"
```

Notice how `record_warranty_status` and `record_issue_type` return `Command` objects that update both the data (`warranty_status`, `issue_type`) AND the `current_step`. This is how the state machine works - tools control workflow progression.

## 3. Define step configurations

Define prompts and tools for each step. First, define the prompts for each step:

**View complete prompt definitions**

```python
# Define prompts as constants for easy reference
WARRANTY_COLLECTOR_PROMPT = """You are a customer support agent helping with device issues.

CURRENT STAGE: Warranty verification

At this step, you need to:
1. Greet the customer warmly
2. Ask if their device is under warranty
3. Use record_warranty_status to record their response and move to the next step

Be conversational and friendly. Don't ask multiple questions at once."""

ISSUE_CLASSIFIER_PROMPT = """You are a customer support agent helping with device issues.

CURRENT STAGE: Issue classification
CUSTOMER INFO: Warranty status is {warranty_status}

At this step, you need to:
1. Ask the customer to describe their issue
2. Determine if it's a hardware issue (physical damage, broken parts) or software issue (app crashes, performance)
3. Use record_issue_type to record the classification and move to the next step

If unclear, ask clarifying questions before classifying."""

RESOLUTION_SPECIALIST_PROMPT = """You are a customer support agent helping with device issues.

CURRENT STAGE: Resolution
CUSTOMER INFO: Warranty status is {warranty_status}, issue type is {issue_type}

At this step, you need to:
1. For SOFTWARE issues: provide troubleshooting steps using provide_solution
2. For HARDWARE issues:
   - If IN WARRANTY: explain warranty repair process using provide_solution
   - If OUT OF WARRANTY: escalate_to_human for paid repair options

Be specific and helpful in your solutions."""
```

Then map step names to their configurations using a dictionary:

```python
# Step configuration: maps step name to (prompt, tools, required_state)
STEP_CONFIG = {
    "warranty_collector": {
        "prompt": WARRANTY_COLLECTOR_PROMPT,
        "tools": [record_warranty_status],
        "requires": [],
    },
    "issue_classifier": {
        "prompt": ISSUE_CLASSIFIER_PROMPT,
        "tools": [record_issue_type],
        "requires": ["warranty_status"],
    },
    "resolution_specialist": {
        "prompt": RESOLUTION_SPECIALIST_PROMPT,
        "tools": [provide_solution, escalate_to_human],
        "requires": ["warranty_status", "issue_type"],
    },
}
```

This dictionary-based configuration makes it easy to:
- See all steps at a glance
- Add new steps (just add another entry)
- Understand the workflow dependencies (`requires` field)
- Use prompt templates with state variables (e.g., `{warranty_status}`)

## 4. Create step-based middleware

Create middleware that reads `current_step` from state and applies the appropriate configuration. We'll use the `@wrap_model_call` decorator for a clean implementation:

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@wrap_model_call  # [!code highlight]
def apply_step_config(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """Configure agent behavior based on the current step."""
    # Get current step (defaults to warranty_collector for first interaction)
    current_step = request.state.get("current_step", "warranty_collector")  # [!code highlight]

# Look up step configuration
stage_config = STEP_CONFIG[current_step]  # [!code highlight]

# Validate required state exists
for key in stage_config["requires"]:
    if request.state.get(key) is None:
        raise ValueError(f"{key} must be set before reaching {current_step}")

# Format prompt with state values (supports {warranty_status}, {issue_type}, etc.)
system_prompt = stage_config["prompt"].format(**request.state)

# Inject system prompt and step-specific tools
request = request.override(  # [!code highlight]
    system_prompt=system_prompt,  # [!code highlight]
    tools=stage_config["tools"],  # [!code highlight]
)

    return handler(request)
```

This middleware:

1. **Reads current step**: Gets `current_step` from state (defaults to "warranty_collector").
2. **Looks up configuration**: Finds the matching entry in `STEP_CONFIG`.
3. **Validates dependencies**: Ensures required state fields exist.
4. **Formats prompt**: Injects state values into the prompt template.
5. **Applies configuration**: Overrides the system prompt and available tools.

The `request.override()` method is key - it allows us to dynamically change the agent's behavior based on state without creating separate agent instances.

## 5. Create the agent

Now create the agent with the step-based middleware and a checkpointer for state persistence:

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# Collect all tools from all step configurations
all_tools = [
    record_warranty_status,
    record_issue_type,
    provide_solution,
    escalate_to_human,
]

# Create the agent with step-based configuration
agent = create_agent(
    model,
    tools=all_tools,
    state_schema=SupportState,  # [!code highlight]
    middleware=[apply_step_config],  # [!code highlight]
    checkpointer=InMemorySaver(),  # [!code highlight]
)
```

**Note:**

**Why a checkpointer?** The checkpointer maintains state across conversation turns. Without it, the `current_step` state would be lost between user messages, breaking the workflow.

## 6. Test the workflow

Test the complete workflow:

```python
from langchain.messages import HumanMessage
from langchain_core.utils.uuid import uuid7

# Configuration for this conversation thread
thread_id = str(uuid7())
config = {"configurable": {"thread_id": thread_id}}

# Turn 1: Initial message - starts with warranty_collector step
print("=== Turn 1: Warranty Collection ===")
result = agent.invoke(
    {"messages": [HumanMessage("Hi, my phone screen is cracked")]},
    config
)
for msg in result['messages']:
    msg.pretty_print()

# Turn 2: User responds about warranty
print("\n=== Turn 2: Warranty Response ===")
result = agent.invoke(
    {"messages": [HumanMessage("Yes, it's still under warranty")]},
    config
)
for msg in result['messages']:
    msg.pretty_print()
print(f"Current step: {result.get('current_step')}")

# Turn 3: User describes the issue
print("\n=== Turn 3: Issue Description ===")
result = agent.invoke(
    {"messages": [HumanMessage("The screen is physically cracked from dropping it")]},
    config
)
for msg in result['messages']:
    msg.pretty_print()
print(f"Current step: {result.get('current_step')}")

# Turn 4: Resolution
print("\n=== Turn 4: Resolution ===")
result = agent.invoke(
    {"messages": [HumanMessage("What should I do?")]},
    config
)
for msg in result['messages']:
    msg.pretty_print()
```

Expected flow:
1. **Warranty verification step**: Asks about warranty status
2. **Issue classification step**: Asks about the problem, determines it's hardware
3. **Resolution step**: Provides warranty repair instructions

## 7. Understanding state transitions

Let's trace what happens at each turn:

### Turn 1: Initial message

```python
{
    "messages": [HumanMessage("Hi, my phone screen is cracked")],
    "current_step": "warranty_collector"  # Default value
}
```

Middleware applies:
- System prompt: `WARRANTY_COLLECTOR_PROMPT`
- Tools: `[record_warranty_status]`

### Turn 2: After warranty recorded

Tool call: `record_warranty_status("in_warranty")` returns:
```python
Command(update={
    "warranty_status": "in_warranty",
    "current_step": "issue_classifier"  # State transition!
})
```

Next turn, middleware applies:
- System prompt: `ISSUE_CLASSIFIER_PROMPT` (formatted with `warranty_status="in_warranty"`)
- Tools: `[record_issue_type]`

### Turn 3: After issue classified

Tool call: `record_issue_type("hardware")` returns:
```python
Command(update={
    "issue_type": "hardware",
    "current_step": "resolution_specialist"  # State transition!
})
```

Next turn, middleware applies:
- System prompt: `RESOLUTION_SPECIALIST_PROMPT` (formatted with `warranty_status` and `issue_type`)
- Tools: `[provide_solution, escalate_to_human]`

The key insight: **Tools drive the workflow** by updating `current_step`, and **middleware responds** by applying the appropriate configuration on the next turn.

## 8. Manage message history

As the agent progresses through steps, message history grows. Use [summarization middleware](/oss/langchain/short-term-memory#summarize-messages) to compress earlier messages while preserving conversational context:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware  # [!code highlight]
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model,
    tools=all_tools,
    state_schema=SupportState,
    middleware=[
        apply_step_config,
        SummarizationMiddleware(  # [!code highlight]
            model="gpt-5.4-mini",
            trigger=("tokens", 4000),
            keep=("messages", 10)
        )
    ],
    checkpointer=InMemorySaver(),
)
```

See the [short-term memory guide](/oss/langchain/short-term-memory) for other memory management techniques.

## 9. Add flexibility: Go back

Some workflows need to allow users to return to previous steps to correct information (e.g., changing warranty status or issue classification). However, not all transitions make sense—for example, you typically can't go back once a refund has been processed. For this support workflow, we'll add tools to return to the warranty verification and issue classification steps.

**Tip:**

If your workflow requires arbitrary transitions between most steps, consider whether you need a structured workflow at all. This pattern works best when steps follow a clear sequential progression with occasional backwards transitions for corrections.

Add "go back" tools to the resolution step:

```python
@tool
def go_back_to_warranty() -> Command:  # [!code highlight]
    """Go back to warranty verification step."""
    return Command(update={"current_step": "warranty_collector"})  # [!code highlight]

@tool
def go_back_to_classification() -> Command:  # [!code highlight]
    """Go back to issue classification step."""
    return Command(update={"current_step": "issue_classifier"})  # [!code highlight]

# Update the resolution_specialist configuration to include these tools
STEP_CONFIG["resolution_specialist"]["tools"].extend([
    go_back_to_warranty,
    go_back_to_classification
])
```

Update the resolution specialist's prompt to mention these tools:

```python
RESOLUTION_SPECIALIST_PROMPT = """You are a customer support agent helping with device issues.

CURRENT STAGE: Resolution
CUSTOMER INFO: Warranty status is {warranty_status}, issue type is {issue_type}

At this step, you need to:
1. For SOFTWARE issues: provide troubleshooting steps using provide_solution
2. For HARDWARE issues:
   - If IN WARRANTY: explain warranty repair process using provide_solution
   - If OUT OF WARRANTY: escalate_to_human for paid repair options

If the customer indicates any information was wrong, use:
- go_back_to_warranty to correct warranty status
- go_back_to_classification to correct issue type

Be specific and helpful in your solutions."""
```

Now the agent can handle corrections:

```python
result = agent.invoke(
    {"messages": [HumanMessage("Actually, I made a mistake - my device is out of warranty")]},
    config
)
# Agent will call go_back_to_warranty and restart the warranty verification step
```

## Complete example

Here's everything together in a runnable script:

**Complete code**

```python
"""
Customer Support State Machine Example

This example demonstrates the state machine pattern.
A single agent dynamically changes its behavior based on the current_step state,
creating a state machine for sequential information collection.
"""

from langchain_core.utils.uuid import uuid7

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from typing import Callable, Literal
from typing_extensions import NotRequired

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse, SummarizationMiddleware
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import tool, ToolRuntime

model = init_chat_model("google_genai:gemini-3.6-flash")

# Define the possible workflow steps
SupportStep = Literal["warranty_collector", "issue_classifier", "resolution_specialist"]

class SupportState(AgentState):
    """State for customer support workflow."""

current_step: NotRequired[SupportStep]
warranty_status: NotRequired[Literal["in_warranty", "out_of_warranty"]]
issue_type: NotRequired[Literal["hardware", "software"]]

@tool
def record_warranty_status(
    status: Literal["in_warranty", "out_of_warranty"],
    runtime: ToolRuntime[None, SupportState],
) -> Command:
    """Record the customer's warranty status and transition to issue classification."""
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content=f"Warranty status recorded as: {status}",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
            "warranty_status": status,
            "current_step": "issue_classifier",
        }
    )

@tool
def record_issue_type(
    issue_type: Literal["hardware", "software"],
    runtime: ToolRuntime[None, SupportState],
) -> Command:
    """Record the type of issue and transition to resolution specialist."""
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content=f"Issue type recorded as: {issue_type}",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
            "issue_type": issue_type,
            "current_step": "resolution_specialist",
        }
    )

@tool
def escalate_to_human(reason: str) -> str:
    """Escalate the case to a human support specialist."""
    # In a real system, this would create a ticket, notify staff, etc.
    return f"Escalating to human support. Reason: {reason}"

@tool
def provide_solution(solution: str) -> str:
    """Provide a solution to the customer's issue."""
    return f"Solution provided: {solution}"

# Define prompts as constants
WARRANTY_COLLECTOR_PROMPT = """You are a customer support agent helping with device issues.

CURRENT STEP: Warranty verification

At this step, you need to:
1. Greet the customer warmly
2. Ask if their device is under warranty
3. Use record_warranty_status to record their response and move to the next step

Be conversational and friendly. Don't ask multiple questions at once."""

ISSUE_CLASSIFIER_PROMPT = """You are a customer support agent helping with device issues.

CURRENT STEP: Issue classification
CUSTOMER INFO: Warranty status is {warranty_status}

At this step, you need to:
1. Ask the customer to describe their issue
2. Determine if it's a hardware issue (physical damage, broken parts) or software issue (app crashes, performance)
3. Use record_issue_type to record the classification and move to the next step

If unclear, ask clarifying questions before classifying."""

RESOLUTION_SPECIALIST_PROMPT = """You are a customer support agent helping with device issues.

CURRENT STEP: Resolution
CUSTOMER INFO: Warranty status is {warranty_status}, issue type is {issue_type}

At this step, you need to:
1. For SOFTWARE issues: provide troubleshooting steps using provide_solution
2. For HARDWARE issues:
   - If IN WARRANTY: explain warranty repair process using provide_solution
   - If OUT OF WARRANTY: escalate_to_human for paid repair options

Be specific and helpful in your solutions."""

# Step configuration: maps step name to (prompt, tools, required_state)
STEP_CONFIG = {
    "warranty_collector": {
        "prompt": WARRANTY_COLLECTOR_PROMPT,
        "tools": [record_warranty_status],
        "requires": [],
    },
    "issue_classifier": {
        "prompt": ISSUE_CLASSIFIER_PROMPT,
        "tools": [record_issue_type],
        "requires": ["warranty_status"],
    },
    "resolution_specialist": {
        "prompt": RESOLUTION_SPECIALIST_PROMPT,
        "tools": [provide_solution, escalate_to_human],
        "requires": ["warranty_status", "issue_type"],
    },
}

@wrap_model_call
def apply_step_config(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """Configure agent behavior based on the current step."""
    # Get current step (defaults to warranty_collector for first interaction)
    current_step = request.state.get("current_step", "warranty_collector")

# Look up step configuration
step_config = STEP_CONFIG[current_step]

# Validate required state exists
for key in step_config["requires"]:
    if request.state.get(key) is None:
        raise ValueError(f"{key} must be set before reaching {current_step}")

# Format prompt with state values
system_prompt = step_config["prompt"].format(**request.state)

# Inject system prompt and step-specific tools
request = request.override(
    system_prompt=system_prompt,
    tools=step_config["tools"],
)

return handler(request)

# Collect all tools from all step configurations
all_tools = [
    record_warranty_status,
    record_issue_type,
    provide_solution,
    escalate_to_human,
]

# Create the agent with step-based configuration and summarization
agent = create_agent(
    model,
    tools=all_tools,
    state_schema=SupportState,
    middleware=[
        apply_step_config,
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=("tokens", 4000),
            keep=("messages", 10)
        )
    ],
    checkpointer=InMemorySaver(),
)

# ============================================================================
# Test the workflow
# ============================================================================

if __name__ == "__main__":
    thread_id = str(uuid7())
    config = {"configurable": {"thread_id": thread_id}}

result = agent.invoke(
    {"messages": [HumanMessage("Hi, my phone screen is cracked")]},
    config
)

result = agent.invoke(
    {"messages": [HumanMessage("Yes, it's still under warranty")]},
    config
)

result = agent.invoke(
    {"messages": [HumanMessage("The screen is physically cracked from dropping it")]},
    config
)

    result = agent.invoke(
        {"messages": [HumanMessage("What should I do?")]},
        config
    )
    for msg in result['messages']:
        msg.pretty_print()
```

## Next steps

- Learn about the [subagents pattern](/oss/langchain/multi-agent/subagents-personal-assistant) for centralized orchestration
- Explore [middleware](/oss/langchain/middleware) for more dynamic behaviors
- Read the [multi-agent overview](/oss/langchain/multi-agent) to compare patterns
- Use [LangSmith](https://smith.langchain.com) to debug and monitor your multi-agent system

---

# Handoffs
> 출처: data/raw/langchain/multi-agent/handoffs.mdx | https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs

In the **handoffs** architecture, behavior changes dynamically based on state. The core mechanism: [tools](/oss/langchain/tools) update a state variable (e.g., `current_step` or `active_agent`) that persists across turns, and the system reads this variable to adjust behavior—either applying different configuration (system prompt, tools) or routing to a different [agent](/oss/langchain/agents). This pattern supports both handoffs between distinct agents and dynamic configuration changes within a single agent.

**Tip:**

The term **handoffs** was coined by [OpenAI](https://openai.github.io/openai-agents-python/handoffs/) for using tool calls (e.g., `transfer_to_sales_agent`) to transfer control between agents or states.

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant Workflow State

User->>Agent: "My phone is broken"
Note over Agent,Workflow State: Step: Get warranty status<br/>Tools: record_warranty_status
Agent-->>User: "Is your device under warranty?"

User->>Agent: "Yes, it's still under warranty"
Agent->>Workflow State: record_warranty_status("in_warranty")
Note over Agent,Workflow State: Step: Classify issue<br/>Tools: record_issue_type
Agent-->>User: "Can you describe the issue?"

    User->>Agent: "The screen is cracked"
    Agent->>Workflow State: record_issue_type("hardware")
    Note over Agent,Workflow State: Step: Provide resolution<br/>Tools: provide_solution, escalate_to_human
    Agent-->>User: "Here's the warranty repair process..."
```

## Key characteristics

* State-driven behavior: Behavior changes based on a state variable (e.g., `current_step` or `active_agent`)
* Tool-based transitions: Tools update the state variable to move between states
* Direct user interaction: Each state's configuration handles user messages directly
* Persistent state: State survives across conversation turns

## When to use

Use the handoffs pattern when you need to enforce sequential constraints (unlock capabilities only after preconditions are met), the agent needs to converse directly with the user across different states, or you're building multi-stage conversational flows. This pattern is particularly valuable for customer support scenarios where you need to collect information in a specific sequence—for example, collecting a warranty ID before processing a refund.

## Basic implementation

The core mechanism is a [tool](/oss/langchain/tools) that returns a [`Command`](/oss/langgraph/graph-api#command) to update state, triggering a transition to a new step or agent:

```python
from langchain.tools import tool
from langchain.messages import ToolMessage
from langgraph.types import Command

@tool
def transfer_to_specialist(runtime) -> Command:
    """Transfer to the specialist agent."""
    return Command(
        update={
            "messages": [
                ToolMessage(  # [!code highlight]
                    content="Transferred to specialist",
                    tool_call_id=runtime.tool_call_id  # [!code highlight]
                )
            ],
            "current_step": "specialist"  # Triggers behavior change
        }
    )
```

**Note:**

**Why include a `ToolMessage`?** When an LLM calls a tool, it expects a response. The `ToolMessage` with matching `tool_call_id` completes this request-response cycle—without it, the conversation history becomes malformed. This is required whenever your handoff tool updates messages.

For a complete implementation, see the tutorial below.

- [Tutorial: Build customer support with handoffs](/oss/langchain/multi-agent/handoffs-customer-support)

    Learn how to build a customer support agent using the handoffs pattern, where a single agent transitions between different configurations.

## Implementation approaches

There are two ways to implement handoffs: **[single agent with middleware](#single-agent-with-middleware)** (one agent with dynamic configuration) or **[multiple agent subgraphs](#multiple-agent-subgraphs)** (distinct agents as graph nodes).

### Single agent with middleware

A single agent changes its behavior based on state. Middleware intercepts each model call and dynamically adjusts the system prompt and available tools. Tools update the state variable to trigger transitions:

```python
from langchain.tools import ToolRuntime, tool
from langchain.messages import ToolMessage
from langgraph.types import Command

@tool
def record_warranty_status(
    status: str,
    runtime: ToolRuntime[None, SupportState]
) -> Command:
    """Record warranty status and transition to next step."""
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content=f"Warranty status recorded: {status}",
                    tool_call_id=runtime.tool_call_id
                )
            ],
            "warranty_status": status,
            "current_step": "specialist"  # Update state to trigger transition
        }
    )
```

**Complete example: Customer support with middleware**

```python
from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from typing import Callable

# 1. Define state with current_step tracker
class SupportState(AgentState):  # [!code highlight]
    """Track which step is currently active."""
    current_step: str = "triage"  # [!code highlight]
    warranty_status: str | None = None

# 2. Tools update current_step via Command
@tool
def record_warranty_status(
    status: str,
    runtime: ToolRuntime[None, SupportState]
) -> Command:  # [!code highlight]
    """Record warranty status and transition to next step."""
    return Command(update={  # [!code highlight]
        "messages": [  # [!code highlight]
            ToolMessage(
                content=f"Warranty status recorded: {status}",
                tool_call_id=runtime.tool_call_id
            )
        ],
        "warranty_status": status,
        # Transition to next step
        "current_step": "specialist"    # [!code highlight]
    })

# 3. Middleware applies dynamic configuration based on current_step
@wrap_model_call  # [!code highlight]
def apply_step_config(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Configure agent behavior based on current_step."""
    step = request.state.get("current_step", "triage")  # [!code highlight]

# Map steps to their configurations
configs = {
    "triage": {
        "prompt": "Collect warranty information...",
        "tools": [record_warranty_status]
    },
    "specialist": {
        "prompt": "Provide solutions based on warranty: {warranty_status}",
        "tools": [provide_solution, escalate]
    }
}

config = configs[step]
request = request.override(  # [!code highlight]
    system_prompt=config["prompt"].format(**request.state),  # [!code highlight]
    tools=config["tools"]  # [!code highlight]
)
return handler(request)

# 4. Create agent with middleware
agent = create_agent(
    model,
    tools=[record_warranty_status, provide_solution, escalate],
    state_schema=SupportState,
    middleware=[apply_step_config],  # [!code highlight]
    checkpointer=InMemorySaver()  # Persist state across turns  # [!code highlight]
)
```

### Multiple agent subgraphs

Multiple distinct agents exist as separate nodes in a graph. Handoff tools navigate between agent nodes using `Command.PARENT` to specify which node to execute next.

**Warning:**

Subgraph handoffs require careful **[context engineering](/oss/langchain/context-engineering)**. Unlike single-agent middleware (where message history flows naturally), you must explicitly decide what messages pass between agents. Get this wrong and agents receive malformed conversation history or bloated context. See [Context engineering](#context-engineering) below.

```python
from langchain.messages import AIMessage, ToolMessage
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command

@tool
def transfer_to_sales(
    runtime: ToolRuntime,
) -> Command:
    """Transfer to the sales agent."""
    last_ai_message = next(  # [!code highlight]
        msg for msg in reversed(runtime.state["messages"]) if isinstance(msg, AIMessage)  # [!code highlight]
    )  # [!code highlight]
    transfer_message = ToolMessage(  # [!code highlight]
        content="Transferred to sales agent",  # [!code highlight]
        tool_call_id=runtime.tool_call_id,  # [!code highlight]
    )  # [!code highlight]
    return Command(
        goto="sales_agent",
        update={
            "active_agent": "sales_agent",
            "messages": [last_ai_message, transfer_message],  # [!code highlight]
        },
        graph=Command.PARENT
    )
```

**Complete example: Sales and support with handoffs**

This example shows a multi-agent system with separate sales and support agents. Each agent is a separate graph node, and handoff tools allow agents to transfer conversations to each other.

```python
from typing import Literal

from langchain.agents import AgentState, create_agent
from langchain.messages import AIMessage, ToolMessage
from langchain.tools import tool, ToolRuntime
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from typing_extensions import NotRequired

# 1. Define state with active_agent tracker
class MultiAgentState(AgentState):
    active_agent: NotRequired[str]

# 2. Create handoff tools
@tool
def transfer_to_sales(
    runtime: ToolRuntime,
) -> Command:
    """Transfer to the sales agent."""
    last_ai_message = next(  # [!code highlight]
        msg for msg in reversed(runtime.state["messages"]) if isinstance(msg, AIMessage)  # [!code highlight]
    )  # [!code highlight]
    transfer_message = ToolMessage(  # [!code highlight]
        content="Transferred to sales agent from support agent",  # [!code highlight]
        tool_call_id=runtime.tool_call_id,  # [!code highlight]
    )  # [!code highlight]
    return Command(
        goto="sales_agent",
        update={
            "active_agent": "sales_agent",
            "messages": [last_ai_message, transfer_message],  # [!code highlight]
        },
        graph=Command.PARENT,
    )

@tool
def transfer_to_support(
    runtime: ToolRuntime,
) -> Command:
    """Transfer to the support agent."""
    last_ai_message = next(  # [!code highlight]
        msg for msg in reversed(runtime.state["messages"]) if isinstance(msg, AIMessage)  # [!code highlight]
    )  # [!code highlight]
    transfer_message = ToolMessage(  # [!code highlight]
        content="Transferred to support agent from sales agent",  # [!code highlight]
        tool_call_id=runtime.tool_call_id,  # [!code highlight]
    )  # [!code highlight]
    return Command(
        goto="support_agent",
        update={
            "active_agent": "support_agent",
            "messages": [last_ai_message, transfer_message],  # [!code highlight]
        },
        graph=Command.PARENT,
    )

# 3. Create agents with handoff tools
sales_agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[transfer_to_support],
    system_prompt="You are a sales agent. Help with sales inquiries. If asked about technical issues or support, transfer to the support agent.",
)

support_agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[transfer_to_sales],
    system_prompt="You are a support agent. Help with technical issues. If asked about pricing or purchasing, transfer to the sales agent.",
)

# 4. Create agent nodes that invoke the agents
def call_sales_agent(state: MultiAgentState) -> Command:
    """Node that calls the sales agent."""
    response = sales_agent.invoke(state)
    return response

def call_support_agent(state: MultiAgentState) -> Command:
    """Node that calls the support agent."""
    response = support_agent.invoke(state)
    return response

# 5. Create router that checks if we should end or continue
def route_after_agent(
    state: MultiAgentState,
) -> Literal["sales_agent", "support_agent", "__end__"]:
    """Route based on active_agent, or END if the agent finished without handoff."""
    messages = state.get("messages", [])

# Check the last message - if it's an AIMessage without tool calls, we're done
if messages:
    last_msg = messages[-1]
    if isinstance(last_msg, AIMessage) and not last_msg.tool_calls:  # [!code highlight]
        return "__end__"  # [!code highlight]

# Otherwise route to the active agent
active = state.get("active_agent", "sales_agent")
return active if active else "sales_agent"

def route_initial(
    state: MultiAgentState,
) -> Literal["sales_agent", "support_agent"]:
    """Route to the active agent based on state, default to sales agent."""
    return state.get("active_agent") or "sales_agent"

# 6. Build the graph
builder = StateGraph(MultiAgentState)
builder.add_node("sales_agent", call_sales_agent)
builder.add_node("support_agent", call_support_agent)

# Start with conditional routing based on initial active_agent
builder.add_conditional_edges(START, route_initial, ["sales_agent", "support_agent"])

# After each agent, check if we should end or route to another agent
builder.add_conditional_edges(
    "sales_agent", route_after_agent, ["sales_agent", "support_agent", END]
)
builder.add_conditional_edges(
    "support_agent", route_after_agent, ["sales_agent", "support_agent", END]
)

graph = builder.compile()
result = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Hi, I'm having trouble with my account login. Can you help?",
            }
        ]
    }
)

for msg in result["messages"]:
    msg.pretty_print()
```

**Tip:**

Use **single agent with middleware** for most handoffs use cases—it's simpler. Only use **multiple agent subgraphs** when you need bespoke agent implementations (e.g., a node that's itself a complex graph with reflection or retrieval steps).

#### Context engineering

With subgraph handoffs, you control exactly what messages flow between agents. This precision is essential for maintaining valid conversation history and avoiding context bloat that could confuse downstream agents. For more on this topic, see [context engineering](/oss/langchain/context-engineering).

**Handling context during handoffs**

When handing off between agents, you need to ensure the conversation history remains valid. LLMs expect tool calls to be paired with their responses, so when using `Command.PARENT` to hand off to another agent, you must include both:

1. **The `AIMessage` containing the tool call** (the message that triggered the handoff)
2. **A `ToolMessage` acknowledging the handoff** (the artificial response to that tool call)

Without this pairing, the receiving agent will see an incomplete conversation and may produce errors or unexpected behavior.

The example below assumes only the handoff tool was called (no parallel tool calls):

```python
@tool
def transfer_to_sales(runtime: ToolRuntime) -> Command:
    # Get the AI message that triggered this handoff
    last_ai_message = runtime.state["messages"][-1]

# Create an artificial tool response to complete the pair
transfer_message = ToolMessage(
    content="Transferred to sales agent",
    tool_call_id=runtime.tool_call_id,
)

    return Command(
        goto="sales_agent",
        update={
            "active_agent": "sales_agent",
            # Pass only these two messages, not the full subagent history
            "messages": [last_ai_message, transfer_message],
        },
        graph=Command.PARENT,
    )
```

**Note:**

**Why not pass all subagent messages?** While you could include the full subagent conversation in the handoff, this often creates problems. The receiving agent may become confused by irrelevant internal reasoning, and token costs increase unnecessarily. By passing only the handoff pair, you keep the parent graph's context focused on high-level coordination. If the receiving agent needs additional context, consider summarizing the subagent's work in the ToolMessage content instead of passing raw message history.

**Returning control to the user**

When returning control to the user (ending the agent's turn), ensure the final message is an `AIMessage`. This maintains valid conversation history and signals to the user interface that the agent has finished its work.

## Implementation considerations

As you design your multi-agent system, consider:

* **Context filtering strategy**: Will each agent receive full conversation history, filtered portions, or summaries? Different agents may need different context depending on their role.
* **Tool semantics**: Clarify whether handoff tools only update routing state or also perform side effects. For example, should `transfer_to_sales()` also create a support ticket, or should that be a separate action?
* **Token efficiency**: Balance context completeness against token costs. Summarization and selective context passing become more important as conversations grow longer.

---

# Multi-agent
> 출처: data/raw/langchain/multi-agent/index.mdx | https://docs.langchain.com/oss/python/langchain/multi-agent

Multi-agent systems coordinate specialized components to tackle complex workflows. However, not every complex task requires this approach—a single agent with the right (sometimes dynamic) tools and prompt can often achieve similar results.

**Tip:**

For built-in multi-agent support, use [Deep Agents](/oss/deepagents/overview): a higher-level harness built on LangChain that ships with [subagents](/oss/deepagents/subagents), [skills](/oss/deepagents/skills), planning, a virtual filesystem, and context management.

## Why multi-agent?

When developers say they need "multi-agent," they're usually looking for one or more of these capabilities:

- 

 **Context management**: Provide specialized knowledge without overwhelming the model's context window. If context were infinite and latency zero, you could dump all knowledge into a single prompt—but since it's not, you need patterns to selectively surface relevant information.
- 

 **Distributed development**: Allow different teams to develop and maintain capabilities independently, composing them into a larger system with clear boundaries.
- 

 **Parallelization**: Spawn specialized workers for subtasks and execute them concurrently for faster results.

Multi-agent patterns are particularly valuable when a single agent has too many [tools](/oss/langchain/tools) and makes poor decisions about which to use, when tasks require specialized knowledge with extensive context (long prompts and domain-specific tools), or when you need to enforce sequential constraints that unlock capabilities only after certain conditions are met.

**Tip:**

At the center of multi-agent design is **[context engineering](/oss/langchain/context-engineering)**—deciding what information each agent sees. The quality of your system depends on ensuring each agent has access to the right data for its task.

## Patterns

Here are the main patterns for building multi-agent systems, each suited to different use cases:

| Pattern | How it works |
|--------------|--------------|
| [**Subagents**](/oss/langchain/multi-agent/subagents) | A main agent coordinates subagents as tools. All routing passes through the main agent, which decides when and how to invoke each subagent. |
| [**Handoffs**](/oss/langchain/multi-agent/handoffs) | Behavior changes dynamically based on state. Tool calls update a state variable that triggers routing or configuration changes, switching agents or adjusting the current agent's tools and prompt. |
| [**Skills**](/oss/langchain/multi-agent/skills) | Specialized prompts and knowledge loaded on-demand. A single agent stays in control while loading context from skills as needed. |
| [**Router**](/oss/langchain/multi-agent/router) | A routing step classifies input and directs it to one or more specialized agents. Results are synthesized into a combined response. |
| [**Custom workflow**](/oss/langchain/multi-agent/custom-workflow) | Build bespoke execution flows with [LangGraph](/oss/langgraph/overview), mixing deterministic logic and agentic behavior. Embed other patterns as nodes in your workflow. |

### Choosing a pattern

Use this table to match your requirements to the right pattern:

| Pattern | Distributed development | Parallelization | Multi-hop | Direct user interaction |
|---------|:-----------------------:|:---------------:|:----------:|:-----------------------:|
| [**Subagents**](/oss/langchain/multi-agent/subagents) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| [**Handoffs**](/oss/langchain/multi-agent/handoffs) | - | - | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| [**Skills**](/oss/langchain/multi-agent/skills) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| [**Router**](/oss/langchain/multi-agent/router) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | - | ⭐⭐⭐ |

- **Distributed development**: Can different teams maintain components independently?
- **Parallelization**: Can multiple agents execute concurrently?
- **Multi-hop**: Does the pattern support calling multiple subagents in series?
- **Direct user interaction**: Can subagents converse directly with the user?

**Tip:**

You can mix patterns! For example, a **subagents** architecture can invoke tools that invoke custom workflows or router agents. Subagents can even use the **skills** pattern to load context on-demand. The possibilities are endless!

### Visual overview

**Subagents**

A main agent coordinates subagents as tools. All routing passes through the main agent.

**Handoffs**

Agents transfer control to each other via tool calls. Each agent can hand off to others or respond directly to the user.

**Skills**

A single agent loads specialized prompts and knowledge on-demand while staying in control.

**Router**

A routing step classifies input and directs it to specialized agents. Results are synthesized.

**Tip:**

Trace the full coordination flow across agents with [LangSmith](https://smith.langchain.com). Follow the [tracing quickstart](/langsmith/trace-with-langchain) to get set up.

We recommend you also set up [LangSmith Engine](/langsmith/engine) which monitors your traces, detects issues, and proposes fixes.

## Performance comparison

Different patterns have different performance characteristics. Understanding these tradeoffs helps you choose the right pattern for your latency and cost requirements.

**Key metrics:**
- **Model calls**: Number of LLM invocations. More calls = higher latency (especially if sequential) and higher per-request API costs.
- **Tokens processed**: Total [context window](/oss/langchain/context-engineering) usage across all calls. More tokens = higher processing costs and potential context limits.

### One-shot request

> **User:** "Buy coffee"

A specialized coffee agent/skill can call a `buy_coffee` tool.

| Pattern | Model calls | Best fit |
|---------|:-----------:|:--------:|
| [**Subagents**](/oss/langchain/multi-agent/subagents) | 4 | |
| [**Handoffs**](/oss/langchain/multi-agent/handoffs) | 3 | ✅ |
| [**Skills**](/oss/langchain/multi-agent/skills) | 3 | ✅ |
| [**Router**](/oss/langchain/multi-agent/router) | 3 | ✅ |

**Subagents**

**4 model calls:**

**Handoffs**

**3 model calls:**

**Skills**

**3 model calls:**

**Router**

**3 model calls:**

**Key insight:** Handoffs, Skills, and Router are most efficient for single tasks (3 calls each). Subagents adds one extra call because results flow back through the main agent—this overhead provides centralized control.

### Repeat request

> **Turn 1:** "Buy coffee"
> **Turn 2:** "Buy coffee again"

The user repeats the same request in the same conversation.

| Pattern | Turn 2 calls | Total (both turns) | Best fit |
|---------|:------------:|:------------------:|:--------:|
| [**Subagents**](/oss/langchain/multi-agent/subagents) | 4 | 8 | |
| [**Handoffs**](/oss/langchain/multi-agent/handoffs) | 2 | 5 | ✅ |
| [**Skills**](/oss/langchain/multi-agent/skills) | 2 | 5 | ✅ |
| [**Router**](/oss/langchain/multi-agent/router) | 3 | 6 | |

**Subagents**

**4 calls again → 8 total**

- Subagents are **stateless by design**—each invocation follows the same flow
- The main agent maintains conversation context, but subagents start fresh each time
- This provides strong context isolation but repeats the full flow

**Handoffs**

**2 calls → 5 total**

- The coffee agent is **still active** from turn 1 (state persists)
- No handoff needed—agent directly calls `buy_coffee` tool (call 1)
- Agent responds to user (call 2)
- **Saves 1 call by skipping the handoff**

**Skills**

**2 calls → 5 total**

- The skill context is **already loaded** in conversation history
- No need to reload—agent directly calls `buy_coffee` tool (call 1)
- Agent responds to user (call 2)
- **Saves 1 call by reusing loaded skill**

**Router**

**3 calls again → 6 total**

- Routers are **stateless**—each request requires an LLM routing call
- Turn 2: Router LLM call (1) → Milk agent calls buy_coffee (2) → Milk agent responds (3)
- Can be optimized by wrapping as a tool in a stateful agent

**Key insight:** Stateful patterns (Handoffs, Skills) save 40-50% of calls on repeat requests. Subagents maintain consistent cost per request—this stateless design provides strong context isolation but at the cost of repeated model calls.

### Multi-domain

> **User:** "Compare Python, JavaScript, and Rust for web development"

Each language agent/skill contains ~2000 tokens of documentation. All patterns can make parallel tool calls.

| Pattern | Model calls | Total tokens | Best fit |
|---------|:-----------:|:------------:|:--------:|
| [**Subagents**](/oss/langchain/multi-agent/subagents) | 5 | ~9K | ✅ |
| [**Handoffs**](/oss/langchain/multi-agent/handoffs) | 7+ | ~14K+ | |
| [**Skills**](/oss/langchain/multi-agent/skills) | 3 | ~15K | |
| [**Router**](/oss/langchain/multi-agent/router) | 5 | ~9K | ✅ |

**Subagents**

**5 calls, ~9K tokens**

Each subagent works in **isolation** with only its relevant context. Total: **9K tokens**.

**Handoffs**

**7+ calls, ~14K+ tokens**

Handoffs executes **sequentially**—can't research all three languages in parallel. Growing conversation history adds overhead. Total: **~14K+ tokens**.

**Skills**

**3 calls, ~15K tokens**

After loading, **every subsequent call processes all 6K tokens of skill documentation**. Subagents processes 67% fewer tokens overall due to context isolation. Total: **15K tokens**.

**Router**

**5 calls, ~9K tokens**

Router uses an **LLM for routing**, then invokes agents in parallel. Similar to Subagents but with explicit routing step. Total: **9K tokens**.

**Key insight:** For multi-domain tasks, patterns with parallel execution (Subagents, Router) are most efficient. Skills has fewer calls but high token usage due to context accumulation. Handoffs is inefficient here—it must execute sequentially and can't leverage parallel tool calling for consulting multiple domains simultaneously.

### Summary

Here's how patterns compare across all three scenarios:

| Pattern | One-shot | Repeat request | Multi-domain |
|---------|:-----------:|:---------:|:----------------:|
| [**Subagents**](/oss/langchain/multi-agent/subagents) | 4 calls | 8 calls (4+4) | 5 calls, 9K tokens |
| [**Handoffs**](/oss/langchain/multi-agent/handoffs) | 3 calls | 5 calls (3+2) | 7+ calls, 14K+ tokens |
| [**Skills**](/oss/langchain/multi-agent/skills) | 3 calls | 5 calls (3+2) | 3 calls, 15K tokens |
| [**Router**](/oss/langchain/multi-agent/router) | 3 calls | 6 calls (3+3) | 5 calls, 9K tokens |

**Choosing a pattern:**

| Optimize for | [Subagents](/oss/langchain/multi-agent/subagents) | [Handoffs](/oss/langchain/multi-agent/handoffs) | [Skills](/oss/langchain/multi-agent/skills) | [Router](/oss/langchain/multi-agent/router) |
|--------------|:---------:|:--------:|:------:|:------:|
| Single requests | | ✅ | ✅ | ✅ |
| Repeat requests | | ✅ | ✅ | |
| Parallel execution | ✅ | | | ✅ |
| Large-context domains | ✅ | | | ✅ |
| Simple, focused tasks | | | ✅ | |

---

# Build a multi-source knowledge base with routing
> 출처: data/raw/langchain/multi-agent/router-knowledge-base.mdx | https://docs.langchain.com/oss/python/langchain/multi-agent/router-knowledge-base

## Overview

The **router pattern** is a [multi-agent](/oss/langchain/multi-agent) architecture where a routing step classifies input and directs it to specialized agents, with results synthesized into a combined response. This pattern excels when your organization's knowledge lives across distinct **verticals** (separate knowledge domains that each require their own agent with specialized tools and prompts).

In this tutorial, you'll build a multi-source knowledge base router that demonstrates these benefits through a realistic enterprise scenario. The system will coordinate three specialists:

- A **GitHub agent** that searches code, issues, and pull requests.
- A **Notion agent** that searches internal documentation and wikis.
- A **Slack agent** that searches relevant threads and discussions.

When a user asks "How do I authenticate API requests?", the router decomposes the query into source-specific sub-questions, routes them to the relevant agents in parallel, and synthesizes results into a coherent answer.

```mermaid
graph LR
    A([Query]) --> B[Classify]
    B --> C[GitHub agent]
    B --> D[Notion agent]
    B --> E[Slack agent]
    C --> F[Synthesize]
    D --> F
    E --> F
    F --> G([Combined answer])

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,G trigger
    class B,C,D,E,F process
```

### Why use a router?

The router pattern provides several advantages:

- **Parallel execution**: Query multiple sources simultaneously, reducing latency compared to sequential approaches.
- **Specialized agents**: Each vertical has focused tools and prompts optimized for its domain.
- **Selective routing**: Not every query needs every source—the router intelligently selects relevant verticals.
- **Targeted sub-questions**: Each agent receives a question tailored to its domain, improving result quality.
- **Clean synthesis**: Results from multiple sources are combined into a single, coherent response.

### Concepts

We will cover the following concepts:

- [Multi-agent systems](/oss/langchain/multi-agent)
- [StateGraph](/oss/langgraph/graph-api) for workflow orchestration
- [Send API](/oss/langgraph/graph-api#send) for parallel execution

**Tip:**

**Router vs. Subagents**: The [subagents pattern](/oss/langchain/multi-agent/subagents) can also route to multiple agents. Use the router pattern when you need specialized preprocessing, custom routing logic, or want explicit control over parallel execution. Use the subagents pattern when you want the LLM to decide which agents to call dynamically.

## Setup

### Installation

This tutorial requires the `langchain` and `langgraph` packages:

```bash pip
pip install langchain langgraph
```
```bash uv
uv add langchain langgraph
```
```bash conda
conda install langchain langgraph -c conda-forge
```

For more details, see our [Installation guide](/oss/langchain/install).

### LangSmith

Set up [LangSmith](https://smith.langchain.com) to inspect what is happening inside your agent. Then set the following environment variables:

```bash Shell
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```
```python Python
import getpass
import os

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass()
```

### Select an LLM

Select a chat model from LangChain's suite of integrations:

**OpenAI**

👉 Read the [OpenAI chat model integration docs](/oss/python/integrations/chat/openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-5.5")
```
```python Model Class
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-..."

model = ChatOpenAI(model="gpt-5.5")
```

**Anthropic**

👉 Read the [Anthropic chat model integration docs](/oss/python/integrations/chat/anthropic/)

```bash pip
pip install -U "langchain[anthropic]"
```

```bash uv
uv add "langchain[anthropic]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = init_chat_model("claude-sonnet-4-6")
```
```python Model Class
import os
from langchain_anthropic import ChatAnthropic

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = ChatAnthropic(model="claude-sonnet-4-6")
```

**Azure**

👉 Read the [Azure chat model integration docs](/oss/python/integrations/chat/azure_chat_openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = init_chat_model(
    "azure_openai:gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
```
```python Model Class
import os
from langchain_openai import AzureChatOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = AzureChatOpenAI(
    model="gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
)
```

**Google Gemini**

👉 Read the [Google GenAI chat model integration docs](/oss/python/integrations/chat/google_generative_ai/)

```bash pip
pip install -U "langchain[google-genai]"
```

```bash uv
uv add "langchain[google-genai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["GOOGLE_API_KEY"] = "..."

model = init_chat_model("google_genai:gemini-3.7-flash")
```
```python Model Class
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "..."

model = ChatGoogleGenerativeAI(model="gemini-3.7-flash")
```

**AWS Bedrock**

👉 Read the [AWS Bedrock chat model integration docs](/oss/python/integrations/chat/bedrock/)

```bash pip
pip install -U "langchain[aws]"
```

```bash uv
uv add "langchain[aws]"
```

```python init_chat_model
from langchain.chat_models import init_chat_model

# Follow the steps here to configure your credentials:
# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html

model = init_chat_model(
    "us.anthropic.claude-sonnet-4-6",
    model_provider="bedrock_converse",
)
```
```python Model Class
from langchain_aws import ChatBedrock

model = ChatBedrock(model="us.anthropic.claude-sonnet-4-6")
```

**HuggingFace**

👉 Read the [HuggingFace chat model integration docs](/oss/python/integrations/chat/huggingface/)

```bash pip
pip install -U "langchain[huggingface]"
```

```bash uv
uv add "langchain[huggingface]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

model = init_chat_model(
    "microsoft/Phi-3-mini-4k-instruct",
    model_provider="huggingface",
    temperature=0.7,
    max_tokens=1024,
)
```

```python Model Class
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    temperature=0.7,
    max_length=1024,
)
model = ChatHuggingFace(llm=llm)
```

**OpenRouter**

👉 Read the [OpenRouter chat model integration docs](/oss/python/integrations/chat/openrouter/)

```bash pip
pip install -U "langchain-openrouter"
```

```bash uv
uv add "langchain-openrouter"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = init_chat_model(
    "auto",
    model_provider="openrouter",
)
```
```python Model Class
import os
from langchain_openrouter import ChatOpenRouter

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = ChatOpenRouter(model="auto")
```

## 1. Define state

First, define the state schemas. We use three types:

- **`AgentInput`**: Simple state passed to each subagent (just a query)
- **`AgentOutput`**: Result returned by each subagent (source name + result)
- **`RouterState`**: Main workflow state tracking the query, classifications, results, and final answer

```python
from typing import Annotated, Literal, TypedDict
import operator

class AgentInput(TypedDict):
    """Simple input state for each subagent."""
    query: str

class AgentOutput(TypedDict):
    """Output from each subagent."""
    source: str
    result: str

class Classification(TypedDict):
    """A single routing decision: which agent to call with what query."""
    source: Literal["github", "notion", "slack"]
    query: str

class RouterState(TypedDict):
    query: str
    classifications: list[Classification]
    results: Annotated[list[AgentOutput], operator.add]  # Reducer collects parallel results
    final_answer: str
```

The `results` field uses a **reducer** (`operator.add` in Python, a concat function in JS) to collect outputs from parallel agent executions into a single list.

## 2. Define tools for each vertical

Create tools for each knowledge domain. In a production system, these would call actual APIs. For this tutorial, we use stub implementations that return mock data. We define 7 tools across 3 verticals: GitHub (search code, issues, PRs), Notion (search docs, get page), and Slack (search messages, get thread).

```python expandable
from langchain.tools import tool

@tool
def search_code(query: str, repo: str = "main") -> str:
    """Search code in GitHub repositories."""
    return f"Found code matching '{query}' in {repo}: authentication middleware in src/auth.py"

@tool
def search_issues(query: str) -> str:
    """Search GitHub issues and pull requests."""
    return f"Found 3 issues matching '{query}': #142 (API auth docs), #89 (OAuth flow), #203 (token refresh)"

@tool
def search_prs(query: str) -> str:
    """Search pull requests for implementation details."""
    return f"PR #156 added JWT authentication, PR #178 updated OAuth scopes"

@tool
def search_notion(query: str) -> str:
    """Search Notion workspace for documentation."""
    return f"Found documentation: 'API Authentication Guide' - covers OAuth2 flow, API keys, and JWT tokens"

@tool
def get_page(page_id: str) -> str:
    """Get a specific Notion page by ID."""
    return f"Page content: Step-by-step authentication setup instructions"

@tool
def search_slack(query: str) -> str:
    """Search Slack messages and threads."""
    return f"Found discussion in #engineering: 'Use Bearer tokens for API auth, see docs for refresh flow'"

@tool
def get_thread(thread_id: str) -> str:
    """Get a specific Slack thread."""
    return f"Thread discusses best practices for API key rotation"
```

## 3. Create specialized agents

Create an agent for each vertical. Each agent has domain-specific tools and a prompt optimized for its knowledge source. All three follow the same pattern—only the tools and system prompt differ.

```python expandable
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-5.5")

github_agent = create_agent(
    model,
    tools=[search_code, search_issues, search_prs],
    system_prompt=(
        "You are a GitHub expert. Answer questions about code, "
        "API references, and implementation details by searching "
        "repositories, issues, and pull requests."
    ),
)

notion_agent = create_agent(
    model,
    tools=[search_notion, get_page],
    system_prompt=(
        "You are a Notion expert. Answer questions about internal "
        "processes, policies, and team documentation by searching "
        "the organization's Notion workspace."
    ),
)

slack_agent = create_agent(
    model,
    tools=[search_slack, get_thread],
    system_prompt=(
        "You are a Slack expert. Answer questions by searching "
        "relevant threads and discussions where team members have "
        "shared knowledge and solutions."
    ),
)
```

## 4. Build the router workflow

Now build the router workflow using a StateGraph. The workflow has four main steps:

1. **Classify**: Analyze the query and determine which agents to invoke with what sub-questions
2. **Route**: Fan out to selected agents in parallel using `Send`
3. **Query agents**: Each agent receives a simple `AgentInput` and returns an `AgentOutput`
4. **Synthesize**: Combine collected results into a coherent response

```python
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

router_llm = init_chat_model("openai:gpt-5.4-mini")

# Define structured output schema for the classifier
class ClassificationResult(BaseModel):  # [!code highlight]
    """Result of classifying a user query into agent-specific sub-questions."""
    classifications: list[Classification] = Field(
        description="List of agents to invoke with their targeted sub-questions"
    )

def classify_query(state: RouterState) -> dict:
    """Classify query and determine which agents to invoke."""
    structured_llm = router_llm.with_structured_output(ClassificationResult)  # [!code highlight]

    result = structured_llm.invoke([
        {
            "role": "system",
            "content": """Analyze this query and determine which knowledge bases to consult.
For each relevant source, generate a targeted sub-question optimized for that source.

Available sources:
- github: Code, API references, implementation details, issues, pull requests
- notion: Internal documentation, processes, policies, team wikis
- slack: Team discussions, informal knowledge sharing, recent conversations

Return ONLY the sources that are relevant to the query. Each source should have
a targeted sub-question optimized for that specific knowledge domain.

Example for "How do I authenticate API requests?":
- github: "What authentication code exists? Search for auth middleware, JWT handling"
- notion: "What authentication documentation exists? Look for API auth guides"
(slack omitted because it's not relevant for this technical question)"""
        },
        {"role": "user", "content": state["query"]}
    ])

return {"classifications": result.classifications}

def route_to_agents(state: RouterState) -> list[Send]:
    """Fan out to agents based on classifications."""
    return [
        Send(c["source"], {"query": c["query"]})  # [!code highlight]
        for c in state["classifications"]
    ]

def query_github(state: AgentInput) -> dict:
    """Query the GitHub agent."""
    result = github_agent.invoke({
        "messages": [{"role": "user", "content": state["query"]}]  # [!code highlight]
    })
    return {"results": [{"source": "github", "result": result["messages"][-1].content}]}

def query_notion(state: AgentInput) -> dict:
    """Query the Notion agent."""
    result = notion_agent.invoke({
        "messages": [{"role": "user", "content": state["query"]}]  # [!code highlight]
    })
    return {"results": [{"source": "notion", "result": result["messages"][-1].content}]}

def query_slack(state: AgentInput) -> dict:
    """Query the Slack agent."""
    result = slack_agent.invoke({
        "messages": [{"role": "user", "content": state["query"]}]  # [!code highlight]
    })
    return {"results": [{"source": "slack", "result": result["messages"][-1].content}]}

def synthesize_results(state: RouterState) -> dict:
    """Combine results from all agents into a coherent answer."""
    if not state["results"]:
        return {"final_answer": "No results found from any knowledge source."}

# Format results for synthesis
formatted = [
    f"**From {r['source'].title()}:**\n{r['result']}"
    for r in state["results"]
]

synthesis_response = router_llm.invoke([
    {
        "role": "system",
        "content": f"""Synthesize these search results to answer the original question: "{state['query']}"

- Combine information from multiple sources without redundancy
- Highlight the most relevant and actionable information
- Note any discrepancies between sources
- Keep the response concise and well-organized"""
        },
        {"role": "user", "content": "\n\n".join(formatted)}
    ])

    return {"final_answer": synthesis_response.content}
```

## 5. Compile the workflow

Now assemble the workflow by connecting nodes with edges. The key is using `add_conditional_edges` with the routing function to enable parallel execution:

```python
workflow = (
    StateGraph(RouterState)
    .add_node("classify", classify_query)
    .add_node("github", query_github)
    .add_node("notion", query_notion)
    .add_node("slack", query_slack)
    .add_node("synthesize", synthesize_results)
    .add_edge(START, "classify")
    .add_conditional_edges("classify", route_to_agents, ["github", "notion", "slack"])
    .add_edge("github", "synthesize")
    .add_edge("notion", "synthesize")
    .add_edge("slack", "synthesize")
    .add_edge("synthesize", END)
    .compile()
)
```

The `add_conditional_edges` call connects the classify node to the agent nodes through the `route_to_agents` function. When `route_to_agents` returns multiple `Send` objects, those nodes execute in parallel.

## 6. Use the router

Test your router with queries that span multiple knowledge domains:

```python
result = workflow.invoke({
    "query": "How do I authenticate API requests?"
})

print("Original query:", result["query"])
print("\nClassifications:")
for c in result["classifications"]:
    print(f"  {c['source']}: {c['query']}")
print("\n" + "=" * 60 + "\n")
print("Final Answer:")
print(result["final_answer"])
```

Expected output:
```
Original query: How do I authenticate API requests?

Classifications:
  github: What authentication code exists? Search for auth middleware, JWT handling
  notion: What authentication documentation exists? Look for API auth guides

============================================================

Final Answer:
To authenticate API requests, you have several options:

1. **JWT Tokens**: The recommended approach for most use cases.
   Implementation details are in `src/auth.py` (PR #156).

2. **OAuth2 Flow**: For third-party integrations, follow the OAuth2
   flow documented in Notion's 'API Authentication Guide'.

3. **API Keys**: For server-to-server communication, use Bearer tokens
   in the Authorization header.

For token refresh handling, see issue #203 and PR #178 for the latest
OAuth scope updates.
```

The router analyzed the query, classified it to determine which agents to invoke (GitHub and Notion, but not Slack for this technical question), queried both agents in parallel, and synthesized the results into a coherent answer.

## 7. Understanding the architecture

The router workflow follows a clear pattern:

### Classification phase

The `classify_query` function uses **structured output** to analyze the user's query and determine which agents to invoke. This is where the routing intelligence lives:

- Uses a Pydantic model (Python) or Zod schema (JS) to ensure valid output
- Returns a list of `Classification` objects, each with a `source` and targeted `query`
- Only includes relevant sources—irrelevant ones are simply omitted

This structured approach is more reliable than free-form JSON parsing and makes the routing logic explicit.

### Parallel execution with send

The `route_to_agents` function maps classifications to `Send` objects. Each `Send` specifies the target node and the state to pass:

```python
# Classifications: [{"source": "github", "query": "..."}, {"source": "notion", "query": "..."}]
# Becomes:
[Send("github", {"query": "..."}), Send("notion", {"query": "..."})]
# Both agents execute simultaneously, each receiving only the query it needs
```

Each agent node receives a simple `AgentInput` with just a `query` field—not the full router state. This keeps the interface clean and explicit.

### Result collection with reducers

Agent results flow back to the main state via a **reducer**. Each agent returns:

```python
{"results": [{"source": "github", "result": "..."}]}
```

The reducer (`operator.add` in Python) concatenates these lists, collecting all parallel results into `state["results"]`.

### Synthesis phase

After all agents complete, the `synthesize_results` function iterates over the collected results:

- Waits for all parallel branches to complete (LangGraph handles this automatically)
- References the original query to ensure the answer addresses what the user asked
- Combines information from all sources without redundancy

**Note:**

**Partial results**: In this tutorial, all selected agents must complete before synthesis.

## 8. Complete working example

Here's everything together in a runnable script:

**View complete code**

```python
"""
Multi-Source Knowledge Router Example

This example demonstrates the router pattern for multi-agent systems.
A router classifies queries, routes them to specialized agents in parallel,
and synthesizes results into a combined response.
"""

import operator
from typing import Annotated, Literal, TypedDict

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from pydantic import BaseModel, Field

# State definitions
class AgentInput(TypedDict):
    """Simple input state for each subagent."""
    query: str

class AgentOutput(TypedDict):
    """Output from each subagent."""
    source: str
    result: str

class Classification(TypedDict):
    """A single routing decision: which agent to call with what query."""
    source: Literal["github", "notion", "slack"]
    query: str

class RouterState(TypedDict):
    query: str
    classifications: list[Classification]
    results: Annotated[list[AgentOutput], operator.add]
    final_answer: str

# Structured output schema for classifier
class ClassificationResult(BaseModel):
    """Result of classifying a user query into agent-specific sub-questions."""
    classifications: list[Classification] = Field(
        description="List of agents to invoke with their targeted sub-questions"
    )

# Tools
@tool
def search_code(query: str, repo: str = "main") -> str:
    """Search code in GitHub repositories."""
    return f"Found code matching '{query}' in {repo}: authentication middleware in src/auth.py"

@tool
def search_issues(query: str) -> str:
    """Search GitHub issues and pull requests."""
    return f"Found 3 issues matching '{query}': #142 (API auth docs), #89 (OAuth flow), #203 (token refresh)"

@tool
def search_prs(query: str) -> str:
    """Search pull requests for implementation details."""
    return f"PR #156 added JWT authentication, PR #178 updated OAuth scopes"

@tool
def search_notion(query: str) -> str:
    """Search Notion workspace for documentation."""
    return f"Found documentation: 'API Authentication Guide' - covers OAuth2 flow, API keys, and JWT tokens"

@tool
def get_page(page_id: str) -> str:
    """Get a specific Notion page by ID."""
    return f"Page content: Step-by-step authentication setup instructions"

@tool
def search_slack(query: str) -> str:
    """Search Slack messages and threads."""
    return f"Found discussion in #engineering: 'Use Bearer tokens for API auth, see docs for refresh flow'"

@tool
def get_thread(thread_id: str) -> str:
    """Get a specific Slack thread."""
    return f"Thread discusses best practices for API key rotation"

# Models and agents
model = init_chat_model("openai:gpt-5.5")
router_llm = init_chat_model("openai:gpt-5.4-mini")

github_agent = create_agent(
    model,
    tools=[search_code, search_issues, search_prs],
    system_prompt=(
        "You are a GitHub expert. Answer questions about code, "
        "API references, and implementation details by searching "
        "repositories, issues, and pull requests."
    ),
)

notion_agent = create_agent(
    model,
    tools=[search_notion, get_page],
    system_prompt=(
        "You are a Notion expert. Answer questions about internal "
        "processes, policies, and team documentation by searching "
        "the organization's Notion workspace."
    ),
)

slack_agent = create_agent(
    model,
    tools=[search_slack, get_thread],
    system_prompt=(
        "You are a Slack expert. Answer questions by searching "
        "relevant threads and discussions where team members have "
        "shared knowledge and solutions."
    ),
)

# Workflow nodes
def classify_query(state: RouterState) -> dict:
    """Classify query and determine which agents to invoke."""
    structured_llm = router_llm.with_structured_output(ClassificationResult)

    result = structured_llm.invoke([
        {
            "role": "system",
            "content": """Analyze this query and determine which knowledge bases to consult.
For each relevant source, generate a targeted sub-question optimized for that source.

Available sources:
- github: Code, API references, implementation details, issues, pull requests
- notion: Internal documentation, processes, policies, team wikis
- slack: Team discussions, informal knowledge sharing, recent conversations

Return ONLY the sources that are relevant to the query."""
        },
        {"role": "user", "content": state["query"]}
    ])

return {"classifications": result.classifications}

def route_to_agents(state: RouterState) -> list[Send]:
    """Fan out to agents based on classifications."""
    return [
        Send(c["source"], {"query": c["query"]})
        for c in state["classifications"]
    ]

def query_github(state: AgentInput) -> dict:
    """Query the GitHub agent."""
    result = github_agent.invoke({
        "messages": [{"role": "user", "content": state["query"]}]
    })
    return {"results": [{"source": "github", "result": result["messages"][-1].content}]}

def query_notion(state: AgentInput) -> dict:
    """Query the Notion agent."""
    result = notion_agent.invoke({
        "messages": [{"role": "user", "content": state["query"]}]
    })
    return {"results": [{"source": "notion", "result": result["messages"][-1].content}]}

def query_slack(state: AgentInput) -> dict:
    """Query the Slack agent."""
    result = slack_agent.invoke({
        "messages": [{"role": "user", "content": state["query"]}]
    })
    return {"results": [{"source": "slack", "result": result["messages"][-1].content}]}

def synthesize_results(state: RouterState) -> dict:
    """Combine results from all agents into a coherent answer."""
    if not state["results"]:
        return {"final_answer": "No results found from any knowledge source."}

formatted = [
    f"**From {r['source'].title()}:**\n{r['result']}"
    for r in state["results"]
]

synthesis_response = router_llm.invoke([
    {
        "role": "system",
        "content": f"""Synthesize these search results to answer the original question: "{state['query']}"

- Combine information from multiple sources without redundancy
- Highlight the most relevant and actionable information
- Note any discrepancies between sources
- Keep the response concise and well-organized"""
        },
        {"role": "user", "content": "\n\n".join(formatted)}
    ])

return {"final_answer": synthesis_response.content}

# Build workflow
workflow = (
    StateGraph(RouterState)
    .add_node("classify", classify_query)
    .add_node("github", query_github)
    .add_node("notion", query_notion)
    .add_node("slack", query_slack)
    .add_node("synthesize", synthesize_results)
    .add_edge(START, "classify")
    .add_conditional_edges("classify", route_to_agents, ["github", "notion", "slack"])
    .add_edge("github", "synthesize")
    .add_edge("notion", "synthesize")
    .add_edge("slack", "synthesize")
    .add_edge("synthesize", END)
    .compile()
)

if __name__ == "__main__":
    result = workflow.invoke({
        "query": "How do I authenticate API requests?"
    })

    print("Original query:", result["query"])
    print("\nClassifications:")
    for c in result["classifications"]:
        print(f"  {c['source']}: {c['query']}")
    print("\n" + "=" * 60 + "\n")
    print("Final Answer:")
    print(result["final_answer"])
```

## 9. Advanced: Stateful routers

The router we've built so far is **stateless** (each request is handled independently with no memory between calls). For multi-turn conversations, you need a **stateful** approach.

### Tool wrapper approach

The simplest way to add conversation memory is to wrap the stateless router as a tool that a conversational agent can call:

```python
from langgraph.checkpoint.memory import InMemorySaver

@tool
def search_knowledge_base(query: str) -> str:
    """Search across multiple knowledge sources (GitHub, Notion, Slack).

Use this to find information about code, documentation, or team discussions.
"""
result = workflow.invoke({"query": query})
return result["final_answer"]

conversational_agent = create_agent(
    model,
    tools=[search_knowledge_base],
    system_prompt=(
        "You are a helpful assistant that answers questions about our organization. "
        "Use the search_knowledge_base tool to find information across our code, "
        "documentation, and team discussions."
    ),
    checkpointer=InMemorySaver(),
)
```

This approach keeps the router stateless while the conversational agent handles memory and context. The user can have a multi-turn conversation, and the agent will call the router tool as needed.

```python
config = {"configurable": {"thread_id": "user-123"}}

result = conversational_agent.invoke(
    {"messages": [{"role": "user", "content": "How do I authenticate API requests?"}]},
    config
)
print(result["messages"][-1].content)

result = conversational_agent.invoke(
    {"messages": [{"role": "user", "content": "What about rate limiting for those endpoints?"}]},
    config
)
print(result["messages"][-1].content)
```

**Tip:**

The tool wrapper approach is recommended for most use cases. It provides clean separation: the router handles multi-source querying, while the conversational agent handles context and memory.

### Full persistence approach

If you need the router itself to maintain state—for example, to use previous search results in routing decisions—use [persistence](/oss/langchain/short-term-memory) to store message history at the router level.

**Warning:**

**Stateful routers add complexity.** When routing to different agents across turns, conversations may feel inconsistent if agents have different tones or prompts. Consider the [handoffs pattern](/oss/langchain/multi-agent/handoffs) or [subagents pattern](/oss/langchain/multi-agent/subagents) instead—both provide clearer semantics for multi-turn conversations with different agents.

## 10. Key takeaways

The router pattern excels when you have:

- **Distinct verticals**: Separate knowledge domains that each require specialized tools and prompts
- **Parallel query needs**: Questions that benefit from querying multiple sources simultaneously
- **Synthesis requirements**: Results from multiple sources need to be combined into a coherent response

The pattern has three phases: **decompose** (analyze the query and generate targeted sub-questions), **route** (execute queries in parallel), and **synthesize** (combine results).

**Tip:**

**When to use the router pattern**

Use the router pattern when you have multiple independent knowledge sources, need low-latency parallel queries, and want explicit control over routing logic.

For simpler cases with dynamic tool selection, consider the [subagents pattern](/oss/langchain/multi-agent/subagents). For workflows where agents need to converse with users sequentially, consider [handoffs](/oss/langchain/multi-agent/handoffs).

## Next steps

- Learn about [handoffs](/oss/langchain/multi-agent/handoffs) for agent-to-agent conversations
- Explore the [subagents pattern](/oss/langchain/multi-agent/subagents-personal-assistant) for centralized orchestration
- Read the [multi-agent overview](/oss/langchain/multi-agent) to compare different patterns
- Use [LangSmith](https://smith.langchain.com) to debug and monitor your router

---

# Router
> 출처: data/raw/langchain/multi-agent/router.mdx | https://docs.langchain.com/oss/python/langchain/multi-agent/router

In the **router** architecture, a routing step classifies input and directs it to specialized [agents](/oss/langchain/agents). This is useful when you have distinct **verticals** (separate knowledge domains that each require their own agent).

```mermaid
graph LR
    A([Query]) --> B[Router]
    B --> C[Agent A]
    B --> D[Agent B]
    B --> E[Agent C]
    C --> F[Synthesize]
    D --> F
    E --> F
    F --> G([Combined answer])

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,G trigger
    class B,C,D,E,F process
```

## Key characteristics

* Router decomposes the query
* Zero or more specialized agents are invoked in parallel
* Results are synthesized into a coherent response

## When to use

Use the router pattern when you have distinct verticals (separate knowledge domains that each require their own agent), need to query multiple sources in parallel, and want to synthesize results into a combined response.

## Basic implementation

The router classifies the query and directs it to the appropriate agent(s). Use [`Command`](/oss/langgraph/graph-api#command) for single-agent routing or [`Send`](/oss/langgraph/graph-api#send) for parallel fan-out to multiple agents.

**Single agent**

Use `Command` to route to a single specialized agent:

```python
from langgraph.types import Command

def classify_query(query: str) -> str:
    """Use LLM to classify query and determine the appropriate agent."""
    # Classification logic here
    ...

def route_query(state: State) -> Command:
    """Route to the appropriate agent based on query classification."""
    active_agent = classify_query(state["query"])

    # Route to the selected agent
    return Command(goto=active_agent)
```

**Multiple agents (parallel)**

Use `Send` to fan out to multiple specialized agents in parallel:

```python
from typing import TypedDict
from langgraph.types import Send

class ClassificationResult(TypedDict):
    query: str
    agent: str

def classify_query(query: str) -> list[ClassificationResult]:
    """Use LLM to classify query and determine which agents to invoke."""
    # Classification logic here
    ...

def route_query(state: State):
    """Route to relevant agents based on query classification."""
    classifications = classify_query(state["query"])

    # Fan out to selected agents in parallel
    return [
        Send(c["agent"], {"query": c["query"]})
        for c in classifications
    ]
```

For a complete implementation, see the tutorial below.

- [Tutorial: Build a multi-source knowledge base with routing](/oss/langchain/multi-agent/router-knowledge-base)

Build a router that queries GitHub, Notion, and Slack in parallel, then synthesizes results into a coherent answer. Covers state definition, specialized agents, parallel execution with `Send`, and result synthesis.

## Stateless vs. stateful

Two approaches:
* [**Stateless routers**](#stateless) address each request independently
* [**Stateful routers**](#stateful) maintain conversation history across requests

## Stateless

Each request is routed independently—no memory between calls. For multi-turn conversations, see [Stateful routers](#stateful).

**Tip:**

**Router vs. Subagents**: Both patterns can dispatch work to multiple agents, but they differ in how routing decisions are made:

- **Router**: A dedicated routing step (often a single LLM call or rule-based logic) that classifies the input and dispatches to agents. The router itself typically doesn't maintain conversation history or perform multi-turn orchestration—it's a preprocessing step.
- **Subagents**: A main supervisor agent dynamically decides which [subagents](/oss/langchain/multi-agent/subagents) to call as part of an ongoing conversation. The main agent maintains context, can call multiple subagents across turns, and orchestrates complex multi-step workflows.

Use a **router** when you have clear input categories and want deterministic or lightweight classification. Use a **supervisor** when you need flexible, conversation-aware orchestration where the LLM decides what to do next based on evolving context.

## Stateful

For multi-turn conversations, you need to maintain context across invocations.

### Tool wrapper

The simplest approach: wrap the stateless router as a tool that a conversational agent can call. The conversational agent handles memory and context; the router stays stateless. This avoids the complexity of managing conversation history across multiple parallel agents.

```python
@tool
def search_docs(query: str) -> str:
    """Search across multiple documentation sources."""
    result = workflow.invoke({"query": query})  # [!code highlight]
    return result["final_answer"]

# Conversational agent uses the router as a tool
conversational_agent = create_agent(
    model,
    tools=[search_docs],
    prompt="You are a helpful assistant. Use search_docs to answer questions."
)
```

### Full persistence

If you need the router itself to maintain state, use [persistence](/oss/langchain/short-term-memory) to store message history. When routing to an agent, fetch previous messages from state and selectively include them in the agent's context—this is a lever for [context engineering](/oss/langchain/context-engineering).

**Warning:**

**Stateful routers require custom history management.** If the router switches between agents across turns, conversations may not feel fluid to end users when agents have different tones or prompts. With parallel invocation, you'll need to maintain history at the router level (inputs and synthesized outputs) and leverage this history in routing logic. Consider the [handoffs pattern](/oss/langchain/multi-agent/handoffs) or [subagents pattern](/oss/langchain/multi-agent/subagents) instead—both provide clearer semantics for multi-turn conversations.

---

# Build a SQL assistant with on-demand skills
> 출처: data/raw/langchain/multi-agent/skills-sql-assistant.mdx | https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant

This tutorial shows how to use **progressive disclosure** - a context management technique where the agent loads information on-demand rather than upfront - to implement **skills** (specialized prompt-based instructions). The agent loads skills via tool calls, rather than dynamically changing the system prompt, discovering and loading only the skills it needs for each task.

**Use case:** Imagine building an agent to help write SQL queries across different business verticals in a large enterprise. Your organization might have separate datastores for each vertical, or a single monolithic database with thousands of tables. Either way, loading all schemas upfront would overwhelm the context window. Progressive disclosure solves this by loading only the relevant schema when needed. This architecture also enables different product owners and stakeholders to independently contribute and maintain skills for their specific business verticals.

**What you'll build:** A SQL query assistant with two skills (sales analytics and inventory management). The agent sees lightweight skill descriptions in its system prompt, then loads full database schemas and business logic through tool calls only when relevant to the user's query.

**Note:**

For a complete example of a SQL agent with query execution, error correction, and validation, see our [SQL Agent tutorial](/oss/langchain/sql-agent). This tutorial focuses on the progressive disclosure pattern which can be applied to any domain.

**Tip:**

Progressive disclosure was popularized by Anthropic as a technique for building scalable agent skills systems. This approach uses a three-level architecture (metadata → core content → detailed resources) where agents load information only as needed. For more on this technique, see [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).

## How it works

Here's the flow when a user asks for a SQL query:

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#E5F4FF','primaryTextColor':'#030710','primaryBorderColor':'#006DDD','lineColor':'#40668D','secondaryColor':'#F6FFDB','tertiaryColor':'#FDF3FF','tertiaryBorderColor':'#7E65AE','tertiaryTextColor':'#504B5F'}}}%%
flowchart TD
    Start([💬 User: Write SQL query<br/>for high-value customers]) --> SystemPrompt[📋 Agent sees skill descriptions:<br/>• sales_analytics<br/>• inventory_management]

SystemPrompt --> Decide{🤔 Need sales schema}

Decide --> LoadSkill[🔧 load_skill<br/>'sales_analytics']

LoadSkill --> Schema[📊 Schema loaded:<br/>customers, orders tables<br/>+ business logic]

Schema --> WriteQuery[✍️ Agent writes SQL query<br/>using schema knowledge]

WriteQuery --> Response([✅ Returns valid SQL<br/>following business rules])

%% Styling for light and dark modes
classDef startEnd fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
classDef decision fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
classDef enrichment fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33

    class Start,Response startEnd
    class SystemPrompt,LoadSkill,WriteQuery process
    class Decide decision
    class Schema enrichment
```

**Why progressive disclosure:**
- **Reduces context usage** - load only the 2-3 skills needed for a task, not all available skills
- **Enables team autonomy** - different teams can develop specialized skills independently (similar to other multi-agent architectures)
- **Scales efficiently** - add dozens or hundreds of skills without overwhelming context
- **Simplifies conversation history** - single agent with one conversation thread

**What are skills:** Skills, as popularized by Claude Code, are primarily prompt-based: self-contained units of specialized instructions for specific business tasks. In Claude Code, skills are exposed as directories with files on the file system, discovered through file operations. Skills guide behavior through prompts and can provide information about tool usage or include sample code for a coding agent to execute.

**Tip:**

Skills with progressive disclosure can be viewed as a form of [RAG (Retrieval-Augmented Generation)](/oss/deepagents/rag), where each skill is a retrieval unit—though not necessarily backed by embeddings or keyword search, but by tools for browsing content (like file operations or, in this tutorial, direct lookup).

**Trade-offs:**
- **Latency**: Loading skills on-demand requires additional tool calls, which adds latency to the first request that needs each skill
- **Workflow control**: Basic implementations rely on prompting to guide skill usage - you cannot enforce hard constraints like "always try skill A before skill B" without custom logic

**Tip:**

**Implementing your own skills system**

When building your own skills implementation (as we do in this tutorial), the core concept is progressive disclosure - loading information on-demand. Beyond that, you have full flexibility in implementation:

- **Storage**: databases, S3, in-memory data structures, or any backend
- **Discovery**: direct lookup (this tutorial), RAG for large skill collections, file system scanning, or API calls
- **Loading logic**: customize latency characteristics and add logic to search through skill content or rank relevance
- **Side effects**: define what happens when a skill loads, such as exposing tools associated with that skill (covered in section 8)

This flexibility lets you optimize for your specific requirements around performance, storage, and workflow control.

## Setup

### Installation

This tutorial requires the `langchain` package:

```bash pip
pip install langchain
```
```bash uv
uv add langchain
```
```bash conda
conda install langchain -c conda-forge
```

For more details, see our [Installation guide](/oss/langchain/install).

### LangSmith

Set up [LangSmith](https://smith.langchain.com) to inspect what is happening inside your agent. Then set the following environment variables:

```bash Shell
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```
```python Python
import getpass
import os

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass()
```

### Select an LLM

Select a chat model from LangChain's suite of integrations:

**OpenAI**

👉 Read the [OpenAI chat model integration docs](/oss/python/integrations/chat/openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-5.5")
```
```python Model Class
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-..."

model = ChatOpenAI(model="gpt-5.5")
```

**Anthropic**

👉 Read the [Anthropic chat model integration docs](/oss/python/integrations/chat/anthropic/)

```bash pip
pip install -U "langchain[anthropic]"
```

```bash uv
uv add "langchain[anthropic]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = init_chat_model("claude-sonnet-4-6")
```
```python Model Class
import os
from langchain_anthropic import ChatAnthropic

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = ChatAnthropic(model="claude-sonnet-4-6")
```

**Azure**

👉 Read the [Azure chat model integration docs](/oss/python/integrations/chat/azure_chat_openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = init_chat_model(
    "azure_openai:gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
```
```python Model Class
import os
from langchain_openai import AzureChatOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = AzureChatOpenAI(
    model="gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
)
```

**Google Gemini**

👉 Read the [Google GenAI chat model integration docs](/oss/python/integrations/chat/google_generative_ai/)

```bash pip
pip install -U "langchain[google-genai]"
```

```bash uv
uv add "langchain[google-genai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["GOOGLE_API_KEY"] = "..."

model = init_chat_model("google_genai:gemini-3.7-flash")
```
```python Model Class
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "..."

model = ChatGoogleGenerativeAI(model="gemini-3.7-flash")
```

**AWS Bedrock**

👉 Read the [AWS Bedrock chat model integration docs](/oss/python/integrations/chat/bedrock/)

```bash pip
pip install -U "langchain[aws]"
```

```bash uv
uv add "langchain[aws]"
```

```python init_chat_model
from langchain.chat_models import init_chat_model

# Follow the steps here to configure your credentials:
# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html

model = init_chat_model(
    "us.anthropic.claude-sonnet-4-6",
    model_provider="bedrock_converse",
)
```
```python Model Class
from langchain_aws import ChatBedrock

model = ChatBedrock(model="us.anthropic.claude-sonnet-4-6")
```

**HuggingFace**

👉 Read the [HuggingFace chat model integration docs](/oss/python/integrations/chat/huggingface/)

```bash pip
pip install -U "langchain[huggingface]"
```

```bash uv
uv add "langchain[huggingface]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

model = init_chat_model(
    "microsoft/Phi-3-mini-4k-instruct",
    model_provider="huggingface",
    temperature=0.7,
    max_tokens=1024,
)
```

```python Model Class
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    temperature=0.7,
    max_length=1024,
)
model = ChatHuggingFace(llm=llm)
```

**OpenRouter**

👉 Read the [OpenRouter chat model integration docs](/oss/python/integrations/chat/openrouter/)

```bash pip
pip install -U "langchain-openrouter"
```

```bash uv
uv add "langchain-openrouter"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = init_chat_model(
    "auto",
    model_provider="openrouter",
)
```
```python Model Class
import os
from langchain_openrouter import ChatOpenRouter

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = ChatOpenRouter(model="auto")
```

## 1. Define skills

First, define the structure for skills. Each skill has a name, a brief description (shown in the system prompt), and full content (loaded on-demand):

```python
from typing import TypedDict

class Skill(TypedDict):  # [!code highlight]
    """A skill that can be progressively disclosed to the agent."""
    name: str  # Unique identifier for the skill
    description: str  # 1-2 sentence description to show in system prompt
    content: str  # Full skill content with detailed instructions
```

Now define example skills for a SQL query assistant. The skills are designed to be **lightweight in description** (shown to the agent upfront) but **detailed in content** (loaded only when needed):

**View complete skill definitions**

```python
SKILLS: list[Skill] = [
    {
        "name": "sales_analytics",
        "description": "Database schema and business logic for sales data analysis including customers, orders, and revenue.",
        "content": """# Sales Analytics Schema

## Tables

### customers
- customer_id (PRIMARY KEY)
- name
- email
- signup_date
- status (active/inactive)
- customer_tier (bronze/silver/gold/platinum)

### orders
- order_id (PRIMARY KEY)
- customer_id (FOREIGN KEY -> customers)
- order_date
- status (pending/completed/cancelled/refunded)
- total_amount
- sales_region (north/south/east/west)

### order_items
- item_id (PRIMARY KEY)
- order_id (FOREIGN KEY -> orders)
- product_id
- quantity
- unit_price
- discount_percent

## Business Logic

**Active customers**: status = 'active' AND signup_date <= CURRENT_DATE - INTERVAL '90 days'

**Revenue calculation**: Only count orders with status = 'completed'. Use total_amount from orders table, which already accounts for discounts.

**Customer lifetime value (CLV)**: Sum of all completed order amounts for a customer.

**High-value orders**: Orders with total_amount > 1000

## Example Query

-- Get top 10 customers by revenue in the last quarter
SELECT
    c.customer_id,
    c.name,
    c.customer_tier,
    SUM(o.total_amount) as total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
  AND o.order_date >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY c.customer_id, c.name, c.customer_tier
ORDER BY total_revenue DESC
LIMIT 10;
""",
    },
    {
        "name": "inventory_management",
        "description": "Database schema and business logic for inventory tracking including products, warehouses, and stock levels.",
        "content": """# Inventory Management Schema

## Tables

### products
- product_id (PRIMARY KEY)
- product_name
- sku
- category
- unit_cost
- reorder_point (minimum stock level before reordering)
- discontinued (boolean)

### warehouses
- warehouse_id (PRIMARY KEY)
- warehouse_name
- location
- capacity

### inventory
- inventory_id (PRIMARY KEY)
- product_id (FOREIGN KEY -> products)
- warehouse_id (FOREIGN KEY -> warehouses)
- quantity_on_hand
- last_updated

### stock_movements
- movement_id (PRIMARY KEY)
- product_id (FOREIGN KEY -> products)
- warehouse_id (FOREIGN KEY -> warehouses)
- movement_type (inbound/outbound/transfer/adjustment)
- quantity (positive for inbound, negative for outbound)
- movement_date
- reference_number

## Business Logic

**Available stock**: quantity_on_hand from inventory table where quantity_on_hand > 0

**Products needing reorder**: Products where total quantity_on_hand across all warehouses is less than or equal to the product's reorder_point

**Active products only**: Exclude products where discontinued = true unless specifically analyzing discontinued items

**Stock valuation**: quantity_on_hand * unit_cost for each product

## Example Query

-- Find products below reorder point across all warehouses
SELECT
    p.product_id,
    p.product_name,
    p.reorder_point,
    SUM(i.quantity_on_hand) as total_stock,
    p.unit_cost,
    (p.reorder_point - SUM(i.quantity_on_hand)) as units_to_reorder
FROM products p
JOIN inventory i ON p.product_id = i.product_id
WHERE p.discontinued = false
GROUP BY p.product_id, p.product_name, p.reorder_point, p.unit_cost
HAVING SUM(i.quantity_on_hand) <= p.reorder_point
ORDER BY units_to_reorder DESC;
""",
    },
]
```

## 2. Create skill loading tool

Create a tool to load full skill content on-demand:

```python
from langchain.tools import tool

@tool  # [!code highlight]
def load_skill(skill_name: str) -> str:
    """Load the full content of a skill into the agent's context.

Use this when you need detailed information about how to handle a specific
type of request. This will provide you with comprehensive instructions,
policies, and guidelines for the skill area.

Args:
    skill_name: The name of the skill to load (e.g., "expense_reporting", "travel_booking")
"""
# Find and return the requested skill
for skill in SKILLS:
    if skill["name"] == skill_name:
        return f"Loaded skill: {skill_name}\n\n{skill['content']}"  # [!code highlight]

    # Skill not found
    available = ", ".join(s["name"] for s in SKILLS)
    return f"Skill '{skill_name}' not found. Available skills: {available}"
```

The `load_skill` tool returns the full skill content as a string, which becomes part of the conversation as a ToolMessage. For more details on creating and using tools, see the [Tools guide](/oss/langchain/tools).

## 3. Build skill middleware

Create custom middleware that injects skill descriptions into the system prompt. This middleware makes skills discoverable without loading their full content upfront.

**Note:**

This guide demonstrates creating custom middleware. For a comprehensive guide on middleware concepts and patterns, see the [custom middleware documentation](/oss/langchain/middleware/custom).

```python
from langchain.agents.middleware import ModelRequest, ModelResponse, AgentMiddleware
from langchain.messages import SystemMessage
from typing import Callable

class SkillMiddleware(AgentMiddleware):  # [!code highlight]
    """Middleware that injects skill descriptions into the system prompt."""

# Register the load_skill tool as a class variable
tools = [load_skill]  # [!code highlight]

def __init__(self):
    """Initialize and generate the skills prompt from SKILLS."""
    # Build skills prompt from the SKILLS list
    skills_list = []
    for skill in SKILLS:
        skills_list.append(
            f"- **{skill['name']}**: {skill['description']}"
        )
    self.skills_prompt = "\n".join(skills_list)

def wrap_model_call(
    self,
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """Sync: Inject skill descriptions into system prompt."""
    # Build the skills addendum
    skills_addendum = ( # [!code highlight]
        f"\n\n## Available Skills\n\n{self.skills_prompt}\n\n" # [!code highlight]
        "Use the load_skill tool when you need detailed information " # [!code highlight]
        "about handling a specific type of request." # [!code highlight]
    )

        # Append to system message content blocks
        new_content = list(request.system_message.content_blocks) + [
            {"type": "text", "text": skills_addendum}
        ]
        new_system_message = SystemMessage(content=new_content)
        modified_request = request.override(system_message=new_system_message)
        return handler(modified_request)
```

The middleware appends skill descriptions to the system prompt, making the agent aware of available skills without loading their full content. The `load_skill` tool is registered as a class variable, making it available to the agent.

**Note:**

**Production consideration**: This tutorial loads the skill list in `__init__` for simplicity. In a production system, you may want to load skills in the `before_agent` hook instead, allowing them to be refreshed periodically to reflect up-to-date changes (e.g., when new skills are added or existing ones are modified). See the [before_agent hook documentation](/oss/langchain/middleware/custom#node-style-hooks) for details.

## 4. Create the agent with skill support

Now create the agent with the skill middleware and a checkpointer for state persistence:

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# Create the agent with skill support
agent = create_agent(
    model,
    system_prompt=(
        "You are a SQL query assistant that helps users "
        "write queries against business databases."
    ),
    middleware=[SkillMiddleware()],  # [!code highlight]
    checkpointer=InMemorySaver(),
)
```

The agent now has access to skill descriptions in its system prompt and can call `load_skill` to retrieve full skill content when needed. The checkpointer maintains conversation history across turns.

## 5. Test progressive disclosure

Test the agent with a question that requires skill-specific knowledge:

```python
from langchain_core.utils.uuid import uuid7

# Configuration for this conversation thread
thread_id = str(uuid7())
config = {"configurable": {"thread_id": thread_id}}

# Ask for a SQL query
result = agent.invoke(  # [!code highlight]
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Write a SQL query to find all customers "
                    "who made orders over $1000 in the last month"
                ),
            }
        ]
    },
    config
)

# Print the conversation
for message in result["messages"]:
    if hasattr(message, 'pretty_print'):
        message.pretty_print()
    else:
        print(f"{message.type}: {message.content}")
```

Expected output:

```
================================ Human Message =================================

Write a SQL query to find all customers who made orders over $1000 in the last month
================================== Ai Message ==================================
Tool Calls:
  load_skill (call_abc123)
 Call ID: call_abc123
  Args:
    skill_name: sales_analytics
================================= Tool Message =================================
Name: load_skill

Loaded skill: sales_analytics

# Sales Analytics Schema

## Tables

### customers
- customer_id (PRIMARY KEY)
- name
- email
- signup_date
- status (active/inactive)
- customer_tier (bronze/silver/gold/platinum)

### orders
- order_id (PRIMARY KEY)
- customer_id (FOREIGN KEY -> customers)
- order_date
- status (pending/completed/cancelled/refunded)
- total_amount
- sales_region (north/south/east/west)

[... rest of schema ...]

## Business Logic

**High-value orders**: Orders with `total_amount > 1000`
**Revenue calculation**: Only count orders with `status = 'completed'`

================================== Ai Message ==================================

Here's a SQL query to find all customers who made orders over $1000 in the last month:

\`\`\`sql
SELECT DISTINCT
    c.customer_id,
    c.name,
    c.email,
    c.customer_tier
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > 1000
  AND o.status = 'completed'
  AND o.order_date >= CURRENT_DATE - INTERVAL '1 month'
ORDER BY c.customer_id;
\`\`\`

This query:
- Joins customers with their orders
- Filters for high-value orders (>$1000) using the total_amount field
- Only includes completed orders (as per the business logic)
- Restricts to orders from the last month
- Returns distinct customers to avoid duplicates if they made multiple qualifying orders
```

The agent saw the lightweight skill description in its system prompt, recognized the question required sales database knowledge, called `load_skill("sales_analytics")` to get the full schema and business logic, and then used that information to write a correct query following the database conventions.

## 6. Advanced: Add constraints with custom state

**Optional: Track loaded skills and enforce tool constraints**

You can add constraints to enforce that certain tools are only available after specific skills have been loaded. This requires tracking which skills have been loaded in custom agent state.

### Define custom state

First, extend the agent state to track loaded skills:

```python
from langchain.agents.middleware import AgentState

class CustomState(AgentState):  # [!code highlight]
    skills_loaded: NotRequired[list[str]]  # Track which skills have been loaded  # [!code highlight]
```

### Update load_skill to modify state

Modify the `load_skill` tool to update state when a skill is loaded:

```python
from langgraph.types import Command  # [!code highlight]
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage  # [!code highlight]

@tool
def load_skill(skill_name: str, runtime: ToolRuntime) -> Command:  # [!code highlight]
    """Load the full content of a skill into the agent's context.

Use this when you need detailed information about how to handle a specific
type of request. This will provide you with comprehensive instructions,
policies, and guidelines for the skill area.

Args:
    skill_name: The name of the skill to load
"""
# Find and return the requested skill
for skill in SKILLS:
    if skill["name"] == skill_name:
        skill_content = f"Loaded skill: {skill_name}\n\n{skill['content']}"

# Update state to track loaded skill
return Command(  # [!code highlight]
    update={  # [!code highlight]
        "messages": [  # [!code highlight]
            ToolMessage(  # [!code highlight]
                content=skill_content,  # [!code highlight]
                tool_call_id=runtime.tool_call_id,  # [!code highlight]
            )  # [!code highlight]
        ],  # [!code highlight]
        "skills_loaded": [skill_name],  # [!code highlight]
    }  # [!code highlight]
)  # [!code highlight]

    # Skill not found
    available = ", ".join(s["name"] for s in SKILLS)
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content=f"Skill '{skill_name}' not found. Available skills: {available}",
                    tool_call_id=runtime.tool_call_id,
                )
            ]
        }
    )
```

### Create constrained tool

Create a tool that's only usable after a specific skill has been loaded:

```python
@tool
def write_sql_query(  # [!code highlight]
    query: str,
    vertical: str,
    runtime: ToolRuntime,
) -> str:
    """Write and validate a SQL query for a specific business vertical.

This tool helps format and validate SQL queries. You must load the
appropriate skill first to understand the database schema.

Args:
    query: The SQL query to write
    vertical: The business vertical (sales_analytics or inventory_management)
"""
# Check if the required skill has been loaded
skills_loaded = runtime.state.get("skills_loaded", [])  # [!code highlight]

if vertical not in skills_loaded:  # [!code highlight]
    return (  # [!code highlight]
        f"Error: You must load the '{vertical}' skill first "  # [!code highlight]
        f"to understand the database schema before writing queries. "  # [!code highlight]
        f"Use load_skill('{vertical}') to load the schema."  # [!code highlight]
    )  # [!code highlight]

    # Validate and format the query
    return (
        f"SQL Query for {vertical}:\n\n"
        f"```sql\n{query}\n```\n\n"
        f"✓ Query validated against {vertical} schema\n"
        f"Ready to execute against the database."
    )
```

### Update middleware and agent

Update the middleware to use the custom state schema:

```python
class SkillMiddleware(AgentMiddleware[CustomState]):  # [!code highlight]
    """Middleware that injects skill descriptions into the system prompt."""

state_schema = CustomState  # [!code highlight]
tools = [load_skill, write_sql_query]  # [!code highlight]

    # ... rest of the middleware implementation stays the same
```

Create the agent with the middleware that registers the constrained tool:

```python
agent = create_agent(
    model,
    system_prompt=(
        "You are a SQL query assistant that helps users "
        "write queries against business databases."
    ),
    middleware=[SkillMiddleware()],  # [!code highlight]
    checkpointer=InMemorySaver(),
)
```

Now if the agent tries to use `write_sql_query` before loading the required skill, it will receive an error message prompting it to load the appropriate skill (e.g., `sales_analytics` or `inventory_management`) first. This ensures the agent has the necessary schema knowledge before attempting to validate queries.

## Complete example

**View complete runnable script**

Here's a complete, runnable implementation combining all the pieces from this tutorial:

```python
from langchain_core.utils.uuid import uuid7
from typing import TypedDict, NotRequired
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, AgentMiddleware
from langchain.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from typing import Callable

# Define skill structure
class Skill(TypedDict):
    """A skill that can be progressively disclosed to the agent."""
    name: str
    description: str
    content: str

# Define skills with schemas and business logic
SKILLS: list[Skill] = [
    {
        "name": "sales_analytics",
        "description": "Database schema and business logic for sales data analysis including customers, orders, and revenue.",
        "content": """# Sales Analytics Schema

## Tables

### customers
- customer_id (PRIMARY KEY)
- name
- email
- signup_date
- status (active/inactive)
- customer_tier (bronze/silver/gold/platinum)

### orders
- order_id (PRIMARY KEY)
- customer_id (FOREIGN KEY -> customers)
- order_date
- status (pending/completed/cancelled/refunded)
- total_amount
- sales_region (north/south/east/west)

### order_items
- item_id (PRIMARY KEY)
- order_id (FOREIGN KEY -> orders)
- product_id
- quantity
- unit_price
- discount_percent

## Business Logic

**Active customers**: status = 'active' AND signup_date <= CURRENT_DATE - INTERVAL '90 days'

**Revenue calculation**: Only count orders with status = 'completed'. Use total_amount from orders table, which already accounts for discounts.

**Customer lifetime value (CLV)**: Sum of all completed order amounts for a customer.

**High-value orders**: Orders with total_amount > 1000

## Example Query

-- Get top 10 customers by revenue in the last quarter
SELECT
    c.customer_id,
    c.name,
    c.customer_tier,
    SUM(o.total_amount) as total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
  AND o.order_date >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY c.customer_id, c.name, c.customer_tier
ORDER BY total_revenue DESC
LIMIT 10;
""",
    },
    {
        "name": "inventory_management",
        "description": "Database schema and business logic for inventory tracking including products, warehouses, and stock levels.",
        "content": """# Inventory Management Schema

## Tables

### products
- product_id (PRIMARY KEY)
- product_name
- sku
- category
- unit_cost
- reorder_point (minimum stock level before reordering)
- discontinued (boolean)

### warehouses
- warehouse_id (PRIMARY KEY)
- warehouse_name
- location
- capacity

### inventory
- inventory_id (PRIMARY KEY)
- product_id (FOREIGN KEY -> products)
- warehouse_id (FOREIGN KEY -> warehouses)
- quantity_on_hand
- last_updated

### stock_movements
- movement_id (PRIMARY KEY)
- product_id (FOREIGN KEY -> products)
- warehouse_id (FOREIGN KEY -> warehouses)
- movement_type (inbound/outbound/transfer/adjustment)
- quantity (positive for inbound, negative for outbound)
- movement_date
- reference_number

## Business Logic

**Available stock**: quantity_on_hand from inventory table where quantity_on_hand > 0

**Products needing reorder**: Products where total quantity_on_hand across all warehouses is less than or equal to the product's reorder_point

**Active products only**: Exclude products where discontinued = true unless specifically analyzing discontinued items

**Stock valuation**: quantity_on_hand * unit_cost for each product

## Example Query

-- Find products below reorder point across all warehouses
SELECT
    p.product_id,
    p.product_name,
    p.reorder_point,
    SUM(i.quantity_on_hand) as total_stock,
    p.unit_cost,
    (p.reorder_point - SUM(i.quantity_on_hand)) as units_to_reorder
FROM products p
JOIN inventory i ON p.product_id = i.product_id
WHERE p.discontinued = false
GROUP BY p.product_id, p.product_name, p.reorder_point, p.unit_cost
HAVING SUM(i.quantity_on_hand) <= p.reorder_point
ORDER BY units_to_reorder DESC;
""",
    },
]

# Create skill loading tool
@tool
def load_skill(skill_name: str) -> str:
    """Load the full content of a skill into the agent's context.

Use this when you need detailed information about how to handle a specific
type of request. This will provide you with comprehensive instructions,
policies, and guidelines for the skill area.

Args:
    skill_name: The name of the skill to load (e.g., "sales_analytics", "inventory_management")
"""
# Find and return the requested skill
for skill in SKILLS:
    if skill["name"] == skill_name:
        return f"Loaded skill: {skill_name}\n\n{skill['content']}"

# Skill not found
available = ", ".join(s["name"] for s in SKILLS)
return f"Skill '{skill_name}' not found. Available skills: {available}"

# Create skill middleware
class SkillMiddleware(AgentMiddleware):
    """Middleware that injects skill descriptions into the system prompt."""

# Register the load_skill tool as a class variable
tools = [load_skill]

def __init__(self):
    """Initialize and generate the skills prompt from SKILLS."""
    # Build skills prompt from the SKILLS list
    skills_list = []
    for skill in SKILLS:
        skills_list.append(
            f"- **{skill['name']}**: {skill['description']}"
        )
    self.skills_prompt = "\n".join(skills_list)

def wrap_model_call(
    self,
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """Sync: Inject skill descriptions into system prompt."""
    # Build the skills addendum
    skills_addendum = (
        f"\n\n## Available Skills\n\n{self.skills_prompt}\n\n"
        "Use the load_skill tool when you need detailed information "
        "about handling a specific type of request."
    )

# Append to system message content blocks
new_content = list(request.system_message.content_blocks) + [
    {"type": "text", "text": skills_addendum}
]
new_system_message = SystemMessage(content=new_content)
modified_request = request.override(system_message=new_system_message)
return handler(modified_request)

# Initialize your chat model (replace with your model)
# Example: from langchain_anthropic import ChatAnthropic
# model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-5.5")

# Create the agent with skill support
agent = create_agent(
    model,
    system_prompt=(
        "You are a SQL query assistant that helps users "
        "write queries against business databases."
    ),
    middleware=[SkillMiddleware()],
    checkpointer=InMemorySaver(),
)

# Example usage
if __name__ == "__main__":
    # Configuration for this conversation thread
    thread_id = str(uuid7())
    config = {"configurable": {"thread_id": thread_id}}

# Ask for a SQL query
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Write a SQL query to find all customers "
                    "who made orders over $1000 in the last month"
                ),
            }
        ]
    },
    config
)

    # Print the conversation
    for message in result["messages"]:
        if hasattr(message, 'pretty_print'):
            message.pretty_print()
        else:
            print(f"{message.type}: {message.content}")
```

This complete example includes:
- Skill definitions with full database schemas
- The `load_skill` tool for on-demand loading
- `SkillMiddleware` that injects skill descriptions into the system prompt
- Agent creation with middleware and checkpointer
- Example usage showing how the agent loads skills and writes SQL queries

To run this, you'll need to:
1. Install required packages: `pip install langchain langchain-openai langgraph`
2. Set your API key (e.g., `export OPENAI_API_KEY=...`)
3. Replace the model initialization with your preferred LLM provider

## Implementation variations

**View implementation options and trade-offs**

This tutorial implemented skills as in-memory Python dictionaries loaded through tool calls. However, there are several ways to implement progressive disclosure with skills:

**Storage backends:**
- **In-memory** (this tutorial): Skills defined as Python data structures, fast access, no I/O overhead
- **File system** (Claude Code approach): Skills as directories with files, discovered via file operations like `read_file`
- **Remote storage**: Skills in S3, databases, Notion, or APIs, fetched on-demand

**Skill discovery** (how the agent learns which skills exist):
- **System prompt listing**: Skill descriptions in system prompt (used in this tutorial)
- **File-based**: Discover skills by scanning directories (Claude Code approach)
- **Registry-based**: Query a skill registry service or API for available skills
- **Dynamic lookup**: List available skills via a tool call

**Progressive disclosure strategies** (how skill content is loaded):
- **Single load**: Load entire skill content in one tool call (used in this tutorial)
- **Paginated**: Load skill content in multiple pages/chunks for large skills
- **Search-based**: Search within a specific skill's content for relevant sections (e.g., using grep/read operations on skill files)
- **Hierarchical**: Load skill overview first, then drill into specific subsections

**Size considerations** (uncalibrated mental model - optimize for your system):
- **Small skills** (< 1K tokens / ~750 words): Can be included directly in system prompt and cached with prompt caching for cost savings and faster responses
- **Medium skills** (1-10K tokens / ~750-7.5K words): Benefit from on-demand loading to avoid context overhead (this tutorial)
- **Large skills** (> 10K tokens / ~7.5K words, or > 5-10% of context window): Should use progressive disclosure techniques like pagination, search-based loading, or hierarchical exploration to avoid consuming excessive context

The choice depends on your requirements: in-memory is fastest but requires redeployment for skill updates, while file-based or remote storage enables dynamic skill management without code changes.

## Progressive disclosure and context engineering

**Combining with few-shot prompting and other techniques**

Progressive disclosure is fundamentally a **[context engineering](/oss/langchain/context-engineering) technique** - you're managing what information is available to the agent and when. This tutorial focused on loading database schemas, but the same principles apply to other types of context.

### Combining with few-shot prompting

For the SQL query use case, you could extend progressive disclosure to dynamically load **few-shot examples** that match the user's query:

**Example approach:**
1. User asks: "Find customers who haven't ordered in 6 months"
2. Agent loads `sales_analytics` schema (as shown in this tutorial)
3. Agent also loads 2-3 relevant example queries (via semantic search or tag-based lookup):
   - Query for finding inactive customers
   - Query with date-based filtering
   - Query joining customers and orders tables
4. Agent writes query using both schema knowledge AND example patterns

This combination of progressive disclosure (loading schemas on-demand) and dynamic few-shot prompting (loading relevant examples) creates a powerful context engineering pattern that scales to large knowledge bases while providing high-quality, grounded outputs.

## Next steps

- Learn about [middleware](/oss/langchain/middleware) for more dynamic agent behaviors
- Explore [context engineering](/oss/langchain/context-engineering) techniques for managing agent context
- Explore the [handoffs pattern](/oss/langchain/multi-agent/handoffs-customer-support) for sequential workflows
- Read the [subagents pattern](/oss/langchain/multi-agent/subagents-personal-assistant) for parallel task routing
- See [multi-agent patterns](/oss/langchain/multi-agent) for other approaches to specialized agents
- Use [LangSmith](https://smith.langchain.com) to debug and monitor skill loading

---

# Skills
> 출처: data/raw/langchain/multi-agent/skills.mdx | https://docs.langchain.com/oss/python/langchain/multi-agent/skills

In the **skills** architecture, specialized capabilities are packaged as invocable "skills" that augment an [agent's](/oss/langchain/agents) behavior. Skills are primarily prompt-driven specializations that an agent can invoke on-demand.
For built-in skill support, see [Deep Agents](/oss/deepagents/skills).

**Tip:**

This pattern is conceptually identical to [Agent Skills](https://agentskills.io/) and [llms.txt](https://llmstxt.org/) (introduced by Jeremy Howard), which uses tool calling for progressive disclosure of documentation. The skills pattern applies progressive disclosure to specialized prompts and domain knowledge rather than just documentation pages.

For ready-to-use skills that improve your agent's performance on LangChain ecosystem tasks, see the [LangChain Skills](https://github.com/langchain-ai/langchain-skills) repository.

```mermaid
graph LR
    A[User] --> B[Agent]
    B --> C[Skill A]
    B --> D[Skill B]
    B --> E[Skill C]
    B --> A

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A trigger
    class B,C,D,E process
```

## Key characteristics

* Prompt-driven specialization: Skills are primarily defined by specialized prompts
* Progressive disclosure: Skills become available based on context or user needs
* Team distribution: Different teams can develop and maintain skills independently
* Lightweight composition: Skills are simpler than full sub-agents
* Reference awareness: Skills can reference scripts, templates, and other resources

## When to use

Use the skills pattern when you want a single [agent](/oss/langchain/agents) with many possible specializations, you don't need to enforce specific constraints between skills, or different teams need to develop capabilities independently. Common examples include coding assistants (skills for different languages or tasks), knowledge bases (skills for different domains), and creative assistants (skills for different formats).

## Basic implementation

```python
from langchain.tools import tool
from langchain.agents import create_agent

@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill prompt.

Available skills:
- write_sql: SQL query writing expert
- review_legal_doc: Legal document reviewer

    Returns the skill's prompt and context.
    """
    # Load skill content from file/database
    ...

agent = create_agent(
    model="gpt-5.5",
    tools=[load_skill],
    system_prompt=(
        "You are a helpful assistant. "
        "You have access to two skills: "
        "write_sql and review_legal_doc. "
        "Use load_skill to access them."
    ),
)
```

For a complete implementation, see the tutorial below.

- [Tutorial: Build a SQL assistant with on-demand skills](/oss/langchain/multi-agent/skills-sql-assistant)

    Learn how to implement skills with progressive disclosure, where the agent loads specialized prompts and schemas on-demand rather than upfront.

## Extending the pattern

When writing custom implementations, you can extend the basic skills pattern in several ways:

- **Dynamic tool registration**: Combine progressive disclosure with state management to register new [tools](/oss/langchain/tools) as skills load. For example, loading a "database_admin" skill could both add specialized context and register database-specific tools (backup, restore, migrate). This uses the same tool-and-state mechanisms used across multi-agent patterns—tools updating state to dynamically change agent capabilities.

- **Hierarchical skills**: Skills can define other skills in a tree structure, creating nested specializations. For instance, loading a "data_science" skill might make available sub-skills like "pandas_expert", "visualization", and "statistical_analysis". Each sub-skill can be loaded independently as needed, allowing for fine-grained progressive disclosure of domain knowledge. This hierarchical approach helps manage large knowledge bases by organizing capabilities into logical groupings that can be discovered and loaded on-demand.

- **Reference awareness**: While each skill only has one prompt, this prompt can reference the location of other assets and provide information on when the agent should use those assets.
When those assets become relevant, the agent will know that those files exist and read them into memory as needed to complete tasks.
This also follows the progressive disclosure pattern and limits the information in the context window.

---

# Build a personal assistant with subagents
> 출처: data/raw/langchain/multi-agent/subagents-personal-assistant.mdx | https://docs.langchain.com/oss/python/langchain/multi-agent/subagents-personal-assistant

## Overview

The **supervisor pattern** is a [multi-agent](/oss/langchain/multi-agent) architecture where a central supervisor agent coordinates specialized worker agents. This approach excels when tasks require different types of expertise. Rather than building one agent that manages tool selection across domains, you create focused specialists coordinated by a supervisor who understands the overall workflow.

In this tutorial, you'll build a personal assistant system that demonstrates these benefits through a realistic workflow. The system will coordinate two specialists with fundamentally different responsibilities:

- A **calendar agent** that handles scheduling, availability checking, and event management.
- An **email agent** that manages communication, drafts messages, and sends notifications.

We will also incorporate [human-in-the-loop review](/oss/langchain/human-in-the-loop) to allow users to approve, edit, and reject actions (such as outbound emails) as desired.

**Note:**

If you are migrating from the [`langgraph-supervisor`](https://github.com/langchain-ai/langgraph-supervisor-py) package, see [Migrate from langgraph-supervisor](/oss/migrate/langgraph-supervisor) for before-and-after patterns, including interrupt and resume flows.

### Why use a supervisor?

Multi-agent architectures allow you to partition [tools](/oss/langchain/tools) across workers, each with their own individual prompts or instructions. Consider an agent with direct access to all calendar and email APIs: it must choose from many similar tools, understand exact formats for each API, and handle multiple domains simultaneously. If performance degrades, it may be helpful to separate related tools and associated prompts into logical groups (in part to manage iterative improvements).

### Concepts

We will cover the following concepts:

- [Multi-agent systems](/oss/langchain/multi-agent)
- [Human-in-the-loop review](/oss/langchain/human-in-the-loop)

## Setup

### Installation

This tutorial requires the `langchain` package:

```bash pip
pip install langchain
```
```bash conda
conda install langchain -c conda-forge
```

For more details, see our [Installation guide](/oss/langchain/install).

### LangSmith

Set up [LangSmith](https://smith.langchain.com) to inspect what is happening inside your agent. Then set the following environment variables:

```bash Shell
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```
```python Python
import getpass
import os

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass()
```

### Components

We will need to select a chat model from LangChain's suite of integrations:

**OpenAI**

👉 Read the [OpenAI chat model integration docs](/oss/python/integrations/chat/openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-5.5")
```
```python Model Class
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-..."

model = ChatOpenAI(model="gpt-5.5")
```

**Anthropic**

👉 Read the [Anthropic chat model integration docs](/oss/python/integrations/chat/anthropic/)

```bash pip
pip install -U "langchain[anthropic]"
```

```bash uv
uv add "langchain[anthropic]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = init_chat_model("claude-sonnet-4-6")
```
```python Model Class
import os
from langchain_anthropic import ChatAnthropic

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = ChatAnthropic(model="claude-sonnet-4-6")
```

**Azure**

👉 Read the [Azure chat model integration docs](/oss/python/integrations/chat/azure_chat_openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = init_chat_model(
    "azure_openai:gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
```
```python Model Class
import os
from langchain_openai import AzureChatOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = AzureChatOpenAI(
    model="gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
)
```

**Google Gemini**

👉 Read the [Google GenAI chat model integration docs](/oss/python/integrations/chat/google_generative_ai/)

```bash pip
pip install -U "langchain[google-genai]"
```

```bash uv
uv add "langchain[google-genai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["GOOGLE_API_KEY"] = "..."

model = init_chat_model("google_genai:gemini-3.7-flash")
```
```python Model Class
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "..."

model = ChatGoogleGenerativeAI(model="gemini-3.7-flash")
```

**AWS Bedrock**

👉 Read the [AWS Bedrock chat model integration docs](/oss/python/integrations/chat/bedrock/)

```bash pip
pip install -U "langchain[aws]"
```

```bash uv
uv add "langchain[aws]"
```

```python init_chat_model
from langchain.chat_models import init_chat_model

# Follow the steps here to configure your credentials:
# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html

model = init_chat_model(
    "us.anthropic.claude-sonnet-4-6",
    model_provider="bedrock_converse",
)
```
```python Model Class
from langchain_aws import ChatBedrock

model = ChatBedrock(model="us.anthropic.claude-sonnet-4-6")
```

**HuggingFace**

👉 Read the [HuggingFace chat model integration docs](/oss/python/integrations/chat/huggingface/)

```bash pip
pip install -U "langchain[huggingface]"
```

```bash uv
uv add "langchain[huggingface]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

model = init_chat_model(
    "microsoft/Phi-3-mini-4k-instruct",
    model_provider="huggingface",
    temperature=0.7,
    max_tokens=1024,
)
```

```python Model Class
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    temperature=0.7,
    max_length=1024,
)
model = ChatHuggingFace(llm=llm)
```

**OpenRouter**

👉 Read the [OpenRouter chat model integration docs](/oss/python/integrations/chat/openrouter/)

```bash pip
pip install -U "langchain-openrouter"
```

```bash uv
uv add "langchain-openrouter"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = init_chat_model(
    "auto",
    model_provider="openrouter",
)
```
```python Model Class
import os
from langchain_openrouter import ChatOpenRouter

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = ChatOpenRouter(model="auto")
```

## 1. Define tools

Start by defining the tools that require structured inputs. In real applications, these would call actual APIs (Google Calendar, SendGrid, etc.). For this tutorial, you'll use stubs to demonstrate the pattern.

```python
from langchain.tools import tool

@tool
def create_calendar_event(
    title: str,
    start_time: str,       # ISO format: "2024-01-15T14:00:00"
    end_time: str,         # ISO format: "2024-01-15T15:00:00"
    attendees: list[str],  # email addresses
    location: str = ""
) -> str:
    """Create a calendar event. Requires exact ISO datetime format."""
    # Stub: In practice, this would call Google Calendar API, Outlook API, etc.
    return f"Event created: {title} from {start_time} to {end_time} with {len(attendees)} attendees"

@tool
def send_email(
    to: list[str],  # email addresses
    subject: str,
    body: str,
    cc: list[str] = []
) -> str:
    """Send an email via email API. Requires properly formatted addresses."""
    # Stub: In practice, this would call SendGrid, Gmail API, etc.
    return f"Email sent to {', '.join(to)} - Subject: {subject}"

@tool
def get_available_time_slots(
    attendees: list[str],
    date: str,  # ISO format: "2024-01-15"
    duration_minutes: int
) -> list[str]:
    """Check calendar availability for given attendees on a specific date."""
    # Stub: In practice, this would query calendar APIs
    return ["09:00", "14:00", "16:00"]
```

## 2. Create specialized sub-agents

Next, we'll create specialized sub-agents that handle each domain.

### Create a calendar agent

The calendar agent understands natural language scheduling requests and translates them into precise API calls. It handles date parsing, availability checking, and event creation.

```python
from datetime import date

from langchain.agents import create_agent

CALENDAR_AGENT_PROMPT = (
    f"Today's date is {date.today().isoformat()}. "
    "You are a calendar scheduling assistant. "
    "Parse natural language scheduling requests (e.g., 'next Tuesday at 2pm') "
    "into proper ISO datetime formats. "
    "Use get_available_time_slots to check availability when needed. "
    "If there is no suitable time slot, stop and confirm unavailability in your response. "
    "Use create_calendar_event to schedule events. "
    "Always confirm what was scheduled in your final response."
)

calendar_agent = create_agent(
    model,
    tools=[create_calendar_event, get_available_time_slots],
    system_prompt=CALENDAR_AGENT_PROMPT,
)
```

Test the calendar agent to see how it handles natural language scheduling:

```python
query = "Schedule a team meeting next Tuesday at 2pm for 1 hour"

stream = calendar_agent.stream_events(
    {"messages": [{"role": "user", "content": query}]},
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        print(f"Tool result: {item.output}")
```

```
================================== Ai Message ==================================
Tool Calls:
  get_available_time_slots (call_EIeoeIi1hE2VmwZSfHStGmXp)
 Call ID: call_EIeoeIi1hE2VmwZSfHStGmXp
  Args:
    attendees: []
    date: 2024-06-18
    duration_minutes: 60
================================= Tool Message =================================
Name: get_available_time_slots

["09:00", "14:00", "16:00"]
================================== Ai Message ==================================
Tool Calls:
  create_calendar_event (call_zgx3iJA66Ut0W8S3NpT93kEB)
 Call ID: call_zgx3iJA66Ut0W8S3NpT93kEB
  Args:
    title: Team Meeting
    start_time: 2024-06-18T14:00:00
    end_time: 2024-06-18T15:00:00
    attendees: []
================================= Tool Message =================================
Name: create_calendar_event

Event created: Team Meeting from 2024-06-18T14:00:00 to 2024-06-18T15:00:00 with 0 attendees
================================== Ai Message ==================================

The team meeting has been scheduled for next Tuesday, June 18th, at 2:00 PM and will last for 1 hour. If you need to add attendees or a location, please let me know!
```

The agent parses "next Tuesday at 2pm" into ISO format ("2024-01-16T14:00:00"), calculates the end time, calls `create_calendar_event`, and returns a natural language confirmation.

### Create an email agent

The email agent handles message composition and sending. It focuses on extracting recipient information, crafting appropriate subject lines and body text, and managing email communication.

```python
EMAIL_AGENT_PROMPT = (
    "You are an email assistant. "
    "Compose professional emails based on natural language requests. "
    "Extract recipient information and craft appropriate subject lines and body text. "
    "Use send_email to send the message. "
    "Always confirm what was sent in your final response."
)

email_agent = create_agent(
    model,
    tools=[send_email],
    system_prompt=EMAIL_AGENT_PROMPT,
)
```

Test the email agent with a natural language request:

```python
query = "Send the design team a reminder about reviewing the new mockups"

stream = email_agent.stream_events(
    {"messages": [{"role": "user", "content": query}]},
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        print(f"Tool result: {item.output}")
```

```
================================== Ai Message ==================================
Tool Calls:
  send_email (call_OMl51FziTVY6CRZvzYfjYOZr)
 Call ID: call_OMl51FziTVY6CRZvzYfjYOZr
  Args:
    to: ['design-team@example.com']
    subject: Reminder: Please Review the New Mockups
    body: Hi Design Team,

This is a friendly reminder to review the new mockups at your earliest convenience. Your feedback is important to ensure that we stay on track with our project timeline.

Please let me know if you have any questions or need additional information.

Thank you!

Best regards,
================================= Tool Message =================================
Name: send_email

Email sent to design-team@example.com - Subject: Reminder: Please Review the New Mockups
================================== Ai Message ==================================

I've sent a reminder to the design team asking them to review the new mockups. If you need any further communication on this topic, just let me know!
```

The agent infers the recipient from the informal request, crafts a professional subject line and body, calls `send_email`, and returns a confirmation. Each sub-agent has a narrow focus with domain-specific tools and prompts, allowing it to excel at its specific task.

## 3. Wrap sub-agents as tools

Now wrap each sub-agent as a tool that the supervisor can invoke. This is the key architectural step that creates the layered system. The supervisor will see high-level tools like "schedule_event", not low-level tools like "create_calendar_event".

```python
@tool
def schedule_event(request: str) -> str:
    """Schedule calendar events using natural language.

Use this when the user wants to create, modify, or check calendar appointments.
Handles date/time parsing, availability checking, and event creation.

Input: Natural language scheduling request (e.g., 'meeting with design team
next Tuesday at 2pm')
"""
result = calendar_agent.invoke({
    "messages": [{"role": "user", "content": request}]
})
return result["messages"][-1].text

@tool
def manage_email(request: str) -> str:
    """Send emails using natural language.

Use this when the user wants to send notifications, reminders, or any email
communication. Handles recipient extraction, subject generation, and email
composition.

    Input: Natural language email request (e.g., 'send them a reminder about
    the meeting')
    """
    result = email_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text
```

The tool descriptions help the supervisor decide when to use each tool, so make them clear and specific. We return only the sub-agent's final response, as the supervisor doesn't need to see intermediate reasoning or tool calls.

## 4. Create the supervisor agent

Now create the supervisor that orchestrates the sub-agents. The supervisor only sees high-level tools and makes routing decisions at the domain level, not the individual API level.

```python
SUPERVISOR_PROMPT = (
    "You are a helpful personal assistant. "
    "You can schedule calendar events and send emails. "
    "Break down user requests into appropriate tool calls and coordinate the results. "
    "When a request involves multiple actions, use multiple tools in sequence or in parallel as appropriate."
)

supervisor_agent = create_agent(
    model,
    tools=[schedule_event, manage_email],
    system_prompt=SUPERVISOR_PROMPT,
)
```

## 5. Use the supervisor

Now test your complete system with complex requests that require coordination across multiple domains:

### Example 1: Simple single-domain request

```python
query = "Schedule a team standup for tomorrow at 9am"

stream = supervisor_agent.stream_events(
    {"messages": [{"role": "user", "content": query}]},
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        print(f"Tool result: {item.output}")
```

```
================================== Ai Message ==================================
Tool Calls:
  schedule_event (call_mXFJJDU8bKZadNUZPaag8Lct)
 Call ID: call_mXFJJDU8bKZadNUZPaag8Lct
  Args:
    request: Schedule a team standup for tomorrow at 9am with Alice and Bob.
================================= Tool Message =================================
Name: schedule_event

The team standup has been scheduled for tomorrow at 9:00 AM with Alice and Bob. If you need to make any changes or add more details, just let me know!
================================== Ai Message ==================================

The team standup with Alice and Bob is scheduled for tomorrow at 9:00 AM. If you need any further arrangements or adjustments, please let me know!
```

The supervisor identifies this as a calendar task, calls `schedule_event`, and the calendar agent handles date parsing and event creation.

**Tip:**

For full transparency into the information flow, including prompts and responses for each chat model call, check out the [LangSmith trace](https://smith.langchain.com/public/91a9a95f-fba9-4e84-aff0-371861ad2f4a/r) for the above run.

### Example 2: Complex multi-domain request

```python
query = (
    "Schedule a meeting with the design team next Tuesday at 2pm for 1 hour, "
    "and send them an email reminder about reviewing the new mockups."
)

stream = supervisor_agent.stream_events(
    {"messages": [{"role": "user", "content": query}]},
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        print(f"Tool result: {item.output}")
```

```
================================== Ai Message ==================================
Tool Calls:
  schedule_event (call_YA68mqF0koZItCFPx0kGQfZi)
 Call ID: call_YA68mqF0koZItCFPx0kGQfZi
  Args:
    request: meeting with the design team next Tuesday at 2pm for 1 hour
  manage_email (call_XxqcJBvVIuKuRK794ZIzlLxx)
 Call ID: call_XxqcJBvVIuKuRK794ZIzlLxx
  Args:
    request: send the design team an email reminder about reviewing the new mockups
================================= Tool Message =================================
Name: schedule_event

Your meeting with the design team is scheduled for next Tuesday, June 18th, from 2:00pm to 3:00pm. Let me know if you need to add more details or make any changes!
================================= Tool Message =================================
Name: manage_email

I've sent an email reminder to the design team requesting them to review the new mockups. If you need to include more information or recipients, just let me know!
================================== Ai Message ==================================

Your meeting with the design team is scheduled for next Tuesday, June 18th, from 2:00pm to 3:00pm.

I've also sent an email reminder to the design team, asking them to review the new mockups.

Let me know if you'd like to add more details to the meeting or include additional information in the email!
```

The supervisor recognizes this requires both calendar and email actions, calls `schedule_event` for the meeting, then calls `manage_email` for the reminder. Each sub-agent completes its task, and the supervisor synthesizes both results into a coherent response.

**Note:**

The supervisor dispatches tasks to subagents sequentially by default. Each tool call completes before the next one starts. However, many LLMs will issue multiple tool calls in a single response (as shown in the trace above, where both `schedule_event` and `manage_email` are called together), which the runtime executes in parallel. You can also configure explicit parallel dispatch. See the [`create_supervisor` reference docs](https://reference.langchain.com/python/langgraph-supervisor/supervisor/create_supervisor) for details.

**Tip:**

Refer to the [LangSmith trace](https://smith.langchain.com/public/95cd00a3-d1f9-4dba-9731-7bf733fb6a3c/r) to see the detailed information flow for the above run, including individual chat model prompts and responses.

### Complete working example

Here's everything together in a runnable script:

**View complete code**

```python
"""
Personal Assistant Supervisor Example

This example demonstrates the tool calling pattern for multi-agent systems.
A supervisor agent coordinates specialized sub-agents (calendar and email)
that are wrapped as tools.
"""

from datetime import date

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

# ============================================================================
# Step 1: Define low-level API tools (stubbed)
# ============================================================================

@tool
def create_calendar_event(
    title: str,
    start_time: str,  # ISO format: "2024-01-15T14:00:00"
    end_time: str,    # ISO format: "2024-01-15T15:00:00"
    attendees: list[str],  # email addresses
    location: str = ""
) -> str:
    """Create a calendar event. Requires exact ISO datetime format."""
    return f"Event created: {title} from {start_time} to {end_time} with {len(attendees)} attendees"

@tool
def send_email(
    to: list[str],      # email addresses
    subject: str,
    body: str,
    cc: list[str] = []
) -> str:
    """Send an email via email API. Requires properly formatted addresses."""
    return f"Email sent to {', '.join(to)} - Subject: {subject}"

@tool
def get_available_time_slots(
    attendees: list[str],
    date: str,  # ISO format: "2024-01-15"
    duration_minutes: int
) -> list[str]:
    """Check calendar availability for given attendees on a specific date."""
    return ["09:00", "14:00", "16:00"]

# ============================================================================
# Step 2: Create specialized sub-agents
# ============================================================================

model = init_chat_model("gpt-5.5")  # for example

calendar_agent = create_agent(
    model,
    tools=[create_calendar_event, get_available_time_slots],
    system_prompt=(
        f"Today's date is {date.today().isoformat()}. "
        "You are a calendar scheduling assistant. "
        "Parse natural language scheduling requests (e.g., 'next Tuesday at 2pm') "
        "into proper ISO datetime formats. "
        "Use get_available_time_slots to check availability when needed. "
        "If there is no suitable time slot, stop and confirm unavailability in your response. "
        "Use create_calendar_event to schedule events. "
        "Always confirm what was scheduled in your final response."
    )
)

email_agent = create_agent(
    model,
    tools=[send_email],
    system_prompt=(
        "You are an email assistant. "
        "Compose professional emails based on natural language requests. "
        "Extract recipient information and craft appropriate subject lines and body text. "
        "Use send_email to send the message. "
        "Always confirm what was sent in your final response."
    )
)

# ============================================================================
# Step 3: Wrap sub-agents as tools for the supervisor
# ============================================================================

@tool
def schedule_event(request: str) -> str:
    """Schedule calendar events using natural language.

Use this when the user wants to create, modify, or check calendar appointments.
Handles date/time parsing, availability checking, and event creation.

Input: Natural language scheduling request (e.g., 'meeting with design team
next Tuesday at 2pm')
"""
result = calendar_agent.invoke({
    "messages": [{"role": "user", "content": request}]
})
return result["messages"][-1].text

@tool
def manage_email(request: str) -> str:
    """Send emails using natural language.

Use this when the user wants to send notifications, reminders, or any email
communication. Handles recipient extraction, subject generation, and email
composition.

Input: Natural language email request (e.g., 'send them a reminder about
the meeting')
"""
result = email_agent.invoke({
    "messages": [{"role": "user", "content": request}]
})
return result["messages"][-1].text

# ============================================================================
# Step 4: Create the supervisor agent
# ============================================================================

supervisor_agent = create_agent(
    model,
    tools=[schedule_event, manage_email],
    system_prompt=(
        "You are a helpful personal assistant. "
        "You can schedule calendar events and send emails. "
        "Break down user requests into appropriate tool calls and coordinate the results. "
        "When a request involves multiple actions, use multiple tools in sequence or in parallel as appropriate."
    )
)

# ============================================================================
# Step 5: Use the supervisor
# ============================================================================

if __name__ == "__main__":
    # Example: User request requiring both calendar and email coordination
    user_request = (
        "Schedule a meeting with the design team next Tuesday at 2pm for 1 hour, "
        "and send them an email reminder about reviewing the new mockups."
    )

print("User Request:", user_request)
print("\n" + "="*80 + "\n")

    stream = supervisor_agent.stream_events(
        {"messages": [{"role": "user", "content": user_request}]},
        version="v3",
    )
    for kind, item in stream.interleave("messages", "tool_calls"):
        if kind == "messages":
            for token in item.text:
                print(token, end="", flush=True)
        elif kind == "tool_calls":
            print(f"\nTool call: {item.tool_name}({item.input})")
            print(f"Tool result: {item.output}")
```

### Understanding the architecture

Your system has three layers. The bottom layer contains rigid API tools that require exact formats. The middle layer contains sub-agents that accept natural language, translate it to structured API calls, and return natural language confirmations. The top layer contains the supervisor that routes to high-level capabilities and synthesizes results.

This separation of concerns provides several benefits: each layer has a focused responsibility, you can add new domains without affecting existing ones, and you can test and iterate on each layer independently.

## 6. Add human-in-the-loop review

It can be prudent to incorporate [human-in-the-loop review](/oss/langchain/human-in-the-loop) of sensitive actions. LangChain includes [built-in middleware](/oss/langchain/human-in-the-loop#configuring-interrupts) to review tool calls, in this case the tools invoked by sub-agents.

Let's add human-in-the-loop review to both sub-agents:
- We configure the `create_calendar_event` and `send_email` tools to interrupt, permitting all [response types](/oss/langchain/human-in-the-loop) (`approve`, `edit`, `reject`)
- We add a [checkpointer](/oss/langchain/short-term-memory) **only to the top-level agent**. This is required to pause and resume execution.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware # [!code highlight]
from langgraph.checkpoint.memory import InMemorySaver # [!code highlight]

calendar_agent = create_agent(
    model,
    tools=[create_calendar_event, get_available_time_slots],
    system_prompt=CALENDAR_AGENT_PROMPT,
    middleware=[ # [!code highlight]
        HumanInTheLoopMiddleware( # [!code highlight]
            interrupt_on={"create_calendar_event": True}, # [!code highlight]
            description_prefix="Calendar event pending approval", # [!code highlight]
        ), # [!code highlight]
    ], # [!code highlight]
)

email_agent = create_agent(
    model,
    tools=[send_email],
    system_prompt=EMAIL_AGENT_PROMPT,
    middleware=[ # [!code highlight]
        HumanInTheLoopMiddleware( # [!code highlight]
            interrupt_on={"send_email": True}, # [!code highlight]
            description_prefix="Outbound email pending approval", # [!code highlight]
        ), # [!code highlight]
    ], # [!code highlight]
)

supervisor_agent = create_agent(
    model,
    tools=[schedule_event, manage_email],
    system_prompt=SUPERVISOR_PROMPT,
    checkpointer=InMemorySaver(), # [!code highlight]
)
```

Let's repeat the query. Note that we gather interrupt events into a list to access downstream:

```python
query = (
    "Schedule a meeting with the design team next Tuesday at 2pm for 1 hour, "
    "and send them an email reminder about reviewing the new mockups."
)

config = {"configurable": {"thread_id": "6"}}

interrupts = []
stream = supervisor_agent.stream_events(
    {"messages": [{"role": "user", "content": query}]},
    config,
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
if stream.interrupted:
    for interrupt_ in stream.interrupts:
        interrupts.append(interrupt_)
        print(f"\nINTERRUPTED: {interrupt_.id}")
```

```
================================== Ai Message ==================================
Tool Calls:
  schedule_event (call_t4Wyn32ohaShpEZKuzZbl83z)
 Call ID: call_t4Wyn32ohaShpEZKuzZbl83z
  Args:
    request: Schedule a meeting with the design team next Tuesday at 2pm for 1 hour.
  manage_email (call_JWj4vDJ5VMnvkySymhCBm4IR)
 Call ID: call_JWj4vDJ5VMnvkySymhCBm4IR
  Args:
    request: Send an email reminder to the design team about reviewing the new mockups before our meeting next Tuesday at 2pm.

INTERRUPTED: 4f994c9721682a292af303ec1a46abb7

INTERRUPTED: 2b56f299be313ad8bc689eff02973f16
```
This time we've interrupted execution. Let's inspect the interrupt events:

```python
for interrupt_ in interrupts:
    for request in interrupt_.value["action_requests"]:
        print(f"INTERRUPTED: {interrupt_.id}")
        print(f"{request['description']}\n")
```

```
INTERRUPTED: 4f994c9721682a292af303ec1a46abb7
Calendar event pending approval

Tool: create_calendar_event
Args: {'title': 'Meeting with the Design Team', 'start_time': '2024-06-18T14:00:00', 'end_time': '2024-06-18T15:00:00', 'attendees': ['design team']}

INTERRUPTED: 2b56f299be313ad8bc689eff02973f16
Outbound email pending approval

Tool: send_email
Args: {'to': ['designteam@example.com'], 'subject': 'Reminder: Review New Mockups Before Meeting Next Tuesday at 2pm', 'body': "Hello Team,\n\nThis is a reminder to review the new mockups ahead of our meeting scheduled for next Tuesday at 2pm. Your feedback and insights will be valuable for our discussion and next steps.\n\nPlease ensure you've gone through the designs and are ready to share your thoughts during the meeting.\n\nThank you!\n\nBest regards,\n[Your Name]"}
```

We can specify decisions for each interrupt by referring to its ID using a `Command`. Refer to the [human-in-the-loop guide](/oss/langchain/human-in-the-loop) for additional details. For demonstration purposes, here we will accept the calendar event, but edit the subject of the outbound email:

```python
from langgraph.types import Command # [!code highlight]

resume = {}
for interrupt_ in interrupts:
    if interrupt_.id == "2b56f299be313ad8bc689eff02973f16":
        # Edit email
        edited_action = interrupt_.value["action_requests"][0].copy()
        edited_action["args"]["subject"] = "Mockups reminder"
        resume[interrupt_.id] = {
            "decisions": [{"type": "edit", "edited_action": edited_action}]
        }
    else:
        resume[interrupt_.id] = {"decisions": [{"type": "approve"}]}

interrupts = []
stream = supervisor_agent.stream_events(
    Command(resume=resume), # [!code highlight]
    config,
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
if stream.interrupted:
    for interrupt_ in stream.interrupts:
        interrupts.append(interrupt_)
        print(f"\nINTERRUPTED: {interrupt_.id}")
```

```
================================= Tool Message =================================
Name: schedule_event

Your meeting with the design team has been scheduled for next Tuesday, June 18th, from 2:00 pm to 3:00 pm.
================================= Tool Message =================================
Name: manage_email

Your email reminder to the design team has been sent. Here’s what was sent:

- Recipient: designteam@example.com
- Subject: Mockups reminder
- Body: A reminder to review the new mockups before the meeting next Tuesday at 2pm, with a request for feedback and readiness for discussion.

Let me know if you need any further assistance!
================================== Ai Message ==================================

- Your meeting with the design team has been scheduled for next Tuesday, June 18th, from 2:00 pm to 3:00 pm.
- An email reminder has been sent to the design team about reviewing the new mockups before the meeting.

Let me know if you need any further assistance!
```
The run proceeds with our input.

## 7. Advanced: Control information flow

By default, sub-agents receive only the request string from the supervisor. You might want to pass additional context, such as conversation history or user preferences.

### Pass additional conversational context to sub-agents

```python
from langchain.tools import tool, ToolRuntime

@tool
def schedule_event(
    request: str,
    runtime: ToolRuntime
) -> str:
    """Schedule calendar events using natural language."""
    # Customize context received by sub-agent
    original_user_message = next(
        message for message in runtime.state["messages"]
        if message.type == "human"
    )
    prompt = (
        "You are assisting with the following user inquiry:\n\n"
        f"{original_user_message.text}\n\n"
        "You are tasked with the following sub-request:\n\n"
        f"{request}"
    )
    result = calendar_agent.invoke({
        "messages": [{"role": "user", "content": prompt}],
    })
    return result["messages"][-1].text
```

This allows sub-agents to see the full conversation context, which can be useful for resolving ambiguities like "schedule it for the same time tomorrow" (referencing a previous conversation).

**Tip:**

You can see the full context received by the sub agent in the [chat model call](https://smith.langchain.com/public/c7d54882-afb8-4039-9c5a-4112d0f458b0/r/6803571e-af78-4c68-904a-ecf55771084d) of the LangSmith trace.

### Control what supervisor receives

You can also customize what information flows back to the supervisor:

```python
import json

@tool
def schedule_event(request: str) -> str:
    """Schedule calendar events using natural language."""
    result = calendar_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })

# Option 1: Return just the confirmation message
return result["messages"][-1].text

    # Option 2: Return structured data
    # return json.dumps({
    #     "status": "success",
    #     "event_id": "evt_123",
    #     "summary": result["messages"][-1].text
    # })
```

**Important:** Make sure sub-agent prompts emphasize that their final message should contain all relevant information. A common failure mode is sub-agents that perform tool calls but don't include the results in their final response.

## 8. Key takeaways

The supervisor pattern creates layers of abstraction where each layer has a clear responsibility. When designing a supervisor system, start with clear domain boundaries and give each sub-agent focused tools and prompts. Write clear tool descriptions for the supervisor, test each layer independently before integration, and control information flow based on your specific needs.

**Tip:**

**When to use the supervisor pattern**

Use the supervisor pattern when you have multiple distinct domains (calendar, email, CRM, database), each domain has multiple tools or complex logic, you want centralized workflow control, and sub-agents don't need to converse directly with users.

For simpler cases with just a few tools, use a single agent. When agents need to have conversations with users, use [handoffs](/oss/langchain/multi-agent/handoffs) instead. For peer-to-peer collaboration between agents, consider other multi-agent patterns.

## Next steps

Learn about [handoffs](/oss/langchain/multi-agent/handoffs) for agent-to-agent conversations, explore [context engineering](/oss/langchain/context-engineering) to fine-tune information flow, read the [multi-agent overview](/oss/langchain/multi-agent) to compare different patterns, and use [LangSmith](https://smith.langchain.com) to debug and monitor your multi-agent system.

---

# Subagents
> 출처: data/raw/langchain/multi-agent/subagents.mdx | https://docs.langchain.com/oss/python/langchain/multi-agent/subagents

In the **subagents** architecture, a central main [agent](/oss/langchain/agents) (often referred to as a **supervisor**) coordinates subagents by calling them as [tools](/oss/langchain/tools). The main agent decides which subagent to invoke, what input to provide, and how to combine results. By default, subagents are stateless—they don't remember past interactions, with all conversation memory maintained by the main agent. This provides [context](/oss/langchain/context-engineering) isolation: each subagent invocation works in a clean context window, preventing context bloat in the main conversation.

You can also pass the main agent's conversation history into a subagent when it needs that context. See [Subagent inputs](#subagent-inputs).

For built-in subagent support, see [Deep Agents](/oss/deepagents/subagents).

```mermaid
graph LR
    A[User] --> B[Main Agent]
    B --> C[Subagent A]
    B --> D[Subagent B]
    B --> E[Subagent C]
    C --> B
    D --> B
    E --> B
    B --> F[User response]

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,F trigger
    class B,C,D,E process
```

## Key characteristics

* Centralized control: All routing passes through the main agent
* No direct user interaction: Subagents return results to the main agent, not the user (though you can use [interrupts](/oss/langgraph/interrupts#pause-using-interrupt) within a subagent to allow user interaction)
* Subagents via tools: Subagents are invoked via tools
* Parallel execution: The main agent can invoke multiple subagents in a single turn

**Note:**

**Supervisor vs. Router**: A supervisor agent (this pattern) is different from a [router](/oss/langchain/multi-agent/router). The supervisor is a full agent that maintains conversation context and dynamically decides which subagents to call across multiple turns. A router is typically a single classification step that dispatches to agents without maintaining ongoing conversation state.

## When to use

Use the subagents pattern when you have multiple distinct domains (e.g., calendar, email, CRM, database), subagents don't need to converse directly with users, or you want centralized workflow control. For simpler cases with just a few [tools](/oss/langchain/tools), use a [single agent](/oss/langchain/agents).

**Tip:**

**Need user interaction within a subagent?** While subagents typically return results to the main agent rather than conversing directly with users, you can use [interrupts](/oss/langgraph/interrupts#pause-using-interrupt) within a subagent to pause execution and gather user input. This is useful when a subagent needs clarification or approval before proceeding. The main agent remains the orchestrator, but the subagent can collect information from the user mid-task.

## Basic implementation

The core mechanism wraps a subagent as a tool that the main agent can call:

```python
from langchain.tools import tool
from langchain.agents import create_agent

# Create a subagent
subagent = create_agent(model="google_genai:gemini-3.6-flash", tools=[...])

# Wrap it as a tool
@tool("research", description="Research a topic and return findings")
def call_research_agent(query: str):
    result = subagent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

# Main agent with subagent as a tool
main_agent = create_agent(model="google_genai:gemini-3.6-flash", tools=[call_research_agent])
```

- [Tutorial: Build a personal assistant with subagents](/oss/langchain/multi-agent/subagents-personal-assistant)

    Learn how to build a personal assistant using the subagents pattern, where a central main agent (supervisor) coordinates specialized worker agents.

## Design decisions

When implementing the subagents pattern, you'll make several key design choices. This table summarizes the options—each is covered in detail in the sections below.

| Decision | Options |
|----------|---------|
| [**Sync vs. async**](#sync-vs-async) | Sync (blocking) vs. async (background) |
| [**Tool patterns**](#tool-patterns) | Tool per agent vs. single dispatch tool |
| [**Subagent specs**](#subagent-specs) | System prompt vs. enum constraint vs. tool-based discovery (single dispatch tool only) |
| [**Subagent inputs**](#subagent-inputs) | Query only vs. full context |
| [**Subagent outputs**](#subagent-outputs) | Subagent result vs full conversation history |

## Sync vs. async

Subagent execution can be **synchronous** (blocking) or **asynchronous** (background). Your choice depends on whether the main agent needs the result to continue.

| Mode | Main agent behavior | Best for | Tradeoff |
|------|---------------------|----------|----------|
| **Sync** | Waits for subagent to complete | Main agent needs result to continue | Simple, but blocks the conversation |
| **Async** | Continues while subagent runs in background | Independent tasks, user shouldn't wait | Responsive, but more complex |

**Tip:**

Not to be confused with Python's `async`/`await`. Here, "async" means the main agent kicks off a background job (typically in a separate process or service) and continues without blocking.

### Synchronous (default)

By default, subagent calls are **synchronous**: the main agent waits for each subagent to complete before continuing. Use sync when the main agent's next action depends on the subagent's result.

```mermaid
sequenceDiagram
    participant User
    participant Main Agent
    participant Research Subagent

    User->>Main Agent: "What's the weather in Tokyo?"
    Main Agent->>Research Subagent: research("Tokyo weather")
    Note over Main Agent: Waiting for result...
    Research Subagent-->>Main Agent: "Currently 72°F, sunny"
    Main Agent-->>User: "It's 72°F and sunny in Tokyo"
```

**When to use sync:**
- Main agent needs the subagent's result to formulate its response
- Tasks have order dependencies (e.g., fetch data → analyze → respond)
- Subagent failures should block the main agent's response

**Tradeoffs:**
- Simple implementation—just call and wait
- User sees no response until all subagents complete
- Long-running tasks freeze the conversation

### Asynchronous

Use **asynchronous execution** when the subagent's work is independent—the main agent doesn't need the result to continue conversing with the user. The main agent kicks off a background job and remains responsive.

```mermaid
sequenceDiagram
    participant User
    participant Main Agent
    participant Job System
    participant Contract Reviewer

User->>Main Agent: "Review this M&A contract"
Main Agent->>Job System: run_agent("legal_reviewer", task)
Job System->>Contract Reviewer: Start agent
Job System-->>Main Agent: job_id: "job_123"
Main Agent-->>User: "Started review (job_123)"

Note over Contract Reviewer: Reviewing 150+ pages...

User->>Main Agent: "What's the status?"
Main Agent->>Job System: check_status(job_id)
Job System-->>Main Agent: "running"
Main Agent-->>User: "Still reviewing contract..."

Note over Contract Reviewer: Review completes

    User->>Main Agent: "Is it done yet?"
    Main Agent->>Job System: check_status(job_id)
    Job System-->>Main Agent: "completed"
    Main Agent->>Job System: get_result(job_id)
    Job System-->>Main Agent: Contract analysis
    Main Agent-->>User: "Review complete: [findings]"
```

**When to use async:**
- Subagent work is independent of the main conversation flow
- Users should be able to continue chatting while work happens
- You want to run multiple independent tasks in parallel

**Three-tool pattern:**
1. **Start job**: Kicks off the background task, returns a job ID
2. **Check status**: Returns current state (pending, running, completed, failed)
3. **Get result**: Retrieves the completed result

**Handling job completion:** When a job finishes, your application needs to notify the user. One approach: surface a notification that, when clicked, sends a `HumanMessage` like "Check job_123 and summarize the results."

## Tool patterns

There are two main ways to expose subagents as tools:

| Pattern | Best for | Trade-off |
|---------|----------|-----------|
| [**Tool per agent**](#tool-per-agent) | Fine-grained control over each subagent's input/output | More setup, but more customization |
| [**Single dispatch tool**](#single-dispatch-tool) | Many agents, distributed teams, convention over configuration | Simpler composition, less per-agent customization |

### Tool per agent

```mermaid
graph LR
    A[User] --> B[Main Agent]
    B --> C[Subagent A]
    B --> D[Subagent B]
    B --> E[Subagent C]
    C --> B
    D --> B
    E --> B
    B --> F[User response]

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,F trigger
    class B,C,D,E process
```

The key idea is wrapping subagents as tools that the main agent can call:

```python
from langchain.tools import tool
from langchain.agents import create_agent

# Create a sub-agent
subagent = create_agent(model="...", tools=[...])  # [!code highlight]

# Wrap it as a tool  # [!code highlight]
@tool("subagent_name", description="subagent_description")  # [!code highlight]
def call_subagent(query: str):  # [!code highlight]
    result = subagent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

# Main agent with subagent as a tool  # [!code highlight]
main_agent = create_agent(model="...", tools=[call_subagent])  # [!code highlight]
```

The main agent invokes the subagent tool when it decides the task matches the subagent's description, receives the result, and continues orchestration. See [Context engineering](#context-engineering) for fine-grained control.

### Single dispatch tool

An alternative approach uses a single parameterized tool to invoke ephemeral sub-agents for independent tasks. Unlike the [tool per agent](#tool-per-agent) approach where each sub-agent is wrapped as a separate tool, this uses a convention-based approach with a single `task` tool: the task description is passed as a human message to the sub-agent, and the sub-agent's final message is returned as the tool result.

Use this approach when you want to distribute agent development across multiple teams, need to isolate complex tasks into separate context windows, need a scalable way to add new agents without modifying the coordinator, or prefer convention over customization. This approach trades flexibility in context engineering for simplicity in agent composition and strong context isolation.

```mermaid
graph LR
    A[User] --> B[Main Agent]
    B --> C{task<br/>agent_name, description}
    C -->|research| D[Research Agent]
    C -->|writer| E[Writer Agent]
    C -->|reviewer| F[Reviewer Agent]
    D --> C
    E --> C
    F --> C
    C --> B
    B --> G[User response]

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
classDef decision fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F

    class A,G trigger
    class B,D,E,F process
    class C decision
```

**Key characteristics:**

* Single task tool: One parameterized tool that can invoke any registered sub-agent by name
* Convention-based invocation: Agent selected by name, task passed as human message, final message returned as tool result
* Team distribution: Different teams can develop and deploy agents independently
* Agent discovery: Sub-agents can be discovered via system prompt (listing available agents) or through [progressive disclosure](/oss/langchain/multi-agent/skills-sql-assistant) (loading agent information on-demand via tools)

**Tip:**

An interesting aspect of this approach is that sub-agents may have the exact same capabilities as the main agent. In such cases, invoking a sub-agent is **really about context isolation** as the primary reason—allowing complex, multi-step tasks to run in isolated context windows without bloating the main agent's conversation history. The sub-agent completes its work autonomously and returns only a concise summary, keeping the main thread focused and efficient.

**Agent registry with task dispatcher**

```python
from langchain.tools import tool
from langchain.agents import create_agent

# Sub-agents developed by different teams
research_agent = create_agent(
    model="gpt-5.5",
    prompt="You are a research specialist..."
)

writer_agent = create_agent(
    model="gpt-5.5",
    prompt="You are a writing specialist..."
)

# Registry of available sub-agents
SUBAGENTS = {
    "research": research_agent,
    "writer": writer_agent,
}

@tool
def task(
    agent_name: str,
    description: str
) -> str:
    """Launch an ephemeral subagent for a task.

Available agents:
- research: Research and fact-finding
- writer: Content creation and editing
"""
agent = SUBAGENTS[agent_name]
result = agent.invoke({
    "messages": [
        {"role": "user", "content": description}
    ]
})
return result["messages"][-1].content

# Main coordinator agent
main_agent = create_agent(
    model="gpt-5.5",
    tools=[task],
    system_prompt=(
        "You coordinate specialized sub-agents. "
        "Available: research (fact-finding), "
        "writer (content creation). "
        "Use the task tool to delegate work."
    ),
)
```

## Context engineering

Control how context flows between the main agent and its subagents:

| Category | Purpose | Impacts |
|----------|---------|---------|
| [**Subagent specs**](#subagent-specs) | Ensure subagents are invoked when they should be | Main agent routing decisions |
| [**Subagent inputs**](#subagent-inputs) | Ensure subagents can execute well with optimized context | Subagent performance |
| [**Subagent outputs**](#subagent-outputs) | Ensure the supervisor can act on subagent results | Main agent performance |

See also our comprehensive guide on [context engineering](/oss/langchain/context-engineering) for agents.

### Subagent specs

The **names** and **descriptions** associated with subagents are the primary way the main agent knows which subagents to invoke. These are prompting levers—choose them carefully.

* **Name**: How the main agent refers to the sub-agent. Keep it clear and action-oriented (e.g., `research_agent`, `code_reviewer`).
* **Description**: What the main agent knows about the sub-agent's capabilities. Be specific about what tasks it handles and when to use it.

For the [single dispatch tool](#single-dispatch-tool) design, you must additionally provide the main agent with information about the subagents it can invoke.
You can provide this information in different ways based on the number of agents and whether your registry is static or dynamic:

| Method | Best for | Tradeoff |
|--------|----------|----------|
| **System prompt enumeration** | Small, static agent lists (< 10 agents) | Simple, but requires prompt updates when agents change |
| **Enum constraint** | Small, static agent lists (< 10 agents) | Type-safe and explicit, but requires code changes when agents change |
| **Tool-based discovery** | Large or dynamic agent registries | Flexible and scalable, but adds complexity |

#### System prompt enumeration

List available agents directly in the main agent's system prompt. The main agent sees the list of agents and their descriptions as part of its instructions.

**When to use:**
- You have a small, fixed set of agents (< 10)
- Agent registry rarely changes
- You want the simplest implementation

**Example:**
```python
main_agent = create_agent(
    model="...",
    tools=[task],
    system_prompt=(
        "You coordinate specialized sub-agents. "
        "Available agents:\n"
        "- research: Research and fact-finding\n"
        "- writer: Content creation and editing\n"
        "- reviewer: Code and document review\n"
        "Use the task tool to delegate work."
    ),
)
```

#### Enum constraint on dispatch tool

Add an enum constraint to the `agent_name` parameter in your dispatch tool. This provides type safety and makes available agents explicit in the tool schema.

**When to use:**
- You have a small, fixed set of agents (< 10)
- You want type safety and explicit agent names
- You prefer schema-based validation over prompt-based guidance

**Example:**
```python
from enum import Enum

class AgentName(str, Enum):
    RESEARCH = "research"
    WRITER = "writer"
    REVIEWER = "reviewer"

@tool
def task(
    agent_name: AgentName,  # Enum constraint
    description: str
) -> str:
    """Launch an ephemeral subagent for a task."""
    # ...
```

#### Tool-based discovery

Provide a separate tool (e.g., `list_agents` or `search_agents`) that the main agent can call to discover available agents on-demand. This enables progressive disclosure and supports dynamic registries.

**When to use:**
- You have many agents (> 10) or a growing registry
- Agent registry changes frequently or is dynamic
- You want to reduce prompt size and token usage
- Different teams manage different agents independently

**Example:**
```python
@tool
def list_agents(query: str = "") -> str:
    """List available subagents, optionally filtered by query."""
    agents = search_agent_registry(query)
    return format_agent_list(agents)

@tool
def task(agent_name: str, description: str) -> str:
    """Launch an ephemeral subagent for a task."""
    # ...

main_agent = create_agent(
    model="...",
    tools=[task, list_agents],
    system_prompt="Use list_agents to discover available subagents, then use task to invoke them."
)
```

### Subagent inputs

Customize what context the subagent receives to execute its task. Add input that isn't practical to capture in a static prompt—full message history, prior results, or task metadata—by pulling from the agent's state.

```python Subagent inputs example expandable
from langchain.agents import AgentState
from langchain.tools import tool, ToolRuntime

class CustomState(AgentState):
    example_state_key: str

@tool(
    "subagent1_name",
    description="subagent1_description"
)
def call_subagent1(query: str, runtime: ToolRuntime[None, CustomState]):
    # Apply any logic needed to transform the messages into a suitable input
    subagent_input = some_logic(query, runtime.state["messages"])
    result = subagent1.invoke({
        "messages": subagent_input,
        # You could also pass other state keys here as needed.
        # Make sure to define these in both the main and subagent's
        # state schemas.
        "example_state_key": runtime.state["example_state_key"]
    })
    return result["messages"][-1].content
```

`some_logic` controls how much context the subagent receives. Passing only the task description (`query`) keeps the subagent isolated. Passing the parent's message history (`runtime.state["messages"]`) instead seeds the subagent with prior work, which helps when it needs to continue something the parent already started, like resuming a PR review or picking up a bug fix.

[Deep Agents](/oss/deepagents/subagents#forked-subagents) names these patterns `mode: "isolated"` (default) and `mode: "fork"`, and implements forking for you: a forked subagent receives the parent's full message history (including tool calls) and system prompt.

| Mode | Subagent receives | Best for | Tradeoff |
|------|-------------------|----------|----------|
| **Isolated** (default) | Only the task description | Focused work that needs little prior context | Context isolation, but re-derives everything the parent already did |
| **Forked** | The parent's conversation history (and, in Deep Agents, the system prompt) | Continuing a task the parent already started | Seeded with prior context, at the cost of a larger prompt and less isolation |

### Subagent outputs

Customize what the main agent receives back so it can make good decisions. Two strategies:

1. **Prompt the sub-agent**: Specify exactly what should be returned. A common failure mode is that the sub-agent performs tool calls or reasoning but doesn't include results in its final message—remind it that the supervisor only sees the final output.
2. **Format in code**: Adjust or enrich the response before returning it. For example, pass specific state keys back in addition to the final text using a [`Command`](/oss/langgraph/graph-api#command).

```python Subagent outputs example expandable
from typing import Annotated
from langchain.agents import AgentState
from langchain.tools import InjectedToolCallId
from langgraph.types import Command

@tool(
    "subagent1_name",
    description="subagent1_description"
)
def call_subagent1(
    query: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    result = subagent1.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return Command(update={
        # Pass back additional state from the subagent
        "example_state_key": result["example_state_key"],
        "messages": [
            ToolMessage(
                content=result["messages"][-1].content,
                tool_call_id=tool_call_id
            )
        ]
    })
```

## Checkpointing and state inspection

By default, subagents use the **inherited checkpointer** mode—each invocation starts with fresh state, supports [interrupts](/oss/langgraph/interrupts#pause-using-interrupt), and runs safely in parallel. If you need a subagent to maintain its own persistent conversation history across invocations, compile it with `checkpointer=True` (continuations mode). See [subgraph persistence](/oss/langgraph/use-subgraphs#subgraph-persistence) for a full comparison of modes.

Because subagents are called inside tool functions, LangGraph cannot [statically discover](/oss/langgraph/use-subgraphs#view-subgraph-state) them. This means [`get_state` with `subgraphs`](/oss/langgraph/use-subgraphs#view-subgraph-state) will not return subagent state. If you need to read nested graph state (e.g., during an [interrupt](/oss/langgraph/interrupts#pause-using-interrupt)), invoke the subagent from a [node function](/oss/langgraph/use-subgraphs#call-a-subgraph-inside-a-node) in a custom graph instead. See [subgraph persistence](/oss/langgraph/use-subgraphs#subgraph-persistence) for details on how each mode affects state visibility.

- [Migrate from langgraph-supervisor](/oss/migrate/langgraph-supervisor)

    The langgraph-supervisor package is no longer actively maintained. Learn how to migrate from create_supervisor to the subagents pattern, including interrupt and resume flows with external API callbacks.

---

# LangSmith Observability
> 출처: data/raw/langchain/observability.mdx | https://docs.langchain.com/oss/python/langchain/observability

As you build and run agents with LangChain, you need visibility into how they behave: which [tools](/oss/langchain/tools) they call, what prompts they generate, and how they make decisions. LangChain agents built with `create_agent` automatically support tracing through [LangSmith](/langsmith/observability), a platform for capturing, debugging, evaluating, and monitoring LLM application behavior.

[_Traces_](/langsmith/observability-concepts#traces) record every step of your agent's execution, from the initial user input to the final response, including all tool calls, model interactions, and decision points. This execution data helps you debug issues, evaluate performance across different inputs, and monitor usage patterns in production.

This guide shows you how to enable tracing for your LangChain agents and use LangSmith to analyze their execution.

## Prerequisites

Before you begin, ensure you have the following:

- **A LangSmith account**: Sign up (for free) or log in at [smith.langchain.com](https://smith.langchain.com).
- **A LangSmith API key**: Follow the [Create an API key](/langsmith/create-account-api-key) guide.

## Enable tracing

All LangChain agents automatically support LangSmith tracing. To enable it, set the following environment variables:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
```

## Quickstart

No extra code is needed to log a trace to LangSmith. Just run your agent code as you normally would:

```python
from langchain.agents import create_agent

def send_email(to: str, subject: str, body: str):
    """Send an email to a recipient."""
    # ... email sending logic
    return f"Email sent to {to}"

def search_web(query: str):
    """Search the web for information."""
    # ... web search logic
    return f"Search results for: {query}"

agent = create_agent(
    model="gpt-5.5",
    tools=[send_email, search_web],
    system_prompt="You are a helpful assistant that can send emails and search the web."
)

# Run the agent - all steps will be traced automatically
response = agent.invoke({
    "messages": [{"role": "user", "content": "Search for the latest AI news and email a summary to john@example.com"}]
})
```

By default, the trace will be logged to the project with the name `default`. To configure a custom project name, see [Log to a project](/langsmith/log-traces-to-project).

## Trace selectively

You may opt to trace specific invocations or parts of your application using LangSmith's `tracing_context` context manager:

```python
import langsmith as ls

# This WILL be traced
with ls.tracing_context(enabled=True):
    agent.invoke({"messages": [{"role": "user", "content": "Send a test email to alice@example.com"}]})

# This will NOT be traced (if LANGSMITH_TRACING is not set)
agent.invoke({"messages": [{"role": "user", "content": "Send another email"}]})
```

## Log to a project

**Statically**

You can set a custom project name for your entire application by setting the `LANGSMITH_PROJECT` environment variable:

```bash
export LANGSMITH_PROJECT=my-agent-project
```

**Dynamically**

You can set the project name programmatically for specific operations:

```python
import langsmith as ls

with ls.tracing_context(project_name="email-agent-test", enabled=True):
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Send a welcome email"}]
    })
```

## Add metadata to traces

You can annotate your traces with custom metadata and tags:

```python
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Send a welcome email"}]},
    config={
        "tags": ["production", "email-assistant", "v1.0"],
        "metadata": {
            "user_id": "user_123",
            "session_id": "session_456",
            "environment": "production"
        }
    }
)
```

`tracing_context` also accepts tags and metadata for fine-grained control:

```python
with ls.tracing_context(
    project_name="email-agent-test",
    enabled=True,
    tags=["production", "email-assistant", "v1.0"],
    metadata={"user_id": "user_123", "session_id": "session_456", "environment": "production"}):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Send a welcome email"}]}
    )
```

This custom metadata and tags will be attached to the trace in LangSmith.

**Tip:**

To learn more about how to use traces to debug, evaluate, and monitor your agents, see the [LangSmith documentation](/langsmith/observability).

---

# LangChain overview
> 출처: data/raw/langchain/overview.mdx | https://docs.langchain.com/oss/python/langchain/overview

LangChain provides create_agent: a minimal, highly configurable agent harness. Compose exactly the agent your use case needs from model, tools, prompt, and middleware.

**Agent = Model + Harness.** LangChain provides `create_agent`: a minimal, highly configurable harness. The harness is everything around the model loop: the prompt, the tools, and any middleware that shapes behavior. Start with the primitives and compose exactly what your use case needs. Supports [OpenAI, Anthropic, Google, and more](/oss/integrations/providers/overview).

**Tip:**

**LangChain vs. LangGraph vs. Deep Agents**

Start with [Deep Agents](/oss/deepagents/overview/) for a "batteries-included" agent with features like automatic context compression, a virtual filesystem, and subagent-spawning. Deep Agents are built on LangChain [agents](/oss/langchain/agents/) which you can also use directly.

Use [LangChain](/oss/langchain/agents) (`create_agent`) for a highly customizable harness, easily tailored to your use case and data.

Use [LangGraph](/oss/langgraph/overview), our low-level orchestration framework, for advanced needs combining deterministic and agentic workflows.

Use [LangSmith](/langsmith/observability) to trace, debug, and evaluate agents built with any of these frameworks. Follow the [tracing quickstart](/langsmith/trace-with-langchain) to get set up. We recommend you also set up [LangSmith Engine](/langsmith/engine) which monitors your traces, detects issues, and proposes fixes.

## 

Create an agent

This example demonstrates how to create a simple LangChain agent with a custom tool:

```python OpenAI
# pip install -qU langchain "langchain[openai]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Google Gemini
# pip install -qU langchain "langchain[google-genai]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Claude (Anthropic)
# pip install -qU langchain "langchain[anthropic]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python OpenRouter
# pip install -qU langchain langchain-openrouter
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openrouter:anthropic/claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Fireworks
# pip install -qU langchain langchain-fireworks
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="fireworks:accounts/fireworks/models/qwen3p5-397b-a17b",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Baseten
# pip install -qU langchain langchain-baseten
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Ollama
# pip install -qU langchain langchain-ollama
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="ollama:devstral-2",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Azure
# pip install -qU langchain "langchain[openai]"
import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

model = init_chat_model(
    "azure_openai:gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python AWS Bedrock
# pip install -qU langchain langchain-aws
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# US cross-region inference profile; use global.anthropic.claude-sonnet-4-6 for worldwide routing.
agent = create_agent(
    model="bedrock_converse:us.anthropic.claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python HuggingFace
# pip install -qU langchain "langchain[huggingface]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="huggingface:microsoft/Phi-3-mini-4k-instruct",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

See the [Installation instructions](/oss/langchain/install) and [Quickstart guide](/oss/langchain/quickstart) to get started building your own agents and applications with LangChain.

**Tip:**

Use [LangSmith](/langsmith/observability) to trace requests, debug agent behavior, and evaluate outputs. Set `LANGSMITH_TRACING=true` and your API key to get started.

## 

Core benefits

- [Standard model interface](/oss/langchain/models)

        Use one interface for chat models, embeddings, and more across providers. Switch models with minimal code changes and keep your application portable as requirements evolve.

- [Highly configurable harness](/oss/langchain/agents)

        Start with `create_agent` as a minimal harness and add capabilities incrementally through middleware. Compose only what your use case needs, from guardrails and retries to routing and custom tool policies.

- [Built on top of LangGraph](/oss/langgraph/overview)

        LangChain's agents are built on top of LangGraph. This allows us to take advantage of LangGraph's durable execution, human-in-the-loop support, persistence, and more.

- [Debug with LangSmith](/langsmith/observability)

        Inspect traces, tool calls, state transitions, and latency in one place. Find failure modes, evaluate quality, and improve agent behavior with execution data.

---

# Philosophy
> 출처: data/raw/langchain/philosophy.mdx | https://docs.langchain.com/oss/python/langchain/philosophy

LangChain exists to be the easiest place to start building with LLMs, while also being flexible and production-ready.

LangChain is driven by a few core beliefs:

- Large Language Models (LLMs) are great, powerful new technology.

- LLMs are even better when you combine them with external sources of data.

- LLMs will transform what the applications of the future look like. Specifically, the applications of the future will look more and more agentic.

- It is still very early on in that transformation.

- While it's easy to build a prototype of those agentic applications, it's still really hard to build agents that are reliable enough to put into production.

Today developers can choose how they build agents: use [LangChain](/oss/langchain/overview) for maximum flexibility and control, or [Deep Agents](/oss/langchain/overview) which allows for similar flexibility and control but comes with opinionated built-in planning, filesystem tools, subagents, and context management. Both are built on [LangGraph](/oss/langgraph/overview).

With LangChain, we have two core focuses:

**We want to enable developers to build with the best models.**

Different providers expose different APIs, with different model parameters and different message formats.

Standardizing these model inputs and outputs is a core focus, making it easy for developer to easily change to the most recent state-of-the-art model, avoiding lock-in.

**We want to make it easy to use models to orchestrate more complex flows that interact with other data and computation.**

Models should be used for more than just *text generation* - they should also be used to orchestrate more complex flows that interact with other data. LangChain makes it easy to define [tools](/oss/langchain/tools) that LLMs can use dynamically, as well as help with parsing of and access to unstructured data.

## History

Given the constant rate of change in the field, LangChain has also evolved over time. Below is a brief timeline of how LangChain has changed over the years, evolving alongside what it means to build with LLMs:

**2022-10-24**

A month before ChatGPT, **LangChain was launched as a Python package**. It consisted of two main components:

- LLM abstractions

    - "Chains", or predetermined steps of computation to run, for common use cases. For example - RAG: run a retrieval step, then run a generation step.

    The name LangChain comes from "Language" (like Language models) and "Chains".

**2022-12**

The first general purpose agents were added to LangChain.

These general purpose agents were based on the [ReAct paper](https://arxiv.org/abs/2210.03629) (ReAct standing for Reasoning and Acting). They used LLMs to generate JSON that represented tool calls, and then parsed that JSON to determine what tools to call.

**2023-01**

OpenAI releases a 'Chat Completion' API.

Previously, models took in strings and returned a string. In the ChatCompletions API, they evolved to take in a list of messages and return a message. Other model providers followed suit, and LangChain updated to work with lists of messages.

**2023-01**

LangChain releases a JavaScript version.

LLMs and agents will change how applications are built and JavaScript is the language of application developers.

**2023-02**

**LangChain Inc. was formed as a company** around the open source LangChain project.

The main goal was to "make intelligent agents ubiquitous". The team recognized that while LangChain was a key part (LangChain made it simple to get started with LLMs), there was also a need for other components.

**2023-03**

OpenAI releases 'function calling' in their API.

This allowed the API to explicitly generate payloads that represented tool calls. Other model providers followed suit, and LangChain was updated to use this as the preferred method for tool calling (rather than parsing JSON).

**2023-06**

**LangSmith is released** as closed source platform by LangChain Inc., providing observability and evals.

The main issue with building agents is getting them to be reliable, and LangSmith, which provides observability and evals, was built to solve that need. LangChain was updated to integrate seamlessly with LangSmith.

**2024-01**

**LangChain releases 0.1.0**, its first non-0.0.x.

The industry matured from prototypes to production, and as such, LangChain increased its focus on stability.

**2024-02**

**LangGraph is released** as an open-source library.

The original LangChain had two focuses: LLM abstractions, and high-level interfaces for getting started with common applications; however, it was missing a low-level orchestration layer that allowed developers to control the exact flow of their agent. Enter: LangGraph.

When building LangGraph, we learned from lessons when building LangChain and added functionality we discovered was needed: streaming, durable execution, short-term memory, human-in-the-loop, and more.

**2024-06**

**LangChain has over 700 integrations.**

Integrations were split out of the core LangChain package, and either moved into their own standalone packages (for the core integrations) or `langchain-community`.

**2024-10**

LangGraph becomes the preferred way to build any AI application that is more than a single LLM call.

As developers tried to improve the reliability of their applications, they needed more control than the high-level interfaces provided. LangGraph provided that low-level flexibility. Most chains and agents were marked as deprecated in LangChain with guides on how to migrate them to LangGraph. There is still one high-level abstraction created in LangGraph: an agent abstraction. It is built on top of low-level LangGraph and has the same interface as the ReAct agents from LangChain.

**2025-04**

Model APIs become more multimodal.

Models started to accept files, images, videos, and more. We updated the `langchain-core` message format accordingly to allow developers to specify these multimodal inputs in a standard way.

**2025-10-20**

**LangChain releases 1.0** with two major changes:

1. Complete revamp of all chains and agents in `langchain`. All chains and agents are now replaced with only one high level abstraction: an agent abstraction built on top of LangGraph. This was the high-level abstraction that was originally created in LangGraph, but just moved to LangChain.

        For users still using old LangChain chains/agents who do NOT want to upgrade (note: we recommend you do), you can continue using old LangChain by installing the `langchain-classic` package.

2. A standard message content format: Model APIs evolved from returning messages with a simple content string to more complex output types - reasoning blocks, citations, server-side tool calls, etc. LangChain evolved its message formats to standardize these across providers.

**2026-03-15**

**Deep Agents is released** as an open-source agent harness built on LangGraph.

While LangChain provides flexible building blocks for custom agent architectures, [Deep Agents](/oss/langchain/overview) offers a batteries-included option for complex, long-running tasks like research and coding. It adds built-in planning tools, a virtual filesystem with pluggable backends (in-memory, disk, LangGraph store, sandboxes), and subagent spawning for context isolation. Use Deep Agents for more autonomous agents with predefined tools; use LangChain for full control over your agent architecture.

---

# Quickstart
> 출처: data/raw/langchain/quickstart.mdx | https://docs.langchain.com/oss/python/langchain/quickstart

Build your first agent in minutes

This quickstart shows you how to create a fully functional AI agent in just a few minutes.

Build a basic LangChain agent in this working directory by following the LangChain quickstart.

## Step 1: Read the guide

Detect whether this project uses Python or TypeScript/JavaScript. Fetch and follow the matching page; treat it as the source of truth for package names, model strings, and code:

- Python: https://docs.langchain.com/oss/python/langchain/quickstart.md
- TypeScript: https://docs.langchain.com/oss/javascript/langchain/quickstart.md

## Step 2: Install dependencies

Install the packages from the guide with the package manager already used in this project (`uv`, `pip`, `npm`, `pnpm`, `yarn`, or `bun`). Prefer pinning current stable versions over a floating `latest` tag when the project already pins versions.

## Step 3: Configure model credentials

Check whether a supported provider API key is already set (for example `OPENAI_API_KEY`, `GOOGLE_API_KEY`, or `ANTHROPIC_API_KEY`). If none is set, ask the user which provider to use, then stop and wait while they create a key and set it in the shell or a `.env` file. Do not invent, hardcode, or commit API keys.

## Step 4: Implement the basic agent

Create the "Build a basic agent" example from the guide: `create_agent`, a simple tool such as `get_weather`, a short system prompt, and an `invoke` call. Use a model string for the provider the user chose. Print the final message content (Python: `.content_blocks`) so the user can verify the run.

## Step 5: Optional LangSmith tracing

Ask the user if they want tracing. If yes, ask them to set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY` themselves, then re-run. Do not invent a LangSmith key.

## Rules

- Stay scoped to this quickstart. Do not add unrelated frameworks, evals, or production deployment.
- Prefer `create_agent` from `langchain.agents` / `langchain` as shown in the guide.
- Ask rather than guess when a secret, provider choice, or project convention is unclear.

**Tip:**

**Using an AI coding assistant?**

- Install the [LangChain Docs MCP servers](/use-these-docs) to give your agent access to up-to-date LangChain documentation and examples.

Connect both LangChain documentation MCP servers to my coding agent so it can look up current LangChain, LangGraph, and LangSmith docs and API reference.

Servers to add:

- `docs-langchain`: https://docs.langchain.com/mcp
- `reference-langchain`: https://reference.langchain.com/mcp

Detect which agent or editor I am using (Claude Code, Cursor, Codex CLI, Claude Desktop, Deep Agents Code, VS Code, Antigravity, or another MCP-compatible client). Use the matching setup from https://docs.langchain.com/use-these-docs.md:

- Claude Code: `claude mcp add --transport http` for each server (project scope by default; use `--scope user` only if I ask for global access).
- Codex CLI: `codex mcp add` with each server URL.
- Cursor, Deep Agents Code, VS Code, or Antigravity: merge both entries into the MCP settings JSON using the field names shown on that page for my client.
- Claude Desktop: add both URLs under Settings > Connectors.

Do not invent alternate MCP URLs. After configuring, confirm both servers are listed and reachable.

- Install [LangChain Skills](https://github.com/langchain-ai/langchain-skills) to improve your agent's performance on LangChain ecosystem tasks.

Install LangChain Skills for my coding agent so it can perform better on LangChain, LangGraph, and Deep Agents tasks.

Use the Agent Skills installer from https://github.com/langchain-ai/langchain-skills:

```bash
npx skills add langchain-ai/langchain-skills --skill '*' --yes
```

If I ask for a global install instead, use:

```bash
npx skills add langchain-ai/langchain-skills --skill '*' --yes --global
```

Detect which agent or editor I am using. If I use Claude Code and prefer the plugin path, follow the marketplace install from that repository README (`/plugin marketplace add` then `/plugin install`). Do not invent alternate skill package names or install URLs. After installing, confirm the skills are available to the agent.

## Install dependencies

Install the following packages to follow along:

```bash uv
uv python pin 3.11
uv init
uv add langchain
uv sync
```

```bash pip
# Install Python 3.11+ separately if needed.
pip install -U langchain
```

```bash venv
# Install Python 3.11+ separately if needed.
python3.11 -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -U langchain
```

## Set up API keys

Get an API key from [any supported model provider](/oss/integrations/providers/overview) (for example, Google Gemini or OpenAI).

Set the API keys in your shell or in a `.env` file, for example:

**OpenAI**

```bash Shell
export OPENAI_API_KEY="your-api-key"
```

```bash .env
OPENAI_API_KEY=your-api-key
```

**Google Gemini**

```bash Shell
export GOOGLE_API_KEY="your-api-key"
```

```bash .env
GOOGLE_API_KEY=your-api-key
```

**Claude (Anthropic)**

```bash Shell
export ANTHROPIC_API_KEY="your-api-key"
```

```bash .env
ANTHROPIC_API_KEY=your-api-key
```

**OpenRouter**

```bash Shell
export OPENROUTER_API_KEY="your-api-key"
```

```bash .env
OPENROUTER_API_KEY=your-api-key
```

**Fireworks**

```bash Shell
export FIREWORKS_API_KEY="your-api-key"
```

```bash .env
FIREWORKS_API_KEY=your-api-key
```

**Baseten**

```bash Shell
export BASETEN_API_KEY="your-api-key"
```

```bash .env
BASETEN_API_KEY=your-api-key
```

**Ollama**

```bash Shell
# Local: Ollama must be running (https://ollama.com)
# Cloud: Set your Ollama API key for hosted inference
export OLLAMA_API_KEY="your-api-key"
```

```bash .env
# Local: Ollama must be running (https://ollama.com)
# Cloud: Set your Ollama API key for hosted inference
OLLAMA_API_KEY=your-api-key
```

**Azure**

```bash Shell
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment"
```

```bash .env
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
```

**AWS Bedrock**

```bash Shell
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

```bash .env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
```

**HuggingFace**

```bash Shell
export HUGGINGFACEHUB_API_TOKEN="hf_..."
```

```bash .env
HUGGINGFACEHUB_API_TOKEN=hf_...
```

**Other**

See the full list of supported [chat model integrations](/oss/integrations/chat).

To load a `.env` file, use [`python-dotenv`](https://pypi.org/project/python-dotenv/) (`load_dotenv()`).

**Tip:**

**Using LangSmith Gateway**

The [LangSmith Gateway](/langsmith/llm-gateway) routes most major providers through LangSmith. You can [bring your own provider keys](/langsmith/llm-gateway-quickstart#send-a-request), or use [Gateway Credits](/langsmith/llm-gateway-credits) to access models without a provider key.

## Build a basic agent

Start by creating a simple agent that can answer questions and call tools. The agent in this example uses the chosen language model, a basic weather function as a tool, and a simple prompt to guide its behavior:

```python OpenAI
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Google Gemini
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Claude (Anthropic)
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python OpenRouter
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openrouter:anthropic/claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Fireworks
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="fireworks:accounts/fireworks/models/qwen3p5-397b-a17b",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Baseten
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Ollama
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="ollama:devstral-2",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python Azure
import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

model = init_chat_model(
    "azure_openai:gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python AWS Bedrock
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="bedrock_converse:us.anthropic.claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```
```python HuggingFace
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="huggingface:microsoft/Phi-3-mini-4k-instruct",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

When you run the code and prompt the agent to tell you about the weather in San Francisco, the agent uses that input and its available context.
The agent understands that you are asking about the weather for the city San Francisco and therefore calls the weather tool with the provided city name.

**Tip:**

You can use [any supported model](/oss/integrations/providers/overview) by changing the model name and setting up the appropriate API key. Trace what is happening inside your agent with [LangSmith](https://smith.langchain.com). Follow the [tracing quickstart](/langsmith/trace-with-langchain) to get set up.

We recommend you also set up [LangSmith Engine](/langsmith/engine) which monitors your traces, detects issues, and proposes fixes.

## Build a real-world agent

In the following example you will build a research agent that can answer questions about text files.
Along the way you will explore the following concepts:

1. **Detailed system prompts** for better agent behavior
1. **Create tools** that integrate with external data
1. **Model configuration** for consistent responses
1. **Conversational memory** for chat-like interactions
1. **Deep Agents** for built-in features
1. **Testing** your agent

**Define the system prompt**

The system prompt defines your agent’s role and behavior. Keep it specific and actionable:

```python wrap
SYSTEM_PROMPT = """You are a literary data assistant.

## Capabilities

- `fetch_text_from_url`: loads document text from a URL into the conversation.
Do not guess line counts or positions—ground them in tool results from the saved file."""
```

**Create tools**

[Tools](/oss/langchain/tools) let a model interact with external systems by calling functions you define.
Tools can depend on [runtime context](/oss/langchain/runtime) and also interact with [agent memory](/oss/langchain/short-term-memory).

This example uses a tool to load a document from a given URL:

```python
import urllib.error
import urllib.request

from langchain.tools import tool

@tool
def fetch_text_from_url(url: str) -> str:
    """Fetch the document from a URL.
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; quickstart-research/1.0)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except urllib.error.URLError as e:
        return f"Fetch failed: {e}"
    text = raw.decode("utf-8", errors="replace")
    return text
```

**Tip:**

Tools should be well-documented: their name, description, and argument names become part of the model's prompt.
LangChain's `@tool` decorator adds metadata and enables runtime injection with the `ToolRuntime` parameter.
Learn more in the [tools guide](/oss/langchain/tools).

**Configure your model**

Set up your [language model](/oss/langchain/models) with the right parameters for your use case. For example:

```python OpenAI
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "openai:gpt-5.5",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```
```python Google Gemini
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "gemini-3.1-pro-preview",
    model_provider="google-genai",
    temperature=0.5,
    timeout=600,
    max_tokens=25000,
    streaming=True,
)
```
```python Claude (Anthropic)
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "claude-sonnet-4-6",
    temperature=0.5,
    timeout=600,
    max_tokens=25000,
    streaming=True,
)
```
```python OpenRouter
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "openrouter:anthropic/claude-sonnet-4-6",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```
```python Fireworks
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "fireworks:accounts/fireworks/models/qwen3p5-397b-a17b",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```
```python Baseten
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "baseten:zai-org/GLM-5.2",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```
```python Ollama
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "ollama:devstral-2",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```
```python Azure
import os
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "azure_openai:gpt-5.5",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
```
```python AWS Bedrock
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "us.anthropic.claude-sonnet-4-6",
    model_provider="bedrock_converse",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```
```python HuggingFace
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "microsoft/Phi-3-mini-4k-instruct",
    model_provider="huggingface",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```

Depending on the model and provider chosen, initialization parameters may vary; refer to their reference pages for details.

**Add memory**

Add [memory](/oss/langchain/short-term-memory) to your agent to maintain state across interactions. This allows
the agent to remember previous conversations and context.

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
```

**Info:**

In production, use a persistent checkpointer that saves message history to a database.
See [Add and manage memory](/oss/langgraph/add-memory#manage-short-term-memory) for more details.

**Create and run the agent**

Now assemble your agent with all the components and run it.

There are two different frameworks for creating agents: LangChain agents and deep agents.
Both LangChain and deep agents provide you with fine-grained control over tools, memory, and more.
The main difference between both is that deep agents come with a range of commonly useful capabilities already built in, such as planning, file system tools, and subagents.

Use deep agents when you want maximum capability with minimal setup; choose LangChain agents when you need fine-grained control.

To compare both in this step, install the `deepagents` package:

```bash uv
uv add deepagents
```

```bash pip
pip install -U deepagents
```

**Warning:**

This example sends the entire text of The Great Gatsby to the model and may take a minute or two to respond. You can view example output in the next step.

Let's try both:

```python wrap
from langchain.agents import create_agent
from deepagents import create_deep_agent

agent = create_agent(
    model=model,
    tools=[fetch_text_from_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

deep_agent = create_deep_agent(
    model=model,
    tools=[fetch_text_from_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

content = f"""Project Gutenberg hosts a full plain-text copy of F. Scott Fitzgerald's The Great Gatsby.
URL: https://www.gutenberg.org/files/64317/64317-0.txt

Answer as much as you can:

1) How many lines in the complete Gutenberg file contain the substring `Gatsby` (count lines, not occurrences within a line, each line ends with a line break).
2) The 1-based line number of the first line in the file that contains `Daisy`.
3) A two-sentence neutral synopsis.

        Do your best on (1) and (2). If at any point you realize you cannot **verify** an exact answer with
        your available tools and reasoning, do not fabricate numbers: use `null` for that field and spell out
        the limitation in `how_you_computed_counts`. If you encounter any errors please report what the error was and what the error message was."""

print("Running create_agent...", flush=True)
agent_result = agent.invoke(
    {"messages": [{"role": "user", "content": content}]},
    config={"configurable": {"thread_id": "great-gatsby-lc"}},
)
print("Running create_deep_agent...", flush=True)
deep_agent_result = deep_agent.invoke(
    {"messages": [{"role": "user", "content": content}]},
    config={"configurable": {"thread_id": "great-gatsby-da"}},
)
print("\ncreate_agent:")
print(agent_result["messages"][-1].content_blocks)
print("\ncreate_deep_agent:")
print(deep_agent_result["messages"][-1].content_blocks)
```

The following expander has everything together in a runnable script:

**Full example code**

```python wrap
import urllib.error
import urllib.request

from langchain.agents import create_agent
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

SYSTEM_PROMPT = """You are a literary data assistant.

## Capabilities

- `fetch_text_from_url`: loads document text from a URL into the conversation.
Do not guess line counts or positions—ground them in tool results from the saved file."""

@tool
def fetch_text_from_url(url: str) -> str:
    """Fetch the document from a URL.
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; quickstart-research/1.0)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except urllib.error.URLError as e:
        return f"Fetch failed: {e}"
    text = raw.decode("utf-8", errors="replace")
    return text

model = init_chat_model(
    "gemini-3.1-pro-preview",
    model_provider="google-genai",
    temperature=0.5,
    timeout=600,
    max_tokens=25000,
    streaming=True,
)

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    tools=[fetch_text_from_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

deep_agent = create_deep_agent(
    model=model,
    tools=[fetch_text_from_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

content = f"""Project Gutenberg hosts a full plain-text copy of F. Scott Fitzgerald's The Great Gatsby.
URL: https://www.gutenberg.org/files/64317/64317-0.txt

Answer as much as you can:

1) How many lines in the complete Gutenberg file contain the substring `Gatsby` (count lines, not occurrences within a line, each line ends with a line break).
2) The 1-based line number of the first line in the file that contains `Daisy`.
3) A two-sentence neutral synopsis.

        Do your best on (1) and (2). If at any point you realize you cannot **verify** an exact answer with
        your available tools and reasoning, do not fabricate numbers: use `null` for that field and spell out
        the limitation in `how_you_computed_counts`. If you encounter any errors please report what the error was and what the error message was."""

print("Running create_agent...", flush=True)
agent_result = agent.invoke(
    {"messages": [{"role": "user", "content": content}]},
    config={"configurable": {"thread_id": "great-gatsby-lc"}},
)
print("Running create_deep_agent...", flush=True)
deep_agent_result = deep_agent.invoke(
    {"messages": [{"role": "user", "content": content}]},
    config={"configurable": {"thread_id": "great-gatsby-da"}},
)
print("\ncreate_agent:")
print(agent_result["messages"][-1].content_blocks)
print("\ncreate_deep_agent:")
print(deep_agent_result["messages"][-1].content_blocks)
```

**Review the results**

The results will differ based on the model and the execution.

**LangChain agents**

````txt wrap expandable
**1) Number of lines containing `Gatsby`:** `null`

**2) First line containing `Daisy`:** `null`

**3) Synopsis:**
The Great Gatsby follows the mysterious millionaire Jay Gatsby and his obsession with reuniting with his former lover, Daisy Buchanan, as narrated by his neighbor Nick Carraway. Set against the backdrop of the Roaring Twenties on Long Island, the novel explores themes of wealth, class, and the elusive nature of the American Dream.

**how_you_computed_counts:**
I successfully fetched the full text of the eBook using the `fetch_text_from_url` tool. However, because I do not have access to a code execution environment (like Python) or text-processing tools (like `grep`), I cannot deterministically split the text by line breaks, iterate through the thousands of lines, and verify the exact line numbers or match counts. LLMs cannot reliably perform exact line-counting or indexing over massive texts within their context window without external computational tools. As instructed, rather than fabricating or guessing a number, I have output `null` for the exact counts and positions.
````

**Deep agents**

````txt wrap expandable
Based on the text fetched directly from the Gutenberg URL and analyzed using filesystem search tools, here are the answers to your questions:

**1) Lines containing the substring `Gatsby`**
**258** lines contain the exact substring `Gatsby`.

**2) First line containing `Daisy`**
Line **181** is the first line in the file that contains the exact substring `Daisy`.
*(For context, the line reads: "Buchanans. Daisy was my second cousin once removed, and I’d known Tom")*

**3) Two-sentence neutral synopsis**
*The Great Gatsby* follows the mysterious millionaire Jay Gatsby and his obsessive pursuit to reunite with his former lover, Daisy Buchanan, in 1920s Long Island. The story is narrated by Nick Carraway, who observes the tragic consequences of Gatsby's relentless ambition and the shallow materialism of the era's wealthy elite.

***

**How counts were computed:**
When fetching the document from the URL, the file was too large for the standard output and was automatically saved to the local filesystem by the system (`/large_tool_results/x246ax2x`). I then used the `grep` tool to search the saved file for the exact literal substrings `Gatsby` and `Daisy`. The `grep` tool returned every matching line along with its 1-based line number. I manually counted the exact number of lines returned for `Gatsby` (which totaled 258) and identified the first line number returned for `Daisy` (which was 181). I also verified there were no uppercase variations (`GATSBY` or `DAISY`) that would have been missed. No errors were encountered during this process.
````

If you look at the output on both tabs, you notice that the LangChain agent provided answers but they are estimates. The agent lacks the tools to answer this question. You may also get errors that the prompt is too long.

The deep agent, on the other hand can:

1. **Plans its approach** using the built-in [`write_todos`](/oss/deepagents/harness#task-planning) tool to break down the research task.
1. **Loads the file** by calling the `fetch_text_from_url` tool to gather information.
1. **Manages context** by using file system tools ([`grep`](/oss/deepagents/harness#virtual-filesystem-access) and [`read_file`](/oss/deepagents/harness#virtual-filesystem-access)).
1. **Spawns subagents** as needed to delegate complex subtasks to specialized subagents.

        For LangChain agents, you must implement more capabilities to get a similar level of service and can customize them along the way as needed.

## Trace agent calls

Most interesting applications you build with LangChain make many calls to LLMs. As these applications get more complex, it becomes important to be able to inspect what exactly is going on inside your agent. The best way to do this is with [LangSmith](https://smith.langchain.com).

Sign up for a [LangSmith](https://smith.langchain.com) account and set these to start logging traces:

```shell
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```

Once set, run your script again and then inspect what happened during your agent calls on [LangSmith](https://smith.langchain.com) .

**Tip:**

To learn more about tracing your agent with LangSmith, see the [LangSmith documentation](/langsmith/trace-with-langchain).

We recommend you also set up [LangSmith Engine](/langsmith/engine) which monitors your traces, detects issues, and proposes fixes.

## Next steps

You now have agents that can:

- **Understand context** and remember conversations
- **Use tools** intelligently
- **Provide structured responses** in a consistent format
- **Handle user-specific information** through context
- **Maintain conversation state** across interactions
- **Plan, research, and synthesize** (deep agents only)

Continue with:

- **LangChain agents**: [Add and manage memory](/oss/langgraph/add-memory#manage-short-term-memory), [deploy to production](/oss/langgraph/deploy)
- **Deep Agents**: [Customization options](/oss/deepagents/customization), [persistent memory](/oss/deepagents/memory), [deploy to production](/oss/langgraph/deploy)

---

# Runtime
> 출처: data/raw/langchain/runtime.mdx | https://docs.langchain.com/oss/python/langchain/runtime

## Overview

LangChain's `create_agent` runs on LangGraph's runtime under the hood.
LangGraph exposes a `Runtime` object with the following information:

1. **Context**: static information like user id, db connections, or other dependencies for an agent invocation
2. **Store**: a BaseStore instance used for [long-term memory](/oss/langchain/long-term-memory)
3. **Stream writer**: an object used for streaming information via the `"custom"` stream mode
4. **Execution info**: identity and retry information for the current execution (thread ID, run ID, attempt number)
5. **Server info**: server-specific metadata when running on LangGraph Server (assistant ID, graph ID, authenticated user)

**Tip:**

Runtime context provides **dependency injection** for your tools and middleware. Instead of hardcoding values or using global state, you can inject runtime dependencies (like database connections, user IDs, or configuration) when invoking your agent. This makes your tools more testable, reusable, and flexible.

You can access the runtime information within [tools](#inside-tools) and [middleware](#inside-middleware).

## Access

When creating an agent with `create_agent`, you can specify a `context_schema` to define the structure of the `context` stored in the agent `Runtime`.

When invoking the agent, pass the `context` argument with the relevant configuration for the run:

```python
from dataclasses import dataclass

from langchain.agents import create_agent

@dataclass
class Context:
    user_name: str

agent = create_agent(
    model="gpt-5-nano",
    tools=[...],
    context_schema=Context  # [!code highlight]
)

agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    context=Context(user_name="John Smith")  # [!code highlight]
)
```

### Inside tools

You can access the runtime information inside tools to:

* Access the context
* Read or write long-term memory
* Write to the [custom stream](/oss/langchain/streaming#custom-updates) (ex, tool progress / updates)

Use the `ToolRuntime` parameter to access the `Runtime` object inside a tool.

```python
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime  # [!code highlight]

@dataclass
class Context:
    user_id: str

@tool
def fetch_user_email_preferences(runtime: ToolRuntime[Context]) -> str:  # [!code highlight]
    """Fetch the user's email preferences from the store."""
    user_id = runtime.context.user_id  # [!code highlight]

preferences: str = "The user prefers you to write a brief and polite email."
if runtime.store:  # [!code highlight]
    if memory := runtime.store.get(("users",), user_id):  # [!code highlight]
        preferences = memory.value["preferences"]

    return preferences
```

### Execution info and server info inside tools

Access execution identity (thread ID, run ID) via `runtime.execution_info`, and server-specific metadata (assistant ID, authenticated user) via `runtime.server_info` when running on LangGraph Server:

```python
from langchain.tools import tool, ToolRuntime

@tool
def context_aware_tool(runtime: ToolRuntime) -> str:
    """A tool that uses execution and server info."""
    # Access thread and run IDs
    info = runtime.execution_info
    print(f"Thread: {info.thread_id}, Run: {info.run_id}")  # [!code highlight]

# Access server info (only available on LangGraph Server)
server = runtime.server_info
if server is not None:
    print(f"Assistant: {server.assistant_id}")  # [!code highlight]
    if server.user is not None:
        print(f"User: {server.user.identity}")  # [!code highlight]

    return "done"
```

`server_info` is `None` when not running on LangGraph Server (e.g., during local development).

**Note:**

Requires `deepagents>=0.5.0` (or `langgraph>=1.1.5`) for `runtime.execution_info` and `runtime.server_info`.

### Inside middleware

You can access runtime information in middleware to create dynamic prompts, modify messages, or control agent behavior based on user context.

Use the `Runtime` parameter to access the `Runtime` object inside [node-style hooks](/oss/langchain/middleware/custom#node-style-hooks).  For [wrap-style hooks](/oss/langchain/middleware/custom#wrap-style-hooks), the `Runtime` object is available inside the `ModelRequest` parameter.

```python
from dataclasses import dataclass

from langchain.messages import AnyMessage
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import dynamic_prompt, ModelRequest, before_model, after_model
from langgraph.runtime import Runtime

@dataclass
class Context:
    user_name: str

# Dynamic prompts
@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    user_name = request.runtime.context.user_name  # [!code highlight]
    system_prompt = f"You are a helpful assistant. Address the user as {user_name}."
    return system_prompt

# Before model hook
@before_model
def log_before_model(state: AgentState, runtime: Runtime[Context]) -> dict | None:  # [!code highlight]
    print(f"Processing request for user: {runtime.context.user_name}")  # [!code highlight]
    return None

# After model hook
@after_model
def log_after_model(state: AgentState, runtime: Runtime[Context]) -> dict | None:  # [!code highlight]
    print(f"Completed request for user: {runtime.context.user_name}")  # [!code highlight]
    return None

agent = create_agent(
    model="gpt-5-nano",
    tools=[...],
    middleware=[dynamic_system_prompt, log_before_model, log_after_model],  # [!code highlight]
    context_schema=Context
)

agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    context=Context(user_name="John Smith")
)
```

### Execution info and server info inside middleware

Middleware hooks can also access `runtime.execution_info` and `runtime.server_info`:

```python
from langchain.agents import AgentState
from langchain.agents.middleware import before_model
from langgraph.runtime import Runtime

@before_model
def auth_gate(state: AgentState, runtime: Runtime) -> dict | None:
    """Block unauthenticated users when running on LangGraph Server."""
    server = runtime.server_info
    if server is not None and server.user is None:  # [!code highlight]
        raise ValueError("Authentication required")
    print(f"Thread: {runtime.execution_info.thread_id}")  # [!code highlight]
    return None
```

**Note:**

Requires `deepagents>=0.5.0` (or `langgraph>=1.1.5`).

---

# Short-term memory
> 출처: data/raw/langchain/short-term-memory.mdx | https://docs.langchain.com/oss/python/langchain/short-term-memory

## Overview

Memory is a system that remembers information about previous interactions. For AI agents, memory is crucial because it lets them remember previous interactions, learn from feedback, and adapt to user preferences. As agents tackle more complex tasks with numerous user interactions, this capability becomes essential for both efficiency and user satisfaction.

Short term memory lets your application remember previous interactions within a single thread or conversation.

**Note:**

A thread organizes multiple interactions in a session, similar to the way email groups messages in a single conversation.

Conversation history is the most common form of short-term memory. Long conversations pose a challenge to today's LLMs; a full history may not fit inside an LLM's context window, resulting in a context loss or errors.

Even if your model supports the full context length, most LLMs still perform poorly over long contexts. They get "distracted" by stale or off-topic content, all while suffering from slower response times and higher costs.

Chat models accept context using [messages](/oss/langchain/messages), which include instructions (a system message) and inputs (human messages). In chat applications, messages alternate between human inputs and model responses, resulting in a list of messages that grows longer over time. Because context windows are limited, many applications can benefit from using techniques to remove or "forget" stale information.

**Tip:**

Need to remember information **across** conversations? Use [long-term memory](/oss/langchain/long-term-memory) to store and recall user-specific or application-level data across different threads and sessions.

## Usage

To add short-term memory (thread-level persistence) to an agent, you need to specify a `checkpointer` when creating an agent.

**Info:**

LangChain's agent manages short-term memory as a part of your agent's state.

By storing these in the graph's state, the agent can access the full context for a given conversation while maintaining separation between different threads.

State is persisted to a database (or memory) using a checkpointer so the thread can be resumed at any time.

Short-term memory updates when the agent is invoked or a step (like a tool call) is completed, and the state is read at the start of each step.

```python Google
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  # [!code highlight]

def get_user_info() -> str:
    """Look up information about the current user."""
    return "No user profile on file."

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),  # [!code highlight]
)

thread_config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "Hi Bob! Nice to see you here. How are you doing?"

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "You are Bob!"
```

```python OpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  # [!code highlight]

def get_user_info() -> str:
    """Look up information about the current user."""
    return "No user profile on file."

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),  # [!code highlight]
)

thread_config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "Hi Bob! Nice to see you here. How are you doing?"

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "You are Bob!"
```

```python Anthropic
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  # [!code highlight]

def get_user_info() -> str:
    """Look up information about the current user."""
    return "No user profile on file."

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),  # [!code highlight]
)

thread_config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "Hi Bob! Nice to see you here. How are you doing?"

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "You are Bob!"
```

```python OpenRouter
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  # [!code highlight]

def get_user_info() -> str:
    """Look up information about the current user."""
    return "No user profile on file."

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),  # [!code highlight]
)

thread_config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "Hi Bob! Nice to see you here. How are you doing?"

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "You are Bob!"
```

```python Fireworks
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  # [!code highlight]

def get_user_info() -> str:
    """Look up information about the current user."""
    return "No user profile on file."

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),  # [!code highlight]
)

thread_config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "Hi Bob! Nice to see you here. How are you doing?"

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "You are Bob!"
```

```python Baseten
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  # [!code highlight]

def get_user_info() -> str:
    """Look up information about the current user."""
    return "No user profile on file."

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),  # [!code highlight]
)

thread_config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "Hi Bob! Nice to see you here. How are you doing?"

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "You are Bob!"
```

```python Ollama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  # [!code highlight]

def get_user_info() -> str:
    """Look up information about the current user."""
    return "No user profile on file."

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),  # [!code highlight]
)

thread_config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "Hi Bob! Nice to see you here. How are you doing?"

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    thread_config,  # [!code highlight]
)["messages"][-1].content

print(response)  # "You are Bob!"
```

- [View example trace](https://smith.langchain.com/public/29a89413-165f-4e8f-9fa6-e0a0ef296df1/r)

  Open a public LangSmith run for this example.

### In production

In production, use a checkpointer backed by a database:

```bash pip
pip install -U langgraph-checkpoint-postgres "psycopg[binary]"
```

```bash uv
uv add langgraph-checkpoint-postgres "psycopg[binary]"
```

**Note:**

By default, `langgraph-checkpoint-postgres` installs `psycopg` (Psycopg 3) without extras. The install above adds `psycopg[binary]`, which is recommended for most users. For other options, see the [Psycopg installation docs](https://www.psycopg.org/psycopg3/docs/basic/install.html).

```python
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver  # [!code highlight]

def get_user_info() -> str:
    """Look up information about the current user."""
    return "No user profile on file."

DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup() # auto create tables in PostgreSQL
    agent = create_agent(
        "gpt-5.5",
        tools=[get_user_info],
        checkpointer=checkpointer,  # [!code highlight]
    )
```

**Note:**

For more checkpointer options including SQLite, Postgres, and Azure Cosmos DB, see the [list of checkpointer libraries](/oss/langgraph/checkpointers#checkpointer-libraries) in the Persistence documentation.

## Customizing agent memory

By default, agents use `AgentState` to manage short term memory, specifically the conversation history via a `messages` key.

You can extend `AgentState` to add additional fields. Custom state schemas are passed to `create_agent` using the `state_schema` parameter.

```python
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver

class CustomAgentState(AgentState):  # [!code highlight]
    user_id: str  # [!code highlight]
    preferences: dict  # [!code highlight]

agent = create_agent(
    "gpt-5.5",
    tools=[get_user_info],
    state_schema=CustomAgentState,  # [!code highlight]
    checkpointer=InMemorySaver(),
)

# Custom state can be passed in invoke
result = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Hello"}],
        "user_id": "user_123",  # [!code highlight]
        "preferences": {"theme": "dark"}  # [!code highlight]
    },
    {"configurable": {"thread_id": "1"}})
```

## Common patterns

With [short-term memory](#usage) enabled, long conversations can exceed the LLM's context window. Common solutions are:

- [Trim messages](#trim-messages)

        Remove first or last N messages (before calling LLM)

- [Delete messages](#delete-messages)

        Delete messages from LangGraph state permanently

- [Summarize messages](#summarize-messages)

        Summarize earlier messages in the history and replace them with a summary

- **Custom strategies**

        Custom strategies (e.g., message filtering, etc.)

This allows the agent to keep track of the conversation without exceeding the LLM's context window.

### Trim messages

Most LLMs have a maximum supported context window (denominated in tokens).

One way to decide when to truncate messages is to count the tokens in the message history and truncate whenever it approaches that limit. If you're using LangChain, you can use the trim messages utility and specify the number of tokens to keep from the list, as well as the `strategy` (e.g., keep the last `max_tokens`) to use for handling the boundary.

To trim message history in an agent, use the `@before_model` middleware decorator:

```python
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig
from typing import Any

@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window."""
    messages = state["messages"]

if len(messages) <= 3:
    return None  # No changes needed

first_msg = messages[0]
recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
new_messages = [first_msg] + recent_messages

return {
    "messages": [
        RemoveMessage(id=REMOVE_ALL_MESSAGES),
        *new_messages
    ]
}

agent = create_agent(
    "gpt-5.5",
    tools=[...],
    middleware=[trim_messages],
    checkpointer=InMemorySaver(),
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

agent.invoke({"messages": "hi, my name is bob"}, config)
agent.invoke({"messages": "write a short poem about cats"}, config)
agent.invoke({"messages": "now do the same but for dogs"}, config)
final_response = agent.invoke({"messages": "what's my name?"}, config)

final_response["messages"][-1].pretty_print()
"""
================================== Ai Message ==================================

Your name is Bob. You told me that earlier.
If you'd like me to call you a nickname or use a different name, just say the word.
"""
```

### Delete messages

You can delete messages from the graph state to manage the message history.

This is useful when you want to remove specific messages or clear the entire message history.

To delete messages from the graph state, you can use the `RemoveMessage`.

For `RemoveMessage` to work, you need to use a state key with `add_messages` [reducer](/oss/langgraph/graph-api#reducers).

The default `AgentState` provides this.

To remove specific messages:

```python
from langchain.messages import RemoveMessage  # [!code highlight]

def delete_messages(state):
    messages = state["messages"]
    if len(messages) > 2:
        # remove the earliest two messages
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}  # [!code highlight]
```

To remove **all** messages:

```python
from langgraph.graph.message import REMOVE_ALL_MESSAGES  # [!code highlight]

def delete_messages(state):
    return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)]}  # [!code highlight]
```

**Warning:**

When deleting messages, **make sure** that the resulting message history is valid. Check the limitations of the LLM provider you're using. For example:

* Some providers expect message history to start with a `user` message
* Most providers require `assistant` messages with tool calls to be followed by corresponding `tool` result messages.

```python
from langchain.messages import RemoveMessage
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig

@after_model
def delete_old_messages(state: AgentState, runtime: Runtime) -> dict | None:
    """Remove old messages to keep conversation manageable."""
    messages = state["messages"]
    if len(messages) > 2:
        # remove the earliest two messages
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}
    return None

agent = create_agent(
    "gpt-5-nano",
    tools=[...],
    system_prompt="Please be concise and to the point.",
    middleware=[delete_old_messages],
    checkpointer=InMemorySaver(),
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

stream = agent.stream_events(
    {"messages": [{"role": "user", "content": "hi! I'm bob"}]},
    config,
    version="v3",
)
for snapshot in stream.values:
    print([(message.type, message.content) for message in snapshot["messages"]])

stream = agent.stream_events(
    {"messages": [{"role": "user", "content": "write a short poem about cats"}]},
    config,
    version="v3",
)
for snapshot in stream.values:
    print([(message.type, message.content) for message in snapshot["messages"]])

stream = agent.stream_events(
    {"messages": [{"role": "user", "content": "what's my name?"}]},
    config,
    version="v3",
)
for snapshot in stream.values:
    print([(message.type, message.content) for message in snapshot["messages"]])
```

```
[('human', "hi! I'm bob")]
[('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today? I can answer questions, brainstorm ideas, draft text, explain things, or help with code.')]
[('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today? I can answer questions, brainstorm ideas, draft text, explain things, or help with code.'), ('human', "write a short poem about cats")]
[('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today? I can answer questions, brainstorm ideas, draft text, explain things, or help with code.'), ('human', "write a short poem about cats"), ('ai', 'There once was a cat on a wall, Who barely moved at all...')]
[('human', 'write a short poem about cats'), ('ai', 'There once was a cat on a wall, Who barely moved at all...')]
[('human', 'write a short poem about cats'), ('ai', 'There once was a cat on a wall, Who barely moved at all...'), ('human', "what's my name?")]
[('human', 'write a short poem about cats'), ('ai', 'There once was a cat on a wall, Who barely moved at all...'), ('human', "what's my name?"), ('ai', "I don't know your name - you haven't told me!")]
[('human', "what's my name?"), ('ai', "I don't know your name - you haven't told me!")]
```

### Summarize messages

The problem with trimming or removing messages, as shown above, is that you may lose information from culling of the message queue.
Because of this, some applications benefit from a more sophisticated approach of summarizing the message history using a chat model.

![Summary](/oss/images/summary.png)

To summarize message history in an agent, use the built-in [``SummarizationMiddleware``](/oss/langchain/middleware#summarization):

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

checkpointer = InMemorySaver()

agent = create_agent(
    model="gpt-5.5",
    tools=[...],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20)
        )
    ],
    checkpointer=checkpointer,
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}
agent.invoke({"messages": "hi, my name is bob"}, config)
agent.invoke({"messages": "write a short poem about cats"}, config)
agent.invoke({"messages": "now do the same but for dogs"}, config)
final_response = agent.invoke({"messages": "what's my name?"}, config)

final_response["messages"][-1].pretty_print()
"""
================================== Ai Message ==================================

Your name is Bob!
"""
```

See [`SummarizationMiddleware`](/oss/langchain/middleware#summarization) for more configuration options.

## Access memory

You can access and modify the short-term memory (state) of an agent in several ways:

### Tools

#### Read short-term memory in a tool

Access short term memory (state) in a tool using the `runtime` parameter (typed as `ToolRuntime`).

The `runtime` parameter is hidden from the tool signature (so the model doesn't see it), but the tool can access the state through it.

```python
from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime

class CustomState(AgentState):
    user_id: str

@tool
def get_user_info(
    runtime: ToolRuntime
) -> str:
    """Look up user info."""
    user_id = runtime.state["user_id"]
    return "User is John Smith" if user_id == "user_123" else "Unknown user"

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_user_info],
    state_schema=CustomState,
)

result = agent.invoke({
    "messages": "look up user information",
    "user_id": "user_123"
})
print(result["messages"][-1].content)
# > User is John Smith.
```

#### Write short-term memory from tools

To modify the agent's short-term memory (state) during execution, you can return state updates directly from the tools.

This is useful for persisting intermediate results or making information accessible to subsequent tools or prompts.

```python
from langchain.tools import tool, ToolRuntime
from langchain_core.runnables import RunnableConfig
from langchain.messages import ToolMessage
from langchain.agents import create_agent, AgentState
from langgraph.types import Command
from pydantic import BaseModel

class CustomState(AgentState):  # [!code highlight]
    user_name: str

class CustomContext(BaseModel):
    user_id: str

@tool
def update_user_info(
    runtime: ToolRuntime[CustomContext, CustomState],
) -> Command:
    """Look up and update user info."""
    user_id = runtime.context.user_id
    name = "John Smith" if user_id == "user_123" else "Unknown user"
    return Command(update={  # [!code highlight]
        "user_name": name,
        # update the message history
        "messages": [
            ToolMessage(
                "Successfully looked up user information",
                tool_call_id=runtime.tool_call_id
            )
        ]
    })

@tool
def greet(
    runtime: ToolRuntime[CustomContext, CustomState]
) -> str | Command:
    """Use this to greet the user once you found their info."""
    user_name = runtime.state.get("user_name", None)
    if user_name is None:
       return Command(update={
            "messages": [
                ToolMessage(
                    "Please call the 'update_user_info' tool it will get and update the user's name.",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        })
    return f"Hello {user_name}!"

agent = create_agent(
    model="gpt-5-nano",
    tools=[update_user_info, greet],
    state_schema=CustomState, # [!code highlight]
    context_schema=CustomContext,
)

agent.invoke(
    {"messages": [{"role": "user", "content": "greet the user"}]},
    context=CustomContext(user_id="user_123"),
)
```

### Prompt

Access short term memory (state) in middleware to create dynamic prompts based on conversation history or custom state fields.

```python
from langchain.agents import create_agent
from typing import TypedDict
from langchain.agents.middleware import dynamic_prompt, ModelRequest

class CustomContext(TypedDict):
    user_name: str

def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is always sunny!"

@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    user_name = request.runtime.context["user_name"]
    system_prompt = f"You are a helpful assistant. Address the user as {user_name}."
    return system_prompt

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
    middleware=[dynamic_system_prompt],
    context_schema=CustomContext,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    context=CustomContext(user_name="John Smith"),
)
for msg in result["messages"]:
    msg.pretty_print()

```

```shell title="Output"
================================ Human Message =================================

What is the weather in SF?
================================== Ai Message ==================================
Tool Calls:
  get_weather (call_WFQlOGn4b2yoJrv7cih342FG)
 Call ID: call_WFQlOGn4b2yoJrv7cih342FG
  Args:
    city: San Francisco
================================= Tool Message =================================
Name: get_weather

The weather in San Francisco is always sunny!
================================== Ai Message ==================================

Hi John Smith, the weather in San Francisco is always sunny!
```

### Before model

Access short term memory (state) in `@before_model` middleware to process messages before model calls.

```mermaid
%%{
    init: {
        "fontFamily": "monospace",
        "flowchart": {
        "curve": "basis"
        }
    }
}%%
graph TD
    S(["`\_\_start\_\_`"])
    PRE(before_model)
    MODEL(model)
    TOOLS(tools)
    END(["`\_\_end\_\_`"])
    S --> PRE
    PRE --> MODEL
    MODEL -.-> TOOLS
    MODEL -.-> END
    TOOLS --> PRE
    classDef blueHighlight fill:#E5F4FF,stroke:#006DDD,color:#030710;
    classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68;
    class S blueHighlight;
    class END blueHighlight;
    class PRE,MODEL,TOOLS neutral;
```

```python
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from typing import Any

@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window."""
    messages = state["messages"]

if len(messages) <= 3:
    return None  # No changes needed

first_msg = messages[0]
recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
new_messages = [first_msg] + recent_messages

return {
    "messages": [
        RemoveMessage(id=REMOVE_ALL_MESSAGES),
        *new_messages
    ]
}

agent = create_agent(
    "gpt-5-nano",
    tools=[],
    middleware=[trim_messages],
    checkpointer=InMemorySaver()
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

agent.invoke({"messages": "hi, my name is bob"}, config)
agent.invoke({"messages": "write a short poem about cats"}, config)
agent.invoke({"messages": "now do the same but for dogs"}, config)
final_response = agent.invoke({"messages": "what's my name?"}, config)

final_response["messages"][-1].pretty_print()
"""
================================== Ai Message ==================================

Your name is Bob. You told me that earlier.
If you'd like me to call you a nickname or use a different name, just say the word.
"""
```

### After model

Access short term memory (state) in `@after_model` middleware to process messages after model calls.

```mermaid
%%{
    init: {
        "fontFamily": "monospace",
        "flowchart": {
        "curve": "basis"
        }
    }
}%%
graph TD
    S(["\_\_start\_\_"])
    MODEL(model)
    POST(after_model)
    TOOLS(tools)
    END(["\_\_end\_\_"])
    S --> MODEL
    MODEL --> POST
    POST -.-> END
    POST -.-> TOOLS
    TOOLS --> MODEL
    classDef blueHighlight fill:#E5F4FF,stroke:#006DDD,color:#030710;
    classDef greenHighlight fill:#F6FFDB,stroke:#6E8900,color:#2E3900;
    classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68;
    class S blueHighlight;
    class END blueHighlight;
    class POST greenHighlight;
    class MODEL,TOOLS neutral;
```

```python
from langchain.messages import RemoveMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langgraph.runtime import Runtime

@after_model
def validate_response(state: AgentState, runtime: Runtime) -> dict | None:
    """Remove messages containing sensitive words."""
    STOP_WORDS = ["password", "secret"]
    last_message = state["messages"][-1]
    if any(word in last_message.content for word in STOP_WORDS):
        return {"messages": [RemoveMessage(id=last_message.id)]}
    return None

agent = create_agent(
    model="gpt-5-nano",
    tools=[],
    middleware=[validate_response],
    checkpointer=InMemorySaver(),
)
```

---

# Build a SQL agent
> 출처: data/raw/langchain/sql-agent.mdx | https://docs.langchain.com/oss/python/langchain/sql-agent

## Overview

In this tutorial, you will learn how to build an agent that can answer questions about a SQL database using LangChain [agents](/oss/langchain/agents).

At a high level, the agent will:

1. Fetch the available tables and schemas from the database
1. Decide which tables are relevant to the question
1. Fetch the schemas for the relevant tables
1. Generate a query based on the question and information from the schemas
1. Double-check the query for common mistakes using an LLM
1. Execute the query and return the results
1. Correct mistakes surfaced by the database engine until the query is successful
1. Formulate a response based on the results

**Warning:**

Building Q&A systems of SQL databases requires executing model-generated SQL queries. There are inherent risks in doing this. Make sure that your database connection permissions are always scoped as narrowly as possible for your agent's needs. This will mitigate, though not eliminate, the risks of building a model-driven system.

### Concepts

The following tutorial covers the following concepts:

- [Tools](/oss/langchain/tools) for reading from SQL databases
- LangChain [agents](/oss/langchain/agents)
- [Human-in-the-loop](/oss/langchain/human-in-the-loop) processes

## Setup

**Install dependencies**

```bash pip
pip install langchain langgraph
```

**Set up LangSmith**

Set up [LangSmith](https://smith.langchain.com) to inspect what is happening inside your chain or agent. Then set the following environment variables:

```shell
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```

## Build your SQL agent

**Select an LLM**

Select a model that supports [tool-calling](/oss/integrations/providers/overview):

**OpenAI**

👉 Read the [OpenAI chat model integration docs](/oss/python/integrations/chat/openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-5.5")
```
```python Model Class
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-..."

model = ChatOpenAI(model="gpt-5.5")
```

**Anthropic**

👉 Read the [Anthropic chat model integration docs](/oss/python/integrations/chat/anthropic/)

```bash pip
pip install -U "langchain[anthropic]"
```

```bash uv
uv add "langchain[anthropic]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = init_chat_model("claude-sonnet-4-6")
```
```python Model Class
import os
from langchain_anthropic import ChatAnthropic

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = ChatAnthropic(model="claude-sonnet-4-6")
```

**Azure**

👉 Read the [Azure chat model integration docs](/oss/python/integrations/chat/azure_chat_openai/)

```bash pip
pip install -U "langchain[openai]"
```

```bash uv
uv add "langchain[openai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = init_chat_model(
    "azure_openai:gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
```
```python Model Class
import os
from langchain_openai import AzureChatOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = "..."
os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

model = AzureChatOpenAI(
    model="gpt-5.5",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
)
```

**Google Gemini**

👉 Read the [Google GenAI chat model integration docs](/oss/python/integrations/chat/google_generative_ai/)

```bash pip
pip install -U "langchain[google-genai]"
```

```bash uv
uv add "langchain[google-genai]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["GOOGLE_API_KEY"] = "..."

model = init_chat_model("google_genai:gemini-3.7-flash")
```
```python Model Class
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "..."

model = ChatGoogleGenerativeAI(model="gemini-3.7-flash")
```

**AWS Bedrock**

👉 Read the [AWS Bedrock chat model integration docs](/oss/python/integrations/chat/bedrock/)

```bash pip
pip install -U "langchain[aws]"
```

```bash uv
uv add "langchain[aws]"
```

```python init_chat_model
from langchain.chat_models import init_chat_model

# Follow the steps here to configure your credentials:
# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html

model = init_chat_model(
    "us.anthropic.claude-sonnet-4-6",
    model_provider="bedrock_converse",
)
```
```python Model Class
from langchain_aws import ChatBedrock

model = ChatBedrock(model="us.anthropic.claude-sonnet-4-6")
```

**HuggingFace**

👉 Read the [HuggingFace chat model integration docs](/oss/python/integrations/chat/huggingface/)

```bash pip
pip install -U "langchain[huggingface]"
```

```bash uv
uv add "langchain[huggingface]"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

model = init_chat_model(
    "microsoft/Phi-3-mini-4k-instruct",
    model_provider="huggingface",
    temperature=0.7,
    max_tokens=1024,
)
```

```python Model Class
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    temperature=0.7,
    max_length=1024,
)
model = ChatHuggingFace(llm=llm)
```

**OpenRouter**

👉 Read the [OpenRouter chat model integration docs](/oss/python/integrations/chat/openrouter/)

```bash pip
pip install -U "langchain-openrouter"
```

```bash uv
uv add "langchain-openrouter"
```

```python init_chat_model
import os
from langchain.chat_models import init_chat_model

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = init_chat_model(
    "auto",
    model_provider="openrouter",
)
```
```python Model Class
import os
from langchain_openrouter import ChatOpenRouter

os.environ["OPENROUTER_API_KEY"] = "sk-..."

model = ChatOpenRouter(model="auto")
```

The output shown in the examples below used OpenAI.

**Configure the database**

You will be creating a [SQLite database](https://www.sqlitetutorial.net/sqlite-sample-database/) for this tutorial. SQLite is a lightweight database that is easy to set up and use. We will be loading the `chinook` database, which is a sample database that represents a digital media store.

For convenience, we have hosted the database (`Chinook.db`) on a public GCS bucket.

```python
import pathlib
import requests

url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")

if local_path.exists():
    print(f"{local_path} already exists, skipping download.")
else:
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"File downloaded and saved as {local_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
```

We will use Python's built-in `sqlite3` module to interact with the database:

```python
import sqlite3

con = sqlite3.connect("Chinook.db")
cursor = con.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]

print("Dialect: sqlite")
print(f"Available tables: {tables}")

cursor.execute("SELECT * FROM Artist LIMIT 5;")
print(f"Sample output: {cursor.fetchall()}")
con.close()
```

```
Dialect: sqlite
Available tables: ['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice', 'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']
Sample output: [(1, 'AC/DC'), (2, 'Accept'), (3, 'Aerosmith'), (4, 'Alanis Morissette'), (5, 'Alice In Chains')]
```

**Add tools for database interactions**

**Warning:**

The following database tools are minimal wrappers for demonstration purposes only. They are not intended to be secure or used in production. Use narrowly scoped database permissions and add application-specific validation before executing model-generated SQL.

We can implement database [tools](/oss/langchain/tools) as thin wrappers using the `@tool` decorator from `langchain.tools`:

```python
import sqlite3
from langchain.tools import tool

# Below are minimal tools for demonstration purposes.
# They are not intended to be secure or for production use.

@tool
def sql_db_list_tables() -> str:
    """Input is an empty string, output is a comma-separated list of tables in the database."""
    con = sqlite3.connect("Chinook.db")
    try:
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]
        return ", ".join(tables)
    finally:
        con.close()

@tool
def sql_db_schema(table_names: str) -> str:
    """Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables.
    Be sure that the tables actually exist by calling sql_db_list_tables first!
    Example Input: table1, table2, table3"""
    con = sqlite3.connect("Chinook.db")
    try:
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        valid_tables = {row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")}
        results = []
        for table in table_names.split(","):
            table = table.strip()
            if table not in valid_tables:
                results.append(f"Error: table_names {{{table!r}}} not found in database")
                continue
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,))
            schema_row = cursor.fetchone()
            if schema_row:
                results.append(schema_row[0])
                try:
                    quoted_table = '"' + table.replace('"', '""') + '"'
                    cursor.execute(f"SELECT * FROM {quoted_table} LIMIT 3;")
                    rows = cursor.fetchall()
                    if rows:
                        col_names = [description[0] for description in cursor.description]
                        results.append(
                            f"/*\n3 rows from {table} table:\n"
                            + "\t".join(col_names)
                            + "\n"
                            + "\n".join("\t".join(str(x) for x in row) for row in rows)
                            + "\n*/"
                        )
                except Exception as e:
                    results.append(f"Error fetching sample rows: {e}")
        return "\n\n".join(results)
    finally:
        con.close()

@tool
def sql_db_query(query: str) -> str:
    """Input to this tool is a detailed and correct SQL query, output is a result from the database.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields."""
    con = sqlite3.connect("Chinook.db")
    try:
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        return str(res)
    except Exception as e:
        return f"Error: {e}"
    finally:
        con.close()

@tool
def sql_db_query_checker(query: str) -> str:
    """Use this tool to double check if your query is correct before executing it.
    Always use this tool before executing a query with sql_db_query!"""
    trigger_prompt = """{query}
Double check the sqlite query above for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

Output the final SQL query only.

SQL Query: """.format(query=query)

response = model.invoke(trigger_prompt)
return response.text.strip()

tools = [sql_db_list_tables, sql_db_schema, sql_db_query, sql_db_query_checker]

# Use a distinct loop variable so it does not shadow the `tool` decorator.
for t in tools:
    print(f"{t.name}: {t.description}\n")
```

```
sql_db_query: Input to this tool is a detailed and correct SQL query, output is a result from the database.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields.

sql_db_schema: Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables.
    Be sure that the tables actually exist by calling sql_db_list_tables first!
    Example Input: table1, table2, table3

sql_db_list_tables: Input is an empty string, output is a comma-separated list of tables in the database.

sql_db_query_checker: Use this tool to double check if your query is correct before executing it.
    Always use this tool before executing a query with sql_db_query!
```

**Create the agent**

Use `create_agent` to build a [ReAct agent](https://arxiv.org/pdf/2210.03629) with minimal code. The agent will interpret the request and generate a SQL command, which the tools will execute. If the command has an error, the error message is returned to the model. The model can then examine the original request and the new error message and generate a new command. This can continue until the LLM generates the command successfully or reaches an end count. This pattern of providing a model with feedback - error messages in this case - is very powerful.

Initialize the agent with a descriptive system prompt to customize its behavior:

```python
system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect="sqlite",
    top_k=5,
)
```

Now, create an agent with the model, tools, and prompt:

```python
from langchain.agents import create_agent

agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
)
```

**Run the agent**

Run the agent on a sample query and observe its behavior:

```python
question = "Which genre on average has the longest tracks?"

stream = agent.stream_events(
    {"messages": [{"role": "user", "content": question}]},
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output
```

```
================================ Human Message =================================

Which genre on average has the longest tracks?
================================== Ai Message ==================================
Tool Calls:
  sql_db_list_tables (call_BQsWg8P65apHc8BTJ1NPDvnM)
 Call ID: call_BQsWg8P65apHc8BTJ1NPDvnM
  Args:
================================= Tool Message =================================
Name: sql_db_list_tables

Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, MediaType, Playlist, PlaylistTrack, Track
================================== Ai Message ==================================
Tool Calls:
  sql_db_schema (call_i89tjKECFSeERbuACYm4w0cU)
 Call ID: call_i89tjKECFSeERbuACYm4w0cU
  Args:
    table_names: Track, Genre
================================= Tool Message =================================
Name: sql_db_schema

CREATE TABLE "Genre" (
	"GenreId" INTEGER NOT NULL,
	"Name" NVARCHAR(120),
	PRIMARY KEY ("GenreId")
)

/*
3 rows from Genre table:
GenreId	Name
1	Rock
2	Jazz
3	Metal
*/

CREATE TABLE "Track" (
	"TrackId" INTEGER NOT NULL,
	"Name" NVARCHAR(200) NOT NULL,
	"AlbumId" INTEGER,
	"MediaTypeId" INTEGER NOT NULL,
	"GenreId" INTEGER,
	"Composer" NVARCHAR(220),
	"Milliseconds" INTEGER NOT NULL,
	"Bytes" INTEGER,
	"UnitPrice" NUMERIC(10, 2) NOT NULL,
	PRIMARY KEY ("TrackId"),
	FOREIGN KEY("MediaTypeId") REFERENCES "MediaType" ("MediaTypeId"),
	FOREIGN KEY("GenreId") REFERENCES "Genre" ("GenreId"),
	FOREIGN KEY("AlbumId") REFERENCES "Album" ("AlbumId")
)

/*
3 rows from Track table:
TrackId	Name	AlbumId	MediaTypeId	GenreId	Composer	Milliseconds	Bytes	UnitPrice
1	For Those About To Rock (We Salute You)	1	1	1	Angus Young, Malcolm Young, Brian Johnson	343719	11170334	0.99
2	Balls to the Wall	2	2	1	U. Dirkschneider, W. Hoffmann, H. Frank, P. Baltes, S. Kaufmann, G. Hoffmann	342562	5510424	0.99
3	Fast As a Shark	3	2	1	F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman	230619	3990994	0.99
*/
================================== Ai Message ==================================
Tool Calls:
  sql_db_query_checker (call_G64yYm6R6UauiVPCXJZMA49b)
 Call ID: call_G64yYm6R6UauiVPCXJZMA49b
  Args:
    query: SELECT Genre.Name, AVG(Track.Milliseconds) AS AverageLength FROM Track INNER JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AverageLength DESC LIMIT 5;
================================= Tool Message =================================
Name: sql_db_query_checker

SELECT Genre.Name, AVG(Track.Milliseconds) AS AverageLength FROM Track INNER JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AverageLength DESC LIMIT 5;
================================== Ai Message ==================================
Tool Calls:
  sql_db_query (call_AnO3SrhD0ODJBxh6dHMwvHwZ)
 Call ID: call_AnO3SrhD0ODJBxh6dHMwvHwZ
  Args:
    query: SELECT Genre.Name, AVG(Track.Milliseconds) AS AverageLength FROM Track INNER JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AverageLength DESC LIMIT 5;
================================= Tool Message =================================
Name: sql_db_query

[('Sci Fi & Fantasy', 2911783.0384615385), ('Science Fiction', 2625549.076923077), ('Drama', 2575283.78125), ('TV Shows', 2145041.0215053763), ('Comedy', 1585263.705882353)]
================================== Ai Message ==================================

On average, the genre with the longest tracks is "Sci Fi & Fantasy" with an average track length of approximately 2,911,783 milliseconds. This is followed by "Science Fiction," "Drama," "TV Shows," and "Comedy."
```

The agent correctly wrote a query, checked the query, and ran it to inform its final response.

**Note:**

You can inspect all aspects of the above run, including steps taken, tools invoked, what prompts were seen by the LLM, and more in the [LangSmith trace](https://smith.langchain.com/public/cd2ce887-388a-4bb1-a29d-48208ce50d15/r).

**(Optional) Use Studio**

[Studio](/langsmith/studio) provides a "client side" loop as well as memory so you can run this as a chat interface and query the database. You can ask questions like "Tell me the scheme of the database" or "Show me the invoices for the 5 top customers". You will see the SQL command that is generated and the resulting output. The details of how to get that started are below.

**Run your agent in Studio**

In addition to the previously mentioned packages, you will need to:

```shell
pip install -U langgraph-cli[inmem]>=0.4.0
```

In directory you will run in, you will need a `langgraph.json` file with the following contents:

```json
{
  "dependencies": ["."],
  "graphs": {
      "agent": "./sql_agent.py:agent",
      "graph": "./sql_agent_langgraph.py:graph"
  },
  "env": ".env"
}
```

Create a file `sql_agent.py` and insert this:

```python
# sql_agent.py for studio
import pathlib
import sqlite3

import requests
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

# Initialize an LLM
model = init_chat_model("gpt-5.5")

# Get the database, store it locally
url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")

if local_path.exists():
    print(f"{local_path} already exists, skipping download.")
else:
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"File downloaded and saved as {local_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

# Below are minimal tools for demonstration purposes.

@tool
def sql_db_list_tables() -> str:
    """Input is an empty string, output is a comma-separated list of tables in the database."""
    con = sqlite3.connect("Chinook.db")
    try:
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]
        return ", ".join(tables)
    finally:
        con.close()

@tool
def sql_db_schema(table_names: str) -> str:
    """Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables.
    Be sure that the tables actually exist by calling sql_db_list_tables first!
    Example Input: table1, table2, table3"""
    con = sqlite3.connect("Chinook.db")
    try:
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        valid_tables = {row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")}
        results = []
        for table in table_names.split(","):
            table = table.strip()
            if table not in valid_tables:
                results.append(f"Error: table_names {{{table!r}}} not found in database")
                continue
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,))
            schema_row = cursor.fetchone()
            if schema_row:
                results.append(schema_row[0])
                try:
                    quoted_table = '"' + table.replace('"', '""') + '"'
                    cursor.execute(f"SELECT * FROM {quoted_table} LIMIT 3;")
                    rows = cursor.fetchall()
                    if rows:
                        col_names = [description[0] for description in cursor.description]
                        results.append(
                            f"/*\n3 rows from {table} table:\n"
                            + "\t".join(col_names)
                            + "\n"
                            + "\n".join("\t".join(str(x) for x in row) for row in rows)
                            + "\n*/"
                        )
                except Exception as e:
                    results.append(f"Error fetching sample rows: {e}")
        return "\n\n".join(results)
    finally:
        con.close()

@tool
def sql_db_query(query: str) -> str:
    """Input to this tool is a detailed and correct SQL query, output is a result from the database.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields."""
    con = sqlite3.connect("Chinook.db")
    try:
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        return str(res)
    except Exception as e:
        return f"Error: {e}"
    finally:
        con.close()

@tool
def sql_db_query_checker(query: str) -> str:
    """Use this tool to double check if your query is correct before executing it.
    Always use this tool before executing a query with sql_db_query!"""
    trigger_prompt = """{query}
Double check the sqlite query above for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

Output the final SQL query only.

SQL Query: """.format(query=query)

response = model.invoke(trigger_prompt)
return response.text.strip()

tools = [sql_db_list_tables, sql_db_schema, sql_db_query, sql_db_query_checker]

# Use a distinct loop variable so it does not shadow the `tool` decorator.
for t in tools:
    print(f"{t.name}: {t.description}\n")

# Use create_agent
system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect="sqlite",
    top_k=5,
)

agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
)
```

**Implement human-in-the-loop review**

It can be prudent to check the agent's SQL queries before they are executed for any unintended actions or inefficiencies.

LangChain agents feature support for built-in [human-in-the-loop middleware](/oss/langchain/human-in-the-loop) to add oversight to agent tool calls. Let's configure the agent to pause for human review on calling the `sql_db_query` tool:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware # [!code highlight]
from langgraph.checkpoint.memory import InMemorySaver # [!code highlight]

agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
    middleware=[ # [!code highlight]
        HumanInTheLoopMiddleware( # [!code highlight]
            interrupt_on={"sql_db_query": True}, # [!code highlight]
            description_prefix="Tool execution pending approval", # [!code highlight]
        ), # [!code highlight]
    ], # [!code highlight]
    checkpointer=InMemorySaver(), # [!code highlight]
)
```

**Note:**

We've added a [checkpointer](/oss/langchain/short-term-memory) to our agent to allow execution to be paused and resumed. See the [human-in-the-loop guide](/oss/langchain/human-in-the-loop) for detalis on this as well as available middleware configurations.

On running the agent, it will now pause for review before executing the `sql_db_query` tool:

```python
question = "Which genre on average has the longest tracks?"
config = {"configurable": {"thread_id": "1"}} # [!code highlight]

stream = agent.stream_events( # [!code highlight]
    {"messages": [{"role": "user", "content": question}]},
    config, # [!code highlight]
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
if stream.interrupted: # [!code highlight]
    print("INTERRUPTED:") # [!code highlight]
    interrupt = stream.interrupts[0] # [!code highlight]
    for request in interrupt.value["action_requests"]: # [!code highlight]
        print(request["description"]) # [!code highlight]
```

```
...

INTERRUPTED:
Tool execution pending approval

Tool: sql_db_query
Args: {'query': 'SELECT g.Name AS Genre, AVG(t.Milliseconds) AS AvgTrackLength FROM Track t JOIN Genre g ON t.GenreId = g.GenreId GROUP BY g.Name ORDER BY AvgTrackLength DESC LIMIT 1;'}
```
We can resume execution, in this case accepting the query, using [Command](/oss/langgraph/use-graph-api#combine-control-flow-and-state-updates-with-command):

```python
from langgraph.types import Command # [!code highlight]

stream = agent.stream_events( # [!code highlight]
    Command(resume={"decisions": [{"type": "approve"}]}), # [!code highlight]
    config,
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
if stream.interrupted:
    print("INTERRUPTED:")
    interrupt = stream.interrupts[0]
    for request in interrupt.value["action_requests"]:
        print(request["description"])
```

```
================================== Ai Message ==================================
Tool Calls:
  sql_db_query (call_7oz86Epg7lYRqi9rQHbZPS1U)
 Call ID: call_7oz86Epg7lYRqi9rQHbZPS1U
  Args:
    query: SELECT Genre.Name, AVG(Track.Milliseconds) AS AvgDuration FROM Track JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AvgDuration DESC LIMIT 5;
================================= Tool Message =================================
Name: sql_db_query

[('Sci Fi & Fantasy', 2911783.0384615385), ('Science Fiction', 2625549.076923077), ('Drama', 2575283.78125), ('TV Shows', 2145041.0215053763), ('Comedy', 1585263.705882353)]
================================== Ai Message ==================================

The genre with the longest average track length is "Sci Fi & Fantasy" with an average duration of about 2,911,783 milliseconds, followed by "Science Fiction" and "Drama."
```

Refer to the [human-in-the-loop guide](/oss/langchain/human-in-the-loop) for details.

## Next steps

For deeper customization, check out [this tutorial](/oss/langgraph/sql-agent) for implementing a SQL agent directly using LangGraph primitives.

---

# Streaming
> 출처: data/raw/langchain/streaming.mdx | https://docs.langchain.com/oss/python/langchain/streaming

Stream real-time updates from agent runs

**Tip:**

For new applications, we recommend [event streaming](/oss/langchain/event-streaming)—the typed-projection API introduced in LangChain v1.3. Event streaming gives you separate iterators per projection (messages, values, tool calls, subgraphs) so you can consume them independently instead of branching on `stream_mode` chunks.

LangChain implements a streaming system to surface real-time updates.

Streaming is crucial for enhancing the responsiveness of applications built on LLMs. By displaying output progressively, even before a complete response is ready, streaming significantly improves user experience (UX), particularly when dealing with the latency of LLMs.

## Overview

LangChain's streaming system lets you surface live feedback from agent runs to your application.

What's possible with LangChain streaming:

* 

 [**Stream agent progress**](#agent-progress)—get state updates after each agent step.
* 

 [**Stream LLM tokens**](#llm-tokens)—stream language model tokens as they're generated.
* 

 [**Stream thinking / reasoning tokens**](#streaming-thinking-/-reasoning-tokens)—surface model reasoning as it's generated.
* 

 [**Stream custom updates**](#custom-updates)—emit user-defined signals (e.g., `"Fetched 10/100 records"`).
* 

 [**Stream multiple modes**](#stream-multiple-modes)—choose from `updates` (agent progress), `messages` (LLM tokens + metadata), or `custom` (arbitrary user data).

See the [common patterns](#common-patterns) section below for additional end-to-end examples.

## Supported stream modes

Pass one or more of the following stream modes as a list to the `stream` or `astream` methods:

| Mode       | Description                                                                                                 |
| ---------- | ----------------------------------------------------------------------------------------------------------- |
| `updates`  | Streams state updates after each agent step. If multiple updates are made in the same step (e.g., multiple nodes are run), those updates are streamed separately. |
| `messages` | Streams tuples of `(token, metadata)` from any graph nodes where an LLM is invoked. |
| `custom`   | Streams custom data from inside your graph nodes using the stream writer. |

## Agent progress

To stream agent progress, use the `stream` or `astream` methods with `stream_mode="updates"`. This emits an event after every agent step.

For example, if you have an agent that calls a tool once, you should see the following updates:

* **LLM node**: `AIMessage` with tool call requests
* **Tool node**: `ToolMessage` with execution result
* **LLM node**: Final AI response

Pass a `thread_id` via `config` so the conversation is checkpointed and follow-up turns can resume the same history. `thread_id` is independent of `stream_mode`; you can also pass `context` alongside it for per-run data your tools read from `runtime.context`.

```python Google
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python OpenAI
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python Anthropic
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python OpenRouter
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python Fireworks
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python Baseten
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

```python Ollama
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[get_weather],
    checkpointer=InMemorySaver()
)
config = {"configurable": {"thread_id": str(uuid7())}}
stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for kind, item in stream.interleave("messages", "tool_calls"):  # [!code highlight]
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output  # [!code highlight]
```

- [View example trace](https://smith.langchain.com/public/9cd9423e-4fda-4987-bfc0-a5c4246a19eb/r)

  Open a public LangSmith run for this example.

```shell title="Output"
step: model
content: [{'type': 'tool_call', 'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_9lBtsDbmmobzyA8xc4I4Ctne'}]
step: tools
content: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]
step: model
content: [{'type': 'text', 'text': "San Francisco weather: It's always sunny in San Francisco!\n\nIf you’d like the exact current conditions (temperature, humidity, wind) and a short forecast, I can fetch that next. Would you like me to pull live details for San Francisco?"}]
```

**Note:**

Persisting conversation history with `thread_id` requires the agent to be configured with a [checkpointer](/oss/langchain/long-term-memory). On [LangSmith deployments](/langsmith/deployment) a checkpointer is provisioned automatically. Locally, pass one explicitly, for example `create_agent(..., checkpointer=InMemorySaver())`. The remaining snippets on this page omit `thread_id` for brevity, but you should pass it in production.

## LLM tokens

To stream tokens as they are produced by the LLM, use `stream_mode="messages"`. Below you can see the output of the agent streaming tool calls and the final response.

```python title="Streaming LLM tokens"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""

return f"It's always sunny in {city}!"

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
)
for chunk in agent.stream(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="messages",
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        print(f"node: {metadata['langgraph_node']}")
        print(f"content: {token.content_blocks}")
        print("\n")
```

```shell title="Output" expandable
node: model
content: [{'type': 'tool_call_chunk', 'id': 'call_vbCyBcP8VuneUzyYlSBZZsVa', 'name': 'get_weather', 'args': '', 'index': 0}]

node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '{"', 'index': 0}]

node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': 'city', 'index': 0}]

node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '":"', 'index': 0}]

node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': 'San', 'index': 0}]

node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': ' Francisco', 'index': 0}]

node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '"}', 'index': 0}]

node: model
content: []

node: tools
content: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]

node: model
content: []

node: model
content: [{'type': 'text', 'text': 'Here'}]

node: model
content: [{'type': 'text', 'text': ''s'}]

node: model
content: [{'type': 'text', 'text': ' what'}]

node: model
content: [{'type': 'text', 'text': ' I'}]

node: model
content: [{'type': 'text', 'text': ' got'}]

node: model
content: [{'type': 'text', 'text': ':'}]

node: model
content: [{'type': 'text', 'text': ' "'}]

node: model
content: [{'type': 'text', 'text': "It's"}]

node: model
content: [{'type': 'text', 'text': ' always'}]

node: model
content: [{'type': 'text', 'text': ' sunny'}]

node: model
content: [{'type': 'text', 'text': ' in'}]

node: model
content: [{'type': 'text', 'text': ' San'}]

node: model
content: [{'type': 'text', 'text': ' Francisco'}]

node: model
content: [{'type': 'text', 'text': '!"\n\n'}]
```

**Note:**

**Wrapping an agent as a node in a parent `StateGraph`?** `create_agent` returns a compiled graph, so using it as a node makes it a subgraph. `stream_mode="messages"` on the parent graph will not emit token chunks from the inner agent's LLM calls unless you pass `subgraphs=True`. See [Subgraph outputs](/oss/langgraph/streaming#subgraph-outputs).

## Custom updates

To stream updates from tools as they are executed, you can use `get_stream_writer`.

```python title="Streaming custom updates"
from langchain.agents import create_agent
from langgraph.config import get_stream_writer  # [!code highlight]

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    writer = get_stream_writer()  # [!code highlight]
    # stream any arbitrary data
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[get_weather],
)

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="custom",  # [!code highlight]
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "custom":  # [!code highlight]
        print(chunk["data"])  # [!code highlight]
```

```shell title="Output"
Looking up data for city: San Francisco
Acquired data for city: San Francisco
```

**Note:**

If you add `get_stream_writer` inside your tool, you won't be able to invoke the tool outside of a LangGraph execution context.

## Stream multiple modes

You can specify multiple streaming modes by passing stream mode as a list: `stream_mode=["updates", "custom"]`.

Each streamed chunk is a `StreamPart` dict with `type`, `ns`, and `data` keys. Use `chunk["type"]` to determine the stream mode and `chunk["data"]` to access the payload.

```python title="Streaming multiple modes"
from langchain.agents import create_agent
from langgraph.config import get_stream_writer

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    writer = get_stream_writer()
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
)

for chunk in agent.stream(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["updates", "custom"],
    version="v2",  # [!code highlight]
):
    print(f"stream_mode: {chunk['type']}")  # [!code highlight]
    print(f"content: {chunk['data']}")  # [!code highlight]
    print("\n")
```

```shell title="Output"
stream_mode: updates
content: {'model': {'messages': [AIMessage(content='', response_metadata={'token_usage': {'completion_tokens': 280, 'prompt_tokens': 132, 'total_tokens': 412, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 256, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-C9tlgBzGEbedGYxZ0rTCz5F7OXpL7', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--480c07cb-e405-4411-aa7f-0520fddeed66-0', tool_calls=[{'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_KTNQIftMrl9vgNwEfAJMVu7r', 'type': 'tool_call'}], usage_metadata={'input_tokens': 132, 'output_tokens': 280, 'total_tokens': 412, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 256}})]}}

stream_mode: custom
content: Looking up data for city: San Francisco

stream_mode: custom
content: Acquired data for city: San Francisco

stream_mode: updates
content: {'tools': {'messages': [ToolMessage(content="It's always sunny in San Francisco!", name='get_weather', tool_call_id='call_KTNQIftMrl9vgNwEfAJMVu7r')]}}

stream_mode: updates
content: {'model': {'messages': [AIMessage(content='San Francisco weather: It's always sunny in San Francisco!\n\n', response_metadata={'token_usage': {'completion_tokens': 764, 'prompt_tokens': 168, 'total_tokens': 932, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 704, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-C9tljDFVki1e1haCyikBptAuXuHYG', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--acbc740a-18fe-4a14-8619-da92a0d0ee90-0', usage_metadata={'input_tokens': 168, 'output_tokens': 764, 'total_tokens': 932, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 704}})]}}
```

## Common patterns

Below are examples showing common use cases for streaming.

### Streaming thinking / reasoning tokens

Some models perform internal reasoning before producing a final answer. You can stream these thinking / reasoning tokens as they're generated by filtering [standard content blocks](/oss/langchain/messages#standard-content-blocks) for the `type` `"reasoning"`.

**Note:**

Reasoning output must be enabled on the model.

See the [reasoning section](/oss/langchain/models#reasoning) and your [provider's integration page](/oss/integrations/providers/overview) for configuration details.

To quickly check a model's reasoning support, see [models.dev](https://models.dev).

To stream thinking tokens from an agent, use `stream_mode="messages"` and filter for reasoning content blocks:

```python
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.runnables import Runnable

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

model = ChatAnthropic(
    model_name="claude-sonnet-4-6",
    timeout=None,
    stop=None,
    thinking={"type": "enabled", "budget_tokens": 5000},
)
agent: Runnable = create_agent(
    model=model,
    tools=[get_weather],
)

stream = agent.stream_events(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    version="v3",
)
for message in stream.messages:
    for token in message.reasoning:
        print(f"[thinking] {token}", end="")
    for token in message.text:
        print(token, end="", flush=True)
```

- [View example trace](https://smith.langchain.com/public/cce5483a-c5fd-4e08-94dc-12b510c6ccf1/r)

  Open a public LangSmith run for this example.

```shell title="Output"
[thinking] The user is asking about the weather in San Francisco. I have a tool
[thinking]  available to get this information. Let me call the get_weather tool
[thinking]  with "San Francisco" as the city parameter.
The weather in San Francisco is: It's always sunny in San Francisco!
```

This works the same way regardless of the model provider—LangChain normalizes provider-specific formats (Anthropic `thinking` blocks, OpenAI `reasoning` summaries, etc.) into a standard `"reasoning"` content block type via the [`content_blocks`](/oss/langchain/messages#standard-content-blocks) property.

To stream reasoning tokens directly from a chat model (without an agent), see [streaming with chat models](/oss/langchain/models#reasoning).

### Streaming tool calls

You may want to stream both:

1. Partial JSON as [tool calls](/oss/langchain/models#tool-calling) are generated
2. The completed, parsed tool calls that are executed

Specifying [`stream_mode="messages"`](#llm-tokens) will stream incremental [message chunks](/oss/langchain/messages#streaming-and-chunks) generated by all LLM calls in the agent. To access the completed messages with parsed tool calls:

1. If those messages are tracked in the [state](/oss/langchain/short-term-memory) (as in the model node of [`create_agent`](/oss/langchain/agents)), use `stream_mode=["messages", "updates"]` to access completed messages through [state updates](#agent-progress) (demonstrated below).
2. If those messages are not tracked in the state, use [custom updates](#custom-updates) or aggregate the chunks during the streaming loop ([next section](#accessing-completed-messages)).

**Note:**

Refer to the section below on [streaming from sub-agents](#streaming-from-sub-agents) if your agent includes multiple LLMs.

```python
from typing import Any

from langchain.agents import create_agent
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage

def get_weather(city: str) -> str:
    """Get weather for a given city."""

return f"It's always sunny in {city}!"

agent = create_agent("openai:gpt-5.5", tools=[get_weather])

def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)
    # N.B. all content is available through token.content_blocks

def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")

input_message = {"role": "user", "content": "What is the weather in Boston?"}
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],  # [!code highlight]
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)  # [!code highlight]
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source in ("model", "tools"):  # `source` captures node name
                _render_completed_message(update["messages"][-1])  # [!code highlight]
```
```shell title="Output" expandable
[{'name': 'get_weather', 'args': '', 'id': 'call_D3Orjr89KgsLTZ9hTzYv7Hpf', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'city', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_D3Orjr89KgsLTZ9hTzYv7Hpf', 'type': 'tool_call'}]
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston!"}]
The| weather| in| Boston| is| **|sun|ny|**|.|
```

#### Accessing completed messages

**Note:**

If completed messages are tracked in an agent's [state](/oss/langchain/short-term-memory), you can use `stream_mode=["messages", "updates"]` as demonstrated in the [Streaming tool calls](#streaming-tool-calls) section to access completed messages during streaming.

In some cases, completed messages are not reflected in [state updates](#agent-progress). If you have access to the agent internals, you can use [custom updates](#custom-updates) to access these messages during streaming. Otherwise, you can aggregate message chunks in the streaming loop (see below).

Consider the below example, where we incorporate a [stream writer](#custom-updates) into a simplified [guardrail middleware](/oss/langchain/guardrails#after-agent-guardrails). This middleware demonstrates tool calling to generate a structured "safe / unsafe" evaluation (one could also use [structured outputs](/oss/langchain/models#structured-output) for this):
```python
from typing import Any, Literal

from langchain.agents.middleware import after_agent, AgentState
from langgraph.runtime import Runtime
from langchain.messages import AIMessage
from langchain.chat_models import init_chat_model
from langgraph.config import get_stream_writer  # [!code highlight]
from pydantic import BaseModel

class ResponseSafety(BaseModel):
    """Evaluate a response as safe or unsafe."""
    evaluation: Literal["safe", "unsafe"]

safety_model = init_chat_model("openai:gpt-5.5")

@after_agent(can_jump_to=["end"])
def safety_guardrail(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Model-based guardrail: Use an LLM to evaluate response safety."""
    stream_writer = get_stream_writer()  # [!code highlight]
    # Get the model response
    if not state["messages"]:
        return None

last_message = state["messages"][-1]
if not isinstance(last_message, AIMessage):
    return None

# Use another model to evaluate safety
model_with_tools = safety_model.bind_tools([ResponseSafety], tool_choice="any")
result = model_with_tools.invoke(
    [
        {
            "role": "system",
            "content": "Evaluate this AI response as generally safe or unsafe."
        },
        {
            "role": "user",
            "content": f"AI response: {last_message.text}"
        }
    ]
)
stream_writer(result)  # [!code highlight]

tool_call = result.tool_calls[0]
if tool_call["args"]["evaluation"] == "unsafe":
    last_message.content = "I cannot provide that response. Please rephrase your request."

    return None
```
We can then incorporate this middleware into our agent and include its custom stream events:
```python
from typing import Any

from langchain.agents import create_agent
from langchain.messages import AIMessageChunk, AIMessage, AnyMessage

def get_weather(city: str) -> str:
    """Get weather for a given city."""

return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[get_weather],
    middleware=[safety_guardrail],  # [!code highlight]
)

def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)

def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")

input_message = {"role": "user", "content": "What is the weather in Boston?"}
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates", "custom"],  # [!code highlight]
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
    elif chunk["type"] == "custom":  # [!code highlight]
        # access completed message in stream
        print(f"Tool calls: {chunk['data'].tool_calls}")  # [!code highlight]
```
```shell title="Output" expandable
[{'name': 'get_weather', 'args': '', 'id': 'call_je6LWgxYzuZ84mmoDalTYMJC', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'city', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_je6LWgxYzuZ84mmoDalTYMJC', 'type': 'tool_call'}]
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston!"}]
The| weather| in| **|Boston|**| is| **|sun|ny|**|.|[{'name': 'ResponseSafety', 'args': '', 'id': 'call_O8VJIbOG4Q9nQF0T8ltVi58O', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'evaluation', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'safe', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'ResponseSafety', 'args': {'evaluation': 'safe'}, 'id': 'call_O8VJIbOG4Q9nQF0T8ltVi58O', 'type': 'tool_call'}]
```

Alternatively, if you aren't able to add custom events to the stream, you can aggregate message chunks within the streaming loop:
```python
input_message = {"role": "user", "content": "What is the weather in Boston?"}
full_message = None  # [!code highlight]
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
            full_message = token if full_message is None else full_message + token  # [!code highlight]
            if token.chunk_position == "last":  # [!code highlight]
                if full_message.tool_calls:  # [!code highlight]
                    print(f"Tool calls: {full_message.tool_calls}")  # [!code highlight]
                full_message = None  # [!code highlight]
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source == "tools":
                _render_completed_message(update["messages"][-1])
```

### Streaming with human-in-the-loop

To handle human-in-the-loop [interrupts](/oss/langchain/human-in-the-loop), we build on the [above example](#streaming-tool-calls):

1. We configure the agent with [human-in-the-loop middleware and a checkpointer](/oss/langchain/human-in-the-loop#configuring-interrupts)
2. We collect interrupts generated during the `"updates"` stream mode
3. We respond to those interrupts with a [command](/oss/langchain/human-in-the-loop#responding-to-interrupts)

```python
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, Interrupt

def get_weather(city: str) -> str:
    """Get weather for a given city."""

return f"It's always sunny in {city}!"

checkpointer = InMemorySaver()

agent = create_agent(
    "openai:gpt-5.5",
    tools=[get_weather],
    middleware=[  # [!code highlight]
        HumanInTheLoopMiddleware(interrupt_on={"get_weather": True}),  # [!code highlight]
    ],  # [!code highlight]
    checkpointer=checkpointer,  # [!code highlight]
)

def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)

def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")

def _render_interrupt(interrupt: Interrupt) -> None:  # [!code highlight]
    interrupts = interrupt.value  # [!code highlight]
    for request in interrupts["action_requests"]:  # [!code highlight]
        print(request["description"])  # [!code highlight]

input_message = {
    "role": "user",
    "content": (
        "Can you look up the weather in Boston and San Francisco?"
    ),
}
config = {"configurable": {"thread_id": "some_id"}}  # [!code highlight]
interrupts = []  # [!code highlight]
for chunk in agent.stream(
    {"messages": [input_message]},
    config=config,  # [!code highlight]
    stream_mode=["messages", "updates"],
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
            if source == "__interrupt__":  # [!code highlight]
                interrupts.extend(update)  # [!code highlight]
                _render_interrupt(update[0])  # [!code highlight]
```
```shell title="Output" expandable
[{'name': 'get_weather', 'args': '', 'id': 'call_GOwNaQHeqMixay2qy80padfE', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"ci', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'ty": ', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"Bosto', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'n"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': 'get_weather', 'args': '', 'id': 'call_Ndb4jvWm2uMA0JDQXu37wDH6', 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"ci', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'ty": ', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"San F', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'ranc', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'isco"', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '}', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_GOwNaQHeqMixay2qy80padfE', 'type': 'tool_call'}, {'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_Ndb4jvWm2uMA0JDQXu37wDH6', 'type': 'tool_call'}]
Tool execution requires approval

Tool: get_weather
Args: {'city': 'Boston'}
Tool execution requires approval

Tool: get_weather
Args: {'city': 'San Francisco'}
```

We next collect a [decision](/oss/langchain/human-in-the-loop#interrupt-decision-types) for each interrupt. Importantly, the order of decisions must match the order of actions we collected.

To illustrate, we will edit one tool call and accept the other:
```python
def _get_interrupt_decisions(interrupt: Interrupt) -> list[dict]:
    return [
        {
            "type": "edit",
            "edited_action": {
                "name": "get_weather",
                "args": {"city": "Boston, U.K."},
            },
        }
        if "boston" in request["description"].lower()
        else {"type": "approve"}
        for request in interrupt.value["action_requests"]
    ]

decisions = {}
for interrupt in interrupts:
    decisions[interrupt.id] = {
        "decisions": _get_interrupt_decisions(interrupt)
    }

decisions
```
```shell title="Output"
{
    'a96c40474e429d661b5b32a8d86f0f3e': {
        'decisions': [
            {
                'type': 'edit',
                 'edited_action': {
                     'name': 'get_weather',
                     'args': {'city': 'Boston, U.K.'}
                 }
            },
            {'type': 'approve'},
        ]
    }
}
```

We can then resume by passing a [command](/oss/langchain/human-in-the-loop#responding-to-interrupts) into the same streaming loop:
```python
interrupts = []
for chunk in agent.stream(
    Command(resume=decisions),  # [!code highlight]
    config=config,
    stream_mode=["messages", "updates"],
    version="v2",  # [!code highlight]
):
    # Streaming loop is unchanged
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
            if source == "__interrupt__":
                interrupts.extend(update)
                _render_interrupt(update[0])
```
```shell title="Output"
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston, U.K.!"}]
Tool response: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]
-| **|Boston|**|:| It|'s| always| sunny| in| Boston|,| U|.K|.|
|-| **|San| Francisco|**|:| It|'s| always| sunny| in| San| Francisco|!|
```

### Streaming from sub-agents

When there are multiple LLMs at any point in an agent, it's often necessary to disambiguate the source of messages as they are generated.

To do this, pass a [`name`](https://reference.langchain.com/python/langchain/agents/create_agent) to each agent when creating it. This name is then available in metadata via the `lc_agent_name` key when streaming in `"messages"` mode.

Below, we update the [streaming tool calls](#streaming-tool-calls) example:

1. We replace our tool with a `call_weather_agent` tool that invokes an agent internally
2. We add a `name` to each agent
3. We specify [`subgraphs=True`](/oss/langgraph/use-subgraphs#stream-subgraph-outputs) when creating the stream
4. Our stream processing is identical to before, but we add logic to keep track of what agent is active using `create_agent`'s `name` parameter

**Tip:**

When you set a `name` on an agent, that name is also attached to any `AIMessage`s generated by that agent.

First we construct the agent:
```python
from typing import Any

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AnyMessage

def get_weather(city: str) -> str:
    """Get weather for a given city."""

return f"It's always sunny in {city}!"

weather_model = init_chat_model("openai:gpt-5.5")
weather_agent = create_agent(
    model=weather_model,
    tools=[get_weather],
    name="weather_agent",  # [!code highlight]
)

def call_weather_agent(query: str) -> str:
    """Query the weather agent."""
    result = weather_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"][-1].text

supervisor_model = init_chat_model("openai:gpt-5.5")
agent = create_agent(
    model=supervisor_model,
    tools=[call_weather_agent],
    name="supervisor",  # [!code highlight]
)
```
Next, we add logic to the streaming loop to report which agent is emitting tokens:
```python
def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)

def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")

input_message = {"role": "user", "content": "What is the weather in Boston?"}
current_agent = None  # [!code highlight]
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],
    subgraphs=True,  # [!code highlight]
    version="v2",  # [!code highlight]
):
    if chunk["type"] == "messages":  # [!code highlight]
        token, metadata = chunk["data"]  # [!code highlight]
        if agent_name := metadata.get("lc_agent_name"):  # [!code highlight]
            if agent_name != current_agent:  # [!code highlight]
                print(f"🤖 {agent_name}: ")  # [!code highlight]
                current_agent = agent_name  # [!code highlight]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":  # [!code highlight]
        for source, update in chunk["data"].items():  # [!code highlight]
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
```
```shell title="Output" expandable
🤖 supervisor:
[{'name': 'call_weather_agent', 'args': '', 'id': 'call_asorzUf0mB6sb7MiKfgojp7I', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'query', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' weather', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' right', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' now', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' and', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': " today's", 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' forecast', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'call_weather_agent', 'args': {'query': "Boston weather right now and today's forecast"}, 'id': 'call_asorzUf0mB6sb7MiKfgojp7I', 'type': 'tool_call'}]
🤖 weather_agent:
[{'name': 'get_weather', 'args': '', 'id': 'call_LZ89lT8fW6w8vqck5pZeaDIx', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'city', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_LZ89lT8fW6w8vqck5pZeaDIx', 'type': 'tool_call'}]
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston!"}]
Boston| weather| right| now|:| **|Sunny|**|.

|Today|'s| forecast| for| Boston|:| **|Sunny| all| day|**|.|Tool response: [{'type': 'text', 'text': 'Boston weather right now: **Sunny**.\n\nToday's forecast for Boston: **Sunny all day**.'}]
🤖 supervisor:
Boston| weather| right| now|:| **|Sunny|**|.

|Today|'s| forecast| for| Boston|:| **|Sunny| all| day|**|.|
```

## Disable streaming

In some applications you might need to disable streaming of individual tokens for a given model. This is useful when:

- Working with [multi-agent](/oss/langchain/multi-agent) systems to control which agents stream their output
- Mixing models that support streaming with those that do not
- Deploying to [LangSmith](/langsmith/observability) and wanting to prevent certain model outputs from being streamed to the client

Set `streaming=False` when initializing the model.

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-5.5",
    streaming=False  # [!code highlight]
)
```

**Tip:**

When deploying to LangSmith, set `streaming=False` on any models whose output you don't want streamed to the client. This is configured in your graph code before deployment.

**Note:**

Not all chat model integrations support the `streaming` parameter. If your model doesn't support it, use `disable_streaming=True` instead. This parameter is available on all chat models via the base class.

See the [LangGraph streaming guide](/oss/langgraph/streaming#disable-streaming-for-specific-chat-models) for more details.

## v2 streaming format

**Note:**

Requires LangGraph 1.1 or later.

Pass `version="v2"` to `stream()` or `astream()` to get a unified output format. Every chunk is a `StreamPart` dict with `type`, `ns`, and `data` keys — the same shape regardless of stream mode or number of modes:

```python v2 (new)
# Unified format — no more tuple unpacking
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["updates", "custom"],
    version="v2",
):
    print(chunk["type"])  # "updates" or "custom"
    print(chunk["data"])  # payload
```
```python v1 (current default)
# Must unpack (mode, data) tuples
for mode, chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["updates", "custom"],
):
    print(mode)   # "updates" or "custom"
    print(chunk)  # payload
```

The v2 format also improves `invoke()` — it returns a `GraphOutput` object with `.value` and `.interrupts` attributes, cleanly separating state from interrupt metadata:

```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Hello"}]},
    version="v2",
)
print(result.value)       # state (dict, Pydantic model, or dataclass)
print(result.interrupts)  # tuple of Interrupt objects (empty if none)
```

See the [LangGraph streaming docs](/oss/langgraph/streaming#stream-output-format-v2) for more details on the v2 format, including type narrowing, Pydantic/dataclass coercion, and subgraph streaming.

## Related

- [Frontend streaming](/oss/langchain/frontend/overview)—Build React UIs with `useStream` for real-time agent interactions
- [Streaming with chat models](/oss/langchain/models#stream)—Stream tokens directly from a chat model without using an agent or graph
- [Reasoning with chat models](/oss/langchain/models#reasoning)—Configure and access reasoning output from chat models
- [Standard content blocks](/oss/langchain/messages#standard-content-blocks)—Understand the normalized content block format used for reasoning, text, and other content types
- [Streaming with human-in-the-loop](/oss/langchain/human-in-the-loop#streaming-with-human-in-the-loop)—Stream agent progress while handling interrupts for human review
- [LangGraph streaming](/oss/langgraph/streaming)—Advanced streaming options including `values`, `debug` modes, and subgraph streaming

---

# Structured output
> 출처: data/raw/langchain/structured-output.mdx | https://docs.langchain.com/oss/python/langchain/structured-output

Structured output allows agents to return data in a specific, predictable format. Instead of parsing natural language responses, you get structured data in the form of JSON objects, [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage), or dataclasses that your application can use directly.

**Tip:**

This page covers structured output with agents using `create_agent`. To use structured output directly on a model (outside of agents), see [Models - Structured output](/oss/langchain/models#structured-output).

LangChain's `create_agent` handles structured output automatically. The user sets their desired structured output schema, and when the model generates the structured data, it's captured, validated, and returned in the `'structured_response'` key of the agent's state.

```python
def create_agent(
    ...
    response_format: Union[
        ToolStrategy[StructuredResponseT],
        ProviderStrategy[StructuredResponseT],
        type[StructuredResponseT],
        None,
    ]
)
```

## Response format

Use `response_format` to control how the agent returns structured data:

- **`ToolStrategy[StructuredResponseT]`**: Uses tool calling for structured output
- **`ProviderStrategy[StructuredResponseT]`**: Uses provider-native structured output
- **`type[StructuredResponseT]`**: Schema type - automatically selects best strategy based on model capabilities
- **`None`**: Structured output not explicitly requested

When a schema type is provided directly, LangChain automatically chooses:

- `ProviderStrategy` if the model and provider chosen supports native structured output (e.g. [OpenAI](/oss/integrations/providers/openai), [Anthropic (Claude)](/oss/integrations/providers/anthropic), or [xAI (Grok)](/oss/integrations/providers/xai)).
- `ToolStrategy` for all other models.

**Warning:**

JSON Schema dictionaries must be wrapped in an explicit strategy (`ProviderStrategy` or `ToolStrategy`). They are not automatically detected when passed directly to `response_format`.

**Note:**

Support for native structured output features is read dynamically from the model's [profile data](/oss/langchain/models#model-profiles) if using `langchain>=1.1`. If data are not available, use another condition or specify manually:
```python
custom_profile = {
    "structured_output": True,
    # ...
}
model = init_chat_model("...", profile=custom_profile)
```
If tools are specified, the model must support simultaneous use of tools and structured output.

The structured response is returned in the `structured_response` key of the agent's final state.

## Provider strategy

Some model providers support structured output natively through their APIs (e.g. OpenAI, xAI (Grok), Gemini, Anthropic (Claude)). This is the most reliable method when available.

To use this strategy, configure a `ProviderStrategy`:

```python
class ProviderStrategy(Generic[SchemaT]):
    schema: type[SchemaT]
    strict: bool | None = None
```

**Info:**

The `strict` param requires `langchain>=1.2`.

The schema defining the structured output format. Supports:
- **Pydantic models**: `BaseModel` subclasses with field validation. Returns validated Pydantic instance.
- **Dataclasses**: Python dataclasses with type annotations. Returns dict.
- **TypedDict**: Typed dictionary classes. Returns dict.
- **JSON Schema**: Dictionary with JSON schema specification. Must include top-level `title` and `description` keys. Returns dict.

    Optional boolean parameter to enable strict schema adherence. Supported by some providers (e.g., [OpenAI](/oss/integrations/chat/openai) and [xAI](/oss/integrations/chat/xai)). Defaults to `None` (disabled).

LangChain automatically uses `ProviderStrategy` when you pass a schema type directly to `create_agent.response_format` and the model supports native structured output:

```python Pydantic Model
from pydantic import BaseModel, Field
from langchain.agents import create_agent

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")

agent = create_agent(
    model="gpt-5.5",
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

print(result["structured_response"])
# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
```

```python Dataclass
from dataclasses import dataclass
from langchain.agents import create_agent

@dataclass
class ContactInfo:
    """Contact information for a person."""
    name: str # The name of the person
    email: str # The email address of the person
    phone: str # The phone number of the person

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

result["structured_response"]
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}
```

```python TypedDict
from typing_extensions import TypedDict
from langchain.agents import create_agent

class ContactInfo(TypedDict):
    """Contact information for a person."""
    name: str # The name of the person
    email: str # The email address of the person
    phone: str # The phone number of the person

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

result["structured_response"]
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}
```

```python JSON Schema
from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy

contact_info_schema = {
    "title": "ContactInfo",
    "type": "object",
    "description": "Contact information for a person.",
    "properties": {
        "name": {"type": "string", "description": "The name of the person"},
        "email": {"type": "string", "description": "The email address of the person"},
        "phone": {"type": "string", "description": "The phone number of the person"}
    },
    "required": ["name", "email", "phone"]
}

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ProviderStrategy(contact_info_schema)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

result["structured_response"]
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}
```

Provider-native structured output provides high reliability and strict validation because the model provider enforces the schema. Use it when available.

**Note:**

If the provider natively supports structured output for your model choice, it is functionally equivalent to write `response_format=ProductReview` instead of `response_format=ProviderStrategy(ProductReview)`.

In either case, if structured output is not supported, the agent will fall back to a tool calling strategy.

## Tool calling strategy

For models that don't support native structured output, LangChain uses tool calling to achieve the same result. This works with all models that support tool calling (most modern models).

To use this strategy, configure a `ToolStrategy`:

```python
class ToolStrategy(Generic[SchemaT]):
    schema: type[SchemaT]
    tool_message_content: str | None
    handle_errors: Union[
        bool,
        str,
        type[Exception],
        tuple[type[Exception], ...],
        Callable[[Exception], str],
    ]
```

The schema defining the structured output format. Supports:
- **Pydantic models**: `BaseModel` subclasses with field validation. Returns validated Pydantic instance.
- **Dataclasses**: Python dataclasses with type annotations. Returns dict.
- **TypedDict**: Typed dictionary classes. Returns dict.
- **JSON Schema**: Dictionary with JSON schema specification. Must include top-level `title` and `description` keys. Returns dict.
- **Union types**: Multiple schema options. The model will choose the most appropriate schema based on the context.

    Custom content for the tool message returned when structured output is generated.
    If not provided, defaults to a message showing the structured response data.

Error handling strategy for structured output validation failures. Defaults to `True`.

- **`True`**: Catch all errors with default error template
- **`str`**: Catch all errors with this custom message
- **`type[Exception]`**: Only catch this exception type with default message
- **`tuple[type[Exception], ...]`**: Only catch these exception types with default message
- **`Callable[[Exception], str]`**: Custom function that returns error message
- **`False`**: No retry, let exceptions propagate

    ```python Pydantic Model
    from pydantic import BaseModel, Field
    from typing import Literal
    from langchain.agents import create_agent
    from langchain.agents.structured_output import ToolStrategy

class ProductReview(BaseModel):
    """Analysis of a product review."""
    rating: int | None = Field(description="The rating of the product", ge=1, le=5)
    sentiment: Literal["positive", "negative"] = Field(description="The sentiment of the review")
    key_points: list[str] = Field(description="The key points of the review. Lowercase, 1-3 words each.")

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ToolStrategy(ProductReview)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
result["structured_response"]
# ProductReview(rating=5, sentiment='positive', key_points=['fast shipping', 'expensive'])
```

```python Dataclass
from dataclasses import dataclass
from typing import Literal
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

@dataclass
class ProductReview:
    """Analysis of a product review."""
    rating: int | None  # The rating of the product (1-5)
    sentiment: Literal["positive", "negative"]  # The sentiment of the review
    key_points: list[str]  # The key points of the review

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ToolStrategy(ProductReview)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
result["structured_response"]
# {'rating': 5, 'sentiment': 'positive', 'key_points': ['fast shipping', 'expensive']}
```

```python TypedDict
from typing import Literal
from typing_extensions import TypedDict
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

class ProductReview(TypedDict):
    """Analysis of a product review."""
    rating: int | None  # The rating of the product (1-5)
    sentiment: Literal["positive", "negative"]  # The sentiment of the review
    key_points: list[str]  # The key points of the review

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ToolStrategy(ProductReview)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
result["structured_response"]
# {'rating': 5, 'sentiment': 'positive', 'key_points': ['fast shipping', 'expensive']}
```

```python JSON Schema
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

product_review_schema = {
    "title": "ProductReview",
    "type": "object",
    "description": "Analysis of a product review.",
    "properties": {
        "rating": {
            "type": ["integer", "null"],
            "description": "The rating of the product (1-5)",
            "minimum": 1,
            "maximum": 5
        },
        "sentiment": {
            "type": "string",
            "enum": ["positive", "negative"],
            "description": "The sentiment of the review"
        },
        "key_points": {
            "type": "array",
            "items": {"type": "string"},
            "description": "The key points of the review"
        }
    },
    "required": ["sentiment", "key_points"]
}

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ToolStrategy(product_review_schema)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
result["structured_response"]
# {'rating': 5, 'sentiment': 'positive', 'key_points': ['fast shipping', 'expensive']}
```

```python Union Types
from pydantic import BaseModel, Field
from typing import Literal, Union
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

class ProductReview(BaseModel):
    """Analysis of a product review."""
    rating: int | None = Field(description="The rating of the product", ge=1, le=5)
    sentiment: Literal["positive", "negative"] = Field(description="The sentiment of the review")
    key_points: list[str] = Field(description="The key points of the review. Lowercase, 1-3 words each.")

class CustomerComplaint(BaseModel):
    """A customer complaint about a product or service."""
    issue_type: Literal["product", "service", "shipping", "billing"] = Field(description="The type of issue")
    severity: Literal["low", "medium", "high"] = Field(description="The severity of the complaint")
    description: str = Field(description="Brief description of the complaint")

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ToolStrategy(Union[ProductReview, CustomerComplaint])
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
result["structured_response"]
# ProductReview(rating=5, sentiment='positive', key_points=['fast shipping', 'expensive'])
```

### Custom tool message content

The `tool_message_content` parameter allows you to customize the message that appears in the conversation history when structured output is generated:

```python
from pydantic import BaseModel, Field
from typing import Literal
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

class MeetingAction(BaseModel):
    """Action items extracted from a meeting transcript."""
    task: str = Field(description="The specific task to be completed")
    assignee: str = Field(description="Person responsible for the task")
    priority: Literal["low", "medium", "high"] = Field(description="Priority level")

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ToolStrategy(
        schema=MeetingAction,
        tool_message_content="Action item captured and added to meeting notes!"
    )
)

agent.invoke({
    "messages": [{"role": "user", "content": "From our meeting: Sarah needs to update the project timeline as soon as possible"}]
})
```

```
================================ Human Message =================================

From our meeting: Sarah needs to update the project timeline as soon as possible
================================== Ai Message ==================================
Tool Calls:
  MeetingAction (call_1)
 Call ID: call_1
  Args:
    task: Update the project timeline
    assignee: Sarah
    priority: high
================================= Tool Message =================================
Name: MeetingAction

Action item captured and added to meeting notes!
```

Without `tool_message_content`, our final `ToolMessage` would be:
```
================================= Tool Message =================================
Name: MeetingAction

Returning structured response: {'task': 'update the project timeline', 'assignee': 'Sarah', 'priority': 'high'}
```

### Error handling

Models can make mistakes when generating structured output via tool calling. LangChain provides intelligent retry mechanisms to handle these errors automatically.

#### Multiple structured outputs error

When a model incorrectly calls multiple structured output tools, the agent provides error feedback in a `ToolMessage` and prompts the model to retry:

```python
from pydantic import BaseModel, Field
from typing import Union
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

class ContactInfo(BaseModel):
    name: str = Field(description="Person's name")
    email: str = Field(description="Email address")

class EventDetails(BaseModel):
    event_name: str = Field(description="Name of the event")
    date: str = Field(description="Event date")

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ToolStrategy(Union[ContactInfo, EventDetails])  # Default: handle_errors=True
)

agent.invoke({
    "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]
})
```

```
================================ Human Message =================================

Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th
None
================================== Ai Message ==================================
Tool Calls:
  ContactInfo (call_1)
 Call ID: call_1
  Args:
    name: John Doe
    email: john@email.com
  EventDetails (call_2)
 Call ID: call_2
  Args:
    event_name: Tech Conference
    date: March 15th
================================= Tool Message =================================
Name: ContactInfo

Error: Model incorrectly returned multiple structured responses (ContactInfo, EventDetails) when only one is expected.
 Please fix your mistakes.
================================= Tool Message =================================
Name: EventDetails

Error: Model incorrectly returned multiple structured responses (ContactInfo, EventDetails) when only one is expected.
 Please fix your mistakes.
================================== Ai Message ==================================
Tool Calls:
  ContactInfo (call_3)
 Call ID: call_3
  Args:
    name: John Doe
    email: john@email.com
================================= Tool Message =================================
Name: ContactInfo

Returning structured response: {'name': 'John Doe', 'email': 'john@email.com'}
```

#### Schema validation error

When structured output doesn't match the expected schema, the agent provides specific error feedback:

```python
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

class ProductRating(BaseModel):
    rating: int | None = Field(description="Rating from 1-5", ge=1, le=5)
    comment: str = Field(description="Review comment")

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ToolStrategy(ProductRating),  # Default: handle_errors=True
    system_prompt="You are a helpful assistant that parses product reviews. Do not make any field or value up."
)

agent.invoke({
    "messages": [{"role": "user", "content": "Parse this: Amazing product, 10/10!"}]
})
```

```
================================ Human Message =================================

Parse this: Amazing product, 10/10!
================================== Ai Message ==================================
Tool Calls:
  ProductRating (call_1)
 Call ID: call_1
  Args:
    rating: 10
    comment: Amazing product
================================= Tool Message =================================
Name: ProductRating

Error: Failed to parse structured output for tool 'ProductRating': 1 validation error for ProductRating.rating
  Input should be less than or equal to 5 [type=less_than_equal, input_value=10, input_type=int].
 Please fix your mistakes.
================================== Ai Message ==================================
Tool Calls:
  ProductRating (call_2)
 Call ID: call_2
  Args:
    rating: 5
    comment: Amazing product
================================= Tool Message =================================
Name: ProductRating

Returning structured response: {'rating': 5, 'comment': 'Amazing product'}
```

#### Error handling strategies

You can customize how errors are handled using the `handle_errors` parameter:

**Custom error message:**
```python
ToolStrategy(
    schema=ProductRating,
    handle_errors="Please provide a valid rating between 1-5 and include a comment."
)
```
If `handle_errors` is a string, the agent will *always* prompt the model to re-try with a fixed tool message:
```
================================= Tool Message =================================
Name: ProductRating

Please provide a valid rating between 1-5 and include a comment.
```

**Handle specific exceptions only:**

```python
ToolStrategy(
    schema=ProductRating,
    handle_errors=ValueError  # Only retry on ValueError, raise others
)
```

If `handle_errors` is an exception type, the agent will only retry (using the default error message) if the exception raised is the specified type. In all other cases, the exception will be raised.

**Handle multiple exception types:**
```python
ToolStrategy(
    schema=ProductRating,
    handle_errors=(ValueError, TypeError)  # Retry on ValueError and TypeError
)
```

If `handle_errors` is a tuple of exceptions, the agent will only retry (using the default error message) if the exception raised is one of the specified types. In all other cases, the exception will be raised.

**Custom error handler function:**

```python

from langchain.agents.structured_output import StructuredOutputValidationError
from langchain.agents.structured_output import MultipleStructuredOutputsError

def custom_error_handler(error: Exception) -> str:
    if isinstance(error, StructuredOutputValidationError):
        return "There was an issue with the format. Try again."
    elif isinstance(error, MultipleStructuredOutputsError):
        return "Multiple structured outputs were returned. Pick the most relevant one."
    else:
        return f"Error: {str(error)}"

agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=ToolStrategy(
                        schema=Union[ContactInfo, EventDetails],
                        handle_errors=custom_error_handler
                    )  # Default: handle_errors=True
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]
})

for msg in result['messages']:
    # If message is actually a ToolMessage object (not a dict), check its class name
    if type(msg).__name__ == "ToolMessage":
        print(msg.content)
    # If message is a dictionary or you want a fallback
    elif isinstance(msg, dict) and msg.get('tool_call_id'):
        print(msg['content'])

```

On `StructuredOutputValidationError`:
```
================================= Tool Message =================================
Name: ToolStrategy

There was an issue with the format. Try again.
```

On `MultipleStructuredOutputsError`:

```
================================= Tool Message =================================
Name: ToolStrategy

Multiple structured outputs were returned. Pick the most relevant one.
```

On other errors:

```
================================= Tool Message =================================
Name: ToolStrategy

Error: <error message>
```

**No error handling:**

```python
response_format = ToolStrategy(
    schema=ProductRating,
    handle_errors=False  # All errors raised
)
```

---

# LangSmith Studio
> 출처: data/raw/langchain/studio.mdx | https://docs.langchain.com/oss/python/langchain/studio

When building agents with LangChain locally, it's helpful to visualize what's happening inside your agent, interact with it in real-time, and debug issues as they occur. **LangSmith Studio** is a free visual interface for developing and testing your LangChain agents from your local machine.

Studio connects to your locally running agent to show you each step your agent takes: the prompts sent to the model, tool calls and their results, and the final output. You can test different inputs, inspect intermediate states, and iterate on your agent's behavior without additional code or deployment.

This pages describes how to set up Studio with your local LangChain agent.

## Prerequisites

Before you begin, ensure you have the following:

- **A LangSmith account**: Sign up (for free) or log in at [smith.langchain.com](https://smith.langchain.com).
- **A LangSmith API key**: Follow the [Create an API key](/langsmith/create-account-api-key) guide.
- If you don't want data [traced](/langsmith/observability-concepts#traces) to LangSmith, set `LANGSMITH_TRACING=false` in your application's `.env` file. With tracing disabled, no data leaves your local server.

## Set up local Agent server

### 1. Install the LangGraph CLI

The [LangGraph CLI](/langsmith/cli) provides a local development server (also called [Agent Server](/langsmith/agent-server)) that connects your agent to Studio.

```bash pip
# Python >= 3.11 is required.
pip install -U "langgraph-cli[inmem]"
```

```bash uv
# Python >= 3.11 is required.
uv add "langgraph-cli[inmem]"
```

### 2. Prepare your agent

If you already have a LangChain agent, you can use it directly. This example uses a simple email agent:

```python title="agent.py"
from langchain.agents import create_agent

def send_email(to: str, subject: str, body: str):
    """Send an email"""
    email = {
        "to": to,
        "subject": subject,
        "body": body
    }
    # ... email sending logic

return f"Email sent to {to}"

agent = create_agent(
    "gpt-5.5",
    tools=[send_email],
    system_prompt="You are an email assistant. Always use the send_email tool.",
)
```

### 3. Environment variables

Studio requires a LangSmith API key to connect your local agent. Create a `.env` file in the root of your project and add your API key from [LangSmith](https://smith.langchain.com/settings).

**Warning:**

Ensure your `.env` file is not committed to version control, such as Git.

```bash .env
LANGSMITH_API_KEY=lsv2...
```

### 4. Create a LangGraph config file

The LangGraph CLI uses a configuration file to locate your agent and manage dependencies. Create a `langgraph.json` file in your app's directory:

```json title="langgraph.json"
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent.py:agent"
  },
  "env": ".env"
}
```

The `create_agent` function automatically returns a compiled LangGraph graph, which is what the `graphs` key expects in the configuration file.

**Info:**

For detailed explanations of each key in the JSON object of the configuration file, refer to the [LangGraph configuration file reference](/langsmith/cli#configuration-file).

At this point, the project structure will look like this:

```bash
my-app/
├── src
│   └── agent.py
├── .env
└── langgraph.json
```

### 5. Install dependencies

Install your project dependencies from the root directory:

```shell pip
pip install langchain langchain-openai
```
```shell uv
uv add langchain langchain-openai
```

### 6. View your agent in Studio

Start the development server to connect your agent to Studio:

```shell
langgraph dev
```

**Warning:**

Safari blocks `localhost` connections to Studio. To work around this, run the above command with `--tunnel` to access Studio via a secure tunnel.

Once the server is running, your agent is accessible both via API at `http://127.0.0.1:2024` and through the Studio UI at `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`:

![Agent view in the Studio UI](/oss/images/studio_create-agent.png)

With Studio connected to your local agent, you can iterate quickly on your agent's behavior. Run a test input, inspect the full execution trace including prompts, tool arguments, return values, and token/latency metrics. When something goes wrong, Studio captures exceptions with the surrounding state to help you understand what happened.

The development server supports hot-reloading—make changes to prompts or tool signatures in your code, and Studio reflects them immediately. Re-run conversation threads from any step to test your changes without starting over. This workflow scales from simple single-tool agents to complex multi-node graphs.

For more information on how to run Studio, refer to the following guides in the [LangSmith docs](/langsmith/observability):

- [Run application](/langsmith/use-studio#run-application)
- [Manage assistants](/langsmith/use-studio#manage-assistants)
- [Manage threads](/langsmith/use-studio#manage-threads)
- [Iterate on prompts](/langsmith/observability-studio)
- [Debug LangSmith traces](/langsmith/observability-studio#debug-langsmith-traces)
- [Add node to dataset](/langsmith/observability-studio#add-node-to-dataset)

## Video guide

<iframe
  className="w-full aspect-video rounded-xl"
  src="https://www.youtube.com/embed/Mi1gSlHwZLM?si=zA47TNuTC5aH0ahd"
  title="Studio"
  frameBorder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowFullScreen
></iframe>

**Tip:**

For more information about deployed agents, see [Deployment](/oss/langchain/deploy).

---

# Agent Evals
> 출처: data/raw/langchain/test/evals.mdx | https://docs.langchain.com/oss/python/langchain/test/evals

Evaluate agent trajectories using deterministic matching or LLM-as-judge evaluators with AgentEvals and LangSmith.

Evaluations ("evals") measure how well your agent performs by assessing its execution trajectory, the sequence of messages and tool calls it produces. Unlike [integration tests](/oss/langchain/test/integration-testing) that verify basic correctness, evals score agent behavior against a reference or rubric, making them useful for catching regressions when you change prompts, tools, or models.

An evaluator is a function that takes agent outputs (and optionally reference outputs) and returns a score:

```python
def evaluator(*, outputs: dict, reference_outputs: dict):
    output_messages = outputs["messages"]
    reference_messages = reference_outputs["messages"]
    score = compare_messages(output_messages, reference_messages)
    return {"key": "evaluator_score", "score": score}
```

The [`agentevals`](https://github.com/langchain-ai/agentevals) package provides prebuilt evaluators for agent trajectories. You can evaluate by performing a **trajectory match** (deterministic comparison) or by using an **LLM judge** (qualitative assessment):

| Approach | When to use |
|----------|-------------|
| [Trajectory match](#trajectory-match-evaluator) | You know the expected tool calls and want fast, deterministic, cost-free checks |
| [LLM-as-judge](#llm-as-judge-evaluator) | You want to assess overall quality and reasoning without strict expectations |

## Install AgentEvals

```bash pip
pip install -U agentevals
```

```bash uv
uv add agentevals
```

Or, clone the [AgentEvals repository](https://github.com/langchain-ai/agentevals) directly.

## Trajectory match evaluator

AgentEvals offers the `create_trajectory_match_evaluator` function to match your agent's trajectory against a reference. There are four modes:

| Mode | Description | Use case |
|------|-------------|----------|
| `strict` | Exact match of message structure and tool calls in the same order (message content can differ) | Testing specific sequences (e.g., policy lookup before authorization) |
| `unordered` | Same message structure and tool calls as reference, but tool calls can happen in any order | Verifying information retrieval when order doesn't matter |
| `subset` | Agent calls only tools from reference (no extras) | Ensuring agent doesn't exceed expected scope |
| `superset` | Agent calls at least the reference tools (extras allowed) | Verifying minimum required actions are taken |

The examples below share a common setup, an agent with a `get_weather` tool:

```python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from agentevals.trajectory.match import create_trajectory_match_evaluator

@tool
def get_weather(city: str):
    """Get weather information for a city."""
    return f"It's 75 degrees and sunny in {city}."

agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
```

**Strict match**

The `strict` mode ensures trajectories contain identical messages in the same order with the same tool calls, though it allows for differences in message content. This is useful when you need to enforce a specific sequence of operations, such as requiring a policy lookup before authorizing an action.

```python
evaluator = create_trajectory_match_evaluator(  # [!code highlight]
    trajectory_match_mode="strict",  # [!code highlight]
)  # [!code highlight]

def test_weather_tool_called_strict():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in San Francisco?")]
    })

reference_trajectory = [
    HumanMessage(content="What's the weather in San Francisco?"),
    AIMessage(content="", tool_calls=[
        {"id": "call_1", "name": "get_weather", "args": {"city": "San Francisco"}}
    ]),
    ToolMessage(content="It's 75 degrees and sunny in San Francisco.", tool_call_id="call_1"),
    AIMessage(content="The weather in San Francisco is 75 degrees and sunny."),
]

    evaluation = evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory
    )
    # {
    #     'key': 'trajectory_strict_match',
    #     'score': True,
    #     'comment': None,
    # }
    assert evaluation["score"] is True
```

**Unordered match**

The `unordered` mode allows the same tool calls in any order. This is helpful when you want to verify that specific information was retrieved but don't care about the sequence. For example, an agent that checks both weather and events for a city with different tool calls.

```python
@tool
def get_events(city: str):
    """Get events happening in a city."""
    return f"Concert at the park in {city} tonight."

agent = create_agent("claude-sonnet-4-6", tools=[get_weather, get_events])

evaluator = create_trajectory_match_evaluator(  # [!code highlight]
    trajectory_match_mode="unordered",  # [!code highlight]
)  # [!code highlight]

def test_multiple_tools_any_order():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's happening in SF today?")]
    })

reference_trajectory = [
    HumanMessage(content="What's happening in SF today?"),
    AIMessage(content="", tool_calls=[
        {"id": "call_1", "name": "get_events", "args": {"city": "SF"}},
        {"id": "call_2", "name": "get_weather", "args": {"city": "SF"}},
    ]),
    ToolMessage(content="Concert at the park in SF tonight.", tool_call_id="call_1"),
    ToolMessage(content="It's 75 degrees and sunny in SF.", tool_call_id="call_2"),
    AIMessage(content="Today in SF: 75 degrees and sunny with a concert at the park tonight."),
]

    evaluation = evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory,
    )
    assert evaluation["score"] is True
```

**Subset and superset match**

The `superset` and `subset` modes match partial trajectories. The `superset` mode verifies that the agent called at least the tools in the reference trajectory, allowing additional tool calls. The `subset` mode ensures the agent did not call any tools beyond those in the reference.

```python
@tool
def get_detailed_forecast(city: str):
    """Get detailed weather forecast for a city."""
    return f"Detailed forecast for {city}: sunny all week."

agent = create_agent("claude-sonnet-4-6", tools=[get_weather, get_detailed_forecast])

evaluator = create_trajectory_match_evaluator(  # [!code highlight]
    trajectory_match_mode="superset",  # [!code highlight]
)  # [!code highlight]

def test_agent_calls_required_tools_plus_extra():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in Boston?")]
    })

# Reference only requires get_weather, but agent may call additional tools
reference_trajectory = [
    HumanMessage(content="What's the weather in Boston?"),
    AIMessage(content="", tool_calls=[
        {"id": "call_1", "name": "get_weather", "args": {"city": "Boston"}},
    ]),
    ToolMessage(content="It's 75 degrees and sunny in Boston.", tool_call_id="call_1"),
    AIMessage(content="The weather in Boston is 75 degrees and sunny."),
]

    evaluation = evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory,
    )
    assert evaluation["score"] is True
```

**Info:**

You can also set the `tool_args_match_mode` property and/or `tool_args_match_overrides` to customize how the evaluator considers equality between tool calls in the actual trajectory vs. the reference. By default, only tool calls with the same arguments to the same tool are considered equal. Visit the [repository](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#tool-args-match-modes) for more details.

## LLM-as-judge evaluator

You can use an LLM to evaluate the agent's execution path with the `create_trajectory_llm_as_judge` function. Unlike trajectory match evaluators, it doesn't require a reference trajectory, but one can be provided if available.

**Without reference trajectory**

```python
from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT

evaluator = create_trajectory_llm_as_judge(  # [!code highlight]
    model="openai:o3-mini",  # [!code highlight]
    prompt=TRAJECTORY_ACCURACY_PROMPT,  # [!code highlight]
)  # [!code highlight]

def test_trajectory_quality():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in Seattle?")]
    })

    evaluation = evaluator(
        outputs=result["messages"],
    )
    assert evaluation["score"] is True
```

**With reference trajectory**

If you have a reference trajectory, use the prebuilt `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE` prompt:

```python
from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE

evaluator = create_trajectory_llm_as_judge(
    model="openai:o3-mini",
    prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE,
)
evaluation = evaluator(
    outputs=result["messages"],
    reference_outputs=reference_trajectory,
)
```

**Info:**

For more configurability over how the LLM evaluates the trajectory, visit the [repository](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#trajectory-llm-as-judge).

### Async support

All `agentevals` evaluators support Python asyncio. Async versions are available by adding `async` after `create_` in the function name.

**Async judge and evaluator example**

```python
from agentevals.trajectory.llm import create_async_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT
from agentevals.trajectory.match import create_async_trajectory_match_evaluator

async_judge = create_async_trajectory_llm_as_judge(
    model="openai:o3-mini",
    prompt=TRAJECTORY_ACCURACY_PROMPT,
)

async_evaluator = create_async_trajectory_match_evaluator(
    trajectory_match_mode="strict",
)

async def test_async_evaluation():
    result = await agent.ainvoke({
        "messages": [HumanMessage(content="What's the weather?")]
    })

    evaluation = await async_judge(outputs=result["messages"])
    assert evaluation["score"] is True
```

## Run evals in LangSmith

For tracking experiments over time, log evaluator results to [LangSmith](https://smith.langchain.com). First, set the required environment variables:

```bash
export LANGSMITH_API_KEY="your_langsmith_api_key"
export LANGSMITH_TRACING="true"
```

LangSmith offers two main approaches for running evaluations: [pytest](/langsmith/pytest) integration and the `evaluate` function.

**Use pytest integration**

```python
import pytest
from langsmith import testing as t
from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT

trajectory_evaluator = create_trajectory_llm_as_judge(
    model="openai:o3-mini",
    prompt=TRAJECTORY_ACCURACY_PROMPT,
)

@pytest.mark.langsmith
def test_trajectory_accuracy():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in SF?")]
    })

reference_trajectory = [
    HumanMessage(content="What's the weather in SF?"),
    AIMessage(content="", tool_calls=[
        {"id": "call_1", "name": "get_weather", "args": {"city": "SF"}},
    ]),
    ToolMessage(content="It's 75 degrees and sunny in SF.", tool_call_id="call_1"),
    AIMessage(content="The weather in SF is 75 degrees and sunny."),
]

t.log_inputs({})
t.log_outputs({"messages": result["messages"]})
t.log_reference_outputs({"messages": reference_trajectory})

    trajectory_evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory
    )
```

Run the evaluation with pytest:

```bash
pytest test_trajectory.py --langsmith-output
```

**Use the evaluate function**

Create a [LangSmith dataset](/langsmith/manage-datasets) and use the `evaluate` function. The dataset must have the following schema:

* **input**: `{"messages": [...]}` input messages to call the agent with.
* **output**: `{"messages": [...]}` expected message history in the agent output. For trajectory evaluation, you can choose to keep only assistant messages.

```python
from langsmith import Client
from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT

client = Client()

trajectory_evaluator = create_trajectory_llm_as_judge(
    model="openai:o3-mini",
    prompt=TRAJECTORY_ACCURACY_PROMPT,
)

def run_agent(inputs):
    return agent.invoke(inputs)["messages"]

experiment_results = client.evaluate(
    run_agent,
    data="your_dataset_name",
    evaluators=[trajectory_evaluator]
)
```

**Tip:**

To learn more about evaluating your agent, see the [LangSmith docs](/langsmith/pytest).

---

# Test
> 출처: data/raw/langchain/test/index.mdx | https://docs.langchain.com/oss/python/langchain/test

Strategies for testing LangChain agents, including unit tests, integration tests, and trajectory evaluations.

Agentic applications let an LLM decide its own next steps to solve a problem. That flexibility is powerful, but the model's black-box nature makes it hard to predict how a tweak in one part of your agent will affect the whole. To build production-ready agents, thorough testing is essential.

There are a few approaches to testing your agents:

- **Unit tests** exercise small, deterministic pieces of your agent in isolation using in-memory fakes so you can assert exact behavior quickly and deterministically.
- **Integration tests** test the agent using real network calls to confirm that components work together, credentials and schemas line up, and latency is acceptable.
- **Evals** use evaluators to assess your agent's execution trajectory, either via deterministic matching or an LLM judge.

Agentic applications tend to lean more on integration because they chain multiple components together and must deal with flakiness due to the nondeterministic nature of LLMs.

**Tip:**

Run evaluations at scale, track results over time, and compare experiments with [LangSmith](https://smith.langchain.com). See [Evaluate an LLM application](/langsmith/evaluate-llm-application) to get started.

- [Unit testing](/oss/langchain/test/unit-testing)

        Mock chat models and use in-memory persistence to test agent logic without API calls.

- [Integration testing](/oss/langchain/test/integration-testing)

        Test your agent with real LLM APIs. Organize tests, manage keys, handle flakiness, and control costs.

- [Evals](/oss/langchain/test/evals)

        Evaluate agent trajectories with deterministic matching or LLM-as-judge evaluators.

---

# Integration testing
> 출처: data/raw/langchain/test/integration-testing.mdx | https://docs.langchain.com/oss/python/langchain/test/integration-testing

Test agents with real LLM APIs by organizing tests, managing keys, handling flakiness, and controlling costs.

Integration tests verify that your agent works correctly with model APIs and external services. Unlike [unit tests](/oss/langchain/test/unit-testing) that use fakes and mocks, integration tests make actual network calls to confirm that components work together, credentials are valid, and latency is acceptable.

Because LLM responses are nondeterministic, integration tests require different strategies than traditional software tests. This guide covers how to organize, write, and run integration tests for your agents. For general test infrastructure when contributing to LangChain itself, see [Contributing to code](/oss/contributing/code#running-tests).

## Separate unit and integration tests

Integration tests are slower and require API credentials, so keep them separate from unit tests. This lets you run fast unit tests on every change and reserve integration tests for CI or pre-deploy checks.

Use pytest markers to tag integration tests:

```python
import pytest
from langchain.agents import create_agent
from langchain.messages import HumanMessage

@pytest.mark.integration
def test_agent_with_real_model():
    agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in SF?")]
    })
    assert len(result["messages"]) > 1
```

Configure pytest to recognize the marker and exclude integration tests from default runs:

```ini pytest.ini
[pytest]
markers =
    integration: tests that call real LLM APIs
addopts = -m "not integration"
```
```toml pyproject.toml
[tool.pytest.ini_options]
markers = [
  "integration: tests that call real LLM APIs"
]
addopts = "-m 'not integration'"
```

Run integration tests explicitly:

```bash
pytest -m integration
```

## Manage API keys

Integration tests require real API credentials. Load them from environment variables so keys stay out of source control.

Use a `conftest.py` fixture to validate that required keys are available:

```python
import os
import pytest

@pytest.fixture(autouse=True)
def check_api_keys():
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")
```

For local development, store keys in a `.env` file and load them with [`python-dotenv`](https://pypi.org/project/python-dotenv/):

```bash .env
OPENAI_API_KEY=sk-...
```

```python conftest.py
from dotenv import load_dotenv

load_dotenv()
```

**Warning:**

Add `.env` to your `.gitignore` to avoid committing credentials. In CI, inject secrets through your provider's secrets management (e.g., GitHub Actions secrets).

## Assert on structure, not content

LLM responses vary between runs. Instead of asserting on exact output strings, verify the structural properties of the response: message types, tool call names, argument shapes, and message count.

```python
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage

def test_agent_calls_weather_tool():
    agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in SF?")]
    })

messages = result["messages"]
tool_calls = [
    tc
    for msg in messages
    if hasattr(msg, "tool_calls")
    for tc in (msg.tool_calls or [])
]

    assert any(tc["name"] == "get_weather" for tc in tool_calls)
    assert isinstance(messages[-1], AIMessage)
    assert len(messages[-1].content) > 0
```

**Tip:**

For more rigorous trajectory assertions, use the [AgentEvals](/oss/langchain/test/evals) evaluators which support fuzzy matching modes like `unordered` and `superset`.

## Reduce cost and latency

Integration tests that call LLM APIs incur real costs. A few practices help keep test suites fast and affordable:

- **Use smaller models**: `gemini-3.1-flash-lite` or equivalent for tests that only need to verify tool calling and response structure.
- **Set `maxTokens`**: Cap response length to avoid long, expensive completions.
- **Limit test scope**: Test one behavior per test. Avoid end-to-end scenarios that chain many LLM calls when a single-turn test suffices.
- **Run selectively**: Use the test separation from [above](#separate-unit-and-integration-tests) to run integration tests only in CI or before deploy, not on every file save.

```python
from langchain.agents import create_agent

agent = create_agent(
    "gemini-3.1-flash-lite",
    tools=[get_weather],
    model_kwargs={"max_tokens": 256},
)
```

## Record and replay HTTP calls

For tests that run frequently in CI, you can record HTTP interactions on the first run and replay them on subsequent runs without making real API calls. This eliminates cost and latency after the initial recording.

[`vcrpy`](https://pypi.org/project/vcrpy/1.5.2/) records HTTP request/response pairs into YAML "cassette" files. The [`pytest-recording`](https://pypi.org/project/pytest-recording/) plugin integrates this with pytest.

Set up your `conftest.py` to filter sensitive information from cassettes:

```py conftest.py
import pytest

@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_headers": [
            ("authorization", "XXXX"),
            ("x-api-key", "XXXX"),
        ],
        "filter_query_parameters": [
            ("api_key", "XXXX"),
            ("key", "XXXX"),
        ],
    }
```

Configure your project to recognize the `vcr` marker:

```ini pytest.ini
[pytest]
markers =
    vcr: record/replay HTTP via VCR
addopts = --record-mode=once
```
```toml pyproject.toml
[tool.pytest.ini_options]
markers = [
  "vcr: record/replay HTTP via VCR"
]
addopts = "--record-mode=once"
```

**Info:**

The `--record-mode=once` option records HTTP interactions on the first run and replays them on subsequent runs.

Decorate your tests with the `vcr` marker:

```python
import pytest
from langchain.agents import create_agent
from langchain.messages import HumanMessage

@pytest.mark.vcr()
def test_agent_trajectory():
    agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in SF?")]
    })
    assert any(
        tc["name"] == "get_weather"
        for msg in result["messages"]
        if hasattr(msg, "tool_calls")
        for tc in (msg.tool_calls or [])
    )
```

The first run makes real network calls and generates a cassette file in `tests/cassettes/`. Subsequent runs replay the recorded responses.

**Warning:**

When you modify prompts, add new tools, or change expected trajectories, your saved cassettes will become outdated and your existing tests **will fail**. Delete the corresponding cassette files and rerun the tests to record fresh interactions.

## Next steps

Learn how to evaluate agent trajectories with deterministic matching or LLM-as-judge evaluators in [Evals](/oss/langchain/test/evals).

---

# Unit testing
> 출처: data/raw/langchain/test/unit-testing.mdx | https://docs.langchain.com/oss/python/langchain/test/unit-testing

Test agent logic without API calls using fake chat models and in-memory persistence.

Unit tests exercise small, deterministic pieces of your agent in isolation. By replacing the real LLM with an in-memory fake (AKA fixture), you can script exact responses (text, tool calls, and errors) so tests are fast, free, and repeatable without API keys.

## Mock chat model

LangChain provides `GenericFakeChatModel` for mocking text responses. It accepts an iterator of responses (`AIMessage` objects or strings) and returns one per invocation. It supports both regular and streaming usage.

```python
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain.messages import AIMessage, ToolCall

model = GenericFakeChatModel(messages=iter([
    AIMessage(content="", tool_calls=[ToolCall(name="foo", args={"bar": "baz"}, id="call_1")]),
    "bar"
]))

model.invoke("hello")
# AIMessage(content='', ..., tool_calls=[{'name': 'foo', 'args': {'bar': 'baz'}, 'id': 'call_1', 'type': 'tool_call'}])
```

If we invoke the model again, it will return the next item in the iterator:

```python
model.invoke("hello, again!")
# AIMessage(content='bar', ...)
```

## InMemorySaver checkpointer

To enable persistence during testing, you can use the `InMemorySaver` checkpointer. This allows you to simulate multiple turns to test state-dependent behavior:

```python
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.messages import HumanMessage

agent = create_agent(
    model,
    tools=[],
    checkpointer=InMemorySaver()
)

# First invocation
agent.invoke(
    {"messages": [HumanMessage(content="I live in Sydney, Australia")]},
    config={"configurable": {"thread_id": "session-1"}}
)

# Second invocation: the first message is persisted (Sydney location), so the model returns GMT+10 time
agent.invoke(
    {"messages": [HumanMessage(content="What's my local time?")]},
    config={"configurable": {"thread_id": "session-1"}}
)
```

## Next steps

Learn how to test your agent with real model provider APIs in [Integration testing](/oss/langchain/test/integration-testing).

---

# Tools
> 출처: data/raw/langchain/tools.mdx | https://docs.langchain.com/oss/python/langchain/tools

Define tools that let LangChain agents fetch real-time data, execute code, query external databases, and take actions.

Tools extend what [agents](/oss/langchain/agents) can do—letting them fetch real-time data, execute code, query external databases, and take actions in the world.

Under the hood, tools are callable functions with well-defined inputs and outputs that get passed to a [chat model](/oss/langchain/models). The model decides when to invoke a tool based on the conversation context, and what input arguments to provide.

**Tip:**

For details on how models handle tool calls, see [Tool calling](/oss/langchain/models#tool-calling). Trace tool calls and debug errors with [LangSmith](https://smith.langchain.com). Follow the [tracing quickstart](/langsmith/trace-with-langchain) to get set up.

We recommend you also set up [LangSmith Engine](/langsmith/engine) which monitors your traces, detects issues, and proposes fixes.

## Create tools

### Basic tool definition

The simplest way to create a tool is with the `@tool` decorator. By default, the function's docstring becomes the tool's description that helps the model understand when to use it:

```python
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"
```

Type hints are **required** as they define the tool's input schema. The docstring should be informative and concise to help the model understand the tool's purpose.

**Note:**

**Server-side tool use:** Some chat models feature built-in tools (web search, code interpreters) that are executed server-side. See [Server-side tool use](#server-side-tool-use) for details.

**Warning:**

Prefer `snake_case` for tool names (e.g., `web_search` instead of `Web Search`). Some model providers have issues with or reject names containing spaces or special characters with errors. Sticking to alphanumeric characters, underscores, and hyphens helps to improve compatibility across providers.

### Customize tool properties

#### Custom tool name

By default, the tool name comes from the function name. Override it when you need something more descriptive:

```python
@tool("web_search")  # Custom name
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

print(search.name)  # web_search
```

#### Custom tool description

Override the auto-generated tool description for clearer model guidance:

```python
@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))
```

### Advanced schema definition

Define complex inputs with Pydantic models or JSON schemas:

```python Pydantic model
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    """Input for weather queries."""
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="Temperature unit preference"
    )
    include_forecast: bool = Field(
        default=False,
        description="Include 5-day forecast"
    )

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result
```

```python JSON Schema
weather_schema = {
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "units": {"type": "string"},
        "include_forecast": {"type": "boolean"}
    },
    "required": ["location", "units", "include_forecast"]
}

@tool(args_schema=weather_schema)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result
```

### Reserved argument names

The following parameter names are reserved and cannot be used as tool arguments. Using these names will cause runtime errors.

| Parameter name | Purpose |
|----------------|---------|
| `config` | Reserved for passing `RunnableConfig` to tools internally |
| `runtime` | Reserved for `ToolRuntime` parameter (accessing state, context, store) |

To access runtime information, use the `ToolRuntime` parameter instead of naming your own arguments `config` or `runtime`.

If you use `InjectedState`, `InjectedStore`, `get_runtime()`, or `InjectedToolCallId`, see [Migrate from older injection patterns](#migrate-from-older-injection-patterns).

## Access context

Tools are most powerful when they can access runtime information like conversation history, user data, and persistent memory. This section covers how to access and update this information from within your tools.

Tools can access runtime information through the `ToolRuntime` parameter, which provides:

| Component | Description | Use case |
|-----------|-------------|----------|
| **State** | Short-term memory - mutable data that exists for the current conversation (messages, counters, custom fields) | Access conversation history, track tool call counts |
| **Context** | Immutable configuration passed at invocation time (user IDs, session info) | Personalize responses based on user identity |
| **Store** | Long-term memory - persistent data that survives across conversations | Save user preferences, maintain knowledge base |
| **Stream Writer** | Emit real-time updates during tool execution | Show progress for long-running operations |
| **Execution Info** | Identity and retry information for the current execution (thread ID, run ID, attempt number) | Access thread/run IDs, adjust behavior based on retry state |
| **Server Info** | Server-specific metadata when running on LangGraph Server (assistant ID, graph ID, authenticated user) | Access assistant ID, graph ID, or authenticated user info |
| **Config** | `RunnableConfig` for the execution | Access callbacks, tags, and metadata |
| **Tool Call ID** | Unique identifier for the current tool invocation | Correlate tool calls for logs and model invocations |

```mermaid
graph LR
    %% Runtime Context
    subgraph "🔧 Tool Runtime Context"
        A[Tool Call] --> B[ToolRuntime]
        B --> C[State Access]
        B --> D[Context Access]
        B --> E[Store Access]
        B --> F[Stream Writer]
    end

%% Available Resources
subgraph "📊 Available Resources"
    C --> G[Messages]
    C --> H[Custom State]
    D --> I[User ID]
    D --> J[Session Info]
    E --> K[Long-term Memory]
    E --> L[User Preferences]
end

%% Tool Capabilities
subgraph "⚡ Enhanced Tool Capabilities"
    M[Context-Aware Tools]
    N[Stateful Tools]
    O[Memory-Enabled Tools]
    P[Streaming Tools]
end

%% Connections
G --> M
H --> N
I --> M
J --> M
K --> O
L --> O
F --> P

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

    class A trigger
    class B,C,D,E,F process
    class G,H,I,J,K,L neutral
    class M,N,O,P output
```

### Short-term memory (State)

State represents short-term memory that exists for the duration of a conversation. It includes the message history and any custom fields you define in your [graph state](/oss/langgraph/graph-api#state).

#### Access state

Add `runtime: ToolRuntime` to your tool signature to access state. At call time, `ToolNode` injects the value automatically; the parameter is not included in the tool schema sent to the model. Use `runtime.state` to read the current conversation state:

```python
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage

@tool
def get_last_user_message(runtime: ToolRuntime) -> str:
    """Get the most recent message from the user."""
    messages = runtime.state["messages"]

# Find the last human message
for message in reversed(messages):
    if isinstance(message, HumanMessage):
        return message.content

return "No user messages found"

# Access custom state fields
@tool
def get_user_preference(
    pref_name: str,
    runtime: ToolRuntime
) -> str:
    """Get a user preference value."""
    preferences = runtime.state.get("user_preferences", {})
    return preferences.get(pref_name, "Not set")
```

**Warning:**

The `runtime` parameter is hidden from the model. For the example above, the model only sees `pref_name` in the tool schema.

#### Update state

Use `Command` to update the agent's state. This is useful for tools that need to update custom state fields.
Include a `ToolMessage` in the update so the model can see the result of the tool call:

```python
from langchain.agents import AgentState
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

class CustomState(AgentState):
    user_name: str

@tool
def set_user_name(new_name: str, runtime: ToolRuntime[None, CustomState]) -> Command:
    """Set the user's name in the conversation state."""
    return Command(
        update={
            "user_name": new_name,
            "messages": [
                ToolMessage(
                    content=f"User name set to {new_name}.",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
```

- [View example trace](https://smith.langchain.com/public/e2d025b4-a79c-4aa5-9efa-953e09a5566c/r)

  Open a public LangSmith run for this example.

**Tip:**

When tools update state variables, consider defining a [reducer](/oss/langgraph/graph-api#reducers) for those fields. Since LLMs can call multiple tools in parallel, a reducer determines how to resolve conflicts when the same state field is updated by concurrent tool calls.

### Context

Context provides immutable configuration data that is passed at invocation time. Use it for user IDs, session details, or application-specific settings that shouldn't change during a conversation.

**Note:**

While `thread_id` (passed via `config={"configurable": {"thread_id": ...}}`) scopes the *conversation*: message history and checkpoints, `context` carries *per-run* data your tools and middleware read at invocation time. Persistence requires a [checkpointer](/oss/langchain/short-term-memory). In production you typically pass both a stable `thread_id` per conversation and a `context` object on every invoke.

Access context through `runtime.context`. Configure a [checkpointer](/oss/langchain/short-term-memory) and pass `context` with a stable `thread_id` so the conversation persists across invocations:

```python
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_core.utils.uuid import uuid7
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

USER_DATABASE = {
    "user123": {
        "name": "Alice Johnson",
        "account_type": "Premium",
        "balance": 5000,
        "email": "alice@example.com",
    },
    "user456": {
        "name": "Bob Smith",
        "account_type": "Standard",
        "balance": 1200,
        "email": "bob@example.com",
    },
}

@dataclass
class UserContext:
    user_id: str

@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """Get the current user's account information."""
    user_id = runtime.context.user_id

if user_id in USER_DATABASE:
    user = USER_DATABASE[user_id]
    return (
        f"Account holder: {user['name']}\n"
        f"Type: {user['account_type']}\n"
        f"Balance: ${user['balance']}"
    )
return "User not found"

model = ChatOpenAI(model="gpt-5.5")
agent = create_agent(
    model,
    tools=[get_account_info],
    context_schema=UserContext,
    checkpointer=InMemorySaver(),
    system_prompt="You are a financial assistant.",
)

thread_id = str(uuid7())
config = {"configurable": {"thread_id": thread_id}}
context = UserContext(user_id="user123")

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my current balance?"}]},
    config=config,
    context=context,
)
print(result["messages"][-1].content_blocks)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What was my balance again?"}]},
    config=config,
    context=context,
)
print(result["messages"][-1].content_blocks)
```

- [View example trace](https://smith.langchain.com/public/9862768e-4c5c-46df-b774-e0eda067aea7/r)

  Open a public LangSmith run for this example.

### Long-term memory (Store)

The `BaseStore` provides persistent storage that survives across conversations. Unlike state (short-term memory), data saved to the store remains available in future sessions.

Access the store through `runtime.store`. The store uses a namespace/key pattern to organize data:

**Tip:**

For production deployments, use a persistent store implementation like `PostgresStore`, `MongoDBStore`, or `RedisStore` instead of `InMemoryStore`. See the [memory documentation](/oss/langgraph/add-memory) for setup details.

```python expandable
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openai import ChatOpenAI

# Access memory
@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """Look up user info."""
    store = runtime.store
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

# Update memory
@tool
def save_user_info(user_id: str, name: str, age: int, email: str, runtime: ToolRuntime) -> str:
    """Save user info."""
    store = runtime.store
    store.put(("users",), user_id, {"name": name, "age": age, "email": email})
    return "Successfully saved user info."

model = ChatOpenAI(model="gpt-5.5")

store = InMemoryStore()
agent = create_agent(
    model,
    tools=[get_user_info, save_user_info],
    store=store
)

# First session: save user info
agent.invoke({
    "messages": [{"role": "user", "content": "Save the following user: userid: abc123, name: Foo, age: 25, email: foo@langchain.dev"}]
})

# Second session: get user info
agent.invoke({
    "messages": [{"role": "user", "content": "Get user info for user with id 'abc123'"}]
})
# Here is the user info for user with ID "abc123":
# - Name: Foo
# - Age: 25
# - Email: foo@langchain.dev
```

### Stream writer

Stream real-time updates from tools during execution. This is useful for providing progress feedback to users during long-running operations.

Use `runtime.stream_writer` to emit custom updates:

```python
from langchain.tools import tool, ToolRuntime

@tool
def get_weather(city: str, runtime: ToolRuntime) -> str:
    """Get weather for a given city."""
    writer = runtime.stream_writer

# Stream custom updates as the tool executes
writer(f"Looking up data for city: {city}")
writer(f"Acquired data for city: {city}")

    return f"It's always sunny in {city}!"
```

**Note:**

If you use `runtime.stream_writer` inside your tool, the tool must be invoked within a LangGraph execution context. See [Streaming](/oss/langchain/streaming) for more details.

### Execution info

Access thread ID, run ID, and retry state from within a tool via `runtime.execution_info`:

```python
from langchain.tools import tool, ToolRuntime

@tool
def log_execution_context(runtime: ToolRuntime) -> str:
    """Log execution identity information."""
    info = runtime.execution_info
    print(f"Thread: {info.thread_id}, Run: {info.run_id}")  # [!code highlight]
    print(f"Attempt: {info.node_attempt}")
    return "done"
```

**Note:**

Requires `deepagents>=0.5.0` (or `langgraph>=1.1.5`).

### Server info

When your tool runs on LangGraph Server, access the assistant ID, graph ID, and authenticated user via `runtime.server_info`:

```python
from langchain.tools import tool, ToolRuntime

@tool
def get_assistant_scoped_data(runtime: ToolRuntime) -> str:
    """Fetch data scoped to the current assistant."""
    server = runtime.server_info
    if server is not None:
        print(f"Assistant: {server.assistant_id}, Graph: {server.graph_id}")  # [!code highlight]
        if server.user is not None:
            print(f"User: {server.user.identity}")  # [!code highlight]
    return "done"
```

`server_info` is `None` when the tool is not running on LangGraph Server (e.g., during local development or testing).

**Note:**

Requires `deepagents>=0.5.0` (or `langgraph>=1.1.5`).

**Migrate from older injection patterns**

Older examples used `InjectedState`, `InjectedStore`, `get_runtime()`, or `InjectedToolCallId`. Use `ToolRuntime` instead for one explicit interface to state, context, store, and execution metadata.

#### Previous pattern

```python
from langchain.tools import tool, InjectedState

@tool
def summarize(state: InjectedState) -> str:
    """Summarize the conversation."""
    messages = state["messages"]
    return f"Conversation length: {len(messages)} messages."
```

#### Recommended pattern

```python
from langchain.tools import tool, ToolRuntime

@tool
def summarize(runtime: ToolRuntime) -> str:
    """Summarize the conversation."""
    messages = runtime.state["messages"]
    return f"Conversation length: {len(messages)} messages."
```

For agent-level migrations (for example `create_react_agent` and custom state), see the [LangChain v1 migration guide](/oss/migrate/langchain-v1).

## Tool execution

In LangChain, tools are used by agents (for example via `create_agent`) and tool error handling is configured through [middleware](/oss/langchain/middleware).

For LangGraph workflows, tool execution is handled by `ToolNode`. See [ToolNode](/oss/langgraph/workflows-agents#toolnode) for Graph API usage, including how tools can access the current graph state and run-scoped context.

### Tool return values

You can choose different return values for your tools:

- Return a `string` for human-readable results.
- Return an `object` for structured results the model should parse.
- Return a `Command` with optional message when you need to write to state.

#### Return a string

Return a string when the tool should provide plain text for the model to read and use in its next response.

```python
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"It is currently sunny in {city}."
```

- [View example trace](https://smith.langchain.com/public/53f46dad-2132-4c21-aa44-58110a7041c8/r)

  Open a public LangSmith run for this example.

Behavior:

- The return value is converted to a `ToolMessage`.
- The model sees that text and decides what to do next.
- No agent state fields are changed unless the model or another tool does so later.

Use this when the result is naturally human-readable text.

#### Return an object

Return an object (for example, a `dict`) when your tool produces structured data that the model should inspect.

```python
from langchain.tools import tool

@tool
def get_weather_data(city: str) -> dict:
    """Get structured weather data for a city."""
    return {
        "city": city,
        "temperature_c": 22,
        "conditions": "sunny",
    }
```

- [View example trace](https://smith.langchain.com/public/5a9566cd-8702-4147-bfe0-f22949d91761/r)

  Open a public LangSmith run for this example.

Behavior:

- The object is serialized and sent back as tool output.
- The model can read specific fields and reason over them.
- Like string returns, this does not directly update graph state.

Use this when downstream reasoning benefits from explicit fields instead of free-form text.

#### Return multimodal content

Tools are not limited to plain text. When the model supports multimodal tool results, the tool can return [standard content blocks](/oss/langchain/messages#standard-content-blocks) so the model receives text, images, and other media in one tool result.

```python
from langchain.tools import tool

@tool
def capture_screenshot() -> list[dict]:
    """Capture a screenshot of the current page."""
    return [
        {"type": "text", "text": "Screenshot of the current page:"},
        {"type": "image", "url": "https://example.com/page.png"},
    ]
```

Behavior:

- The return value is converted to a `ToolMessage` with multimodal `content`.
- Use `message.content_blocks` to read the normalized block list after the tool runs.
- The model must support the modalities you return. Check your [model's capabilities](/oss/integrations/chat) before returning images, audio, or video.

For block types and provider-specific requirements, see [Multimodal messages](/oss/langchain/messages#multimodal).

MCP tools that return images or mixed content are converted the same way. See [Multimodal content](/oss/langchain/mcp/tools#multimodal-content).

#### Return a Command

Return a `Command` when the tool needs to update graph state (for example, setting user preferences or app state).
When the `Command` targets the current graph, include a `ToolMessage` in the update whose tool call ID matches the current tool call.
Every tool call in the message history must have a corresponding `ToolMessage`.

Use `runtime.tool_call_id` for the `tool_call_id` parameter. `ToolNode` enforces this requirement: if the update has no `ToolMessage` matching the tool call, it raises a `ValueError`.

```python
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

@tool
def set_language(language: str, runtime: ToolRuntime) -> Command:
    """Set the preferred response language."""
    return Command(
        update={
            "preferred_language": language,
            "messages": [
                ToolMessage(
                    content=f"Language set to {language}.",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
```

- [View example trace](https://smith.langchain.com/public/7d36f0e9-8036-4ad0-a0f9-68a94e45628f/r)

  Open a public LangSmith run for this example.

Behavior:

- The command updates state using `update`.
- Updated state is available to subsequent steps in the same run.
- Use reducers for fields that may be updated by parallel tool calls.

Use this when the tool is not just returning data, but also mutating agent state.

#### Return directly from a tool

Set return direct on a tool to short-circuit the agent loop: the agent returns the tool's output to the caller immediately, without sending it back through the model for further processing.

```python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

@tool(return_direct=True)
def fetch_order_status(order_id: str) -> str:
    """Fetch the current status of a customer order."""
    # In production, query your order management system here
    return f"Order {order_id} is shipped and will arrive in 2 days."

agent = create_agent(
    ChatOpenAI(model="gpt-4o-mini"),
    tools=[fetch_order_status],
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What is the status of order #12345?"}]
})
# The agent returns the tool output directly without another LLM call:
# "Order 12345 is shipped and will arrive in 2 days."
```

- [View example trace](https://smith.langchain.com/public/b1764d7e-9786-4040-a1dd-720102c9b0b0/r)

  Open a public LangSmith run for this example.

Behavior:

- The tool executes normally and its output is wrapped in a `ToolMessage`.
- The agent stops looping and returns the tool's output as the final response, bypassing any additional model call.
- **Multiple parallel tool calls:** When the model calls several tools in one step, all of them execute first. After all tools finish, the agent routes to `END` only if **every** tool in that batch has `return_direct=True`. The final response includes the `ToolMessage` outputs of every tool that was called in that step.

Use this when:

- The tool's output is the complete, user-ready answer (for example, a lookup that returns a ready-to-display result).
- You want to avoid an extra model call when no additional reasoning is needed.
- You need deterministic, unmodified output: the model cannot rephrase, summarize, or act on the tool result.

**Warning:**

Because the model does not process the tool's output, `return_direct=True` is not suitable for tools whose results require further reasoning, summarization, or chaining with other tool calls.

**Warning:**

**Mixed parallel calls:** If the model calls a `return_direct=True` tool alongside tools that do not have `return_direct=True`, the agent does **not** exit after that step. It routes back to the model with every `ToolMessage` from the batch, so the model can reason over all results. `return_direct` only short-circuits the loop when every tool call in the step has `return_direct=True`.

#### Return a Command with return_direct

A tool with `return_direct=True` can also return a `Command` to update graph state before the agent exits. Unlike a plain return value, a `Command` is not automatically converted into a `ToolMessage`. When the `Command` targets the current graph (`graph` is not set or is `None`), include a `ToolMessage` in `Command.update` matching the tool call's `tool_call_id`. Omitting it causes `ToolNode` to raise a `ValueError`, because every `AIMessage` tool call must have a corresponding `ToolMessage` in the message history.

```python
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

@tool(return_direct=True)
def fetch_and_store_order(order_id: str, runtime: ToolRuntime) -> Command:
    """Fetch order status and store it in state."""
    status = f"Order {order_id} is shipped and will arrive in 2 days."
    return Command(
        update={
            "last_order_status": status,
            # Must include a ToolMessage so the message history stays valid
            "messages": [
                ToolMessage(
                    content=status,
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
```

- [View example trace](https://smith.langchain.com/public/a4000b2b-d692-4e4f-ad34-2317ff0bd93d/r)

  Open a public LangSmith run for this example.

To write to a parent graph instead, set `graph=Command.PARENT`. In that case the `ToolMessage` requirement is lifted because execution leaves the current graph entirely.

### Error handling

Handle tool errors using LangChain agent [middleware](/oss/langchain/middleware) to retry failed tool calls or return custom error messages:

```python Google
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest

@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python OpenAI
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest

@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python Anthropic
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest

@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python OpenRouter
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest

@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python Fireworks
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest

@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python Baseten
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest

@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python Ollama
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest

@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[],
    middleware=[handle_tool_errors],
)
```

- [View example trace](https://smith.langchain.com/public/ab5801b7-dc0e-40c5-ac56-a55ac8c65af6/r)

  Open a public LangSmith run for this example.

### State injection

Tools access graph state through `ToolRuntime`. See [Access context](#access-context) for state, context, store, and streaming APIs.

```python
from langchain.tools import tool, ToolRuntime

@tool
def get_message_count(runtime: ToolRuntime) -> str:
    """Get the number of messages in the conversation."""
    messages = runtime.state["messages"]
    return f"There are {len(messages)} messages."
```

For more details on accessing state, context, and long-term memory from tools, see [Access context](#access-context).

## Dynamic tool selection

With dynamic tools, the set of tools available to the agent is modified at runtime rather than defined all upfront. Not every tool is appropriate for every situation. Too many tools may overwhelm the model (overload context) and increase errors; too few limit capabilities. Dynamic tool selection enables adapting the available toolset based on authentication state, user permissions, feature flags, or conversation stage.

There are two approaches depending on whether tools are known ahead of time:

**Filtering pre-registered tools**

When all possible tools are known at agent creation time, you can pre-register them and dynamically filter which ones are exposed to the model based on state, permissions, or context.

**State**

Enable advanced tools only after certain conversation milestones:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@wrap_model_call
def state_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on conversation State."""
    # Read from State: check if user has authenticated
    state = request.state
    is_authenticated = state.get("authenticated", False)
    message_count = len(state["messages"])

# Only enable sensitive tools after authentication
if not is_authenticated:
    tools = [t for t in request.tools if t.name.startswith("public_")]
    request = request.override(tools=tools)
elif message_count < 5:
    # Limit tools early in conversation
    tools = [t for t in request.tools if t.name != "advanced_search"]
    request = request.override(tools=tools)

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[public_search, private_search, advanced_search],
    middleware=[state_based_tools]
)
```

**Store**

Filter tools based on user preferences or feature flags in Store:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

@wrap_model_call
def store_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on Store preferences."""
    user_id = request.runtime.context.user_id

# Read from Store: get user's enabled features
store = request.runtime.store
feature_flags = store.get(("features",), user_id)

if feature_flags:
    enabled_features = feature_flags.value.get("enabled_tools", [])
    # Only include tools that are enabled for this user
    tools = [t for t in request.tools if t.name in enabled_features]
    request = request.override(tools=tools)

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[search_tool, analysis_tool, export_tool],
    middleware=[store_based_tools],
    context_schema=Context,
    store=InMemoryStore()
)
```

**Runtime Context**

Filter tools based on user permissions from Runtime Context:

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@dataclass
class Context:
    user_role: str

@wrap_model_call
def context_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on Runtime Context permissions."""
    # Read from Runtime Context: get user role
    if request.runtime is None or request.runtime.context is None:
        # If no context provided, default to viewer (most restrictive)
        user_role = "viewer"
    else:
        user_role = request.runtime.context.user_role

if user_role == "admin":
    # Admins get all tools
    pass
elif user_role == "editor":
    # Editors can't delete
    tools = [t for t in request.tools if t.name != "delete_data"]
    request = request.override(tools=tools)
else:
    # Viewers get read-only tools
    tools = [t for t in request.tools if t.name.startswith("read_")]
    request = request.override(tools=tools)

return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[read_data, write_data, delete_data],
    middleware=[context_based_tools],
    context_schema=Context
)
```

This approach is best when:
- All possible tools are known at compile/startup time
- You want to filter based on permissions, feature flags, or conversation state
- Tools are static but their availability is dynamic

    See [Dynamically selecting tools](/oss/langchain/middleware/custom#dynamically-selecting-tools) for more examples.

**Runtime tool registration**

When tools are discovered or created at runtime (e.g., loaded from an MCP server, generated based on user data, or fetched from a remote registry), you need to both register the tools and handle their execution dynamically.

This requires two middleware hooks:
1. `wrap_model_call` - Add the dynamic tools to the request
2. `wrap_tool_call` - Handle execution of the dynamically added tools

    ```python
    from langchain.tools import tool
    from langchain.agents import create_agent
    from langchain.agents.middleware import AgentMiddleware, ModelRequest, ToolCallRequest

# A tool that will be added dynamically at runtime
@tool
def calculate_tip(bill_amount: float, tip_percentage: float = 20.0) -> str:
    """Calculate the tip amount for a bill."""
    tip = bill_amount * (tip_percentage / 100)
    return f"Tip: ${tip:.2f}, Total: ${bill_amount + tip:.2f}"

class DynamicToolMiddleware(AgentMiddleware):
    """Middleware that registers and handles dynamic tools."""

def wrap_model_call(self, request: ModelRequest, handler):
    # Add dynamic tool to the request
    # This could be loaded from an MCP server, database, etc.
    updated = request.override(tools=[*request.tools, calculate_tip])
    return handler(updated)

def wrap_tool_call(self, request: ToolCallRequest, handler):
    # Handle execution of the dynamic tool
    if request.tool_call["name"] == "calculate_tip":
        return handler(request.override(tool=calculate_tip))
    return handler(request)

agent = create_agent(
    model="gpt-5.5",
    tools=[get_weather],  # Only static tools registered here
    middleware=[DynamicToolMiddleware()],
)

# The agent can now use both get_weather AND calculate_tip
result = agent.invoke({
    "messages": [{"role": "user", "content": "Calculate a 20% tip on $85"}]
})
```

This approach is best when:
- Tools are discovered at runtime (e.g., from an MCP server)
- Tools are generated dynamically based on user data or configuration
- You're integrating with external tool registries

**Note:**

The `wrap_tool_call` hook is required for runtime-registered tools because the agent needs to know how to execute tools that weren't in the original tool list. Without it, the agent won't know how to invoke the dynamically added tool.

## Headless tools

Some tools should run **where your user's app runs** (typically the browser), not inside the process. **Headless tools** are tool definitions, which include the name, description, and argument schema, that you register on the **server** with your agent. The **implementation** is registered only on the **client** and executed after a short interrupt/resume handshake.

This is different from ordinary tools whose function body runs on the server, and from [server-side tool use](#server-side-tool-use) where the model provider executes built-in tools remotely.

### When to use headless tools

Use them when the work depends on the **environment, device, or UI** that only exists on the client. For example:

- **Browser APIs:** Geolocation, IndexedDB, Clipboard, Canvas 2D, file pickers, Battery API, etc.
- **Privacy and locality:** Data stays on the device (for example, local “memory” in IndexedDB).
- **Latency:** No extra server round trip for purely local operations.
- **Structured, safe effects:** Prefer many small, typed tools (for example one tool per canvas primitive) instead of sending arbitrary code to `eval`.

### How the pattern works

In both runtimes, the model sees a normal tool it can call, but the actual execution happens outside the server process.

1. **Define** a headless tool with `tool(name=..., description=..., args_schema=...)` from `langchain.tools`. A headless tool is schema-only, with no in-process implementation.
2. **Register** that tool with `create_agent` or your LangGraph graph so the model can call it normally.
3. **Handle** the interrupt payload when the tool is invoked. Instead of running locally, the graph pauses with a payload shaped like `{"type": "tool", "tool_call": {"id", "name", "args"}}`.
4. **Resume** the graph after your app, another service, or a human step performs the action. For browser-based flows, you can mirror the schema in the frontend and attach `.implement(...)` there.

**Info:**

If you call `tool(...)` in Python with only `name`, `description`, and `args_schema`, LangChain returns a `HeadlessTool`. There is no `.implement()` API on the Python side.

When the model issues a tool call for one of these tools, the run **interrupts** instead of executing the tool locally. Your app can inspect the payload, perform the action in the right environment (for example a browser, another service, or a human review step), then **resume** the graph with the tool result. When you use the supported JS SDK hooks, they can detect headless-tool interrupts, run the matching client implementation, and submit the resume command for you.

Use the optional **`onTool`** callback to observe lifecycle events (`start`, `success`, `error`) for UI feedback such as spinners or toasts.

- [Headless tools frontend pattern](/oss/langchain/frontend/headless-tools)

    See an end-to-end example of schema-only tools executed in the client with `useStream`.

## Prebuilt tools

LangChain provides a large collection of prebuilt tools and toolkits for common tasks like web search, code interpretation, database access, and more. These ready-to-use tools can be directly integrated into your agents without writing custom code.

See the [tools and toolkits](/oss/integrations/tools) integration page for a complete list of available tools organized by category.

## Tools from MCP servers

[Model Context Protocol (MCP)](https://modelcontextprotocol.io) is an open protocol that standardizes how applications expose tools to language models. Rather than hand-authoring a tool, you connect to an MCP server and adapt the tools it advertises into LangChain tools, ready to pass to an agent like any other tool.

`MCPAdapter` discovers a server's tools and converts them into LangChain tools. Open the adapter, call `list_tools()`, and hand the result to `create_agent`:

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

async with MCPAdapter("https://example.com/mcp") as adapter:
    tools = await adapter.list_tools()
    agent = create_agent("claude-sonnet-4-6", tools)
```

**Note:**

The `langchain.mcp` namespace requires `langchain[mcp]>=1.4.0` and is in beta. The API may change.

For transports, authentication, multiple servers, and handling tool results, see [Model Context Protocol (MCP)](/oss/langchain/mcp).

## Server-side tool use

Some chat models feature built-in tools that are executed server-side by the model provider. These include capabilities like web search and code interpreters that don't require you to define or host the tool logic.

Refer to the individual [chat model integration pages](/oss/integrations/providers) and the [tool calling documentation](/oss/langchain/models#server-side-tool-use) for details on enabling and using these built-in tools.

---

# Agent Chat UI
> 출처: data/raw/langchain/ui.mdx | https://docs.langchain.com/oss/python/langchain/ui

[Agent Chat UI](https://github.com/langchain-ai/agent-chat-ui) is a Next.js application that provides a conversational interface for interacting with any LangChain agent. It supports real-time chat, tool visualization, and advanced features like time-travel debugging and state forking. Agent Chat UI works seamlessly with agents created using `create_agent` and provides interactive experiences for your agents with minimal setup, whether you're running locally or in a deployed context (such as [LangSmith](/langsmith/observability)).

Agent Chat UI is open source and can be adapted to your application needs.

<iframe
  className="w-full aspect-video rounded-xl"
  src="https://www.youtube.com/embed/lInrwVnZ83o?si=Uw66mPtCERJm0EjU"
  title="Agent Chat UI"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowFullScreen
/>

**Tip:**

You can use generative UI in the Agent Chat UI. For more information, see [Implement generative user interfaces with LangGraph](/langsmith/generative-ui-react).

### Quick start

The fastest way to get started is using the hosted version:

1. **Visit [Agent Chat UI](https://agentchat.vercel.app)**
2. **Connect your agent** by entering your deployment URL or local server address
3. **Start chatting** - the UI will automatically detect and render tool calls and interrupts

### Local development

For customization or local development, you can run Agent Chat UI locally:

```bash Use npx
# Create a new Agent Chat UI project
npx create-agent-chat-app --project-name my-chat-ui
cd my-chat-ui

# Install dependencies and start
pnpm install
pnpm dev
```
```bash Clone repository
# Clone the repository
git clone https://github.com/langchain-ai/agent-chat-ui.git
cd agent-chat-ui

# Install dependencies and start
pnpm install
pnpm dev
```

### Connect to your agent

Agent Chat UI can connect to both [local](/oss/langchain/studio) and [deployed agents](/oss/langchain/deploy).

After starting Agent Chat UI, you'll need to configure it to connect to your agent:

1. **Graph ID**: Enter your graph name (find this under `graphs` in your `langgraph.json` file)
2. **Deployment URL**: Your Agent server's endpoint (e.g., `http://localhost:2024` for local development, or your deployed agent's URL)
3. **LangSmith API key (optional)**: Add your LangSmith API key (not required if you're using a local Agent server)

Once configured, Agent Chat UI will automatically fetch and display any interrupted threads from your agent.

**Tip:**

Agent Chat UI has out-of-the-box support for rendering tool calls and tool result messages. To customize what messages are shown, see [Hiding Messages in the Chat](https://github.com/langchain-ai/agent-chat-ui?tab=readme-ov-file#hiding-messages-in-the-chat).

---

# Build a voice agent with LangChain
> 출처: data/raw/langchain/voice-agent.mdx | https://docs.langchain.com/oss/python/langchain/voice-agent

## Overview

Chat interfaces have dominated how we interact with AI, but recent breakthroughs in multimodal AI are opening up exciting new possibilities. High-quality generative models and expressive text-to-speech (TTS) systems now make it possible to build agents that feel less like tools and more like conversational partners.

Voice agents are one example of this. Instead of relying on a keyboard and mouse to type inputs into an agent, you can use spoken words to interact with it. This can be a more natural and engaging way to interact with AI, and can be especially useful for certain contexts.

### What are voice agents?

Voice agents are [agents](/oss/langchain/agents) that can engage in natural spoken conversations with users. These agents combine speech recognition, natural language processing, generative AI, and text-to-speech technologies to create seamless, natural conversations.

They're suited for a variety of use cases, including:

- Customer support
- Personal assistants
- Hands-free interfaces
- Coaching and training

### How do voice agents work?

At a high level, every voice agent needs to handle three tasks:

1. **Listen** - capture audio and transcribe it
2. **Think** - interpret intent, reason, plan
3. **Speak** - generate audio and stream it back to the user

The difference lies in how these steps are sequenced and coupled. In practice, production agents follow one of two main architectures:

#### 1. STT > Agent > TTS architecture (The "Sandwich")

The Sandwich architecture composes three distinct components: speech-to-text (STT), a text-based LangChain agent, and text-to-speech (TTS).

```mermaid
flowchart LR
    A[User Audio] --> B[Speech-to-Text]
    B --> C[LangChain Agent]
    C --> D[Text-to-Speech]
    D --> E[Audio Output]

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,E trigger
    class B,C,D process
```

**Pros:**
- Full control over each component (swap STT/TTS providers as needed)
- Access to latest capabilities from modern text-modality models
- Transparent behavior with clear boundaries between components

**Cons:**
- Requires orchestrating multiple services
- Additional complexity in managing the pipeline
- Conversion from speech to text loses information (e.g., tone, emotion)

#### 2. Speech-to-Speech architecture (S2S)

Speech-to-speech uses a multimodal model that processes audio input and generates audio output natively.

```mermaid
flowchart LR
    A[User Audio] --> B[Multimodal Model]
    B --> C[Audio Output]

classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,C trigger
    class B process
```

**Pros:**
- Simpler architecture with fewer moving parts
- Typically lower latency for simple interactions
- Direct audio processing captures tone and other nuances of speech

**Cons:**
- Limited model options, greater risk of provider lock-in
- Features may lag behind text-modality models
- Less transparency in how audio is processed
- Reduced controllability and customization options

This guide demonstrates the **sandwich architecture** to balance performance, controllability, and access to modern model capabilities. The sandwich can achieve sub-700ms latency with some STT and TTS providers while maintaining control over modular components.

### Demo Application overview

We'll walk through building a voice-based agent using the sandwich architecture. The agent will manage orders for a sandwich shop. The application will demonstrate all three components of the sandwich architecture, using [AssemblyAI](https://www.assemblyai.com/) for STT and [Cartesia](https://cartesia.ai/) for TTS (although adapters can be built for most providers).

An end-to-end reference application is available in the [voice-sandwich-demo](https://github.com/langchain-ai/voice-sandwich-demo) repository. We will walk through that application here.

The demo uses WebSockets for real-time bidirectional communication between the browser and server. The same architecture can be adapted for other transports like telephony systems (Twilio, Vonage) or WebRTC connections.

### Architecture

The demo implements a streaming pipeline where each stage processes data asynchronously:

**Client (Browser)**
- Captures microphone audio and encodes it as PCM
- Establishes WebSocket connection to the backend server
- Streams audio chunks to the server in real-time
- Receives and plays back synthesized speech audio

**Server (Python)**

- Accepts WebSocket connections from clients
- Orchestrates the three-step pipeline:
  - [Speech-to-text (STT)](#1-speech-to-text): Forwards audio to the STT provider (e.g., AssemblyAI), receives transcript events
  - [Agent](#2-langchain-agent): Processes transcripts with LangChain agent, streams response tokens
  - [Text-to-speech (TTS)](#3-text-to-speech): Sends agent responses to the TTS provider (e.g., Cartesia), receives audio chunks

- Returns synthesized audio to the client for playback

The pipeline uses async generators to enable streaming at each stage. This allows downstream components to begin processing before upstream stages complete, minimizing end-to-end latency.

## Setup

For detailed installation instructions and setup, see the [repository README](https://github.com/langchain-ai/voice-sandwich-demo#readme).

## 1. Speech-to-text

The STT stage transforms an incoming audio stream into text transcripts. The implementation uses a producer-consumer pattern to handle audio streaming and transcript reception concurrently.

### Key concepts

**Producer-Consumer Pattern**: Audio chunks are sent to the STT service concurrently with receiving transcript events. This allows transcription to begin before all audio has arrived.

**Event Types**:
- `stt_chunk`: Partial transcripts provided as the STT service processes audio
- `stt_output`: Final, formatted transcripts that trigger agent processing

**WebSocket Connection**: Maintains a persistent connection to AssemblyAI's real-time STT API, configured for 16kHz PCM audio with automatic turn formatting.

### Implementation

```python
from typing import AsyncIterator
import asyncio
from assemblyai_stt import AssemblyAISTT
from events import VoiceAgentEvent

async def stt_stream(
    audio_stream: AsyncIterator[bytes],
) -> AsyncIterator[VoiceAgentEvent]:
    """
    Transform stream: Audio (Bytes) → Voice Events (VoiceAgentEvent)

Uses a producer-consumer pattern where:
- Producer: Reads audio chunks and sends them to AssemblyAI
- Consumer: Receives transcription events from AssemblyAI
"""
stt = AssemblyAISTT(sample_rate=16000)

async def send_audio():
    """Background task that pumps audio chunks to AssemblyAI."""
    try:
        async for audio_chunk in audio_stream:
            await stt.send_audio(audio_chunk)
    finally:
        # Signal completion when audio stream ends
        await stt.close()

# Launch audio sending in background
send_task = asyncio.create_task(send_audio())

    try:
        # Receive and yield transcription events as they arrive
        async for event in stt.receive_events():
            yield event
    finally:
        # Cleanup
        with contextlib.suppress(asyncio.CancelledError):
            send_task.cancel()
            await send_task
        await stt.close()
```

The application implements an AssemblyAI client to manage the WebSocket connection and message parsing. See below for implementations; similar adapters can be constructed for other STT providers.

**AssemblyAI Client**

```python
class AssemblyAISTT:
    def __init__(self, api_key: str | None = None, sample_rate: int = 16000):
        self.api_key = api_key or os.getenv("ASSEMBLYAI_API_KEY")
        self.sample_rate = sample_rate
        self._ws: WebSocketClientProtocol | None = None

async def send_audio(self, audio_chunk: bytes) -> None:
    """Send PCM audio bytes to AssemblyAI."""
    ws = await self._ensure_connection()
    await ws.send(audio_chunk)

async def receive_events(self) -> AsyncIterator[STTEvent]:
    """Yield STT events as they arrive from AssemblyAI."""
    async for raw_message in self._ws:
        message = json.loads(raw_message)

if message["type"] == "Turn":
    # Final formatted transcript
    if message.get("turn_is_formatted"):
        yield STTOutputEvent.create(message["transcript"])
    # Partial transcript
    else:
        yield STTChunkEvent.create(message["transcript"])

    async def _ensure_connection(self) -> WebSocketClientProtocol:
        """Establish WebSocket connection if not already connected."""
        if self._ws is None:
            url = f"wss://streaming.assemblyai.com/v3/ws?sample_rate={self.sample_rate}&format_turns=true"
            self._ws = await websockets.connect(
                url,
                additional_headers={"Authorization": self.api_key}
            )
        return self._ws
```

## 2. LangChain agent

The agent stage processes text transcripts through a LangChain [agent](/oss/langchain/agents) and streams the response tokens. In this case, we stream all [text content blocks](/oss/langchain/messages#content-block-reference) generated by the agent.

### Key concepts

**Streaming Responses**: The agent uses [`stream_events(version="v3")`](/oss/langchain/streaming) with `stream.messages` to emit response tokens as they are generated, rather than waiting for the complete response. This enables the TTS stage to begin synthesis immediately.

**Conversation Memory**: A [checkpointer](/oss/langchain/short-term-memory) maintains conversation state across turns using a unique thread ID. This allows the agent to reference previous exchanges in the conversation.

### Implementation

```python
from langchain_core.utils.uuid import uuid7
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

# Define agent tools
def add_to_order(item: str, quantity: int) -> str:
    """Add an item to the customer's sandwich order."""
    return f"Added {quantity} x {item} to the order."

def confirm_order(order_summary: str) -> str:
    """Confirm the final order with the customer."""
    return f"Order confirmed: {order_summary}. Sending to kitchen."

# Create agent with tools and memory
agent = create_agent(
    model="google_genai:gemini-3.6-flash",  # Select your model
    tools=[add_to_order, confirm_order],
    system_prompt="""You are a helpful sandwich shop assistant.
    Your goal is to take the user's order. Be concise and friendly.
    Do NOT use emojis, special characters, or markdown.
    Your responses will be read by a text-to-speech engine.""",
    checkpointer=InMemorySaver(),
)

async def agent_stream(
    event_stream: AsyncIterator[VoiceAgentEvent],
) -> AsyncIterator[VoiceAgentEvent]:
    """
    Transform stream: Voice Events → Voice Events (with Agent Responses)

Passes through all upstream events and adds agent_chunk events
when processing STT transcripts.
"""
# Generate unique thread ID for conversation memory
thread_id = str(uuid7())

async for event in event_stream:
    # Pass through all upstream events
    yield event

# Process final transcripts through the agent
if event.type == "stt_output":
    # Stream agent response with conversation context
    stream = await agent.astream_events(
        {"messages": [HumanMessage(content=event.transcript)]},
        {"configurable": {"thread_id": thread_id}},
        version="v3",
    )

            # Yield agent response chunks as they arrive
            async for message in stream.messages:
                async for token in message.text:
                    yield AgentChunkEvent.create(token)
```

## 3. Text-to-speech

The TTS stage synthesizes agent response text into audio and streams it back to the client. Like the STT stage, it uses a producer-consumer pattern to handle concurrent text sending and audio reception.

### Key concepts

**Concurrent Processing**: The implementation merges two async streams:
- **Upstream processing**: Passes through all events and sends agent text chunks to the TTS provider
- **Audio reception**: Receives synthesized audio chunks from the TTS provider

**Streaming TTS**: Some providers (such as [Cartesia](https://cartesia.ai/)) begin synthesizing audio as soon as it receives text, enabling audio playback to start before the agent finishes generating its complete response.

**Event Passthrough**: All upstream events flow through unchanged, allowing the client or other observers to track the full pipeline state.

### Implementation

```python
from cartesia_tts import CartesiaTTS
from utils import merge_async_iters

async def tts_stream(
    event_stream: AsyncIterator[VoiceAgentEvent],
) -> AsyncIterator[VoiceAgentEvent]:
    """
    Transform stream: Voice Events → Voice Events (with Audio)

Merges two concurrent streams:
1. process_upstream(): passes through events and sends text to Cartesia
2. tts.receive_events(): yields audio chunks from Cartesia
"""
tts = CartesiaTTS()

async def process_upstream() -> AsyncIterator[VoiceAgentEvent]:
    """Process upstream events and send agent text to Cartesia."""
    async for event in event_stream:
        # Pass through all events
        yield event
        # Send agent text to Cartesia for synthesis
        if event.type == "agent_chunk":
            await tts.send_text(event.text)

    try:
        # Merge upstream events with TTS audio events
        # Both streams run concurrently
        async for event in merge_async_iters(
            process_upstream(),
            tts.receive_events()
        ):
            yield event
    finally:
        await tts.close()
```

The application implements a Cartesia client to manage the WebSocket connection and audio streaming. See below for implementations; similar adapters can be constructed for other TTS providers.

**Cartesia Client**

```python
import base64
import json
import websockets

class CartesiaTTS:
    def __init__(
        self,
        api_key: Optional[str] = None,
        voice_id: str = "f6ff7c0c-e396-40a9-a70b-f7607edb6937",
        model_id: str = "sonic-3",
        sample_rate: int = 24000,
        encoding: str = "pcm_s16le",
    ):
        self.api_key = api_key or os.getenv("CARTESIA_API_KEY")
        self.voice_id = voice_id
        self.model_id = model_id
        self.sample_rate = sample_rate
        self.encoding = encoding
        self._ws: WebSocketClientProtocol | None = None

def _generate_context_id(self) -> str:
    """Generate a valid context_id for Cartesia."""
    timestamp = int(time.time() * 1000)
    counter = self._context_counter
    self._context_counter += 1
    return f"ctx_{timestamp}_{counter}"

async def send_text(self, text: str | None) -> None:
    """Send text to Cartesia for synthesis."""
    if not text or not text.strip():
        return

ws = await self._ensure_connection()
payload = {
    "model_id": self.model_id,
    "transcript": text,
    "voice": {
        "mode": "id",
        "id": self.voice_id,
    },
    "output_format": {
        "container": "raw",
        "encoding": self.encoding,
        "sample_rate": self.sample_rate,
    },
    "language": self.language,
    "context_id": self._generate_context_id(),
}
await ws.send(json.dumps(payload))

async def receive_events(self) -> AsyncIterator[TTSChunkEvent]:
    """Yield audio chunks as they arrive from Cartesia."""
    async for raw_message in self._ws:
        message = json.loads(raw_message)

# Decode and yield audio chunks
if "data" in message and message["data"]:
    audio_chunk = base64.b64decode(message["data"])
    if audio_chunk:
        yield TTSChunkEvent.create(audio_chunk)

async def _ensure_connection(self) -> WebSocketClientProtocol:
    """Establish WebSocket connection if not already connected."""
    if self._ws is None:
        url = (
            f"wss://api.cartesia.ai/tts/websocket"
            f"?api_key={self.api_key}&cartesia_version={self.cartesia_version}"
        )
        self._ws = await websockets.connect(url)

        return self._ws
```

### LangSmith

Many of the applications you build with LangChain will contain multiple steps with multiple invocations of LLM calls. As these applications get more complex, it becomes crucial to be able to inspect what exactly is going on inside your chain or agent. The best way to do this is with [LangSmith](https://smith.langchain.com).

After you sign up at the link above, make sure to set your environment variables to start logging traces:

```shell
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```

Or, set them in Python:

```python
import getpass
import os

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass()
```

## Putting it all together

The complete pipeline chains the three stages together:

```python
from langchain_core.runnables import RunnableGenerator

pipeline = (
    RunnableGenerator(stt_stream)      # Audio → STT events
    | RunnableGenerator(agent_stream)  # STT events → Agent events
    | RunnableGenerator(tts_stream)    # Agent events → TTS audio
)

# Use in WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

async def websocket_audio_stream():
    """Yield audio bytes from WebSocket."""
    while True:
        data = await websocket.receive_bytes()
        yield data

# Transform audio through pipeline
output_stream = pipeline.atransform(websocket_audio_stream())

    # Send TTS audio back to client
    async for event in output_stream:
        if event.type == "tts_chunk":
            await websocket.send_bytes(event.audio)
```

We use [RunnableGenerators](https://reference.langchain.com/python/langchain-core/runnables) to compose each step of the pipeline. This is an abstraction LangChain uses internally to manage [streaming across components](https://reference.langchain.com/python/langchain-core/runnables).

Each stage processes events independently and concurrently: audio transcription begins as soon as audio arrives, the agent starts reasoning as soon as a transcript is available, and speech synthesis begins as soon as agent text is generated. This architecture can achieve sub-700ms latency to support natural conversation.

For more on building agents with LangChain, see the [Agents guide](/oss/langchain/agents).