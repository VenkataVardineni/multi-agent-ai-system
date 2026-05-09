from multi_agent.agents import build_planner, build_writer_agent
from multi_agent.llm.mock import MockLLM
from multi_agent.llm.protocol import ChatResult
from multi_agent.memory import SharedMemory
from multi_agent.orchestrator import Orchestrator
from multi_agent.tools import build_default_registry
from multi_agent.types import AgentRole, WorkflowStep


def test_workflow_writes_memory_and_outputs():
    registry = build_default_registry()
    llm = MockLLM(
        responses=[
            ChatResult(content="plan-done", tool_calls=()),
            ChatResult(content="write-done", tool_calls=()),
        ]
    )

    orchestrator = Orchestrator(
        {
            AgentRole.PLANNER: lambda: build_planner(registry, llm),
            AgentRole.WRITER: lambda: build_writer_agent(registry, llm),
        }
    )

    steps = [
        WorkflowStep(role=AgentRole.PLANNER, instruction="draft milestones"),
        WorkflowStep(
            role=AgentRole.WRITER,
            instruction="summarize the milestones",
            read_keys=("planner_step_0",),
            write_key="final_draft",
        ),
    ]

    memory = SharedMemory()
    outputs = orchestrator.run_workflow(steps, memory, workspace_dir=None)

    assert outputs["final_draft"] == "write-done"
    assert memory.get("planner_step_0") == "plan-done"
    snap = orchestrator.memory_snapshot_between_steps(memory)
    assert "final_draft" in snap
