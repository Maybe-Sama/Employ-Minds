---
name: employ-minds-context
description: Progressive disclosure and compact ledgers for keeping long-running work coherent without flooding the primary context.
---
# Employ-Minds Context

The primary context is a **decision surface**, not a warehouse.

## Progressive disclosure
Consume repository information at the lowest sufficient level:

- **L0 — map:** diff/stat, filenames, symbols, call sites, test names, ownership boundaries.
- **L1 — evidence:** targeted snippets, relevant tests, interfaces, errors, config fragments.
- **L2 — full material:** complete files, long logs, generated output, or dependency source only when a concrete unanswered question requires it.

Do not jump to L2 because it is convenient. A scout can inspect noisy material and return a compact evidence packet instead.

## Working ledger
For long or multi-agent work, retain only:
- accepted requirements / non-goals;
- current risk profile and reason;
- decisions already settled;
- open hypotheses / unknowns;
- active delegated work and ownership;
- changed boundaries/files;
- required gates and status;
- fresh evidence after the latest relevant change.

## Context escrow
A child mind owns its raw exploration. The parent receives conclusions plus precise references, not a transcript. Pull raw material into the parent only to resolve a disputed or consequential point.

## Loop detector
If two consecutive investigation/execution cycles produce no new evidence, do not repeat the same action with different wording. Change the hypothesis, instrument the boundary, reduce the scope, or escalate.

Compress exploration aggressively after a decision is settled. Never compress away acceptance criteria, unresolved risk, file/symbol references, or exact final verification evidence.
