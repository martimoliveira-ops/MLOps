# PRD: Portuguese Electricity Demand Forecaster

- **Author:** Martim Oliveira   **Status:** Draft
- **Last updated:** 2026-10-26   **Stakeholders:** Martim Oliveira (product, engineering, sole reviewer)

## Overview

An end-to-end MLOps project that forecasts electricity demand 24 hours ahead from Portuguese smart-meter data (UCI ElectricityLoadDiagrams20112014). It covers data ingestion, baselines and gradient-boosted models with backtesting, experiment tracking, a reproducible training pipeline, a containerised prediction API, continuous deployment on AWS, and monitoring with scheduled retraining. It is primarily a portfolio project for senior ML/MLOps roles, and a stepping stone toward a collective self-consumption idea where demand forecasts are an input.

## Problem

Short-term demand forecasts are the input to energy decisions such as load shifting and sizing shared generation for self-consumption. Many ML projects stop at a notebook with a good-looking metric. What is hard, and what is rarely demonstrated, is the path from that notebook to a versioned, tested, deployed and monitored service that can be retrained safely.

Evidence (current state of this repo, not market research):

- The repo already has a working CI/CD skeleton from earlier exercises: `Makefile` targets (format, lint, test), a GitHub Actions workflow (Python 3.12 and 3.13), a CodeBuild `buildspec.yml` that builds and pushes a Docker image to ECR, and a `src/forecaster` package with a smoke test.
- The forecasting work itself is not built yet. Only the raw dataset (stored in S3, SHA256 recorded in the README) and an exploration notebook exist.
- This is a learning project: the author writes the code, so the PRD also acts as the plan against which progress is reviewed.

## Goals

- Produce a 24h-ahead hourly demand forecast that beats naive baselines on a time-based backtest.
- Make training reproducible: one command (`make train`) reads raw data from S3, builds features, trains, evaluates, and writes a versioned model artifact and metrics back to S3.
- Serve forecasts through an HTTP API in a container built and pushed by the existing CI/CD pipeline.
- Deploy automatically from `main` to AWS after tests pass.
- Detect degraded forecast quality and retrain on a schedule, with the whole stack inside a small cost cap.

## Non-goals

- Real-time or sub-hourly forecasting, and horizons other than 24h ahead.
- Per-household personalisation or forecasts for individual meters beyond what the chosen target (see Open questions) requires.
- A frontend or dashboard. Monitoring uses CloudWatch.
- Multi-region, high availability, autoscaling, or auth beyond what a demo needs.
- Live ingestion of real meter data. The dataset is a historical 2011–2014 snapshot.
- Phase 7 stretch items (SageMaker, PVGIS solar data, ONNX export) are out of scope for the first release.

## Requirements / User stories

Persona: the author (ML engineer building and demonstrating the system), plus an interviewer or reviewer reading the repo and calling the API.

**Must**

- As the author, I want the raw dataset pulled from S3 with its checksum verified so that experiments start from known-identical data. *(Phase 1)*
- As the author, I want exploratory analysis of seasonality, missing values, zero-filled periods and daylight-saving effects so that feature and split decisions are grounded in the data. *(Phase 1)*
- As the author, I want naive baselines (previous day, previous week) and LightGBM/XGBoost models evaluated with rolling-origin backtesting so that I can show a real improvement without leakage. *(Phase 2)*
- As the author, I want experiments logged to a local MLflow instance so that runs, parameters and metrics are comparable. *(Phase 2)*
- As the author, I want ingestion, feature, train and evaluate steps as importable modules in `src/forecaster` with unit tests so that the pipeline is testable and `make train` is thin. *(Phase 3)*
- As a client, I want `GET /health` and `POST /predict` (FastAPI) so that I can check liveness and get the next-24h forecast. *(Phase 4)*
- As the author, I want the Dockerfile to build and run the new service so that the existing CodeBuild/ECR pipeline ships a working image. *(Phase 4)*

