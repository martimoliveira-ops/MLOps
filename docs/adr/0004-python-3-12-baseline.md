# 0004. Use Python 3.12 as the baseline

- **Date:** 2026-11-06
- **Status:** Accepted

## Context

The project runs in four places:
- local development (Python 3.12.10)
- GitHub Actions
- CodeBuild, where Python 3.12 is available on the current Amazon Linux and Ubuntu standard images
- the Docker image

The GitHub Actions matrix originally tested 3.11, 3.12 and 3.13. Declaring `requires-python = ">=3.12"` made the 3.11 job fail at install. That was correct behaviour, but it showed that the matrix and the declared minimum had drifted apart.

This is an application, not a library. It only ever runs on the version we choose, so testing older versions protects nothing real.

## Decision

We will use Python 3.12 as the baseline everywhere:
- `requires-python = ">=3.12"` in `pyproject.toml`
- `python: 3.12` in `buildspec.yml`
- `python:3.12-slim` as the Docker base image
- a GitHub Actions matrix of `["3.12", "3.13"]`, where 3.13 gives early warning before an upgrade

## Consequences

- One version is used consistently, so "works on my machine" can't come down to a Python version difference.
- **Upgrading means changing all four places in the same PR.** The lowest version in the matrix must always equal the declared minimum.
- When a dependency (pandas, LightGBM, MLflow) raises its minimum Python version, it may force an upgrade.
