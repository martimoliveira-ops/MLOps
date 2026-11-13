---
applyTo: 'docs/**/*.md'
---

- Decisions live in ADRs in `docs/adr/`. Before proposing something that contradicts an accepted ADR, say so.
- Never edit an accepted ADR. Write a new ADR that supersedes it, and link the two.
- Start a new ADR from `docs/adr/0000-template.md`. Use the next free number.
- Use the same section headings as the existing ADRs, and keep each one short.
- Use the Conventional Commits format for the commit that adds or changes a doc: `docs(adr): add ADR-0009 ...`.
