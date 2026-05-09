from __future__ import annotations

from typing import Any

from multi_agent.tools.registry import ToolContext, ToolDefinition


def _memory_get(ctx: ToolContext, args: dict[str, Any]) -> str:
    key = str(args["key"])
    default = args.get("default")
    value = ctx.memory.get(key, default)
    return str(value)


def _memory_set(ctx: ToolContext, args: dict[str, Any]) -> str:
    key = str(args["key"])
    value = args["value"]
    ctx.memory.set(key, value)
    return f"stored:{key}"


def memory_tool_definitions() -> list[ToolDefinition]:
    return [
        ToolDefinition(
            name="memory_get",
            description="Read a value from shared session memory by key.",
            parameters={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "default": {},
                },
                "required": ["key"],
            },
            handler=_memory_get,
        ),
        ToolDefinition(
            name="memory_set",
            description="Persist a JSON-serializable value into shared session memory.",
            parameters={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "value": {},
                },
                "required": ["key", "value"],
            },
            handler=_memory_set,
        ),
    ]
