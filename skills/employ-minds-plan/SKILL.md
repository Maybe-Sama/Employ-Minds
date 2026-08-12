---
name: employ-minds-plan
description: Convert an accepted goal into an executable engineering plan with files, tests, risks, and evidence.
---
# Employ-Minds Plan

A plan must be executable by another competent agent without guessing the core intent.

Include:
- accepted behavior / acceptance criteria;
- relevant files or boundaries to inspect/change;
- ordered implementation increments;
- RED test or regression evidence for behavior changes;
- external research questions if any;
- data/security/compatibility risks and rollback notes when applicable;
- review gates required by the current profile;
- final commands or observable checks that prove completion.

For STANDARD and CRITICAL work, split independent tasks clearly enough that `employ-minds-parallel` can determine whether concurrent delegation is safe. Avoid vague steps such as “implement feature” or “test everything.”
