# GitHub workflow

How work moves from an idea to `main`: issues, branches, pull requests and board statuses. It applies to humans and AI agents alike.

## The flow at a glance

```
Issue (Backlog) ──▶ Ready ──▶ In progress ──▶ In review ──▶ Done
                     │            │               │            │
             meets Definition  branch +      PR marked     PR squash-merged,
               of Ready        draft PR      ready for     issue closed
                                opened        review       automatically
```

1. **Every change starts as an issue.** Small fixes can skip this. Anything that takes more than an hour, or involves a decision, shouldn't.
2. **Start work:** move the issue to **In progress**, create the branch, and open a **draft PR** straight away.
3. **Finish work:** CI is green and the PR checklist is done. Mark the PR **Ready for review**, and move the issue to **In review**.
4. **Merge:** squash-merge into `main`. The issue closes and moves to **Done** automatically. On `main`, CodeBuild builds and pushes the image.

## 1. Issues

Create issues from the **Task** template (`.github/ISSUE_TEMPLATE/task.md`). An issue is **Ready** when it meets the Definition of Ready:

| Section | What it needs |
|---|---|
| Context | Why this matters, with links to the PRD phase, ADRs and earlier issues. |
| Acceptance criteria | Written as test scenarios (*Given … When … Then …*), so each one can be checked. |
| Out of scope | What this issue deliberately does not do. |
| Size | S (< ½ day), M (½–2 days), L (> 2 days: split it). |
| Test steps | The commands or checks that prove it works. |

Labels:
- **`phase:0` … `phase:7`:** which roadmap phase the issue belongs to. The phases are defined in the PRD.
- **One type label:** `feat`, `fix`, `data`, `exp`, `docs`, `chore` or `ci`.
- **`decision`:** the issue needs an ADR.

## 2. Project board and statuses

Use a GitHub Project (table or board view) with a **Status** field:

| Status | Meaning | Who moves it |
|---|---|---|
| **Backlog** | Captured, not yet refined. | Auto-added. |
| **Ready** | Meets the Definition of Ready. | You, after refining. |
| **In progress** | Someone is working on it. There's a branch and a draft PR. | **You, when you start.** |
| **In review** | The PR is ready for review and CI is green. | You, when you click "Ready for review". |
| **Done** | The PR is merged and the issue closed. | Automatic. |

### Setting an issue to **In progress**

Do all of this when you start, not when you finish:

1. **Assign yourself** to the issue.
2. **Set Status → In progress** on the project board. Use the issue sidebar under "Projects", or drag the card.
3. **Create the branch from the issue:** in the issue sidebar, under **Development**, click **Create a branch**. This links the branch to the issue. From the CLI, use `gh issue develop <number> --name <branch> --checkout`.
4. **Push one commit and open a draft PR** with `Closes #<issue>` in the description:
   ```powershell
   gh pr create --draft --fill
   ```
   The draft PR is the visible signal that work is in progress. CI starts running on every push.

### Automating the board

In the project, go to **⋯ → Workflows** and enable:
- **Auto-add to project:** adds this repo's issues and PRs, filtered by `is:issue,pr is:open`.
- **Item added to project:** sets the status to Backlog.
- **Item closed:** sets the status to Done.
- **Pull request merged:** sets the status to Done.

Moving to **In progress** and **In review** stays manual, using the steps above. It takes one click and records when work actually started.

## 3. Branches

- **Short-lived branches off `main`:** one issue per branch, merged within a few days.
- **Naming:** `<type>/<issue-number>-<short-slug>`, for example:
  - `data/12-mask-pre-connection-zeros`
  - `feat/18-lag-features`
  - `docs/21-adr-target-definition`
- **Types** match the labels:
  - `feat`: new functionality
  - `fix`: a bug fix
  - `data`: cleaning or validation
  - `exp`: an experiment or notebook
  - `docs`: documentation
  - `chore`: maintenance
  - `ci`: pipelines
- To pick up changes from `main`, **merge `main` into your branch**; don't rebase a branch that's already pushed.

## 4. Commits

