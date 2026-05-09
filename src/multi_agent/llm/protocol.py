from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, Sequence


@dataclass(frozen=True)
class ToolCallSpec:
    id: str
    name: str
    arguments: str


@dataclass(frozen=True)
class ChatResult:
    content: str | None
    tool_calls: tuple[ToolCallSpec, ...]


class ChatClient(Protocol):
    def chat(
        self,
        messages: Sequence[dict[str, Any]],
        tools: Sequence[dict[str, Any]] | None,
    ) -> ChatResult:
        """Return the assistant message for the provided conversation."""
