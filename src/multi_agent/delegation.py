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

    @classmethod
    def from_mapping(
        cls,
        raw: dict[str, tuple[str, ...]],
        *,
        default_role: AgentRole = AgentRole.PLANNER,
    ) -> "DelegationRouter":
        keywords = {AgentRole(k): v for k, v in raw.items()}
        return cls(keywords=keywords, default_role=default_role)

    def route(self, message: str) -> AgentRole:
        """Score keyword hits (weighted by length) and return the best role."""
        text = message.lower()
        scores: dict[AgentRole, int] = {role: 0 for role in AgentRole}
        for role, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in text:
                    scores[role] += len(keyword)

        best_score = max(scores.values())
        if best_score == 0:
            return self.default_role

        tied = [role for role, score in scores.items() if score == best_score]
        if len(tied) == 1:
            return tied[0]

        # Prefer reviewer feedback when multiple specialists tie.
        if AgentRole.REVIEWER in tied:
            return AgentRole.REVIEWER
        return min(tied, key=lambda r: r.value)
