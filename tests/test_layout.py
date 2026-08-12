import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

install = load("em_install", ROOT / "scripts" / "install.py")
doctor = load("em_doctor", ROOT / "scripts" / "doctor.py")

class EmployMindsTests(unittest.TestCase):
    def test_policy_and_source_layout(self):
        policy = json.loads((ROOT / "config/employ-minds-policy.json").read_text(encoding="utf-8"))
        self.assertEqual(policy["schema_version"], 2)
        self.assertEqual(policy["default_profile"], "standard")
        self.assertTrue(policy["completion_requires_fresh_evidence"])
        self.assertTrue(policy["native_agent_separation"])
        self.assertEqual(doctor.self_check(ROOT), [])

    def test_managed_block_is_idempotent_and_preserves_user_content(self):
        original = "# Existing instructions\nDo not touch this.\n"
        once = install.replace_block(original, install.CLAUDE_BLOCK)
        twice = install.replace_block(once, install.CLAUDE_BLOCK)
        self.assertEqual(once, twice)
        self.assertIn("Do not touch this.", twice)
        self.assertEqual(twice.count(install.BEGIN), 1)
        self.assertIn("Do not touch this.", install.remove_block(twice))

    def test_install_both_registers_native_agents(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            (project / "CLAUDE.md").write_text("# Mine\n", encoding="utf-8")
            (project / "AGENTS.md").write_text("# Also mine\n", encoding="utf-8")
            install.copy_payload(ROOT, project, "both")
            self.assertEqual(doctor.check_project(project, "both"), [])
            self.assertTrue((project / ".claude/agents/em-verifier.md").exists())
            self.assertTrue((project / ".codex/agents/em-verifier.toml").exists())
            self.assertTrue((project / ".claude/agents/em-scout.md").exists())
            self.assertTrue((project / ".codex/agents/em-scout.toml").exists())
            state = json.loads((project / ".employ-minds/install-state.json").read_text())
            self.assertTrue(state["native_agents"])

    def test_reinstall_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            install.copy_payload(ROOT, project, "both")
            install.copy_payload(ROOT, project, "both")
            self.assertEqual((project / "CLAUDE.md").read_text().count(install.BEGIN), 1)
            self.assertEqual((project / "AGENTS.md").read_text().count(install.BEGIN), 1)
            self.assertEqual(doctor.check_project(project, "both"), [])

    def test_partial_uninstall_keeps_other_target(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            install.copy_payload(ROOT, project, "both")
            install.uninstall(project, "claude")
            self.assertTrue((project / ".employ-minds").exists())
            self.assertFalse((project / ".claude/agents/em-verifier.md").exists())
            self.assertTrue((project / ".codex/agents/em-verifier.toml").exists())
            self.assertEqual(doctor.check_project(project, "codex"), [])
            install.uninstall(project, "codex")
            self.assertFalse((project / ".employ-minds").exists())

    def test_unrelated_skills_and_agents_survive(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            skill = project / ".claude/skills/my-own-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("mine\n")
            agent = project / ".claude/agents/my-agent.md"
            agent.parent.mkdir(parents=True, exist_ok=True)
            agent.write_text("mine\n")
            codex_agent = project / ".codex/agents/my-agent.toml"
            codex_agent.parent.mkdir(parents=True, exist_ok=True)
            codex_agent.write_text("mine\n")
            install.copy_payload(ROOT, project, "both")
            install.uninstall(project, "both")
            self.assertTrue(skill.exists())
            self.assertEqual(agent.read_text(), "mine\n")
            self.assertEqual(codex_agent.read_text(), "mine\n")

    def test_native_role_capabilities_are_separated(self):
        for name in doctor.AGENTS:
            codex = (ROOT / f"native/codex/agents/em-{name}.toml").read_text()
            claude = (ROOT / f"native/claude/agents/em-{name}.md").read_text()
            if name == "implementer":
                self.assertIn('sandbox_mode = "workspace-write"', codex)
                self.assertNotIn("permissionMode: plan", claude)
            else:
                self.assertIn('sandbox_mode = "read-only"', codex)
                self.assertIn("permissionMode: plan", claude)

if __name__ == "__main__":
    unittest.main()
