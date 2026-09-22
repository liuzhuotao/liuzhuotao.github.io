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
        self.links, self.images = [], []
        self.anchor = None
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
        if tag == "a":
            self.anchor = [attrs, []]
        if tag == "img":
            self.images.append(attrs)
        if tag == "article" and "publication" in attrs.get("class", "").split():
            self.article = []

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor is not None:
            self.links.append((self.anchor[0], "".join(self.anchor[1])))
            self.anchor = None
        if tag == "article" and self.article is not None:
            self.articles.append("".join(self.article))
            self.article = None

    def handle_data(self, data):
        self.parts.append(data)
        if self.anchor is not None:
            self.anchor[1].append(data)
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
    papers = []
    for row in records:
        if row["kind"] != "page" or row["section"] != "publications":
            continue
        frontmatter = (source / row["path"]).read_text(encoding="utf-8").split("---", 2)[1]
        if not re.search(r'''(?m)^category:\s*["']?patent["']?\s*(?:#.*)?$''', frontmatter):
            papers.append(row)
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
    require(all(year >= 2020 for year in years), "Pre-2020 papers still have individual year groups")
    require("year-before-2020" in listing.ids, "The combined Before 2020 group is missing")
    require("patents" not in listing.ids and not any(ref.endswith("#patents") for ref in listing.refs),
            "A patent section or navigation link remains on the publication listing")
    require("patents or applications" not in listing.text,
            "The publication count still includes patents")
    require(not any("citation_for_view=" in ref for ref in listing.refs),
            "A per-paper Scholar citation link remains on the publication listing")
    ringsg = next((article for article in listing.articles if RINGSG_TITLE in article), "")
    require(re.search(r"Zhuotao Liu\s*†", ringsg), "RingSG lost its corresponding-author marker")
    require("Corresponding author" in ringsg, "RingSG lost its author-note explanation")
    martfl = Page(output / "publications/martfl/index.html")
    qi_links = [attrs for attrs, text in martfl.links
                if text == "Qi Li" and "student-author" in attrs.get("class", "").split()]
    require(len(qi_links) == 1 and qi_links[0]["href"].endswith("/students/qi-li/#publications"),
            "martFL must link only the student Qi Li, not the professor with the same name")
    qi_papers = Page(output / "students/qi-li/index.html")
    require(any("martFL:" in article for article in qi_papers.articles),
            "The student Qi Li's marked martFL authorship is missing from their paper list")
    directory = Page(output / "students/index.html")
    paper_links = [(attrs, text) for attrs, text in directory.links
                   if "student-papers-link" in attrs.get("class", "").split()]
    require(not re.search(r"\b\d+\s+papers?\b", directory.text),
            "A student directory row still displays a numeric paper count")
    for attrs, text in paper_links:
        require("Publications" in text and not re.search(r"\d+\s+papers?", attrs.get("aria-label", "")),
                "A student publication link still uses a numeric paper label")
    for student_page in (output / "students").rglob("*.html"):
        profile = Page(student_page)
        require(not profile.images, f"Student page still contains a portrait: {student_page}")
        if student_page.parent == output / "students":
            continue
        heading = re.search(r'<div class="student-publications-heading">(.*?)</div>',
                            student_page.read_text(encoding="utf-8"), re.S)
        require(heading and not re.search(r"\b\d+\s+papers?\b", heading.group(1)),
                f"A student profile still displays a numeric paper count: {student_page}")
        suffix = "/" + student_page.parent.relative_to(output).as_posix() + "/#publications"
        linked = any(attrs.get("href", "").endswith(suffix) for attrs, _ in paper_links)
        require(linked == bool(profile.articles),
                f"The directory must offer a Publications link only when papers exist: {student_page}")
    return len(home.articles)


def student_group_names(output, group):
    html = (output / "students/index.html").read_text(encoding="utf-8")
    section = re.search(rf'<section[^>]+aria-labelledby="students-{group}">(.*?)</section>', html, re.S)
    require(section, f"Student group is missing: {group}")
    return re.findall(r'<h3><a[^>]*>([^<]+)</a></h3>', section.group(1))


