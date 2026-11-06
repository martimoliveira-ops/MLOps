# 0002. Use a src layout with an editable install

- **Date:** 2026-11-06
- **Status:** Accepted

## Context

The chapter 1 exercises kept loose `.py` files at the repo root, and tests imported them straight from the working directory. That works for a few files. It breaks down once there's a real package with data loading, features, training and serving modules. Tests can pass locally because of the current directory and then fail in Docker or CI, where the code is installed differently.

The options were:
- a flat layout (`forecaster/` at the root)
- a `src/` layout with `PYTHONPATH` hacks
- a `src/` layout installed as a package

## Decision

We will put the package in `src/forecaster/` and describe it in `pyproject.toml`, with setuptools as the build backend.
- Development and CI install it in editable mode: `python -m pip install -e .`, run by `make install`.
- The Docker image installs it normally, with `pip install .`.
- The version is defined once, in `pyproject.toml`. `forecaster.__version__` reads it from the installed package's metadata.

## Consequences

- Tests import `forecaster` exactly the way production does, so a missing install fails loudly. `tests/test_smoke.py` checks for this.
- Python files in `src/` and `tests/` are picked up by black, pylint and pytest without editing the Makefile.
- An extra step is needed: forgetting `pip install -e .` gives `ModuleNotFoundError: forecaster`.
- pylint needs `--recursive=y`, because `src/` and `tests/` are plain folders, not packages.
- The Dockerfile has to copy `pyproject.toml` and `src/` and install the package. It currently still copies the deleted chapter 1 files: see [ADR-0007](0007-build-image-from-phase-0.md).
