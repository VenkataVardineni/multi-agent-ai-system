from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from multi_agent.memory import SharedMemory
from multi_agent.tools.registry import ToolRegistry


@dataclass
class AgentSession:
    """Bundles shared memory and resources for one orchestrated run."""

    memory: SharedMemory
    registry: ToolRegistry
    workspace_dir: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
