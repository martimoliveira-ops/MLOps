# 0003. Use FastAPI for the prediction service

- **Date:** 2026-11-06
- **Status:** Accepted

## Context

Phase 4 serves 24 hourly forecasts from `/predict`, plus a `/health` endpoint. The book and the original project plan use Flask, with gunicorn as the production server. In the chapter 1 exercise, the service was built with FastAPI and uvicorn instead. That covered input validation, `TestClient` tests and a container that binds to `0.0.0.0` and runs as a non-root user.

Options:
- **Flask + gunicorn:** matches the book one-to-one, but input validation has to be written by hand.
- **FastAPI + uvicorn:** validates inputs from type hints and generates OpenAPI docs. It's closer to the owner's ASP.NET Core minimal-APIs background.

## Decision

We will build the prediction service with FastAPI, served by uvicorn.
- The container binds to `0.0.0.0:8000` and runs as a non-root user.
- `fastapi` and `uvicorn` go in `requirements.txt`, the runtime dependencies.
- `httpx`, which `TestClient` needs, goes in `requirements-dev.txt`.

## Consequences

- Bad input (missing or invalid parameters) gets a `422` with a clear error, without hand-written checks. Tests should check those cases explicitly.
- `/docs` gives an interactive API page for free, which is useful for the README screenshot in Phase 5.
- Flask examples from the book need translating. The concepts carry over directly.
- uvicorn runs a single process by default. That's enough for a single-instance deployment, but revisit if Phase 5's load tests show a CPU bottleneck. Running several workers is the first thing to try.
