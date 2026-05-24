import importlib

import multi_agent.constants as constants


def test_effective_tool_loop_max_defaults(monkeypatch):
    monkeypatch.delenv("MULTI_AGENT_MAX_TOOL_LOOPS", raising=False)
    importlib.reload(constants)
    assert constants.effective_tool_loop_max() == 12


def test_effective_tool_loop_max_clamps(monkeypatch):
    monkeypatch.setenv("MULTI_AGENT_MAX_TOOL_LOOPS", "9999")
    importlib.reload(constants)
    assert constants.effective_tool_loop_max() == 256


def test_effective_tool_loop_max_invalid_env(monkeypatch):
    monkeypatch.setenv("MULTI_AGENT_MAX_TOOL_LOOPS", "not-a-number")
    importlib.reload(constants)
    assert constants.effective_tool_loop_max() == 12

