---
name: conventional-commit
description: Write a Conventional Commits message for the staged changes, with the why in the body. Use when the owner asks for a commit message or is about to commit.
disable-model-invocation: true
---

Write the message for what is staged, not the whole working tree. Start with `git diff --staged --stat` and `git diff --staged`.

Format:

```
<type>(<scope>): <imperative summary, lowercase, no full stop, under 72 characters>

<body: why the change is needed, in short paragraphs. Leave it out if the summary says enough.>

<attribution trailer>
```

Types and scopes follow [docs/github-workflow.md](../../../docs/github-workflow.md). Types are `feat`, `fix`, `data`, `exp`, `docs`, `chore` and `ci`. Use the package or notebook name as the scope, for example `feat(features): add hour and weekday calendar features`.

Rules:

- Commit only what the owner has staged. If something unrelated is staged, say so and stop.
- Never stage or commit `data/`, model files, `.env` or `.aws/`.
- Show the message and wait for a yes before running `git commit`.
- Add the attribution trailer for the agent doing the work, on its own line at the end.
