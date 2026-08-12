#!/usr/bin/env python3
"""Deterministic conformance checks for the risk router. Not an LLM benchmark."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def classify(case: dict, policy: dict) -> str:
    flags = set(case.get("flags", []))
    uncertainty = set(case.get("uncertainty", []))
    critical = set(policy["critical_triggers"])
    upgrades = set(policy["uncertainty_upgrade_triggers"])
    if flags & critical:
        return "critical"
    base = "standard" if flags else "fast"
    if uncertainty & upgrades:
        return {"fast": "standard", "standard": "critical"}[base]
    return base


def main() -> int:
    policy = json.loads((ROOT / "config/employ-minds-policy.json").read_text())
    cases = json.loads((ROOT / "evals/router-cases.json").read_text())
    failures = []
    for case in cases:
        actual = classify(case, policy)
        if actual != case["expected"]:
            failures.append(f'{case["id"]}: expected {case["expected"]}, got {actual}')
    if failures:
        print("Router conformance: FAIL")
        for failure in failures: print(" -", failure)
        return 1
    print(f"Router conformance: OK ({len(cases)} cases)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
