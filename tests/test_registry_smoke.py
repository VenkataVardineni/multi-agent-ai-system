
def test_default_registry_has_memory_list():
    reg = build_default_registry()
    assert "memory_list" in reg.tool_names()

