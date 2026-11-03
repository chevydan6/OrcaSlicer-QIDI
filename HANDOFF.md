# Project handoff

Last updated: 2026-11-03, new Ubuntu host recovery. **Resumed at the user's request.
The project is unfinished; no candidate has final acceptance.** This file is the resumption point for another developer.
Update it when the candidate, validation result, installation or remaining work changes.

## Goal and authorization

Build current official OrcaSlicer with QIDI Studio MAX4 and QIDI Box functionality,
preserving current Orca behavior. Complete a general port, then a dedicated bug-fix
and validation phase, especially starting-filament selection and GUI stability.
Deliver a coexisting Linux installation, corresponding source, reproducible build
instructions, feature checklist, and explicit limitations. The user authorized
downloads, autonomous software work and GitHub backup.

**No MAX4 is connected. Do not flash firmware, change printer configuration,
activate heaters, move/feed hardware or start a real print without explicit
user authorization.** Simulated commands go only to `127.0.0.1:19025`; the fixture
records/discards requests and never executes or forwards them. Hardware testing
is a separate acceptance stage and is not implied by software test success.

## Latest acceptance failure

The 57-patch build input is `0b5a0e57608e4bf261dc5efe6c647a79c7911496`.
Integration run 41600542116 and static run 41600547497 were launched.
Its compiled artifact and manifest were verified (see recovery artifact-57.json).
Fresh GUI setup on Ubuntu leaves Prepare blank until manual maximize:
see `validation/gui-57`. Patch 58 attempts to correct GTK notebook page sizing.
Its exact reproduced source tree is `b99ca8416243c44dffb53c4c08d299045551976b`.
This shared layout correction needs a matching build/static pass and GUI retest.
Do not install candidate 57 as accepted or combine its evidence with candidate 58.

Dan supplied printer LAN access and authorized read-only inspection. Sanitized
telemetry is under validation/recovery-2026-11-03. One Box reports MCU 02.03.01.21;
main MCU 02.01.01.12; overall MAX4 firmware version is still unconfirmed.
Only GET requests were made; valid camera JPEG decoded. No heating, feeding,
motion, RFID action, settings change or print was initiated. Active tests require
an explicit approved supervised session after software acceptance.

## Recovery update

Recovered integration revision `70d58fc17f0132d926424a5a74144bf80cb1dcfd` into
`/home/dan/qidi-orca-port` on Ubuntu 24.04.5 x86_64 / GNOME, GCC 13.3,
14 GiB RAM, 23 GiB swap and 279 GiB available disk. Use parallelism 2.
The 56-patch source exactly reproduces recorded tree
`20f0b1398164ca1b5ab5bd44c6ecd6071aaaad3e`; upstream pins are unchanged.

Run 41595285772 completed successfully. Its report has 2,912 unit cases,
zero failures/skips; all 21 MAX4 cases pass. Static run 41595289239 failed:
`AMSMaterialsSetting.cpp` needs a direct `<wx/colourdata.h>` include.
Patch 57 supplies that include; reproduced tree is
`0e97b1e9b901311fc5b8cd40f3d5330ef70f1888`. New CI and exact-artifact GUI
acceptance are required. No installation or hardware test has occurred here.
See `validation/recovery-2026-11-03/`.

The following pause/host notes are historical, retained as evidence.

## Historical pause state

The user requested: "ok you can pause. create a github handoff". Development and
new validation are paused. The already-started GitHub builds may finish; their
states below are a snapshot, not a promise of success. Check their live results
first on resumption. No new build was launched for this handoff.

The isolated GUI55 closed normally with exit code 0. Its loopback simulator,
private Openbox and Xvfb :99 were stopped. No local build or GUI test is being
left running. The installed 42-patch candidate remains unchanged. The user's
desktop session was not stopped. Historical sleep-prevention settings remain as
the user requested; this pause does not restore system sleep.

## Repository and source state

- Private backup: https://github.com/chevydan6/OrcaSlicer-QIDI
- Local workspace: `/home/dan/qidi-orca-port`; integration branch `main`.
- Official Orca pin: `896557bce5281553ee0c6210f2da301b3b3c262e`.
- Official QIDI Studio pin: `403b619d56147160bb883e94f95a7951245bc6d0`.
- Local downstream checkout: `OrcaSlicer`, branch `qidi-max4-port`,
  commit `da74d6d6` (56 patches).
- Latest build input: integration commit `111e328` (includes the corrected thermal-argument validator).
- Numbered patches plus `sources.json` reproduce the downstream tree. The ignored
  full source checkouts are not needed to restore from GitHub: run
  `python3 scripts/prepare-source.py` into a fresh destination.
- Licensing/attribution: root LICENSE, patches/README.md, docs/maintenance.md;
  preserve original source and third-party notices with any binary distribution.

## Current builds and installation

