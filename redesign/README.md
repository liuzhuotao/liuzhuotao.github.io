# Personal research website preview

This directory is a standalone preview of Zhuotao Liu's personal research website.
It uses Hugo **0.152.2** with local templates and CSS; no theme, Node.js, package
installation, or Hugo modules are needed. The repository's existing website is
still the production site.

The preview includes a new homepage and **three representative publications**.
The rest of the publication archive and group pages have not been migrated.
Links to the full archive, InspiringGroup, and openings point to their existing
pages at `https://liuzhuotao.github.io/`.

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

## Add a publication

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

Save the file and Hugo adds it to the preview's publication list, grouped by
year. Author order is preserved, and the name matching `data/profile.yaml` is
highlighted automatically. There is no mandatory abstract or publication form.

Add any of these optional fields before the closing `---` when useful:

```yaml
paper: "https://example.org/paper"
pdf: "https://example.org/paper.pdf"
code: "https://github.com/example/project"
award: "Distinguished Paper Award"
selected: true
corresponding: ["Zhuotao Liu"]
equal_contribution: ["First Author", "Second Author"]
```

- `selected: true` also includes the paper on the homepage.
- `corresponding` and `equal_contribution` are lists of exact author names.
- Paper, PDF, and code links accept `https://` URLs or local paths beginning
  with `/`. Local files belong in `redesign/static/`; for example,
  `redesign/static/papers/my-paper.pdf` is linked as `/papers/my-paper.pdf`.
- Write an optional abstract as ordinary Markdown after the closing `---`.
  Each publication gets a page even without an abstract.
- Add `draft: true` to hide an unfinished entry. To include drafts locally, run
  `hugo server --source redesign --buildDrafts`.

You can also generate the short entry with Hugo:

```sh
hugo new content --source redesign publications/my-paper.md
```

The generated entry starts with `draft: true`. Remove that line or set it to
`false` when ready. The build checks that required fields are present, that
authors are a list, that the year has four digits, and that publication links
use a supported URL format.

## Update your profile, awards, and news

Most homepage edits use three short YAML files:

| File under `redesign/` | What to edit |
| --- | --- |
| `data/profile.yaml` | Name, affiliation, contact links, research statement, biography, research directions, and portrait path |
| `data/awards.yaml` | Award entries with a year, title, and optional description |
| `data/news.yaml` | News entries with a date and text; put the newest first |

Use plain text for fields, quoting values that contain a colon. The biography
and news text also support Markdown links. The homepage shows the first three
news entries. Keep awards in the order you want them displayed.

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
`portrait` path in `data/profile.yaml`. Site-wide external links to the current
archive, group, and openings are configured in `redesign/hugo.yaml`.

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

Publishing this design is a separate migration milestone. Before switching
production, migrate and review the full publication archive, retain existing
publication URLs or provide redirects, verify group and other page links,
remove preview notices and indexing restrictions, and update the production
build to use the completed design.
