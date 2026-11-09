# 0005. Store raw data in S3, never in git

- **Date:** 2026-11-06
- **Status:** Superseded by [ADR-0008](0008-version-data-with-dvc.md)

## Context

The UCI ElectricityLoadDiagrams20112014 dataset is a 249 MB zip, or 678 MB unzipped. Git isn't designed for large binary files: they bloat the history permanently, and GitHub rejects files over 100 MB.

Later phases need the data outside the laptop: training in CodeBuild (Phase 3) and scheduled retraining (Phase 6). Model artifacts will need the same kind of storage. Results are only reproducible if everyone can prove they trained on the same bytes.

## Decision

We will store raw data in S3 and never commit data to git.
- The bucket `martim-forecaster-data` is in `eu-north-1`. Raw files go under `raw/<source>/` exactly as downloaded, and are never modified.
- The SHA256 of each raw file is recorded in the README. The UCI zip's hash is `F6C4D0E0…D4E1`.
- `data/` is gitignored. Locally, `data/raw/` mirrors S3, and `data/interim/` holds parquet caches built from it.
- A lifecycle rule on the bucket aborts incomplete multipart uploads after 7 days.

## Consequences

- The repo stays small, and the raw data has a single, verifiable source of truth.
- Getting the data needs AWS credentials or the public UCI download. The README tells people where it is.
- Phase 3's `make train` must download from S3 and check the hash before using the data.
- S3 storage costs very little (well under $0.01 a month for this file). Model artifacts under `models/` will need an expiry lifecycle rule once they exist.
