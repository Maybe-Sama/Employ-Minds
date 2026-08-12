# Changelog

## 2.0.0 - 2026-08-12

- Turn specialist minds into **native project subagents** for Claude Code and Codex, with real read-only reviewer/verifier boundaries and bounded Claude turns.
- Make `agents/manifest.json` the single source of truth and generate both harness adapters with CI parity checks.
- Add a read-only Scout plus strict writer/reviewer/verifier separation; the primary agent remains the thin governor instead of adding an orchestrator persona.
- Add context/token economy rules: progressive disclosure, diff-first review, read-on-demand, bounded summaries, capped fan-out, loop detection, and anti-bloat admission rules.
- Add a CI-enforced **prompt budget** for always-on discovery metadata, managed instructions, individual skills, and aggregate contracts.
- Make STANDARD and CRITICAL review genuinely independent instead of role-play in one context.
- Require isolated worktrees/branches/sandboxes for parallel writers and fresh integrated verification after combination.
- Add contrastive brainstorming for useful novelty without idea-list sprawl.
- Add an eval lab that separates harness conformance from real A/B coding performance and exposes correctness, false-completion, regressions, critical misses, tokens, and latency separately.
- Make native-agent installation ownership exact: reinstall/uninstall can only mutate agent files recorded as Employ-Minds-owned, even when unrelated agents share the `em-` prefix.
- Add a research Pattern Atlas that records both adopted mechanisms and rejected agent-theater/bloat patterns.
- Upgrade policy schema to v2, strengthen `doctor`, and expand cross-platform CI gates.
- Clarify AI-assisted authorship and upstream provenance.
- Keep internal evidence/gates structured while explicitly requiring natural, concise, teammate-like user-facing handoffs.

## 1.0.0 - 2026-08-12

- Initial risk-adaptive harness with FAST/STANDARD/CRITICAL routing, skills, role contracts, safe installer, doctor, and cross-platform CI.
