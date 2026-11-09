# PRD: Portuguese electricity demand forecaster

- **Author:** Martim Oliveira
- **Status:** Approved
- **Last updated:** 2026-11-09
- **Stakeholders:** Martim (owner and builder); readers of the public repo (reviewers, interviewers)

> This PRD follows the *Portuguese Electricity Demand Forecaster: Implementation Plan* (2 Nov 2026), which is the detailed, step-by-step plan of record. Step numbers in this document (e.g. **1.4**) refer to that plan. There are two deliberate differences from it:
> - Python 3.12–3.13 ([ADR-0004](../adr/0004-python-3-12-baseline.md)) instead of 3.11–3.13.
> - The existing names are kept: package `forecaster`, bucket `martim-forecaster-data`, ECR repository `mlopstest` and tag `project=forecaster`, instead of `energy_forecast` / `energy-forecast`. Plan step 0.12, which creates a new ECR repository, is skipped.

## Overview

A service that forecasts the next 24 hours of Portuguese electricity demand, one value per hour. It's trained on real smart-meter data and runs on AWS as a monitored service that retrains itself.

```
GitHub → CodeBuild (lint, test, train smoke test) → image in ECR → CodePipeline → Elastic Beanstalk
                    │                                                            │
            DVC data + MLflow runs → champion model in S3 ◀── weekly retrain ── daily replay + monitoring
```

### The simulated clock

The dataset ends on 31 December 2014, so "production" needs a simulated present:
- Data up to a **cut-off date** (for example 30 June 2014) is history, used for training and backtesting.
- A **replay job** moves a simulated "today" forward by one day per run, and publishes that day's real readings to S3 as if the meters had just reported them.
- The API forecasts the day after the simulated today. Monitoring compares yesterday's forecast with the readings that just arrived.

This gives real drift, real actuals and real retraining decisions, all on historical data.

## Problem

Most portfolio ML projects stop at a notebook trained on a toy dataset. They don't show what ML engineering roles need:
- handling messy real-world data
- evaluating without leakage
- showing that a model is *significantly* better, and what that's worth in money
- tested pipeline code, CI/CD and safe release strategies
- monitoring, drift detection and automated retraining
- knowing what it all costs

Demand forecasting is also a building block for a collective self-consumption settlement platform, an idea the owner wants to pursue.

## Goals

1. Forecast the 24 hours of day D+1 at midnight of day D, beating both naive baselines on **error and euro cost**, with a Diebold-Mariano test supporting the difference.
2. Make training reproducible with one command (`dvc repro`), from versioned data to a versioned champion model in S3. Bad data stops the pipeline.
3. Serve versioned forecasts from a container. Every merge to `main` deploys automatically, protected by a smoke test, and blue-green, canary and rollback have each been performed at least once.
4. Detect degradation (data and concept drift), retrain weekly, test challengers in shadow, and promote only when they're better in euros, without manual work.
5. Know the running cost and compare it with the value the model delivers (an ROI line).
6. Document every significant decision as an ADR, so the repo explains itself.

## Non-goals

- Real-time or sub-hourly forecasting.
- Serving forecasts for each of the 370 clients. Individual clients are explored, not served (per-client models are a future improvement).
- State-of-the-art accuracy. A well-evaluated gradient-boosting model is the target.
- SageMaker or hosted MLflow in the core path. These are future improvements.
- Multiple regions, or high availability beyond what the release exercises need.

## Requirements: the roadmap

Each phase is done only when its "done when" is true.

