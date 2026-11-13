# AI tools in this repo

This repo is set up for three AI tools in VS Code: GitHub Copilot, OpenAI Codex and Claude Code. They share one set of rules, so the three never disagree about how the project works.

## The single source of truth

[AGENTS.md](../AGENTS.md) holds the project rules. Codex reads it directly. Claude reads it through [CLAUDE.md](../CLAUDE.md), which imports it with `@AGENTS.md`. Copilot reads [.github/copilot-instructions.md](../.github/copilot-instructions.md), which points back to it.

Change the rules in AGENTS.md. Don't copy them elsewhere.

## Which file each tool reads

| Need | Copilot | Codex | Claude Code |
|---|---|---|---|
| Project rules | `.github/copilot-instructions.md`, plus `AGENTS.md` | `AGENTS.md` | `CLAUDE.md` → `AGENTS.md` |
| Rules for certain files | `.github/instructions/*.instructions.md` (`applyTo`) | `AGENTS.md` (nearest folder wins) | `.claude/skills/data-and-ml-rules` (`paths`) |
| Specialist agents | `.github/agents/*.agent.md` | Built-in subagents, enabled in `.codex/config.toml` | `.claude/agents/*.md` |
| Reusable workflows | `.github/skills/*/SKILL.md` | `.github/skills/` (also reads `.agents/skills/`) | `.claude/skills/*/SKILL.md` |
| Permissions | VS Code approvals | `.codex/config.toml` (`approval_policy`, `sandbox_mode`) | `.claude/settings.json` (`allow`, `ask`, `deny`) |
| Personal settings | `~/.codex/config.toml` (Codex), VS Code profile (Copilot) | `~/.codex/config.toml` | `~/.claude/` and `.claude/settings.local.json` (git-ignored) |

Copilot and Codex read the `.github/skills/` copies. Claude reads the `.claude/skills/` copies. The two sets have the same content. The only difference is that Claude's `data-and-ml-rules` also has a `paths` field, which Copilot ignores.

## Keeping the skills in sync

Edit a skill in both places, and keep the body text the same:

- `.claude/skills/<name>/SKILL.md`
- `.github/skills/<name>/SKILL.md`

The same goes for agents, if you change the rules in one place: `.claude/agents/<name>.md` and `.github/agents/<name>.agent.md`.

## What's where

```
AGENTS.md                              project rules (all three tools)
CLAUDE.md                              imports AGENTS.md, Claude-only notes
.github/copilot-instructions.md        Copilot's repo-wide pointer to AGENTS.md
.github/instructions/                  Copilot rules for certain files
.github/agents/                        Copilot agents: reviewer, leakage auditor, test designer, tutor
.github/skills/                        skills for Copilot and Codex
.claude/agents/                        Claude agents: the same four
.claude/skills/                        skills for Claude
.claude/settings.json                  Claude permissions (team-shared)
.codex/config.toml                     Codex approvals, sandbox and subagents (team-shared)
.vscode/settings.json                  workspace settings for VS Code and Python
.vscode/extensions.json                recommended extensions
```

## Skills

| Skill | Use it for | Invoked by |
|---|---|---|
| `check` | Format, lint and test, with real output | You, or `/check` |
| `open-pr` | Draft PR following the GitHub workflow | You only |
| `new-issue` | Draft an issue from the Task template | You, or Claude when relevant |
| `new-adr` | Next ADR as a Proposed draft | You only |
| `notebook-review` | Review a `.ipynb` on disk, outputs included | You, or Claude when relevant |
| `conventional-commit` | Commit message for staged changes | You only |
| `data-and-ml-rules` | Data and forecasting rules while coding | Claude loads it automatically for `src/forecaster` and notebooks |

Skills marked "You only" set `disable-model-invocation`, so the agent can't start them on its own. They can change the repo or GitHub.

## Agents

| Agent | Does | Edits files? |
|---|---|---|
| `code-reviewer` | Reviews a diff for correctness, leakage, ADR conflicts and hygiene | No |
| `leakage-auditor` | Runs the eight leakage and baseline checks on feature and backtest code | No |
| `test-designer` | Turns acceptance criteria into test scenarios | No |
| `tutor` | Explains code and decisions step by step, and checks understanding | No |

None of the agents write code, so the owner stays the one writing it. That's the learning-project rule in AGENTS.md.

## Permissions

Claude's `.claude/settings.json` is the strictest of the three:

- **Allowed without asking:** `make` targets, `python -m black`, `pylint` and `pytest`, read-only git and `dvc status`.
- **Asks first:** commits, pushes, PR creation or merging, installs, `dvc push` and `dvc repro`, Docker, AWS CLI, and edits to `buildspec.yml`, `Dockerfile`, `pyproject.toml`, requirements files, `.github/workflows/` and accepted ADRs.
- **Denied:** reading `.env` or `.aws/`, force-pushing, and `rm -rf`.

Codex runs with `on-request` approvals, workspace-only writes, and no network access. Copilot asks before it runs commands, as usual.

## Personal settings

Keep personal overrides out of git:

- `.claude/settings.local.json` is git-ignored. Use it for your own permission changes.
- `~/.codex/config.toml` holds your model and account settings. The project file doesn't set them.
- Don't put API keys or account details in any file in this repo.

## Adding a new skill or agent

1. Create it in `.claude/` and in `.github/`, with the same body text.
2. Use a name in lowercase with hyphens. For a skill, the folder name must match the `name` field.
3. Write a description that says when to use it. The tools use that text to decide whether to load it.
4. For anything that changes the repo or GitHub, set `disable-model-invocation: true`.
