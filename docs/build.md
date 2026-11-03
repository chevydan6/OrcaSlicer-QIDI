# Linux build and installation

Status: the 42-patch integration build passed compilation, unit tests, all seven
CLI regressions, all 72 profile bundles and all 19 MAX4 slicing cases in run
41574937523. This fixes the four G-code import regressions found on earlier
builds. Actual GUI simulation through patch 38 has exercised controls, faults,
camera display and filament-three to Box-B2 submission. Later source patches
address additional GUI defects; their full build and acceptance remain pending.
This is not yet a validated final release or physical printer certification.

The tested host is Fedora 44 x86_64. Builds target Ubuntu 24.04 x86_64 AppImage,
using the official Orca build script and dependency recipes at the pinned source
revision. The local host lacks GUI development packages and passwordless sudo;
the GitHub workflow provides a separate build machine.

## Reproduce

```sh
git clone https://github.com/chevydan6/OrcaSlicer-QIDI.git
cd OrcaSlicer-QIDI
python3 scripts/prepare-source.py
python3 scripts/write-build-manifest.py build/source
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
The packaged `resources/qidi-port-build.json` records those source commits, the
integration commit and every patch checksum.
Upstream dependency recipes govern third-party downloads; the runner image,
package repositories and some build utilities are not bit-for-bit pinned.
Install `ccache` and `xvfb` with the build prerequisites. The upstream unit-test
runner installs its pinned NumPy into the bundled test interpreter and excludes
tests already labelled NotWorking. CLI regression tests run separately.

The equivalent GitHub Actions job is **Linux integration build**, triggered
manually. It uploads the AppImage and available test/configuration logs. A run
that predates a patch does not validate that patch. Only a successful patched
run can be used as evidence of compilation and test execution.

The separate **Downstream C++ include and static checks** workflow runs upstream's
`scripts/run_clang_tidy.sh --base PINNED_ORCA_COMMIT --no-fetch --yes -j 2` against
the applied patches, without precompiled headers. Dispatch it after a dependency
cache is available; it deliberately fails on a cache miss rather than duplicating
the dependency build. Static checks complement compilation and runtime tests.

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
On hosts without FUSE, add `--extract` to install an AppDir. On this Fedora host,
WebKitGTK is supplied by the existing GNOME runtime used by the installed slicers:

```sh
python3 scripts/install-linux.py /path/to/custom.AppImage --flatpak-runtime org.gnome.Platform//50
```

On this Fedora/LXQt session, the desktop portal cannot start because its
`graphical-session.target` prerequisite is inactive. The GUI test's file chooser
works in a private D-Bus session with the GTK portal. For that specific host issue:

```sh
python3 scripts/install-linux.py /path/to/custom.AppImage \
  --flatpak-runtime org.gnome.Platform//50 --private-session-bus
```

This option requires `dbus-run-session` and a working GTK portal backend. It uses
an application-specific session bus and a matching menu-entry override; it does
not alter the desktop's systemd targets or other slicers. The normal Flatpak
launch remains the default on desktops with working portals. The private-session
mode has been tested with the registered validation runtime; final installation
validation remains pending. It does not disable image-loader sandboxing.

This mode verifies that the runtime is installed, extracts the AppImage, packages
and installs the separate Flatpak application `io.github.chevydan6.OrcaSlicerQIDI`.
It retains `OrcaSlicer-QIDI.flatpak` beside the original image. The exported menu
entry and convenience launcher both run that application. Settings are stored in
`~/.var/app/io.github.chevydan6.OrcaSlicerQIDI/config/OrcaSlicer-QIDI`; the native
AppImage installation uses the host config directory instead. Existing settings
are not migrated between these modes or from other slicers.

The Flatpak grants home-directory, graphics/display and network access for normal
slicer use. Installation does not launch it. Software validation overrides network
access with `--unshare=network`. A registered application is necessary: launching
directly inside a bare GNOME runtime fails when its sandboxed image loaders ask
the portal to create a child sandbox without application metadata. This was
reproduced and resolved using the official QIDI Studio reference binary on this
host; validation of the custom Orca binary remains pending.

To package an already extracted build independently, use:

```sh
python3 scripts/package-flatpak.py /path/to/AppDir --runtime org.gnome.Platform//50 \
  --output artifacts/OrcaSlicer-QIDI.flatpak --workdir build/flatpak-package
