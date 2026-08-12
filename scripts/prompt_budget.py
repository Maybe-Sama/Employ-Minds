#!/usr/bin/env python3
"""Guard canonical prompt surface against accidental instruction bloat.

Word counts are a stable cross-model proxy, not a claim about tokenizer-exact cost.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def metrics(root: Path = ROOT) -> dict[str, int]:
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    skill_counts = {p.parent.name: words(p.read_text(encoding="utf-8")) for p in skill_files}
    manifest = json.loads((root / "agents/manifest.json").read_text(encoding="utf-8"))
    agent_counts = {
        name: words(spec["description"] + " " + spec["instructions"])
        for name, spec in manifest["agents"].items()
    }
    return {
        "core_words": words((root / "rules/core.md").read_text(encoding="utf-8")),
        "router_words": skill_counts.get("employ-minds-router", 0),
        "single_skill_words": max(skill_counts.values(), default=0),
        "all_skills_words": sum(skill_counts.values()),
        "single_agent_instruction_words": max(agent_counts.values(), default=0),
        "all_agent_contract_words": sum(agent_counts.values()),
    }


def check(root: Path = ROOT) -> list[str]:
    cfg = json.loads((root / "config/prompt-budget.json").read_text(encoding="utf-8"))
    actual = metrics(root)
    errors = []
    for key, limit in cfg["limits"].items():
        value = actual[key]
        if value > limit:
            errors.append(f"{key}: {value} > budget {limit}")
    return errors


def main() -> int:
    actual = metrics()
    errors = check()
    for key, value in actual.items():
        print(f"{key}: {value}")
    if errors:
        print("Prompt budget: FAIL")
        for error in errors: print(" -", error)
        return 1
    print("Prompt budget: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