| Phase | Scope (plan steps) | Done when |
|---|---|---|
| **0. Restructure the repo** | Branch and PR (0.1, 0.16). Remove chapter 1 code but keep `/health` (0.2). Package layout `src/forecaster/` with `api.py` (0.3). `pyproject.toml` with black and pylint settings (0.4). Makefile with `make run` (0.5). Three requirements files plus `make install-train` (0.6). `.gitignore` (0.7). Dockerfile installs the package and runs uvicorn (0.8). Local checks (0.9). GitHub Actions (0.10). CodeBuild limited to `main` (0.11). Resource tags (0.13). README (0.14). FastAPI ADR (0.15, done as ADR-0003). | The restructured repo is on `main`, CI is green, and the new image serves `/health` |
| **1. Data and exploration** | Download and read the dataset notes (1.1–1.2). S3 bucket with versioning, encryption, tags and a lifecycle rule (1.3). DVC with an S3 remote, round trip tested (1.4–1.6). Loader and cleaning rules in `data.py`, tested against small fixtures (1.7–1.9). Exploration: overall shape, daily and weekly patterns, seasons, holidays, client differences, data quality, choice of resolution, choice of target (1.10–1.18). Data card, five findings, DVC ADR (1.19–1.21). | Raw data is versioned in S3 through DVC, the cleaning rules are tested, and the main patterns can be explained in five sentences, each backed by a chart |
| **2. Baselines, model and business value** | Forecast setup and data split (2.1–2.2). Rolling-origin backtesting, and a test for it (2.3–2.4). Daily and weekly seasonal-naive baselines (2.5–2.7). Lag, rolling, calendar and holiday features; LightGBM (2.8–2.11). Local MLflow (2.12–2.13). MAE, MAPE, OMIE prices and a cost model in euros (2.14–2.17). Diebold-Mariano test with the HLN correction (2.18–2.20). Model and evaluation ADR (2.21). | The model beats both baselines on error and euro cost, the Diebold-Mariano test supports the difference, and every run can be reproduced from MLflow |
| **3. Notebook to tested pipeline** | Modules and `params.yaml` (3.1–3.2). Feature tests and **the leakage test** (3.3–3.5). Pandera schemas as a hard gate (3.6–3.8). `train.py` and `make train` (3.9–3.10). DVC pipeline: prepare, features, train (3.11–3.13). MLflow registry with a `champion` alias; publish to S3 with a manifest (3.14–3.16). Registry ADR (3.17). Training smoke test in CI (3.18). | `dvc repro` reproduces the model from versioned data, bad data stops the pipeline, the leakage test passes, and the champion is published to S3 with its manifest |
| **4. Serving and the simulated clock** | Live data layout in S3, replay `advance` and `reset`, tests (4.1–4.4). API: load the model at startup, plus `/health`, `/model`, `POST /predict`, `GET /forecast` and structured logs (4.5–4.10). API tests (4.11). Container: serving dependencies, configuration through environment variables, a local run, Locust, image size (4.12–4.16). | The container serves versioned forecasts locally, replay moves the simulated clock forward, and all API tests pass in CI |
| **5. Continuous delivery and safe releases** | Check Beanstalk availability, instance role, single-instance environment (5.1–5.3). `Dockerrun.aws.json`, one manual deploy (5.4–5.5). CodePipeline (Source → Build → Deploy), deploy artifact, roles, smoke test stage (5.6–5.11). Blue-green with green as staging for Locust, a canary release, the rollback runbook (5.12–5.15). README screenshot, hosting and release-strategy ADRs (5.16–5.17). | A merged change reaches production with no manual steps, the smoke test guards it, and a blue-green swap, a canary release and a rollback have each been performed |
| **6. Monitoring, drift and retraining** | RFC first, and a budget for build minutes (6.1–6.2). Daily job: replay, score, forecast, on a schedule (6.3–6.5). CloudWatch metrics, Evidently data drift, concept drift, SNS alarms (6.6–6.10). Challenger served in shadow (6.11–6.13). Weekly retraining, a promotion rule, reloading models without a redeploy, promotion ADR (6.14–6.19). Deliberate drift and failure injection (6.20–6.21). | The system detects degradation, retrains, tests the new model in shadow and promotes it safely without you, and both injection tests behave as expected |
| **7. FinOps, documentation and close-out** | Cost Explorer by tag, unit costs, ROI line, one saving applied (7.1–7.5). Architecture doc, model card, runbook, README rewrite, 3-minute demo (7.6–7.10). Tag `v1.0.0`, pause resources, test the restart path (7.11–7.13). | The README shows costs and ROI, every decision is documented, the demo is recorded, and cloud resources are paused with a tested restart path |

