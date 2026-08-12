# Employ-Minds core rules

1. **One governor.** Route non-trivial engineering through `employ-minds-router`; skills are gates, not competing orchestrators.
2. **Risk buys ceremony.** FAST must stay cheap; CRITICAL must stay difficult to wave through.
3. **Root cause before patching.** Unexplained failures require a falsifiable failure model, not symptom whack-a-mole.
4. **Behavior earns tests.** Prefer RED → GREEN → REFACTOR for observable behavior and regression-first bug fixing.
5. **Spec before aesthetics.** Review specification compliance before code quality.
6. **Security follows triggers.** Auth, money, secrets, migrations, destructive/data work, dependency execution and trust boundaries activate the security gate.
7. **Evidence before claims.** Never claim done/fixed/passing/safe from stale output or another agent's summary.
8. **Current facts are researched.** Versioned/unfamiliar external behavior comes from primary sources and is translated into implementation constraints.
9. **Parallel only when independent.** Delegated tasks need disjoint ownership or an explicit integration contract.
10. **Escalation is one-way unless evidence changes.** Do not downgrade merely to save time.
11. **User instructions survive installation.** Employ-Minds owns only its managed block and namespaced directories.
12. **Stop on unresolved blockers.** A task is not complete while any profile-required gate is unresolved.
