---
name: new-issue
description: Draft a GitHub issue from a rough idea, using the Task template and the Definition of Ready in docs/github-workflow.md. Use when the owner wants to write up a new task or bug.
argument-hint: [rough idea]
---

Turn `$ARGUMENTS` into an issue that's ready for the board.

1. Read `.github/ISSUE_TEMPLATE/task.md` and use its sections exactly.
2. Fill in each section:
   - **Context:** why it matters, with links to the PRD phase (`docs/prd/0001-demand-forecaster.md`), relevant ADRs and earlier issues.
   - **Acceptance criteria:** Given / When / Then, one per behaviour, each one checkable.
   - **Out of scope:** what this issue deliberately doesn't do.
   - **Size:** S, M or L. If it's L, propose how to split it.
   - **Test steps:** the exact `make` or pytest commands that prove it works.
3. Suggest labels: one phase (`phase:0` to `phase:7`), one type (`feat`, `fix`, `data`, `exp`, `docs`, `chore` or `ci`), and `decision` if it needs an ADR.
4. Check the Definition of Ready and list anything missing.
5. Print the issue as markdown. Don't create it on GitHub unless the owner asks.

If the idea involves a decision with real trade-offs, such as a target definition or a threshold, say so and suggest the `new-adr` skill. Ask the one question that would change the acceptance criteria most, and lead with your recommended answer.
