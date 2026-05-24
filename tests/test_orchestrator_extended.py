import pytest

from multi_agent.llm.mock import MockLLM
from multi_agent.llm.protocol import ChatResult
from multi_agent.memory import SharedMemory
from multi_agent.orchestrator import Orchestrator
from multi_agent.tools import build_default_registry
from multi_agent.types import AgentRole, WorkflowStep


def _builders(registry, llm):
    from multi_agent.agents import build_planner

    return {AgentRole.PLANNER: lambda: build_planner(registry, llm)}


def test_orchestrator_injects_memory_context():
    registry = build_default_registry()
    llm = MockLLM(responses=[ChatResult(content="done", tool_calls=())])
    orch = Orchestrator(_builders(registry, llm))
    mem = SharedMemory()
    mem.set("prior", "value")
    steps = [WorkflowStep(role=AgentRole.PLANNER, instruction="go", read_keys=("prior",))]
    outputs = orch.run_workflow(steps, mem, ".")
    assert "planner_step_0" in outputs


def test_orchestrator_missing_factory():
    orch = Orchestrator({})
    with pytest.raises(KeyError, match="no agent factory"):
        orch.run_workflow(
            [WorkflowStep(role=AgentRole.PLANNER, instruction="x")],
            SharedMemory(),
            ".",
        )

