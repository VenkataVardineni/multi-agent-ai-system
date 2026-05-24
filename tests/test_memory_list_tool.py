import json

from multi_agent.memory import SharedMemory
from multi_agent.tools.memory_tools import memory_tool_definitions
from multi_agent.tools.registry import ToolContext, ToolRegistry


def test_memory_list_tool_returns_keys():
    mem = SharedMemory()
    mem.set("a", 1)
    mem.set("b", 2)
    reg = ToolRegistry(memory_tool_definitions())
    ctx = ToolContext(memory=mem)
    out = reg.execute("memory_list", "{}", ctx)
    payload = json.loads(out)
    assert sorted(payload["keys"]) == ["a", "b"]

