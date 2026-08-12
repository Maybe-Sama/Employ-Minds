#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

BEGIN = "<!-- EMPLOY-MINDS:BEGIN -->"
END = "<!-- EMPLOY-MINDS:END -->"
SKILL_PREFIX = "employ-minds-"
LEGACY_V1_SKILLS = [
    f"{SKILL_PREFIX}{name}" for name in (
        "router", "brainstorm", "plan", "tdd", "debug", "execute", "review",
        "verify", "security", "parallel", "research", "context", "release",
    )
]

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


def read_state(payload: Path) -> dict:
    path = payload / "install-state.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) and data.get("name") == "employ-minds" else {}
    except (OSError, json.JSONDecodeError):
        return {}


def source_file_names(src: Path) -> list[str]:
    return sorted(p.name for p in src.iterdir() if p.is_file())


def source_dir_names(src: Path, prefix: str) -> list[str]:
    return sorted(p.name for p in src.iterdir() if p.is_dir() and p.name.startswith(prefix))


def legacy_owned_skills(state: dict, src: Path, key: str) -> list[str]:
    if key in state:
        return [Path(name).name for name in state.get(key, [])]
    version = str(state.get("version", ""))
    if version.startswith("1."):
        return LEGACY_V1_SKILLS.copy()
    if version.startswith("2."):
        return source_dir_names(src, SKILL_PREFIX)
    return []


def prior_owned(state: dict, key: str) -> list[str]:
    return [Path(name).name for name in state.get(key, [])]


def collision_paths(src: Path, project: Path, target: str, state: dict) -> list[Path]:
    """Return paths this install would overwrite without prior ownership."""
    collisions: list[Path] = []

    def check_files(source: Path, dest: Path, owned: list[str]) -> None:
        owned_set = set(owned)
        for name in source_file_names(source):
            path = dest / name
            if path.exists() and name not in owned_set:
                collisions.append(path)

    def check_dirs(source: Path, dest: Path, owned: list[str]) -> None:
        owned_set = set(owned)
        for name in source_dir_names(source, SKILL_PREFIX):
            path = dest / name
            if path.exists() and name not in owned_set:
                collisions.append(path)

    if target in ("claude", "both"):
        check_dirs(
            src / "skills", project / ".claude/skills",
            legacy_owned_skills(state, src / "skills", "claude_skills"),
        )
        check_files(
            src / "native/claude/agents", project / ".claude/agents",
            prior_owned(state, "claude_agents"),
        )
        command = project / ".claude/commands/employ-minds.md"
        command_owned = state.get("claude_command") == "employ-minds.md" or bool(state and str(state.get("version", "")).startswith(("1.", "2.")))
        if command.exists() and not command_owned:
            collisions.append(command)

    if target in ("codex", "both"):
        check_dirs(
            src / "skills", project / ".agents/skills",
            legacy_owned_skills(state, src / "skills", "codex_skills"),
        )
        check_files(
            src / "native/codex/agents", project / ".codex/agents",
            prior_owned(state, "codex_agents"),
        )
    return collisions


def preflight(src: Path, project: Path, target: str, state: dict) -> None:
    collisions = collision_paths(src, project, target, state)
    if collisions:
        rendered = "\n".join(f" - {p}" for p in collisions)
        raise RuntimeError(
            "Employ-Minds refused to overwrite unowned project paths. "
            "Move/rename them or explicitly remove them before installing:\n" + rendered
        )


def install_owned_files(src: Path, dst: Path, previous: list[str]) -> list[str]:
    dst.mkdir(parents=True, exist_ok=True)
    for name in previous:
        old = dst / Path(name).name
        if old.is_file() or old.is_symlink():
            old.unlink()
    names = source_file_names(src)
    for name in names:
        shutil.copy2(src / name, dst / name)
    return names


def install_owned_dirs(src: Path, dst: Path, previous: list[str]) -> list[str]:
    dst.mkdir(parents=True, exist_ok=True)
    for name in previous:
        old = dst / Path(name).name
        if old.is_dir():
            shutil.rmtree(old)
    names = source_dir_names(src, SKILL_PREFIX)
    for name in names:
        shutil.copytree(src / name, dst / name)
    return names


def remove_owned_files(dst: Path, names: list[str]) -> None:
    if not dst.exists():
        return
    for name in names:
        path = dst / Path(name).name
        if path.is_file() or path.is_symlink():
            path.unlink()


