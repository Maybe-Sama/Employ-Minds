---
name: employ-minds-release
description: Final ship/no-ship gate plus concise, natural handoff after STANDARD/CRITICAL changes.
---
# Employ-Minds Release

Use when the task includes a PR, merge, release, deployment, migration, or explicit handoff.

Before SHIP:
1. inspect the final diff/status for accidental files, debug output, secrets, generated noise, and unrelated cleanup;
2. ensure accepted behavior has implementation plus matching evidence;
3. ensure profile-required reviews are resolved against the latest diff;
4. run final claim-mapped verification after the last relevant change;
5. for data/migrations, confirm forward path, rollback/recovery, compatibility window, and the signal that should trigger rollback.

**Internal result:** SHIP or NO-SHIP with blockers. Keep that structure inside the workflow.

**User-facing handoff:** sound like a competent teammate, not a process engine. Usually state what materially changed, the most relevant verification performed, and any caveat/action the user needs. Do not dump every gate, agent handoff, command, or checklist unless the task, risk, or user asks for that detail.
