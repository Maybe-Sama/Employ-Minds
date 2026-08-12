import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

install_spec = importlib.util.spec_from_file_location("em_install", ROOT / "scripts" / "install.py")
install = importlib.util.module_from_spec(install_spec)
assert install_spec.loader is not None
install_spec.loader.exec_module(install)

doctor_spec = importlib.util.spec_from_file_location("em_doctor", ROOT / "scripts" / "doctor.py")
doctor = importlib.util.module_from_spec(doctor_spec)
assert doctor_spec.loader is not None
doctor_spec.loader.exec_module(doctor)


class EmployMindsTests(unittest.TestCase):
    def test_policy_and_source_layout(self):
        policy = json.loads((ROOT / "config" / "employ-minds-policy.json").read_text(encoding="utf-8"))
        self.assertEqual(policy["default_profile"], "standard")
        self.assertTrue(policy["completion_requires_fresh_evidence"])
        self.assertEqual(policy["review_order"][0], "spec_compliance")
        self.assertEqual(doctor.self_check(ROOT), [])

    def test_managed_block_is_idempotent_and_preserves_user_content(self):
        original = "# Existing instructions\nDo not touch this.\n"
        once = install.replace_block(original, install.CLAUDE_BLOCK)
        twice = install.replace_block(once, install.CLAUDE_BLOCK)
        self.assertEqual(once, twice)
        self.assertIn("Do not touch this.", twice)
        self.assertEqual(twice.count(install.BEGIN), 1)
        removed = install.remove_block(twice)
        self.assertIn("Do not touch this.", removed)
        self.assertNotIn(install.BEGIN, removed)

    def test_install_both_is_valid_and_uninstall_preserves_user_instructions(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            (project / "CLAUDE.md").write_text("# Mine\n", encoding="utf-8")
            (project / "AGENTS.md").write_text("# Also mine\n", encoding="utf-8")

            install.copy_payload(ROOT, project, "both")
            self.assertEqual(doctor.check_project(project, "both"), [])
            self.assertTrue((project / ".claude/skills/employ-minds-router/SKILL.md").exists())
            self.assertTrue((project / ".agents/skills/employ-minds-router/SKILL.md").exists())
            self.assertTrue((project / ".claude/commands/employ-minds.md").exists())
            self.assertIn("# Mine", (project / "CLAUDE.md").read_text(encoding="utf-8"))
            self.assertIn("# Also mine", (project / "AGENTS.md").read_text(encoding="utf-8"))

            install.copy_payload(ROOT, project, "both")
            self.assertEqual((project / "CLAUDE.md").read_text(encoding="utf-8").count(install.BEGIN), 1)
            self.assertEqual((project / "AGENTS.md").read_text(encoding="utf-8").count(install.BEGIN), 1)

            install.uninstall(project, "both")
            self.assertFalse((project / ".employ-minds").exists())
            self.assertNotIn(install.BEGIN, (project / "CLAUDE.md").read_text(encoding="utf-8"))
            self.assertNotIn(install.BEGIN, (project / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertIn("# Mine", (project / "CLAUDE.md").read_text(encoding="utf-8"))
            self.assertIn("# Also mine", (project / "AGENTS.md").read_text(encoding="utf-8"))

    def test_partial_uninstall_keeps_other_target_and_shared_payload(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            install.copy_payload(ROOT, project, "both")
            install.uninstall(project, "claude")
            self.assertTrue((project / ".employ-minds").exists())
            self.assertFalse((project / ".claude/skills/employ-minds-router").exists())
            self.assertTrue((project / ".agents/skills/employ-minds-router/SKILL.md").exists())
            self.assertIn(install.BEGIN, (project / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertEqual(doctor.check_project(project, "codex"), [])
            install.uninstall(project, "codex")
            self.assertFalse((project / ".employ-minds").exists())

    def test_first_install_backup_is_created_once(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            original = "# Personal rules\nNever delete this.\n"
            (project / "CLAUDE.md").write_text(original, encoding="utf-8")
            install.copy_payload(ROOT, project, "claude")
            backup = project / ".employ-minds/backups/CLAUDE.md.pre-employ-minds"
            self.assertEqual(backup.read_text(encoding="utf-8"), original)
            backup.write_text("sentinel\n", encoding="utf-8")
            install.copy_payload(ROOT, project, "claude")
            self.assertEqual(backup.read_text(encoding="utf-8"), "sentinel\n")

    def test_unrelated_skills_survive_install_and_uninstall(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            unrelated = project / ".claude/skills/my-own-skill"
            unrelated.mkdir(parents=True)
            (unrelated / "SKILL.md").write_text("mine\n", encoding="utf-8")
            install.copy_payload(ROOT, project, "claude")
            self.assertTrue(unrelated.exists())
            install.uninstall(project, "claude")
            self.assertTrue(unrelated.exists())
            self.assertEqual((unrelated / "SKILL.md").read_text(encoding="utf-8"), "mine\n")


if __name__ == "__main__":
    unittest.main()
