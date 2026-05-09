from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from multi_agent.llm.protocol import ChatResult


class MockLLM:
    """Deterministic fake LLM for tests and offline demos."""

    def __init__(
        self,
        responses: Sequence[ChatResult] | None = None,
        responder: Callable[[Sequence[dict[str, Any]]], ChatResult] | None = None,
    ) -> None:
        self._responses = list(responses or [])
        self._responder = responder
        self._idx = 0

    def reset(self) -> None:
        """Rewind scripted responses for repeatable tests."""

        self._idx = 0

    def chat(
        self,
        messages: Sequence[dict[str, Any]],
        tools: Sequence[dict[str, Any]] | None,
    ) -> ChatResult:
        if self._responder is not None:
            return self._responder(messages)
        if self._idx >= len(self._responses):
            return ChatResult(content="mock-final", tool_calls=())
        result = self._responses[self._idx]
        self._idx += 1
        return result
