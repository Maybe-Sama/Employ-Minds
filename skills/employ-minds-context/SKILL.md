---
name: employ-minds-context
description: Progressive disclosure, compact ledgers, and selective experience reuse without flooding the primary context.
---
# Employ-Minds Context

The primary context is a **decision surface**, not a warehouse.

## Progressive disclosure
Consume repository information at the lowest sufficient level:
- **L0 — map:** diff/stat, filenames, symbols, call sites, test names, ownership boundaries.
- **L1 — evidence:** targeted snippets, relevant tests, interfaces, errors, config fragments.
- **L2 — full material:** complete files, long logs, generated output, or dependency source only when a concrete unanswered question requires it.

Do not jump to L2 because it is convenient. A Scout can inspect noisy material and return a compact evidence packet instead.

## Working ledger
Retain accepted requirements/non-goals, current risk/reason, settled decisions, open hypotheses, delegated ownership, changed boundaries, gate state, and fresh evidence after the latest relevant change.

## Context escrow
A child mind owns its raw exploration. The parent receives conclusions plus precise references, not a transcript. Pull raw material into the parent only to resolve a disputed or consequential point.

## Selective experience reuse
Prior work is a candidate hint, never automatic context. Reuse a compact prior decision/debugging summary only when the current task shares a concrete dependency, subsystem, failure signature, or invariant. Preserve provenance and revalidate assumptions against the current code/version. If relevance is weak or uncertain, retrieve nothing: irrelevant memory is negative context.

## Loop detector
If two consecutive investigation/execution cycles produce no new evidence, do not repeat the same action with different wording. Change the hypothesis, instrument the boundary, reduce scope, or escalate.

Compress settled exploration aggressively. Never compress away acceptance criteria, unresolved risk, file/symbol references, provenance, or exact final verification evidence.
