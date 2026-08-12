#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

BEGIN = "<!-- EMPLOY-MINDS:BEGIN -->"
END = "<!-- EMPLOY-MINDS:END -->"
REQUIRED_SKILLS = [
    "router", "brainstorm", "plan", "tdd", "debug", "execute", "review",
    "verify", "security", "parallel", "research", "context", "release",
]
REQUIRED_AGENTS = [
    "orchestrator", "architect", "researcher", "debugger", "implementer",
    "spec-reviewer", "quality-reviewer", "security-reviewer", "verifier",
]


def check_project(project: Path, target: str) -> list[str]:
    errors: list[str] = []
    payload = project / ".employ-minds"
    for rel in ("VERSION", "config/employ-minds-policy.json", "rules/core.md", "install-state.json"):
        if not (payload / rel).exists():
            errors.append(f"missing .employ-minds/{rel}")

    policy_path = payload / "config" / "employ-minds-policy.json"
    if policy_path.exists():
        try:
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            if policy.get("default_profile") != "standard":
                errors.append("unexpected default profile")
            if not policy.get("completion_requires_fresh_evidence"):
                errors.append("fresh-evidence invariant disabled")
        except Exception as exc:
            errors.append(f"invalid policy JSON: {exc}")

    configs = [
        ("claude", target in ("claude", "both"), "CLAUDE.md", project / ".claude" / "skills"),
        ("codex", target in ("codex", "both"), "AGENTS.md", project / ".agents" / "skills"),
    ]
    for kind, enabled, instruction_name, skill_base in configs:
        if not enabled:
            continue
        instruction = project / instruction_name
        text = instruction.read_text(encoding="utf-8") if instruction.exists() else ""
        if BEGIN not in text or END not in text:
            errors.append(f"{instruction_name} managed block missing")
        for suffix in REQUIRED_SKILLS:
            if not (skill_base / f"employ-minds-{suffix}" / "SKILL.md").exists():
                errors.append(f"{kind}: missing skill employ-minds-{suffix}")
        if kind == "claude" and not (project / ".claude" / "commands" / "employ-minds.md").exists():
            errors.append("claude: missing /employ-minds command")
    return errors


def self_check(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        policy = json.loads((root / "config" / "employ-minds-policy.json").read_text(encoding="utf-8"))
        if policy.get("schema_version") != 1:
            errors.append("policy schema_version must be 1")
        if policy.get("default_profile") != "standard":
            errors.append("policy default_profile must be standard")
        if not policy.get("completion_requires_fresh_evidence"):
            errors.append("policy must require fresh evidence")
        if policy.get("review_order", [None])[0] != "spec_compliance":
            errors.append("spec compliance must precede quality review")
    except Exception as exc:
        errors.append(f"policy: {exc}")

    for suffix in REQUIRED_SKILLS:
        path = root / "skills" / f"employ-minds-{suffix}" / "SKILL.md"
        if not path.exists():
            errors.append(f"missing source skill employ-minds-{suffix}")
        elif f"name: employ-minds-{suffix}" not in path.read_text(encoding="utf-8"):
            errors.append(f"skill frontmatter mismatch: employ-minds-{suffix}")

    for name in REQUIRED_AGENTS:
        if not (root / "agents" / f"{name}.md").exists():
            errors.append(f"missing agent {name}")

    required_files = (
        "LICENSE", "NOTICE.md", "VERSION", "README.md", "CHANGELOG.md",
        "scripts/install.py", "scripts/doctor.py", "docs/ARCHITECTURE.md",
        "commands/employ-minds.md", "UPSTREAMS.lock.json",
    )
    for rel in required_files:
        if not (root / rel).exists():
            errors.append(f"missing {rel}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Employ-Minds source and project installations.")
    parser.add_argument("--project")
    parser.add_argument("--target", choices=["claude", "codex", "both"], default="both")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    if args.self_check:
        errors.extend(self_check(root))
    if args.project:
        errors.extend(check_project(Path(args.project).expanduser().resolve(), args.target))
    if not args.self_check and not args.project:
        parser.error("use --self-check and/or --project")

    if errors:
        print("Employ-Minds doctor: FAIL")
        for error in errors:
            print(" -", error)
        return 1
    print("Employ-Minds doctor: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
