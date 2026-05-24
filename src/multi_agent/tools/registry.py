from __future__ import annotations

import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from multi_agent.exceptions import ToolExecutionError
from multi_agent.memory import SharedMemory


@dataclass
class ToolContext:
    """Execution context passed into every tool handler."""

    memory: SharedMemory
    workspace_dir: str | None = None


ToolHandler = Callable[[ToolContext, Mapping[str, Any]], Any]


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    parameters: Mapping[str, Any]
    handler: ToolHandler


class ToolRegistry:
    """Maps tool names to schemas and Python handlers."""

    def __init__(self, definitions: Sequence[ToolDefinition] | None = None) -> None:
        self._defs: dict[str, ToolDefinition] = {}
        if definitions:
            for d in definitions:
                self.register(d)

    def register(self, definition: ToolDefinition) -> None:
        self._defs[definition.name] = definition

    def unregister(self, name: str) -> None:
        self._defs.pop(name, None)

    def get(self, name: str) -> ToolDefinition:
        if name not in self._defs:
            raise KeyError(f"unknown tool: {name}")
        return self._defs[name]

    def definitions(self) -> list[ToolDefinition]:
        return list(self._defs.values())

    def tool_names(self) -> list[str]:
        return sorted(self._defs.keys())

    def execute(self, name: str, arguments_json: str, ctx: ToolContext) -> str:
        definition = self.get(name)
        try:
            args = json.loads(arguments_json or "{}")
        except json.JSONDecodeError as exc:
            raise ToolExecutionError(f"invalid JSON for {name}: {exc}") from exc
        if not isinstance(args, dict):
            raise ToolExecutionError("tool arguments must be a JSON object")
        try:
            result = definition.handler(ctx, args)
        except ToolExecutionError:
            raise
        except Exception as exc:  # noqa: BLE001 — surface as tool error
            raise ToolExecutionError(f"{name} failed: {exc}") from exc
        if isinstance(result, str):
            return result
        return json.dumps(result, ensure_ascii=False, default=str)

    def openai_tools_payload(self) -> list[dict[str, Any]]:
        payload: list[dict[str, Any]] = []
        for d in self.definitions():
            payload.append(
                {
                    "type": "function",
                    "function": {
                        "name": d.name,
                        "description": d.description,
                        "parameters": dict(d.parameters),
                    },
                }
            )
        return payload
