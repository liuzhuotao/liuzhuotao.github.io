import { readdir, readFile, access } from 'node:fs/promises';
import path from 'node:path';

// Check rendered HTML so template regressions are caught as well as data typos.
const root = path.resolve(process.argv[2] ?? 'public');
const publications = path.join(root, 'publications');
await access(path.join(publications, 'index.html'));

async function* htmlFiles(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const filename = path.join(directory, entry.name);
    if (entry.isDirectory()) yield* htmlFiles(filename);
    else if (entry.name.endsWith('.html')) yield filename;
  }
}

let pages = 0;
let links = 0;
const failures = [];
for await (const filename of htmlFiles(publications)) {
  pages++;
  const html = await readFile(filename, 'utf8');
  const hrefs = html.matchAll(/\bhref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))/gi);
  for (const match of hrefs) {
    const href = match[1] ?? match[2] ?? match[3];
    if (!/^https?:\/\//i.test(href)) continue;
    links++;
    try {
      const url = new URL(href);
      // A URL inside a query/fragment may be intentional; one in the path is
      // the DOI-prefix / repeated-paste regression this check guards against.
      if (/https?:\/\//i.test(url.pathname)) throw new Error('embedded URL in path');
    } catch (error) {
      failures.push(`${path.relative(root, filename)}: ${href} (${error.message})`);
    }
  }
}

if (failures.length) {
  console.error(failures.join('\n'));
  process.exitCode = 1;
} else {
  console.log(`Checked ${links} external links in ${pages} publication pages: no malformed URLs.`);
}