**Should**

- As the author, I want merges to `main` to deploy the image to Elastic Beanstalk after CI passes so that releases need no manual steps. *(Phase 5)*
- As the author, I want CloudWatch metrics and alarms for latency, errors and forecast error so that I notice degradation. *(Phase 6)*
- As the author, I want an EventBridge schedule to retrain, evaluate against the current model and promote only if it is not worse, so that the model does not go stale silently. *(Phase 6)*
- As the author, I want a $1 budget alert and lifecycle rules on ECR and S3 so that the project cannot run up cost. *(Phase 0–6)*

**Could**

- As the author, I want drift checks on input features so that retraining can be triggered by data change, not only by schedule.
- *Stretch (Phase 7):* SageMaker training, PVGIS solar features, ONNX inference.

## Success metrics

Targets are proposals to be confirmed after the Phase 1 EDA and baseline results.

- **Accuracy:** best model reduces MAE (and sMAPE) by at least 15% against the seasonal-naive (same hour, previous week) baseline on the held-out backtest folds. Report per-horizon error, not only an average.
- **Reproducibility:** `make train` from a clean checkout produces the same metrics within tolerance, and every model artifact is stored with its data checksum, git SHA and parameters.
- **Serving:** `/predict` p95 latency under 500 ms on the deployed instance, `/health` returns 200 after every deploy.
- **Delivery:** commit to `main` to live service in under 15 minutes with no manual steps. CI stays green on Python 3.12 and 3.13.
- **Quality bar:** test coverage of `src/forecaster` of at least 80%, `make format-check` and `make lint` clean.
- **Cost:** monthly AWS spend stays under the $1 budget alert threshold, or the alert fires and is explained.

## Constraints & assumptions

- **Dataset:** UCI ElectricityLoadDiagrams20112014 (CC BY 4.0, Trindade 2015). It contains 15-minute readings for several hundred clients over 2011–2014. Many series start late or are zero-filled. Timestamps follow local time, so DST days need explicit handling. These properties are to be verified in the EDA, not assumed.
- **Stack:** Python 3.12+, FastAPI, pandas, LightGBM/XGBoost, MLflow (local), Docker. AWS region `eu-north-1`.
- **Existing pipeline:** deployment reuses the current Makefile, CodeBuild and ECR setup. Work goes directly on `main`.
- **Known gaps in the repo today:** the `Dockerfile` still copies `chain_of_functions.py` and `app.py` from the deleted chapter-1 exercise and must be rewritten. `requirements.txt` has no model libraries (LightGBM/XGBoost, MLflow, boto3, scikit-learn) and is currently missing a trailing newline.
- **Way of working:** the author writes the code; reviews happen after each phase. No fixed deadline. Phases are worked in order 0–7.
- **Known unknowns:** how much the 2011–2014 pattern generalises to current Portuguese demand, and whether a free-tier-sized Elastic Beanstalk instance can load the model within the latency target.

## Open questions

- **Forecast target:** total load summed across clients, a subset of clients, or per-client forecasts? This drives features, the API contract and metrics. Proposal: start with the aggregate.
- **Resolution:** aggregate to hourly from 15-minute data, or forecast 96 steps? Proposal: hourly.
- **`/predict` contract:** does the caller send recent history, or does the service read it from S3? Proposal: service reads the latest window from S3 so the endpoint takes only a forecast origin timestamp.
- **Model loading:** baked into the image at build time, or pulled from S3 at start-up? This affects whether retraining requires a new image.
- **Promotion rule:** what exact comparison decides that a retrained model replaces the current one?
- **Elastic Beanstalk vs ECS/App Runner** for Phase 5, given the image is already built into ECR. The earlier plan says Elastic Beanstalk, so this stays unless it blocks.
- **Ground truth for monitoring:** the dataset is historical, so how is "live" forecast error simulated (replay of held-out period)?
