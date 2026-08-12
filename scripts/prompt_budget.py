#!/usr/bin/env python3
"""Guard both startup and on-demand prompt surfaces against accidental bloat.

Counts are stable cross-model proxies, not tokenizer-exact cost claims. Startup
metadata is tracked separately because skill/agent bodies are progressively loaded.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def skill_description(text: str) -> str:
    match = re.search(r"(?m)^description:\s*(.+?)\s*$", text)
    return match.group(1).strip().strip('"\'') if match else ""


def load_install_module(root: Path):
    path = root / "scripts/install.py"
    spec = importlib.util.spec_from_file_location("employ_minds_budget_install", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def metrics(root: Path = ROOT) -> dict[str, int]:
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    skill_text = {p.parent.name: p.read_text(encoding="utf-8") for p in skill_files}
    skill_counts = {name: words(text) for name, text in skill_text.items()}
    skill_description_chars = sum(len(skill_description(text)) for text in skill_text.values())

    manifest = json.loads((root / "agents/manifest.json").read_text(encoding="utf-8"))
    agent_counts = {
        name: words(spec["description"] + " " + spec["instructions"])
        for name, spec in manifest["agents"].items()
    }
    agent_description_chars = sum(len(spec["description"]) for spec in manifest["agents"].values())

    install = load_install_module(root)
    managed_instruction_words = max(words(install.CLAUDE_BLOCK), words(install.CODEX_BLOCK))

    return {
        "managed_instruction_words": managed_instruction_words,
        "skill_description_chars": skill_description_chars,
        "agent_description_chars": agent_description_chars,
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
        for error in errors:
            print(" -", error)
        return 1
    print("Prompt budget: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
