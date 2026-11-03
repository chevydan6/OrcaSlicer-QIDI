#!/usr/bin/env python3
"""Package an extracted custom AppImage with an installed GNOME Flatpak runtime."""
import argparse
from pathlib import Path
import shutil
import subprocess

APP_ID = 'io.github.chevydan6.OrcaSlicerQIDI'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('appdir', type=Path)
parser.add_argument('--runtime', default='org.gnome.Platform//50')
parser.add_argument('--output', required=True, type=Path)
parser.add_argument('--workdir', required=True, type=Path)
args = parser.parse_args()
appdir = args.appdir.resolve()
output = args.output.resolve()
workdir = args.workdir.resolve()
if not (appdir / 'AppRun').is_file():
    raise SystemExit('AppDir must contain AppRun')
if not (appdir / 'resources/qidi-port-build.json').is_file():
    raise SystemExit('AppDir lacks the custom build provenance manifest')
if output.exists() or workdir.exists():
    raise SystemExit('Output and work directory must not already exist')
runtime = subprocess.check_output(['flatpak', 'info', '--show-ref', args.runtime], text=True).strip()
parts = runtime.split('/')
if len(parts) != 4 or parts[0] != 'runtime':
    raise SystemExit(f'Expected an installed runtime, got {runtime!r}')
runtime_commit = subprocess.check_output(['flatpak', 'info', '--show-commit', args.runtime], text=True).strip()
workdir.mkdir(parents=True)
staging = workdir / 'staging'
files = staging / 'files'
shutil.copytree(appdir, files / 'lib/orca-slicer-qidi', symlinks=True)
(files / 'bin').mkdir()
launcher = files / 'bin/orca-slicer-qidi'
launcher.write_text('''#!/bin/sh
# Use the runtime's CA bundle instead of the build machine's OpenSSL path.
if [ -z "${SSL_CERT_FILE:-}" ] && [ -s /etc/ssl/certs/ca-certificates.crt ]; then
    export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
fi
exec /app/lib/orca-slicer-qidi/AppRun "$@"
''')
launcher.chmod(0o755)
(staging / 'metadata').write_text(
    f'[Application]\nname={APP_ID}\nruntime={"/".join(parts[1:])}\ncommand=orca-slicer-qidi\n')
applications = files / 'share/applications'
applications.mkdir(parents=True)
(applications / f'{APP_ID}.desktop').write_text(
    '[Desktop Entry]\nType=Application\nName=OrcaSlicer QIDI (Custom)\n'
    'Comment=Personal MAX4 and QIDI Box build\nExec=orca-slicer-qidi %F\n'
    f'Icon={APP_ID}\nTerminal=false\nCategories=Graphics;3DGraphics;Engineering;\n')
icon = appdir / 'resources/images/OrcaSlicer_192px.png'
if icon.is_file():
    icons = files / 'share/icons/hicolor/192x192/apps'
    icons.mkdir(parents=True)
    shutil.copyfile(icon, icons / f'{APP_ID}.png')
(files / 'share/qidi-runtime-build.txt').write_text(f'Runtime: {runtime}\nCommit at packaging: {runtime_commit}\n')
subprocess.run(['flatpak', 'build-finish', '--command=orca-slicer-qidi', '--share=network',
                '--share=ipc', '--socket=x11', '--socket=wayland', '--device=dri',
                '--filesystem=home', str(staging)], check=True)
repo = workdir / 'repo'
subprocess.run(['flatpak', 'build-export', str(repo), str(staging)], check=True)
output.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(['flatpak', 'build-bundle', str(repo), str(output), APP_ID], check=True)
print(f'Created {output}; app ID {APP_ID}; runtime {runtime}')
