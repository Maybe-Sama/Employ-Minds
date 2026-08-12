---
name: employ-minds-review
description: Two-pass engineering review: specification compliance first, code quality second.
---
# Employ-Minds Review

Do not combine the passes.

## Pass 1 — specification compliance
- Does every acceptance criterion have an implementation path?
- Is required behavior missing?
- Did scope drift introduce behavior the request did not authorize?
- Do tests/evidence actually exercise the requested behavior and material edge cases?

Resolve spec blockers before quality review.

## Pass 2 — code quality
- Correctness, invariants, error handling, concurrency and resource lifecycle.
- Simplicity and consistency with repository architecture.
- API/naming ergonomics and unnecessary complexity.
- Test clarity, determinism and brittleness.
- Material performance or operational concerns.

For CRITICAL work, prefer reviewers that did not implement the change. If independent agents are unavailable, perform a cold review from the diff and accepted spec rather than relying on implementation memory.

Security-sensitive findings route through `employ-minds-security`. Any unresolved blocker prevents completion.
