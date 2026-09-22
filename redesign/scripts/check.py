#!/usr/bin/env python3
"""Check the preview and editing workflow with Python's standard library."""

import argparse
import csv
from html.parser import HTMLParser
import io
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import unquote, urljoin, urlsplit


RINGSG_TITLE = "RingSG: Optimal Secure Vertex-Centric Computation for Collaborative Graph Processing"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids, self.articles, self.parts = [], set(), [], []
        self.redirects = []
        self.article = None
        self.feed(path.read_text(encoding="utf-8"))
        self.text = "".join(self.parts)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.refs.append(attrs[attr])
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            redirect = re.search(r"(?:^|;)\s*url\s*=\s*(.+)$", attrs.get("content", ""), re.I)
            if redirect:
                target = redirect.group(1).strip().strip("\"'")
                self.redirects.append(target)
                self.refs.append(target)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "name" in attrs:
            self.ids.add(attrs["name"])
        if tag == "article" and "publication" in attrs.get("class", "").split():
            self.article = []

    def handle_endtag(self, tag):
        if tag == "article" and self.article is not None:
            self.articles.append("".join(self.article))
            self.article = None

    def handle_data(self, data):
        self.parts.append(data)
        if self.article is not None:
            self.article.append(data)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def build(hugo, source, output, base, expect_success=True):
    result = subprocess.run(
        [hugo, "--source", str(source), "--destination", str(output),
         "--baseURL", base, "--noBuildLock", "--cacheDir", str(source.parent / "cache")],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60,
    )
    if expect_success:
        require(result.returncode == 0, "Hugo build failed:\n" + result.stdout)
    return result


def check_links(output, base):
    pages = {p.resolve(): Page(p) for p in output.rglob("*.html")}
    origin, prefix = urlsplit(base).netloc, urlsplit(base).path
    checked = 0
    for path, page in pages.items():
        relative = path.relative_to(output).as_posix()
        page_url = urljoin(base, relative.removesuffix("index.html"))
        for ref in page.refs:
            target = urlsplit(urljoin(page_url, ref))
            if target.scheme not in ("http", "https") or target.netloc != origin:
                continue
            pathname = unquote(target.path)
            require(pathname.startswith(prefix), f"{relative}: link escapes preview prefix: {ref}")
            destination = (output / pathname[len(prefix):]).resolve()
            require(destination.is_relative_to(output), f"{relative}: link escapes output: {ref}")
            if destination.is_dir():
                destination /= "index.html"
            require(destination.is_file(), f"{relative}: broken internal link: {ref}")
            if target.fragment and destination.suffix == ".html":
                require(unquote(target.fragment) in pages[destination].ids,
                        f"{relative}: missing fragment: {ref}")
            checked += 1
    require(checked > 0, "No internal links were checked")


