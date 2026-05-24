
def test_loader_invalid_role():
    with pytest.raises(WorkflowError, match="role is invalid"):
        parse_workflow_payload({"steps": [{"role": "invalid", "instruction": "x"}]})

