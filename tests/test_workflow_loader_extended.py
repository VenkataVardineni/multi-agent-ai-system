import pytest

from multi_agent.exceptions import WorkflowError
from multi_agent.workflow_loader import parse_workflow_payload


def test_loader_rejects_missing_instruction():
    with pytest.raises(WorkflowError, match="instruction"):
        parse_workflow_payload({"steps": [{"role": "planner"}]})


def test_loader_rejects_non_list_steps():
    with pytest.raises(WorkflowError, match="must be a list"):
        parse_workflow_payload({"steps": "bad"})