| Candidate | Run | State / significance |
| --- | --- | --- |
| 56 patches | [41595285772](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41595285772) | Integration passed; static check failed, superseded by patch 57 |
| 56 static checks | [41595289239](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41595289239) | Failed: missing direct wx/colourdata.h include |
| 55 patches | [41593288187](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41593288187) | Compiles; 2,912 unit cases pass without skips, seven CLI checks and 72 vendor bundles pass; all 21 slices execute, 20 assertions pass; one parameter-order assertion fails, validator corrected in 4061021 |
| 55 static checks | [41593291506](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41593291506) | Pass |
| 54 patches | [41592928800](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41592928800) | Compiles; same parameter-order assertion failure, corrected validator |
| 51 patches | [41590831679](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41590831679) | Compiles; 2,912 unit cases pass with no skips; 19/21 MAX4 cases pass; two embedded-machine CLI cases fail, fixed in patch 54 |
| 49 patches | [41589611367](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41589611367) | Full pass: 2,911 unit cases, seven CLI regressions, 72 vendor bundles, 19 MAX4 cases |
| 42 patches | [41574937523](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41574937523) | Currently installed candidate; superseded, not final |

The installed menu entry is **OrcaSlicer QIDI (Custom)**; launcher
`~/.local/bin/orca-slicer-qidi`; app ID `io.github.chevydan6.OrcaSlicerQIDI`.
Settings are isolated under
`~/.var/app/io.github.chevydan6.OrcaSlicerQIDI/config/OrcaSlicer-QIDI`.
The installed 42-patch AppImage SHA256 is
`390077ccd362606fab08e51aacc66f0a7d4c056c1520d0f88bfb773a9a68893f`.
Existing official Orca/Bambu installations and file associations are separate.
Upgrade this installation only with the accepted final candidate.

The host is Fedora 44 x86_64/LXQt, with limited RAM and no passwordless sudo.
Compilation uses GitHub Ubuntu 24.04, `-j 2`, CTest parallelism 2, and a 6 GB
compiler cache. The Fedora GUI uses the installed GNOME 50 Flatpak runtime.
The private-session-bus installer option resolves this host's broken desktop
portal activation without changing global desktop services.

## Implemented and validated work

See [the feature checklist](docs/feature-checklist.md) for the complete inventory,
[dependencies](docs/dependencies.md), [mapping design](docs/filament-mapping.md),
and [limitations](docs/limitations.md). The checklist has historical status rows;
this handoff and revision-specific validation records identify the current candidate.

The port covers missing MAX4 materials, persistent Box thermal settings and G-code,
chamber/fan/light/speed controls, physical slot operations/RFID/material metadata,
Box/external telemetry, pre-print mapping/options, camera snapshots, detection and
named-object exclusion. Current Orca profiles/engine are preserved where already
supported. Cloud/MQTT, manual drying, ambiguous refill commands and experimental
QIDI multi-device submission are explicit gaps, not completed features.

Software evidence includes:

- Official QIDI Studio reference slices and projects in `validation/qidi-reference`.
- Sparse GUI submission through patch 38: logical filament 3 stays T2 and maps to
  physical B2/slot5 before the simulated start; submitted G-code is unchanged.
- GUI38: load/unload/eject/RFID, zero/four Boxes, external spool, chamber/fans/light/
  speed/options, malformed telemetry, HTTP errors/delay, WebSocket recovery and
  valid/invalid camera frames. No physical operations occurred.
- GUI49: populated material list and exact B2 metadata request; stale object
  chooser rejects a changed job before HTTP dispatch; fresh selection works;
  startup RFID toggle and normal empty-project shutdown pass.
- GUI51: original QIDI support-first project slices with embedded machine G-code;
  closing/discarding exits with status 0. This fixes the chamber-placeholder error
  and shutdown modal/watchdog failure observed in the installed 42-patch build.
- GUI55: five material editor reopenings retain identical dimensions, B2 metadata
  uses SLOT=5, and malformed telemetry/HTTP errors/delay/WebSocket reconnect recover
  in the tested scenarios. See `validation/gui-55`. The color palette placement
  defect remains pending compiled validation of patch 56.
- Static checks pass through patch 55. Exact source reproduction passes for 56.
- Isolated protocol sanitizer tests use production helper bodies, not the entire
  GUI. Complete GUI stability cannot be inferred from sanitizer/unit results alone.

## Latest fixes requiring acceptance

1. Patch 47/49 guards object exclusion with a locked current-status snapshot.
   GUI49 verified both stale rejection and fresh acceptance.
2. Patch 48 fixes QIDI material lookup and hides Bambu PA/reset; GUI49 verifies it.
3. Patch 50 adds QIDI `chamber_temperatures` placeholder compatibility. GUI51 passes.
4. Patch 51 suppresses validation modals once application shutdown is committed.
   GUI51 closes/discards the imported support project normally.
