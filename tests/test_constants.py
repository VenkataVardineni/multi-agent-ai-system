
def test_effective_tool_loop_max_invalid_env(monkeypatch):
    import importlib

    import multi_agent.constants as constants

    monkeypatch.setenv("MULTI_AGENT_MAX_TOOL_LOOPS", "not-a-number")
    importlib.reload(constants)
    assert constants.effective_tool_loop_max() == 12

