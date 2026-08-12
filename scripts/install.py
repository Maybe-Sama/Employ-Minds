#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

BEGIN = "<!-- EMPLOY-MINDS:BEGIN -->"
END = "<!-- EMPLOY-MINDS:END -->"
NAMESPACE = "employ-minds-"

CLAUDE_BLOCK = f"""{BEGIN}
## Employ-Minds
For non-trivial coding, debugging, refactoring, migration, review, integration, or implementation work, first read `.claude/skills/employ-minds-router/SKILL.md`. Route the task as FAST/STANDARD/CRITICAL, escalate when new risk appears, and never claim completion without fresh evidence matching the important claims. Preserve project-specific instructions outside this block.
{END}"""

CODEX_BLOCK = f"""{BEGIN}
## Employ-Minds
For non-trivial coding, debugging, refactoring, migration, review, integration, or implementation work, first read `.agents/skills/employ-minds-router/SKILL.md`. Route the task as FAST/STANDARD/CRITICAL, escalate when new risk appears, and never claim completion without fresh evidence matching the important claims. Preserve project-specific instructions outside this block.
{END}"""


def replace_block(text: str, block: str) -> str:
    """Add or replace our managed block while preserving all surrounding text."""
    if BEGIN in text and END in text:
        start = text.index(BEGIN)
        stop = text.index(END, start) + len(END)
        before = text[:start].rstrip()
        after = text[stop:].lstrip()
        pieces = [p for p in (before, block, after) if p]
        return "\n\n".join(pieces).rstrip() + "\n"
    base = text.rstrip()
    return ((base + "\n\n") if base else "") + block + "\n"


def remove_block(text: str) -> str:
    """Remove only our managed block."""
    if BEGIN not in text or END not in text:
        return text
    start = text.index(BEGIN)
    stop = text.index(END, start) + len(END)
    before = text[:start].rstrip()
    after = text[stop:].lstrip()
    out = "\n\n".join(p for p in (before, after) if p).strip()
    return (out + "\n") if out else ""


def write_managed(path: Path, block: str, backup_dir: Path) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if path.exists() and BEGIN not in old:
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup = backup_dir / f"{path.name}.pre-employ-minds"
        if not backup.exists():
            shutil.copy2(path, backup)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(replace_block(old, block), encoding="utf-8")


def _replace_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def _install_skills(src: Path, base: Path) -> None:
    base.mkdir(parents=True, exist_ok=True)
    for old in base.glob(f"{NAMESPACE}*"):
        if old.is_dir():
            shutil.rmtree(old)
    for skill in sorted((src / "skills").iterdir()):
        if skill.is_dir() and skill.name.startswith(NAMESPACE):
            shutil.copytree(skill, base / skill.name)


def copy_payload(src: Path, project: Path, target: str) -> None:
    payload = project / ".employ-minds"
    payload.mkdir(parents=True, exist_ok=True)

    for rel in ("config", "agents", "rules"):
        _replace_tree(src / rel, payload / rel)
    for filename in ("VERSION", "NOTICE.md", "LICENSE"):
        shutil.copy2(src / filename, payload / filename)

    if target in ("claude", "both"):
        _install_skills(src, project / ".claude" / "skills")
        commands = project / ".claude" / "commands"
        commands.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / "commands" / "employ-minds.md", commands / "employ-minds.md")

    if target in ("codex", "both"):
        _install_skills(src, project / ".agents" / "skills")

    backup_dir = payload / "backups"
    if target in ("claude", "both"):
        write_managed(project / "CLAUDE.md", CLAUDE_BLOCK, backup_dir)
    if target in ("codex", "both"):
        write_managed(project / "AGENTS.md", CODEX_BLOCK, backup_dir)

    state = {
        "name": "employ-minds",
        "version": (src / "VERSION").read_text(encoding="utf-8").strip(),
        "last_install_target": target,
    }
    (payload / "install-state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def _remove_namespaced_skills(base: Path) -> None:
    if not base.exists():
        return
    for path in base.glob(f"{NAMESPACE}*"):
        if path.is_dir():
            shutil.rmtree(path)


def uninstall(project: Path, target: str) -> None:
    if target in ("claude", "both"):
        instructions = project / "CLAUDE.md"
        if instructions.exists():
            instructions.write_text(remove_block(instructions.read_text(encoding="utf-8")), encoding="utf-8")
        _remove_namespaced_skills(project / ".claude" / "skills")
        command = project / ".claude" / "commands" / "employ-minds.md"
        if command.exists():
            command.unlink()

    if target in ("codex", "both"):
        instructions = project / "AGENTS.md"
        if instructions.exists():
            instructions.write_text(remove_block(instructions.read_text(encoding="utf-8")), encoding="utf-8")
        _remove_namespaced_skills(project / ".agents" / "skills")

    payload = project / ".employ-minds"
    claude_active = (project / "CLAUDE.md").exists() and BEGIN in (project / "CLAUDE.md").read_text(encoding="utf-8")
    codex_active = (project / "AGENTS.md").exists() and BEGIN in (project / "AGENTS.md").read_text(encoding="utf-8")
    if payload.exists() and not claude_active and not codex_active:
        shutil.rmtree(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Employ-Minds without overwriting existing project instructions.")
    parser.add_argument("--project", default=".", help="Target project path")
    parser.add_argument("--target", choices=["claude", "codex", "both"], default="both")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()

    src = Path(__file__).resolve().parent.parent
    project = Path(args.project).expanduser().resolve()
    project.mkdir(parents=True, exist_ok=True)

    if args.uninstall:
        uninstall(project, args.target)
        print(f"Employ-Minds removed from {project} ({args.target}).")
        return 0

    copy_payload(src, project, args.target)
    version = (src / "VERSION").read_text(encoding="utf-8").strip()
    print(f"Employ-Minds {version} installed in {project} ({args.target}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
