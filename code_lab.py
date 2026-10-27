"""List or run the programs printed in a High Performance Scientific Computing chapter.

A runnable listing is a <pre><code data-file=...> block. Its build and run commands sit in
data-build and data-run; the next <pre><code class="output"> block is its printed output.
data-check="exact" (default) compares output byte for byte after trimming; "returncode"
accepts any output from a successful run (timings, thread interleaving). data-needs lists
"gpu" or "mpi" requirements. Programs run in a Linux shell: natively on Linux, through WSL
on Windows.
"""
from __future__ import annotations

import argparse
import html
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
ENV = 'export PATH="$PATH:/usr/local/cuda/bin"; export OMPI_MCA_rmaps_base_oversubscribe=1\n'


def attr(attrs, name, default=''):
    match = re.search(rf'{name}="([^"]*)"', attrs)
    return html.unescape(match[1]) if match else default


def chapter_programs(path):
    text = path.read_bytes().decode('utf-8')
    if '<!-- BOOK-CONTENT-START -->' in text:
        text = text.split('<!-- BOOK-CONTENT-START -->', 1)[1].split('<!-- BOOK-CONTENT-END -->', 1)[0]
    blocks = re.findall(r'<pre\b[^>]*>\s*<code([^>]*)>(.*?)</code>\s*</pre>', text, re.S)
    clean = lambda value: html.unescape(re.sub(r'<[^>]+>', '', value)).replace('\r\n', '\n')
    result = []
    for i, (attrs, source) in enumerate(blocks):
        if 'data-file=' not in attrs:
            continue
        if i + 1 >= len(blocks) or 'output' not in blocks[i + 1][0]:
            raise ValueError(f'{path.name}: listing {attr(attrs, "data-file")} lacks its printed output')
        result.append({'file': attr(attrs, 'data-file'), 'build': attr(attrs, 'data-build'),
                       'run': attr(attrs, 'data-run'), 'check': attr(attrs, 'data-check', 'exact'),
                       'needs': attr(attrs, 'data-needs').split(), 'code': clean(source),
                       'expected': clean(blocks[i + 1][1]).strip('\n')})
    return result


def linux_path(folder):
    if os.name != 'nt':
        return str(folder)
    drive, rest = str(folder).split(':', 1)
    return f'/mnt/{drive.lower()}' + rest.replace('\\', '/')


def run_program(program, folder):
    """Write the listing, build it, run it; return (returncode, stdout, stderr)."""
    folder = Path(folder)
    (folder / program['file']).write_bytes(program['code'].encode('utf-8'))
    script = ENV + f'cd "{linux_path(folder)}"\n'
    if program['build']:
        script += f'{program["build"]} || exit 97\n'
    script += program['run'] + '\n'
    (folder / 'run.sh').write_bytes(script.encode('utf-8'))
    shell = ['wsl', '-d', os.environ.get('HPSC_WSL_DISTRO', 'Ubuntu'), '--', 'bash'] if os.name == 'nt' else ['bash']
    run = subprocess.run(shell + [linux_path(folder / 'run.sh')], capture_output=True, timeout=600)
    decode = lambda b: b.replace(b'\0', b'').decode('utf-8', 'replace').replace('\r\n', '\n')
    stderr = '\n'.join(l for l in decode(run.stderr).splitlines() if 'wslconfig' not in l)
    return run.returncode, decode(run.stdout), stderr


def passed(program, returncode, stdout):
    if returncode:
        return False
    return program['check'] == 'returncode' or stdout.strip('\n') == program['expected']


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--chapter', type=int, help='Run the programs of one chapter')
    parser.add_argument('--skip', nargs='*', default=[], help='Requirements to skip, e.g. gpu mpi')
    args = parser.parse_args()
    paths = sorted(ROOT.glob('chapter-[0-9][0-9]-*.html'))
    if args.chapter is None:
        for path in paths:
            programs = chapter_programs(path)
            print(f'{int(path.name[8:10]):02d}: {path.stem[11:]} ({len(programs)} program(s): '
                  f'{", ".join(p["file"] for p in programs)})')
        return
    selected = [p for p in paths if int(p.name[8:10]) == args.chapter]
    if len(selected) != 1:
        parser.error('Expected one chapter file for the selected number')
    failures = 0
    for program in chapter_programs(selected[0]):
        if set(program['needs']) & set(args.skip):
            print(f'--- {program["file"]}: skipped (needs {" ".join(program["needs"])})')
            continue
        with tempfile.TemporaryDirectory(prefix='hpsc-lab-') as folder:
            code, out, err = run_program(program, folder)
        ok = passed(program, code, out)
        failures += not ok
        print(f'--- {program["file"]}: {"passed" if ok else "FAILED"} ({program["check"]})')
        print(out, end='')
        if not ok and err:
            print(err[-1500:], file=sys.stderr)
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
