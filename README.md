# MLOps: Portuguese electricity demand forecaster

Forecasts the next 24 hours of electricity demand, hour by hour. It's trained on real Portuguese smart-meter data, retrained automatically, and deployed on AWS through a CI/CD pipeline.

**Status:** Phase 0 (restructure) is nearly done: the package layout, CI and container image are in place. The API currently serves `/health` only. Phase 1 (data and exploration) is in progress. The full roadmap is in the [PRD](docs/prd/0001-demand-forecaster.md).

## What it does

At midnight of each day, the service forecasts every hour of the next day. The data is from 370 Portuguese clients and ends in 2014, so "production" runs on a simulated clock. Data before a cut-off date trains the model. A daily replay job then publishes one more day of real readings, as if the meters had just reported them. That gives real forecasts to score, real drift to detect and real retraining decisions to make. Each model is judged by its error, and also by what that error costs in euros on the Portuguese day-ahead market.

## Architecture

- **Data:** the raw readings are versioned with DVC in S3, and a Pandera validation gate stops the pipeline on bad data.
- **Training:** a `dvc repro` pipeline builds features, backtests LightGBM against two naive baselines, logs runs to MLflow, and publishes the winning model to S3 with a manifest.
- **CI:** GitHub Actions and AWS CodeBuild run formatting, lint and tests. On `main`, CodeBuild builds the Docker image and pushes it to ECR.
- **Serving:** a FastAPI container, deployed to Elastic Beanstalk through CodePipeline, forecasts the day after the simulated today.
- **Monitoring and retraining:** a daily CodeBuild job replays a day, scores yesterday's forecast and checks for drift. A weekly job retrains a challenger, which serves in shadow and replaces the champion only when it's cheaper in euros.

## Run it locally

You need Python 3.12 and Docker. On Windows, activate the venv with `.venv\Scripts\Activate.ps1`. The comment after each `make` command is the same command without `make`, for machines that don't have it.

```powershell
make install          # python -m pip install -r requirements.txt -r requirements-dev.txt; python -m pip install -e .
make install-train    # notebooks and training: python -m pip install -r requirements-train.txt
make test             # python -m pytest -vv --cov=forecaster tests
make run              # python -m uvicorn forecaster.api:app --reload
```

`make run` serves the API at http://127.0.0.1:8000/health, with interactive docs at `/docs`.

To run the container instead:

```powershell
docker build -t forecaster:local .
docker run --rm -p 8000:8000 forecaster:local
```

Then open http://localhost:8000/health.

## Docs

- [Product requirements and roadmap](docs/prd/0001-demand-forecaster.md)
- [Architecture decisions (ADRs)](docs/adr/README.md)
- [GitHub workflow: issues, branches and PRs](docs/github-workflow.md)
- [Instructions for AI agents](AGENTS.md)

## Data

- Source: UCI ElectricityLoadDiagrams20112014 (CC BY 4.0), Trindade, A. (2015), https://doi.org/10.24432/C58C86
- Versioning: DVC, with its remote in the project's S3 bucket ([ADR-0008](docs/adr/0008-version-data-with-dvc.md)). Run `dvc pull` to fetch the data once it's tracked (plan step 1.5).
- SHA256 of the original UCI download (`electricityloaddiagrams20112014.zip`): `F6C4D0E0DF12ECDB9EA008DD6EEF3518ADB52C559D04A9BAC2E1B81DCFC8D4E1`
