"""Regression tests for conservative, non-destructive publication enrichment."""

from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "enrich_publications.py"
SPEC = importlib.util.spec_from_file_location("enrich_publications", SCRIPT)
enrich = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = enrich
SPEC.loader.exec_module(enrich)


class CandidateMatchingTests(unittest.TestCase):
    def setUp(self):
        self.metadata = {
            "title": "Private Systems: A Practical Design",
            "authors": ["Zhuotao Liu", "José García"],
            "year": 2025,
        }
        self.candidate = enrich.Candidate(
            title=self.metadata["title"],
            authors=list(self.metadata["authors"]),
            year=2025,
            source_url="https://arxiv.org/abs/2501.01234",
            paper="https://doi.org/10.1234/example",
            pdf="https://arxiv.org/pdf/2501.01234",
            abstract="A practical system for private computation.",
            preprint="https://arxiv.org/abs/2501.01234",
        )

    def test_normalization_handles_case_accents_and_punctuation(self):
        self.assertEqual(enrich.normalize("  Café—Systems: A Practical Design! "),
                         enrich.normalize("cafe systems a practical design"))
        self.assertNotEqual(enrich.normalize("Private System"), enrich.normalize("Private Systems"))

    def test_authors_require_complete_names_but_allow_reordering(self):
        self.assertTrue(enrich.authors_match(
            ["José García", "Zhuotao Liu"], ["ZHUOTAO LIU", "Jose Garcia"]))
        for remote in (["J. Garcia", "Zhuotao Liu"], ["José García"],
                       ["José García", "Zhuotao Liu", "Another Author"],
                       ["José García", "Zhuotao Li"], []):
            with self.subTest(remote=remote):
                self.assertFalse(enrich.authors_match(self.metadata["authors"], remote))

    def test_exact_match_and_two_year_boundary_are_accepted(self):
        for year in (2023, 2025, 2027):
            candidate = replace(self.candidate, title="private systems — a practical design",
                                authors=["Jose Garcia", "Zhuotao Liu"], year=year)
            with self.subTest(year=year):
                self.assertEqual(enrich.choose_candidate(self.metadata, [candidate]), candidate)

    def test_near_title_wrong_authors_and_unverifiable_year_are_rejected(self):
        rejected = (
            replace(self.candidate, title="Private Systems: Another Practical Design"),
            replace(self.candidate, title="Private Systems: A Practical Design, Extended Version"),
            replace(self.candidate, authors=["J. García", "Zhuotao Liu"]),
            replace(self.candidate, authors=["Zhuotao Liu"]),
            replace(self.candidate, authors=["José García", "Someone Else"]),
            replace(self.candidate, year=2022),
            replace(self.candidate, year=2028),
            replace(self.candidate, year=None),
            replace(self.candidate, source_url="http://arxiv.org/abs/2501.01234"),
            replace(self.candidate, source_url="https://127.0.0.1/private"),
        )
        for candidate in rejected:
            with self.subTest(candidate=candidate):
                self.assertIsNone(enrich.choose_candidate(self.metadata, [candidate]))

    def test_multiple_sources_are_ambiguous_but_identical_duplicates_are_not(self):
        second = replace(self.candidate, source_url="https://doi.org/10.9999/another-record")
        self.assertIsNone(enrich.choose_candidate(self.metadata, [self.candidate, second]))
        self.assertEqual(enrich.choose_candidate(self.metadata, [self.candidate, replace(self.candidate)]),
                         self.candidate)
        self.assertIsNone(enrich.choose_candidate(self.metadata, []))

    def test_unrelated_search_results_do_not_make_a_unique_match_ambiguous(self):
        unrelated = replace(self.candidate, title="A Different Research Paper",
                            source_url="https://doi.org/10.9999/unrelated")
        self.assertEqual(enrich.choose_candidate(self.metadata, [unrelated, self.candidate]), self.candidate)

    def test_conflicting_payloads_at_the_same_source_are_rejected(self):
        conflicting = replace(self.candidate, abstract="A different, conflicting abstract from the same record.")
        for candidates in ([self.candidate, conflicting], [conflicting, self.candidate]):
            self.assertIsNone(enrich.choose_candidate(self.metadata, candidates))


class PublicationFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "publication.md"
        self.candidate = enrich.Candidate(
            title="Private Systems",
            authors=["Zhuotao Liu", "Research Author"],
            year=2025,
            source_url="https://arxiv.org/abs/2501.01234",
            paper="https://doi.org/10.1234/verified",
            pdf="https://arxiv.org/pdf/2501.01234",
            abstract="A verified abstract describing useful research.",
            preprint="https://arxiv.org/abs/2501.01234",
        )
        self.frontmatter = (
            '---\n'
            '# Hand-maintained metadata; keep this comment verbatim.\n'
            'title: "Private Systems"\n'
            'authors: ["Zhuotao Liu", "Research Author"]\n'
            'venue: "My Chosen Venue"\n'
            'year: 2025\n'
            'selected: true  # homepage choice\n'
            'aliases: ["/publications/original-path/"]\n'
            'group_authors: [2]\n'
            'custom_notes:\n'
            '  text: "Preserve my punctuation: café & systems."\n'
        )

    def load(self, raw):
        self.path.write_text(raw, encoding="utf-8")
        return enrich.load_publication(self.path)

    def reload_result(self, updated):
        self.path.write_text(updated, encoding="utf-8")
        return enrich.load_publication(self.path)

    def assert_original_lines_preserved(self, original_frontmatter, updated):
        """Existing frontmatter bytes must occur in their original order."""
        cursor = 0
        for line in original_frontmatter.splitlines(keepends=True):
            position = updated.find(line, cursor)
            self.assertGreaterEqual(position, 0, f"Lost or altered original metadata line: {line!r}")
            cursor = position + len(line)


class PublicationPreservationTests(PublicationFixture):
    def test_fills_missing_fields_without_writing_the_source_file(self):
        raw = self.frontmatter + '---\n\n'
        publication = self.load(raw)
        self.assertEqual(publication.raw, raw)
        self.assertEqual(publication.path, self.path)
        updated = enrich.apply_candidate(publication, self.candidate)
        self.assertEqual(self.path.read_text(encoding="utf-8"), raw)
        enriched = self.reload_result(updated)
        for key in ("paper", "pdf", "preprint"):
            self.assertEqual(enriched.metadata[key], getattr(self.candidate, key))
        self.assertIn("verified abstract describing useful research", enriched.body)
        self.assert_original_lines_preserved(self.frontmatter, updated)
        for key, value in publication.metadata.items():
            self.assertEqual(enriched.metadata[key], value)

    def test_manual_links_body_and_all_metadata_are_preserved(self):
        manual = (
            'paper: "https://example.org/author-chosen-paper"\n'
            'pdf: "https://example.org/author-chosen.pdf"\n'
            'preprint: "https://example.org/author-chosen-preprint"\n'
            'auto_enrich: false\n'
        )
        body = '\nMy **handwritten abstract**, including [my link](https://example.org/notes).\n\nSecond paragraph.\n'
        raw = self.frontmatter + manual + '---\n' + body
        publication = self.load(raw)
        updated = enrich.apply_candidate(publication, self.candidate)
        enriched = self.reload_result(updated)
        self.assertEqual(enriched.metadata, publication.metadata)
        self.assertEqual(enriched.body, publication.body)
        self.assert_original_lines_preserved(self.frontmatter + manual, updated)

    def test_empty_and_null_manual_keys_are_not_filled(self):
        manual = 'paper: ""\npdf:\npreprint: null\n'
        publication = self.load(self.frontmatter + manual + '---\n\n')
        updated = enrich.apply_candidate(publication, self.candidate)
        enriched = self.reload_result(updated)
        self.assertEqual(enriched.metadata["paper"], "")
        self.assertIsNone(enriched.metadata["pdf"])
        self.assertIsNone(enriched.metadata["preprint"])
        self.assert_original_lines_preserved(self.frontmatter + manual, updated)

    def test_reloading_and_enriching_again_is_idempotent(self):
        publication = self.load(self.frontmatter + '---\n\n')
        first = enrich.apply_candidate(publication, self.candidate)
        reloaded = self.reload_result(first)
        self.assertEqual(enrich.apply_candidate(reloaded, self.candidate), first)

    def test_crlf_metadata_and_handwritten_body_keep_their_bytes(self):
        frontmatter = self.frontmatter.replace('\n', '\r\n')
        raw = frontmatter + '---\r\n\r\nMy original abstract.\r\n\r\nSecond paragraph.\r\n'
        publication = self.load(raw)
        updated = enrich.apply_candidate(publication, self.candidate)
        self.assertEqual(self.path.read_bytes().decode('utf-8'), raw)
        self.assert_original_lines_preserved(frontmatter, updated)
        self.assertEqual(self.reload_result(updated).body, publication.body)

    def test_duplicate_metadata_keys_are_rejected_without_changing_the_file(self):
        raw = self.frontmatter + 'selected: false\n---\n\n'
        self.path.write_text(raw, encoding='utf-8')
        with self.assertRaisesRegex(ValueError, "Duplicate frontmatter key"):
            enrich.load_publication(self.path)
        self.assertEqual(self.path.read_text(encoding='utf-8'), raw)

    def test_unsafe_candidate_links_are_never_inserted(self):
        candidate = replace(self.candidate, paper="javascript:alert(1)",
                            pdf="https://localhost/private.pdf", preprint="file:///etc/passwd")
        publication = self.load(self.frontmatter + '---\n\nExisting abstract.\n')
        enriched = self.reload_result(enrich.apply_candidate(publication, candidate))
        self.assertFalse(any(key in enriched.metadata for key in ("paper", "pdf", "preprint")))
        self.assertEqual(enriched.body, publication.body)

    def test_remote_html_and_markdown_become_inert_abstract_text(self):
        abstract = ('<script>alert("bad")</script><p>Useful <b>research</b>.</p>\n'
                    '# Remote heading\n- Remote list\n'
                    '[click](javascript:alert(1)) ![pixel](https://example.org/track.png) '
                    '{{% remote-shortcode %}}')
        publication = self.load(self.frontmatter + '---\n\n')
        updated = enrich.apply_candidate(publication, replace(self.candidate, abstract=abstract))
        body = self.reload_result(updated).body
        self.assertIn("Useful", body)
        self.assertIn("research", body)
        self.assertNotRegex(body, r"<\s*/?\s*(?:script|p|b)\b")
        self.assertNotRegex(body, r"(?<!\\)!?\[[^\n]*?\]\(")
        self.assertNotRegex(body, r"(?m)^\s{0,3}(?:#{1,6}\s|[-+*]\s)")
        self.assertNotIn("{{%", body)


