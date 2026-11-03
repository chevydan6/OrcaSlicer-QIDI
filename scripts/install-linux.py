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
import sys

APP_ID = 'io.github.chevydan6.OrcaSlicerQIDI'

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('image', type=Path)
parser.add_argument('--extract', action='store_true', help='Install an extracted AppDir; no FUSE required')
parser.add_argument('--x11', action='store_true',
                    help='Use the supported X11/XWayland backend for the native installation')
parser.add_argument('--flatpak-runtime', help='Package and install a separate Flatpak app using an installed runtime, e.g. org.gnome.Platform//50')
parser.add_argument('--private-session-bus', action='store_true',
                    help='Use a private D-Bus session with the GTK portal for a broken desktop portal session (Flatpak only)')
args = parser.parse_args()
if args.x11 and args.flatpak_runtime:
    raise SystemExit('--x11 is supported by the native installation only')
if args.private_session_bus and (not args.flatpak_runtime or not shutil.which('dbus-run-session')):
    raise SystemExit('--private-session-bus requires --flatpak-runtime and dbus-run-session')
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
if args.x11:
    command = ['env', 'GDK_BACKEND=x11', *command]
if args.flatpak_runtime:
    # A registered application is required: GNOME image loaders use the portal
    # to create a nested sandbox, which rejects a bare runtime's metadata.
    with tempfile.TemporaryDirectory(prefix='flatpak-', dir=directory) as temporary:
        package_dir = Path(temporary)
        bundle = package_dir / 'OrcaSlicer-QIDI.flatpak'
        subprocess.run([sys.executable, str(Path(__file__).with_name('package-flatpak.py')),
                        str(extracted), '--runtime', args.flatpak_runtime,
                        '--output', str(bundle), '--workdir', str(package_dir / 'build')], check=True)
        subprocess.run(['flatpak', 'install', '--user', '--assumeyes', '--noninteractive',
                        '--no-deps', '--no-related', '--reinstall', str(bundle)], check=True)
        shutil.copyfile(bundle, directory / 'OrcaSlicer-QIDI.flatpak')
    command = ['flatpak', 'run', APP_ID]
    if args.private_session_bus:
        # LXQt sessions without graphical-session.target can fail to activate
        # the portal. Keep the workaround confined to this application's bus.
        command = ['env', 'XDG_CURRENT_DESKTOP=GNOME', 'dbus-run-session', '--', *command]
launcher = home / '.local/bin/orca-slicer-qidi'
launcher.parent.mkdir(parents=True, exist_ok=True)
marker = '# Managed by OrcaSlicer-QIDI installer'
if launcher.exists() and marker not in launcher.read_text():
    raise SystemExit(f'Refusing to overwrite unrelated launcher: {launcher}')
body = f'exec {shlex.join(command)} "$@"\n' if args.flatpak_runtime else (
    'qidi_config="${XDG_CONFIG_HOME:-$HOME/.config}/OrcaSlicer-QIDI"\n'
    'mkdir -p "$qidi_config"\n'
    f'exec {shlex.join(command)} --datadir "$qidi_config" "$@"\n')
launcher.write_text('#!/bin/sh\n' + marker + '\nset -eu\n' + body)
launcher.chmod(0o755)
desktop = Path(os.environ.get('XDG_DATA_HOME', str(home / '.local/share'))) / 'applications/orca-slicer-qidi.desktop'
desktop.parent.mkdir(parents=True, exist_ok=True)
if desktop.exists() and marker not in desktop.read_text():
    raise SystemExit(f'Refusing to overwrite unrelated desktop entry: {desktop}')
escaped = str(launcher).replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$').replace('%', '%%')
if args.flatpak_runtime:
    # Flatpak exports the application menu entry. Avoid two identical entries.
    desktop.unlink(missing_ok=True)
    override = desktop.with_name(APP_ID + '.desktop')
    if args.private_session_bus:
        if override.exists() and marker not in override.read_text():
            raise SystemExit(f'Refusing to overwrite unrelated desktop entry: {override}')
        # Same ID overrides the exported entry instead of adding a duplicate.
        override.write_text('[Desktop Entry]\n' + marker + '\nType=Application\n'
            'Name=OrcaSlicer QIDI (Custom)\nComment=Personal MAX4 and QIDI Box build\n'
            f'Exec="{escaped}" %F\nIcon={APP_ID}\nTerminal=false\n'
            f'X-Flatpak={APP_ID}\nCategories=Graphics;3DGraphics;Engineering;\n')
    elif override.exists() and marker in override.read_text():
        override.unlink()
else:
    desktop.write_text('[Desktop Entry]\n' + marker + '\nType=Application\n'
        'Name=OrcaSlicer QIDI (Custom)\nComment=Personal MAX4 and QIDI Box build\n'
        f'Exec="{escaped}" %F\nTerminal=false\nCategories=Graphics;3DGraphics;Engineering;\n')
print(f'Installed: {installed}\nSHA256: {digest}\nLauncher: {launcher}')
if args.flatpak_runtime:
    print(f'Runtime: {args.flatpak_runtime}; app ID: {APP_ID}')
    print(f'Settings: ~/.var/app/{APP_ID}/config/OrcaSlicer-QIDI')
else:
    print('Settings: ${XDG_CONFIG_HOME:-~/.config}/OrcaSlicer-QIDI')
print('Application was not launched.')
