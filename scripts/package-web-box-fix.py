#!/usr/bin/env python3
"""Package the printer-web companion fix without vendor bundles or LAN settings.

The directory form is included in the slicer's resources by
write-build-manifest.py. The ZIP is a separate main-build download. Neither form
installs on a printer or changes slicer/printer configuration.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / 'firmware-fixes/qidi-fluidd-box-status'
FILES = ('box-status.js', 'patch_bundle.py', 'test-model.cjs', 'test-temperature.cjs',
         'test-status.cjs', 'check_browser.py', 'fixtures/status.json')


def payload():
    files = {name: (FIX / name).read_bytes() for name in FILES}
    files['LICENSE'] = (ROOT / 'LICENSE').read_bytes()
    manifest = {
        'component': 'QIDI Fluidd Box status and manual temperature companion fix',
        'integration_commit': subprocess.check_output(
            ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
        'installation': 'Printer-hosted web files; see patch_bundle.py usage. Installation is manual.',
        'behavior': ['Modern Box material/presence/loaded-slot display',
                     'Manual target 0-65 C, respecting lower configured limits',
                     'Material profile maximum displayed separately'],
        'vendor_files_included': False,
        'automatic_printer_changes': False,
        'files': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
    }
    files['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--directory', action='store_true')
    args = parser.parse_args()
    files = payload()
    if args.directory:
        args.output.mkdir(parents=True, exist_ok=True)
        for name, data in files.items():
            target = args.output / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(args.output, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name, data in files.items():
                info = zipfile.ZipInfo('qidi-web-box-fix/' + name)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data)
    print('Packaged QIDI web Box companion fix:', args.output)


if __name__ == '__main__':
    main()
