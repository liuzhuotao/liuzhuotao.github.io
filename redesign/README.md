# Personal research website editing guide

The live website is [liuzhuotao.github.io](https://liuzhuotao.github.io/).
Its source is the [`redesign/` directory on `main`](https://github.com/liuzhuotao/liuzhuotao.github.io/tree/main/redesign).
It uses Hugo **0.152.2** with local templates and CSS; no theme, Node.js, or Hugo
modules are needed. Building locally only requires Hugo; the optional publication
updater and its CI tests use Python 3.12 and PyYAML. The old content and templates outside
`redesign/` are retained for reference and are not used for deployment.

The website includes the personal homepage, selected publications, a complete
publication list grouped by year, awards, academic service, teaching, news, students, and
Join Us. The selected
and complete publication lists use the **same short text files**. Existing
publication and student URLs redirect to their migrated detail pages. Students
have text profiles linked to their papers, without individual portraits.

## Edit and publish through GitHub

Start from the [`redesign/` folder on `main`](https://github.com/liuzhuotao/liuzhuotao.github.io/tree/main/redesign).
Open a file and choose the pencil icon to edit it, or use **Add file → Create
new file** to add an entry. When saving, choose a new branch and open a pull
request so you can review the change before publishing. Wait for all build and
content checks to pass, then merge the pull request into `main`.

Merging into `main` starts the [production deployment](https://github.com/liuzhuotao/liuzhuotao.github.io/actions/workflows/deploy.yml).
The workflow checks and builds the site before uploading or deploying it. If a
check or build fails, the existing live website stays in place. A successful
deployment publishes the update to [liuzhuotao.github.io](https://liuzhuotao.github.io/).

## View locally

With Hugo 0.152.2 installed, run this from the repository root:

```sh
hugo server --source redesign
```

Open the local address printed by Hugo, normally `http://localhost:1313/`.
This shows the production layout, without a preview banner. Hugo reloads the
page when you save a content or template change.

For an explicitly marked preview with a banner and `noindex`, run:

```sh
hugo server --source redesign --environment preview
```

To create a static build:

```sh
hugo --source redesign --minify --destination public
```

Hugo resolves the destination relative to the source directory, so the output
is `redesign/public/` and is ignored by Git. To build a marked preview, add
`--environment preview`. For a site served under a URL prefix, also pass the
full address with `--baseURL`, including its trailing slash.

## Edit publications once for both lists

Every paper lives in one Markdown file in
[`redesign/content/publications/`](https://github.com/liuzhuotao/liuzhuotao.github.io/tree/main/redesign/content/publications).
Edit that file to update its title, authors, venue, year, links, or abstract; the
complete list, homepage selection, and detail page all use that one entry.
There is no separate homepage publication list to maintain.

In GitHub, open that folder on `main` and follow the edit-and-publish steps above.
Locally, save the file and Hugo reloads automatically.

### Add a paper to the complete list

Create a Markdown file such as `redesign/content/publications/my-paper.md`.
Only four fields are required:

In GitHub's **Name your file** box, use a short filename ending in **`.md`**
(for example, `trafficflex.md`). Put the full paper title in the `title:` field
inside the file. Copy the entire example, including both **`---`** lines; those
lines mark the start and end of the publication metadata.

```yaml
---
title: "My paper title"
authors: ["First Author", "Zhuotao Liu", "Third Author"]
venue: "ACM CCS"
year: 2026
---
```

Save the file and Hugo adds it to **All Publications**, grouped by year with
newer years first. Papers before 2021 (2020 and earlier) share one **Before 2021** section, with each
paper's year still visible. Author order is preserved, and the name matching
`data/profile.yaml` is highlighted automatically. There is no mandatory
abstract or publication form.

### Newly accepted papers: add once, details follow automatically

The same four-field entry above is enough. The
[publication updater](https://github.com/liuzhuotao/liuzhuotao.github.io/actions/workflows/enrich-publications.yml)
runs when publication files change and daily at **11:17 a.m. China time** (GitHub
may delay scheduled runs). It checks Crossref, OpenAlex, and arXiv for the missing details.
You do not need to return to the file when the abstract or links become available.

- An automatic match requires an exact normalized title, the same full author
  names, a nearby publication year, and one unambiguous result per source.
- It adds a publisher/DOI **Paper** link, a deposited **PDF** link if available,
  an **Abstract**, and/or a clearly labeled **Preprint** link to arXiv.
- Existing fields, abstracts, authors, venue, year, selection, and aliases are
  preserved. Even an explicitly empty link field is left alone; remove the key
  entirely to allow automatic filling. Source comments record where additions came from.
- Minimal entries are picked up automatically. Once details start arriving, the
  updater adds `auto_enrich: true` to keep checking for remaining links. Set
  `auto_enrich: false` to stop updates for that paper. You can also set it to
  `true` on an older entry that already has an abstract and Paper link but needs
  a PDF or preprint link. An available preprint does not stop it from looking for
  a publisher PDF later.
- Papers with unavailable or ambiguous metadata stay as they are and are tried
  again. Code links, acceptance announcements, and revised titles/author lists
  are not inferred. arXiv provides a preprint, not confirmation of acceptance.
- Updates are committed and published automatically **only after the enrichment
  tests, full site checks, production build, and output validation pass**.
  Concurrent changes on GitHub cause the updater to stop rather than overwrite
  your edits. The next run retries against the current files.

To run it immediately, open the updater's **Actions** page above and choose
**Run workflow** on `main`. Each run saves a JSON report under its artifacts with
changed files, sources, pending files, and temporary source errors. No API keys
or additional accounts are needed. Normal website builds do not query these sources.

GitHub can disable schedules in a public repository after 60 days without
repository activity. If updates stop, open the workflow in Actions and re-enable
it. See [GitHub's scheduled workflow documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

For a local, non-writing sample:

```sh
python3 -m pip install -r redesign/scripts/requirements-enrichment.txt
python3 redesign/scripts/enrich_publications.py --limit 2
```

Without `--write`, the script only reports potential changes. Remove `--limit`
and add `--write` to apply available details locally. Source API documentation:
[Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/),
[OpenAlex](https://help.openalex.org/api/authentication/),
and [arXiv](https://info.arxiv.org/help/api/user-manual.html).

### Choose and order selected publications

Add one line to a paper's existing entry, before the closing `---`, to also show
it on the homepage:

```yaml
selected: true
```

Remove that line or set `selected: false` to remove it from the homepage. The
paper remains in the complete list. Selected papers are **always sorted by
publication year, newest first**, just like the complete list. No order numbers
are needed; older `selected_order` fields are ignored and can be removed.

You can select eight, ten, or as many papers as you want: **there is no fixed
limit**. Each selected paper still appears in the complete list, using the same
file.

### Optional publication details

Add any of these optional fields before the closing `---` when useful:

```yaml
paper: "https://example.org/paper"
pdf: "https://example.org/paper.pdf"
preprint: "https://arxiv.org/abs/2601.01234"
code: "https://github.com/example/project"
conference: "https://example.org/conference"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=PROFILE&citation_for_view=RECORD"
award: "Distinguished Paper Award"
corresponding: ["Zhuotao Liu"]
equal_contribution: ["First Author", "Second Author"]
```

- `corresponding` and `equal_contribution` are lists of exact author names.
- `award` accepts a short text label or a list of labels for multiple awards.
- `scholar` is optional source metadata. It is retained for reference but does
  not display a link beside each paper. The profile and publication-list header
  retain the main Google Scholar link.
- Paper, PDF, preprint, code, conference, and Scholar links accept `https://` URLs or local paths beginning
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
entries. Leave `category` out for ordinary research publications and preprints.
The site displays research publications only. The four imported patent records
are retained as drafts for source history; `category: patent` entries are excluded
from the homepage, complete list, and student publication lists.

The Scholar comparison added 36 research entries and four patent/application
entries to the original 58 papers. The website displays 94 research items
(including preprints and a thesis). All 109 Scholar
records, including duplicate versions, are accounted for in
`redesign/SCHOLAR-IMPORT.md`. These are editable text files; the site does not
automatically overwrite your edits from Scholar.

You can also generate the short entry with Hugo:

```sh
hugo new content --source redesign publications/my-paper.md
```

The generated entry starts with `draft: true`. Remove that line or set it to
`false` when ready. The build checks required fields, author lists, four-digit
years, and publication link formats. To remove a paper from both lists, delete its file or set `draft: true`.

## Add or update students

In [`redesign/content/students/`](https://github.com/liuzhuotao/liuzhuotao.github.io/tree/main/redesign/content/students),
create `first-last/index.md`. Only two fields are required:

```yaml
---
title: "First Last"
group: "phd"
---
```

Use `postdoc`, `phd`, `master`, or `alumni` for the group. The directory shows
each member's name linked to their profile, and a **Publications →** link only
when they have matching papers. Paper counts are not displayed. Papers are collected
from the same publication files used by the complete list, by matching the
student's full name against `authors`. Adding a matching paper updates the link
and student page automatically. No photo or separate paper list is needed.
Students without matching papers still have a page with an empty-state message.
Patents are excluded from student paper lists.

Optional fields can go before the closing `---`:

```yaml
since: 2026
interests: ["Systems Security", "Privacy"]
homepage: "https://example.org"
email: "student@example.org"
github: "https://github.com/example"
scholar: "https://scholar.google.com/citations?user=PROFILE"
orcid: "https://orcid.org/0000-0000-0000-0000"
```

Write an optional biography as ordinary Markdown below the closing `---`.
Change `group` to `alumni` when a student graduates; their papers and links stay
intact. Each group is sorted by `since`, newest first; names break ties
alphabetically. Entries without a starting year appear last. Preserve existing
`aliases` and folder names when editing so links continue to work.

If a student publishes under another spelling, add exact alternatives with
`author_names: ["Alternative Name"]`. For a name shared by different people,
add `match: "marked"` to the student file, then mark the correct author's
position in each paper with `group_authors: [1]` (positions start at 1). Include
any other existing marked positions in that list. **Qi Li is already configured
this way** to distinguish the student from the professor. Only marked matching
occurrences link to this student's papers.

To generate a starter file locally:

```sh
hugo new content --source redesign students/first-last/index.md
```

Set its title to the student's full name and remove `draft: true` when ready.
The build checks the required name/group, supported groups, enrollment year,
lists, and profile link formats.

## Edit Join Us

Edit [`redesign/content/join/index.md`](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/main/redesign/content/join/index.md).
Its headings and paragraphs are ordinary
Markdown, covering openings, postdoctoral positions, group culture, and contact.
The contact box uses the email in `redesign/data/profile.yaml`.

## Update academic service

Edit [`redesign/data/services.yaml`](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/main/redesign/data/services.yaml).
Add or edit a short entry under `editorial`
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
| [`data/profile.yaml`](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/main/redesign/data/profile.yaml) | Name, affiliation, contact links, biography, research directions, and portrait path |
| [`data/awards.yaml`](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/main/redesign/data/awards.yaml) | Award entries with a year, title, and optional description |
| [`data/news.yaml`](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/main/redesign/data/news.yaml) | News entries with a `YYYY-MM` date and text; newest entries appear first automatically |
| [`data/teaching.yaml`](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/main/redesign/data/teaching.yaml) | Course titles, years, levels, teaching roles, and the mentoring paragraph |

Use plain text for fields, quoting values that contain a colon. The biography
and news text also support Markdown links. Keep awards in the order you want
them displayed.

An award entry looks like this:

```yaml
- year: 2026
  title: "Award name"
  description: "Awarding organization or short description"
```

A news entry looks like this:

```yaml
- date: "2026-09"
  text: "Our paper was accepted to Conference Name."
```

Add or edit entries in `data/news.yaml`; both the homepage and the
[complete news archive](https://liuzhuotao.github.io/news/) use this one list.
The homepage automatically shows the **six newest** entries directly below
your profile. The archive shows every entry, grouped by year, newest first.
Use quoted `YYYY-MM` dates, such as `"2026-09"` for September 2026. Entries with
the same month keep their order in the file. There is no separate homepage list
to maintain and no need to delete older news. The build checks dates and
requires text for every entry.

Replace the portrait in `redesign/static/images/portrait.jpg`, or change the
`portrait` path in `data/profile.yaml`. The image is cropped to a circle by CSS;
the original image file stays intact. Navigation links to the local Students
and Join Us pages.

## Colors and publication text size

Section accents alternate between teal and navy. Headings, links, and author
underlines use the section's color; ordinary text remains neutral. Publication
and news year groups, and student groups, alternate automatically as content
is added. These presentation settings live in `redesign/static/css/site.css`;
ordinary content edits do not need any color fields.

Publication rows use 22px titles and 17px author names on desktop, and 20px
and 16px on smaller screens. The same styles apply to selected publications,
the complete list, and students' paper lists.

## Build checks and recovery

`.github/workflows/redesign-preview.yml` builds only this directory on relevant
pull requests, relevant pushes to `codex/personal-site-preview`, and manual
runs. Let its checks pass before merging a pull request. A successful run
provides a downloadable `personal-site-preview`
artifact in GitHub Actions. It does **not** create a public preview URL or
deploy to GitHub Pages. Its only repository permission is `contents: read`.

The production workflow, `.github/workflows/deploy.yml`, uses Hugo **0.152.2**
to build `redesign/`. It runs the content-editing checks and production build
before uploading the Pages artifact, and deploys only when they succeed.
Automatic deployment runs on pushes to `main`; the deployment job is restricted
to `main`, including manual runs. A manual run on another branch cannot publish
the website.

Run the same build and content-editing checks locally from the repository root:

```sh
python3 redesign/scripts/check.py
```

Use `--hugo /path/to/hugo` if Hugo is not on your `PATH`. The checks build
temporary copies, verify internal links and legacy redirects, and exercise
adding a four-field paper, switching homepage selection, checking newest-first selection
order, editing academic service, adding students, and matching their papers.
Your source files are not changed.

If a published change needs to be undone, revert its merge on `main` through a
new pull request. Wait for the checks, then merge the revert; the same workflow
rebuilds and deploys the restored version. Keep the Git history intact; do not
force-push to roll back the website.
