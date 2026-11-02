#!/usr/bin/env python3
"""Verify the patch series reproduces the local downstream tree using a temporary index."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
repo = root / 'OrcaSlicer'
pin = json.loads((root / 'sources.json').read_text())['orca']['commit']
patches = sorted((root / 'patches').glob('*.patch'))
with tempfile.TemporaryDirectory(prefix='qidi-patch-index-') as directory:
    environment = dict(os.environ, GIT_INDEX_FILE=str(Path(directory) / 'index'))
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=repo, env=environment, text=True).strip()
    git('read-tree', pin)
    for patch in patches:
        git('apply', '--cached', str(patch))
    actual = git('write-tree')
    expected = git('rev-parse', 'HEAD^{tree}')
    if actual != expected:
        raise SystemExit(f'FAIL: patched tree {actual} differs from local HEAD {expected}')
    print(f'PASS: {len(patches)} patches applied to {pin} reproduce downstream tree {actual}')
