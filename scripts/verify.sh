#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python -m pip install -e ".[dev]" >/dev/null
if python -m ruff --version >/dev/null 2>&1; then
  python -m ruff check src tests
fi
pytest -q
