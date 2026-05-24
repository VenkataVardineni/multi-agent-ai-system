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

import json


def test_cli_delegate_mock_json():
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "multi_agent",
            "delegate",
            "plan release",
            "--mock-llm",
        ],
        cwd=_repo(),
        env={**os.environ, "PYTHONPATH": str(_repo() / "src")},
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert "role" in data and "output" in data


def test_cli_delegate_role_override():
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "multi_agent",
            "delegate",
            "anything",
            "--role",
            "coding",
            "--mock-llm",
        ],
        cwd=_repo(),
        env={**os.environ, "PYTHONPATH": str(_repo() / "src")},
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["role"] == "coding"


def test_cli_agent_data_mock():
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "multi_agent",
            "agent",
            "--role",
            "data",
            "--task",
            "summarize",
            "--mock-llm",
        ],
        cwd=_repo(),
        env={**os.environ, "PYTHONPATH": str(_repo() / "src")},
        capture_output=True,
        text=True,
        check=True,
    )
    assert proc.stdout.strip()

