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

