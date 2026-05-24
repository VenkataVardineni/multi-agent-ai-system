import pytest

from multi_agent.llm.openai_client import OpenAICompatClient


def test_openai_client_missing_key():
    client = OpenAICompatClient(api_key="")
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        client.chat([{"role": "user", "content": "hi"}], None)

