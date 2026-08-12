---
name: employ-minds-parallel
description: Delegate work concurrently only when tasks are genuinely independent and have explicit handoff contracts.
---
# Employ-Minds Parallel

Parallelism is useful only when coordination cost and merge risk are lower than the time saved.

Before delegating two tasks concurrently, confirm:
- they do not modify the same state/files/contracts, or the integration boundary is explicit;
- neither depends on the other task's undiscovered result;
- each has bounded scope and acceptance criteria;
- each knows the current risk profile and active gates;
- the orchestrator owns final integration and verification.

Every subtask returns conclusion/files changed, checks run with exact outcomes, assumptions, and blockers. Do not parallelize sequential debugging hypotheses or tightly coupled refactors merely because multiple agents are available.
