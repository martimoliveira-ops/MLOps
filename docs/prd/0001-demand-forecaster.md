# PRD: Portuguese electricity demand forecaster

- **Author:** Martim Oliveira
- **Status:** Approved
- **Last updated:** 2026-11-06
- **Stakeholders:** Martim (owner and builder); readers of the public repo (reviewers, interviewers)

## Overview

A service that forecasts electricity consumption for the next 24 hours, one value per hour. It's trained on real Portuguese smart-meter data, retrained automatically, and deployed on AWS through a fully automated pipeline:

```
GitHub → CodeBuild (lint, test, train) → model in S3 → image in ECR
       → deploy to AWS → monitoring → scheduled retraining
```

## Problem

Most portfolio ML projects stop at a notebook trained on a toy dataset. They don't show what ML engineering roles actually need: handling messy real-world data, evaluating without data leakage, tested pipeline code, CI/CD, monitoring, and automated retraining. Time series bring these problems out naturally: seasonality, missing data, leakage and backtesting. These are also topics that come up often in interviews.

Demand forecasting is also a building block for a collective self-consumption settlement platform, an idea the owner wants to pursue. So the work has a use beyond this project.

## Goals

1. Forecast the next 24 hourly values of the chosen target, beating both naive baselines on a held-out period.
2. Make training reproducible with one command, from versioned data to a versioned model in S3.
3. Serve predictions from a container, deployed automatically when changes merge to `main`.
4. Retrain weekly, and promote a new model only if it does better than the current one on recent data.
5. Document decisions (ADRs) and findings well enough that the repo explains itself.

## Non-goals

- Real-time or sub-hourly forecasting.
- Forecasting every one of the 370 clients separately in production. Individual clients are explored, not served.
- Being state of the art. A well-evaluated gradient-boosting model is the target, not deep learning.
- Paid managed ML platforms in the core path. SageMaker is a Phase 7 stretch goal.
- Multiple regions or high availability.

## Requirements: the roadmap

Each phase has a definition of done. It's met only when that's true.

| Phase | Scope | Done when |
|---|---|---|
| **0. Scaffolding** | `src/` layout, Makefile, pytest, pylint, black, `buildspec.yml`, CodeBuild limited to `main` | CI is green on an empty project |
| **1. Data and exploration** | Raw data in S3. Notebook covering daily, weekly and seasonal patterns, differences between clients, missing data and outliers, and 15-minute vs hourly data. Choose the target. | The main patterns can be explained in five sentences, each backed by a chart |
| **2. Baselines and modelling** | "Same as yesterday" and "same as last week" baselines. LightGBM or XGBoost with lag and calendar features (including Portuguese holidays). Time-based backtesting. MAE and MAPE. MLflow running locally. | The model beats both baselines on a held-out period, and you can explain why |
| **3. Notebook to pipeline** | Modules for loading data, features, training and evaluation. Tests for the features, including a test proving no data leakage. Data validation. `make train` writes a versioned model to S3. | One command trains, evaluates and saves a model reproducibly |
| **4. Serving** | FastAPI with `/health` and `/predict` (24 hourly values). Input validation and tests. A slim, non-root container listening on `0.0.0.0`. CI pushes the image to ECR. | The container serves predictions locally |
| **5. Continuous delivery** | Single-instance Elastic Beanstalk with the Docker platform. Automatic deploys when changes merge to `main`. A smoke test after each deploy. The Locust load test against the deployed URL. A README with a screenshot. | A merged change reaches production with no manual steps |
| **6. Monitoring and retraining** | Predictions and latency logged to CloudWatch. Weekly retraining triggered by EventBridge and run as a CodeBuild build. Champion vs challenger promotion. A drift check. | The system retrains and promotes models without you |
| **7. Stretch (optional)** | SageMaker rebuild and comparison. Solar production from the PVGIS API. ONNX export. | |

## Success metrics

- **Model:** better MAE and MAPE than both baselines on a held-out period, measured with backtesting across several periods, not a single split.
- **Pipeline:** from merging to `main` to a deployed service needs zero manual steps (Phase 5).
- **Operations:** retraining and promotion run weekly without anyone stepping in (Phase 6).
- **Cost:** the $1 budget alert is never exceeded in an ordinary month ([ADR-0006](../adr/0006-single-region-and-cost-guardrails.md)).
- **Clarity:** each phase's decisions are recorded as ADRs, and the README explains the project without needing the notebooks.

## Constraints and assumptions

- 5–8 hours a week. Phases are sized for that.
- AWS free tier and a budget close to zero. Everything runs in `eu-north-1`.
- Data: UCI ElectricityLoadDiagrams20112014, CC BY 4.0. It covers 370 clients at 15-minute resolution from 2011 to 2014. It's static and ends in 2014.
- Python 3.12 ([ADR-0004](../adr/0004-python-3-12-baseline.md)). FastAPI for serving ([ADR-0003](../adr/0003-fastapi-for-serving.md)).

## Open questions

1. **Forecast target:**
   - the total load of clients active from the start
   - the total from 2012 onwards
   - the average per active client

   The naive total grows as clients join, which would mislead a model. Decide at the end of Phase 1, and record it as an ADR.
2. **How to handle daylight saving time:** interpolate the zero hour in March and halve the doubled hour in October, or something else? Decide in Phase 1, and implement and test it in Phase 3.
3. **A data source for retraining:** the UCI data stops in 2014. Switch to Portugal's national load from the ENTSO-E Transparency Platform for Phase 6? If so, a total-load target makes the switch easier.
4. **Elastic Beanstalk availability:** is it available in `eu-north-1` on the current plan? Check before Phase 5. The fallback is Lambda running the ECR image.
5. **Outliers:** remove, cap or keep spikes? Decide in Phase 1, stage 7, and turn the decision into data validation rules in Phase 3.
