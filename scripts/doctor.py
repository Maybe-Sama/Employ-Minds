#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

BEGIN = "<!-- EMPLOY-MINDS:BEGIN -->"
END = "<!-- EMPLOY-MINDS:END -->"
SKILLS = ["router", "brainstorm", "plan", "tdd", "debug", "execute", "review", "verify", "security", "parallel", "research", "context", "release", "budget"]
AGENTS = ["scout", "architect", "researcher", "debugger", "implementer", "spec-reviewer", "quality-reviewer", "security-reviewer", "verifier"]
READ_ONLY_AGENTS = set(AGENTS) - {"implementer"}


def expected_skills() -> list[str]:
    return [f"employ-minds-{name}" for name in SKILLS]


def expected_claude_agents() -> list[str]:
    return [f"em-{name}.md" for name in AGENTS]


def expected_codex_agents() -> list[str]:
    return [f"em-{name}.toml" for name in AGENTS]


def check_project(project: Path, target: str) -> list[str]:
    errors: list[str] = []
    payload = project / ".employ-minds"
    for rel in ("VERSION", "config/employ-minds-policy.json", "config/prompt-budget.json", "rules/core.md", "agents/manifest.json", "install-state.json"):
        if not (payload / rel).exists():
            errors.append(f"missing .employ-minds/{rel}")

    policy_path = payload / "config/employ-minds-policy.json"
    if policy_path.exists():
        try:
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            if policy.get("default_profile") != "standard": errors.append("unexpected default profile")
            if not policy.get("completion_requires_fresh_evidence"): errors.append("fresh-evidence invariant disabled")
            if not policy.get("native_agent_separation"): errors.append("native-agent separation disabled")
        except Exception as exc:
            errors.append(f"invalid policy JSON: {exc}")

    state = {}
    state_path = payload / "install-state.json"
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            if state.get("name") != "employ-minds": errors.append("install-state owner mismatch")
            if not state.get("native_agents"): errors.append("install-state native_agents missing/false")
        except Exception as exc:
            errors.append(f"invalid install-state JSON: {exc}")

    configs = (
        ("claude", target in ("claude", "both"), "CLAUDE.md", project / ".claude/skills"),
        ("codex", target in ("codex", "both"), "AGENTS.md", project / ".agents/skills"),
    )
    for kind, enabled, instruction, skill_base in configs:
        if not enabled:
            continue
        f = project / instruction
        text = f.read_text(encoding="utf-8") if f.exists() else ""
        if BEGIN not in text or END not in text:
            errors.append(f"{instruction} managed block missing")
        for suffix in SKILLS:
            if not (skill_base / f"employ-minds-{suffix}/SKILL.md").exists():
                errors.append(f"{kind}: missing skill employ-minds-{suffix}")

        if kind == "claude":
            if not (project / ".claude/commands/employ-minds.md").exists():
                errors.append("claude: missing /employ-minds command")
            if sorted(state.get("claude_skills", [])) != sorted(expected_skills()):
                errors.append("claude: install-state skill ownership mismatch")
            if sorted(state.get("claude_agents", [])) != sorted(expected_claude_agents()):
                errors.append("claude: install-state agent ownership mismatch")
            if state.get("claude_command") != "employ-minds.md":
                errors.append("claude: install-state command ownership mismatch")
            for name in AGENTS:
                path = project / ".claude/agents" / f"em-{name}.md"
                if not path.exists():
                    errors.append(f"claude: missing native agent em-{name}")
                elif name in READ_ONLY_AGENTS and "permissionMode: plan" not in path.read_text(encoding="utf-8"):
                    errors.append(f"claude: read-only agent em-{name} lacks plan permission mode")
        else:
            if sorted(state.get("codex_skills", [])) != sorted(expected_skills()):
                errors.append("codex: install-state skill ownership mismatch")
            if sorted(state.get("codex_agents", [])) != sorted(expected_codex_agents()):
                errors.append("codex: install-state agent ownership mismatch")
            for name in AGENTS:
                path = project / ".codex/agents" / f"em-{name}.toml"
                if not path.exists():
                    errors.append(f"codex: missing native agent em-{name}")
                elif name in READ_ONLY_AGENTS and 'sandbox_mode = "read-only"' not in path.read_text(encoding="utf-8"):
                    errors.append(f"codex: read-only agent em-{name} lacks read-only sandbox")
    return errors


