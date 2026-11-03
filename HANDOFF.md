# Project handoff

Updated 2026-11-03 on the recovered Ubuntu computer. Work resumed at Dan's request.
**Unfinished: no accepted candidate and no installation on this computer.**
Feature expansion is frozen pending one complete software acceptance.

## Current candidate and workspace

- Integration repository: https://github.com/chevydan6/OrcaSlicer-QIDI, branch main.
- Workspace: `/home/dan/qidi-orca-port`; recovered at `70d58fc17f0132d926424a5a74144bf80cb1dcfd`.
- Next candidate: **62 patches**, build dispatch pending. Latest evaluated build input: `cd6d820543ddaabad4846b6eb053b4508e65c448` (59 patches).
- Orca pin: `896557bce5281553ee0c6210f2da301b3b3c262e`.
- QIDI Studio pin: `403b619d56147160bb883e94f95a7951245bc6d0`.
- Prepared source: `build/source`, local commit `171f0274`.
- Exact downstream tree: `8e41a9fe4e99edd185d7ddfa840eab0f97d6881b`.
- All 62 patches reproduce that tree via `scripts/verify-patches.py`.
- Original 56-patch recovery matched recorded tree `20f0b1398164ca1b5ab5bd44c6ecd6071aaaad3e`.
- Pins remain fixed. Local recovery commits have fresh metadata; tree identity is verified.

## Build gates

| Candidate | Integration | Static | Acceptance |
| --- | --- | --- | --- |
| 59 / cd6d820 | [41602372652](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41602372652), passed | [41602379555](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41602379555), passed | Verified matching artifact; GUI failed layout, repeated material dialogs and restart |
| 58 / c1aa8e5 | 41601936217, cancelled | 41601942066, cancelled | Superseded by fresh-connection fix; cancellation is not a pass |
| 57 / 0b5a0e5 | 41600542116, passed | 41600547497, passed | GUI fresh setup and fresh connection failures; not accepted |
| 56 / 111e328 | 41595285772, passed | 41595289239, failed direct include check | Not accepted |

Check live results; these are observations, not promises of success. Required:
compilation; zero failed unit/CLI cases; 72 vendor bundles; all 21 MAX4 cases;
static checks; then the full GUI matrix on one matching artifact.

The 56-patch report has 2,912 unit cases with no failures/skips, seven CLI cases,
72 vendor bundles and all 21 MAX4 slices/persistence cases passing. Its two
original embedded-machine cases pass, including support-first parameter order.
Verified artifact/report hashes and manifests are in `validation/recovery-2026-11-03`.
Candidate 57 AppImage SHA256:
`7d806251b2bb3e4094db1b78a7ff971b4df052165a3f6acc530794ab412ceb28`.
Its ZIP digest and 57-patch manifest match GitHub and build input 0b5a0e5.

## Observed defects and attempted corrections

- Patch 57 adds `<wx/colourdata.h>` demanded by the failed patch-56 include check.
  Static run 41600547497 verifies this correction.
- GUI57 fresh setup left Prepare blank until manual maximization. Patch 44 alone
  is insufficient. Patch 58 forwards GTK frame sizing to the notebook's current
  page even when the notebook's dimensions are unchanged. **GUI59 disproved this correction.**
- GUI57 fresh native address connection stores printer_type `Qidi X-Max 4`, but
  the display lookup only recognized vendor ID `Qidi-XMax-4`, resulting in Unknown
  and an empty material dropdown. Patch 59 adds QIDI-only vendor name matching.
  **GUI59 verified populated choices and material/color dispatch.**
- The patch-56 native RGB chooser appeared fully on-screen in GUI57.
- A diagnostic manual substitution of the old model ID produced a tiny 2x5 editor;
  it was inconclusive, reverted and is not a workaround or accepted path.
- GUI57 exited normally (status 0) in the observed setup/connection sessions.
- Preserve failed GUI52 sizing evidence and all later failures. Earlier GUI passes
  do not accept later binaries. See `validation/gui-57` and the full checklist.

Candidate 59 has 2,912 unit cases with zero failures/skips, seven CLI regressions,
72 vendors and all 21 MAX4 cases passing. ZIP and manifest verification and test
report summary are in `validation/recovery-2026-11-03/{artifact-59,ci-59}.json`.
Its AppImage SHA256 is `be664d179a2209cd348fd14d2fb9e30f8f8dde60a0ad59e0d3e4d9f25cc5edc4`.
`validation/gui-59` records **failed acceptance**, including eight 2x5 material
reopens. Patches 60–62 address minimum sizing, lost endpoint scheme/port and
native page allocation. Debugger interventions support these changes but do not
accept them. Check the next matching binary without debugger intervention.

## Host and isolated GUI environment

