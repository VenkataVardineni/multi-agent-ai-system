import json
import os
import subprocess
import sys
from pathlib import Path


def test_sample_workflow_json_mock():
    repo = Path(__file__).resolve().parents[1]
    wf = repo / "examples" / "sample_workflow.json"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "multi_agent",
            "workflow",
            "--mock-llm",
            "--file",
            str(wf),
        ],
        cwd=repo,
        env={**os.environ, "PYTHONPATH": str(repo / "src")},
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert len(data["outputs"]) >= 1

