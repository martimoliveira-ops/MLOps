# 0008. Version data with DVC

- **Date:** 2026-11-09
- **Status:** Accepted
- **Supersedes:** [ADR-0005](0005-raw-data-in-s3-not-git.md)

## Context

[ADR-0005](0005-raw-data-in-s3-not-git.md) kept raw data out of git by storing it at a plain S3 path, with its SHA256 recorded in the README. That covers one raw file. The plan of record needs more than that:
- **Several datasets:** load data now, OMIE prices in Phase 2, and replayed actuals in Phase 6.
- **Derived data and models:** cleaned hourly parquet, feature tables, trained models.
- **A reproducible pipeline:** `dvc repro` (Phase 3) should rebuild the model and rerun only the stages whose inputs changed.
- **A link from every MLflow run to the exact data version** it trained on (Phase 2.13).
- **CodeBuild jobs that fetch exactly the right data** (Phases 3 and 6).

With plain S3 paths and checksums, all of that would be manual bookkeeping. There's also a practical problem: the object uploaded under ADR-0005 is the unzipped `.txt` stored under a `.zip` name, so the recorded checksum doesn't describe it.

## Options

1. **Plain S3 paths plus checksums** (the current approach). No new tool, but data versions, the links between pipeline stages and caching would all be tracked by hand. Nothing ties a git commit to a data version.
2. **Git LFS.** Data versions live alongside commits, but GitHub's free LFS storage and bandwidth quotas are small next to a 678 MB file that CI downloads repeatedly. It also doesn't help with pipelines.
3. **DVC with an S3 remote.** Small `.dvc` and `dvc.lock` files in git pin exact data versions. The data itself lives in our own S3 bucket. `dvc.yaml` describes the pipeline stages, with caching.

## Decision

We will version data, intermediate outputs and model artifacts with **DVC**, using the existing bucket as its remote:
- The remote is `s3://martim-forecaster-data/dvc` (`dvc remote add -d storage …`). `.dvc/config` is committed.
- `data/raw/LD2011_2014.txt` is tracked with `dvc add`. Its `.dvc` file is committed, and the data goes up with `dvc push`. The unzipped text file is tracked, because that's the file the pipeline reads. The SHA256 of the original UCI zip stays in the README to record where the data came from.
- Bucket versioning is turned on, with a lifecycle rule that expires noncurrent object versions after 30 days.
- Once `dvc pull` has been shown to restore the file (step 1.6), the wrongly named object `raw/uci-electricity/LD2011_2014.txt.zip` is deleted.
- In Phase 3, `dvc.yaml` defines the `prepare`, `features` and `train` stages, and `dvc.lock` is committed with every model change.

## Consequences

- Each git commit pins the exact data and parameters behind it. The `.dvc` hash is what MLflow records as the data version.
- `dvc repro` only reruns the stages whose inputs changed. `dvc metrics diff` compares runs.
- There's a new tool to learn, with its own commands: remember `dvc push` after `git push`, or the data won't be in the remote.
- Every environment that needs data must have credentials for the remote. That includes the laptop, CodeBuild and the retraining jobs. The CodeBuild roles need `s3:GetObject`, and for jobs that push, `s3:PutObject`, on `dvc/*`.
- `dvc[s3]` goes in `requirements-train.txt`, not in the serving image.
- The data is now stored twice for a while (the old object plus the DVC cache) until the old object is deleted. That costs pennies.
