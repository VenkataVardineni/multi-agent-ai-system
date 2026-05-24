from multi_agent.agents import build_planner
from multi_agent.llm.mock import MockLLM
from multi_agent.llm.protocol import ChatResult
from multi_agent.memory import SharedMemory
from multi_agent.orchestration_hooks import OrchestrationHooks
from multi_agent.orchestrator import Orchestrator
from multi_agent.tools import build_default_registry
from multi_agent.types import AgentRole, WorkflowStep


def test_orchestrator_hooks_none_callbacks():
    registry = build_default_registry()
    llm = MockLLM(responses=[ChatResult(content="ok", tool_calls=())])
    hooks = OrchestrationHooks(on_step_start=None, on_step_complete=None)
    orch = Orchestrator({AgentRole.PLANNER: lambda: build_planner(registry, llm)})
    out = orch.run_workflow(
        [WorkflowStep(role=AgentRole.PLANNER, instruction="x")],
        SharedMemory(),
        ".",
        hooks=hooks,
    )
    assert "planner_step_0" in out

