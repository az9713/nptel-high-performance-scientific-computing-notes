"""Build and run every printed chapter program and compare its displayed output."""
from __future__ import annotations

import argparse
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from code_lab import chapter_programs, passed, run_program, temporary_directory


def program_fingerprint(programs):
    payload = json.dumps(programs, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--chapter', type=int, action='append', help='Run only this chapter (repeatable)')
    selection.add_argument('--file', type=Path, help='Run a staged chapter file inside the workspace')
    parser.add_argument('--merge-report', action='store_true', help='Retain matching verified chapter results')
    parser.add_argument('--report', type=Path, help='Write selected-chapter evidence to this workspace file')
    args = parser.parse_args()
    paths = sorted(ROOT.glob('chapter-[0-9][0-9]-*.html'))
    if args.file:
        staged = args.file.resolve()
        if not staged.is_relative_to(ROOT.parent.resolve()) or not staged.is_file() or not staged.name.startswith('chapter-'):
            parser.error('--file must be a chapter file inside the workspace')
        paths = [p for p in paths if p.name != staged.name] + [staged]
        selected = [staged]
    else:
        selected = [p for p in paths if not args.chapter or int(p.name[8:10]) in args.chapter]
    if args.chapter and ({int(p.name[8:10]) for p in selected} != set(args.chapter) or len(selected) != len(set(args.chapter))):
        parser.error('Every selected chapter must have exactly one chapter file')
    report_path = args.report.resolve() if args.report else ROOT / 'chapter-code-validation.json'
    if args.report:
        if not report_path.is_relative_to(ROOT.parent.resolve()):
            parser.error('--report must be inside the workspace')
        report_path.parent.mkdir(parents=True, exist_ok=True)
        if not args.merge_report:
            paths = list(selected)
    previous = json.loads(report_path.read_text(encoding='utf-8')) if args.merge_report and report_path.exists() else {}
    results = {}
    for path in paths:
        if path in selected:
            continue
        fingerprint = program_fingerprint(chapter_programs(path))
        old = previous.get('chapters', {}).get(path.name, {})
        if old.get('status') == 'passed' and old.get('fingerprint_sha256') == fingerprint and old.get('checked_at_utc'):
            results[path.name] = old
        else:
            results[path.name] = {'status': 'needs full rerun', 'fingerprint_sha256': fingerprint, 'checks': []}
    for path in selected:
        checks = []
        programs = chapter_programs(path)
        for i, program in enumerate(programs, 1):
            with temporary_directory(prefix='hpsc-code-checks-') as folder:
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
        results[path.name] = {'status': status if checks else 'no runnable listings', 'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'fingerprint_sha256': program_fingerprint(programs),
                              'execution_profile': ('Workspace-contained execution; MPI self,tcp transport.' if os.environ.get('HPSC_RUNTIME_ROOT') else 'Default launcher execution environment.'),
                              'checks': checks}
        print(path.name, results[path.name]['status'], flush=True)
    ok = all(r['status'] in ('passed', 'no runnable listings') for r in results.values())
    report = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'passed' if ok else 'failed',
              'timestamp_scope': 'Aggregate update only; per-chapter checked_at_utc records actual execution time.',
              'report_scope': 'Selected chapters only' if args.report and not args.merge_report else 'Current written chapter inventory',
              'scope': ('Cumulative actual execution evidence; retained results keep their original timestamps and execution profiles. '
                        'Historical pre-workspace-policy results were not rerun under the current runtime. '
                        'Exact printed-output comparison where data-check="exact", successful exit only where '
                        'data-check="returncode"; input identity does not imply environment equivalence; not a scientific review'),
              'machine': 'WSL Ubuntu 24.04, gcc 13.3 (OpenMP, OpenACC nvptx offload), Open MPI, CUDA 13.3, '
                         'NVIDIA GeForce RTX 3050 Laptop GPU (sm_86), 12 logical CPUs',
              'host': platform.platform(), 'chapters': results}
    report_path.write_bytes((json.dumps(report, indent=2) + '\n').encode())
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
