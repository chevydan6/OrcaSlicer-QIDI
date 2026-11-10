#!/usr/bin/env python3
"""Verify the deliverable and normal build-resource integration without a printer."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def run(script, *args, check=True):
    return subprocess.run([sys.executable, str(ROOT / script), *map(str, args)],
                          capture_output=True, text=True, check=check)


with tempfile.TemporaryDirectory(prefix='qidi-web-package-') as tmp:
    tmp = Path(tmp)
    source = tmp / 'source'
    (source / 'resources').mkdir(parents=True)
    run('scripts/write-build-manifest.py', source)
    build = json.loads((source / 'resources/qidi-port-build.json').read_text())
    companion = build['printer_web_companion']
    assert companion['installed_automatically'] is False
    directory = source / companion['path']
    raw = (directory / 'manifest.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == companion['manifest_sha256']
    manifest = json.loads(raw)
    assert manifest['integration_commit'] == build['integration_commit']
    assert manifest['vendor_files_included'] is False
    assert manifest['automatic_printer_changes'] is False
    for name, digest in manifest['files'].items():
        assert hashlib.sha256((directory / name).read_bytes()).hexdigest() == digest
    first, second = tmp / 'first.zip', tmp / 'second.zip'
    run('scripts/package-web-box-fix.py', first)
    run('scripts/package-web-box-fix.py', second)
    assert first.read_bytes() == second.read_bytes()
    with zipfile.ZipFile(first) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(manifest['files']) + 1
        for name in [*manifest['files'], 'manifest.json']:
            assert archive.read('qidi-web-box-fix/' + name) == (directory / name).read_bytes()
        archive.extractall(tmp / 'extracted')
    # Execute the shipped tests from the extracted archive, not the workspace.
    for test in ('test-model.cjs', 'test-temperature.cjs'):
        subprocess.run(['node', str(tmp / 'extracted/qidi-web-box-fix' / test)],
                       check=True, capture_output=True, text=True)
    bad = tmp / 'unknown-vendor.js'
    bad.write_text('Unrecognized firmware must not be patched.')
    out = tmp / 'fixed.js'
    result = run('firmware-fixes/qidi-fluidd-box-status/patch_bundle.py', bad, out, check=False)
    assert result.returncode != 0 and not out.exists()
    assert 'differs from the inspected version' in result.stderr
    result = run('firmware-fixes/qidi-fluidd-box-status/patch_bundle.py', bad, bad, check=False)
    assert result.returncode != 0 and bad.read_text() == 'Unrecognized firmware must not be patched.'
print('PASS: main build resources, source checksums, reproducible ZIP, extracted tests and unknown-vendor/input protection')
