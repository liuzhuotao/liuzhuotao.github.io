#!/usr/bin/env python3
"""Check site builds, deployment artifacts, and the editing workflow using the standard library."""

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
import xml.etree.ElementTree as ET

from publication_files import validate_publication_files


RINGSG_TITLE = "RingSG: Optimal Secure Vertex-Centric Computation for Collaborative Graph Processing"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids, self.articles, self.parts = [], set(), [], []
        self.links, self.images = [], []
        self.id_order, self.robot_directives, self.canonicals = [], [], []
        self.classes = set()
        self.anchor = None
        self.redirects = []
        self.article = None
        self.news_items, self.news_item = [], None
        self.section_stack, self.publication_groups = [], {}
        self.feed(path.read_text(encoding="utf-8"))
        self.text = "".join(self.parts)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.classes.update(attrs.get("class", "").split())
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.refs.append(attrs[attr])
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            redirect = re.search(r"(?:^|;)\s*url\s*=\s*(.+)$", attrs.get("content", ""), re.I)
            if redirect:
                target = redirect.group(1).strip().strip("\"'")
                self.redirects.append(target)
                self.refs.append(target)
        if tag == "meta" and attrs.get("name", "").lower() in ("robots", "googlebot"):
            self.robot_directives.extend(re.split(r"[,\s]+", attrs.get("content", "").lower()))
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append(attrs.get("href", ""))
        if "id" in attrs:
            self.ids.add(attrs["id"])
            self.id_order.append(attrs["id"])
        if tag == "a" and "name" in attrs:
            self.ids.add(attrs["name"])
        if tag == "a":
            self.anchor = [attrs, []]
        if tag == "img":
            self.images.append(attrs)
        if tag == "section":
            self.section_stack.append(attrs.get("aria-labelledby", ""))
        if tag == "article" and "publication" in attrs.get("class", "").split():
            self.article = []
        if tag == "time" and "news-date" in attrs.get("class", "").split():
            self.news_item = [attrs.get("datetime", ""), []]

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor is not None:
            self.links.append((self.anchor[0], "".join(self.anchor[1])))
            self.anchor = None
        if tag == "article" and self.article is not None:
            article = "".join(self.article)
            self.articles.append(article)
            if self.section_stack:
                self.publication_groups.setdefault(self.section_stack[-1], []).append(article)
            self.article = None
        if tag == "section" and self.section_stack:
            self.section_stack.pop()
        if tag == "li" and self.news_item is not None:
            self.news_items.append((self.news_item[0], normalized_text("".join(self.news_item[1]))))
            self.news_item = None

    def handle_data(self, data):
        self.parts.append(data)
        if self.anchor is not None:
            self.anchor[1].append(data)
        if self.article is not None:
            self.article.append(data)
        if self.news_item is not None:
            self.news_item[1].append(data)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def normalized_text(value):
    return re.sub(r"\s+", " ", value).strip()


