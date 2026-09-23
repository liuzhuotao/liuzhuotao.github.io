"""Reject publication editing mistakes before a successful build can hide them."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from publication_files import validate_publication_files


TITLE = "TrafficFlex: A Multi-Functional Incremental Learning Model for Evolving Network Traffic Analysis"
FIELDS = (
    f'title: "{TITLE}"\n'
    'authors: ["Xiaodong Lei", "Lin Liu", "Zhuotao Liu", "Junjie Huang", "Luming Yang", '
    '"Shiyu Liang", "Shaojing Fu", "Shuhui Chen", "Yongjun Wang"]\n'
    'venue: "ISOC NDSS"\nyear: 2027\n'
)


class PublicationFileTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name) / "content/publications"
        self.directory.mkdir(parents=True)

    def test_exact_extensionless_trafficflex_entry_explains_required_filename(self):
        entry = self.directory / TITLE
        entry.write_text(FIELDS, encoding="utf-8")
        with self.assertRaises(ValueError) as caught:
            validate_publication_files(self.directory)
        message = str(caught.exception)
        self.assertIn(str(entry), message)
        self.assertIn(TITLE + ".md", message)
        self.assertIn("trafficflex.md", message)
        self.assertIn("opening and closing '---'", message)

    def test_renaming_alone_does_not_hide_missing_frontmatter(self):
        entry = self.directory / "trafficflex.md"
        entry.write_text(FIELDS, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "trafficflex.md: missing opening '---'"):
            validate_publication_files(self.directory)

    def test_opening_boundary_without_closing_boundary_is_rejected(self):
        entry = self.directory / "trafficflex.md"
        entry.write_text("---\n" + FIELDS, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "trafficflex.md: missing closing '---'"):
            validate_publication_files(self.directory)

    def test_minimal_fixed_entry_draft_index_and_hidden_files_remain_valid(self):
        (self.directory / "trafficflex.md").write_text("---\n" + FIELDS + "---\n", encoding="utf-8")
        (self.directory / "draft.md").write_text("---\n" + FIELDS + "draft: true\n---\n", encoding="utf-8")
        (self.directory / "_index.md").write_text('---\ntitle: "Publications"\n---\n', encoding="utf-8")
        (self.directory / ".DS_Store").write_bytes(b"ignored operating-system metadata")
        hidden = self.directory / ".drafts"
        hidden.mkdir()
        (hidden / "scratch").write_text("incomplete private draft", encoding="utf-8")
        validate_publication_files(self.directory)

    def test_windows_newlines_and_abstract_with_separators_remain_valid(self):
        raw = "---\n" + FIELDS + "---\n\nA user-written abstract.\n\n---\n\nMore text.\n"
        (self.directory / "trafficflex.md").write_bytes(raw.replace("\n", "\r\n").encode())
        validate_publication_files(self.directory)

    def test_invalid_entry_is_checked_before_hugo_can_omit_it(self):
        (self.directory / TITLE).write_text(FIELDS, encoding="utf-8")
        spec = importlib.util.spec_from_file_location("publication_inventory_check", SCRIPTS / "check.py")
        check = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(check)
        with patch.object(check.subprocess, "run") as hugo:
            with self.assertRaisesRegex(ValueError, "must have a .md filename"):
                check.published_papers("hugo", Path(self.temporary.name))
        hugo.assert_not_called()


if __name__ == "__main__":
    unittest.main()
