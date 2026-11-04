# Remaining limitations and physical verification

Candidate70 completed one authorized physical MAX4 test on2026-11-04: a20-layer
10×10×4mm cube with sparse logical T2 mapped to A1. Firmware history reports
completed; yellow deposition and the finished cube were visible. Normal end
unloaded the Box path and set all heater targets to0. This establishes that one
mapping/session, not general hardware certification or print-quality measurements.
See [hardware evidence](../validation/hardware-2026-11-04/README.md). The real GUI
exposed inaccurate layer counters and remaining-time estimates; those remain
unfixed. Read-only reports identify one Box, main MCU02.01.01.12 and Box02.03.01.21;
the overall release version and independent material identity remain unestablished.

Automated communication tests use only 127.0.0.1:19025, whose fixture records
and discards requests. A recorded heater, load, RFID or start request does not
prove physical execution. Candidates 59, 62 and 64 passed build gates but failed GUI
acceptance. Candidate 66 passed build gates and targeted layout/import checks;
candidate 68 passed build gates but failed unsupported-job GUI status.
Candidate 69 passed CI and 61 GUI cases but failed timelapse selection.
Candidate70 passed its complete matching CI/63-case GUI gate and is installed
with X11/XWayland; see [acceptance](../validation/accepted-70.json). These earlier
failed records are retained and are not combined with70's positive evidence.

## Supported scope and gaps

- Public LAN/Moonraker communication is implemented. QIDI account login, cloud
  discovery, proprietary networking, MQTT and remote tunnels are not bundled.
- HTTPS/WSS is not accepted as verified secure transport: the inherited WebSocket
  TLS path disables peer certificate verification. Current acceptance uses trusted
  local HTTP. The CA field alone does not establish end-to-end TLS verification.
- Single-printer jobs support Box mappings and single-material external-spool
  mode. Mixed Box/external jobs, multicolor external-spool jobs and incomplete
  mappings are rejected. Experimental multi-device submission refuses QIDI jobs
  because that separate path lacks a per-printer mapping snapshot.
- Custom Orca exposes neither manual drying nor automatic-refill controls.
  Firmware may already have refill enabled, as observed on Dan's MAX4. Public source
  evidence did not establish unambiguous control commands for both workflows. The
  incompatible Bambu refill/calibration/reset operations are hidden for QIDI.
  Filament Box temperatures used during printing are implemented separately.
- Current Orca process and material tuning is retained where a counterpart
  already exists. Missing QIDI profiles are imported with attribution. Matching
  controls and G-code does not make the engines or print quality identical.
- Native camera uses the reported local HTTP snapshot endpoint. The native GUI displayed snapshots from the real MAX4 during the authorized print.
  Authentication and other proxy configurations remain unverified.
- New QIDI-specific interface strings fall back to English when a translation
  catalog has no translation. Some shared upstream monitoring labels still say AMS.
- This deliverable targets Linux x86_64. Other platforms have not been built.
  The old Fedora/LXQt host needed GNOME 50 Flatpak and a private session bus.
  The recovered Ubuntu 24.04.5 host runs the native AppImage; launcher/menu/file chooser/settings/exit acceptance passed with --extract --x11.
  Native Wayland is unaccepted: isolated Weston main controls were unreliable.
  The later display-pipe exit came from the harness closing the compositor, not
  an application crash. Actual GNOME/XWayland launch/render/exit passed.
  No Flatpak bundle is supported for this milestone. Dependencies vary by distribution.
- Official Orca application/preset updates do not include the downstream patches.
  Keep automatic preset updates disabled and rebuild this port for updates.

## Starting filament: what is proven

Software tests preserve logical indices through slicing and submission, including
unused leading filaments. The GUI case selecting filament 3 and physical B2 emits
T2 and sets value_t2 to slot5 before the simulated start. Support-first projects
retain separate preparation and deposition tools, matching QIDI Studio's reference
trace. See filament-mapping.md and the validation records.

The physical cause of the reported MAX4 starting-filament symptom is not proven.
The port explicitly sets Box mode, validates every used tool mapping, and captures
submission options before asynchronous upload. A physical T2→A1 print now passed on the reported firmware, but multiple-Box,
support-first and sequential QIDI Studio comparisons remain outstanding.

## Hardware test scope

Record the MAX4 firmware version, Box count and slot layout first. Work within
Dan's authorized test session; do not repeatedly request permission for operations
already authorized. Dan authorized autonomous execution of this ABS refill
session. New firmware flashing or persistent configuration changes remain outside
that test scope. Suggested checks include single-material
external mode, sparse logical filament 3 to B2, reversed/multiple-Box mappings,
support-first startup, filament changes, RFID and material sync, chamber/fan
telemetry, camera, and network failure recovery. Heating, feeding, motion and print
starts are never part of an automatic software acceptance run.

No software test suite can guarantee that a GUI will never crash. The control
stability gate covers documented malformed inputs, delayed/failed communication,
dialog lifetimes, repeated actions, recovery and subsequent slicing. Unobserved
hardware responses or platform conditions can still expose defects.

## ABS refill reference, 2026-11-04

Official QIDI Studio2.07.02.73 was tested before the custom Orca comparison.
The first cut donor failed initial loading; Dan confirmed it was too short.
The restored-donor retry completed40 orange layers. A2's inlet became empty at
layer38, but toolhead filament remained present through completion and no A3
transfer occurred. This is inconclusive for automatic refill. The firmware had
reported auto_reload_detect=1 and a matched blue ABS A2/A3 group; custom Orca still
has no refill control and has not been physically tested for refill.
All heater targets returned0. Post-end loaded_slot1/sensor-present remained despite
the reference job's unload command, so unload success is not claimed.
[Exact jobs, traces and results](../validation/refill-reference-2026-11-04/README.md)
are retained. Repeat with sufficient consumption after the donor inlet empties,
then compare Orca sequentially after clearing the plate.
