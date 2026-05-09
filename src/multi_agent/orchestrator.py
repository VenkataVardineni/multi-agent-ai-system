from __future__ import annotations

from collections.abc import Callable, Mapping

from multi_agent.agent_base import BaseAgent
from multi_agent.memory import SharedMemory
from multi_agent.tools.registry import ToolContext
from multi_agent.types import AgentRole, Task, WorkflowStep

AgentFactory = Callable[[], BaseAgent]


class Orchestrator:
    """Runs sequential workflow steps with shared memory snapshots."""

    def __init__(self, builders: Mapping[AgentRole, AgentFactory]) -> None:
        self._builders = dict(builders)

    def run_workflow(
        self,
        steps: list[WorkflowStep],
        memory: SharedMemory,
        workspace_dir: str | None,
    ) -> dict[str, str]:
        outputs: dict[str, str] = {}
        for index, step in enumerate(steps):
            factory = self._builders.get(step.role)
            if factory is None:
                raise KeyError(f"no agent factory registered for role={step.role}")

            agent = factory()
            ctx = ToolContext(memory=memory, workspace_dir=workspace_dir)

            memory_fragments = []
            for key in step.read_keys:
                memory_fragments.append(f"[memory:{key}]={memory.get(key)}")
            enriched_instruction = step.instruction
            if memory_fragments:
                enriched_instruction = (
                    f"{step.instruction}\n\nContext:\n" + "\n".join(memory_fragments)
                )

            task = Task(
                id=f"workflow-{index}",
                description=enriched_instruction,
                role=step.role,
            )
            result = agent.run(task, ctx)

            write_key = step.write_key or f"{step.role.value}_step_{index}"
            memory.set(write_key, result)
            outputs[write_key] = result

        return outputs

    def memory_snapshot_between_steps(self, memory: SharedMemory) -> dict[str, object]:
        """Expose a JSON-friendly snapshot for logging or downstream tooling."""

        return memory.snapshot()
