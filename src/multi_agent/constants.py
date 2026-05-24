"""Shared literals for the multi-agent runtime."""

import os

DEFAULT_MODEL = "gpt-4o-mini"
GLOBAL_MEMORY_NS = "global"
ENV_TOOL_LOOP_MAX = "MULTI_AGENT_MAX_TOOL_LOOPS"
ENV_WORKSPACE = "MULTI_AGENT_WORKSPACE"
ENV_MOCK_LLM = "MULTI_AGENT_MOCK_LLM"


def effective_tool_loop_max() -> int:
    raw = os.environ.get(ENV_TOOL_LOOP_MAX, "").strip()
    if not raw:
        return 12
    try:
        value = int(raw)
    except ValueError:
        return 12
    return max(1, min(value, 256))


# Back-compat constant used when env is unset at import time
TOOL_LOOP_MAX = effective_tool_loop_max()
