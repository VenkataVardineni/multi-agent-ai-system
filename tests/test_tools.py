import json

from multi_agent.memory import SharedMemory
from multi_agent.tools import build_default_registry
from multi_agent.tools.registry import ToolContext


def test_registry_executes_memory_tools():
    registry = build_default_registry()
    mem = SharedMemory()
    ctx = ToolContext(memory=mem, workspace_dir=None)
    out = registry.execute(
        "memory_set",
        json.dumps({"key": "answer", "value": 42}),
        ctx,
    )
    assert "stored" in out
    assert mem.get("answer") == 42


def test_csv_tool_reports_columns(tmp_path):
    csv_path = tmp_path / "rows.csv"
    csv_path.write_text("a,b\n1,x\n2,\n", encoding="utf-8")

    registry = build_default_registry()
    mem = SharedMemory()
    ctx = ToolContext(memory=mem, workspace_dir=str(tmp_path))
    payload = registry.execute(
        "analyze_csv",
        json.dumps({"path": "rows.csv", "sample_rows": 5}),
        ctx,
    )
    data = json.loads(payload)
    assert data["row_count"] == 2
    assert set(data["columns"]) == {"a", "b"}
