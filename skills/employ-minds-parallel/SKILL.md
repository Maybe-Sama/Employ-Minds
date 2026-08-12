---
name: employ-minds-parallel
description: Collision-aware concurrency: parallelize only independent information or isolated write scopes with explicit integration ownership.
---
# Employ-Minds Parallel

Parallelism is useful only when coordination cost and merge risk are lower than the time saved.

## Read-only fan-out
Parallel scouting, research, or independent review is safe when questions are orthogonal. Ordinary fan-out is capped by policy. Two minds should not answer the same question unless deliberate diversity is justified by a consequential decision.

## Parallel writers
Never let two writers mutate the same working tree concurrently. Parallel implementation requires **isolated branches/worktrees/sandboxes** and disjoint ownership boundaries. If two tasks touch the same contract, schema, state machine, migration, shared test fixture, or likely file set, serialize them.

Before concurrent delegation, confirm:
- neither task depends on the other's undiscovered result;
- write scopes are disjoint or isolated;
- each has bounded acceptance criteria;
- shared interfaces are frozen or owned by one integrator;
- the parent owns merge order, conflict resolution, integrated review, and final verification.

A child returns only: RESULT, CHANGED/REFERENCES, CHECKS, ASSUMPTIONS, BLOCKERS. The parent does not merge merely because both children report success; integrated behavior gets fresh verification after combination.
