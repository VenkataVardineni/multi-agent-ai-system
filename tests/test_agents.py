from multi_agent.agents import build_planner
from multi_agent.llm.mock import MockLLM
from multi_agent.llm.protocol import ChatResult, ToolCallSpec
from multi_agent.memory import SharedMemory
from multi_agent.tools import build_default_registry
from multi_agent.tools.registry import ToolContext
from multi_agent.types import AgentRole, Task


def test_agent_invokes_tool_then_returns():
    registry = build_default_registry()
    llm = MockLLM(
        responses=[
            ChatResult(
                content=None,
                tool_calls=(
                    ToolCallSpec(
                        id="t1",
                        name="memory_set",
                        arguments='{"key":"k","value":"v"}',
                    ),
                ),
            ),
            ChatResult(content="final", tool_calls=()),
        ]
    )
    agent = build_planner(registry, llm)
    mem = SharedMemory()
    ctx = ToolContext(memory=mem, workspace_dir=None)
    task = Task(id="t", description="store then answer", role=AgentRole.PLANNER)
    result = agent.run(task, ctx)
    assert result == "final"
    assert mem.get("k") == "v"
