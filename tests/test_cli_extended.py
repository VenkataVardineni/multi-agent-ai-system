import os
import subprocess
import sys
from pathlib import Path


def _repo():
    return Path(__file__).resolve().parents[1]


def test_cli_version():
    proc = subprocess.run(
        [sys.executable, "-m", "multi_agent", "--version"],
        cwd=_repo(),
        env={**os.environ, "PYTHONPATH": str(_repo() / "src")},
        capture_output=True,
        text=True,
        check=True,
    )
    assert "multi-agent" in proc.stdout

