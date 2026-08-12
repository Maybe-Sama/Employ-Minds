---
name: employ-minds-execute
description: Implement bounded slices with evidence-driven cadence, minimal scope, and explicit re-routing when assumptions break.
---
# Employ-Minds Execute

Work one coherent slice at a time. Reference the relevant acceptance-criterion ID; do not copy its prose back into context.

For a slice:
1. inspect the exact path/boundary needed for the next edit;
2. make the smallest architecture-consistent change;
3. run the narrowest check that can falsify that slice;
4. retain only new evidence, changed files, and new assumptions in the ledger.

Run expensive broad suites at meaningful integration points and final verification rather than after every trivial edit. Do not postpone a cheap focused regression test that gives immediate signal.

Do not silently widen scope. A new subsystem/public contract, production data/security trigger, hidden dependency, or invalidated assumption returns control to the router for reclassification/re-planning.

If two consecutive execution cycles add no new evidence, stop changing code and revisit the hypothesis or design. Leave unrelated cleanup/refactoring outside the task unless it is required for correctness or explicitly accepted.
