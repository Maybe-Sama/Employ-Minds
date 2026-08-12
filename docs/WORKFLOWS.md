# Workflows

These examples show how profile selection changes **ceremony**, not quality expectations.

## FAST — typo or tiny local fix

Example: rename a mislabeled UI string with no API/data implications.

```text
inspect exact usage
→ change smallest surface
→ inspect diff
→ run focused test/build/check
→ report evidence
```

No architecture essay. No swarm of reviewers.

## STANDARD — normal feature

Example: add an API endpoint backed by existing service patterns.

```text
inspect neighboring endpoint + tests
→ short plan with files and acceptance criteria
→ RED test for requested behavior
→ GREEN minimum implementation
→ REFACTOR while green
→ spec review
→ quality review
→ focused + relevant suite
→ completion summary with evidence
```

If authz or secrets appear, activate the security gate. If the endpoint touches a payment boundary, escalate to CRITICAL.

## STANDARD debugging — bug with unclear mechanism

```text
reproduce
→ capture exact divergence
→ trace state/input backward
→ form falsifiable hypothesis
→ test one variable
→ regression test reproduces bug
→ root-cause fix
→ reviews + verification
```

Three failed speculative fixes are a signal to stop patching and rebuild the failure model.

## CRITICAL — database migration

```text
inspect schema + migration conventions + production constraints
→ research version-specific database behavior if needed
→ explicit plan: forward path, backfill, compatibility window, rollback
→ tests/equivalent rehearsal evidence
→ implementation in bounded increments
→ independent spec review
→ independent quality review
→ mandatory security/data-safety review
→ migration/rollback verification
→ ship/no-ship decision from evidence
```

“Migration file was generated successfully” is not sufficient evidence that production data is safe.

## Dynamic escalation example

A FAST config change reveals a token is serialized into logs. The task immediately becomes CRITICAL because a secret boundary is involved. The original profile does not survive new evidence.