def build(hugo, source, output, base, expect_success=True, environment="production"):
    result = subprocess.run(
        [hugo, "--source", str(source), "--destination", str(output),
         "--baseURL", base, "--environment", environment,
         "--noBuildLock", "--cacheDir", str(source.parent / "cache")],
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


def check_indexing(output, base, environment):
    preview = environment == "preview"
    for path in output.rglob("*.html"):
        page = Page(path)
        if page.redirects or path.name == "404.html":
            continue
        relative = path.relative_to(output).as_posix()
        if preview:
            require("noindex" in page.robot_directives and "nofollow" in page.robot_directives,
                    f"Preview page is missing noindex, nofollow: {relative}")
            require("preview-banner" in page.classes, f"Preview page is not labeled as a preview: {relative}")
        else:
            require(not {"noindex", "nofollow", "none"}.intersection(page.robot_directives),
                    f"Production page is still blocked from indexing: {relative}")
            require("preview-banner" not in page.classes, f"Production page still has a preview banner: {relative}")
            expected = urljoin(base, relative.removesuffix("index.html"))
            require(page.canonicals == [expected], f"Production page has an incorrect canonical URL: {relative}")
    robots = output / "robots.txt"
    require(robots.is_file(), "robots.txt is missing")
    blocked = re.search(r"(?mi)^Disallow:\s*/\s*(?:#.*)?$", robots.read_text(encoding="utf-8"))
    require(bool(blocked) == preview, "robots.txt does not match the requested production/preview environment")
    if not preview:
        sitemap = output / "sitemap.xml"
        require(sitemap.is_file(), "Production sitemap.xml is missing")
        locations = [node.text for node in ET.parse(sitemap).iter() if node.tag.rsplit("}", 1)[-1] == "loc"]
        require(base in locations and all(location and location.startswith(base) for location in locations),
                "The production sitemap is empty or contains URLs outside the deployed site")
        require(urljoin(base, "sitemap.xml") in robots.read_text(encoding="utf-8"),
                "Production robots.txt does not advertise the sitemap")


def published_papers(hugo, source):
    validate_publication_files(source / "content/publications")
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
            year = re.search(r'''(?m)^year:\s*["']?(\d{4})["']?\s*(?:#.*)?$''', frontmatter)
            require(year, f'Publication has no valid year: {row["path"]}')
            row["year"] = int(year.group(1))
            papers.append(row)
    require(papers, "No published publications found")
    return papers


def check_initial(output, papers):
    home = Page(output / "index.html")
    listing = Page(output / "publications/index.html")
    require(len(listing.articles) == len(papers), "Publication row count does not match published content")
    for paper in papers:
        require(any(normalized_text(paper["title"]) in normalized_text(article) for article in listing.articles),
                f'Missing {paper["title"]} on the publication listing')
    for article in home.articles:
        require(any(normalized_text(paper["title"]) in normalized_text(article) for paper in papers),
                "Homepage contains an unknown paper")
    selected_years = [next(paper["year"] for paper in papers
                           if normalized_text(paper["title"]) in normalized_text(article))
                      for article in home.articles]
    require(selected_years == sorted(selected_years, reverse=True),
            "Selected publications are not shown newest first")
    years = [int(identifier.removeprefix("year-")) for identifier in listing.id_order
             if re.fullmatch(r"year-\d{4}", identifier)]
    require(years and years == sorted(set(years), reverse=True), "Year groups are not descending")
    require(all(year >= 2021 for year in years), "Pre-2021 papers still have individual year groups")
    require("year-before-2021" in listing.ids, "The combined Before 2021 group is missing")
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
        heading = re.search(r'<div class=(?:"student-publications-heading"|student-publications-heading)>(.*?)</div>',
                            student_page.read_text(encoding="utf-8"), re.S)
        require(heading and not re.search(r"\b\d+\s+papers?\b", heading.group(1)),
                f"A student profile still displays a numeric paper count: {student_page}")
        suffix = "/" + student_page.parent.relative_to(output).as_posix() + "/#publications"
        linked = any(attrs.get("href", "").endswith(suffix) for attrs, _ in paper_links)
        require(linked == bool(profile.articles),
                f"The directory must offer a Publications link only when papers exist: {student_page}")
    news = Page(output / "news/index.html")
    require(news.news_items, "The complete news archive is missing its entries")
    dates = [date for date, _ in news.news_items]
    require(dates == sorted(dates, reverse=True), "The news archive is not newest first")
    require(home.news_items == news.news_items[:6],
            "The homepage does not show the six most recent archive entries")
    require(any(urlsplit(ref).path.endswith("/news/") for ref in home.refs),
            "The homepage has no link to the complete news archive")
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
    return next((index for index, article in enumerate(page.articles)
                 if normalized_text(title) in normalized_text(article)), None)


def write_paper(entry, minimal, metadata=""):
    frontmatter, body = minimal.rsplit("---", 1)
    entry.write_text(frontmatter + metadata + "---" + body, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hugo", default="hugo", help="Hugo executable (default: hugo)")
    parser.add_argument("--output", type=Path, help="Validate an existing build without changing or rebuilding it")
    parser.add_argument("--base-url", help="Exact deployed site URL, including a trailing slash (required with --output)")
    parser.add_argument("--environment", choices=("production", "preview"), default="production",
                        help="Environment of an existing --output build (default: production)")
    args = parser.parse_args()
    if bool(args.output) != bool(args.base_url):
        parser.error("--output and --base-url must be supplied together")
    if args.base_url:
        address = urlsplit(args.base_url)
        if address.scheme not in ("http", "https") or not address.netloc or not address.path.endswith("/") \
                or address.query or address.fragment:
            parser.error("--base-url must be an absolute http(s) URL ending in /, without a query or fragment")
    executable = shutil.which(args.hugo)
    require(executable, f"Hugo executable not found: {args.hugo}")
    hugo = str(Path(executable).resolve())
    original = Path(__file__).resolve().parents[1]
    if args.output:
        output = args.output.resolve()
        require(output.is_dir(), f"Build output does not exist: {output}")
        check_initial(output, published_papers(hugo, original))
        check_links(output, args.base_url)
        check_indexing(output, args.base_url, args.environment)
        print(f"PASS: existing {args.environment} artifact, publications, internal links, and indexing settings")
        return
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
            check_indexing(output, base, "production")
            print(f"PASS: {name} production build, publication rendering, internal links, and indexing")

        output, base = scratch / "explicit-preview", "https://preview.invalid/preview/"
        build(hugo, source, output, base, environment="preview")
        check_initial(output, papers)
        check_links(output, base)
        check_indexing(output, base, "preview")
        print("PASS: explicit preview build is labeled, noindex/nofollow, and prefix-safe")

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

        write_paper(entry, minimal, 'preprint: "https://arxiv.org/abs/2601.01234"\nauto_enrich: true\n')
        output = scratch / "enriched-links"
        build(hugo, source, output, base)
        for relative in ("publications/index.html", "publications/four-field-check/index.html"):
            page = Page(output / relative)
            require(any(attrs.get("href") == "https://arxiv.org/abs/2601.01234" and "Preprint" in text
                        for attrs, text in page.links), "The preprint is missing or not labeled as a preprint")
        write_paper(entry, minimal, 'auto_enrich: "false"\n')
        invalid = build(hugo, source, scratch / "invalid-auto-enrich", base, expect_success=False)
        require(invalid.returncode != 0 and "auto_enrich must be true or false" in invalid.stdout
                and "four-field-check.md" in invalid.stdout,
                "A quoted enrichment setting does not report its filename and expected type")
        entry.write_text(minimal, encoding="utf-8")
        print("PASS: enrichment preprints are labeled and the per-paper setting requires a boolean")

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

        many_selected = []
        for index in range(10):
            selected_title = f"Unlimited selection fixture {index + 1:02d}"
            selected_entry = source / f"content/publications/unlimited-selection-{index + 1:02d}.md"
            year = 1900 + index if index < 5 else 2800 + index
            selected_minimal = minimal.replace(title, selected_title).replace("year: 2999", f"year: {year}")
            write_paper(selected_entry, selected_minimal, "selected: true\n")
            many_selected.append((selected_entry, selected_title, selected_minimal, year))
        output = scratch / "unlimited-selected"
        build(hugo, source, output, base)
        home, listing = Page(output / "index.html"), Page(output / "publications/index.html")
        require(len(home.articles) == home_count + len(many_selected),
                "The homepage caps or duplicates selected publications")
        for _, selected_title, _, _ in many_selected:
            require(sum(selected_title in article for article in home.articles) == 1,
                    f"A selected publication did not render exactly once: {selected_title}")
            require(article_index(listing, selected_title) is not None,
                    f"Selecting many papers lost a complete-list entry: {selected_title}")
        expected = [fixture[1] for fixture in sorted(many_selected, key=lambda fixture: fixture[3], reverse=True)]
        positions = [article_index(home, selected_title) for selected_title in expected]
        require(positions == sorted(positions),
                "Selected papers are not sorted newest first across the complete uncapped list")
        archive_titles = [paper[1] for paper in many_selected]
        for selected_entry, _, selected_minimal, _ in (many_selected[0], many_selected[-1]):
            write_paper(selected_entry, selected_minimal, "selected: false\n")
        output = scratch / "unlimited-deselected"
        build(hugo, source, output, base)
        home, listing = Page(output / "index.html"), Page(output / "publications/index.html")
        require(len(home.articles) == home_count + len(many_selected) - 2
                and article_index(home, many_selected[0][1]) is None
                and article_index(home, many_selected[-1][1]) is None,
                "Deselecting newer and older entries did not update the uncapped homepage list")
        require(len(listing.articles) == len(papers) + len(many_selected) + 1
                and all(article_index(listing, selected_title) is not None for selected_title in archive_titles),
                "Deselecting from a large homepage list changed the complete publication archive")
        check_links(output, base)
        for selected_entry, _, _, _ in many_selected:
            selected_entry.unlink()
        print("PASS: ten selected papers render newest first without a cap and remain in the archive when deselected")

        write_paper(entry, minimal, "selected: true\nselected_order: 2\n")
        older_title = "Regression fixture: older selected paper"
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
            require(old_index is not None and new_index is not None and new_index < old_index,
                    "A legacy selected_order field incorrectly overrides newest-first homepage sorting")
            require(article_index(listing, title) == 0 and article_index(listing, older_title) > 0,
                    "Legacy selection metadata changed the complete list's year order")
            listing_html = (output / "publications/index.html").read_text(encoding="utf-8")
            require(older_title in listing_html.split('id="year-before-2021"', 1)[1]
                    and 'id="year-1999"' not in listing_html and '#year-1999' not in listing_html,
                    "An older paper did not join the single Before 2021 group")
            alias = Page(output / "publications/legacy-check/index.html")
            require(alias.redirects == [urljoin(base, "publications/selection-order-check/")],
                    "A legacy publication URL does not redirect to the new detail page")
            check_links(output, base)
        print("PASS: selected papers ignore legacy manual order, both lists stay newest first, and old URLs redirect")

        boundary_student = source / "content/students/boundary-author.md"
        boundary_student.write_text('---\ntitle: "Boundary Author"\ngroup: master\n---\n', encoding="utf-8")
        boundary_entries = []
        for year in (2020, 2021):
            boundary_title = f"Regression fixture: publication grouping boundary {year}"
            boundary_entry = source / f"content/publications/boundary-{year}.md"
            boundary_entry.write_text(minimal.replace(title, boundary_title)
                                      .replace("First Author", "Boundary Author")
                                      .replace("year: 2999", f"year: {year}"), encoding="utf-8")
            boundary_entries.append((boundary_entry, boundary_title))
        for name, base in (("boundary", "https://preview.invalid/"),
                           ("boundary-prefix", "https://preview.invalid/preview/")):
            output = scratch / name
            build(hugo, source, output, base)
            for relative in ("publications/index.html", "students/boundary-author/index.html"):
                page = Page(output / relative)
                old_group = page.publication_groups.get("year-before-2021", [])
                recent_group = page.publication_groups.get("year-2021", [])
                require(any(boundary_entries[0][1] in article for article in old_group)
                        and not any(boundary_entries[1][1] in article for article in old_group),
                        f"{relative}: the combined earlier group must include 2020 but exclude 2021")
                require(any(boundary_entries[1][1] in article for article in recent_group)
                        and not any(boundary_entries[0][1] in article for article in recent_group),
                        f"{relative}: 2021 must retain its separate year group")
                require("year-2020" not in page.ids
                        and not any(ref.endswith("#year-2020") for ref in page.refs),
                        f"{relative}: 2020 still has its own year section or navigation item")
            check_links(output, base)
        for boundary_entry, _ in boundary_entries:
            boundary_entry.unlink()
        boundary_student.unlink()
        print("PASS: 2020 joins the earlier group and 2021 stays separate in full and student lists at root and prefix URLs")

        news = source / "data/news.yaml"
        original_news = news.read_text(encoding="utf-8")
        news_entries = [(date, f"Unsorted news fixture {index + 1:02d}") for index, date in enumerate(
            ("2024-03", "2027-10", "2025-06", "2026-02", "2027-01", "2024-12", "2026-09", "2025-11"))]

        def write_news(entries):
            news.write_text("".join(f'- date: "{date}"\n  text: "{text}"\n' for date, text in entries),
                            encoding="utf-8")

        write_news(news_entries)
        output, base = scratch / "news-unsorted", "https://preview.invalid/preview/"
        build(hugo, source, output, base)
        home, archive = Page(output / "index.html"), Page(output / "news/index.html")
        expected_news = sorted(news_entries, reverse=True)
        require([date for date, _ in home.news_items] == [date for date, _ in expected_news[:6]],
                "The homepage did not select exactly the six newest dates from unsorted news")
        require([date for date, _ in archive.news_items] == [date for date, _ in expected_news],
                "The complete news archive lost entries or retained source order instead of date order")
        for (expected_date, expected_text), (actual_date, actual_text) in zip(expected_news, archive.news_items):
            require(expected_date == actual_date and expected_text in actual_text,
                    "A news entry's date and text were mismatched while sorting")
        require(all(text not in home.text for _, text in expected_news[6:]),
                "Older news leaked into the six-entry homepage summary")
        check_links(output, base)

        revised_news = list(news_entries)
        revised_news[0] = ("2028-01", "Revised news fixture now appears first")
        write_news(revised_news)
        output = scratch / "news-updated"
        build(hugo, source, output, base)
        home, archive = Page(output / "index.html"), Page(output / "news/index.html")
        for page in (home, archive):
            require(page.news_items[0][0] == revised_news[0][0]
                    and revised_news[0][1] in page.news_items[0][1]
                    and news_entries[0][1] not in page.text,
                    "Editing a shared news date/text did not update and reorder both homepage and archive")
        require(len(home.news_items) == 6 and len(archive.news_items) == 8,
                "Editing news changed the homepage limit or dropped archived entries")
        check_links(output, base)
        print("PASS: eight unsorted news entries produce six newest home items, a complete archive, and shared edits")

        write_news([("2028-13", "Invalid date fixture")])
        result = build(hugo, source, scratch / "news-invalid", base, expect_success=False)
        require(result.returncode != 0 and "data/news.yaml" in result.stdout
                and "date must use YYYY-MM with a valid month" in result.stdout,
                "An invalid news month did not produce an actionable error:\n" + result.stdout)
        news.write_text(original_news, encoding="utf-8")
        print("PASS: malformed news dates report the source file and expected format")

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
            require(value.casefold() in home.text.casefold(), f"A service data edit did not render: {value}")
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
        require("postdoctoral researcher" in postdoc.text.casefold() and "3002" in postdoc.text,
                "A postdoc profile lost its role or enrollment year")
        check_links(output, base)
        print("PASS: enrollment order, alphabetical ties, missing years, and the postdoc group")

        paper_awards = ("Fixture Distinguished Paper Award", "Fixture Research Prize")
        author_metadata = (
            f'corresponding: ["{student_name}", "Zhuotao Liu"]\n'
            f'equal_contribution: ["{student_name}"]\n'
            f'award: ["{paper_awards[0]}", "{paper_awards[1]}"]\n'
            'selected: true\n'
        )
        write_paper(entry, minimal.replace("First Author", student_name), author_metadata)
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
        for relative in ("index.html", "publications/index.html", "students/fixture-student/index.html",
                         "publications/four-field-check/index.html"):
            page = Page(output / relative)
            if relative == "publications/four-field-check/index.html":
                paper_text = normalized_text(page.text)
            else:
                paper_index = article_index(page, title)
                require(paper_index is not None, f"The author/award fixture is missing from {relative}")
                paper_text = normalized_text(page.articles[paper_index])
            require(re.search(re.escape(student_name) + r"\s*†\s*\*", paper_text)
                    and re.search(r"Zhuotao Liu\s*†", paper_text),
                    f"{relative}: multiple corresponding authors or overlapping equal contribution lost a marker")
            require("† Corresponding authors" in paper_text and "* Equal contribution" in paper_text,
                    f"{relative}: corresponding-author or equal-contribution explanations are missing")
            for award in paper_awards:
                require(paper_text.count(award) == 1, f"{relative}: paper award was lost or duplicated: {award}")
            student_links = [(attrs, text) for attrs, text in page.links
                             if "student-author" in attrs.get("class", "").split()
                             and attrs.get("href") == "/students/fixture-student/#publications"]
            require(len(student_links) == 1 and student_links[0][1] == student_name,
                    f"{relative}: corresponding-author emphasis changed the student link or included its markers")
        check_links(output, base)
        print("PASS: two-field students, automatic paper lists, and conditional Publications links")
        print("PASS: multiple corresponding authors, shared contribution markers, and two awards retain student links on all paper views")

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
                    'category: patent\ndraft: false\nselected: true\n')
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
    print("All site and editing-workflow checks passed; the source directory was not modified.")


if __name__ == "__main__":
    main()
