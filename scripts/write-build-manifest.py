#!/usr/bin/env python3
"""Embed source provenance in the packaged resources; no credentials or host paths."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
source = Path(sys.argv[1]).resolve()
pins = json.loads((root / 'sources.json').read_text())
manifest = {
    'application': 'OrcaSlicer QIDI',
    'integration_commit': subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip(),
    'sources': pins,
    'patches': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root / 'patches').glob('*.patch'))},
    'build_instructions': 'docs/build.md in the integration repository',
    'physical_printer_verification': False,
}
(source / 'resources/qidi-port-build.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('Recorded source pins and', len(manifest['patches']), 'patch checksums in packaged resources.')
