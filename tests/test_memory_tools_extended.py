from multi_agent.memory import SharedMemory
from multi_agent.tools.memory_tools import memory_tool_definitions
from multi_agent.tools.registry import ToolContext, ToolRegistry


def test_memory_get_default():
    reg = ToolRegistry(memory_tool_definitions())
    ctx = ToolContext(memory=SharedMemory())
    out = reg.execute("memory_get", '{"key": "missing", "default": "fallback"}', ctx)
    assert out == "fallback"