Ubuntu 24.04.5 x86_64, GNOME Wayland, GCC 13.3, 24 logical CPUs, 14 GiB RAM,
23 GiB swap, initially 279 GiB available disk. Keep build/test parallelism 2.
Native AppRun works here; do not inherit Fedora Flatpak/portal workarounds by default.

Private Xvfb selected **:2** using `-displayfd`; verified by xdpyinfo. The real
session uses :0/Wayland. GUI commands must use `DISPLAY=:2`, `GDK_BACKEND=x11`,
`XDG_SESSION_TYPE=x11`, and remove WAYLAND_DISPLAY. Do not automate the real desktop.
Ignored helpers: `research/gui-control.py`, `research/fetch-artifact.py` (parallel
artifact ranges with digest verification and no credential/URL logging).
Fixture venv: `research/printer-fixture-venv`; pinned requirements and self-tests pass.
Fixture binds only `127.0.0.1:19025`, records/discards requests and never forwards.
GUI files: `research/gui-57`, `research/gui-59`, `research/gui-59-layout`; runtimes also include `research/runtime-59`.
Raw downloads are under `artifacts/`; these ignored paths are not GitHub backups.

## Printer access boundary and observations

Dan authorized read-only inspection and supplied LAN access. GET-only inspection
found one Box, main MCU `02.01.01.12`, Box MCU `02.03.01.21`, a valid 1920x1080
JPEG snapshot, and slot 2 present with blue Generic ABS metadata. Overall MAX4
release version remains unknown (printer/info returns ?); loaded materials need
Dan's confirmation. Existing targets were bed 90 C and chamber 65 C; we changed
nothing. `auto_reload_detect=1` and `auto_refill=[]` are evidence, not established
refill prerequisites or a verified implementation.

Sanitized observations: `validation/recovery-2026-11-03/printer-readonly.json` and
`actual-telemetry-sanitized.json`. Raw responses remain ignored. Never commit
credentials. No real printer address is configured in the test GUI.

Availability is not permission to heat, feed, move, RFID-refresh, change persistent
configuration or print. Finish software acceptance first, then present a concrete
small supervised sequence and obtain explicit authorization for grouped operations.
Firmware flashing and persistent configuration changes require separate approval.
QIDI Studio/Orca comparisons must be sequential, with identical model/materials/settings.

## Next steps

1. Build candidate 62, check actual integration/static results and fix failures.
2. Download its matching AppImage and reports, verify GitHub ZIP digest, record ZIP
   and AppImage hashes, compare packaged manifest against the new build input and all 62 patch hashes.
3. Start with fresh settings: rerun setup/layout and native blank-key connection.
   Verify populated materials without hand-editing model identity; native color
   edits; repeated Box/external dialogs; slot switching; duplicate opens; disconnect
   during dialogs; callbacks; cancel/reopen. Then execute every checklist case:
   sparse/reversed/multi-Box maps, zero/four Boxes, external spool, support-first
   import/slice/preview, stale/fresh exclusion, all controls, telemetry/HTTP/WS/camera
   faults and recovery, subsequent slicing, shutdown/discard/file chooser/persistence.
4. If source changes, rebuild and retest a matching artifact. Do not aggregate
   different binaries into final acceptance.
5. Only after acceptance install via scripts/install-linux.py; inspect its current
   behavior first. Back up existing custom settings, retain rollback, remove fixture
   connections, validate actual launcher/menu/chooser/persistence/fresh layout/exit.
6. Publish matching AppImage, supported Flatpak if applicable, source archive,
   manifest/checksums, patch kit, instructions and evidence to private GitHub.
   Update README/build/checklist/limitations and this handoff to that exact candidate.
7. Investigate refill after the stable milestone using actual QIDI source/protocol
   evidence and separately authorized comparisons. Do not guess commands.

## Scope and preserved rules

Implemented: MAX4 missing materials; Box thermal settings; controls/telemetry;
slot/RFID/material editing; pre-print mapping/options; LAN monitoring/submission;
camera; detection; named exclusion; QIDI project compatibility; separate identity.
Not accepted as a complete port. Refill/manual drying/cloud/MQTT/tunnels remain
unfinished; mixed Box/external and multicolor external jobs are rejected;
experimental multi-device QIDI submission is rejected. Linux x86_64 only.

Project filament identity, G-code tool and physical slot stay distinct. Filament 3
remains T2; Box 2 slot 2 is physical 5; mapping is [-1,-1,5], never [5]. Capture
mappings/options before asynchronous upload. Reject malformed/incomplete mappings;
telemetry loss must not silently select external mode. Support-first preparation
T2 and initial deposition T0 remain distinct and both require mapping.

No physical starting-filament, refill, temperature or print behavior is verified.
Preserve Orca engine/tuning and non-QIDI regressions, copyright/AGPL/dependency notices.
Historical host/install details are preserved in
`validation/recovery-2026-11-03/original-handoff.md` and Git history.
