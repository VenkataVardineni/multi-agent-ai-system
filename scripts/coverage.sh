#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python -m pip install -e ".[dev]" >/dev/null
python -m pytest --cov=multi_agent --cov-report=term-missing -q
