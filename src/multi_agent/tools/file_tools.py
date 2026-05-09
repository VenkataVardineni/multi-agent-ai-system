from __future__ import annotations

from pathlib import Path
from typing import Any

from multi_agent.tools.registry import ToolContext, ToolDefinition


def _safe_join(workspace: str | None, rel_path: str) -> Path:
    base = Path(workspace or ".").resolve()
    target = (base / rel_path).resolve()
    if not str(target).startswith(str(base)):
        raise ValueError("path escapes workspace")
    return target


def _read_text_file(ctx: ToolContext, args: dict[str, Any]) -> str:
    rel = str(args["path"])
    max_bytes = int(args.get("max_bytes", 50_000))
    path = _safe_join(ctx.workspace_dir, rel)
    if not path.is_file():
        return f"error: not a file: {path}"
    data = path.read_bytes()[:max_bytes]
    return data.decode("utf-8", errors="replace")


def file_tool_definitions() -> list[ToolDefinition]:
    return [
        ToolDefinition(
            name="read_text_file",
            description="Read a UTF-8 text file relative to the workspace directory.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "max_bytes": {"type": "integer"},
                },
                "required": ["path"],
            },
            handler=_read_text_file,
        )
    ]
