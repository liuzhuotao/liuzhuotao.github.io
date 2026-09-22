# Personal research website preview

This directory is a standalone preview of Zhuotao Liu's personal research website.
It uses Hugo **0.152.2** with local templates and CSS; no theme, Node.js, package
installation, or Hugo modules are needed. The repository's existing website is
still the production site.

The preview includes the personal homepage, selected publications, a complete
publication list grouped by year, awards, academic service, and news. The selected
and complete publication lists use the **same short text files**. Existing
publication URLs redirect to their migrated detail pages. InspiringGroup and
openings link to their existing pages at `https://liuzhuotao.github.io/`.

## View the preview

With Hugo 0.152.2 installed, run this from the repository root:

```sh
hugo server --source redesign
```

Open the local address printed by Hugo, normally `http://localhost:1313/`.
Hugo reloads the page when you save a content or template change.

To create a static build:

```sh
cd redesign
hugo --minify --destination public
```

The output is `redesign/public/` and is ignored by Git. For a preview served
under a URL prefix, pass the full address with `--baseURL`, including its
trailing slash. The preview includes a design-preview notice and a `noindex`
directive.

## Edit publications once for both lists

Every paper lives in one Markdown file in `redesign/content/publications/`.
Edit that file to update its title, authors, venue, year, links, or abstract; the
complete list, homepage selection, and detail page all use that one entry.
There is no separate homepage publication list to maintain.

In GitHub, open this folder on the redesign branch, choose a paper, and use the
pencil icon to edit. To add a paper, use **Add file → Create new file**. Save the
change using GitHub's commit controls. While this redesign is a preview, these
edits update the preview branch; the current live website still uses its original
content. Locally, save the file and Hugo's preview reloads automatically.

### Add a paper to the complete list

Create a Markdown file such as `redesign/content/publications/my-paper.md`.
Only four fields are required:

```yaml
---
title: "My paper title"
authors: ["First Author", "Zhuotao Liu", "Third Author"]
venue: "ACM CCS"
year: 2026
---
```

Save the file and Hugo adds it to **All publications**, grouped by year with
newer years first. Author order is preserved, and the name matching
`data/profile.yaml` is highlighted automatically. There is no mandatory
abstract or publication form.

### Choose and order selected publications

Add one line to a paper's existing entry to also show it on the homepage:

```yaml
selected: true
```

Remove that line or set `selected: false` to remove it from the homepage. The
paper remains in the complete list. By default, selected papers appear with
newer years first.

For a hand-picked homepage order, add a positive whole number to the same file:

```yaml
selected: true
selected_order: 1
```

Number other selected papers `2`, `3`, and so on. Numbered papers appear first,
in ascending order; selected papers without a number follow in descending year
order. Use distinct numbers when you want an exact order. This changes only the
homepage; **All publications** keeps its year grouping. There is no fixed limit
on the number of selected papers.

### Optional publication details

Add any of these optional fields before the closing `---` when useful:

```yaml
paper: "https://example.org/paper"
pdf: "https://example.org/paper.pdf"
code: "https://github.com/example/project"
conference: "https://example.org/conference"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=PROFILE&citation_for_view=RECORD"
award: "Distinguished Paper Award"
corresponding: ["Zhuotao Liu"]
equal_contribution: ["First Author", "Second Author"]
```

- `corresponding` and `equal_contribution` are lists of exact author names.
- `award` accepts a short text label or a list of labels for multiple awards.
- Paper, PDF, code, conference, and Scholar links accept `https://` URLs or local paths beginning
  with `/`. Local files belong in `redesign/static/`; for example,
  `redesign/static/papers/my-paper.pdf` is linked as `/papers/my-paper.pdf`.
- Write an optional abstract as ordinary Markdown after the closing `---`.
  Each publication gets a page even without an abstract.
- Add `draft: true` to hide an unfinished entry. To include drafts locally, run
  `hugo server --source redesign --buildDrafts`.
- Keep a migrated entry's `aliases` lines so old publication links continue to
  work. When adding a new paper, no aliases are needed. Keep existing filenames
  when editing; filenames form the publication URLs.
