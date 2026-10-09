import re
from urllib.parse import urlsplit

from langchain_core.messages import AIMessage

from src.const.models import create_openai_model
from src.graph.chat_service import text_content
from src.prompt.answer_prompt import ANSWER_SYSTEM_PROMPT


def document_context(docs):
    blocks = []
    for index, doc in enumerate(docs, 1):
        meta = doc.metadata
        source = meta.get("source_url") or meta.get("source", "")
        blocks.append(f"[{index}] {meta.get('title', '')} | {source}\n{doc.page_content}")
    return "\n\n---\n\n".join(blocks)


def cited_sources(text, docs):
    """Return only retrieved documents explicitly cited as [n] in the answer."""
    sources, seen = [], set()
    for match in re.finditer(r"\[(\d+)\]", text):
        index = int(match.group(1)) - 1
        if index < 0 or index >= len(docs):
            continue
        doc = docs[index]
        meta = doc.metadata
        url = meta.get("source_url")
        if not isinstance(url, str):
            continue
        parsed = urlsplit(url)
        if parsed.scheme not in ("https", "http") or not parsed.netloc or url in seen:
            continue
        seen.add(url)
        score = meta.get("score")
        sources.append({
            "url": url, "title": meta.get("title") or url,
            "tech": meta.get("technology"), "version": meta.get("version"),
            "doc_type": meta.get("document_type"), "snippet": doc.page_content[:800],
            "score": score if isinstance(score, (int, float)) else None,
        })
    return sources


def answer_node(state):
    docs = state.get("retrieved_docs", [])
    if state.get("route") == "rag" and not docs:
        answer = "검색한 문서에서 질문에 대한 근거를 찾지 못했습니다. 기술명이나 오류 메시지를 더 구체적으로 알려주세요."
        return {"messages": [AIMessage(content=answer)], "answer": answer, "sources": []}
    model = create_openai_model(timeout=60)
    response = model.invoke([
        {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
        *state["messages"],
        {"role": "user", "content": str({
            "original_question": state["original_question"],
            "image_analysis": state.get("image_analysis", ""),
            "retrieved_context": document_context(docs),
            "mcp_results": state.get("mcp_results", []),
        })},
    ])
    answer = text_content(response.content)
    return {"messages": [response], "answer": answer, "sources": cited_sources(answer, docs)}
