import sys
from pathlib import Path

import pytest

from multi_agent.memory import SharedMemory
from multi_agent.tools import build_default_registry
from multi_agent.tools.registry import ToolContext

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture
def tmp_workspace(tmp_path):
    return str(tmp_path)


@pytest.fixture
def shared_memory():
    return SharedMemory()


@pytest.fixture
def default_registry():
    return build_default_registry()


@pytest.fixture
def tool_context(shared_memory, tmp_workspace):
    return ToolContext(memory=shared_memory, workspace_dir=tmp_workspace)

