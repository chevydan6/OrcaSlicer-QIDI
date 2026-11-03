# Updating the downstream port

Keep the integration repository and each delivered binary together. `sources.json`
pins the two official source trees; `patches/` contains ordered `git format-patch`
commits; `resources/qidi-port-build.json` in a built package records their hashes.
The ignored local checkouts are disposable. GitHub backs up the patch kit and
validation evidence, not local printer credentials or user slicer settings.

## Rebase procedure

1. Create a new integration branch before changing the pins. Fetch official Orca
   and QIDI Studio, record their new commit IDs, and read changes affecting the
   files in the patch series. Keep the old release and validation records.
2. In a fresh Orca checkout, check out the old pinned Orca commit and apply the
   current patch series with `git am /absolute/path/to/patches/*.patch`. Create a
   downstream branch and use `git rebase --onto NEW_ORCA_SHA OLD_ORCA_SHA`.
   Resolve conflicts by preserving the new upstream behavior and the QIDI-only
   additions. Drop downstream changes only after confirming upstream now provides
   the same behavior. Do not replace whole current Orca files with QIDI versions.
3. Recheck QIDI Studio's LAN dispatcher, Box telemetry parser, submission dialog,
   MAX4 profiles and G-code generator. Public firmware source can clarify a
   protocol, but it does not identify the firmware installed on a user's printer.
4. Generate the rebased series into a separate directory with
   `git format-patch NEW_ORCA_SHA..HEAD -o /path/to/new-patches`. Review it before
   replacing the tracked series. Update source pins, patch attribution and the
   feature checklist. Preserve upstream and QIDI copyright/license headers.
5. Run `python3 scripts/verify-patches.py --source /path/to/rebased-checkout` after
   updating the tracked series and pins. It applies patches to a temporary index
   and compares the result with the rebased checkout's committed tree.
6. Repeat profile structure/inheritance checks, the isolated protocol checks, the
   complete Linux build, upstream regression tests and MAX4 runtime validation.
   Reuse the saved QIDI reference projects for initial-tool comparisons. Check
   sparse/reversed/multi-Box maps, support-first startup, external mode, rejected
   malformed maps, HTTP failure handling, GUI persistence and coexistence.
7. Publish a new installable artifact only with its exact integration commit,
   checksums, build/test logs and remaining limitations. Retain the previous
   installed checksum directory for rollback. Software test success never implies
   physical filament, temperature or print-quality verification.

The isolated helper and profile inventory scripts default to local `OrcaSlicer/`
and `QIDIStudio/` checkouts. Use those names for a maintenance workspace or adapt
those explicit paths when working elsewhere. The CI workflow reads pins from the
integration commit and creates its own clean source checkout.

## Shared-code changes to review during upstream updates

Most controls and telemetry are gated by the QIDI agent. The changes to shared
code also need review: the CLI filament-diameter default, structured QIDI 3MF
recognition/configuration migration, optional QIDI API-key handling, and delayed
Moonraker response lifetime. In particular, queued message dispatchers must stop
after callback clearing, connection reset or agent destruction. Keep the existing
non-QIDI access-control and cache-merge regression cases when updating these
paths. QIDI's four-part product version must not be interpreted as an Orca
application version or trigger obsolete plate-origin migrations.

## Licensing and distribution

OrcaSlicer and QIDI Studio source in this port is AGPL-3.0. Their original license
files, copyright notices and bundled third-party notices stay in the source and
package. The root LICENSE is QIDI Studio's AGPL-3.0 text. Patch attribution is in
`patches/README.md`, with the exact source revisions in `sources.json`.

Distribute the corresponding patched source and build instructions alongside a
binary. Keep dependency licenses and notices supplied by the official Orca build
recipes. Do not substitute a proprietary QIDI network binary for Orca's existing
network stack: this port implements public LAN protocols and does not include
QIDI cloud authentication, MQTT or tunneling components.

## Rollback

The installer stores each binary under its SHA-256 prefix. Re-run the installer
with a retained older custom AppImage to point the dedicated launcher at that
version. Back up the custom `OrcaSlicer-QIDI` settings before downgrading across
schema changes. Existing official Orca/Bambu/QIDI application directories and file
associations are independent of this installation.
