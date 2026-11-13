---
name: new-adr
description: Create the next Architecture Decision Record from docs/adr/0000-template.md as a proposed draft. Use when the owner wants to record a decision, or when a change has real trade-offs.
disable-model-invocation: true
argument-hint: [short title]
---

Create a new ADR titled from `$ARGUMENTS`.

1. Find the highest number in `docs/adr/` and use the next one, zero-padded to four digits. Never reuse a number.
2. Read `docs/adr/0000-template.md` and `docs/adr/README.md`. Follow the template's headings exactly.
3. Read the existing ADRs that relate to the decision, and link them. Don't change them.
4. Write `docs/adr/NNNN-<slug>.md` with the status **Proposed**. Cover the context, the options with their trade-offs, the decision and its consequences. If the owner hasn't decided, leave the decision section open and say what they need to choose.
5. If the README has an index of ADRs, add the new one to it.
6. Never edit an accepted ADR. If the new one replaces an existing one, link the two in the new file, and ask the owner before touching the old one. Its status is theirs to change.
7. Show the file path and a short summary. Ask the owner to confirm the status before it's accepted.
