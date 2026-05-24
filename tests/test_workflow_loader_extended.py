
def test_loader_invalid_role():
    with pytest.raises(WorkflowError, match="role is invalid"):
        parse_workflow_payload({"steps": [{"role": "invalid", "instruction": "x"}]})


def test_loader_non_object_step():
    with pytest.raises(WorkflowError, match="must be an object"):
        parse_workflow_payload({"steps": ["bad"]})

