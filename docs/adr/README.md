# Architecture Decision Records

An ADR records **one** technical decision: the context that forced it, what was chosen, and what it costs. Each one should fit on about a page. The format follows [PRD vs ADR vs RFC: decision documents](https://aridanemartin.dev/blog/prd-adr-rfc-decision-documents/).

## When to write one

| Document | Use it for | Where it lives |
|---|---|---|
| **PRD** | *What* to build and why: goals, non-goals, success metrics. | [`docs/prd/`](../prd/) |
| **RFC** | *How* to build something, when you want feedback before committing. The decision must still be open. | A GitHub issue labelled `decision`, or a draft PR |
| **ADR** | Recording a technical decision once it's made, often after an RFC resolves. | Here |
| **None** | Small changes with no real trade-offs. | |

Write an ADR when someone could reasonably ask, six months from now, "why did we do it this way?" In this project, that includes things like the forecast target, how missing data is handled, the split and backtest strategy, the model family, where things are deployed, and when a retrained model gets promoted.

## Rules

1. **File name:** `NNNN-kebab-case-title.md`, numbered in order and zero-padded (`0007-…`). Never reuse a number.
2. **Template:** copy [`0000-template.md`](0000-template.md).
3. **Statuses:**
   - `Proposed`: written and under discussion in its PR.
   - `Accepted`: merged.
   - `Deprecated`: no longer relevant, and nothing replaced it.
   - `Superseded by ADR-NNNN`: a later ADR replaced it.
4. **Accepted ADRs are never edited,** apart from changing their status line. If the decision changes, write a new ADR and set the old one to `Superseded by ADR-NNNN`.
5. **The ADR goes in the same PR as the change it decides,** so the PR review is also the review of the decision.
6. **Consequences** is the section future readers value most. Include the costs, not just the benefits.

## Index

| # | Title | Status |
|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [0002](0002-src-layout-with-editable-install.md) | Use a src layout with an editable install | Accepted |
| [0003](0003-fastapi-for-serving.md) | Use FastAPI for the prediction service | Accepted |
| [0004](0004-python-3-12-baseline.md) | Use Python 3.12 as the baseline | Accepted |
| [0005](0005-raw-data-in-s3-not-git.md) | Store raw data in S3, never in git | Accepted |
| [0006](0006-single-region-and-cost-guardrails.md) | Use a single AWS region and cost guardrails | Accepted |
| [0007](0007-build-image-from-phase-0.md) | Build and push the container image from Phase 0 | Accepted |
