from __future__ import annotations

import json
import os
from typing import Any, Sequence

import httpx

from multi_agent.constants import DEFAULT_MODEL
from multi_agent.llm.protocol import ChatResult, ToolCallSpec


class OpenAICompatClient:
    """Minimal OpenAI-compatible chat completions client with tool calling."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        timeout: float = 120.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model or os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.timeout = timeout

    def chat(
        self,
        messages: Sequence[dict[str, Any]],
        tools: Sequence[dict[str, Any]] | None,
    ) -> ChatResult:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")

        url = f"{self.base_url}/chat/completions"
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": list(messages),
            "temperature": 0.2,
        }
        if tools:
            payload["tools"] = list(tools)
            payload["tool_choice"] = "auto"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=headers, content=json.dumps(payload))
            response.raise_for_status()
            data = response.json()

        choice = data["choices"][0]["message"]
        content = choice.get("content")
        raw_calls = choice.get("tool_calls") or []
        tool_calls: list[ToolCallSpec] = []
        for call in raw_calls:
            fn = call["function"]
            tool_calls.append(
                ToolCallSpec(
                    id=call["id"],
                    name=fn["name"],
                    arguments=fn.get("arguments") or "{}",
                )
            )
        return ChatResult(content=content, tool_calls=tuple(tool_calls))
