---
name: employ-minds-tdd
description: Evidence-first test-driven development for behavior changes and regressions.
---
# Employ-Minds TDD

For observable behavior changes:

1. **RED** — write the smallest test that expresses the missing/failing behavior. Run it and confirm it fails for the intended reason.
2. **GREEN** — implement the minimum production change that makes that test pass. Run the focused test again.
3. **REFACTOR** — improve structure only while behavior remains green; do not smuggle new behavior into refactoring.
4. Run the relevant broader suite after the focused loop.

For bugs, prefer a regression test that reproduces the bug before the fix.

For generated artifacts, metadata-only edits, hardware/external systems, or cases where automation is genuinely impractical, record why and define an alternative repeatable verification check. A test written only after implementation is useful regression coverage, but it is not evidence that RED occurred.
