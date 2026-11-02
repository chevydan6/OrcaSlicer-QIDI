# Linux build and installation

Status: build workflow exists; no successful custom binary build is recorded yet.

The tested host is Fedora 44 x86_64. Builds target Ubuntu 24.04 x86_64 AppImage,
using the official Orca build script and dependency recipes at the pinned source
revision. The local host lacks GUI development packages and passwordless sudo;
the GitHub workflow provides a separate build machine.

## Reproduce

```sh
git clone https://github.com/chevydan6/OrcaSlicer-QIDI.git
cd OrcaSlicer-QIDI
python3 scripts/prepare-source.py
cd build/source
./build_linux.sh -u
./build_linux.sh -drlL -j 2
./build_linux.sh -sitrlL -j 2
ctest --test-dir build -C Release --output-on-failure
python3 scripts/orca_profile_tool.py check
```

Use Ubuntu 24.04 with adequate disk and RAM; `-u` installs OS packages and needs
sudo. The source preparation script refuses an existing destination. Source
commits are pinned in `sources.json`, and numbered patches apply in order.
Upstream dependency recipes govern third-party downloads; the runner image,
package repositories and some build utilities are not bit-for-bit pinned.

The equivalent GitHub Actions job is **Linux integration build**, triggered
manually. It uploads the AppImage and available test/configuration logs. A run
that predates a patch does not validate that patch. Only a successful patched
run can be used as evidence of compilation and test execution.

## Install once the custom artifact passes validation

```sh
python3 scripts/install-linux.py /path/to/custom.AppImage
~/.local/bin/orca-slicer-qidi
```

Installation is per-user and does not require sudo. It adds a distinct desktop
entry and stores each image by checksum under `~/.local/opt/orca-slicer-qidi`.
The launcher passes a separate `--datadir` under `OrcaSlicer-QIDI`; it neither
migrates existing slicer settings nor changes file associations. Installation
does not launch the application or contact a printer. The AppImage path also
gives it a distinct single-instance identity in Orca's Linux implementation.

GUI coexistence and persistence must still be verified with the compiled build.
Automatic application/profile updates require review so official updates do not
replace downstream features or profiles; this is not yet disabled in code.
