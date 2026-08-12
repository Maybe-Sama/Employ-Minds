---
name: employ-minds-release
description: Final ship/no-ship discipline for diffs, release notes, migrations, CI, and unresolved risk.
---
# Employ-Minds Release

Use before shipping a STANDARD or CRITICAL change when the task includes a PR, release, merge, deployment, migration, or handoff.

1. Inspect the final diff for accidental files, debug output, secrets and unrelated cleanup.
2. Confirm acceptance criteria map to implementation and tests/evidence.
3. Confirm all profile-required reviews are resolved.
4. Run the final verification set after the last relevant change.
5. For migrations/data changes, confirm forward/rollback procedure and compatibility window.
6. Produce concise release notes: behavior changed, operational action required, known limitations, rollback signal.
7. Return **SHIP** only when no required gate is unresolved; otherwise return **NO-SHIP** with blockers.
