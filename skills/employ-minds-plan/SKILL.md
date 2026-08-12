---
name: employ-minds-plan
description: Produce the smallest executable plan justified by branching, coordination, risk, and irreversibility.
---
# Employ-Minds Plan

Planning is a tool, not a ceremony. If the implementation path is obvious and reversible, use a micro-plan. Spend detail where choices or failure cost are real.

A useful plan identifies:
- acceptance criteria by short IDs rather than repeatedly restating prose;
- affected boundaries/files only as far as currently known;
- ordered slices where order matters and independent slices where it does not;
- the RED/regression evidence for behavior changes;
- unresolved external facts that must be researched before coding;
- compatibility, data, security, rollout or rollback concerns when triggered;
- required review/verification gates.

For STANDARD work, a few precise bullets are often enough. For CRITICAL work, add assumptions, rollback/data-safety procedure, stop conditions, and the evidence required before irreversible action.

Do not predict exact implementation details that repository inspection has not established. A plan that fabricates certainty is worse than a short plan with an explicit unknown.
