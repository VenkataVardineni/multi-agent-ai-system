from multi_agent.llm.mock import MockLLM
from multi_agent.llm.protocol import ChatResult


def test_mock_llm_reset():
    llm = MockLLM(responses=[ChatResult(content="first", tool_calls=()), ChatResult(content="second", tool_calls=())])
    assert llm.chat([], None).content == "first"
    assert llm.chat([], None).content == "second"
    llm.reset()
    assert llm.chat([], None).content == "first"

