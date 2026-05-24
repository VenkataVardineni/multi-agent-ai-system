import json

from multi_agent.memory import SharedMemory
from multi_agent.tools.code_tools import code_tool_definitions
from multi_agent.tools.registry import ToolContext, ToolRegistry


def test_run_python_snippet_result(tmp_path):
    reg = ToolRegistry(code_tool_definitions())
    ctx = ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))
    out = reg.execute("run_python_snippet", '{"code": "result = 2 + 2"}', ctx)
    assert out == "4"


def test_run_python_snippet_memory_keys(tmp_path):
    mem = SharedMemory()
    mem.set("x", 10)
    reg = ToolRegistry(code_tool_definitions())
    ctx = ToolContext(memory=mem, workspace_dir=str(tmp_path))
    out = reg.execute(
        "run_python_snippet",
        '{"code": "result = x + 1", "memory_keys": ["x"]}',
        ctx,
    )
    assert out == "11"


def test_run_python_snippet_banned(tmp_path):
    reg = ToolRegistry(code_tool_definitions())
    ctx = ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))
    args = json.dumps({"code": 'open("/etc/passwd")'})
    out = reg.execute("run_python_snippet", args, ctx)
    assert "error:unsafe" in out

