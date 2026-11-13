---
name: open-pr
description: Open a draft pull request for the current branch, following docs/github-workflow.md. Use only when the owner asks to open or create a PR.
disable-model-invocation: true
argument-hint: [issue-number]
---

Follow [docs/github-workflow.md](../../../docs/github-workflow.md). Go through these steps in order, and stop at the first one that fails.

1. **Branch.** Run `git branch --show-current`. Stop if it's `main`. The name must be `<type>/<issue-number>-<short-slug>`, for example `feat/18-lag-features`.
2. **Issue.** Take the issue number from the branch name or from `$ARGUMENTS`. Confirm it with `gh issue view <number>`. The PR body must contain `Closes #<number>`.
3. **Checks.** Run the `check` skill. Stop if anything fails.
4. **Scope.** Run `git status`. Stop if there are uncommitted changes. Run `git diff main...HEAD --stat`. Stop if the diff includes anything under `data/`, any model file, or any `.env` or `.aws/` file.
5. **Title and body.** The title uses Conventional Commits and is under 72 characters. Build the body from `.github/pull_request_template.md`, with every section filled in or marked n/a with a reason. End it with the attribution line for the agent doing the work.
6. **Confirm.** Show the title and body to the owner and wait for a yes. Pushing and opening a PR are visible to others.
7. **Open.** Write the body to a temporary file, then run `git push -u origin HEAD` and `gh pr create --draft --title "<title>" --body-file <file>`. A file avoids quoting problems in PowerShell and Git Bash.

Never merge, never push to `main`, and never force-push. When it's done, report the PR URL.
