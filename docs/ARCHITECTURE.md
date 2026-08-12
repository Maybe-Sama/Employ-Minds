# Architecture

## One governor, native specialist contexts

Employ-Minds is a thin control plane over the native agent primitives of each coding harness. The **primary agent owns routing and integration**; specialists are bounded contexts, not a simulated company hierarchy.

```text
request
  |
  v
risk + uncertainty router
  |
  +-- FAST -------------------------------- small edit -> fresh check
  |
  +-- STANDARD -- optional discovery/reasoning minds
  |                  |                    |
  |                  v                    v
  |                writer -> spec -> quality -> [security] -> verifier
  |
  +-- CRITICAL -- explicit acceptance + rollback + isolation
                       -> writer -> spec -> quality -> security -> verifier
```

## Why the primary agent is the governor

A supervisor should not become another expensive conversation layer. Claude/Codex already provide native subagent dispatch. The primary context holds the user's intent, accepted design, unresolved risks, and evidence ledger and calls narrow specialists as tools. This also avoids nested delegation limitations and makes the routing behavior inspectable.

## Native separation

Claude installs project minds under `.claude/agents/em-*.md`; Codex installs `.codex/agents/em-*.toml`. Read-oriented Codex minds are sandboxed read-only and only the implementer gets workspace-write. Claude roles restrict their declared tools and are instructed not to edit; the final verifier never repairs what it judges.

Independence is a correctness mechanism: an implementer is optimized to make the plan work; a reviewer is optimized to falsify assumptions; a verifier is optimized to decide whether claims are actually proven.

## Progressive context disclosure

Information enters the primary context in levels:
1. **map** — diff/stat, filenames, symbols, call sites, test names;
2. **targeted evidence** — relevant snippets/interfaces/errors/tests;
3. **full material** — only when a concrete unanswered question requires it.

Raw exploration stays with Scout/Researcher where possible. Their result is a compact evidence packet with references. The primary context therefore accumulates decisions rather than transcripts.

## Reasoning vs editing

Architecture is activated only when a real design decision exists. Separating reasoning from editing can increase focus, but making every two-line fix pay for an Architect wastes time/tokens. FAST avoids it; STANDARD/CRITICAL invoke Architect when ambiguity, cross-cutting boundaries or rollback concerns justify the cost.

## Review pipeline

Specification review precedes quality review because elegant wrong behavior is still wrong. Reviews are diff-first and expand context only to validate a finding. A reviewer reports evidence/failure mode and cannot quietly fix its own finding. After corrections, the relevant review is repeated against the new diff.

Security is trigger-based for STANDARD and mandatory for CRITICAL. The final verifier maps each important completion claim to a **fresh check after the final relevant change** and returns SHIP/NO-SHIP.

## Parallelism

Read-only independent work may fan out (policy caps ordinary fan-out). Parallel writers require disjoint scopes **and isolated worktrees/branches/sandboxes**. Shared contracts serialize. Integration always gets a fresh combined review/verification pass.

## State and loop control

Long tasks use a compact ledger: requirements/non-goals, risk profile, settled decisions, open hypotheses, delegated ownership, changed boundaries, gate state, and latest evidence. Two consecutive cycles with no new evidence trigger a changed hypothesis/instrumentation/scope rather than repeated prompting.

## Risk profiles

**FAST:** minimum ceremony; smallest correct change + diff + focused fresh evidence.

**STANDARD:** normal engineering; optional specialist discovery/design/debug/research, bounded writer, independent spec/quality, triggered security, final verifier.

**CRITICAL:** auth, money, secrets, migrations, destructive/data/security/high-blast-radius work; explicit rollback/data safety, isolation, independent reviews, mandatory security, strong claim-mapped evidence.

Risk can only be lowered when new evidence actually removes a trigger, never merely to save tokens.

## Installation boundary

The repository is canonical. `scripts/install.py` owns only namespaced material:
- Claude: `.claude/skills/employ-minds-*`, `.claude/agents/em-*`, `.claude/commands/employ-minds.md`, managed `CLAUDE.md` block.
- Codex: `.agents/skills/employ-minds-*`, `.codex/agents/em-*`, managed `AGENTS.md` block.
- Shared: `.employ-minds/` policy/roles/rules/version/backups.

Reinstallation is idempotent and uninstall cannot delete unrelated skills, agents, or project instructions.
