import httpx
import pytest

from multi_agent.llm.mock import MockLLM
from multi_agent.llm.protocol import ChatResult
from multi_agent.llm.retry import RetryingChatClient


class FlakyLLM:
    def __init__(self):
        self.calls = 0

    def chat(self, messages, tools):
        self.calls += 1
        raise httpx.ConnectError("down", request=httpx.Request("GET", "https://x"))


def test_retry_exhausts_attempts():
    inner = FlakyLLM()
    client = RetryingChatClient(inner, attempts=2, base_delay=0.01, max_delay=0.02)
    with pytest.raises(httpx.ConnectError):
        client.chat([], None)
    assert inner.calls == 2

