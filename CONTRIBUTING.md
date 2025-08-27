# Contributing to Tokra Shield

## Dev setup
```bash
python -m venv venv && . venv/bin/activate
pip install -U pip
pip install -e ".[api]" pytest
pytest -q
Commit & PRConventional commits preferred (feat:, fix:, docs:, chore:, ci:).

Run pytest and scripts/self_check.sh before pushing.

One focused PR per change; include tests when applicable.

Code style

Keep modules small and pure.

Avoid heavy dependencies.
