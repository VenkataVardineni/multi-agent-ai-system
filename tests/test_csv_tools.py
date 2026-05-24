from multi_agent.memory import SharedMemory
from multi_agent.tools.csv_tools import csv_tool_definitions
from multi_agent.tools.registry import ToolContext, ToolRegistry


def test_analyze_csv_summaries(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("name,value\nalpha,1\n,2\n", encoding="utf-8")
    reg = ToolRegistry(csv_tool_definitions())
    ctx = ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))
    out = reg.execute("analyze_csv", '{"path": "data.csv"}', ctx)
    assert "row_count" in out
    assert "name" in out


def test_analyze_csv_missing(tmp_path):
    reg = ToolRegistry(csv_tool_definitions())
    ctx = ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))
    out = reg.execute("analyze_csv", '{"path": "missing.csv"}', ctx)
    assert "error" in out

