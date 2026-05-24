import pytest

from multi_agent.exceptions import ToolExecutionError
from multi_agent.memory import SharedMemory
from multi_agent.tools.registry import ToolContext, ToolRegistry


def test_registry_unknown_tool():
    reg = ToolRegistry()
    ctx = ToolContext(memory=SharedMemory())
    with pytest.raises(KeyError, match="unknown tool"):
        reg.execute("nope", "{}", ctx)

