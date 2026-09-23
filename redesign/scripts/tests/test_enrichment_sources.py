"""Source and retry regressions for automatic publication enrichment."""

from copy import deepcopy
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.parse import parse_qs, unquote, urlsplit


SCRIPT = Path(__file__).resolve().parents[1] / "enrich_publications.py"
SPEC = importlib.util.spec_from_file_location("enrichment_sources_under_test", SCRIPT)
enrich = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = enrich
SPEC.loader.exec_module(enrich)


class OpenAlexSourceTests(unittest.TestCase):
    def setUp(self):
        self.metadata = {
            "title": "Secure Networks: An Exact Analysis",
            "authors": ["Zhuotao Liu", "First Author"],
            "year": 2026,
            "venue": "ACM CCS",
        }
        self.record = {
            "id": "https://openalex.org/W12345",
            "doi": "https://doi.org/10.1234/secure-networks",
            "display_name": self.metadata["title"],
            "publication_year": 2026,
            "type": "article",
            "authorships": [{"author": {"display_name": name}}
                            for name in self.metadata["authors"]],
            "abstract_inverted_index": {
                "systems.": [9], "secure": [8], "We": [0], "and": [3],
                "prove": [1], "x<y": [2], "y>z": [4], "for": [5],
                "all": [6], "networked": [7],
            },
            "primary_location": {
                "landing_page_url": "https://publisher.example/article/secure-networks",
            },
            "best_oa_location": {
                "version": "publishedVersion",
                "landing_page_url": "https://publisher.example/article/secure-networks",
                "pdf_url": "https://publisher.example/article/secure-networks.pdf",
            },
            "content_urls": {"pdf": "https://content.openalex.org/works/W12345.pdf"},
        }
        self.urls = []

    def client(self, payload):
        client = enrich.MetadataClient()

        def get(url):
            self.urls.append(url)
            return json.dumps(payload).encode()

        client.get = get
        return client

    def parse(self, record=None):
        return self.client({"results": [record or self.record]}).openalex(self.metadata)[0]

    def test_search_uses_title_without_credentials_and_retains_full_authors(self):
        candidate = self.parse()
        query = parse_qs(urlsplit(self.urls[0]).query)
        self.assertEqual(query["search"], [self.metadata["title"]])
        self.assertEqual(query["per-page"], ["5"])
        self.assertNotIn("api_key", query)
        self.assertEqual(candidate.authors, self.metadata["authors"])
        self.assertEqual(enrich.choose_candidate(self.metadata, [candidate]), candidate)
        wrong_authors = replace(candidate, authors=["Zhuotao Liu", "Another Author"])
        self.assertIsNone(enrich.choose_candidate(self.metadata, [wrong_authors]))

    def test_known_doi_uses_direct_lookup(self):
        metadata = dict(self.metadata, paper=self.record["doi"])
        candidate, = self.client(self.record).openalex(metadata)
        self.assertEqual(unquote(self.urls[0]),
                         "https://api.openalex.org/works/" + self.record["doi"])
        self.assertEqual(candidate.paper, self.record["doi"])
        self.assertEqual(candidate.source_url, self.record["id"])

    def test_abstract_order_and_math_are_preserved_as_plain_text(self):
        candidate = self.parse()
        self.assertEqual(candidate.abstract,
                         "We prove x<y and y>z for all networked secure systems.")
        self.assertFalse(candidate.abstract_is_html)
        cleaned = enrich.clean_abstract(candidate.abstract, is_html=candidate.abstract_is_html)
        self.assertEqual(cleaned,
                         "We prove x&lt;y and y&gt;z for all networked secure systems.")

    def test_only_public_published_version_pdf_is_used(self):
        candidate = self.parse()
        self.assertEqual(candidate.pdf, self.record["best_oa_location"]["pdf_url"])
        self.assertNotEqual(candidate.pdf, self.record["content_urls"]["pdf"])
        for version, pdf in (
            ("acceptedVersion", "https://repository.example/accepted.pdf"),
            ("submittedVersion", "https://repository.example/preprint.pdf"),
            ("publishedVersion", "https://content.openalex.org/works/W12345.pdf"),
            ("publishedVersion", "https://arxiv.org/pdf/2601.01234"),
            ("publishedVersion", "http://publisher.example/article.pdf"),
            ("publishedVersion", "https://127.0.0.1/private.pdf"),
        ):
            with self.subTest(version=version, pdf=pdf):
                record = deepcopy(self.record)
                record["best_oa_location"].update(version=version, pdf_url=pdf)
                self.assertEqual(self.parse(record).pdf, "")

    def test_preprint_is_not_labeled_as_published_paper_or_pdf(self):
        record = deepcopy(self.record)
        record["type"] = "preprint"
        record["primary_location"]["landing_page_url"] = "https://arxiv.org/abs/2601.01234"
        record["best_oa_location"] = {
            "version": "publishedVersion",
            "landing_page_url": "https://arxiv.org/abs/2601.01234",
            "pdf_url": "https://arxiv.org/pdf/2601.01234",
        }
        candidate = self.parse(record)
        self.assertEqual(candidate.paper, "")
        self.assertEqual(candidate.pdf, "")
        self.assertEqual(candidate.preprint, "https://arxiv.org/abs/2601.01234")

    def test_publisher_record_can_expose_separately_labeled_arxiv_preprint(self):
        record = deepcopy(self.record)
        record["best_oa_location"] = {
            "version": "submittedVersion",
            "landing_page_url": "https://arxiv.org/abs/2601.01234",
            "pdf_url": "https://arxiv.org/pdf/2601.01234",
        }
        candidate = self.parse(record)
        self.assertEqual(candidate.paper, self.record["doi"])
        self.assertEqual(candidate.preprint, "https://arxiv.org/abs/2601.01234")
        self.assertEqual(candidate.pdf, "")

    def test_empty_results_and_missing_abstract_are_valid(self):
        self.assertEqual(self.client({"results": []}).openalex(self.metadata), [])
        record = deepcopy(self.record)
        record["abstract_inverted_index"] = None
        self.assertEqual(self.parse(record).abstract, "")

    def test_malformed_abstract_positions_are_rejected(self):
        for index in ({"a": [0], "b": [0]}, {"a": [-1]}, {"a": [True]},
                      {"a": [10000]}, {"a": "0"}, {"a": ["0"]}):
            with self.subTest(index=index):
                record = deepcopy(self.record)
                record["abstract_inverted_index"] = index
                with self.assertRaises(ValueError):
                    self.parse(record)

    def test_unverified_source_is_rejected(self):
        record = deepcopy(self.record)
        record["id"] = "https://example.org/W12345"
        self.assertEqual(self.client({"results": [record]}).openalex(self.metadata), [])


class SourceLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "secure-networks.md"
        self.metadata = {
            "title": "Secure Networks: An Exact Analysis",
            "authors": ["Zhuotao Liu", "First Author"],
            "year": 2026,
            "venue": "ACM CCS",
            "paper": "https://doi.org/10.1234/secure-networks",
        }

    def write_publication(self, extra="", body=""):
        self.path.write_text(
            '---\ntitle: "Secure Networks: An Exact Analysis"\n'
            'authors: ["Zhuotao Liu", "First Author"]\nyear: 2026\nvenue: "ACM CCS"\n'
            'paper: "https://doi.org/10.1234/secure-networks"\n'
            'preprint: "https://arxiv.org/abs/2601.01234"\nauto_enrich: true\n'
            + extra + '---\n' + body, encoding="utf-8")
        return enrich.load_publication(self.path)

    def test_later_publisher_pdf_is_added_after_abstract_paper_and_preprint(self):
        original = self.write_publication(body="\nThe author's original **abstract** stays exactly the same.\n")
        self.assertTrue(enrich.eligible(original))
        candidate = enrich.Candidate(
            title=self.metadata["title"], authors=self.metadata["authors"], year=2026,
            source_url=self.metadata["paper"], paper=self.metadata["paper"],
            pdf="https://publisher.example/final.pdf", abstract="An alternative publisher abstract that must not replace the user's words.")
        calls = []

        class Client:
            def crossref(self, metadata):
                calls.append("crossref")
                return [candidate]

            def arxiv(self, metadata):
                raise AssertionError("A present preprint and abstract do not need another arXiv lookup")

        report = enrich.run(Path(self.directory.name), Client(), write=True)
        updated = enrich.load_publication(self.path)
        self.assertEqual(calls, ["crossref"])
        self.assertEqual(updated.metadata["pdf"], candidate.pdf)
        self.assertEqual(updated.metadata["preprint"], original.metadata["preprint"])
        self.assertEqual(updated.body, original.body)
        self.assertEqual(len(report["changed"]), 1)
        self.assertFalse(enrich.eligible(updated))

    def test_explicit_empty_pdf_and_opt_out_stop_tracking_complete_entry(self):
        publication = self.write_publication(extra="pdf: null\n", body="\nA manually supplied complete abstract.\n")
        self.assertFalse(enrich.eligible(publication))
        publication.metadata.pop("pdf")
        publication.metadata["auto_enrich"] = False
        self.assertFalse(enrich.eligible(publication))

    def test_different_doi_cannot_supply_details_to_known_paper(self):
        candidate = enrich.Candidate(
            title=self.metadata["title"], authors=self.metadata["authors"], year=2026,
            source_url="https://openalex.org/W12345", paper="https://doi.org/10.1234/other-version")
        self.assertIsNone(enrich.choose_candidate(self.metadata, [candidate]))
        correct = replace(candidate, paper=self.metadata["paper"])
        self.assertEqual(enrich.choose_candidate(self.metadata, [correct]), correct)

    def test_crossref_uses_existing_doi_instead_of_title_search(self):
        client = enrich.MetadataClient()
        urls = []
        item = {
            "DOI": "10.1234/secure-networks",
            "title": [self.metadata["title"]],
            "author": [{"given": "Zhuotao", "family": "Liu"}, {"given": "First", "family": "Author"}],
            "published": {"date-parts": [[2026]]},
        }

        def get(url):
            urls.append(url)
            return json.dumps({"message": item}).encode()

        client.get = get
        candidate, = client.crossref(self.metadata)
        request = urlsplit(unquote(urls[0]))
        self.assertEqual(request.path, "/works/10.1234/secure-networks")
        self.assertNotIn("query.bibliographic", parse_qs(request.query))
        self.assertEqual(candidate.paper, self.metadata["paper"])

    def test_arxiv_plain_math_and_untrusted_markup_remain_inert_text(self):
        feed = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
          <id>http://arxiv.org/abs/2601.01234v2</id><title>Secure Networks: An Exact Analysis</title>
          <published>2026-01-02T00:00:00Z</published>
          <author><name>Zhuotao Liu</name></author><author><name>First Author</name></author>
          <summary>We prove x&lt;y and y&gt;z for all networked secure systems. {{&lt; bad &gt;}} &lt;script&gt;bad()&lt;/script&gt;</summary>
        </entry></feed>'''
        client = enrich.MetadataClient()
        client.get = lambda url: feed
        candidate, = client.arxiv(self.metadata)
        self.assertFalse(candidate.abstract_is_html)
        publication = self.write_publication()
        updated = enrich.apply_candidate(publication, candidate)
        self.assertIn("x&lt;y and y&gt;z", updated)
        self.assertNotIn("{{<", updated)
        self.assertNotIn("<script>", updated)
        self.assertIn("&lt;script&gt;", updated)


if __name__ == "__main__":
    unittest.main()
