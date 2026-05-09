from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from multi_agent.exceptions import WorkflowError
from multi_agent.types import AgentRole, ParsedWorkflow, WorkflowStep


def load_workflow_file(path: Path) -> ParsedWorkflow:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"invalid JSON workflow ({path}): {exc}") from exc
    if not isinstance(payload, dict):
        raise WorkflowError("workflow root must be an object")
    return parse_workflow_payload(payload)


def parse_workflow_payload(payload: dict[str, Any]) -> ParsedWorkflow:
    workspace = payload.get("workspace")
    raw_steps = payload.get("steps")
    warnings: list[str] = []
    if raw_steps is None:
        raise WorkflowError("workflow.steps is required")
    if not isinstance(raw_steps, list):
        raise WorkflowError("workflow.steps must be a list")

    steps: list[WorkflowStep] = []
    planned_keys: list[str | None] = []
    for idx, item in enumerate(raw_steps):
        if not isinstance(item, dict):
            raise WorkflowError(f"steps[{idx}] must be an object")
        try:
            role = AgentRole(str(item["role"]))
        except KeyError as exc:
            raise WorkflowError(f"steps[{idx}].role is required") from exc
        except ValueError as exc:
            raise WorkflowError(f"steps[{idx}].role is invalid") from exc
        if "instruction" not in item:
            raise WorkflowError(f"steps[{idx}].instruction is required")
        instruction = str(item["instruction"])
        read_keys = tuple(str(k) for k in item.get("read_keys", []) or [])
        write_key = item.get("write_key")
        label = item.get("label")
        step = WorkflowStep(
            role=role,
            instruction=instruction,
            read_keys=read_keys,
            write_key=str(write_key) if write_key else None,
            label=str(label) if label else None,
        )
        steps.append(step)
        planned_keys.append(step.resolved_write_key(idx))

    duplicates = _duplicate_warnings(planned_keys)
    warnings.extend(duplicates)

    ws: str | None
    if workspace is None:
        ws = None
    else:
        ws = str(workspace)

    return ParsedWorkflow(workspace=ws, steps=steps, warnings=tuple(warnings))


def _duplicate_warnings(keys: list[str | None]) -> list[str]:
    seen: dict[str, int] = {}
    warnings: list[str] = []
    for key in keys:
        if key is None:
            continue
        seen[key] = seen.get(key, 0) + 1
    for key, count in seen.items():
        if count > 1:
            warnings.append(f"duplicate write_key detected: {key!r} ({count} steps)")
    return warnings
