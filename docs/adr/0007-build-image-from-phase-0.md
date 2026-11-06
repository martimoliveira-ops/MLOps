# 0007. Build and push the container image from Phase 0

- **Date:** 2026-11-06
- **Status:** Accepted

## Context

There's no service to put in a container until Phase 4. The options during Phases 0–3 were:
- **Remove the Docker and ECR steps** from `buildspec.yml`, and restore them in Phase 4. This saves build minutes and ECR storage, and avoids a meaningless `latest` tag.
- **Keep them,** so the whole pipeline (GitHub → CodeBuild → ECR) runs from day one, and problems with it show up early, not in Phase 4.

## Decision

We will keep building and pushing the image from Phase 0.
- CodeBuild runs on `main` only.
- It tags each image with the short commit SHA and with `latest`.
- It pushes only when `CODEBUILD_BUILD_SUCCEEDING` is `1`, so an image is never pushed after failed checks.
- The ECR repository is `mlopstest`.

## Consequences

- Breakages in the pipeline (IAM, ECR login, Docker) show up straight away, while there's little else changing.
- Every merge costs a few extra build minutes and adds an image to ECR. An ECR lifecycle rule must expire old images ([ADR-0006](0006-single-region-and-cost-guardrails.md)).
- **The Dockerfile must stay buildable at all times.** At the time of writing, it still copies the deleted `chain_of_functions.py` and `app.py`, and it starts a uvicorn app that no longer exists. CodeBuild will fail at `docker build` until it's updated:
  - copy `pyproject.toml` and `src/`
  - run `pip install .`
  - use a placeholder `CMD` until Phase 4
- `latest` points at a placeholder image until Phase 4. Nothing should deploy from it before then.
