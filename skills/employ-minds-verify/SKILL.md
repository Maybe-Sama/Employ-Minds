---
name: employ-minds-verify
description: Map every important completion claim to fresh observable evidence after the final change.
---
# Employ-Minds Verify

Never say “done”, “fixed”, “passes”, “safe”, or equivalent based on stale output, intuition, or another agent's summary.

1. List the important completion claims.
2. Map each claim to the command/check that can prove it.
3. Run those checks **after the final relevant change**.
4. Inspect exit status and actual output; do not infer success from truncated/partial logs.
5. Run focused tests plus the relevant broader suite for STANDARD/CRITICAL work.
6. Include build/typecheck/lint/static checks when they materially support a claim.
7. For migration/security/data changes, verify rollback/safety properties where feasible.
8. Report checks not run and why.

Evidence must match the claim: a successful build is not proof of runtime behavior, and an unrelated green suite is not proof of an untested acceptance criterion.
