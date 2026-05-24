from multi_agent.types import AgentRole, WorkflowStep


def test_resolved_write_key_explicit():
    step = WorkflowStep(role=AgentRole.PLANNER, instruction="go", write_key="custom")
    assert step.resolved_write_key(0) == "custom"


def test_resolved_write_key_default():
    step = WorkflowStep(role=AgentRole.WRITER, instruction="go")
    assert step.resolved_write_key(2) == "writer_step_2"

