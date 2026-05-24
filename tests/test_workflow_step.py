
def test_to_wire_dict_with_optionals():
    from multi_agent.types import AgentRole, WorkflowStep

    step = WorkflowStep(
        role=AgentRole.REVIEWER,
        instruction="review",
        read_keys=("a",),
        write_key="out",
        label="Review",
    )
    wire = step.to_wire_dict()
    assert wire["write_key"] == "out"
    assert wire["label"] == "Review"
    assert wire["read_keys"] == ["a"]

