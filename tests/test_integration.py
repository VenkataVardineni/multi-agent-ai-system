from multi_agent.agents import (
    build_coding_agent,
    build_data_agent,
    build_planner,
    build_research_agent,
    build_reviewer_agent,
    build_writer_agent,
)
from multi_agent.llm.mock import MockLLM
from multi_agent.llm.protocol import ChatResult
from multi_agent.memory import SharedMemory
from multi_agent.tools import build_default_registry
from multi_agent.tools.registry import ToolContext
from multi_agent.types import AgentRole, Task


def _silent_llm(lines: list[str]) -> MockLLM:
    return MockLLM(responses=[ChatResult(content=text, tool_calls=()) for text in lines])


def test_each_role_executes_with_mock_llm():
    registry = build_default_registry()
    llm = _silent_llm(
        [
            "planner",
            "research",
            "coding",
            "data",
            "writer",
            "reviewer",
        ]
    )

    ctx = ToolContext(memory=SharedMemory(), workspace_dir=None)
    agents = [
        build_planner(registry, llm),
        build_research_agent(registry, llm),
        build_coding_agent(registry, llm),
        build_data_agent(registry, llm),
        build_writer_agent(registry, llm),
        build_reviewer_agent(registry, llm),
    ]
    roles = [
        AgentRole.PLANNER,
        AgentRole.RESEARCH,
        AgentRole.CODING,
        AgentRole.DATA,
        AgentRole.WRITER,
        AgentRole.REVIEWER,
    ]

    for agent, role in zip(agents, roles, strict=True):
        task = Task(id=f"{role.value}-t", description=f"hello as {role.value}", role=role)
        out = agent.run(task, ctx)
        assert out == role.value