def published_papers(hugo, source):
    result = subprocess.run(
        [hugo, "list", "published", "--source", str(source), "--noBuildLock", "--renderToMemory"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
    )
    require(result.returncode == 0, "Could not list published content:\n" + result.stderr)
    records = csv.DictReader(io.StringIO(result.stdout))
    papers = [row for row in records if row["kind"] == "page" and row["section"] == "publications"]
    require(papers, "No published publications found")
    return papers


def check_initial(output, papers):
    home = Page(output / "index.html")
    listing = Page(output / "publications/index.html")
    require(len(listing.articles) == len(papers), "Publication row count does not match published content")
    for paper in papers:
        require(any(paper["title"] in article for article in listing.articles),
                f'Missing {paper["title"]} on the publication listing')
    for article in home.articles:
        require(any(paper["title"] in article for paper in papers), "Homepage contains an unknown paper")
    html = (output / "publications/index.html").read_text(encoding="utf-8")
    years = [int(year) for year in re.findall(r'id="year-(\d{4})"', html)]
    require(years and years == sorted(set(years), reverse=True), "Year groups are not descending")
    ringsg = next((article for article in listing.articles if RINGSG_TITLE in article), "")
    require(re.search(r"Zhuotao Liu\s*†", ringsg), "RingSG lost its corresponding-author marker")
    require("Corresponding author" in ringsg, "RingSG lost its author-note explanation")
    return len(home.articles)


def article_index(page, title):
    return next((index for index, article in enumerate(page.articles) if title in article), None)


def write_paper(entry, minimal, metadata=""):
    frontmatter, body = minimal.rsplit("---", 1)
    entry.write_text(frontmatter + metadata + "---" + body, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hugo", default="hugo", help="Hugo executable (default: hugo)")
    args = parser.parse_args()
    executable = shutil.which(args.hugo)
    require(executable, f"Hugo executable not found: {args.hugo}")
    hugo = str(Path(executable).resolve())
    original = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="personal-site-check-") as directory:
        scratch = Path(directory).resolve()
        source = scratch / "redesign"
        shutil.copytree(original, source, ignore=shutil.ignore_patterns(
            "public", "resources", ".hugo_build.lock", "__pycache__", ".git"))
        papers = published_papers(hugo, source)
        for name, base in (("root", "https://preview.invalid/"),
                           ("prefix", "https://preview.invalid/preview/")):
            output = scratch / name
            build(hugo, source, output, base)
            home_count = check_initial(output, papers)
            check_links(output, base)
            print(f"PASS: {name} build, publication rendering, and internal links")

        title = "Regression fixture: four-field publication"
        entry = source / "content/publications/four-field-check.md"
        minimal = (f'---\ntitle: "{title}"\n'
                   'authors: ["First Author", "Zhuotao Liu"]\n'
                   'venue: "Example Conference"\nyear: 2999\n---\n')
        entry.write_text(minimal, encoding="utf-8")
        output, base = scratch / "minimal", "https://preview.invalid/"
        build(hugo, source, output, base)
        listing = Page(output / "publications/index.html")
        require(len(listing.articles) == len(papers) + 1, "The four-field paper is missing from the listing")
        require(title in listing.articles[0], "Newer four-field paper is not sorted first")
        for value in ("First Author", "Zhuotao Liu", "Example Conference", "2999"):
            require(value in listing.articles[0], f"Four-field paper lost {value}")
        detail = Page(output / "publications/four-field-check/index.html")
        require(title in detail.text, "The four-field paper's page is missing its title")
        require("Abstract" not in listing.articles[0] and "Abstract" not in detail.text,
                "The four-field paper has an abstract link or heading without an abstract")
        require(len(Page(output / "index.html").articles) == home_count,
                "An unselected paper unexpectedly appeared on the homepage")
        check_links(output, base)
        print("PASS: four-field paper builds, sorts first, and needs no optional metadata")

        write_paper(entry, minimal, "selected: true\n")
        output = scratch / "selected"
        build(hugo, source, output, base)
        home, listing = Page(output / "index.html"), Page(output / "publications/index.html")
        require(len(home.articles) == home_count + 1 and article_index(home, title) is not None,
                "selected: true did not add the paper to the homepage")
        require(len(listing.articles) == len(papers) + 1 and article_index(listing, title) is not None,
                "Selecting a paper changed its presence in the complete list")

        write_paper(entry, minimal, "selected: false\n")
        output = scratch / "unselected"
        build(hugo, source, output, base)
        home, listing = Page(output / "index.html"), Page(output / "publications/index.html")
        require(len(home.articles) == home_count and article_index(home, title) is None,
                "selected: false did not remove the paper from the homepage")
        require(len(listing.articles) == len(papers) + 1 and article_index(listing, title) is not None,
                "Deselecting a paper removed it from the complete list")
        print("PASS: selected toggles the homepage while retaining the same complete-list entry")

        write_paper(entry, minimal, "selected: true\nselected_order: 2\n")
        older_title = "Regression fixture: older paper selected first"
        older_entry = source / "content/publications/selection-order-check.md"
        older_minimal = minimal.replace(title, older_title).replace("year: 2999", "year: 1999")
        write_paper(older_entry, older_minimal,
                    "selected: true\nselected_order: 1\naliases: ['/publications/legacy-check/']\n")
        for name, base in (("selection-order", "https://preview.invalid/"),
                           ("selection-order-prefix", "https://preview.invalid/preview/")):
            output = scratch / name
            build(hugo, source, output, base)
            home, listing = Page(output / "index.html"), Page(output / "publications/index.html")
            old_index, new_index = article_index(home, older_title), article_index(home, title)
            require(old_index is not None and new_index is not None and old_index < new_index,
                    "selected_order does not override year order on the homepage")
            require(article_index(listing, title) == 0 and article_index(listing, older_title) > 0,
                    "Homepage selection order changed the complete list's year order")
            alias = Page(output / "publications/legacy-check/index.html")
            require(alias.redirects == [urljoin(base, "publications/selection-order-check/")],
                    "A legacy publication URL does not redirect to the new detail page")
            check_links(output, base)
        print("PASS: custom homepage order, complete-list year sorting, and legacy URL redirects")

        services = source / "data/services.yaml"
        services.write_text(
            'editorial:\n  - years: "2028–present"\n    role: "Fixture Editor"\n'
            '    organization: "Fixture Research Journal"\n'
            'committees:\n  - years: "2029"\n'
            '    venues: ["Fixture Conference A", "Fixture Conference B"]\n',
            encoding="utf-8",
        )
        output, base = scratch / "services", "https://preview.invalid/"
        build(hugo, source, output, base)
        home = Page(output / "index.html")
        require("service" in home.ids, "Academic service is missing its navigation anchor")
        for value in ("Editorial service", "Program committees", "2028–present", "Fixture Editor",
                      "Fixture Research Journal", "2029", "Fixture Conference A", "Fixture Conference B"):
            require(value in home.text, f"A service data edit did not render: {value}")
        check_links(output, base)
        print("PASS: editorial and committee service can be edited in one data file")

        entry.write_text(minimal.replace('venue: "Example Conference"\n', ""), encoding="utf-8")
        result = build(hugo, source, scratch / "invalid", base, expect_success=False)
        require(result.returncode != 0, "Missing venue unexpectedly built successfully")
        require('missing required field "venue"' in result.stdout and "four-field-check.md" in result.stdout,
                "Missing venue did not produce an actionable error:\n" + result.stdout)
        print("PASS: missing venue fails with the filename and required field")
    print("All preview checks passed; the source directory was not modified.")


if __name__ == "__main__":
    main()
