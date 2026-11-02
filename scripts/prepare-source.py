#!/usr/bin/env python3
"""Create a pinned, patched Orca checkout without touching existing directories."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
destination = Path(sys.argv[1] if len(sys.argv) == 2 else root / 'build/source').resolve()
if destination.exists():
    raise SystemExit(f'Refusing to replace existing directory: {destination}')
source = json.loads((root / 'sources.json').read_text())['orca']
subprocess.run(['git', 'init', str(destination)], check=True)
def git(*args):
    subprocess.run(['git', '-C', str(destination), *args], check=True)
git('remote', 'add', 'origin', source['repository'])
git('fetch', '--depth', '1', 'origin', source['commit'])
git('checkout', '--detach', source['commit'])
for patch in sorted((root / 'patches').glob('*.patch')):
    git('apply', '--index', str(patch))
print(f'Prepared {destination}; downstream patches are staged for inspection.')
