# Pattern atlas

This file records design influences and, more importantly, **selection decisions**. Employ-Minds studies public agent systems for mechanisms, not text to copy. General engineering patterns are re-expressed through Employ-Minds' own constraints: quality/token, risk proportionality, independence, and evidence.

## Adopted / adapted

| System | Observed mechanism | Employ-Minds decision |
|---|---|---|
| Claude Code native agents | separate contexts, per-agent tools/models, project agents | Native Claude minds; cheap Scout/Researcher; independent review contexts |
| Codex multi-agent | standalone `.codex/agents`, narrow roles, sandbox/model overrides | Native TOML minds; read-only reviewers; parent-owned routing |
| Everything Claude Code | broad reusable skills/agent conventions | Keep reusable skill vocabulary but collapse governance into one router |
| Superpowers | strict TDD, root-cause debugging, spec/quality review, verification-before-completion | Preserve the strongest discipline while making ceremony risk-adaptive |
| mini-SWE-agent | radical scaffold simplicity; easy-to-understand trajectories | Anti-bloat invariant; prefer model capability + small control plane |
| SWE-agent | benchmark-first autonomous software engineering | Separate harness conformance from real coding evals |
| Aider | repo maps; Architect/Editor split; lint/test loops | Progressive disclosure; optional reasoning/editing split; change-local checks |
| OpenHands | isolated execution/backends and evaluation infrastructure | Isolation as a CRITICAL/parallel-write concern; benchmarkability |
| Cline | independent task worktrees, dependency-aware parallel teams | Parallel writers require isolation and explicit integration ownership |
| Continue | source-controlled repeatable AI checks | Gates/check definitions belong in repo and CI where deterministic |
| OpenCode | read-only Plan vs write-capable Build agents | Capability separation: writers write; judges do not |
| LangGraph | stateful graphs; current preference for tool-based supervisor/context engineering | Primary agent acts as thin supervisor; specialists are tools/contexts, not chatter topology |
| AutoGen | layered runtime + benchmark tooling | Keep orchestration/evaluation distinct; reject unnecessary conversational layers |
| smolagents | simple multi-step agents and explicit memory | Compact working ledger; avoid hidden sprawling transcript memory |
| Plandex | project maps, cumulative diff sandbox, branches/plan versioning | Progressive context + isolation/reversibility for large changes |
| CrewAI | bounded specialized roles, delegation controls, caching/memory options | Narrow roles and explicit delegation; no generic role-play crew by default |
| MetaGPT | SOP-driven software-company roles | **Rejected as default:** too much fixed organizational ceremony for risk-adaptive coding |
| goose | provider/tool interoperability via open protocols | Keep Employ-Minds harness-native and provider-light instead of owning another runtime |

## Explicitly rejected patterns

- **Agent count as capability metric.** More minds increase coordination/context tax.
- **Debate by default.** Multiple agents answering one question is allowed only for consequential diversity, not theater.
- **Full-repository context by default.** Map and retrieve progressively.
- **One omnipotent writer/reviewer.** Self-review is accepted only for FAST; higher profiles demand independent judges.
- **Universal heavyweight planning.** Architecture/design rounds are conditional on material ambiguity.
- **Magic aggregate benchmark scores.** Safety/correctness/token/latency metrics remain visible separately.
- **Vendor-specific model pins in the core policy.** Harness defaults evolve; roles describe capability/cost class and pin only when the native platform benefits from a stable alias.
- **Automatic memory hoarding.** Persist decisions/evidence, not every thought or tool result.

## Admission rule

A new pattern enters Employ-Minds only if it supplies a mechanism we do not already have **and** it can plausibly improve one of: correctness, safety, uncertainty reduction, context cost, latency, or reversibility. Otherwise the pattern stays in research notes instead of becoming another skill.
