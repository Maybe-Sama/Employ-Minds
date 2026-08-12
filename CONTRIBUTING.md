# Contributing

Employ-Minds should become stricter **only where risk justifies it**. Contributions that turn every task into a heavyweight ceremony are regressions just as much as changes that weaken safety gates.

## Before changing behavior

1. Read `docs/ARCHITECTURE.md` and `skills/employ-minds-router/SKILL.md`.
2. Identify which profile/gate is affected.
3. Add or update a focused test when installer/doctor behavior changes.
4. Keep Claude and Codex integration semantically equivalent unless a harness genuinely requires a different adapter.
5. Preserve user-owned `CLAUDE.md` and `AGENTS.md` content.

## Required checks

```bash
python -m unittest discover -s tests -v
python scripts/doctor.py --self-check
python -m compileall -q scripts tests
```

On Bash-capable systems:

```bash
bash -n scripts/install.sh scripts/uninstall.sh
```

## Pull requests

Describe the risk profile of the change, the behavioral invariant affected, and the exact verification evidence. Avoid unrelated cleanup in the same change unless it is required to make the change safe.
