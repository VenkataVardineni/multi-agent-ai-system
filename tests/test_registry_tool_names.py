from multi_agent.tools import build_default_registry


def test_registry_lists_sorted_tool_names():
    registry = build_default_registry()
    names = registry.tool_names()
    assert names == sorted(names)
    assert "memory_get" in names
    assert "fetch_url_text" in names