def self_check(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        policy = json.loads((root / "config/employ-minds-policy.json").read_text(encoding="utf-8"))
        if policy.get("schema_version") != 2: errors.append("policy schema_version must be 2")
        if policy.get("default_profile") != "standard": errors.append("policy default_profile must be standard")
        if not policy.get("completion_requires_fresh_evidence"): errors.append("policy must require fresh evidence")
        if not policy.get("native_agent_separation"): errors.append("policy must require native-agent separation")
        if policy.get("review_order", [None])[0] != "spec_compliance": errors.append("spec compliance must precede quality review")
    except Exception as exc:
        errors.append(f"policy: {exc}")

    manifest_path = root / "agents/manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("schema_version") != 1: errors.append("agent manifest schema_version must be 1")
        if list(manifest.get("agents", {})) != AGENTS: errors.append("agent manifest names/order do not match doctor contract")
    except Exception as exc:
        errors.append(f"agent manifest: {exc}")

    for suffix in SKILLS:
        path = root / "skills" / f"employ-minds-{suffix}/SKILL.md"
        if not path.exists(): errors.append(f"missing source skill employ-minds-{suffix}")
        elif f"name: employ-minds-{suffix}" not in path.read_text(encoding="utf-8"): errors.append(f"skill frontmatter mismatch: employ-minds-{suffix}")

    for name in AGENTS:
        claude = root / "native/claude/agents" / f"em-{name}.md"
        codex = root / "native/codex/agents" / f"em-{name}.toml"
        if not claude.exists(): errors.append(f"missing Claude native agent em-{name}")
        else:
            text = claude.read_text(encoding="utf-8")
            if f"name: em-{name}" not in text: errors.append(f"Claude agent name mismatch: em-{name}")
            if name in READ_ONLY_AGENTS and "permissionMode: plan" not in text: errors.append(f"Claude agent em-{name} must be plan/read-only")
        if not codex.exists(): errors.append(f"missing Codex native agent em-{name}")
        else:
            text = codex.read_text(encoding="utf-8")
            if f'name = "em-{name}"' not in text: errors.append(f"Codex agent name mismatch: em-{name}")
            expected = 'sandbox_mode = "read-only"' if name in READ_ONLY_AGENTS else 'sandbox_mode = "workspace-write"'
            if expected not in text: errors.append(f"Codex agent em-{name} sandbox mismatch")

    required_files = (
        "LICENSE", "NOTICE.md", "VERSION", "README.md", "CHANGELOG.md", "UPSTREAMS.lock.json",
        "agents/manifest.json", "config/prompt-budget.json", "scripts/install.py", "scripts/doctor.py",
        "scripts/render_agents.py", "scripts/prompt_budget.py", "scripts/eval_policy.py", "scripts/score_runs.py",
        "docs/ARCHITECTURE.md", "docs/DESIGN_PRINCIPLES.md", "docs/UPSTREAM.md", "commands/employ-minds.md",
        "evals/README.md", "evals/BENCHMARK_PLAN.md", "evals/router-cases.json", "evals/run-result.schema.json",
        "research/PATTERN_ATLAS.md", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json",
    )
    for rel in required_files:
        if not (root / rel).exists(): errors.append(f"missing {rel}")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description="Validate Employ-Minds source/project installations.")
    p.add_argument("--project")
    p.add_argument("--target", choices=["claude", "codex", "both"], default="both")
    p.add_argument("--self-check", action="store_true")
    args = p.parse_args()
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    if args.self_check: errors += self_check(root)
    if args.project: errors += check_project(Path(args.project).expanduser().resolve(), args.target)
    if not args.self_check and not args.project: p.error("use --self-check and/or --project")
    if errors:
        print("Employ-Minds doctor: FAIL")
        for e in errors: print(" -", e)
        return 1
    print("Employ-Minds doctor: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
