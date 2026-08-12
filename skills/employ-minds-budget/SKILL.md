---
name: employ-minds-budget
description: Context and token economy rules: spend cognition where it changes decisions, not on duplicated reading or ceremony.
---
# Employ-Minds Budget

Optimize **quality per token**, not raw token count.

1. Keep the primary context for decisions, constraints, accepted design, and the evidence ledger.
2. Delegate noisy exploration/research when the returned summary will be smaller than the material inspected.
3. Use **diff-first, read-on-demand** review: inspect the change, then fetch only code needed to prove or refute a finding.
4. Do not restate the task, repository map, or previous findings unless the restatement changes a decision.
5. Give subagents explicit output contracts. Default to <=250 words for scouting/research and <=12 findings for review.
6. Never spawn two agents to answer the same question unless deliberate diversity is valuable for a critical decision.
7. Parallelize independent questions; serialize dependent gates.
8. Prefer the least expensive capable model for retrieval/classification and reserve stronger reasoning for architecture, difficult debugging, implementation, and consequential review.
9. Prune dead branches. Once evidence rules an approach out, remove it from active context.
10. Compression must preserve file/symbol references, acceptance criteria, unresolved risks, and exact verification evidence.

**Anti-bloat test:** if removing a step does not measurably reduce safety, correctness, uncertainty, or context load, remove the step.