class RunTests(PublicationFixture):
    class Client:
        def __init__(self, crossref=(), arxiv=()):
            self.results = {"crossref": crossref, "arxiv": arxiv}
            self.calls = []

        def result(self, provider, metadata):
            self.calls.append(provider)
            result = self.results[provider]
            if isinstance(result, Exception):
                raise result
            return result(metadata) if callable(result) else result

        def crossref(self, metadata):
            return self.result("crossref", metadata)

        def arxiv(self, metadata):
            return self.result("arxiv", metadata)

    def test_run_is_dry_by_default(self):
        raw = self.frontmatter + '---\n\n'
        self.load(raw)
        client = self.Client(crossref=[self.candidate])
        report = enrich.run(self.path.parent, client)
        self.assertEqual(report["mode"], "dry-run")
        self.assertEqual([change["file"] for change in report["changed"]], [self.path.name])
        self.assertEqual(self.path.read_text(encoding="utf-8"), raw)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_provider_failure_does_not_block_the_other_provider(self):
        self.load(self.frontmatter + '---\n\n')
        arxiv = replace(self.candidate, paper="", pdf="")
        client = self.Client(crossref=RuntimeError("Publisher service unavailable"), arxiv=[arxiv])
        report = enrich.run(self.path.parent, client, write=True)
        enriched = enrich.load_publication(self.path)
        self.assertEqual(client.calls, ["crossref", "arxiv"])
        self.assertEqual(enriched.metadata["preprint"], arxiv.preprint)
        self.assertNotIn("paper", enriched.metadata)
        self.assertNotIn("pdf", enriched.metadata)
        self.assertTrue(enriched.body.strip())
        self.assertEqual(report["warnings"][0]["provider"], "crossref")
        self.assertEqual(len(report["changed"]), 1)

    def test_two_providers_fill_complementary_fields_without_replacing_manual_null(self):
        publication = self.load(self.frontmatter + 'pdf: null\n---\n\n')
        publisher = replace(self.candidate, source_url="https://doi.org/10.1234/verified", pdf="",
                            preprint="", abstract="")
        arxiv = replace(self.candidate, paper="", pdf="")
        client = self.Client(crossref=[publisher], arxiv=[arxiv])
        report = enrich.run(self.path.parent, client, write=True)
        enriched = enrich.load_publication(self.path)
        self.assertEqual(client.calls, ["crossref", "arxiv"])
        self.assertEqual(enriched.metadata["paper"], publisher.paper)
        self.assertEqual(enriched.metadata["preprint"], arxiv.preprint)
        self.assertIsNone(enriched.metadata["pdf"])
        self.assertIn("verified abstract", enriched.body)
        self.assertEqual(enriched.metadata["selected"], publication.metadata["selected"])
        self.assertEqual(report["changed"][0]["sources"], [publisher.source_url, arxiv.source_url])

    def test_concurrent_local_edit_is_fatal_and_never_overwritten(self):
        self.load(self.frontmatter + '---\n\n')
        user_edit = self.frontmatter + '---\n\nNew abstract written while metadata was being fetched.\n'

        def concurrent_edit(_):
            self.path.write_text(user_edit, encoding="utf-8")
            return [self.candidate]

        with self.assertRaisesRegex(RuntimeError, "file changed during enrichment"):
            enrich.run(self.path.parent, self.Client(crossref=concurrent_edit), write=True)
        self.assertEqual(self.path.read_text(encoding="utf-8"), user_edit)

    def test_drafts_patents_and_explicit_opt_out_are_not_queried(self):
        for name, metadata in (("draft", "draft: true\n"), ("patent", "category: patent\n"),
                               ("opt-out", "auto_enrich: false\n")):
            (self.path.parent / f"{name}.md").write_text(self.frontmatter + metadata + '---\n\n', encoding="utf-8")
        client = self.Client(crossref=[self.candidate])
        report = enrich.run(self.path.parent, client, write=True)
        self.assertEqual(client.calls, [])
        self.assertEqual(report["checked"], 0)
        self.assertEqual(report["changed"], [])


