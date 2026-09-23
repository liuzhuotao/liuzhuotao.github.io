#!/usr/bin/env python3
"""Fill missing publication details from uniquely matched public metadata.

Dry run by default. Remote text is data, never HTML or executable Markdown.
Only --write changes files; unavailable and ambiguous records remain pending.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import html
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import re
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import yaml


def normalize(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', html.unescape(text)).casefold()
                   if c.isalnum())


def authors_match(local, remote):
    # Full names and the whole author set are required; initials alone are ambiguous.
    if not local or not remote or any(not isinstance(n, str) or not normalize(n) for n in local + remote):
        return False
    return sorted(map(normalize, local)) == sorted(map(normalize, remote))


def safe_url(value):
    if not isinstance(value, str) or re.search(r'[\s\\<>]', value):
        return ''
    try:
        u = urlsplit(value)
        if u.scheme != 'https' or not u.hostname or u.username or u.password or u.port not in (None, 443):
            return ''
        host = u.hostname.lower()
        if '.' not in host or host.endswith(('.local', '.localhost', '.internal')):
            return ''
        try:
            if not ipaddress.ip_address(host).is_global:
                return ''
        except ValueError:
            pass
        return urlunsplit(u)
    except ValueError:
        return ''


@dataclass
class Candidate:
    title: str
    authors: list[str]
    year: int | None
    source_url: str
    paper: str = ''
    pdf: str = ''
    abstract: str = ''
    preprint: str = ''
    abstract_is_html: bool = True


def choose_candidate(metadata, candidates):
    matches = {}
    for candidate in candidates:
        existing_doi = doi_link(metadata.get('paper'))
        candidate_doi = doi_link(candidate.paper)
        if existing_doi and candidate_doi and existing_doi.casefold() != candidate_doi.casefold():
            continue
        if (normalize(candidate.title) == normalize(metadata['title'])
                and authors_match(metadata['authors'], candidate.authors)
                and type(candidate.year) is int
                and abs(candidate.year - metadata['year']) <= 2
                and safe_url(candidate.source_url)):
            if candidate.source_url in matches and matches[candidate.source_url] != candidate:
                return None
            matches[candidate.source_url] = candidate
    return next(iter(matches.values())) if len(matches) == 1 else None


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f'Duplicate frontmatter key: {key}')
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


@dataclass
class Publication:
    path: Path
    metadata: dict
    body: str
    raw: str


FRONTMATTER = re.compile(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', re.S)


def load_publication(path):
    raw = path.read_bytes().decode('utf-8')
    match = FRONTMATTER.match(raw)
    if not match:
        raise ValueError(f'{path}: YAML frontmatter is required')
    metadata = yaml.load(match[1], Loader=UniqueLoader)
    if not isinstance(metadata, dict):
        raise ValueError(f'{path}: frontmatter must be a mapping')
    return Publication(path, metadata, raw[match.end():], raw)


class AbstractText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        elif not self.hidden and tag in ('p', 'br', 'div', 'jats:p', 'jats:title'):
            self.parts.append(' ')

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden:
            self.hidden -= 1
        elif not self.hidden:
            self.parts.append(' ')

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def clean_abstract(value, is_html=True):
    if is_html:
        parser = AbstractText()
        parser.feed(value)
        value = ''.join(parser.parts)
    plain = re.sub(r'\s+', ' ', value).strip()
    plain = re.sub(r'^abstract\s*[:—-]?\s+', '', plain, flags=re.I)
    if len(plain) < 40 or len(plain) > 30000:
        return ''
    # Escape Markdown and Hugo shortcodes as well as raw HTML.
    plain = html.escape(plain, quote=False)
    return re.sub(r'([\\`*_{}\[\]#!|])', r'\\\1', plain)


def apply_candidate(publication, candidate):
    if not safe_url(candidate.source_url):
        return publication.raw
    additions = []
    for field in ('paper', 'pdf', 'preprint'):
        value = safe_url(getattr(candidate, field))
        if field not in publication.metadata and value:
            additions.append(f'{field}: {json.dumps(value, ensure_ascii=False)}')
    abstract = clean_abstract(candidate.abstract, candidate.abstract_is_html) if not publication.body.strip() else ''
    if not additions and not abstract:
        return publication.raw
    if 'auto_enrich' not in publication.metadata:
        additions.append('auto_enrich: true')
    match = FRONTMATTER.match(publication.raw)
    newline = '\r\n' if '\r\n' in publication.raw else '\n'
    front = publication.raw[:match.end(1)]
    if additions:
        front += newline + f'# Metadata source: {candidate.source_url}' + newline + newline.join(additions)
    result = front + publication.raw[match.end(1):match.end()]
    if abstract:
        # Source lives in a comment and is not presented as a paper-authored claim.
        result += newline + f'<!-- Abstract source: {candidate.source_url} -->' + newline + abstract + newline
    else:
        result += publication.body
    return result


def doi_link(value):
    url = safe_url(value)
    return url if url and re.match(r'^https://doi\.org/10\.\d{4,9}/\S+$', url) else ''


class MetadataClient:
    def __init__(self, contact='zhuotaoliu@tsinghua.edu.cn'):
        self.contact = contact
        self.last_request = 0.0
        self.successes = 0

    def get(self, url):
        for attempt in range(2):
            time.sleep(max(0, 3.1 - (time.monotonic() - self.last_request)))
            self.last_request = time.monotonic()
            try:
                request = Request(url, headers={'User-Agent': f'ZhuotaoLiuPublicationUpdater/1.0 (mailto:{self.contact})'})
                with urlopen(request, timeout=25) as response:
                    data = response.read(5_000_001)
                    if len(data) > 5_000_000:
                        raise ValueError('Metadata response exceeded size limit')
                    self.successes += 1
                    return data
            except (HTTPError, URLError, TimeoutError, ValueError) as exc:
                if isinstance(exc, HTTPError) and exc.code == 404:
                    raise LookupError('Record not indexed by this provider') from exc
                if attempt == 0:
                    delay = 5
                    if isinstance(exc, HTTPError):
                        retry = exc.headers.get('Retry-After', '')
                        if retry:
                            try:
                                seconds = int(retry) if retry.isdigit() else (parsedate_to_datetime(retry) - datetime.now(timezone.utc)).total_seconds()
                            except (TypeError, ValueError):
                                seconds = 5
                            if seconds > 30:
                                raise RuntimeError(f'{urlsplit(url).hostname}: retry deferred until a later run') from exc
                            delay = max(5, seconds)
                    time.sleep(delay)
                else:
                    raise RuntimeError(f'{urlsplit(url).hostname}: {exc}') from exc

    def crossref(self, metadata):
        known = doi_link(metadata.get('paper'))
        try:
            if known:
                url = 'https://api.crossref.org/works/' + quote(urlsplit(known).path.lstrip('/'), safe='')
                items = [json.loads(self.get(url + '?' + urlencode({'mailto': self.contact})))['message']]
            else:
                params = urlencode({'query.bibliographic': metadata['title'], 'query.author': 'Zhuotao Liu',
                                    'rows': 5, 'mailto': self.contact})
                items = json.loads(self.get('https://api.crossref.org/works?' + params))['message']['items']
        except LookupError:
            return []
        records = []
        for item in items:
            doi = item.get('DOI', '')
            if not re.match(r'^10\.\d{4,9}/\S+$', doi):
                continue
            paper = 'https://doi.org/' + quote(doi, safe='/():;._-')
            year = None
            for field in ('published-print', 'published', 'published-online', 'issued'):
                dates = item.get(field, {}).get('date-parts', [])
                if dates and dates[0]:
                    year = dates[0][0]
                    break
            pdfs = [link.get('URL', '') for link in item.get('link', [])
                    if link.get('content-type') == 'application/pdf' and safe_url(link.get('URL', ''))
                    and link.get('intended-application') != 'text-mining'
                    and not urlsplit(link['URL']).hostname.startswith('api.')]
            records.append(Candidate(
                title=(item.get('title') or [''])[0],
                authors=[' '.join(filter(None, [a.get('given', ''), a.get('family', '')])) for a in item.get('author', [])],
                year=year, source_url=paper, paper=paper,
                pdf=pdfs[0] if len(set(pdfs)) == 1 else '', abstract=item.get('abstract') or ''))
        return records

    def openalex(self, metadata):
        paper = doi_link(metadata.get('paper'))
        try:
            if paper:
                url = 'https://api.openalex.org/works/' + quote(paper, safe=':/')
                items = [json.loads(self.get(url))]
            else:
                url = 'https://api.openalex.org/works?' + urlencode({'search': metadata['title'], 'per-page': 5})
                items = json.loads(self.get(url))['results']
        except LookupError:
            return []
        records = []
        for item in items:
            source = item.get('id', '')
            if not re.fullmatch(r'https://openalex\.org/W\d+', source):
                continue
            words = {}
            for word, positions in (item.get('abstract_inverted_index') or {}).items():
                if not isinstance(word, str) or not isinstance(positions, list):
                    raise ValueError('Malformed OpenAlex abstract')
                for pos in positions:
                    if type(pos) is not int or not 0 <= pos < 10000 or pos in words:
                        raise ValueError('Malformed OpenAlex abstract positions')
                    words[pos] = word
            abstract = ' '.join(words[i] for i in sorted(words))
            location = item.get('best_oa_location') or {}
            primary = item.get('primary_location') or {}
            landing = safe_url(primary.get('landing_page_url', ''))
            doi = safe_url(item.get('doi'))
            preprint = ''
            pdf = ''
            for loc in (primary, location):
                candidate_url = safe_url(loc.get('landing_page_url', ''))
                if candidate_url and urlsplit(candidate_url).hostname == 'arxiv.org':
                    preprint = candidate_url
            # Repository/preprint PDFs can differ from the accepted publication.
            if location.get('version') == 'publishedVersion' and item.get('type') != 'preprint':
                pdf = safe_url(location.get('pdf_url', ''))
                if pdf and urlsplit(pdf).hostname in ('content.openalex.org', 'arxiv.org'):
                    pdf = ''
            records.append(Candidate(
                title=item.get('display_name') or '',
                authors=[a.get('author', {}).get('display_name', '') for a in item.get('authorships', [])],
                year=item.get('publication_year'), source_url=source,
                paper=(doi or landing) if item.get('type') != 'preprint' else '',
                pdf=pdf, preprint=preprint or (landing if item.get('type') == 'preprint' else ''),
                abstract=abstract, abstract_is_html=False))
        return records

    def arxiv(self, metadata):
        words = ' '.join(re.findall(r'\w+', metadata['title']))
        query = f'ti:"{words}" AND au:"Liu"'
        url = 'https://export.arxiv.org/api/query?' + urlencode({'search_query': query, 'max_results': 5})
        root = ET.fromstring(self.get(url))
        ns = {'a': 'http://www.w3.org/2005/Atom'}
        records = []
        for entry in root.findall('a:entry', ns):
            identifier = entry.findtext('a:id', '', ns)
            if not re.match(r'^https?://arxiv\.org/abs/(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?$', identifier):
                continue
            identifier = re.sub(r'v\d+$', '', identifier.replace('http://', 'https://', 1))
            date = entry.findtext('a:published', '', ns)
            records.append(Candidate(
                title=entry.findtext('a:title', '', ns),
                authors=[a.findtext('a:name', '', ns) for a in entry.findall('a:author', ns)],
                year=int(date[:4]) if re.match(r'^\d{4}-', date) else None,
                source_url=identifier, preprint=identifier,
                abstract=entry.findtext('a:summary', '', ns), abstract_is_html=False))
        return records


def eligible(publication):
    data = publication.metadata
    if data.get('draft') or data.get('category') == 'patent' or data.get('auto_enrich') is False:
        return False
    if 'auto_enrich' in data and type(data['auto_enrich']) is not bool:
        raise ValueError(f'{publication.path}: auto_enrich must be true or false')
    if (not isinstance(data.get('title'), str) or not isinstance(data.get('authors'), list)
            or not data['authors'] or type(data.get('year')) is not int or not data.get('venue')):
        raise ValueError(f'{publication.path}: title, authors, venue, and integer year are required')
    # Minimal entries are enrolled automatically. Existing complete entries stay untouched.
    incomplete = not publication.body.strip() or 'paper' not in data
    tracking = data.get('auto_enrich') is True and 'pdf' not in data
    return incomplete or tracking


def run(directory, client, write=False, limit=None):
    publications = [load_publication(p) for p in sorted(directory.glob('*.md')) if not p.name.startswith('_')]
    publications = sorted((p for p in publications if eligible(p)), key=lambda p: (-p.metadata['year'], p.path.name))
    if limit is not None:
        publications = publications[:limit]
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'mode': 'write' if write else 'dry-run',
              'checked': len(publications), 'changed': [], 'pending': [], 'warnings': []}
    unavailable = set()
    for publication in publications:
        current = publication
        sources = []
        for name in ('crossref', 'openalex', 'arxiv'):
            if name in unavailable or not hasattr(client, name):
                continue
            if name == 'openalex' and current.body.strip() and 'paper' in current.metadata and 'pdf' in current.metadata:
                continue
            # Publisher metadata is preferred; arXiv is explicitly a preprint link.
            if name == 'arxiv' and current.body.strip() and ('pdf' in current.metadata or 'preprint' in current.metadata):
                continue
            try:
                candidates = getattr(client, name)(current.metadata)
                candidate = choose_candidate(current.metadata, candidates)
                if candidate:
                    updated = apply_candidate(current, candidate)
                    if updated != current.raw:
                        match = FRONTMATTER.match(updated)
                        current = Publication(current.path, yaml.load(match[1], Loader=UniqueLoader), updated[match.end():], updated)
                        sources.append(candidate.source_url)
            except (RuntimeError, ValueError, LookupError, TypeError, ET.ParseError) as exc:
                report['warnings'].append({'file': publication.path.name, 'provider': name, 'error': str(exc)})
                if isinstance(exc, RuntimeError):
                    # After the client's bounded retry, leave this service alone until
                    # the next scheduled run. Other sources can still enrich papers.
                    unavailable.add(name)
        if current.raw != publication.raw:
            if write:
                # Refuse to overwrite an edit made during the network lookups.
                if publication.path.read_bytes().decode('utf-8') != publication.raw:
                    raise RuntimeError(f'{publication.path}: file changed during enrichment; no overwrite')
                publication.path.write_bytes(current.raw.encode('utf-8'))
            report['changed'].append({'file': publication.path.name, 'sources': sources})
        else:
            report['pending'].append(publication.path.name)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parents[1] / 'content/publications')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--limit', type=int, help='Inspect only this many eligible entries (for a dry-run sample)')
    args = parser.parse_args()
    if args.limit is not None and (args.limit < 1 or args.write):
        parser.error('--limit must be positive and is only supported for dry runs')
    client = MetadataClient()
    report = run(args.directory, client, args.write, args.limit)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    if report['checked'] and report['warnings'] and not client.successes:
        raise SystemExit('All metadata lookups failed; leaving publication files unchanged.')


if __name__ == '__main__':
    main()