def remove_owned_dirs(dst: Path, names: list[str]) -> None:
    if not dst.exists():
        return
    for name in names:
        path = dst / Path(name).name
        if path.is_dir():
            shutil.rmtree(path)


def copy_payload(src: Path, project: Path, target: str) -> None:
    payload = project / ".employ-minds"
    previous_state = read_state(payload)
    preflight(src, project, target, previous_state)  # Must happen before any mutation.

    payload.mkdir(parents=True, exist_ok=True)
    for rel in ("config", "agents", "rules"):
        replace_tree(src / rel, payload / rel)
    for filename in ("VERSION", "NOTICE.md", "LICENSE"):
        shutil.copy2(src / filename, payload / filename)

    claude_skills = legacy_owned_skills(previous_state, src / "skills", "claude_skills")
    codex_skills = legacy_owned_skills(previous_state, src / "skills", "codex_skills")
    claude_agents = prior_owned(previous_state, "claude_agents")
    codex_agents = prior_owned(previous_state, "codex_agents")
    claude_command = previous_state.get("claude_command")

    if target in ("claude", "both"):
        claude_skills = install_owned_dirs(src / "skills", project / ".claude/skills", claude_skills)
        claude_agents = install_owned_files(src / "native/claude/agents", project / ".claude/agents", claude_agents)
        commands = project / ".claude/commands"
        commands.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / "commands/employ-minds.md", commands / "employ-minds.md")
        claude_command = "employ-minds.md"

    if target in ("codex", "both"):
        codex_skills = install_owned_dirs(src / "skills", project / ".agents/skills", codex_skills)
        codex_agents = install_owned_files(src / "native/codex/agents", project / ".codex/agents", codex_agents)

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
        "claude_skills": claude_skills,
        "codex_skills": codex_skills,
        "claude_agents": claude_agents,
        "codex_agents": codex_agents,
        "claude_command": claude_command,
    }
    (payload / "install-state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def uninstall(project: Path, target: str) -> None:
    payload = project / ".employ-minds"
    state = read_state(payload)

    if target in ("claude", "both"):
        f = project / "CLAUDE.md"
        if f.exists():
            f.write_text(remove_block(f.read_text(encoding="utf-8")), encoding="utf-8")
        remove_owned_dirs(project / ".claude/skills", prior_owned(state, "claude_skills") or LEGACY_V1_SKILLS)
        remove_owned_files(project / ".claude/agents", prior_owned(state, "claude_agents"))
        if state.get("claude_command") == "employ-minds.md" or str(state.get("version", "")).startswith("1."):
            command = project / ".claude/commands/employ-minds.md"
            if command.exists():
                command.unlink()
        state["claude_skills"] = []
        state["claude_agents"] = []
        state["claude_command"] = None

    if target in ("codex", "both"):
        f = project / "AGENTS.md"
        if f.exists():
            f.write_text(remove_block(f.read_text(encoding="utf-8")), encoding="utf-8")
        remove_owned_dirs(project / ".agents/skills", prior_owned(state, "codex_skills") or LEGACY_V1_SKILLS)
        remove_owned_files(project / ".codex/agents", prior_owned(state, "codex_agents"))
        state["codex_skills"] = []
        state["codex_agents"] = []

    claude_active = (project / "CLAUDE.md").exists() and BEGIN in (project / "CLAUDE.md").read_text(encoding="utf-8")
    codex_active = (project / "AGENTS.md").exists() and BEGIN in (project / "AGENTS.md").read_text(encoding="utf-8")
    if payload.exists() and not claude_active and not codex_active:
        shutil.rmtree(payload)
    elif payload.exists():
        (payload / "install-state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description="Install Employ-Minds without overwriting project-owned instructions, skills, or agents.")
    p.add_argument("--project", default=".")
    p.add_argument("--target", choices=["claude", "codex", "both"], default="both")
    p.add_argument("--uninstall", action="store_true")
    args = p.parse_args()
    src = Path(__file__).resolve().parent.parent
    project = Path(args.project).expanduser().resolve()
    project.mkdir(parents=True, exist_ok=True)
    try:
        if args.uninstall:
            uninstall(project, args.target)
            print(f"Employ-Minds removed from {project} ({args.target}).")
        else:
            copy_payload(src, project, args.target)
            version = (src / "VERSION").read_text(encoding="utf-8").strip()
            print(f"Employ-Minds {version} installed in {project} ({args.target}).")
    except RuntimeError as exc:
        print(f"Employ-Minds install aborted:\n{exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