class ProviderParsingTests(unittest.TestCase):
    def test_crossref_uses_the_doi_and_only_unambiguous_public_pdf_links(self):
        record = {
            "DOI": "10.1234/record",
            "title": ["A Research Paper"],
            "author": [{"given": "Zhuotao", "family": "Liu"}],
            "published-online": {"date-parts": [[2025, 3, 1]]},
            "link": [{"URL": "https://localhost/private.pdf", "content-type": "application/pdf"},
                     {"URL": "https://example.org/paper.pdf", "content-type": "application/pdf"}],
        }
        client = enrich.MetadataClient()
        client.get = lambda _: json.dumps({"message": {"items": [record]}}).encode()
        candidate, = client.crossref({"title": "A Research Paper"})
        self.assertEqual(candidate.source_url, "https://doi.org/10.1234/record")
        self.assertEqual(candidate.paper, candidate.source_url)
        self.assertEqual(candidate.pdf, "https://example.org/paper.pdf")
        self.assertEqual(candidate.authors, ["Zhuotao Liu"])
        self.assertEqual(candidate.year, 2025)
        record["link"].append({"URL": "https://example.org/another.pdf", "content-type": "application/pdf"})
        candidate, = client.crossref({"title": "A Research Paper"})
        self.assertEqual(candidate.pdf, "")

    def test_arxiv_is_labeled_as_a_preprint_and_not_a_publisher_pdf(self):
        atom = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
          <id>http://arxiv.org/abs/2501.01234v2</id>
          <title>A Research Paper</title><published>2025-01-02T00:00:00Z</published>
          <author><name>Zhuotao Liu</name></author>
          <summary>A useful research abstract is supplied by the preprint archive.</summary>
          <link href="https://arxiv.org/pdf/2501.01234v2" type="application/pdf" />
        </entry></feed>'''
        client = enrich.MetadataClient()
        client.get = lambda _: atom
        candidate, = client.arxiv({"title": "A Research Paper"})
        self.assertEqual(candidate.source_url, "https://arxiv.org/abs/2501.01234")
        self.assertEqual(candidate.preprint, candidate.source_url)
        self.assertEqual(candidate.paper, "")
        self.assertEqual(candidate.pdf, "")
        self.assertEqual(candidate.year, 2025)
        self.assertEqual(candidate.authors, ["Zhuotao Liu"])


class SafeURLTests(unittest.TestCase):
    def test_public_https_url_is_retained(self):
        url = "https://doi.org/10.1234/example?version=1&format=full"
        self.assertEqual(enrich.safe_url(url), url)

    def test_schemes_credentials_private_hosts_and_controls_are_rejected(self):
        unsafe = (
            "http://example.org/paper", "//example.org/paper", "javascript:alert(1)",
            "data:text/html,<script>alert(1)</script>", "file:///tmp/paper.pdf", "ftp://example.org/paper",
            "https://user:password@example.org/paper", "https://localhost/paper", "https://127.0.0.1/paper",
            "https://10.0.0.1/paper", "https://192.168.1.1/paper", "https://169.254.169.254/latest/meta-data",
            "https://[::1]/paper", "https://example.org/paper\nInjected", "https://example.org/paper\r\nInjected",
        )
        for url in unsafe:
            with self.subTest(url=url):
                self.assertEqual(enrich.safe_url(url), "")


if __name__ == "__main__":
    unittest.main()
