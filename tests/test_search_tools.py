from multi_agent.memory import SharedMemory
from multi_agent.tools.registry import ToolContext, ToolRegistry
from multi_agent.tools.search_tools import search_tool_definitions


def test_web_search_stub(tmp_path):
    reg = ToolRegistry(search_tool_definitions())
    ctx = ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))
    out = reg.execute("web_search_stub", '{"query": "multi agent"}', ctx)
    assert "multi agent" in out

