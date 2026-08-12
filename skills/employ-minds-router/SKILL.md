---
name: employ-minds-router
description: Classify engineering work by risk and route it through the minimum safe Employ-Minds workflow.
---
# Employ-Minds Router

Use this at the start of non-trivial coding, debugging, refactoring, migration, review, integration, or implementation work.

## 1. Classify

Choose exactly one current profile:

- **FAST** — tiny/local, clear requirement, low blast radius, no critical trigger.
- **STANDARD** — normal feature, bug, integration, bounded refactor, or multi-file change.
- **CRITICAL** — auth/authz, payments, secrets, destructive/data work, migrations, security boundaries, production incidents, dependency execution risk, major refactors, or failure that can materially harm users/data/money.

When material uncertainty remains, upgrade one level. Never downgrade merely to save time.

## 2. Route

### FAST
1. Inspect relevant code and constraints.
2. Add/update a focused test when behavior changes and a useful automated test is practical.
3. Make the smallest correct change.
4. Review the final diff.
5. Run fresh focused verification.

### STANDARD
1. Resolve material ambiguity; use `employ-minds-brainstorm` only when a real design choice exists.
2. Use `employ-minds-plan` for a short executable plan.
3. Use `employ-minds-tdd` for observable behavior changes.
4. Implement in bounded increments with `employ-minds-execute`.
5. Run `employ-minds-review`: spec compliance first, code quality second.
6. Run `employ-minds-security` if any trigger appears.
7. Finish with `employ-minds-verify`.

### CRITICAL
1. Inspect repository conventions and operational constraints before editing.
2. Use `employ-minds-research` for versioned/current/unfamiliar external behavior.
3. Produce an explicit plan including rollback/data-safety and stop conditions.
4. Use TDD unless genuinely impractical; record equivalent repeatable evidence if not.
5. Prefer isolated branch/worktree and independent implementation/review minds when available.
6. Require spec review, quality review, security review, and claim-mapped fresh verification.
7. Do not merge, deploy, delete, migrate, or claim success while any required gate is unresolved.

## 3. Dynamic escalation

Escalate immediately when scope expands, a hidden dependency appears, tests reveal unknown behavior, production data or secrets become involved, root cause is unclear, or an external API assumption is version-sensitive. Re-plan from the new evidence rather than forcing the old plan.

## 4. Completion

Before the final completion claim, enumerate the important claims and ensure `employ-minds-verify` has fresh evidence for each one. An agent summary is not evidence.
