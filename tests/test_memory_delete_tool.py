from multi_agent.memory import SharedMemory
from multi_agent.tools.memory_tools import memory_tool_definitions
from multi_agent.tools.registry import ToolContext, ToolRegistry


def test_memory_delete_tool():
    mem = SharedMemory()
    mem.set("temp", 1)
    reg = ToolRegistry(memory_tool_definitions())
    ctx = ToolContext(memory=mem)
    out = reg.execute("memory_delete", '{"key": "temp"}', ctx)
    assert out == "deleted"
    assert "temp" not in mem

