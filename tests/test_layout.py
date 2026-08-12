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

install = load("em_install", ROOT / "scripts/install.py")
doctor = load("em_doctor", ROOT / "scripts/doctor.py")
renderer = load("em_renderer", ROOT / "scripts/render_agents.py")

class EmployMindsTests(unittest.TestCase):
    def test_policy_source_layout_and_generated_agent_parity(self):
        policy = json.loads((ROOT / "config/employ-minds-policy.json").read_text(encoding="utf-8"))
        self.assertEqual(policy["schema_version"], 2)
        self.assertEqual(policy["default_profile"], "standard")
        self.assertTrue(policy["completion_requires_fresh_evidence"])
        self.assertTrue(policy["native_agent_separation"])
        self.assertEqual(doctor.self_check(ROOT), [])
        self.assertEqual(renderer.check(), [])

    def test_managed_block_is_idempotent_and_preserves_user_content(self):
        original = "# Existing instructions\nDo not touch this.\n"
        once = install.replace_block(original, install.CLAUDE_BLOCK)
        twice = install.replace_block(once, install.CLAUDE_BLOCK)
        self.assertEqual(once, twice)
        self.assertIn("Do not touch this.", twice)
        self.assertEqual(twice.count(install.BEGIN), 1)
        self.assertIn("Do not touch this.", install.remove_block(twice))

    def test_install_both_registers_exact_ownership(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            (project / "CLAUDE.md").write_text("# Mine\n", encoding="utf-8")
            (project / "AGENTS.md").write_text("# Also mine\n", encoding="utf-8")
            install.copy_payload(ROOT, project, "both")
            self.assertEqual(doctor.check_project(project, "both"), [])
            state = json.loads((project / ".employ-minds/install-state.json").read_text())
            self.assertIn("em-verifier.md", state["claude_agents"])
            self.assertIn("em-verifier.toml", state["codex_agents"])
            self.assertIn("employ-minds-router", state["claude_skills"])
            self.assertIn("employ-minds-router", state["codex_skills"])
            self.assertEqual(state["claude_command"], "employ-minds.md")

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
            state = json.loads((project / ".employ-minds/install-state.json").read_text())
            self.assertEqual(state["claude_agents"], [])
            self.assertIn("em-verifier.toml", state["codex_agents"])
            install.uninstall(project, "codex")
            self.assertFalse((project / ".employ-minds").exists())

    def test_unrelated_em_prefix_agents_survive_install_and_uninstall(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            claude_agent = project / ".claude/agents/em-personal.md"
            claude_agent.parent.mkdir(parents=True, exist_ok=True)
            claude_agent.write_text("mine\n")
            codex_agent = project / ".codex/agents/em-personal.toml"
            codex_agent.parent.mkdir(parents=True, exist_ok=True)
            codex_agent.write_text("mine\n")
            install.copy_payload(ROOT, project, "both")
            install.copy_payload(ROOT, project, "both")
            install.uninstall(project, "both")
            self.assertEqual(claude_agent.read_text(), "mine\n")
            self.assertEqual(codex_agent.read_text(), "mine\n")

    def test_first_install_refuses_exact_agent_collision_without_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            collision = project / ".claude/agents/em-verifier.md"
            collision.parent.mkdir(parents=True)
            collision.write_text("user-owned\n")
            with self.assertRaises(RuntimeError):
                install.copy_payload(ROOT, project, "claude")
            self.assertEqual(collision.read_text(), "user-owned\n")
            self.assertFalse((project / ".employ-minds").exists())
            self.assertFalse((project / "CLAUDE.md").exists())

    def test_first_install_refuses_exact_skill_collision_without_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            collision = project / ".agents/skills/employ-minds-router"
            collision.mkdir(parents=True)
            (collision / "SKILL.md").write_text("user-owned\n")
            with self.assertRaises(RuntimeError):
                install.copy_payload(ROOT, project, "codex")
            self.assertEqual((collision / "SKILL.md").read_text(), "user-owned\n")
            self.assertFalse((project / ".employ-minds").exists())
            self.assertFalse((project / "AGENTS.md").exists())

    def test_first_install_refuses_command_collision_without_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            command = project / ".claude/commands/employ-minds.md"
            command.parent.mkdir(parents=True)
            command.write_text("user-owned\n")
            with self.assertRaises(RuntimeError):
                install.copy_payload(ROOT, project, "claude")
            self.assertEqual(command.read_text(), "user-owned\n")
            self.assertFalse((project / ".employ-minds").exists())

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
