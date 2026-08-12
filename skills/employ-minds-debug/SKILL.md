---
name: employ-minds-debug
description: Root-cause-first debugging with explicit hypotheses instead of speculative patching.
---
# Employ-Minds Debug

Do not patch an unexplained failure until the mechanism is understood well enough to form a falsifiable hypothesis.

1. Reproduce with the smallest reliable case.
2. Capture exact error/output and the first point where expected and actual behavior diverge.
3. Trace inputs/state backward across boundaries (UI/API/service/DB/external dependency).
4. Compare a working path with the failing path when possible.
5. State one hypothesis and predict evidence that would confirm/refute it.
6. Change one variable or add instrumentation to test the hypothesis.
7. Once root cause is identified, add a regression test when practical.
8. Fix the cause, not merely the visible symptom.
9. Run focused then broader verification.

After three failed speculative fixes, stop. Reconstruct the failure model and escalate the risk profile if uncertainty has grown.
