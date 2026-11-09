# Architecture Decision Records

An ADR records **one** technical decision: the context that forced it, the options, what was chosen, and what it costs. Each one should fit on about a page. The format follows [PRD vs ADR vs RFC: decision documents](https://aridanemartin.dev/blog/prd-adr-rfc-decision-documents/) and the project's implementation plan, which adds an **Options** section.

## When to write one

| Document | Use it for | Where it lives |
|---|---|---|
| **PRD** | *What* to build and why: goals, non-goals, success metrics. | [`docs/prd/`](../prd/) |
| **RFC** | *How* to build something, when you want feedback before committing. The decision must still be open. | [`docs/rfc/`](../rfc/) (e.g. `001-monitoring-retraining.md` in Phase 6), or a GitHub issue labelled `decision` |
| **ADR** | Recording a technical decision once it's made, often after an RFC resolves. | Here |
| **None** | Small changes with no real trade-offs. | |

Write an ADR when someone could reasonably ask, six months from now, "why did we do it this way?"

## Rules

1. **File name:** `NNNN-kebab-case-title.md`, numbered in order and zero-padded (`0009-…`). Never reuse a number.
2. **Template:** copy [`0000-template.md`](0000-template.md). It has Context, Options, Decision and Consequences.
3. **Statuses:**
   - `Proposed`: written and under discussion in its PR.
   - `Accepted`: merged.
   - `Deprecated`: no longer relevant, and nothing replaced it.
   - `Superseded by ADR-NNNN`: a later ADR replaced it.
4. **Accepted ADRs are never edited,** apart from changing their status line. If the decision changes, write a new ADR with a `Supersedes:` line, and set the old one to `Superseded by ADR-NNNN`.
5. **The ADR goes in the same PR as the change it decides,** so the PR review is also the review of the decision.
6. **Consequences** is the section future readers value most. Include the costs, not just the benefits.

ADRs 0001–0007 were written before the Options section existed. They describe their alternatives in Context instead.

## Index

| # | Title | Status |
|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [0002](0002-src-layout-with-editable-install.md) | Use a src layout with an editable install | Accepted |
| [0003](0003-fastapi-for-serving.md) | Use FastAPI for the prediction service | Accepted |
| [0004](0004-python-3-12-baseline.md) | Use Python 3.12 as the baseline | Accepted |
| [0005](0005-raw-data-in-s3-not-git.md) | Store raw data in S3, never in git | Superseded by [0008](0008-version-data-with-dvc.md) |
| [0006](0006-single-region-and-cost-guardrails.md) | Use a single AWS region and cost guardrails | Accepted |
| [0007](0007-build-image-from-phase-0.md) | Build and push the container image from Phase 0 | Accepted |
| [0008](0008-version-data-with-dvc.md) | Version data with DVC | Accepted |

## Planned

The implementation plan calls for these ADRs. They get the next free numbers when they're written. The plan's own numbers are in brackets.

| Plan step | Topic | Plan's number |
|---|---|---|
| 2.21 | Model and evaluation approach: gradient boosting, rolling-origin backtesting, Diebold-Mariano, cost model assumptions | ADR 003 |
| 3.17 | Model registry design: local MLflow for experiments, an S3 manifest for production | ADR 004 |
| 5.17 | Hosting: Beanstalk vs ECS vs Lambda | ADR 005 |
| 5.17 | Release strategy for routine model updates | ADR 006 |
| 6.19 | Promotion policy | ADR 007 |

The plan's ADR 001 (FastAPI vs Flask) is [ADR-0003](0003-fastapi-for-serving.md), and its ADR 002 (DVC) is [ADR-0008](0008-version-data-with-dvc.md).
