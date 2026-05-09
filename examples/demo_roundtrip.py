"""Programmatic demo: delegation + orchestration without the CLI."""

from __future__ import annotations

from multi_agent.agents import build_planner, build_writer_agent
from multi_agent.delegation import DelegationRouter
from multi_agent.llm.mock import MockLLM
from multi_agent.llm.protocol import ChatResult
from multi_agent.memory import SharedMemory
from multi_agent.orchestrator import Orchestrator
from multi_agent.tools import build_default_registry
from multi_agent.types import AgentRole, WorkflowStep


def main() -> None:
    registry = build_default_registry()
    llm = MockLLM(
        responses=[
            ChatResult(content="1) prototype\n2) harden\n3) ship", tool_calls=()),
            ChatResult(content="Stakeholder update draft...", tool_calls=()),
        ]
    )

    router = DelegationRouter()
    chosen = router.route("draft an announcement for the launch")

    orchestrator = Orchestrator(
        {
            AgentRole.PLANNER: lambda: build_planner(registry, llm),
            AgentRole.WRITER: lambda: build_writer_agent(registry, llm),
        }
    )

    steps = [
        WorkflowStep(role=AgentRole.PLANNER, instruction="outline rollout"),
        WorkflowStep(
            role=AgentRole.WRITER,
            instruction="convert outline into mail-friendly prose",
            read_keys=("planner_step_0",),
            write_key="mail",
        ),
    ]

    memory = SharedMemory()
    outputs = orchestrator.run_workflow(steps, memory, workspace_dir=".")

    print({"delegated_role": chosen.value, "workflow": outputs, "memory_keys": memory.keys()})


if __name__ == "__main__":
    main()