- Migrated entries may also include `topics`, a list of research-area labels,
  and `group_authors`, a list of author positions counted from 1. These preserve
  the archive's topic labels and group-member highlighting. Both are optional;
  if you reorder authors, update any `group_authors` positions to match.

For alternate versions of the same paper, keep one entry and optionally add links:

```yaml
versions:
  - label: "Preprint"
    url: "https://arxiv.org/abs/1234.56789"
  - label: "Workshop version"
    url: "https://example.org/workshop-paper"
```

Journal extensions and independently published conference papers can have separate
entries. Add `category: patent` to place a patent or application in the separate
**Patents & applications** section. Use the inventor names in `authors` and the
patent/application number in `venue`; the same four required fields still apply.
Leave `category` out for ordinary research publications and preprints.

The Scholar comparison added 36 research entries and four patent/application
entries to the original 58 papers. The website now contains 94 research items
(including preprints and a thesis) plus four patents/applications. All 109 Scholar
records, including duplicate versions, are accounted for in
`redesign/SCHOLAR-IMPORT.md`. These are editable text files; the site does not
automatically overwrite your edits from Scholar.

You can also generate the short entry with Hugo:

```sh
hugo new content --source redesign publications/my-paper.md
```

The generated entry starts with `draft: true`. Remove that line or set it to
`false` when ready. The build checks required fields, author lists, four-digit
years, publication link formats, and positive whole-number `selected_order`
values. To remove a paper from both lists, delete its file or set `draft: true`.

## Update academic service

Edit `redesign/data/services.yaml`. Add or edit a short entry under `editorial`
for journal roles, or under `committees` for conference service:

```yaml
editorial:
  - years: "2025–present"
    role: "Associate Editor"
    organization: "IEEE Transactions on Dependable and Secure Computing (TDSC)"

committees:
  - years: "2027"
    venues: ["IEEE S&P", "ACM CCS", "USENIX Security"]
```

Keep the section names once at the top of each list. To add another item, copy
just the indented entry beginning with `- years:`. Keep entries in the order you
want them displayed, normally newest first. Use spaces for YAML indentation.

## Update your profile, awards, and news

Other homepage edits use these short YAML files:

| File under `redesign/` | What to edit |
| --- | --- |
| `data/profile.yaml` | Name, affiliation, contact links, biography, research directions, and portrait path |
| `data/awards.yaml` | Award entries with a year, title, and optional description |
| `data/news.yaml` | News entries with a date and text; put the newest first |

Use plain text for fields, quoting values that contain a colon. The biography
and news text also support Markdown links. The homepage shows the first three
news entries directly below your profile. Keep awards in the order you want them displayed.

An award entry looks like this:

```yaml
- year: 2026
  title: "Award name"
  description: "Awarding organization or short description"
```

A news entry looks like this:

```yaml
- date: "Sep 2026"
  text: "Our paper was accepted to Conference Name."
```

Replace the portrait in `redesign/static/images/portrait.jpg`, or change the
`portrait` path in `data/profile.yaml`. Site-wide external links to the group and
openings are configured in `redesign/hugo.yaml`.

## Preview checks and publishing

`.github/workflows/redesign-preview.yml` builds only this directory on relevant
pull requests, relevant pushes to `codex/personal-site-preview`, and manual
runs. A successful run provides a downloadable `personal-site-preview`
artifact in GitHub Actions. It does **not** create a public preview URL or
deploy to GitHub Pages. Its only repository permission is `contents: read`.

The production workflow, `.github/workflows/deploy.yml`, continues to build the
existing site from the repository root. It runs automatically only for pushes
to `main`, and its deployment job is also restricted to `main`, including
manual runs. A manual run on another branch cannot publish the preview.

Run the same build and content-editing checks locally from the repository root:

```sh
python3 redesign/scripts/check.py
```

Use `--hugo /path/to/hugo` if Hugo is not on your `PATH`. The checks build
temporary copies, verify internal links and legacy redirects, and exercise
adding a four-field paper, switching homepage selection, changing selection
order, and editing academic service. Your source files are not changed.

Publishing this design is a separate milestone. Before switching production,
review the migrated publication archive and redirects, verify group and other
page links, remove preview notices and indexing restrictions, and update the
production build to use the completed design.
