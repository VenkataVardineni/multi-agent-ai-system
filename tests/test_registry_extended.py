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

from multi_agent.tools.registry import ToolDefinition


def test_registry_serializes_dict_result():
    def handler(ctx, args):
        return {"ok": True}

    reg = ToolRegistry([ToolDefinition("demo", "d", {"type": "object", "properties": {}}, handler)])
    ctx = ToolContext(memory=SharedMemory())
    out = reg.execute("demo", "{}", ctx)
    assert '"ok": true' in out.replace(" ", "")


def test_registry_reraises_tool_execution_error():
    def handler(ctx, args):
        raise ToolExecutionError("boom")

    reg = ToolRegistry([ToolDefinition("bad", "d", {"type": "object", "properties": {}}, handler)])
    ctx = ToolContext(memory=SharedMemory())
    with pytest.raises(ToolExecutionError, match="boom"):
        reg.execute("bad", "{}", ctx)

