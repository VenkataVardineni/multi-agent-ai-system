from __future__ import annotations

import json
import os
import tempfile
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
    if b"\x00" in data[:1024]:
        return "error: file appears binary"
    return data.decode("utf-8", errors="replace")


def _stat_workspace_path(ctx: ToolContext, args: dict[str, Any]) -> str:
    rel = str(args["path"])
    path = _safe_join(ctx.workspace_dir, rel)
    exists = path.exists()
    payload = {
        "path": str(path),
        "exists": exists,
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
    }
    if exists:
        stat = path.stat()
        payload.update(
            {
                "size": stat.st_size,
                "mtime": stat.st_mtime,
            }
        )
    return json.dumps(payload, ensure_ascii=False)


def _list_workspace_entries(ctx: ToolContext, args: dict[str, Any]) -> str:
    rel = str(args.get("path", "."))
    recursive = bool(args.get("recursive", False))
    limit = int(args.get("limit", 200))
    root = _safe_join(ctx.workspace_dir, rel)
    if not root.is_dir():
        return json.dumps({"error": f"not a directory: {root}"})
    entries: list[str] = []
    if recursive:
        for idx, item in enumerate(sorted(root.rglob("*"))):
            if idx >= limit:
                break
            try:
                rel_item = item.relative_to(root)
            except ValueError:
                continue
            entries.append(str(rel_item))
    else:
        for idx, child in enumerate(sorted(root.iterdir())):
            if idx >= limit:
                break
            entries.append(child.name)
    return json.dumps({"root": str(root), "entries": entries}, ensure_ascii=False)


def _write_workspace_text_file(ctx: ToolContext, args: dict[str, Any]) -> str:
    rel = str(args["path"])
    content = str(args["content"])
    path = _safe_join(ctx.workspace_dir, rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".multi-agent-", text=True)
    os.close(fd)
    tmp = Path(tmp_path)
    try:
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)
    return f"wrote:{path}"


def _glob_workspace_files(ctx: ToolContext, args: dict[str, Any]) -> str:
    pattern = str(args["pattern"])
    limit = int(args.get("limit", 200))
    base = Path(ctx.workspace_dir or ".").resolve()
    matches: list[str] = []
    for idx, match in enumerate(sorted(base.glob(pattern))):
        if idx >= limit:
            break
        try:
            rel = match.relative_to(base)
        except ValueError:
            rel = match
        matches.append(str(rel))
    return json.dumps({"workspace": str(base), "matches": matches}, ensure_ascii=False)


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
        ),
        ToolDefinition(
            name="stat_workspace_path",
            description="Return metadata about a path relative to the workspace.",
            parameters={
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
            handler=_stat_workspace_path,
        ),
        ToolDefinition(
            name="list_workspace_entries",
            description="List files or directories under a workspace-relative folder.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "recursive": {"type": "boolean"},
                    "limit": {"type": "integer"},
                },
            },
            handler=_list_workspace_entries,
        ),
        ToolDefinition(
            name="write_workspace_text_file",
            description="Atomically write UTF-8 text under the workspace directory.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
            handler=_write_workspace_text_file,
        ),
        ToolDefinition(
            name="glob_workspace_files",
            description="Glob files relative to the workspace root.",
            parameters={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "limit": {"type": "integer"},
                },
                "required": ["pattern"],
            },
            handler=_glob_workspace_files,
        ),
    ]
