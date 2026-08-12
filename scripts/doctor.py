#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

BEGIN = "<!-- EMPLOY-MINDS:BEGIN -->"
END = "<!-- EMPLOY-MINDS:END -->"
SKILLS = ["router", "brainstorm", "plan", "tdd", "debug", "execute", "review", "verify", "security", "parallel", "research", "context", "release", "budget"]
AGENTS = ["scout", "architect", "researcher", "debugger", "implementer", "spec-reviewer", "quality-reviewer", "security-reviewer", "verifier"]


def check_project(project: Path, target: str) -> list[str]:
    errors: list[str] = []
    payload = project / ".employ-minds"
    for rel in ("VERSION", "config/employ-minds-policy.json", "rules/core.md", "install-state.json"):
        if not (payload / rel).exists(): errors.append(f"missing .employ-minds/{rel}")
    policy_path = payload / "config/employ-minds-policy.json"
    if policy_path.exists():
        try:
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            if policy.get("default_profile") != "standard": errors.append("unexpected default profile")
            if not policy.get("completion_requires_fresh_evidence"): errors.append("fresh-evidence invariant disabled")
            if not policy.get("native_agent_separation"): errors.append("native-agent separation disabled")
        except Exception as exc:
            errors.append(f"invalid policy JSON: {exc}")

    for kind, enabled, instruction, skill_base in (
        ("claude", target in ("claude", "both"), "CLAUDE.md", project / ".claude" / "skills"),
        ("codex", target in ("codex", "both"), "AGENTS.md", project / ".agents" / "skills"),
    ):
        if not enabled: continue
        f = project / instruction
        text = f.read_text(encoding="utf-8") if f.exists() else ""
        if BEGIN not in text or END not in text: errors.append(f"{instruction} managed block missing")
        for suffix in SKILLS:
            if not (skill_base / f"employ-minds-{suffix}" / "SKILL.md").exists(): errors.append(f"{kind}: missing skill employ-minds-{suffix}")
        if kind == "claude":
            if not (project / ".claude" / "commands" / "employ-minds.md").exists(): errors.append("claude: missing /employ-minds command")
            for name in AGENTS:
                if not (project / ".claude" / "agents" / f"em-{name}.md").exists(): errors.append(f"claude: missing native agent em-{name}")
        else:
            for name in AGENTS:
                if not (project / ".codex" / "agents" / f"em-{name}.toml").exists(): errors.append(f"codex: missing native agent em-{name}")
    return errors


def self_check(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        policy = json.loads((root / "config" / "employ-minds-policy.json").read_text(encoding="utf-8"))
        if policy.get("schema_version") != 2: errors.append("policy schema_version must be 2")
        if policy.get("default_profile") != "standard": errors.append("policy default_profile must be standard")
        if not policy.get("completion_requires_fresh_evidence"): errors.append("policy must require fresh evidence")
        if not policy.get("native_agent_separation"): errors.append("policy must require native-agent separation")
        if policy.get("review_order", [None])[0] != "spec_compliance": errors.append("spec compliance must precede quality review")
    except Exception as exc:
        errors.append(f"policy: {exc}")
    for suffix in SKILLS:
        path = root / "skills" / f"employ-minds-{suffix}" / "SKILL.md"
        if not path.exists(): errors.append(f"missing source skill employ-minds-{suffix}")
        elif f"name: employ-minds-{suffix}" not in path.read_text(encoding="utf-8"): errors.append(f"skill frontmatter mismatch: employ-minds-{suffix}")
    for name in AGENTS:
        if not (root / "agents" / f"{name}.md").exists(): errors.append(f"missing canonical agent {name}")
        if not (root / "native" / "claude" / "agents" / f"em-{name}.md").exists(): errors.append(f"missing Claude native agent em-{name}")
        if not (root / "native" / "codex" / "agents" / f"em-{name}.toml").exists(): errors.append(f"missing Codex native agent em-{name}")
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
