from pathlib import Path

import pytest

from multi_agent.exceptions import WorkflowError
from multi_agent.workflow_loader import load_workflow_file, parse_workflow_payload


def test_duplicate_write_keys_warn(tmp_path: Path):
    payload = {
        "workspace": ".",
        "steps": [
            {"role": "planner", "instruction": "a", "write_key": "same"},
            {"role": "writer", "instruction": "b", "write_key": "same"},
        ],
    }
    parsed = parse_workflow_payload(payload)
    assert any("duplicate write_key" in w for w in parsed.warnings)


def test_invalid_role_raises():
    payload = {
        "steps": [
            {"role": "not-a-role", "instruction": "x"},
        ],
    }
    with pytest.raises(WorkflowError):
        parse_workflow_payload(payload)


def test_load_file_roundtrip(tmp_path: Path):
    path = tmp_path / "wf.json"
    path.write_text(
        '{"steps":[{"role":"planner","instruction":"hi","label":"alpha"}]}',
        encoding="utf-8",
    )
    parsed = load_workflow_file(path)
    assert parsed.steps[0].label == "alpha"
