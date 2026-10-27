"""Check the public book inventory, chapter-body digests, and evidence links."""
from __future__ import annotations

import datetime
import hashlib
import json
from pathlib import Path
import re

from build_book import original_body, read

ROOT = Path(__file__).resolve().parents[1]


def main():
    failures = []
    manifest = json.loads(read(ROOT / 'source-manifest.json'))
    completion = json.loads(read(ROOT / 'completion.json'))
    editorial = json.loads(read(ROOT / 'editorial-review-summary.json'))
    paths = sorted(ROOT.glob('chapter-[0-9][0-9]-*.html'))
    # ponytail: partial edition; a manifest chapter with status 'pending' is not written yet.
    unwritten = [c['order'] for c in manifest['chapters'] if c.get('chapter_status') == 'pending']
    if len(manifest['chapters']) != 31 or len(paths) != 31 - len(unwritten):
        failures.append('Expected 31 manifest entries and one chapter file per written chapter')
    listings = solutions = 0
    for path in paths:
        body = original_body(read(path))
        actual = hashlib.sha256(body.encode()).hexdigest()
        if completion['chapter_body_sha256'].get(path.name) != actual:
            failures.append(f'{path.name}: baseline chapter-body mismatch')
        if not path.with_suffix('.meta.json').is_file():
            failures.append(f'{path.name}: missing source sidecar')
        listings += len(re.findall(r'<code[^>]*data-file="', body))
        solutions += len(re.findall(r'<summary\b[^>]*>\s*(?:Solution|Worked solution)', body, re.I))
    required = ('README.md', 'WORKFLOW.md', 'index.html', 'source-map.html', 'references.html',
                'code-lab.html', 'code_lab.py', 'source-validation-summary.json',
                'chapter-code-validation.json', 'reader-validation.json', 'assets/site-preview.png')
    for name in required:
        if not (ROOT / name).is_file():
            failures.append(f'Missing public file: {name}')
    for name in ('README.md', 'WORKFLOW.md'):
        for target in re.findall(r'\]\(([^)]+)\)', read(ROOT / name)):
            if '://' not in target and target not in ('package-validation.json', 'publication-validation.json') and not (ROOT / target.split('#')[0]).exists():
                failures.append(f'{name}: broken relative link {target}')
    pending = editorial.get('final_independent_signoff_pending_chapters', [])
    if any(c['order'] not in pending + unwritten and c.get('chapter_status') != 'reviewed and locally validated'
           for c in manifest['chapters']):
        failures.append('A chapter without final sign-off is not listed as pending')
    report = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'failed' if failures else 'passed', 'scope': 'Public package inventory and exact chapter-body preservation, not scientific acceptance',
              'chapter_count': len(paths), 'runnable_listings': listings, 'worked_solution_disclosures': solutions,
              'failures': failures, 'final_independent_signoff_pending_chapters': pending,
              'unwritten_chapters': unwritten}
    (ROOT / 'package-validation.json').write_bytes((json.dumps(report, indent=2) + '\n').encode())
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
