#!/usr/bin/env python3
"""Install a built AppImage under the current user's home; never launch it."""
import hashlib
import argparse
from pathlib import Path
import os
import shlex
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('image', type=Path)
parser.add_argument('--extract', action='store_true', help='Install an extracted AppDir; no FUSE required')
parser.add_argument('--flatpak-runtime', help='Run the extracted AppDir in an installed runtime, e.g. org.gnome.Platform//50')
args = parser.parse_args()
image = args.image.resolve()
with image.open('rb') as stream:
    header = stream.read(12)
    if header[:4] != b'\x7fELF' or header[8:11] != b'AI\x02':
        raise SystemExit('Expected a type-2 AppImage')
if args.flatpak_runtime:
    subprocess.run(['flatpak', 'info', '--show-commit', args.flatpak_runtime], check=True)
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
extracted = directory / 'AppDir'
if args.extract or args.flatpak_runtime:
    if not extracted.exists():
        with tempfile.TemporaryDirectory(prefix='extract-', dir=directory) as temporary:
            with (directory / 'extraction.log').open('w') as log:
                subprocess.run([str(installed), '--appimage-extract'], cwd=temporary,
                               stdout=log, stderr=subprocess.STDOUT, check=True)
            staged = Path(temporary) / 'squashfs-root'
            if not (staged / 'AppRun').is_file():
                raise SystemExit('Extracted image contains no AppRun')
            staged.rename(extracted)
entrypoint = extracted / 'AppRun' if args.extract or args.flatpak_runtime else installed
command = [str(entrypoint)]
if args.flatpak_runtime:
    command = ['flatpak', 'run', '--share=network', '--share=ipc', '--socket=x11', '--socket=wayland',
               '--device=dri', '--filesystem=home', f'--env=APPIMAGE={installed}',
               f'--command={entrypoint}', args.flatpak_runtime]
launcher = home / '.local/bin/orca-slicer-qidi'
launcher.parent.mkdir(parents=True, exist_ok=True)
marker = '# Managed by OrcaSlicer-QIDI installer'
if launcher.exists() and marker not in launcher.read_text():
    raise SystemExit(f'Refusing to overwrite unrelated launcher: {launcher}')
launcher.write_text('#!/bin/sh\n' + marker + '\n'
    'set -eu\n'
    'qidi_config="${XDG_CONFIG_HOME:-$HOME/.config}/OrcaSlicer-QIDI"\n'
    'mkdir -p "$qidi_config"\n'
    f'exec {shlex.join(command)} --datadir "$qidi_config" "$@"\n')
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
if args.flatpak_runtime:
    print(f'Runtime: {args.flatpak_runtime}; AppDir: {extracted}')
print('Settings: ${XDG_CONFIG_HOME:-~/.config}/OrcaSlicer-QIDI. Application was not launched.')
