from multi_agent.agents import build_planner, build_writer_agent
from multi_agent.llm.mock import MockLLM
from multi_agent.llm.protocol import ChatResult
from multi_agent.memory import SharedMemory
from multi_agent.orchestration_hooks import OrchestrationHooks
from multi_agent.orchestrator import Orchestrator
from multi_agent.tools import build_default_registry
from multi_agent.types import AgentRole, WorkflowStep


def test_hooks_fire_per_step():
    registry = build_default_registry()
    llm = MockLLM(
        responses=[
            ChatResult(content="a", tool_calls=()),
            ChatResult(content="b", tool_calls=()),
        ]
    )
    orchestrator = Orchestrator(
        {
            AgentRole.PLANNER: lambda: build_planner(registry, llm),
            AgentRole.WRITER: lambda: build_writer_agent(registry, llm),
        }
    )

    starts: list[int] = []
    ends: list[tuple[int, str]] = []

    hooks = OrchestrationHooks(
        on_step_start=lambda idx, step: starts.append(idx),
        on_step_complete=lambda idx, step, output: ends.append((idx, output)),
    )

    steps = [
        WorkflowStep(role=AgentRole.PLANNER, instruction="plan"),
        WorkflowStep(role=AgentRole.WRITER, instruction="write"),
    ]

    memory = SharedMemory()
    orchestrator.run_workflow(steps, memory, workspace_dir=None, hooks=hooks)

    assert starts == [0, 1]
    assert [pair[0] for pair in ends] == [0, 1]
