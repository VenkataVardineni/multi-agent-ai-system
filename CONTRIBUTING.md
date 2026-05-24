# Contributing

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Verify locally

```bash
bash scripts/verify.sh
```

Or run `pytest` and `ruff check src tests` directly.

## Pull requests

- Keep commits focused and descriptive.
- Add tests for behavior changes.
- Update docs when CLI flags or workflow format change.
