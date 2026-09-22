# Content provenance

This preview includes 94 research items and four patents/applications, with three
research papers selected for the homepage. It retains all 58 publications from
the existing archive and adds works from the user’s Google Scholar profile.
See [SCHOLAR-IMPORT.md](SCHOLAR-IMPORT.md) for the complete 109-record mapping,
version consolidation, and verified source corrections. The original profile, awards, and news were read from
`liuzhuotao/liuzhuotao.github.io` at commit
`86c60c36f734ebd0b09cf9b4d1d7beddc46500ac` on 21 September 2026; links below
remain pinned to that source. The complete publication migration uses the source
at commit `a749607bf301a43bb0397fea29e1718df536eaa0` on 22 September 2026.
See [PUBLICATION-MIGRATION.md](PUBLICATION-MIGRATION.md) for every source mapping,
preserved field, and existing data issue.

| Preview content | Repository source | Treatment |
| --- | --- | --- |
| `data/profile.yaml`: name, role, affiliation, department, email, Scholar, GitHub, ORCID | [Zhuotao Liu author profile](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/86c60c36f734ebd0b09cf9b4d1d7beddc46500ac/content/authors/liuzhuotao/_index.md) | Retains the real identity and profile links. Converts the obfuscated email to a working email address. |
| `data/profile.yaml`: bio | [Zhuotao Liu author profile](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/86c60c36f734ebd0b09cf9b4d1d7beddc46500ac/content/authors/liuzhuotao/_index.md) | Proposed concise first-person rewrite of the real prose biography below the front matter. Keeps the Tsinghua role, group, Google experience, and education. |
| `data/profile.yaml`: four research directions; page descriptions | [Research taxonomy](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/86c60c36f734ebd0b09cf9b4d1d7beddc46500ac/content/research-topics/_index.md) and the author profile above | Proposed wording distilled from the existing research areas. No new research claims or performance claims. |
| `static/images/portrait.jpg` | [Existing author portrait](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/86c60c36f734ebd0b09cf9b4d1d7beddc46500ac/content/authors/liuzhuotao/avatar.jpg) | Exact binary copy; source Git blob `6e76f8c291ab934ca2d1d7a74d9628903bfeb661`, 174646 bytes. |
| `content/publications/euston.md` | [Euston](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/86c60c36f734ebd0b09cf9b4d1d7beddc46500ac/content/publications/ai_and_data_security/privacy-preserving_machinelearning/2-1-4.md) | Full title, all six authors in order, IEEE S&P 2026, and the original paper link. Original abstract moved into the Markdown body. |
| `content/publications/ringsg.md` | [RingSG](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/86c60c36f734ebd0b09cf9b4d1d7beddc46500ac/content/publications/ai_and_data_security/privacy-preserving_machinelearning/2-1-3.md) | Full title, all six authors in order, ACM CCS 2025, original paper link, Distinguished Paper Award, and Zhuotao Liu's corresponding-author note. Original abstract moved into the Markdown body. |
| `content/publications/pred.md` | [PRED](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/86c60c36f734ebd0b09cf9b4d1d7beddc46500ac/content/publications/networking_infrastructure_for_ai/datacenter_networking/3-1-1.md) | Full title, all nine authors in order, USENIX NSDI 2025, and the original paper link. Original abstract moved into the Markdown body. |
| `data/awards.yaml` | [Awards](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/86c60c36f734ebd0b09cf9b4d1d7beddc46500ac/content/awards/_index.md) | All eleven entries retained, with compact titles/descriptions. Original Chinese award names are retained. Dates are the years stated by the source. |
| `data/news.yaml` | [News](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/86c60c36f734ebd0b09cf9b4d1d7beddc46500ac/content/news/_index.md) and RingSG above | Proposed concise rewrites of the latest three entries (August 2026, May 2026, October 2025). Promotional superlatives removed. RingSG's name is supported by its publication record. |
| Original 58 files in `content/publications/` | [Publication migration report](PUBLICATION-MIGRATION.md) | Preserves source titles, author order, abstracts, paper/PDF/code/conference links, awards, contribution notes, research topics, and group-member markers. Each old detail URL has a redirect. |
| `data/services.yaml` | Roles supplied directly by Zhuotao Liu in this conversation on 22 September 2026 | TDSC Associate Editor (2025–present) and conference program committees for 2022–2027. No additional appointments inferred. |
| `content/students/` | [Original student profiles](https://github.com/liuzhuotao/liuzhuotao.github.io/tree/a749607bf301a43bb0397fea29e1718df536eaa0/content/authors) | All 12 students retained, grouped by the source `student_level`. Enrollment years, interests, real biographies, valid profile links, and Jinzhu Yan's CV are preserved. Portraits are omitted. Student paper lists are derived from the shared publication collection. |
| `content/join/index.md` | [Original Join us page](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/a749607bf301a43bb0397fea29e1718df536eaa0/content/join/index.md) | Concise rewrite preserving the student/postdoctoral opportunities, funding, additional annual postdoctoral compensation, and friendly/supportive/flourishing culture. No new deadlines or eligibility requirements. |

Author identifiers were expanded using existing author profiles: `liuzhuotao` becomes
Zhuotao Liu using the author profile above; `zouzhenhua` becomes Zhenhua Zou using
the [Zhenhua Zou author profile](https://github.com/liuzhuotao/liuzhuotao.github.io/blob/86c60c36f734ebd0b09cf9b4d1d7beddc46500ac/content/authors/zouzhenhua/_index.md).
Other resolved identifiers and unresolved source details are recorded in the
migration report. No authors were removed or reordered. Existing source abstracts
are preserved, including their wording; line wrapping is normalized.

The existing author front matter also contains unrelated template examples of
employment, education, skills, and awards (including Meta, OpenAI, and Stanford).
Those examples are excluded. The standalone `content/awards/_index.md` and the real
prose biography are the sources for those subjects. No CV link is included because
the available resume has not been verified as the user's current CV.

The latest source news is August 2026. No September 2026 announcement is invented.
The selected-paper choices are proposed editorial choices for this preview.
The broad introductory research slogan was removed at the user’s request; the
compact profile now leads with role, affiliation, and biography, followed by news.

Student migration excludes copied template contact details: Mengyu Zhang's source
email and social links belonged to Zhuotao Liu, and Wang You's source ORCID was
copied from another profile. The student Qi Li uses the original publication
author-position markers so papers by the professor with the same name are not
misattributed. Jinzhu Yan's CV is an exact copy of the existing linked file
(Git blob `8fd0d3ebf2cbc32aee8c405f58b6df7b42ddc037`).

Per-paper Scholar source URLs remain in the text entries for provenance but are
not rendered. Pre-2020 research items share one section; titles, years, and
individual paper records are unchanged.
