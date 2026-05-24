import pytest

from multi_agent.exceptions import WorkflowError
from multi_agent.workflow_loader import parse_workflow_payload


def test_loader_rejects_missing_instruction():
    with pytest.raises(WorkflowError, match="instruction"):
        parse_workflow_payload({"steps": [{"role": "planner"}]})


def test_loader_rejects_non_list_steps():
    with pytest.raises(WorkflowError, match="must be a list"):
        parse_workflow_payload({"steps": "bad"})

from pathlib import Path

from multi_agent.workflow_loader import load_workflow_file


def test_loader_invalid_json_file(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(WorkflowError, match="invalid JSON"):
        load_workflow_file(bad)


def test_loader_null_workspace():
    parsed = parse_workflow_payload(
        {"workspace": None, "steps": [{"role": "planner", "instruction": "x"}]}
    )
    assert parsed.workspace is None
    assert len(parsed.steps) == 1


def test_loader_invalid_role():
    with pytest.raises(WorkflowError, match="role is invalid"):
        parse_workflow_payload({"steps": [{"role": "invalid", "instruction": "x"}]})


def test_loader_non_object_step():
    with pytest.raises(WorkflowError, match="must be an object"):
        parse_workflow_payload({"steps": ["bad"]})

