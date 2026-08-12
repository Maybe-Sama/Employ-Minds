#!/usr/bin/env python3
"""Render harness-native agent adapters from one canonical manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "agents" / "manifest.json"


def load_manifest() -> dict:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("agents"), dict):
        raise ValueError("invalid agents/manifest.json")
    return data


def claude_text(name: str, spec: dict) -> str:
    c = spec["claude"]
    lines = ["---", f"name: em-{name}", f"description: {spec['description']}"]
    if c.get("tools"):
        lines.append("tools: " + ", ".join(c["tools"]))
    if c.get("model"):
        lines.append(f"model: {c['model']}")
    if c.get("permissionMode"):
        lines.append(f"permissionMode: {c['permissionMode']}")
    if c.get("maxTurns") is not None:
        lines.append(f"maxTurns: {c['maxTurns']}")
    lines.extend(["---", spec["instructions"], ""])
    return "\n".join(lines)


def codex_text(name: str, spec: dict) -> str:
    sandbox = spec["codex"]["sandbox_mode"]
    instructions = spec["instructions"].replace('"""', '\"\"\"')
    return (
        f'name = "em-{name}"\n'
        f'description = {json.dumps(spec["description"])}\n'
        f'sandbox_mode = "{sandbox}"\n'
        'developer_instructions = """\n'
        f'{instructions}\n'
        '"""\n'
    )


def expected_files() -> dict[Path, str]:
    out = {}
    for name, spec in load_manifest()["agents"].items():
        out[ROOT / "native" / "claude" / "agents" / f"em-{name}.md"] = claude_text(name, spec)
        out[ROOT / "native" / "codex" / "agents" / f"em-{name}.toml"] = codex_text(name, spec)
    return out


def check() -> list[str]:
    errors = []
    for path, expected in expected_files().items():
        if not path.exists():
            errors.append(f"missing generated adapter: {path.relative_to(ROOT)}")
        elif path.read_text(encoding="utf-8") != expected:
            errors.append(f"generated adapter drift: {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    p = argparse.ArgumentParser()
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = p.parse_args()
    files = expected_files()
    if args.write:
        for path, text in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        print(f"Rendered {len(files)} native agent adapters.")
        return 0
    errors = check()
    if errors:
        print("Native agent parity: FAIL")
        for error in errors: print(" -", error)
        return 1
    print(f"Native agent parity: OK ({len(files)} adapters)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
