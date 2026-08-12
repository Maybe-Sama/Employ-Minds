# Employ-Minds evals

Employ-Minds does not call itself better because its prompts look sophisticated. Improvements should survive repeatable evaluation.

## Two layers

### 1. Harness conformance
Deterministic tests verify installation, native-agent discovery layout, risk-policy invariants, permissions, and safe uninstall. These are CI tests; they do **not** prove coding quality.

### 2. Agent performance
Run the same task corpus against a baseline (for example a plain coding agent or a previous workflow) and Employ-Minds. Store one JSON object per run using `run-result.schema.json`, then compare with `scripts/score_runs.py`.

Primary metrics:
- `solved`: acceptance criteria truly satisfied;
- `false_completion`: agent claimed completion when evidence says otherwise — treated as a severe failure;
- `regression`: previously correct behavior broken;
- `critical_miss`: security/data/money/destructive risk missed;
- `reviewer_catches`: defects caught before final ship;
- input/output tokens;
- wall-clock seconds.

Report metrics separately. Do not hide quality/cost trade-offs behind one magic score. A candidate dominates a baseline only when it is at least as safe/correct and strictly better on one meaningful dimension without a compensating regression.

## Corpus design
Use a mix of tiny fixes, normal features, ambiguous bugs, cross-file refactors, current API changes, auth/authz mistakes, migrations, concurrency/lifecycle defects, and deliberately misleading green tests. Keep task definitions and graders versioned.

`router-cases.json` is only a deterministic policy conformance corpus; it is **not** a coding benchmark.
