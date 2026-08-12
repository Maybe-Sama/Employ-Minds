# Performance benchmark plan

Employ-Minds 2.0 should earn replacement of an existing workflow through paired runs, not prompt aesthetics.

## Tracks

### A. Repair / feature correctness
Use reproducible repository tasks with executable graders (SWE-bench Verified-style where practical). Compare the same model/harness baseline against Employ-Minds. Record solved, regression, false-completion, tokens and wall time.

### B. Exploration efficiency
For each task, define or derive relevant files/regions. Measure Scout Recall@K / coverage under fixed returned-line or token budgets, plus whether the downstream solver succeeds. A Scout that reads less but misses the causal path is not efficient.

### C. Review value
Seed realistic defects into otherwise plausible diffs: missing acceptance criterion, concurrency/lifecycle bug, authz/object-ownership bug, misleading green test, stale API assumption, destructive migration without rollback, and prompt/instruction injection in changed repository content. Measure true defects caught, false positives, findings per review, and tokens.

### D. Experience reuse
Pair related tasks from the same subsystem. Compare no prior experience vs compact relevant summary vs deliberately irrelevant summary. Reuse wins only if relevant summaries improve quality/cost without increasing false completion; irrelevant memories should be ignored.

## Experimental discipline
- same base commit and acceptance criteria;
- same primary model/config where comparing harnesses;
- multiple runs for stochastic models;
- freeze task graders before seeing candidate outputs;
- never count a model's own self-assessment as solved;
- preserve failed trajectories, not just wins;
- publish per-task results so aggregate gains cannot hide critical regressions.

The included scorer intentionally keeps safety/correctness/cost dimensions separate. A new Employ-Minds mechanism is admitted only when it fixes a demonstrated failure mode or improves a meaningful Pareto axis.
