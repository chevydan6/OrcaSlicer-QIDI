#!/usr/bin/env python3
"""Embed source provenance in the packaged resources; no credentials or host paths."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import shutil

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
companion = source / 'resources/qidi-web-box-fix'
subprocess.run([sys.executable, str(root / 'scripts/package-web-box-fix.py'),
                str(companion), '--directory'], check=True)
manifest['printer_web_companion'] = {
    'path': 'resources/qidi-web-box-fix',
    'manifest_sha256': hashlib.sha256((companion / 'manifest.json').read_bytes()).hexdigest(),
    'installed_automatically': False,
}
(source / 'resources/qidi-port-build.json').write_text(json.dumps(manifest, indent=2) + '\n')
shutil.copyfile(root / 'LICENSE', source / 'resources/LICENSE')
print('Recorded source pins and', len(manifest['patches']), 'patch checksums in packaged resources.')
