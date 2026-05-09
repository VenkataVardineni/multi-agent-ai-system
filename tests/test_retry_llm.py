from unittest.mock import patch

import httpx

from multi_agent.llm.protocol import ChatResult
from multi_agent.llm.retry import RetryingChatClient


class FlakyClient:
    def __init__(self) -> None:
        self.calls = 0

    def chat(self, messages, tools):
        self.calls += 1
        if self.calls == 1:
            raise httpx.ConnectError("boom", request=httpx.Request("POST", "http://example"))
        return ChatResult(content="ok", tool_calls=())


def test_retrying_client_recovers():
    inner = FlakyClient()
    retrying = RetryingChatClient(inner, attempts=3, base_delay=0.01, max_delay=0.05)

    with patch("multi_agent.llm.retry.time.sleep", return_value=None):
        result = retrying.chat((), None)

    assert result.content == "ok"
    assert inner.calls == 2
