import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import lint_agents  # noqa: E402

ROLE = """---
name: {name}
description: Use only when the my-tech-team lead dispatches the {name} role.
model: sonnet
effort: medium
{tools}skills:
  - my-tech-team:{name}
---

Body.
"""

SCOUT = """---
name: scout
description: Use only when the my-tech-team lead needs a quick lookup.
model: haiku
effort: low
tools: Read, Grep, Glob, Bash
---

Body.
"""

TOOLS = {
    "reviewer": "tools: Read, Grep, Glob, Bash, Skill, ReportFindings\n",
    "marketer": "tools: Read, Write, Edit, Grep, Glob, WebFetch, WebSearch, Skill\n",
}


def write_set(root: Path, overrides=None):
    overrides = overrides or {}
    for name in ["developer", "tester", "reviewer", "qa", "marketer"]:
        text = ROLE.format(name=name, tools=TOOLS.get(name, ""))
        (root / f"{name}.md").write_text(overrides.get(name, text))
    (root / "scout.md").write_text(overrides.get("scout", SCOUT))


class LintAgentsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def errors(self, overrides=None):
        write_set(self.root, overrides)
        return lint_agents.lint_dir(self.root)

    def test_good_set_passes(self):
        self.assertEqual(self.errors(), [])

    def test_missing_agent(self):
        write_set(self.root)
        (self.root / "qa.md").unlink()
        errs = lint_agents.lint_dir(self.root)
        self.assertTrue(any("missing agent 'qa'" in e for e in errs), errs)

    def test_unexpected_agent(self):
        write_set(self.root)
        (self.root / "designer.md").write_text(ROLE.format(name="designer", tools=""))
        errs = lint_agents.lint_dir(self.root)
        self.assertTrue(any("unexpected agent 'designer'" in e for e in errs), errs)

    def test_name_must_match_file(self):
        bad = ROLE.format(name="developer", tools="").replace("name: developer", "name: dev")
        errs = self.errors({"developer": bad})
        self.assertTrue(any("does not match file" in e for e in errs), errs)

    def test_model_required_and_not_inherit(self):
        missing = ROLE.format(name="tester", tools="").replace("model: sonnet\n", "")
        self.assertTrue(any("model" in e for e in self.errors({"tester": missing})))
        inherit = ROLE.format(name="tester", tools="").replace("model: sonnet", "model: inherit")
        self.assertTrue(any("model" in e for e in self.errors({"tester": inherit})))

    def test_effort_must_be_valid(self):
        bad = ROLE.format(name="qa", tools="").replace("effort: medium", "effort: extreme")
        self.assertTrue(any("effort" in e for e in self.errors({"qa": bad})))

    def test_role_must_preload_its_skill(self):
        bad = ROLE.format(name="developer", tools="").replace("my-tech-team:developer", "my-tech-team:tester")
        errs = self.errors({"developer": bad})
        self.assertTrue(any("skills must include 'my-tech-team:developer'" in e for e in errs), errs)

    def test_reviewer_cannot_edit(self):
        bad = ROLE.format(name="reviewer", tools="tools: Read, Bash, Skill, Edit\n")
        errs = self.errors({"reviewer": bad})
        self.assertTrue(any("reviewer must not have Edit" in e for e in errs), errs)

    def test_reviewer_needs_tools_line(self):
        bad = ROLE.format(name="reviewer", tools="")
        errs = self.errors({"reviewer": bad})
        self.assertTrue(any("reviewer must set tools" in e for e in errs), errs)

    def test_reviewer_needs_skill_tool(self):
        bad = ROLE.format(name="reviewer", tools="tools: Read, Grep, Glob, Bash\n")
        errs = self.errors({"reviewer": bad})
        self.assertTrue(any("reviewer must have Skill" in e for e in errs), errs)

    def test_scout_cannot_write(self):
        bad = SCOUT.replace("tools: Read, Grep, Glob, Bash", "tools: Read, Write")
        errs = self.errors({"scout": bad})
        self.assertTrue(any("scout must not have Write" in e for e in errs), errs)

    def test_marketer_has_no_shell(self):
        bad = ROLE.format(name="marketer", tools="tools: Read, Write, Bash, Skill\n")
        errs = self.errors({"marketer": bad})
        self.assertTrue(any("marketer must not have Bash" in e for e in errs), errs)

    def test_plugin_ignored_keys_are_errors(self):
        bad = ROLE.format(name="qa", tools="").replace("effort: medium", "effort: medium\npermissionMode: acceptEdits")
        errs = self.errors({"qa": bad})
        self.assertTrue(any("permissionMode" in e for e in errs), errs)

    def test_tools_as_yaml_list(self):
        listed = ROLE.format(name="reviewer", tools="tools:\n  - Read\n  - Bash\n  - Skill\n")
        self.assertEqual(self.errors({"reviewer": listed}), [])


if __name__ == "__main__":
    unittest.main()
