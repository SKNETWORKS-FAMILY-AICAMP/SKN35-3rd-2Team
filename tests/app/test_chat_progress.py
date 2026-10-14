from unittest.mock import Mock

import pytest
from langchain_core.messages import AIMessage, AIMessageChunk

from src.app.chat_service import run_chat
from src.graph.progress import START, NEXT, BY_ROUTE


@pytest.mark.parametrize('with_tokens', [False, True])
def test_stage_stream_preserves_answer_and_filters_internal_tokens(with_tokens):
    graph = Mock()
    graph.stream.return_value = iter([
        ('updates', {'supervisor': {'route': 'rag'}}),
        ('messages', (AIMessageChunk(content='internal'), {'langgraph_node': 'supervisor'})),
        ('updates', {'rag': {'retrieved_docs': []}}),
        ('updates', {'supervisor': {'route': 'answer'}}),
        ('messages', (AIMessageChunk(content='answer'), {'langgraph_node': 'answer'})),
        ('updates', {'answer': {'route': 'end', 'answer': 'answer', 'messages': [AIMessage(content='answer')]}}),
    ])
    stages, tokens = [], []
    result = run_chat([{'role': 'user', 'content': 'question'}], graph=graph,
                      on_stage=stages.append, on_token=tokens.append if with_tokens else None)
    assert result['status'] == 'success' and result['answer'] == 'answer'
    assert stages == [START, BY_ROUTE['rag'], NEXT, BY_ROUTE['answer']]
    assert tokens == (['answer'] if with_tokens else [])
    graph.invoke.assert_not_called()
