---
name: employ-minds-execute
description: Implement bounded plan slices in small verified increments while controlling scope drift.
---
# Employ-Minds Execute

Implement the accepted plan one coherent slice at a time.

For each slice:
1. restate the local acceptance criterion;
2. inspect the exact code path before editing;
3. apply the smallest architecture-consistent change;
4. run the narrow evidence check immediately;
5. record files changed and any new assumption.

Do not silently broaden scope. If a required change crosses a new subsystem, changes a public contract, touches production data/security, or invalidates the plan, return to the router and reclassify/re-plan.

Leave refactoring that is not necessary for correctness out of the task unless the plan explicitly includes it.
