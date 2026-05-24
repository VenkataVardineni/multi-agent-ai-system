from multi_agent.tools.memory_tools import memory_tool_definitions
from multi_agent.tools.registry import ToolRegistry


def test_unregister_removes_tool():
    reg = ToolRegistry(memory_tool_definitions())
    assert "memory_get" in reg.tool_names()
    reg.unregister("memory_get")
    assert "memory_get" not in reg.tool_names()

