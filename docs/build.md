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
CTEST_PARALLEL_LEVEL=2 xvfb-run -a ./scripts/run_unit_tests.sh build/tests Release
xvfb-run -a ctest --test-dir build/tests -C Release -L RequiresApp --no-tests=error --output-on-failure --timeout 300
python3 scripts/orca_profile_tool.py check
```

Use Ubuntu 24.04 with adequate disk and RAM; `-u` installs OS packages and needs
sudo. The source preparation script refuses an existing destination. Source
commits are pinned in `sources.json`, and numbered patches apply in order.
Upstream dependency recipes govern third-party downloads; the runner image,
package repositories and some build utilities are not bit-for-bit pinned.
Install `ccache` and `xvfb` with the build prerequisites. The upstream unit-test
runner installs its pinned NumPy into the bundled test interpreter and excludes
tests already labelled NotWorking. CLI regression tests run separately.

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
The compiled Linux default and launcher use a separate datadir under `OrcaSlicer-QIDI`; it neither
migrates existing slicer settings nor changes file associations. Installation
does not launch the application or contact a printer. The AppImage path also
gives it a distinct single-instance identity in Orca's Linux implementation.

GUI coexistence and persistence must still be verified with the compiled build.
The upstream default for automatic preset bundle updates is off. Keep it off for
this fork until a downstream update process is available. Official application
updates do not contain these patches; use this integration workflow for updates.

## MAX4 runtime validation

After building, run `python3 scripts/validate-max4-slicing.py --source build/source`
from the integration repository (use `xvfb-run -a` on a headless machine). It uses
an isolated datadir, generates a cube locally, slices all MAX4 nozzle sizes and
newly imported materials, checks emitted macros, and saves/reloads a custom Box
temperature through 3MF. It never uploads files or sends printer commands.
Use `--binary PATH` for another executable layout and `--output NEW_DIRECTORY`
for subsequent runs. The output directory must not already exist.

The isolated protocol harness is `python3 scripts/check-protocol-helpers.py` with
the development checkout at `OrcaSlicer/`. It compiles actual helper/dispatch
method bodies with a recording transport, not the complete slicer or its HTTP
implementation. `python3 scripts/verify-patches.py` verifies source reproduction
without modifying the developer checkout's index or working tree.
