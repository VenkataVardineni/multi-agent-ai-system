import json
import os
import subprocess
import sys
from pathlib import Path


def test_cli_workflow_mock(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    wf = {
        "workspace": str(tmp_path),
        "steps": [
            {"role": "planner", "instruction": "think"},
            {"role": "writer", "instruction": "write", "read_keys": ["planner_step_0"]},
        ],
    }
    wf_path = tmp_path / "wf.json"
    wf_path.write_text(json.dumps(wf), encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "multi_agent",
            "workflow",
            "--mock-llm",
            "--file",
            str(wf_path),
        ],
        cwd=repo,
        env={**os.environ, "PYTHONPATH": str(repo / "src")},
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert "outputs" in data and "memory" in data