5. Patch 52's initial material-window sizing hypothesis was disproved by GUI52:
   repeated opens still shrink 25 pixels each and clip buttons. Keep that failed
   evidence. Patch 55 instead creates a fresh QIDI Box/external editor after each
   completed session and refuses duplicate opening while shown. GUI55 passes five reopenings at identical 370x232 client size; Confirm remains usable.
6. Patch 53 replaces clipped custom connection fields with native address/key/CA
   and Connect/Cancel controls. GUI54 verifies connection with blank API key, cancellation and reopening; exit 0.
7. Patch 54 preserves the original QIDI printer compatibility name alongside its
   Orca alias. The new original-machine CLI cases failed with -17 before this fix;
   both now slice without overriding the embedded machine. One test incorrectly required VT0 before VT2; named parameters are now compared independently of order, while values, completeness and duplicates remain strictly checked.

8. Patch 56 replaces an off-screen QIDI color palette with a native single-RGB
   dialog. GUI55 exposed the placement defect. This is the remaining source fix
   awaiting compiled GUI validation.

## Next steps, in order

1. After the user requests resumption, check run 41595285772 and static run 41595289239. Inspect failures; do not treat
   packaging alone as a full pass. Required: compilation, zero failed unit/CLI
   regressions, 72 vendor bundles and all **21** MAX4 slicing/persistence cases.
2. Download the AppImage artifact and verify the GitHub artifact ZIP digest before
   extracting. Record both ZIP and AppImage hashes and the packaged build manifest.
   The local `research/fetch-artifact-ranges.py` helper avoids printing credentials
   or signed URLs; ordinary `gh run download` is an alternative.
3. Run the final GUI against the loopback fixture with isolated settings:
   repeated material-dialog open/close (Box and external), material/color edits,
   native address dialog with blank optional key, disconnection while a dialog is
   open, stale object selection, malformed status/HTTP/camera recovery, and the
   control matrix in docs/feature-checklist.md. Recheck sparse starting-filament
   submission, slice/preview after controls and clean shutdown. Fix observed bugs.
4. Use **only private Xvfb display :99** for automation/screenshots. The user's
   desktop is :0; do not drive it. Private Openbox/Xvfb may need restarting after
   a long session. An absent X server is an environment failure, not an app crash.
5. Install the accepted build using the command below. Back up only this custom
   application's test settings first; restore a normal MAX4 profile, remove test
   fixture connections from the delivered settings, and keep native agents enabled.
   Validate the actual launcher/menu, file chooser, persistence and clean exit.
   Test fresh setup/layout and coexistence with existing slicer registrations.
6. Update README, build guide, feature checklist and this handoff to the accepted
   revision and exact evidence. Package the corresponding source archive, patch
   kit, build manifest, checksums and limitations with the AppImage/Flatpak.
   Back up deliverables on this private GitHub repository and retain rollback.
7. Report software completion separately from unperformed hardware verification.
   Do not claim that the physical starting-slot symptom is conclusively resolved.

```sh
python3 scripts/install-linux.py /path/to/accepted.AppImage \
  --flatpak-runtime org.gnome.Platform//50 --private-session-bus
```

Full reproduction and validation commands: [docs/build.md](docs/build.md).
User-facing controls and mapping: [docs/using-the-build.md](docs/using-the-build.md).
Upstream refresh procedure: [docs/maintenance.md](docs/maintenance.md).

## Local evidence and working tools

- `artifacts/custom-N-verified`: verified AppImage artifacts; corresponding
  `custom-N-tests-verified` directories contain logs/CTest XML/slicing reports.
- `research/custom-N-runtime/squashfs-root`: extracted GUI candidates.
- `research/qidi-gui-fixture`: isolated settings, screenshots, request traces and
  GUI process exit records. These ignored local files are not the GitHub backup;
  curated evidence is committed under `validation/gui-N`.
- Fixture command: `research/printer-fixture-venv/bin/python
  scripts/qidi-printer-fixture.py --log /path/to/new-requests.jsonl --boxes 2`.
  It binds loopback only. Use a fresh trace for final acceptance.
- Private GUI automation: `research/private_gui.py` and
  `research/run-private-gui.py`. Both require DISPLAY=:99. The portal PID guard in
  the helper must match the current private GTK portal before using a file chooser.
- Latest corresponding source archive already generated locally:
  `artifacts/OrcaSlicer-QIDI-source-a9295a1a.tar.gz`, SHA256
  `73018f1a551395a82d3894e1cedb354bcde8b6061ae04418593031b6b4ddcd2c`.
  This archive is superseded by patch 56; regenerate from da74d6d6 before delivery.
  It is not a final GitHub release asset.

Do not upload access tokens, API keys, signed artifact URLs or personal slicer
settings. The committed fixture evidence contains synthetic loopback data only.
