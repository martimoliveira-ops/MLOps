<!-- Title: Conventional Commits, e.g. "feat(features): add calendar features". It becomes the squash-merge commit message. -->

## Summary

<!-- What changes and why, in two or three sentences. -->

## Linked issue

Closes #

## Changes

-

## How to test

```powershell
make format-check
make lint
make test
```

<!-- Add any other commands or manual checks, e.g. which notebook cells to run. -->

## Data and ML checks

<!-- Tick what applies. Strike out the lines that don't, and say why. -->

- [ ] No future data reaches features (there's a leakage test for any new feature function)
- [ ] Train/test splits and backtests are time-based, never random
- [ ] Metrics are compared against both baselines ("same as yesterday", "same as last week")
- [ ] No data files, model files or credentials are committed

## Evidence

<!-- Charts, metrics tables, CI run links, screenshots. -->

## Decisions

<!-- Link any ADR this PR adds or relies on, e.g. docs/adr/0008-....md. Write "None" if there are none. -->

## AI assistance

<!-- One of: None / Assisted (AI suggested, reviewed or explained; human wrote the code) / Generated (AI wrote the code; human reviewed it). For "Generated", say which parts. -->

## Checklist

- [ ] CI is green
- [ ] Every section above is filled in, or marked n/a with a reason
- [ ] README, AGENTS.md or other docs updated if the behaviour or a command changed
- [ ] Issue moved to **In review** when this PR was marked ready
