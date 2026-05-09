from __future__ import annotations

import copy
import threading
from typing import Any

from multi_agent.constants import GLOBAL_MEMORY_NS


class SharedMemory:
    """Thread-safe key/value memory shared across agents in a session."""

    def __init__(self, namespace: str = GLOBAL_MEMORY_NS) -> None:
        self._namespace = namespace
        self._data: dict[str, Any] = {}
        self._lock = threading.RLock()

    @property
    def namespace(self) -> str:
        return self._namespace

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = value

    def update(self, other: dict[str, Any]) -> None:
        with self._lock:
            self._data.update(other)

    def merge_snapshot(self, snapshot: dict[str, Any]) -> None:
        self.update(snapshot)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self._data)

    def keys(self) -> list[str]:
        with self._lock:
            return list(self._data.keys())

    def __contains__(self, key: str) -> bool:
        with self._lock:
            return key in self._data
