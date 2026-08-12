#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

BEGIN = "<!-- EMPLOY-MINDS:BEGIN -->"
END = "<!-- EMPLOY-MINDS:END -->"
SKILL_PREFIX = "employ-minds-"
AGENT_PREFIX = "em-"

CLAUDE_BLOCK = f"""{BEGIN}
## Employ-Minds
For non-trivial engineering work, route through `employ-minds-router`. Use native
Employ-Minds subagents when their role matches the work. Keep the primary context
lean: delegate noisy exploration/research, separate writing from review, escalate
risk when evidence changes, and never claim completion without fresh evidence.
{END}"""

CODEX_BLOCK = f"""{BEGIN}
## Employ-Minds
For non-trivial engineering work, route through `employ-minds-router`. Use project
subagents in `.codex/agents/` when their role matches the work. Keep the primary
context lean, separate writing from review, and require fresh evidence for claims.
{END}"""


def replace_block(text: str, block: str) -> str:
    if BEGIN in text and END in text:
        start = text.index(BEGIN)
        stop = text.index(END, start) + len(END)
        before, after = text[:start].rstrip(), text[stop:].lstrip()
        return "\n\n".join(p for p in (before, block, after) if p).rstrip() + "\n"
    base = text.rstrip()
    return ((base + "\n\n") if base else "") + block + "\n"


def remove_block(text: str) -> str:
    if BEGIN not in text or END not in text:
        return text
    start = text.index(BEGIN)
    stop = text.index(END, start) + len(END)
    before, after = text[:start].rstrip(), text[stop:].lstrip()
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


def replace_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def install_namespaced(src: Path, dst: Path, prefix: str) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for old in dst.glob(f"{prefix}*"):
        if old.is_dir():
            shutil.rmtree(old)
        else:
            old.unlink()
    for item in sorted(src.iterdir()):
        if not item.name.startswith(prefix):
            continue
        target = dst / item.name
        shutil.copytree(item, target) if item.is_dir() else shutil.copy2(item, target)


def remove_namespaced(dst: Path, prefix: str) -> None:
    if not dst.exists():
        return
    for item in dst.glob(f"{prefix}*"):
        shutil.rmtree(item) if item.is_dir() else item.unlink()


def copy_payload(src: Path, project: Path, target: str) -> None:
    payload = project / ".employ-minds"
    payload.mkdir(parents=True, exist_ok=True)
    for rel in ("config", "agents", "rules"):
        replace_tree(src / rel, payload / rel)
    for filename in ("VERSION", "NOTICE.md", "LICENSE"):
        shutil.copy2(src / filename, payload / filename)

    if target in ("claude", "both"):
        install_namespaced(src / "skills", project / ".claude" / "skills", SKILL_PREFIX)
        install_namespaced(src / "native" / "claude" / "agents", project / ".claude" / "agents", AGENT_PREFIX)
        commands = project / ".claude" / "commands"
        commands.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / "commands" / "employ-minds.md", commands / "employ-minds.md")

    if target in ("codex", "both"):
        install_namespaced(src / "skills", project / ".agents" / "skills", SKILL_PREFIX)
        install_namespaced(src / "native" / "codex" / "agents", project / ".codex" / "agents", AGENT_PREFIX)

    backups = payload / "backups"
    if target in ("claude", "both"):
        write_managed(project / "CLAUDE.md", CLAUDE_BLOCK, backups)
    if target in ("codex", "both"):
        write_managed(project / "AGENTS.md", CODEX_BLOCK, backups)

    state = {
        "name": "employ-minds",
        "version": (src / "VERSION").read_text(encoding="utf-8").strip(),
        "last_install_target": target,
        "native_agents": True,
    }
    (payload / "install-state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def uninstall(project: Path, target: str) -> None:
    if target in ("claude", "both"):
        f = project / "CLAUDE.md"
        if f.exists():
            f.write_text(remove_block(f.read_text(encoding="utf-8")), encoding="utf-8")
        remove_namespaced(project / ".claude" / "skills", SKILL_PREFIX)
        remove_namespaced(project / ".claude" / "agents", AGENT_PREFIX)
        command = project / ".claude" / "commands" / "employ-minds.md"
        if command.exists():
            command.unlink()

    if target in ("codex", "both"):
        f = project / "AGENTS.md"
        if f.exists():
            f.write_text(remove_block(f.read_text(encoding="utf-8")), encoding="utf-8")
        remove_namespaced(project / ".agents" / "skills", SKILL_PREFIX)
        remove_namespaced(project / ".codex" / "agents", AGENT_PREFIX)

    payload = project / ".employ-minds"
    claude_active = (project / "CLAUDE.md").exists() and BEGIN in (project / "CLAUDE.md").read_text(encoding="utf-8")
    codex_active = (project / "AGENTS.md").exists() and BEGIN in (project / "AGENTS.md").read_text(encoding="utf-8")
    if payload.exists() and not claude_active and not codex_active:
        shutil.rmtree(payload)


def main() -> int:
    p = argparse.ArgumentParser(description="Install Employ-Minds without overwriting project instructions.")
    p.add_argument("--project", default=".")
    p.add_argument("--target", choices=["claude", "codex", "both"], default="both")
    p.add_argument("--uninstall", action="store_true")
    args = p.parse_args()
    src = Path(__file__).resolve().parent.parent
    project = Path(args.project).expanduser().resolve()
    project.mkdir(parents=True, exist_ok=True)
    if args.uninstall:
        uninstall(project, args.target)
        print(f"Employ-Minds removed from {project} ({args.target}).")
    else:
        copy_payload(src, project, args.target)
        version = (src / "VERSION").read_text(encoding="utf-8").strip()
        print(f"Employ-Minds {version} installed in {project} ({args.target}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
