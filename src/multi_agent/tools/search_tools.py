from __future__ import annotations

from typing import Any

import httpx

from multi_agent.tools.registry import ToolContext, ToolDefinition


def _web_search_stub(ctx: ToolContext, args: dict[str, Any]) -> str:
    query = str(args["query"])
    return (
        f"[stub] No live web search configured. "
        f"Echo query for offline demos: {query!r}. "
        "Set OPENAI_API_KEY and use the Research agent for synthesis."
    )


def _fetch_url_text(ctx: ToolContext, args: dict[str, Any]) -> str:
    url = str(args["url"])
    timeout = float(args.get("timeout_seconds", 15.0))
    max_bytes = int(args.get("max_bytes", 200_000))
    headers = {"User-Agent": "multi-agent/0.2 (+https://example.local)"}
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            raw = response.content[:max_bytes]
    except httpx.HTTPError as exc:
        return f"error:http:{exc}"
    if b"\x00" in raw[:1024]:
        return "error:response appears binary"
    return raw.decode("utf-8", errors="replace")


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
        ),
        ToolDefinition(
            name="fetch_url_text",
            description=(
                "HTTP GET a URL and return UTF-8 text (truncated). "
                "Use for lightweight research fetches."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "timeout_seconds": {"type": "number"},
                    "max_bytes": {"type": "integer"},
                },
                "required": ["url"],
            },
            handler=_fetch_url_text,
        ),
    ]
