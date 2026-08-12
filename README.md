# Employ-Minds

> **Employ the right mind for the risk.**

[![Validate](https://github.com/Maybe-Sama/Employ-Minds/actions/workflows/validate.yml/badge.svg)](https://github.com/Maybe-Sama/Employ-Minds/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Employ-Minds is a **risk-adaptive engineering harness for coding agents**. It combines the breadth of a full agent harness with the engineering discipline of TDD, root-cause debugging, independent review, security gates, and fresh verification — without installing two competing workflow governors.

It is designed for **Claude Code and Codex-style project agents** and intentionally keeps one canonical decision-maker: the **Employ-Minds Router**.

## Why it exists

Broad harnesses are excellent at giving an agent more capabilities. Strict engineering workflows are excellent at making an agent less reckless. Stacking both wholesale often produces duplicate planning, duplicated reviews, conflicting instructions, and unnecessary ceremony.

Employ-Minds takes a different approach:

```text
                         ┌──────────────────┐
                         │   user request   │
                         └────────┬─────────┘
                                  │
                         ┌────────▼─────────┐
                         │ Employ-Minds     │
                         │ Router           │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                  FAST         STANDARD      CRITICAL
                    │             │             │
                    └──────┬──────┴──────┬──────┘
                           │             │
                     specialist minds + gates
                           │             │
                     fresh verification
```

One governor. Multiple specialist minds. Ceremony proportional to risk.

## Risk profiles

| Profile | Typical work | Required discipline |
|---|---|---|
| **FAST** | tiny/local change, obvious fix, docs, low blast radius | inspect → smallest change → self-review → focused fresh verification |
| **STANDARD** | features, bugs, integrations, bounded refactors | plan → TDD for behavior → implement → spec review → quality review → relevant verification |
| **CRITICAL** | auth, permissions, payments, migrations, secrets, destructive/data/security work, major refactors | research → explicit plan + rollback → TDD/equivalent evidence → independent reviews → security gate → strong verification |

The profile can **escalate at any time**. A task that discovers production data, unclear root cause, a hidden dependency, or a wider blast radius stops being “small” just because it started that way.

## What gets installed

Employ-Minds is repository-local. It does not replace your own project instructions.

```text
CLAUDE.md                         # managed block only; your text is preserved
AGENTS.md                         # managed block only; your text is preserved
.claude/skills/employ-minds-*     # Claude project skills
.claude/commands/employ-minds.md  # explicit Claude command
.agents/skills/employ-minds-*     # Codex / compatible agent skills
.employ-minds/                    # canonical policy, roles, rules, version, backups
```

The installer is **idempotent** and only owns the namespaced content above.

## Install

Requires Python 3.9+.

```bash
git clone https://github.com/Maybe-Sama/Employ-Minds.git
cd Employ-Minds
```

### macOS / Linux

```bash
./scripts/install.sh --project /path/to/project --target both
```

### Windows PowerShell

```powershell
.\scripts\install.ps1 --project C:\path\to\project --target both
```

Targets are `claude`, `codex`, or `both` (default).

Validate the installation:

```bash
python scripts/doctor.py --project /path/to/project --target both
```

Remove only Employ-Minds-managed content:

```bash
./scripts/uninstall.sh --project /path/to/project --target both
```

## Use

Usually you do not need special prompting. Give the coding agent the task normally; the managed project instruction routes non-trivial engineering through `employ-minds-router`.

When you want to be explicit in Claude Code, use:

```text
/employ-minds Implement the requested change. Route it by risk and do not claim completion without fresh evidence.
```

Or simply say:

```text
Use Employ-Minds. Pick the risk profile before editing and apply every gate required by that profile.
```

## The minds

The harness separates **thinking responsibilities** so one agent is not simultaneously author, reviewer, security auditor, and judge of its own success.

| Mind | Responsibility |
|---|---|
| Orchestrator | route, delegate, escalate, collect evidence, enforce stop conditions |
| Architect | frame the problem, constraints, acceptance criteria, plan and rollback |
| Researcher | resolve current/versioned external facts from primary sources |
| Debugger | reproduce and identify root cause before patching |
| Implementer | make a bounded change and report exact evidence |
| Spec reviewer | decide whether the requested behavior was actually implemented |
| Quality reviewer | correctness, architecture, maintainability, tests, lifecycle, concurrency |
| Security reviewer | trust boundaries, authz, injection, secrets, destructive/data risks |
| Verifier | independently map completion claims to fresh checks |

## Skills

- `employ-minds-router` — risk classification, gate selection and dynamic escalation.
- `employ-minds-brainstorm` — design exploration only when ambiguity is material.
- `employ-minds-plan` — executable plan with files, tests, risks and rollback.
- `employ-minds-tdd` — RED → GREEN → REFACTOR; regression-first bug fixing.
- `employ-minds-debug` — root-cause-first debugging with falsifiable hypotheses.
- `employ-minds-execute` — small verified increments and scope control.
- `employ-minds-review` — specification compliance before code quality.
- `employ-minds-security` — security/destructive-change gate.
- `employ-minds-verify` — completion claims require fresh observable evidence.
- `employ-minds-parallel` — parallelize only independent tasks with explicit contracts.
- `employ-minds-research` — current/unfamiliar external behavior from primary sources.
- `employ-minds-context` — context-budget control and evidence ledger for long tasks.
- `employ-minds-release` — clean final diff, release notes and ship/no-ship gate.

## The invariant

> **No completion claim outruns its evidence.**

A green build does not prove runtime behavior. An unrelated test suite does not prove an acceptance criterion. A reviewer saying “looks good” does not prove a migration is reversible. Employ-Minds requires evidence that matches the claim being made.

## Development

```bash
python -m unittest discover -s tests -v
python scripts/doctor.py --self-check
python -m compileall -q scripts tests
```

On Bash-capable systems:

```bash
bash -n scripts/install.sh scripts/uninstall.sh
```

CI runs the validation suite across Linux, Windows, and macOS.

## Architecture and docs

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — internal model and gate ordering.
- [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md) — concrete FAST/STANDARD/CRITICAL examples.
- [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — shortest path to adoption.
- [`docs/UPSTREAM.md`](docs/UPSTREAM.md) — upstream provenance and synthesis boundaries.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution contract.
- [`SECURITY.md`](SECURITY.md) — responsible disclosure and security scope.

## Upstream inspiration and license

Employ-Minds is independently authored and MIT licensed. It synthesizes architectural/process ideas from two MIT-licensed projects:

- **Everything Claude Code (ECC)** — `affaan-m/ECC`
- **Superpowers** — `obra/superpowers`

Exact upstream revisions used for the initial synthesis are pinned in [`UPSTREAMS.lock.json`](UPSTREAMS.lock.json), with preserved license notices under [`third_party/`](third_party/). Employ-Minds is not affiliated with or endorsed by either upstream project.
