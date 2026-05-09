"""Errors surfaced by orchestration and agents."""


class MultiAgentError(Exception):
    """Base error for the framework."""


class ToolExecutionError(MultiAgentError):
    """Raised when a tool handler fails."""


class WorkflowError(MultiAgentError):
    """Raised when a workflow definition or run is invalid."""
