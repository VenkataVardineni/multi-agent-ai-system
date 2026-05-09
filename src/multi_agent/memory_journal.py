from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MemoryEvent:
    kind: str
    key: str | None
    payload: dict[str, Any]


class MemoryJournal:
    """Append-only ring buffer for observability around shared memory writes."""

    def __init__(self, max_events: int = 256) -> None:
        self._max_events = max(16, max_events)
        self._events: deque[MemoryEvent] = deque(maxlen=self._max_events)

    def record(self, kind: str, key: str | None = None, **payload: Any) -> None:
        event = MemoryEvent(
            kind=kind,
            key=key,
            payload={"ts": time.time(), **payload},
        )
        self._events.append(event)

    def tail(self, limit: int = 50) -> list[MemoryEvent]:
        items = list(self._events)
        if limit >= len(items):
            return items
        return items[-limit:]
