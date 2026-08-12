---
name: employ-minds-brainstorm
description: Resolve meaningful design ambiguity without turning straightforward tasks into design theater.
---
# Employ-Minds Brainstorm

Use only when there are multiple materially different valid designs or when requirements contain unresolved tradeoffs.

1. State the decision to make and the invariant that must survive it.
2. Identify repository constraints before proposing architecture.
3. Generate 2–4 meaningfully different options, not cosmetic variants.
4. Compare correctness risk, complexity, reversibility, operability, testability, and migration cost where relevant.
5. Choose one direction and record why the rejected options lost.
6. Convert the decision into acceptance criteria for `employ-minds-plan`.

Do not invoke brainstorming for a clear mechanical edit. Design ceremony is a cost and should buy risk reduction.
