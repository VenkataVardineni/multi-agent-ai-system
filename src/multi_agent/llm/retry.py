from __future__ import annotations

import random
import time
from collections.abc import Sequence
from typing import Any

import httpx

from multi_agent.llm.protocol import ChatClient, ChatResult


class RetryingChatClient:
    """Wraps a ChatClient with exponential backoff for transient HTTP failures."""

    def __init__(
        self,
        inner: ChatClient,
        *,
        attempts: int = 3,
        base_delay: float = 0.4,
        max_delay: float = 6.0,
    ) -> None:
        self._inner = inner
        self._attempts = max(1, attempts)
        self._base_delay = max(0.05, base_delay)
        self._max_delay = max(self._base_delay, max_delay)

    def chat(
        self,
        messages: Sequence[dict[str, Any]],
        tools: Sequence[dict[str, Any]] | None,
    ) -> ChatResult:
        last_exc: Exception | None = None
        for attempt in range(self._attempts):
            try:
                return self._inner.chat(messages, tools)
            except httpx.HTTPError as exc:
                last_exc = exc
                if attempt >= self._attempts - 1:
                    break
                delay = min(
                    self._max_delay,
                    self._base_delay * (2**attempt) + random.random() * 0.1,
                )
                time.sleep(delay)
        assert last_exc is not None
        raise last_exc
