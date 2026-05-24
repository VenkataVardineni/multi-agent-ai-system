from multi_agent.types import AgentRole, WorkflowStep


def test_resolved_write_key_explicit():
    step = WorkflowStep(role=AgentRole.PLANNER, instruction="go", write_key="custom")
    assert step.resolved_write_key(0) == "custom"


def test_resolved_write_key_default():
    step = WorkflowStep(role=AgentRole.WRITER, instruction="go")
    assert step.resolved_write_key(2) == "writer_step_2"


def test_to_wire_dict_minimal():
    step = WorkflowStep(role=AgentRole.DATA, instruction="analyze")
    wire = step.to_wire_dict()
    assert wire == {"role": "data", "instruction": "analyze", "read_keys": []}
    assert "write_key" not in wire
    assert "label" not in wire

