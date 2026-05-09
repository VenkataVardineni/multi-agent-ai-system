from __future__ import annotations

from multi_agent.tools.code_tools import code_tool_definitions
from multi_agent.tools.csv_tools import csv_tool_definitions
from multi_agent.tools.file_tools import file_tool_definitions
from multi_agent.tools.memory_tools import memory_tool_definitions
from multi_agent.tools.registry import ToolRegistry
from multi_agent.tools.search_tools import search_tool_definitions


def build_default_registry() -> ToolRegistry:
    defs = []
    defs.extend(memory_tool_definitions())
    defs.extend(file_tool_definitions())
    defs.extend(csv_tool_definitions())
    defs.extend(code_tool_definitions())
    defs.extend(search_tool_definitions())
    return ToolRegistry(defs)
