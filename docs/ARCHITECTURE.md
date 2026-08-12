# Architecture

## The core idea: one governor, many minds

Employ-Minds separates **orchestration** from **specialist cognition**. The router owns the workflow. Skills define reusable gates. Specialist roles perform bounded work and return structured evidence. This prevents planning, implementation, review, and completion from all being judged by the same context and incentives.

The design draws from two complementary traditions: broad agent harnesses that provide composition and tool-native conventions, and strict engineering workflows that impose TDD, debugging, review and verification discipline. Loading both as independent governors creates overlap. Employ-Minds collapses that overlap into one deterministic control plane.

## Control plane

```text
request
  │
  ▼
route ──► FAST / STANDARD / CRITICAL
  │
  ├─► research/design when uncertainty requires it
  ├─► plan
  ├─► test + implement
  ├─► specification review
  ├─► quality review
  ├─► security review when triggered
  └─► verification mapped to completion claims
```

The router may escalate the profile after any gate. A hidden dependency or production-data touch discovered during implementation changes the risk model immediately.

## Profiles

### FAST

Purpose: avoid turning a two-line safe change into a committee meeting.

Non-negotiables remain: inspect the relevant code, make the smallest correct change, review the diff, and verify the actual behavior freshly.

### STANDARD

Purpose: default professional engineering path.

Requires a short executable plan, TDD for observable behavior where practical, bounded implementation, spec review before quality review, security only when triggered, and fresh relevant verification.

### CRITICAL

Purpose: make high-blast-radius changes deliberately hard to self-approve.

Requires explicit assumptions and rollback/data-safety thinking, current research when external behavior is version-sensitive, strong test evidence, independent reviews when the harness can provide them, mandatory security review, and completion evidence tied to each important claim.

## Why spec review precedes quality review

A clean, elegant implementation of the wrong requirement is still wrong. The first reviewer asks only whether the accepted behavior exists without unintended scope. Only after that passes does quality review judge architecture, correctness properties, maintainability and tests.

## Agent handoff contract

A delegated mind receives:

- goal and bounded scope;
- relevant acceptance criteria;
- files/areas it may change or inspect;
- profile and active gates;
- expected evidence.

It returns:

- conclusion or files changed;
- exact checks executed and outcomes;
- assumptions and unresolved risks;
- explicit blockers.

No subagent may declare the entire parent task complete unless it is the orchestrator and all required gates have returned evidence.

## Context control

Long tasks fail when the working context becomes an unstructured transcript. `employ-minds-context` maintains a compact ledger of accepted requirements, decisions, open hypotheses, changed files, gate status, and verification evidence. Summaries are working memory, not proof; raw command output or repeatable checks remain the evidence source.

## Integration model

The repository is canonical. `scripts/install.py` adapts it into tool-native project locations:

- Claude: `.claude/skills/employ-minds-*`, `.claude/commands/employ-minds.md`, managed `CLAUDE.md` block.
- Codex/compatible agents: `.agents/skills/employ-minds-*`, managed `AGENTS.md` block.
- Shared payload: `.employ-minds/` containing policy, role definitions, rules, version and first-install backups.

The installer is idempotent and never takes ownership of instructions outside the `EMPLOY-MINDS` managed markers.
