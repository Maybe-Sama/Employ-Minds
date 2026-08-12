---
name: employ-minds-review
description: Independent diff-first review: specification compliance before engineering quality, with evidence rather than stylistic noise.
---
# Employ-Minds Review

Review the **change**, not the entire repository. Start with the accepted requirement and final diff; expand context only to answer a concrete review question.

## Pass 1 — specification
For every acceptance criterion: IMPLEMENTED? OBSERVABLE? EVIDENCE? Check missing behavior, accidental behavior, scope drift, and tests that appear relevant but do not exercise the requested path. Spec blockers stop the pipeline.

## Pass 2 — quality
Trace changed execution paths for correctness, invariants, error handling, state/resource lifecycle, concurrency, compatibility, performance/operational risk, maintainability, and meaningful test gaps.

Prioritize findings that can change runtime behavior or future engineering cost. Avoid style-only findings already enforced by tooling. A finding must include evidence and a concrete failure mode; uncertainty is labeled as such rather than upgraded to a defect.

STANDARD and CRITICAL use independent native reviewers. Reviewers do not fix their own findings: return to the writer, then re-review the resulting diff. Security-sensitive findings route to `employ-minds-security`.
