# AGENTS.md

Instructions for AI coding agents (Claude Code, Copilot, Codex, Cursor, …) working in this repo. Humans should start with [README.md](README.md).

## Project

A service that forecasts Portuguese electricity demand for the next 24 hours, hour by hour. It's trained on the UCI ElectricityLoadDiagrams20112014 smart-meter dataset, retrained automatically, and deployed on AWS.

It's a learning and portfolio project that follows the book *Practical MLOps*. The plan of record is the step-by-step *Implementation Plan* (2 Nov 2026), summarised in [docs/prd/0001-demand-forecaster.md](docs/prd/0001-demand-forecaster.md). Step numbers such as "1.4" refer to that plan.

The dataset ends in 2014, so production runs on a **simulated clock**:
- Data before a cut-off date (about 30 June 2014) is history, used for training.
- A replay job publishes one more day of real readings at a time.
- The API forecasts the next day.

**Current phase: finishing Phase 0 (restructure) while starting Phase 1 (data).** Loading is done in `notebooks/01_exploration.ipynb`. `src/forecaster/` is still a scaffold.

## How to work in this repo

- **This is a learning project. Explain and review by default.** The owner writes most of the code. Give steps, pointers to docs and review comments. Write or edit code only when explicitly asked.
- **Pause after each group of files** and summarise what changed before moving on.
- **Decisions live in ADRs.** Before proposing something that contradicts an accepted ADR in [docs/adr/](docs/adr/), say so. A new decision with real trade-offs gets a new ADR. Never edit an accepted ADR: supersede it instead.
- **Follow the GitHub workflow** in [docs/github-workflow.md](docs/github-workflow.md): issue, branch, draft PR, review, then squash-merge.

## Stack

| Area | Choice |
|---|---|
| Language | Python 3.12 ([ADR-0004](docs/adr/0004-python-3-12-baseline.md)) |
| Packaging | `src/` layout, `pyproject.toml`, editable install ([ADR-0002](docs/adr/0002-src-layout-with-editable-install.md)) |
| Data | pandas, numpy, pyarrow (parquet) |
| Data versioning | DVC with an S3 remote at `s3://martim-forecaster-data/dvc` ([ADR-0008](docs/adr/0008-version-data-with-dvc.md)) |
| Modelling (Phase 2+) | LightGBM, MLflow running locally, Pandera validation, `holidays` (PT); Evidently for drift in Phase 6 |
| Serving (Phase 4) | FastAPI + uvicorn ([ADR-0003](docs/adr/0003-fastapi-for-serving.md)) |
| Quality | black, pylint (`--disable=R,C`), pytest + pytest-cov |
| CI | GitHub Actions (Python 3.12 + 3.13 matrix) and AWS CodeBuild (`buildspec.yml`, `main` only) |
| Artifacts | Docker image in ECR (repo `mlopstest`), raw data in S3 ([ADR-0005](docs/adr/0005-raw-data-in-s3-not-git.md)) |
| AWS region | `eu-north-1` only ([ADR-0006](docs/adr/0006-single-region-and-cost-guardrails.md)) |

## Layout

```
src/forecaster/     package code; the target modules are listed in the PRD ("Target repository layout")
tests/              pytest tests, named test_*.py; tests/fixtures/ holds small hand-made samples
notebooks/          numbered notebooks: 01_exploration, 02_modeling
data/               managed by DVC, gitignored; raw/ is never modified, interim/ holds parquet caches
docs/adr/           architecture decision records
docs/prd/           product requirements
.github/            CI workflow, PR and issue templates
buildspec.yml       CodeBuild: lint, test, build and push the image
Makefile            single entry point for install, format, lint and test
```

## Commands

Run everything from the repo root with the venv active. The Makefile is the source of truth. CI runs the same targets.

| Task | make | Direct command (Windows without make) |
|---|---|---|
| Install | `make install` | `python -m pip install -r requirements.txt`, then `-r requirements-dev.txt`, then `-e .` |
| Format | `make format` | `python -m black src tests` |
| Format check | `make format-check` | `python -m black --check src tests` |
| Lint | `make lint` | `python -m pylint --recursive=y --disable=R,C src tests` |
| Test | `make test` | `python -m pytest -vv --cov=forecaster tests` |
| Get the data | `dvc pull` | same (needs AWS credentials; available after step 1.5) |

