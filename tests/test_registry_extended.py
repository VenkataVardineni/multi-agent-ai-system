import pytest

from multi_agent.exceptions import ToolExecutionError
from multi_agent.memory import SharedMemory
from multi_agent.tools.registry import ToolContext, ToolRegistry


def test_registry_unknown_tool():
    reg = ToolRegistry()
    ctx = ToolContext(memory=SharedMemory())
    with pytest.raises(KeyError, match="unknown tool"):
        reg.execute("nope", "{}", ctx)


def test_registry_invalid_json():
    from multi_agent.tools.memory_tools import memory_tool_definitions

    reg = ToolRegistry(memory_tool_definitions())
    ctx = ToolContext(memory=SharedMemory())
    with pytest.raises(ToolExecutionError, match="invalid JSON"):
        reg.execute("memory_set", "{bad", ctx)