```

Both output paths must be new. This requires Flatpak and the runtime, but no SDK.
The bundle includes the build manifest, original resources and license notices;
runtime updates remain managed by Flatpak. Use the exported menu entry; upstream's
optional desktop integration does not reconstruct the Flatpak launcher. Its
desktop filenames are nevertheless namespaced with `-qidi`.

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
For offline validation on this Fedora host, point `--binary` at the extracted
`AppDir/AppRun`, add `--flatpak-app io.github.chevydan6.OrcaSlicerQIDI`, and use
`--artifact /path/to/custom.AppImage` to record the original package checksum.
This validation mode disables networking and uses fresh datadirs; it is separate
from the normal installed launcher.

The isolated protocol harness is `python3 scripts/check-protocol-helpers.py` with
the development checkout at `OrcaSlicer/`. It compiles actual helper/dispatch
method bodies with a recording transport, not the complete slicer or its HTTP
implementation. `python3 scripts/verify-patches.py` verifies source reproduction
without modifying the developer checkout's index or working tree.

Add `--sanitize` to the protocol harness to enable AddressSanitizer and
UndefinedBehaviorSanitizer, including float-to-integer overflow; sanitizer errors
terminate the check. This checks the isolated production helper bodies,
not the complete GUI. Use `--source PATH` for a prepared source checkout. The
Linux workflow runs this check before compiling the application. On a host with
sanitizer libraries extracted into a private directory rather than installed,
`--sanitizer-libs DIRECTORY` supplies their link/runtime path.

## Offline GUI communication fixture

The loopback server records requests and supplies synthetic MAX4/Box status. It
never executes or forwards G-code, changes a real printer, or simulates a successful
physical operation. Its tests validate the fixture itself; the GUI stability gate
in `feature-checklist.md` still requires the compiled application.

```sh
python3 -m venv research/printer-fixture-venv
research/printer-fixture-venv/bin/pip install -r scripts/requirements-fixture.txt
research/printer-fixture-venv/bin/python scripts/check-printer-fixture.py
research/printer-fixture-venv/bin/python scripts/qidi-printer-fixture.py \
  --port 19025 --boxes 2 --log logs/gui-fixture-requests.jsonl
```

The native QIDI controls use upstream's **Preferences → Developer → Experimental
Features → Use printer agents instead of print hosts** option. Enable it in the
isolated custom-slicer configuration, select a MAX4 profile (its printer agent is
`qidi`), and add the QIDI device at
`http://127.0.0.1:19025`. The fixture binds only `127.0.0.1`; it has no discovery or
outbound connection code. Use the native app or a Flatpak with network sharing
for this test so the app can reach host loopback. Configure only this fixture
address in the isolated settings directory.

The API-key field is optional for trusted Moonraker LAN access. Leave it blank
for this fixture. A real server that requires a key still requires its valid key;
the client must not substitute an invented credential. Exact dialog navigation
and native-control activation remain part of the compiled GUI validation gate.

`POST /__fixture__/state` accepts JSON with `update` (recursive status update),
`replace` (whole status replacement), `notification` (arbitrary WebSocket JSON),
`raw` (malformed message testing), `disconnect`, `http_error` (0 restores normal
HTTP responses), `delay` (0–60 seconds), and `invalid_camera_frame` (malformed JPEG response). These controls affect only the test
fixture. For example:

```sh
curl -sS http://127.0.0.1:19025/__fixture__/state \
  -H 'Content-Type: application/json' --data '{"disconnect":true}'
```

The fixture serves a clearly labeled synthetic camera JPEG. Real RFID reads,
thermal changes, motion and printing are not emulated. Unexpected GET endpoints return
404 so missing fixture coverage remains visible in the logs.