### Target repository layout

```
src/forecaster/
  __init__.py · config.py · data.py · features.py · validation.py · models.py
  backtest.py · cost.py · stats.py · train.py · registry.py · replay.py · monitoring.py · api.py
tests/ (fixtures/ for small hand-made samples)
notebooks/                      01_exploration.ipynb, 02_modeling.ipynb
docs/adr/ · docs/prd/ · docs/rfc/ · docs/data-card.md · docs/model-card.md · docs/runbook.md · docs/architecture.md
data/                           managed by DVC, gitignored
loadtest/locustfile.py
dvc.yaml · params.yaml · pyproject.toml · Makefile · Dockerfile
buildspec.yml (CI + image) · buildspec-deploy.yml (CD smoke test) · buildspec-replay.yml (daily) · buildspec-retrain.yml (weekly)
requirements.txt (serving) · requirements-dev.txt (checks, load test) · requirements-train.txt (training, notebooks)
```

## Success metrics

- **Model:** lower MAE (MWh), MAPE and euro cost than both seasonal-naive baselines, across 6–12 rolling-origin folds, with Diebold-Mariano support for the difference.
- **Reproducibility:** `dvc repro` rebuilds the champion. Each MLflow run records the DVC data version and the git commit.
- **Delivery:** zero manual steps from merging to `main` to production. Blue-green, canary and rollback have each been performed once.
- **Operations:** drift alarms fire on injected drift, a better challenger gets promoted, and a deliberately bad challenger never does.
- **Cost:** CodeBuild stays within about 80 of the 100 free minutes a month. The $1 budget alert isn't exceeded in a normal month. The monthly cost appears next to the monthly euro saving.

## Constraints and assumptions

- 5–8 hours a week.
- AWS free tier and a budget close to zero. Everything runs in `eu-north-1` ([ADR-0006](../adr/0006-single-region-and-cost-guardrails.md)). Resources are tagged `project=forecaster`.
- Local AWS access never uses root keys. Use either IAM Identity Center (`aws configure sso`), or an IAM user limited by an inline policy to the project bucket and ECR repository.
- Data: UCI ElectricityLoadDiagrams20112014 (CC BY 4.0), 370 clients at 15-minute resolution, 2011–2014. Prices: OMIE Portuguese day-ahead prices for the same years.
- **The period after the cut-off date is reserved for the simulated production period.** It's never used in Phase 2 modelling or backtesting.
- Python 3.12 ([ADR-0004](../adr/0004-python-3-12-baseline.md)). FastAPI for serving ([ADR-0003](../adr/0003-fastapi-for-serving.md)). DVC for data versioning ([ADR-0008](../adr/0008-version-data-with-dvc.md)).

## Open questions

1. **Cut-off date:** is 30 June 2014 right? It needs enough simulated production days (Phase 6 needs several weeks of shadow scoring) and enough training history before it.
2. **Target definition:** the plan suggests the total of clients with full history (1.17). Confirm it in Phase 1, and record it in the data card.
3. **DST repair:** interpolate the zero hour in March and split the doubled hour in October (1.8)? Confirm it against the data, and test it in 1.9.
4. **Cost model parameters:** the premium and discount for under- and over-forecasting (2.16) need a sourced, defensible starting value.
5. **Elastic Beanstalk availability** on the current plan (5.1). The fallback is Lambda running the ECR image.
6. **Build-minute budget** (6.2): if CI, the daily job and the weekly retrain don't fit, move the simulated clock forward several days per run, and run less often.

## Future improvements (after v1.0.0)

These come from the plan's list:
- weather features (Open-Meteo)
- probabilistic forecasts
- a global per-client model with hierarchical reconciliation
- PVGIS solar estimates
- Terraform or CDK
- GitHub Actions to AWS through OIDC
- Lambda or Fargate serving
- hosted MLflow, SageMaker, a feature store, ONNX export
- data contracts, Great Expectations data docs
- a dashboard
- API authentication and HTTPS
- automated rollback
- a pre-registered promotion test
