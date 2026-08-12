---
name: employ-minds-context
description: Keep long-running agent work coherent with a compact decision, hypothesis, gate, and evidence ledger.
---
# Employ-Minds Context

For long or multi-agent tasks, maintain a compact working ledger instead of relying on the full conversation transcript.

Track:
- accepted requirements and non-goals;
- current risk profile and why;
- architecture decisions already settled;
- open hypotheses / unknowns;
- active delegated tasks and ownership;
- files/contracts changed;
- required gates and their status;
- verification evidence captured after the latest relevant change.

Compress old exploration aggressively once a decision is settled, but do not replace proof with summaries. A summary may say a test passed; the verifier still needs fresh repeatable evidence before the final claim.
