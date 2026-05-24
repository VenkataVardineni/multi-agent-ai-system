import json
import os
import subprocess
import sys
from pathlib import Path


def _repo():
    return Path(__file__).resolve().parents[1]


def test_cli_validate_success(tmp_path):
    wf = {"steps": [{"role": "planner", "instruction": "plan"}]}
    wf_path = tmp_path / "wf.json"
    wf_path.write_text(json.dumps(wf), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-m", "multi_agent", "validate", "--file", str(wf_path)],
        cwd=_repo(),
        env={**os.environ, "PYTHONPATH": str(_repo() / "src")},
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["valid"] is True
    assert data["steps"] == 1


def test_cli_validate_duplicate_warnings(tmp_path):
    wf = {
        "steps": [
            {"role": "planner", "instruction": "a", "write_key": "dup"},
            {"role": "writer", "instruction": "b", "write_key": "dup"},
        ]
    }
    wf_path = tmp_path / "wf.json"
    wf_path.write_text(json.dumps(wf), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-m", "multi_agent", "validate", "--file", str(wf_path)],
        cwd=_repo(),
        env={**os.environ, "PYTHONPATH": str(_repo() / "src")},
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert any("duplicate" in w for w in data["warnings"])

