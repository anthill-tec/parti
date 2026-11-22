"""Repository guards: the licence, the glossary's rules, decision numbering, and links.

These run in CI on every develop push and pull request. They guard what the design exercise settled
(D20 licence, the Ubiquitous Language rules, the PRD's decision table) until code brings its own tests.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "docs" / "research" / "DN-ubiquitous-language.md"
PRD = ROOT / "docs" / "research" / "PRD-parti.md"
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def section(text: str, heading: str) -> str:
    """The body of a `## heading` section, up to the next `## ` heading."""
    start = text.index(f"## {heading}\n")
    end = text.find("\n## ", start + 1)
    return text[start : end if end != -1 else len(text)]


def table_rows(text: str) -> list[list[str]]:
    """The body rows of the markdown tables in `text`, as stripped cells (header and rule excluded)."""
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


class LicenceTest(unittest.TestCase):
    """D20: Parti is GPL-3.0-only, declared the same way everywhere."""

    def test_licence_file_is_gpl_v3(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", text)
        self.assertIn("Version 3, 29 June 2007", text)

    def test_package_json_declares_gpl_3_only(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertEqual(package["license"], "GPL-3.0-only")

    def test_readme_names_the_same_licence(self):
        self.assertIn("GPL-3.0-only", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_no_apache_notice_file(self):
        self.assertFalse((ROOT / "NOTICE").exists(), "NOTICE belongs to Apache-2.0, not GPL-3.0-only")


class GlossaryTest(unittest.TestCase):
    """The Ubiquitous Language's rules: one meaning per term, one owning context."""

    def setUp(self):
        rows = table_rows(section(GLOSSARY.read_text(encoding="utf-8"), "Terms"))
        self.assertEqual(rows[0], ["Term", "Meaning", "Context"])
        self.terms = rows[1:]

    def test_has_terms(self):
        self.assertGreater(len(self.terms), 20)

    def test_each_term_appears_once(self):
        names = [row[0].lower() for row in self.terms]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        self.assertEqual(duplicates, [], f"terms defined more than once: {duplicates}")

    def test_each_term_has_a_meaning_and_a_context(self):
        for term, meaning, context in self.terms:
            with self.subTest(term=term):
                self.assertTrue(meaning, "no meaning")
                self.assertTrue(context, "no owning context ('—' when none)")


class DecisionsTest(unittest.TestCase):
    """The PRD's decision table: D1..Dn, each exactly once, none missing."""

    def test_decisions_are_numbered_without_gaps_or_repeats(self):
        rows = table_rows(section(PRD.read_text(encoding="utf-8"), "3. Decisions already taken (owner)"))
        numbers = [int(row[0][1:]) for row in rows if re.fullmatch(r"D\d+", row[0])]
        self.assertEqual(len(numbers), len(set(numbers)), "a decision number is used twice")
        self.assertEqual(sorted(numbers), list(range(1, max(numbers) + 1)), "a decision number is missing")


class LinksTest(unittest.TestCase):
    """Every relative markdown link in the repository's documents points at a file that exists."""

    def test_relative_links_resolve(self):
        documents = [ROOT / "README.md", ROOT / "AGENTS.md", *sorted((ROOT / "docs").rglob("*.md"))]
        broken = []
        for document in documents:
            for target in LINK.findall(document.read_text(encoding="utf-8")):
                if re.match(r"[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                path = target.split("#", 1)[0]
                if not (document.parent / path).exists():
                    broken.append(f"{document.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [], "broken links:\n" + "\n".join(broken))


if __name__ == "__main__":
    unittest.main()
