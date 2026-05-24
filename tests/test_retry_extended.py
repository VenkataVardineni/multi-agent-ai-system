import httpx
import pytest

from multi_agent.llm.retry import RetryingChatClient


class FlakyOnce:
    def __init__(self):
        self.calls = 0

    def chat(self, messages, tools):
        self.calls += 1
        if self.calls == 1:
            raise httpx.ConnectError("down", request=httpx.Request("GET", "https://x"))
        return __import__("multi_agent.llm.protocol", fromlist=["ChatResult"]).ChatResult(
            content="ok", tool_calls=()
        )


def test_retry_respects_max_delay(monkeypatch):
    sleeps = []
    monkeypatch.setattr(
        "multi_agent.llm.retry.time.sleep", lambda s: sleeps.append(s)
    )
    client = RetryingChatClient(FlakyOnce(), attempts=2, base_delay=0.4, max_delay=0.5)
    client.chat([], None)
    assert sleeps and sleeps[0] <= 0.5

