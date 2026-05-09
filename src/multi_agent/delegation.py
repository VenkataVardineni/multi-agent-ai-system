from __future__ import annotations

from dataclasses import dataclass, field

from multi_agent.types import AgentRole

DEFAULT_KEYWORDS: dict[AgentRole, tuple[str, ...]] = {
    AgentRole.RESEARCH: ("research", "find", "search", "source", "reference", "paper"),
    AgentRole.CODING: ("code", "implement", "debug", "refactor", "patch", "build"),
    AgentRole.PLANNER: ("plan", "roadmap", "milestones", "steps", "outline"),
    AgentRole.DATA: ("csv", "dataset", "analyze", "dataframe", "column", "aggregate"),
    AgentRole.WRITER: ("write", "draft", "blog", "essay", "announce", "compose"),
    AgentRole.REVIEWER: ("review", "critique", "feedback", "issues", "risks"),
}


@dataclass
class DelegationRouter:
    """Routes a natural-language wish to the best-scoring specialist."""

    keywords: dict[AgentRole, tuple[str, ...]] = field(
        default_factory=lambda: dict(DEFAULT_KEYWORDS),
    )
    default_role: AgentRole = AgentRole.PLANNER

    def route(self, message: str) -> AgentRole:
        text = message.lower()
        scores: dict[AgentRole, int] = {role: 0 for role in AgentRole}
        for role, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in text:
                    scores[role] += 1
        best_role, best_score = max(scores.items(), key=lambda item: item[1])
        if best_score == 0:
            return self.default_role
        return best_role
