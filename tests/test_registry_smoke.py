from multi_agent.tools import build_default_registry
from multi_agent.tools.registry import ToolContext
from multi_agent.memory import SharedMemory


def test_default_registry_tool_names_sorted():
    reg = build_default_registry()
    names = reg.tool_names()
    assert names == sorted(names)
    assert "memory_get" in names
    assert "read_text_file" in names


def test_default_registry_has_memory_list():
    reg = build_default_registry()
    assert "memory_list" in reg.tool_names()

