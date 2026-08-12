# Quickstart

## 1. Clone Employ-Minds

```bash
git clone https://github.com/Maybe-Sama/Employ-Minds.git
cd Employ-Minds
```

## 2. Install into a project

macOS/Linux:

```bash
./scripts/install.sh --project ../my-project --target both
```

Windows PowerShell:

```powershell
.\scripts\install.ps1 --project ..\my-project --target both
```

## 3. Verify

```bash
python scripts/doctor.py --project ../my-project --target both
```

Expected result:

```text
Employ-Minds doctor: OK
```

## 4. Work normally

Open Claude Code or Codex in the target project and describe the engineering task. The project instructions route non-trivial work automatically.

For explicit routing, say:

```text
Use Employ-Minds. Classify this task before editing and finish only after the profile-required gates have fresh evidence.
```

## 5. Remove it safely

```bash
./scripts/uninstall.sh --project ../my-project --target both
```

Your pre-existing `CLAUDE.md` / `AGENTS.md` content remains untouched.
