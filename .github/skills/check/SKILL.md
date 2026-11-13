---
name: check
description: Run the full local check (format, lint and tests) and report the real output. Use when the owner asks to check, verify or run CI locally before a PR.
disable-model-invocation: true
---

Run the three checks from the Makefile, in this order:

1. `make format-check`
2. `make lint`
3. `make test`

Run all three even if one fails, so the report is complete.

If `make` isn't on PATH, run the direct commands from the table in AGENTS.md:

- `python -m black --check src tests`
- `python -m pylint --recursive=y --disable=R,C src tests`
- `python -m pytest -vv --cov=forecaster tests`

Run them with the venv active (`.venv\Scripts\Activate.ps1`). If it isn't active, say so and stop.

Report:

- Each check as PASS or FAIL.
- For any failure, the last 20 lines of its real output, with the file and line.
- Never say a check passes without showing the output that proves it.

Don't fix failures unless the owner asks.
