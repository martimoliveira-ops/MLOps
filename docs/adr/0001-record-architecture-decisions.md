# 0001. Record architecture decisions

- **Date:** 2026-11-06
- **Status:** Accepted

## Context

This project is built in phases over several months, often with an AI agent helping. Decisions so far (the package layout, the web framework, the Python version, where data is stored) were made in conversation and existed nowhere in the repo. Without a written record:
- the reasoning is lost
- AI agents can't see why things are the way they are, so they suggest undoing decisions that were made on purpose
- interview conversations about the project depend on memory

## Decision

We will record each significant technical decision as an ADR in `docs/adr/`, using the format and rules in [`docs/adr/README.md`](README.md). ADRs 0002–0007 record decisions made before this ADR existed. They're dated when they were written down, not when they were decided.

## Consequences

- A new contributor or agent can understand the project's main choices by reading a handful of one-page documents. `AGENTS.md` points agents to them.
- Changing a decision means writing a new ADR. That's deliberate friction: a reversal has to explain itself.
- Writing an ADR takes some time. The cost is kept low by limiting each one to a single decision of about a page, and by skipping ADRs for changes without real trade-offs.
