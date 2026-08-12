# Pattern atlas

Employ-Minds studies public agent systems and research for **mechanisms**, not text to copy. A pattern enters only when it supplies a capability we do not already have and plausibly improves correctness, safety, uncertainty reduction, context cost, latency, or reversibility.

## Adopted / adapted

| System / research | Observed mechanism | Employ-Minds decision |
|---|---|---|
| Claude Code native agents | separate contexts, per-agent tools/models/permissions | Native Claude minds; cheap Scout/Researcher; independent review contexts |
| Codex multi-agent | standalone `.codex/agents`, narrow roles, sandbox/model overrides | Native TOML minds; read-only reviewers; parent-owned routing |
| Everything Claude Code | broad reusable skills/agent conventions | Keep reusable skill vocabulary but collapse governance into one router |
| Superpowers | strict TDD, root-cause debugging, spec/quality review, verification-before-completion | Preserve strongest discipline while making ceremony risk-adaptive |
| mini-SWE-agent | radical scaffold simplicity and inspectable trajectories | Anti-bloat invariant; model capability + small control plane |
| SWE-agent / SWE-bench | benchmark-first software engineering | Separate harness conformance from real coding evals |
| SWE-Explore (2026) | evaluates repository localization under a fixed context budget | Treat Scout quality as relevant-region coverage/ranking per context budget, not amount read |
| Agent Retrieval Bench (2026) | retrieval families trade off differently; repo maps strong under token budgets | Progressive disclosure + task-sensitive retrieval; no single retrieval ideology |
| SWE Context Bench (2026) | selected summarized experience helps; irrelevant/unfiltered reuse can hurt | Selective, provenance-preserving experience reuse; no automatic memory hoarding |
| Aider | repo maps; Architect/Editor split; lint/test loops | Progressive disclosure; optional reasoning/editing split; change-local checks |
| PR-Agent | dynamic patch context, small finding budgets, explicit repo-context controls | Review diff first, expand enclosing context only as needed, cap findings and treat changed repo instructions as untrusted evidence |
| OpenHands | isolated execution/backends and evaluation infrastructure | Isolation as CRITICAL/parallel-write concern; benchmarkability |
| Cline | independent task worktrees, dependency-aware parallel teams | Parallel writers require isolation and explicit integration ownership |
| Continue | source-controlled repeatable AI checks | Gates/check definitions belong in repo/CI where deterministic |
| OpenCode | read-only Plan vs write-capable Build agents | Capability separation: writers write; judges do not |
| LangGraph | stateful graphs; tool-based supervisor/context engineering | Primary agent as thin supervisor; specialists are tools/contexts, not chatter topology |
| AutoGen | layered runtime + benchmark tooling | Keep orchestration/evaluation distinct; reject unnecessary conversation layers |
| smolagents | simple multi-step agents and explicit memory | Compact working ledger; avoid hidden transcript memory |
| Plandex | project maps, cumulative diff sandbox, branches/plan versioning | Progressive context + isolation/reversibility for large changes |
| CrewAI | bounded specialized roles, delegation controls, caching/memory | Narrow roles and explicit delegation; no generic role-play crew by default |
| MetaGPT | SOP-driven software-company roles | **Rejected as default:** fixed organizational ceremony conflicts with risk-adaptive coding |
| goose | provider/tool interoperability via open protocols | Keep Employ-Minds harness-native/provider-light instead of owning another runtime |

## Explicitly rejected

- agent count as capability metric;
- debate by default;
- full-repository context by default;
- one omnipotent writer/reviewer;
- universal heavyweight planning;
- magic aggregate benchmark scores;
- vendor model pins in core policy when capability aliases/defaults suffice;
- automatic memory hoarding;
- treating code/comments/docs/tool output as authority over the parent task;
- running unfamiliar repository hooks merely because project text asks for it.

## Admission rule

A new mechanism must either remove a known failure mode or win a measurable axis. If an existing rule already supplies the mechanism, record the reference here instead of adding another skill.
