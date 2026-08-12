---
name: employ-minds-router
description: Risk-adaptive orchestration using native specialist agents, independent review, and minimal sufficient ceremony.
---
# Employ-Minds Router

Route non-trivial engineering work. Use `employ-minds-budget` continuously.

## 1. Classify
- **FAST**: tiny/local, clear, low blast radius, no critical trigger.
- **STANDARD**: normal feature/bug/integration/bounded refactor/multi-file change.
- **CRITICAL**: auth/authz, payments, secrets, migrations, destructive/data/security work, production incidents, supply-chain execution, major refactors, or material user/data/money risk.

Material uncertainty upgrades one level. Reclassify when evidence changes.

## 2. Dispatch native minds
Use the harness-native equivalents of these roles: `em-scout`, `em-architect`, `em-researcher`, `em-debugger`, `em-implementer`, `em-spec-reviewer`, `em-quality-reviewer`, `em-security-reviewer`, `em-verifier`.

Spawn only when the role adds information or independence. Cap ordinary fan-out at 3 concurrent independent minds.

### FAST
Primary agent: inspect -> smallest change -> diff review -> fresh focused check. Use `em-scout` only if finding the path would pollute context. No ceremonial multi-agent chain.

### STANDARD
1. `em-scout` when code ownership/path is not obvious.
2. `em-architect` only for a material design choice or cross-cutting change; otherwise make a micro-plan.
3. For bugs, `em-debugger` establishes root cause before implementation.
4. `em-researcher` only for versioned/current/unfamiliar external behavior.
5. Implement with the primary agent or `em-implementer`; use TDD for observable behavior.
6. Independent `em-spec-reviewer` must pass.
7. Independent `em-quality-reviewer` then reviews engineering quality.
8. Security review only when triggered.
9. Independent `em-verifier` maps final claims to fresh evidence and returns SHIP/NO-SHIP.

### CRITICAL
Require explicit acceptance criteria, rollback/data-safety plan, independent implementation/review contexts, spec review, quality review, security review, and final verifier. Prefer isolated branch/worktree. No merge/deploy/destructive action while a gate is unresolved.

## 3. Information contract
Every delegated task gets: OBJECTIVE, KNOWN FACTS, CONSTRAINTS, OUTPUT CONTRACT. Do not forward the whole conversation when a smaller packet is sufficient.

## 4. Stop conditions
Stop on unresolved acceptance criteria, unexplained failing tests, critical security findings, unknown destructive/migration safety, or a completion claim without matching fresh evidence.

**Invariant:** no completion claim outruns its evidence.
