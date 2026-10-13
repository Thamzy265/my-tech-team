import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import lint_skills  # noqa: E402

GOOD = """---
name: team-demo
description: Use when testing the linter. Does nothing else.
license: MIT
metadata:
  checked: "2026-10-12"
---

# Demo

Load `references/extra.md` when needed.

## Host safety

Ask the PM first.
"""


def make_skill(root: Path, name: str, text: str, refs=("references/extra.md",)) -> Path:
    d = root / name
    (d / "references").mkdir(parents=True)
    (d / "SKILL.md").write_text(text)
    for r in refs:
        (d / r).parent.mkdir(parents=True, exist_ok=True)
        (d / r).write_text("# extra\n")
    return d


class ParseFrontmatter(unittest.TestCase):
    def test_parses_top_level_keys_and_body(self):
        meta, body = lint_skills.parse_frontmatter(GOOD)
        self.assertEqual(meta["name"], "team-demo")
        self.assertEqual(set(meta), {"name", "description", "license", "metadata"})
        self.assertIn("# Demo", body)

    def test_missing_frontmatter_raises(self):
        with self.assertRaises(ValueError):
            lint_skills.parse_frontmatter("# no frontmatter\n")


class LintSkill(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_good_skill_has_no_errors(self):
        d = make_skill(self.root, "team-demo", GOOD)
        self.assertEqual(lint_skills.lint_skill(d), [])

    def test_host_safety_section_required(self):
        d = make_skill(self.root, "team-demo", GOOD.replace("## Host safety", "## Something else"))
        self.assertTrue(any("missing '## Host safety' section" in e for e in lint_skills.lint_skill(d)))

    def test_name_must_match_folder(self):
        d = make_skill(self.root, "team-other", GOOD)
        self.assertTrue(any("does not match folder" in e for e in lint_skills.lint_skill(d)))

    def test_name_format(self):
        d = make_skill(self.root, "Team--Bad", GOOD.replace("team-demo", "Team--Bad"))
        self.assertTrue(any("invalid name" in e for e in lint_skills.lint_skill(d)))

    def test_claude_only_key_rejected(self):
        text = GOOD.replace("license: MIT", "license: MIT\nwhen_to_use: always")
        d = make_skill(self.root, "team-demo", text)
        self.assertTrue(any("non-spec frontmatter key 'when_to_use'" in e for e in lint_skills.lint_skill(d)))

    def test_description_too_long(self):
        text = GOOD.replace("Use when testing the linter. Does nothing else.", "x" * 1025)
        d = make_skill(self.root, "team-demo", text)
        self.assertTrue(any("description" in e and "1024" in e for e in lint_skills.lint_skill(d)))

    def test_too_many_lines(self):
        d = make_skill(self.root, "team-demo", GOOD + "line\n" * 500)
        self.assertTrue(any("500" in e for e in lint_skills.lint_skill(d)))

    def test_missing_reference_file(self):
        d = make_skill(self.root, "team-demo", GOOD, refs=())
        self.assertTrue(any("missing file references/extra.md" in e for e in lint_skills.lint_skill(d)))

    def test_flutterdeck_leftovers_rejected(self):
        for bad in ("Use the deck-reviewer skill.", "Run pnpm check.", "FlutterDeck rules", "Validate with zod."):
            with self.subTest(bad=bad):
                sub = self.root / bad[:5]
                d = make_skill(sub, "team-demo", GOOD + bad + "\n")
                self.assertTrue(any("project-specific term" in e for e in lint_skills.lint_skill(d)))

    def test_deck_template_filename_is_allowed(self):
        d = make_skill(self.root, "team-demo", GOOD + "Copy `assets/deck-template.html`.\n",
                       refs=("references/extra.md", "assets/deck-template.html"))
        self.assertEqual(lint_skills.lint_skill(d), [])

    def test_url_path_is_not_a_file_reference(self):
        d = make_skill(self.root, "team-demo", GOOD + "See https://example.com/references/missing.md.\n")
        self.assertEqual(lint_skills.lint_skill(d), [])

    def test_banned_terms_scanned_in_assets_and_scripts(self):
        d = make_skill(self.root, "team-demo", GOOD,
                       refs=("references/extra.md", "assets/deck-template.html", "scripts/run.py"))
        (d / "assets" / "deck-template.html").write_text("<h1>FlutterDeck</h1>\n")
        errors = lint_skills.lint_skill(d)
        self.assertTrue(any("deck-template.html" in e and "project-specific term" in e for e in errors))

    def test_block_scalar_description_rejected(self):
        for marker in (">", "|"):
            with self.subTest(marker=marker):
                text = GOOD.replace("description: Use when testing the linter. Does nothing else.",
                                    f"description: {marker}\n  Use when testing the linter.")
                d = make_skill(self.root / ("s" + str(ord(marker))), "team-demo", text)
                self.assertTrue(any("single line" in e for e in lint_skills.lint_skill(d)))


class Main(unittest.TestCase):
    def test_exit_code_reflects_errors(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            make_skill(root, "team-demo", GOOD)
            self.assertEqual(lint_skills.main([str(root)]), 0)
            make_skill(root, "team-bad", GOOD)  # name mismatch
            self.assertEqual(lint_skills.main([str(root)]), 1)


if __name__ == "__main__":
    unittest.main()
