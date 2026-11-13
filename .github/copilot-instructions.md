# Copilot instructions

The full rules for this repo are in [AGENTS.md](../AGENTS.md). Read it before suggesting changes. The short version:

- This is a learning project. Explain and review by default. Write or edit code only when the owner asks for it.
- Follow the data rules in AGENTS.md. Every feature must be known at midnight of day D. Splits and backtests are by time only.
- Never touch data, credentials, `.aws/` or `.env` files. Never edit an accepted ADR. Write a superseding one instead.
- Use black, and keep pylint clean. Before saying something works, run `make format-check`, `make lint` and `make test`, and report the actual output.
- Commit messages and PR titles use Conventional Commits. See [docs/github-workflow.md](../docs/github-workflow.md).
