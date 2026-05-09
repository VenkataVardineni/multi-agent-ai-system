from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AgentRole(str, Enum):
    RESEARCH = "research"
    CODING = "coding"
    PLANNER = "planner"
    DATA = "data"
    WRITER = "writer"
    REVIEWER = "reviewer"


@dataclass(frozen=True)
class Message:
    role: str  # system | user | assistant | tool
    content: str
    name: str | None = None
    tool_call_id: str | None = None


@dataclass
class Task:
    """Unit of work handed to a specialized agent."""

    id: str
    description: str
    role: AgentRole | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowStep:
    """Single orchestrated stage executed by a concrete agent role."""

    role: AgentRole
    instruction: str
    read_keys: tuple[str, ...] = ()
    write_key: str | None = None
    label: str | None = None

    def resolved_write_key(self, index: int) -> str:
        if self.write_key:
            return self.write_key
        return f"{self.role.value}_step_{index}"

    def to_wire_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "role": self.role.value,
            "instruction": self.instruction,
            "read_keys": list(self.read_keys),
        }
        if self.write_key is not None:
            payload["write_key"] = self.write_key
        if self.label is not None:
            payload["label"] = self.label
        return payload


@dataclass
class ParsedWorkflow:
    """Validated workflow document loaded from JSON."""

    workspace: str | None
    steps: list[WorkflowStep]
    warnings: tuple[str, ...] = ()