Use [Conventional Commits](https://www.conventionalcommits.org/): `<type>(optional scope): <summary>`.

```
data(cleaning): mask zeros before each client's first reading
feat(features): add hour, weekday and holiday calendar features
fix(resample): use right-closed intervals for end-of-interval timestamps
docs(adr): add ADR-0008 forecast target definition
```

- Write the summary in the imperative ("add", not "added"), in lowercase, with no full stop, under 72 characters.
- Use the body to explain *why*, when it isn't obvious.
- Commits made with an AI agent's help carry the agent's `Co-Authored-By:` trailer.

## 5. Pull requests

### Title

The PR title follows the same Conventional Commits format. **It becomes the commit message on `main`** when the PR is squash-merged, so write it for the history.

### Description

GitHub fills in [`.github/pull_request_template.md`](../.github/pull_request_template.md) automatically. Fill in every section, or write "n/a" with a reason. The sections:

- **Summary:** what changes and why, in two or three sentences.
- **Linked issue:** `Closes #N`, which closes the issue and moves it to Done when the PR merges.
- **Changes:** bullet points of what changed.
- **How to test:** the exact commands.
- **Data and ML checks:** leakage, time-based splits, baselines, data not committed.
- **Evidence:** charts, metrics tables, CI links.
- **Decisions:** links to any ADR this PR adds or follows.
- **AI assistance:** none, assisted or generated, plus what the human reviewed.

### Size

- Aim for **under 400 changed lines**, not counting notebook output.
- A notebook PR covers one analysis stage.
- If a PR is getting large, split it. It's always easier to review two small PRs than one big one.

### Draft vs ready

| State | When |
|---|---|
| **Draft** | From the first push until the work is finished. CI runs, and you can ask for early feedback. |
| **Ready for review** | CI is green, the checklist is done and the description is complete. Move the issue to **In review** at the same time. |

### Review

The reviewer (a human, or an AI agent asked to review) checks:
1. **Correctness:** the acceptance criteria are met, with tests that would fail without the change.
2. **Data and ML risk:** no future data in features, no random splits, metrics compared against the baselines.
3. **Decisions:** anything with real trade-offs has an ADR, and no accepted ADR is silently contradicted.
4. **Hygiene:** no data, secrets or credentials; dependencies are in the right requirements file; documentation is updated.

When the author is also the only maintainer, a self-review is acceptable. Read the full diff in the GitHub UI before merging.

### Merging

- **Squash merge only.** One PR becomes one commit on `main`, titled with the PR title.
- The branch is deleted automatically after merging.
- Never merge with failing checks.

## 6. AI-assisted work

- **The human who opens the PR is accountable for it,** whoever or whatever wrote the code.
- Disclose AI involvement in the PR's **AI assistance** section:
  - **None.**
  - **Assisted:** an AI suggested, reviewed or explained, and the human wrote the code.
  - **Generated:** the AI wrote the code, and the human reviewed it. Say which parts.
- PR descriptions that an agent writes end with its attribution line, e.g. `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
- Agents follow [AGENTS.md](../AGENTS.md). In particular, they never push to `main` and never commit secrets or data.

## 7. Repository settings (one-time setup)

**Settings → General → Pull Requests**
- ☑ Allow squash merging (default message: *Pull request title and description*)
- ☐ Allow merge commits
- ☐ Allow rebase merging
- ☑ Always suggest updating pull request branches
- ☑ Automatically delete head branches

**Settings → Rules → Rulesets → New branch ruleset**, targeting `main`:
- ☑ Restrict deletions
- ☑ Block force pushes
- ☑ Require a pull request before merging. Required approvals: **0** while this is a single-maintainer repo, because GitHub doesn't let you approve your own PR. Raise it when collaborators join.
- ☑ Require status checks to pass: add the GitHub Actions jobs `build (3.12)` and `build (3.13)`.
- ☑ Require linear history

**What CodeBuild does and doesn't check:** the CodeBuild webhook only runs on `main`, so it runs **after** a merge, and it isn't a PR check. GitHub Actions is the PR gate. CodeBuild is the build-and-publish step.

**Labels:** create `phase:0` … `phase:7`, `feat`, `fix`, `data`, `exp`, `docs`, `chore`, `ci` and `decision`.
