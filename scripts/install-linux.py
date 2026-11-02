#!/usr/bin/env python3
"""Install a built AppImage under the current user's home; never launch it."""
import hashlib
from pathlib import Path
import os
import shlex
import shutil
import sys

if len(sys.argv) != 2:
    raise SystemExit('Usage: install-linux.py PATH_TO_BUILT_APPIMAGE')
image = Path(sys.argv[1]).resolve()
with image.open('rb') as stream:
    if stream.read(4) != b'\x7fELF':
        raise SystemExit('Expected an ELF AppImage')
digest = hashlib.sha256(image.read_bytes()).hexdigest()
home = Path.home()
directory = home / '.local/opt/orca-slicer-qidi' / digest[:16]
directory.mkdir(parents=True, exist_ok=True)
installed = directory / 'OrcaSlicer-QIDI.AppImage'
if installed.exists():
    if hashlib.sha256(installed.read_bytes()).hexdigest() != digest:
        raise SystemExit('Existing installation has unexpected contents')
else:
    shutil.copyfile(image, installed)
installed.chmod(0o755)
launcher = home / '.local/bin/orca-slicer-qidi'
launcher.parent.mkdir(parents=True, exist_ok=True)
marker = '# Managed by OrcaSlicer-QIDI installer'
if launcher.exists() and marker not in launcher.read_text():
    raise SystemExit(f'Refusing to overwrite unrelated launcher: {launcher}')
launcher.write_text('#!/bin/sh\n' + marker + '\n'
    'set -eu\n'
    'qidi_config="${XDG_CONFIG_HOME:-$HOME/.config}/OrcaSlicer-QIDI"\n'
    'mkdir -p "$qidi_config"\n'
    f'exec {shlex.quote(str(installed))} --datadir "$qidi_config" "$@"\n')
launcher.chmod(0o755)
desktop = Path(os.environ.get('XDG_DATA_HOME', str(home / '.local/share'))) / 'applications/orca-slicer-qidi.desktop'
desktop.parent.mkdir(parents=True, exist_ok=True)
if desktop.exists() and marker not in desktop.read_text():
    raise SystemExit(f'Refusing to overwrite unrelated desktop entry: {desktop}')
escaped = str(launcher).replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$').replace('%', '%%')
desktop.write_text('[Desktop Entry]\n' + marker + '\nType=Application\n'
    'Name=OrcaSlicer QIDI (Custom)\nComment=Personal MAX4 and QIDI Box build\n'
    f'Exec="{escaped}" %F\nTerminal=false\nCategories=Graphics;3DGraphics;Engineering;\n')
print(f'Installed: {installed}\nSHA256: {digest}\nLauncher: {launcher}')
print('Settings: ${XDG_CONFIG_HOME:-~/.config}/OrcaSlicer-QIDI. Application was not launched.')