def student_publication_links(output, slug):
    directory = Page(output / "students/index.html")
    return [(attrs, text) for attrs, text in directory.links
            if "student-papers-link" in attrs.get("class", "").split()
            and attrs.get("href", "").endswith(f"/students/{slug}/#publications")]


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
            listing_html = (output / "publications/index.html").read_text(encoding="utf-8")
            require(older_title in listing_html.split('id="year-before-2020"', 1)[1]
                    and 'id="year-1999"' not in listing_html and '#year-1999' not in listing_html,
                    "An older paper did not join the single Before 2020 group")
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

        student_name = "Fixture Student"
        student = source / "content/students/fixture-student/index.md"
        student.parent.mkdir()
        student_minimal = f'---\ntitle: "{student_name}"\ngroup: master\n---\n'
        student.write_text(student_minimal, encoding="utf-8")
        for slug, name, group, since in (
            ("fixture-newest", "Zebra Newest Fixture", "master", 3001),
            ("fixture-tie-zeta", "Zeta Tie Fixture", "master", 3000),
            ("fixture-tie-alpha", "Alpha Tie Fixture", "master", 3000),
            ("fixture-postdoc", "Fixture Postdoc", "postdoc", 3002),
        ):
            (source / f"content/students/{slug}.md").write_text(
                f'---\ntitle: "{name}"\ngroup: {group}\nsince: {since}\n---\n', encoding="utf-8")
        output, base = scratch / "student-minimal", "https://preview.invalid/"
        build(hugo, source, output, base)
        directory_html = (output / "students/index.html").read_text(encoding="utf-8")
        masters = re.search(r'<section[^>]+aria-labelledby="students-master">(.*?)</section>',
                            directory_html, re.S)
        require(masters and student_name in masters.group(1),
                "A two-field student is missing from the master's group")
        profile = Page(output / "students/fixture-student/index.html")
        require(student_name in profile.text and not profile.articles,
                "A two-field student did not receive an empty publication page")
        require("Publications will appear here" in profile.text,
                "A student without publications has no explanation")
        require(not student_publication_links(output, "fixture-student"),
                "A student without papers has an empty Publications link on the directory")
        master_names = student_group_names(output, "master")
        require(master_names[:3] == ["Zebra Newest Fixture", "Alpha Tie Fixture", "Zeta Tie Fixture"]
                and master_names[-1] == student_name,
                "Students must sort by newest enrollment first, alphabetical ties, and missing year last")
        require("Fixture Postdoc" in student_group_names(output, "postdoc"),
                "The postdoc group did not accept a new member")
        postdoc = Page(output / "students/fixture-postdoc/index.html")
        require("Postdoctoral researcher" in postdoc.text and "3002" in postdoc.text,
                "A postdoc profile lost its role or enrollment year")
        check_links(output, base)
        print("PASS: enrollment order, alphabetical ties, missing years, and the postdoc group")

        write_paper(entry, minimal.replace("First Author", student_name))
        output = scratch / "student-paper"
        build(hugo, source, output, base)
        profile = Page(output / "students/fixture-student/index.html")
        require(len(profile.articles) == 1 and title in profile.articles[0],
                "Adding a matching publication did not automatically update the student's paper list")
        paper_links = student_publication_links(output, "fixture-student")
        require(len(paper_links) == 1 and "Publications" in paper_links[0][1]
                and not re.search(r"\d+\s+papers?", paper_links[0][1]),
                "Adding a paper did not reveal a plain Publications link in the directory")
        detail = Page(output / "publications/four-field-check/index.html")
        require(any(text == student_name and attrs.get("href") == "/students/fixture-student/#publications"
                    for attrs, text in detail.links),
                "The publication author does not link to the student's papers")
        check_links(output, base)
        print("PASS: two-field students, automatic paper lists, and conditional Publications links")

        student.write_text(
            student_minimal.replace("group: master", 'group: alumni\nauthor_names: ["Fixture Author"]\n'
                                    'aliases: ["/authors/fixture-student/"]'),
            encoding="utf-8",
        )
        write_paper(entry, minimal.replace("First Author", "Fixture Author"))
        write_paper(older_entry, older_minimal.replace("First Author", "Qi Li"),
                    "aliases: ['/publications/legacy-check/']\n")
        output, base = scratch / "student-prefix", "https://preview.invalid/preview/"
        build(hugo, source, output, base)
        directory_html = (output / "students/index.html").read_text(encoding="utf-8")
        alumni = re.search(r'<section[^>]+aria-labelledby="students-alumni">(.*?)</section>',
                           directory_html, re.S)
        masters = re.search(r'<section[^>]+aria-labelledby="students-master">(.*?)</section>',
                            directory_html, re.S)
        require(alumni and student_name in alumni.group(1)
                and (not masters or student_name not in masters.group(1)),
                "Changing group to alumni did not move the student between groups")
        profile = Page(output / "students/fixture-student/index.html")
        require(len(profile.articles) == 1 and title in profile.articles[0],
                "An alternate author spelling did not match the student's paper")
        detail = Page(output / "publications/four-field-check/index.html")
        require(any(text == "Fixture Author"
                    and attrs.get("href") == "/preview/students/fixture-student/#publications"
                    for attrs, text in detail.links),
                "An alternate author name does not link to the student's papers under a preview prefix")
        alias = Page(output / "authors/fixture-student/index.html")
        require(alias.redirects == [urljoin(base, "students/fixture-student/")],
                "A legacy student URL does not redirect to the new profile")
        qi_papers = Page(output / "students/qi-li/index.html")
        require(article_index(qi_papers, older_title) is None,
                "An unmarked author with the ambiguous name Qi Li was assigned to the student")
        unrelated = Page(output / "publications/selection-order-check/index.html")
        require(not any(text == "Qi Li" and "student-author" in attrs.get("class", "").split()
                        for attrs, text in unrelated.links),
                "An unmarked Qi Li author occurrence incorrectly links to the student")
        check_links(output, base)
        print("PASS: student groups, alternate author names, legacy URLs, prefixes, and ambiguous names")

        write_paper(entry, minimal,
                    'selected: true\n'
                    'scholar: "https://scholar.google.com/citations?user=fixture"\n'
                    'versions: [{label: "Fixture version", url: "/publications/ringsg/"}]\n')
        output, base = scratch / "versions", "https://preview.invalid/preview/"
        build(hugo, source, output, base)
        html = (output / "publications/index.html").read_text(encoding="utf-8")
        listing = Page(output / "publications/index.html")
        home = Page(output / "index.html")
        require(article_index(listing, title) is not None and article_index(home, title) is not None,
                "The ordinary version fixture is missing from the complete list or selected papers")
        require('https://scholar.google.com/citations?user=fixture' not in listing.refs
                and 'https://scholar.google.com/citations?user=fixture' not in home.refs
                and 'https://scholar.google.com/citations?user=fixture'
                not in Page(output / "publications/four-field-check/index.html").refs,
                "A per-paper Scholar link was rendered from retained source metadata")
        require('href="/preview/publications/ringsg/">Fixture version' in html,
                "The optional version link does not honor the preview prefix")
        require(len(listing.articles) == len(papers) + 2,
                "Adding alternate versions lost or duplicated a publication row")
        check_links(output, base)
        print("PASS: hidden per-paper Scholar links and prefix-safe alternate versions")

        write_paper(entry, minimal,
                    'category: patent\ndraft: false\nselected: true\nselected_order: 1\n')
        output = scratch / "patents"
        build(hugo, source, output, base)
        html = (output / "publications/index.html").read_text(encoding="utf-8")
        listing, home = Page(output / "publications/index.html"), Page(output / "index.html")
        require("patents" not in listing.ids and not any(ref.endswith("#patents") for ref in listing.refs)
                and "patents or applications" not in listing.text,
                "A patent section, navigation item, or count was added to the research listing")
        require(article_index(listing, title) is None and article_index(home, title) is None,
                "A non-draft patent appeared in the complete list or selected homepage papers")
        require('id="year-2999"' not in html and '#year-2999' not in html,
                "A patent year leaked into the research year navigation")
        require(len(listing.articles) == len(papers) + 1 and len(home.articles) == home_count,
                "Excluding the patent changed the remaining research paper counts")
        check_links(output, base)
        print("PASS: patents stay out of the publication list and homepage even when selected and non-draft")

        student.write_text(student_minimal.replace("group: master", "group: unknown"), encoding="utf-8")
        result = build(hugo, source, scratch / "student-invalid", base, expect_success=False)
        require(result.returncode != 0, "An invalid student group unexpectedly built successfully")
        require("group must be postdoc, phd, master, or alumni" in result.stdout
                and "fixture-student/index.md" in result.stdout,
                "An invalid student group did not produce an actionable error:\n" + result.stdout)
        student.write_text(student_minimal, encoding="utf-8")
        print("PASS: an invalid student group reports the filename and allowed values")

        entry.write_text(minimal.replace('venue: "Example Conference"\n', ""), encoding="utf-8")
        result = build(hugo, source, scratch / "invalid", base, expect_success=False)
        require(result.returncode != 0, "Missing venue unexpectedly built successfully")
        require('missing required field "venue"' in result.stdout and "four-field-check.md" in result.stdout,
                "Missing venue did not produce an actionable error:\n" + result.stdout)
        print("PASS: missing venue fails with the filename and required field")
    print("All preview checks passed; the source directory was not modified.")


if __name__ == "__main__":
    main()
