from __future__ import annotations

from typing import Any

from multi_agent.tools.registry import ToolContext, ToolDefinition


def _web_search_stub(ctx: ToolContext, args: dict[str, Any]) -> str:
    query = str(args["query"])
    return (
        f"[stub] No live web search configured. "
        f"Echo query for offline demos: {query!r}. "
        "Set OPENAI_API_KEY and use the Research agent for synthesis."
    )


def search_tool_definitions() -> list[ToolDefinition]:
    return [
        ToolDefinition(
            name="web_search_stub",
            description=(
                "Offline-friendly placeholder for web search. "
                "Returns an echo of the query unless wired to a real provider."
            ),
            parameters={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
            handler=_web_search_stub,
        )
    ]
