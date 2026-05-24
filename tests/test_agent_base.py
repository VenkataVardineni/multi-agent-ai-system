from multi_agent.agent_base import BaseAgent
from multi_agent.llm.mock import MockLLM
from multi_agent.llm.protocol import ChatResult
from multi_agent.memory import SharedMemory
from multi_agent.tools import build_default_registry
from multi_agent.tools.registry import ToolContext
from multi_agent.types import AgentRole, Task


def test_agent_returns_trimmed_content():
    registry = build_default_registry()
    llm = MockLLM(responses=[ChatResult(content="  hello  ", tool_calls=())])
    agent = BaseAgent(AgentRole.PLANNER, registry, llm)
    ctx = ToolContext(memory=SharedMemory())
    out = agent.run(Task(id="1", description="hi"), ctx)
    assert out == "hello"

import json

from multi_agent.llm.protocol import ToolCallSpec


def test_agent_tool_loop_limit(monkeypatch):
    monkeypatch.setenv("MULTI_AGENT_MAX_TOOL_LOOPS", "2")
    import importlib
    import multi_agent.constants as constants
    importlib.reload(constants)
    import multi_agent.agent_base as agent_base
    importlib.reload(agent_base)

    registry = build_default_registry()
    tc = ToolCallSpec(id="1", name="memory_set", arguments=json.dumps({"key": "k", "value": 1}))
    llm = MockLLM(
        responses=[
            ChatResult(content=None, tool_calls=(tc,)),
            ChatResult(content=None, tool_calls=(tc,)),
            ChatResult(content=None, tool_calls=(tc,)),
        ]
    )
    agent = agent_base.BaseAgent(AgentRole.PLANNER, registry, llm)
    ctx = ToolContext(memory=SharedMemory())
    out = agent.run(Task(id="1", description="loop"), ctx)
    assert out == "error: tool loop limit exceeded"

