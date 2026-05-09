from __future__ import annotations

import csv
from collections import Counter
from typing import Any

from multi_agent.tools.file_tools import _safe_join
from multi_agent.tools.registry import ToolContext, ToolDefinition


def _analyze_csv(ctx: ToolContext, args: dict[str, Any]) -> dict[str, Any]:
    rel = str(args["path"])
    sample_rows = int(args.get("sample_rows", 5))
    path = _safe_join(ctx.workspace_dir, rel)
    if not path.is_file():
        return {"error": f"not a file: {path}"}

    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows: list[dict[str, str]] = []
        null_counts: Counter[str] = Counter()
        nonempty: Counter[str] = Counter()
        total = 0
        for row in reader:
            total += 1
            for key in fieldnames:
                val = row.get(key, "")
                if val == "" or val is None:
                    null_counts[key] += 1
                else:
                    nonempty[key] += 1
            if len(rows) < sample_rows:
                rows.append({k: row.get(k, "") for k in fieldnames})

    column_summaries = []
    for col in fieldnames:
        column_summaries.append(
            {
                "column": col,
                "non_empty": int(nonempty[col]),
                "empty_or_missing": int(null_counts[col]),
            }
        )

    return {
        "path": str(path),
        "row_count": total,
        "columns": fieldnames,
        "column_summaries": column_summaries,
        "sample": rows,
    }


def csv_tool_definitions() -> list[ToolDefinition]:
    return [
        ToolDefinition(
            name="analyze_csv",
            description=(
                "Summarize a CSV file: columns, row count, null-ish counts, "
                "and a few sample rows."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "sample_rows": {"type": "integer"},
                },
                "required": ["path"],
            },
            handler=_analyze_csv,
        )
    ]
