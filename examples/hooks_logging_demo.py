"""Demonstrate OrchestrationHooks step lifecycle callbacks."""

from multi_agent.agents import build_planner, build_writer
from multi_agent.llm.mock import MockLLM
from multi_agent.llm.protocol import ChatResult
from multi_agent.memory import SharedMemory
from multi_agent.orchestration_hooks import OrchestrationHooks
from multi_agent.orchestrator import Orchestrator
from multi_agent.tools import build_default_registry
from multi_agent.types import AgentRole, WorkflowStep


def main() -> None:
    registry = build_default_registry()
    llm = MockLLM(responses=[ChatResult(content="step done", tool_calls=())] * 4)
    hooks = OrchestrationHooks(
        on_step_start=lambda i, s: print(f"start {i}: {s.role.value}"),
        on_step_complete=lambda i, s, r: print(f"done {i}: {len(r)} chars"),
    )
    orch = Orchestrator(
        {
            AgentRole.PLANNER: lambda: build_planner(registry, llm),
            AgentRole.WRITER: lambda: build_writer(registry, llm),
        }
    )
    steps = [
        WorkflowStep(role=AgentRole.PLANNER, instruction="outline"),
        WorkflowStep(role=AgentRole.WRITER, instruction="draft", read_keys=["planner_step_0"]),
    ]
    orch.run_workflow(steps, SharedMemory(), ".", hooks=hooks)


if __name__ == "__main__":
    main()
