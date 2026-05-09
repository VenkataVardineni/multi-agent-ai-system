from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from multi_agent.types import WorkflowStep


@dataclass
class OrchestrationHooks:
    """Optional lifecycle callbacks for orchestrator runs."""

    on_step_start: Callable[[int, WorkflowStep], None] | None = None
    on_step_complete: Callable[[int, WorkflowStep, str], None] | None = None
