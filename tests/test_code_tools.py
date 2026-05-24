from multi_agent.memory import SharedMemory
from multi_agent.tools.code_tools import code_tool_definitions
from multi_agent.tools.registry import ToolContext, ToolRegistry


def test_run_python_snippet_result(tmp_path):
    reg = ToolRegistry(code_tool_definitions())
    ctx = ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))
    out = reg.execute("run_python_snippet", '{"code": "result = 2 + 2"}', ctx)
    assert out == "4"