`make run` (the API with reload) and `make install-train` (training and notebook dependencies) arrive with steps 0.5 and 0.6. Phase 3 adds `make train` and `dvc repro`.

On Windows:
- Activate the venv with `.venv\Scripts\Activate.ps1`.
- Always call tools as `python -m <tool>`, so you get the venv's copy. `pip` can't upgrade itself any other way on Windows.

A change is done only when the format check, lint and tests all pass locally.

## Dependencies

There are three files. Step 0.6 finishes the split; until then, notebook tools live in the dev file.
- `requirements.txt`: **serving** only (fastapi, uvicorn, pandas, lightgbm, boto3, pyarrow). This is all that goes into the Docker image.
- `requirements-dev.txt`: checks (pytest, pytest-cov, pylint, black, httpx, locust).
- `requirements-train.txt`: training and notebooks (jupyter, matplotlib, scikit-learn, mlflow, `dvc[s3]`, pandera, holidays, evidently).
- List each package in only one file.
- Ask before adding a dependency.

## Data rules: read before touching data code

These come from Phase 1 findings. Breaking them produces models that look right but are wrong.

- **Never commit data.** `data/` is gitignored. Data is versioned with DVC: commit the `.dvc` and `dvc.lock` files, then run `dvc push`. The SHA256 of the original UCI zip is in the README, as a record of where the data came from.
- **The forecast setup.** At midnight of day D, forecast all 24 hours of day D+1. Every feature must be known at midnight of day D, so a lag is always **at least 24 hours** before the hour it predicts.
- **The period after the cut-off date is reserved for the simulated production period.** By default that's after 30 June 2014; the date is set in `params.yaml`. It's never used for training, tuning or backtesting in Phases 2–3.
- **Tests never use the full dataset.** Use small hand-made files in `tests/fixtures/`.
- **The raw file format:** separator `;`, decimal comma (`decimal=","`), first column is the timestamp, one column per client (`MT_001` … `MT_370`).
- **Units:** values are the average kW over 15 minutes. Divide by 4 to get kWh. Hourly energy is the **sum** of four kWh values.
- **Timestamps mark the end of each interval.** `00:15` covers 00:00–00:15, and the last row is `2015-01-01 00:00`, which belongs to 2014. Resample with `label="right", closed="right"`.
- **Daylight saving time is in the values, not the index.** The index is a regular 15-minute grid on local wall-clock time. On the March change day, 1:00–2:00 is zero. On the October change day, that hour holds two hours of consumption.
- **A zero can mean "not a client".** Clients that joined after 2011 have zeros before their first reading, and some may have zeros after leaving. Treat those zeros as missing, not as zero consumption.
- **No data leakage.**
  - Split by time only, never randomly.
  - A feature for time *t* may only use data that would be known at forecast time.
  - Backtest with expanding or rolling windows.
  - Any new feature function needs a test proving it uses no future data.
- **Every model must beat both seasonal-naive baselines** (daily and weekly) across rolling-origin backtest folds. It must beat them on MAE, MAPE **and euro cost**, with a Diebold-Mariano test supporting the difference.

## Code conventions

- black formatting, and pylint must be clean.
- Small, pure functions that take and return DataFrames or Series are easiest to test.
- Keep I/O (S3, files) at the edges.
- Tests go in `tests/test_<module>.py`, with names that describe the behaviour, e.g. `test_lag_features_use_only_past_values`.
- Notebooks: run them top to bottom before committing, and keep the outputs, since the charts are the deliverable. Never print a whole DataFrame; use `.head()`.
- Commit messages and PR titles follow Conventional Commits. See [docs/github-workflow.md](docs/github-workflow.md).

## Boundaries

**Always**
- Run the format check, lint and tests before saying something works.
- Report failures with the actual output.
- Read a file before changing it, and keep to the style around the code you change.

**Ask first**
- Adding or upgrading dependencies.
- Changing `buildspec.yml`, `.github/workflows/`, `Dockerfile` or `pyproject.toml`.
- Anything that creates, changes or deletes AWS resources, including `aws` CLI write commands.
- Starting long-running processes (servers, training runs, load tests).

**Never**
- Commit secrets, AWS credentials, `.aws/` contents, `.env` files or data files.
- Push to `main`, force-push, or rewrite published history.
- Edit an accepted ADR. Write a superseding one instead.
- Use a random train/test split on time-series data.
- Use data from after the cut-off date for training, tuning or backtesting.
