# Employ-Minds

> **Employ the right mind for the risk — and no more.**

[![Validate](https://github.com/Maybe-Sama/Employ-Minds/actions/workflows/validate.yml/badge.svg)](https://github.com/Maybe-Sama/Employ-Minds/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Employ-Minds is an **AI-assisted, risk-adaptive native multi-agent engineering harness** for Claude Code and Codex. Its objective is not maximum agent count; it is **maximum trustworthy engineering per unit of context, latency and cost**.

It combines one small risk router with native specialist contexts, TDD/root-cause discipline, independent specification and quality review, security gates, and claim-mapped fresh verification.

## The architecture

```text
request
  |
  v
risk router ---- FAST -----------------> smallest change -> fresh check
  |
  +---- STANDARD -> [Scout?] [Architect?] [Debugger/Researcher?]
  |                    -> writer -> Spec Review -> Quality Review -> [Security?] -> Verifier
  |
  +---- CRITICAL -> explicit plan/rollback + isolated work
                       -> writer -> Spec -> Quality -> Security -> Verifier
```

`?` means **only when it adds information**. This is deliberate: multi-agent overhead is a tax, not a badge of sophistication.

## Native minds

Employ-Minds 2.0 installs real project subagents, not role-play prompts:

| Mind | Writes? | Job |
|---|---:|---|
| Scout | no | compact codebase map; keep noisy exploration out of parent context |
| Architect | no | material design decisions, invariants, plan, rollback |
| Researcher | no | current/versioned external facts from primary sources |
| Debugger | no | reproduce and establish root cause before fixes |
| Implementer | **yes** | bounded implementation; never self-certifies completion |
| Spec Reviewer | no | independent acceptance-criteria compliance |
| Quality Reviewer | no | independent correctness/architecture/test review |
| Security Reviewer | no | independent trust-boundary/security/data gate |
| Verifier | no | fresh claim -> check -> result ledger; final SHIP/NO-SHIP |

Claude agents install under `.claude/agents/em-*.md`; Codex agents under `.codex/agents/em-*.toml`. Skills remain namespaced and project-local.

## Context economy

Employ-Minds uses **progressive disclosure**: map/diff/symbols first, targeted snippets second, full files/logs only for a concrete unanswered question. Child agents keep raw exploration in their own context and return compact evidence packets. Review is diff-first. Ordinary independent fan-out is capped at three.

The primary context retains decisions, acceptance criteria, unresolved uncertainty and final evidence — not transcripts.

## Install

Requires Python 3.9+.

```bash
git clone https://github.com/Maybe-Sama/Employ-Minds.git
cd Employ-Minds
./scripts/install.sh --project /path/to/project --target both
python scripts/doctor.py --project /path/to/project --target both
```

Windows:

```powershell
.\scripts\install.ps1 --project C:\path\to\project --target both
python .\scripts\doctor.py --project C:\path\to\project --target both
```

Targets: `claude`, `codex`, `both`. Reinstallation is idempotent. Existing `CLAUDE.md`, `AGENTS.md`, unrelated skills and unrelated agents are preserved; uninstall removes only Employ-Minds-owned namespaces/blocks.

## Use

Usually, just ask for the engineering task. For explicit routing in Claude:

```text
/employ-minds Implement this. Use the minimum safe profile and do not claim success without fresh evidence.
```

Or in either harness:

```text
Use Employ-Minds. Optimize quality per token; escalate only when evidence requires it.
```

## Profiles

- **FAST** — tiny/local/clear/low-risk: no ceremonial agent chain.
- **STANDARD** — normal engineering: independent spec + quality + verifier; optional specialist minds only when needed.
- **CRITICAL** — auth, money, secrets, migrations, destructive/data/security or high-blast-radius work: explicit rollback/data safety, independent reviews, security gate and strong verification.

Profiles escalate dynamically when uncertainty or blast radius grows.

## Evals, not vibes

```bash
python -m unittest discover -s tests -v
python scripts/doctor.py --self-check
python scripts/eval_policy.py
python scripts/score_runs.py evals/example-results.jsonl
```

CI proves the harness installs and preserves project content. It does **not** prove Employ-Minds outperforms another coding workflow. `evals/` defines the A/B result format so real task corpora can compare solved rate, false completion, regressions, critical misses, reviewer catches, tokens and latency without hiding tradeoffs behind a magic score.

## Design principles

See [`docs/DESIGN_PRINCIPLES.md`](docs/DESIGN_PRINCIPLES.md). The short version: progressive disclosure, strong cognition only where scarce, writer/judge separation, evidence over confidence, risk-proportional ceremony, stop unproductive loops, and delete any component that cannot justify its cost.

## Provenance

Employ-Minds is independently designed and maintained with AI assistance. It synthesizes and extends software-engineering patterns found across public agent systems. Two initial MIT-licensed inspirations are tracked explicitly: **Everything Claude Code (ECC)** and **Superpowers**. Their license notices are preserved under `third_party/`, and the initial reference revisions are pinned in `UPSTREAMS.lock.json`.

General methods such as TDD, root-cause debugging, subagents and code review are not claimed as proprietary. See [`NOTICE.md`](NOTICE.md) and [`docs/UPSTREAM.md`](docs/UPSTREAM.md).

MIT licensed.
