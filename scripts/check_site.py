"""Check catalog evidence fields, generated page, local links, and dist consistency."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.resources = []
        self.libraries = []
        self.h1 = 0
        self.in_catalog = False
        self.catalog = ''
        self.lang = None
        self.count_live = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'h1':
            self.h1 += 1
        if 'data-resource' in attrs:
            self.resources.append(attrs['data-resource'])
        if 'data-library' in attrs:
            self.libraries.append(attrs['data-library'])
        for name in ['href', 'src']:
            if name in attrs:
                self.links.append(attrs[name])
        if attrs.get('id') == 'result-count':
            self.count_live = attrs.get('aria-live') == 'polite'
        if tag == 'script' and attrs.get('id') == 'catalog-data':
            self.in_catalog = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_catalog = False

    def handle_data(self, data):
        if self.in_catalog:
            self.catalog += data


def main():
    data = json.loads((ROOT / 'data/catalog.json').read_text(encoding='utf-8'))
    entries = data['entries']
    ids = [x['id'] for x in entries]
    skills = [x for x in entries if x['kind'] == 'skill']
    libraries = [x for x in entries if x['kind'] == 'library']
    assert len(entries) == 13 and len(ids) == len(set(ids)), 'Expected 13 distinct catalog entries'
    assert len(skills) == 12 and len(libraries) == 1, '12 skill entries; 1 separate supporting library'
    assert sorted(x['source_post_number'] for x in entries if x['origin'] == 'source-post') == [9, 10]
    assert sum(x['origin'] == 'supplement' for x in entries) == 11
    assert sum(x.get('application') == 'studio-desk' for x in skills) == 4
    for entry in entries:
        for key in ['name', 'repo', 'category', 'kind', 'origin', 'headline', 'summary', 'best_for',
                    'requirements', 'limits', 'install', 'install_context', 'task_brief', 'license', 'license_note']:
            assert entry.get(key), f'{entry["id"]}: missing {key}'
        assert re.fullmatch(r'[0-9a-f]{40}', entry['revision']), 'Revision must be a full commit SHA'
        assert entry['verified_on'] == data['verified_on']
        assert entry['verification'] == 'primary_source_reviewed_not_runtime_tested'
        for key in ['source_url', 'readme_url', 'license_url']:
            assert f'/blob/{entry["revision"]}/' in entry[key], f'{entry["id"]}: unpinned {key}'
        assert entry['repository_url'] == 'https://github.com/' + entry['repo']
        assert entry['category'] in ['direction', 'review', 'interaction', 'implementation', 'design-system', 'workflow']
    page = Page()
    page.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
    assert page.lang == 'ja' and page.h1 == 1
    assert len(page.ids) == len(set(page.ids)), 'Duplicate HTML id'
    assert page.resources == [x['id'] for x in skills], 'Catalog/page skill order mismatch'
    assert page.libraries == [x['id'] for x in libraries], 'Supporting library separation mismatch'
    assert json.loads(page.catalog) == skills, 'Search data must contain skills only'
    assert page.count_live, 'Result count must announce changes'
    for required_id in ['search', 'origin', 'filters', 'empty', 'copy-status', 'catalog', 'main']:
        assert required_id in page.ids, f'Missing UI element {required_id}'
    for link in page.links:
        parsed = urlsplit(link)
        if parsed.scheme:
            assert parsed.scheme == 'https', f'Unexpected external URL scheme: {link}'
            continue
        if parsed.path:
            assert (ROOT / unquote(parsed.path)).is_file(), f'Broken local file link: {link}'
        elif parsed.fragment:
            assert unquote(parsed.fragment) in page.ids, f'Broken fragment: {link}'
    for filename in ['README.md', 'ATTRIBUTION.md', 'RESEARCH.md']:
        content = (ROOT / filename).read_text(encoding='utf-8')
        if filename != 'RESEARCH.md':
            for entry in entries:
                assert entry['license_url'] in content, f'{filename}: missing evidence link'
        for link in re.findall(r'\]\(([^)]+)\)', content):
            if not urlsplit(link).scheme:
                assert (ROOT / link).is_file(), f'{filename}: broken local link {link}'
    css = (ROOT / 'styles.css').read_text(encoding='utf-8')
    assert 'prefers-reduced-motion' in css and ':focus-visible' in css
    filenames = ['index.html', 'styles.css', 'app.js', 'README.md', 'RESEARCH.md', 'ATTRIBUTION.md', 'LICENSE', 'data/catalog.json', 'data/research-2026-10-13.json', 'data/research-official-2026-10-13.json']
    filenames.extend(str(p.relative_to(ROOT)) for p in (ROOT / 'examples/studio-desk').rglob('*') if p.is_file())
    for filename in filenames:
        assert (ROOT / filename).read_bytes() == (ROOT / 'dist' / filename).read_bytes(), f'Stale dist file: {filename}'
    print(f'PASS: {len(entries)} records, pinned evidence, 12 skills/1 supporting library, Japanese page, {len(page.links)} links, IDs, accessibility hooks, example files, dist consistency')


if __name__ == '__main__':
    main()
