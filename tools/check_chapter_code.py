"""Build and run every printed chapter program and compare its displayed output."""
from __future__ import annotations

import datetime
import difflib
import hashlib
import json
from pathlib import Path
import platform
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from code_lab import chapter_programs, passed, run_program


def main():
    results = {}
    for path in sorted(ROOT.glob('chapter-[0-9][0-9]-*.html')):
        checks = []
        for i, program in enumerate(chapter_programs(path), 1):
            with tempfile.TemporaryDirectory(prefix='hpsc-code-checks-') as folder:
                code, out, err = run_program(program, folder)
            ok = passed(program, code, out)
            actual = out.strip('\n')
            checks.append({'listing': i, 'file': program['file'], 'needs': program['needs'],
                           'check': program['check'], 'returncode': code, 'passed': ok,
                           'listing_sha256': hashlib.sha256(program['code'].encode()).hexdigest(),
                           'stderr_tail': '' if ok else err[-800:],
                           'output_diff': [] if ok or program['check'] != 'exact' else
                           list(difflib.unified_diff(program['expected'].splitlines(), actual.splitlines(),
                                                     fromfile='printed', tofile='executed', lineterm=''))[:40]})
        status = 'passed' if all(c['passed'] for c in checks) else 'failed'
        results[path.name] = {'status': status if checks else 'no runnable listings', 'checks': checks}
        print(path.name, results[path.name]['status'], flush=True)
    ok = all(r['status'] != 'failed' for r in results.values())
    report = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'passed' if ok else 'failed',
              'scope': ('Actual isolated build and execution of each runnable listing; exact printed-output comparison '
                        'where data-check="exact", successful exit only where data-check="returncode"; not a scientific review'),
              'machine': 'WSL Ubuntu 24.04, gcc 13.3 (OpenMP, OpenACC nvptx offload), Open MPI, CUDA 13.3, '
                         'NVIDIA GeForce RTX 3050 Laptop GPU (sm_86), 12 logical CPUs',
              'host': platform.platform(), 'chapters': results}
    (ROOT / 'chapter-code-validation.json').write_bytes((json.dumps(report, indent=2) + '\n').encode())
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
