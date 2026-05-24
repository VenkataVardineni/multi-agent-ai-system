
def test_run_python_snippet_runtime_error(tmp_path):
    reg = ToolRegistry(code_tool_definitions())
    ctx = ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))
    out = reg.execute("run_python_snippet", '{"code": "result = 1 / 0"}', ctx)
    assert out.startswith("error:")

