# Project handoff

**2026-11-09 main-build integration:** Patches 71–73 are consolidated from the tested monitoring/refill branch. Patch 74 replaces the Bambu camera fallback artwork; patch 75 changes the embedded HTTP snapshot refresh to 100 ms with the existing in-flight guard. The normal source build applies all 75 patches; no machine-specific address or local executable patch is part of that build. The camera scheduling regression runs with the Linux workflow. Full build/check status is recorded in GitHub Actions for the integration commit.

**Physical test, 2026-11-06:** Candidate72 printed a 20-layer ABS cube from A3 and Orca showed 20/20. Timelapse captured and rendered; leveling executed. ETA was inflated by startup, so patch73 changes the estimate to use elapsed time and progress measured from the first observed model layer; testing/build pending. Dan says he has no polar cooler; leave it off despite firmware reporting the pin. See [physical test](validation/monitoring-physical-72/README.md).

**2026-11-06 monitoring update:** Candidate72 is installed and validated with the loopback fixture. It displays QIDI layer counters and an explicitly approximate time based on file progress; unknown input shows N/A. Linux CI and static checks passed. The new binary has not been tested during a real print. Candidate71 remains rollback. See [verification](validation/monitoring-72/README.md).

**2026-11-06 installed update:** Candidate71 adds a QIDI Auto Refill control under Device → Print Options. Linux CI, static checks, fixture GUI checks and real idle MAX4 off/on checks passed; refill was restored on. Installed image SHA256 72b56eef023aced0775a0d56ffc643dec2e2f2d19d52840d066029f7dcb898e1; candidate70 remains rollback. See [verification](validation/gui-71/README.md). The new binary has not run a physical refill print.

**2026-11-05 Orca update:** Candidate70 GUI submitted an ABS job that physically refilled A2→A3 and automatically resumed with visible blue deposition. The job was still running when recorded. See [Orca refill test](validation/orca-refill-2026-11-05/README.md). Orca refill settings controls remain unimplemented.

**2026-11-05 update:** The installed firmware fix physically passed an A2→A3 ABS refill: the printer automatically resumed and blue material was visible on the orange block. The test was still printing when recorded. See [retest](validation/refill-retest-2026-11-05/README.md). This was an API submission of the previously reviewed QIDI job, not an Orca refill validation.

Updated 2026-11-04. **Candidate70 is software-accepted and installed for personal
Linux x86_64 use with the X11 backend (XWayland on GNOME).** The general port is
not complete: automatic refill and broader physical validation remain unfinished.
One authorized sparse T2→A1 physical print completed on2026-11-04; see below.

**Latest status:** Dan reports a large remaining PLA jam, has powered the MAX4
off, and will repair it tomorrow. Hardware testing is paused at his request.
Do not heat, feed or submit another job until recovery resumes. Clear the jam and
verify actual clean extrusion before another refill test; the installed fix has
not yet been exercised by a physical refill.

**Current hardware session:** Dan subsequently authorized backing up and fixing
the MAX4 host firmware and repeating the ABS refill test. The reversible,
hash-pinned extension is installed and Klipper returned ready after a service
restart; the whole printer was not rebooted or power-cycled. Original vendor
modules and MCU firmware are unchanged. The private backup was verified both on
the printer and this computer. See [deployment](validation/firmware-fix-2026-11-04/deployment.json)
and [fix/rollback instructions](firmware-fixes/max4-refill-tool-identity/README.md).
The official QIDI Studio repeat `MAX4-QIDI-ABS-refill-fixed-20261104.gcode.3mf`
was interrupted by a full printer reboot during startup, before deposition;
**no physical fix acceptance yet**. The reboot initiator is not yet established.
The fix remained enabled after reboot. A subsequent printer-side eject command
was observed; do not submit another job while Dan is handling the feed.
Dan subsequently reported a PLA extruder jam and then confirmed it was fixed.
Read-only preflight now shows loaded_slot=slot16, an empty toolhead sensor,
A1 absent, A2/A3 present, and all heater targets0. Dan instructed proceeding after
the front-cover observation; the camera still showed it removed, so do not claim
reassembly was visually verified. The [retry](validation/firmware-fix-2026-11-04/retry/README.md)
was submitted from official QIDI Studio, then cancelled from the printer side at
reported layer22. The uploaded G-code again matches the failed reference exactly.
No formed block was visible after lowering the bed: advancing layer/filament
telemetry did not prove successful extrusion. The earlier statement that deposition
was established was unsupported. Refill never triggered; correction_count remained0.
All heater targets0 were verified after TURN_OFF_HEATERS; a later printer-side
A2 eject operation reheated the nozzle to a280C target. Do not confuse that later
manual recovery with the completed test cleanup. Actual extrusion/adhesion behavior
awaits Dan's observation before any further print. Physical refill acceptance is pending.
Its executable G-code is byte-identical to the failed larger reference.
Dan reports refill works when starting from printer memory. That observation is
recorded, but the reason for the different behavior has not been independently
traced. The historical no-firmware-change statements below describe earlier runs.

Release: [candidate70 deliverables](https://github.com/chevydan6/OrcaSlicer-QIDI/releases/tag/qidi-linux-2026-11-03-c70).
The definitive identity/gate record is [accepted-70.json](validation/accepted-70.json).
[Publication verification](validation/release-70.json) confirms all8 GitHub asset
digests match their local files. Release assets include AppImage, matching patched source, complete integration kit,
manifest, checksums, test reports and GUI/installation evidence. Verify SHA256SUMS.

## Exact accepted input

- Repository/branch: chevydan6/OrcaSlicer-QIDI, main; recovered workspace `/home/dan/qidi-orca-port`.
- Recovered integration revision: `70d58fc17f0132d926424a5a74144bf80cb1dcfd`.
- Binary build input: `7352b62f30804ecbeaa96c7996ff86614fadf7a8`; **70 patches**.
- Orca pin: `896557bce5281553ee0c6210f2da301b3b3c262e`.
- QIDI Studio pin: `403b619d56147160bb883e94f95a7951245bc6d0`.
- Reconstructed source commit: `54d95481c2e88abba71bfd5b43889c75d40cb728`.
- Exact downstream tree: `dd5107b2ecaa9dc53d7c503ebf096ae11e8fc68b`.
- AppImage SHA256: `7614dd15d467d0bf08b9e8846111e29940da4c53248a1d238a35d53b1dff35a7`.
- Original GitHub artifact ZIP SHA256: `5a8b2e0b004f96278039321f4dff6b8d7cacb3e5b2bb4135cf5ea294bd442fcc` (GitHub digest verified).
- Patched source archive SHA256: `70f5a306805a32144cb59ac3aac010d47fb417685b9b63d12e5e44e289d80e01`.
- Test-report ZIP SHA256: `b74e6cb5e6e8165dad57cd650c6dc4ffa88d59cd91f1299827feb737375b7cbc` (GitHub digest verified).

Later integration commits contain acceptance evidence, documentation and the native
installer's explicit --x11 option; the product source/patches/pins and tested binary
are unchanged. The packaged resources/qidi-port-build.json matches all70 patches.

## Verified software

[Integration41622045346](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41622045346)
and [static41622050016](https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41622050016)
passed. Actual reports establish compilation, **2,916 unit cases with no failures,
skips or disabled cases; seven CLI regressions; 72 vendor bundles; 21 MAX4
slicing/persistence cases**. All patches reproduce the expected tree.

[GUI70](validation/gui-70/README.md) records **63 passed cases on that exact
AppImage**, after its complete CI pass. Fresh setup, blank-key connection and
cancel/reopen; twenty Box/external editor cycles, slot colors, duplicate opens,
disconnects and delayed callbacks; all supported controls; zero/four Boxes;
telemetry/HTTP/WebSocket/camera faults and recovery; sparse/reversed/multi-Box
mappings, external mode, original support-first import/slice/preview; stale/fresh
object exclusion; rejected unsupported jobs; Box temperature persistence;
timelapse On/Off and storage guard; post-control slicing; normal and pending-request
shutdown all passed. Both GUI processes exited0. Non-QIDI A1 slicing also passed.
The fixture binds only127.0.0.1:19025, records/discards requests and never forwards.

[Installation70](validation/install-70/README.md) verifies the actual launcher,
desktop entry, native chooser/export, settings persistence and clean exits.
The real GNOME/XWayland session additionally rendered the MAX4 profile/bed and
exited0. Native Wayland is **not accepted**: isolated Weston testing exposed
unresponsive main controls. Its later display-pipe exit was caused by the harness
closing the compositor, not an application crash. Use the tested --x11 installation.

## Installed build and rollback

- Menu: **OrcaSlicer QIDI (Custom)**.
- Launcher: `~/.local/bin/orca-slicer-qidi`.
- Installed image/AppDir: `~/.local/opt/orca-slicer-qidi/7614dd15d467d0bf/`.
- Settings: `~/.config/OrcaSlicer-QIDI` (native; separate from official slicers).
- MAX4 0.4 profile, QIDI materials and printer agents are configured; automatic
  preset updates are disabled. No printer or loopback test connection is delivered.
- Accepted settings backup: `~/.local/share/orca-slicer-qidi/backups/accepted-70-settings-2026-11-03.tar.gz`.
- Candidate69 is retained at `~/.local/opt/orca-slicer-qidi/2bed31d5e66ad36a1/` for
  comparison only; it failed timelapse GUI acceptance. There was no previous accepted
  custom installation on this computer. Keep accepted70 as the rollback baseline.
- Reinstall retained70 with `python3 scripts/install-linux.py IMAGE --extract --x11`.
  Close the application and back up custom settings before any future downgrade.
- No Flatpak package was built/accepted here. Historical Fedora packaging helpers
  remain available but are outside this Ubuntu milestone.

## Host and preserved failure evidence

Ubuntu24.04.5 x86_64/GNOME Wayland, GCC13.3, 24 logical CPUs, 14GiB RAM/23GiB swap,
about267GiB free after acceptance. Build/test parallelism2. Private displays were
allocated independently: Xvfb:2 for full GUI acceptance, :3 for installation.
Do not assume these numbers remain available. A missing display is an environment
failure. The old Fedora Flatpak/private-session-bus workaround was not carried over.

Optional Weston installation exposed pre-existing half-configured NVIDIA/kernel
packages; apt returned100 although Weston installed. No driver repair, firmware
change or reboot was performed. See recovery evidence/wayland-environment.json.

Earlier failed attempts remain in validation/gui-52, gui-57, gui-59, gui-62,
gui-64, gui-68 and gui-69. In particular, patch52/58/63 layout attempts were
insufficient; later material sizing, GTK allocation, import identity, physical-slot
guards, fan layout, external-job status and timelapse UI fixes were verified on70.
[The prior detailed handoff](validation/recovery-2026-11-03/pre-acceptance-handoff-70.md)
and Git history preserve historical passes/failures. Earlier binaries do not
contribute positive evidence to this final acceptance.

## Physical hardware evidence and boundary

The authorized ABS refill reference session completed two attempts in official
QIDI Studio2.07.02.73. The first failed initial loading (QDE_004_006); Dan confirmed
the cut donor was too short. The retry completed40 layers/21m21s in orange fromA2.
Its inlet became empty at layer38 but toolhead filament remained present through
completion; noA3 transfer occurred. Automatic refill remains **inconclusive**,
not passed or failed. All heater targets returned0; telemetry still reportedA2
loaded after normal end, so successful unload is not established. Both reference
GUIs exited0. [Reference evidence](validation/refill-reference-2026-11-04/README.md)
includes exact uploads, hashes, sanitized telemetry/history and retry HTTP/WS traces.
Next physical step: remove the block after cooling, establish cut timing/location,
and arrange enough remaining model consumption to reach runout. Orca comparison
is pending. No product source, pin or accepted-binary change accompanied this work.
Dan subsequently requested a larger test. The [30×30×32mm prepared jobs](validation/refill-large-2026-11-04/README.md)
use160 layers/~11.5m ABS, with the same temperatures and planned A2→A3 refill.
Official QIDI GUI export and both CLI slices were checked. Dan confirmed ready;
preflight established clear bed and restored A2/A3 feed. The [larger reference run](validation/refill-large-2026-11-04/run/README.md)
failed refill acceptance and was cancelled at layer61/160. The firmware initiated
reload after A2 exhaustion, changed value_t0 to slot2/A3, then enabled the slot0/A1
PLA feeder; telemetry and the reference GUI corroborated that wrong slot. No
manual Resume/load/refill command was sent. A subsequent [read-only firmware diagnosis](validation/firmware-refill-2026-11-04/README.md)
reproduced the cause using the exact loaded modules: inlet reload writes physical
replacement index2 to extrude_state, then resume interprets it as logical T2 and
loads retained value_t2=slot0. Seven offline cases passed; preserving the logical
tool corrected the requested slot in two counterfactuals. No live fix is installed. No blue
continuation was observed. History00002C confirms cancelled, not completed.
All heater targets0/standby and lampOff were verified; GUI exited0. The bed still
holds the block and the feed needs inspection/reset before another physical job.
Startup targeted280C despite the requested260C, sampled286C, then returned250C;
that discrepancy is unresolved. Exact run evidence and failure are retained.
Orca comparison is pending; no product or firmware changes were made.

On2026-11-04 Dan authorized a small physical test and delegated its setup choices.
Accepted70's actual GUI submitted a10×10×4mm cube using only logical T2 mapped to
physical A1 ([-1,-1,0]). The exact upload preserved T2 and its executable G-code
matched the reviewed draft. Firmware acknowledged value_t2='slot0' before start,
reported slot0 loaded, and the camera showed yellow purge, deposition and the
finished cube. All20 layers completed; matching printer history reports completed
in781.57s. Normal end unloaded to slot16 and all heater targets returned to0.
The isolated GUI exited0; the lamp was restored Off. Dan reported clearing the bed.
[Hardware evidence](validation/hardware-2026-11-04/README.md) includes the exact
uploaded project, hashes, sanitized request/response trace, telemetry and history.
Raw captures, camera frames and connection settings remain private/ignored.

The printer reports main MCU02.01.01.12, toolhead02.02.01.08, Box02.03.01.21 and
one box_v1. This session used A1's reported yellow Generic PLA, not the historical
November3 material arrangement. Overall firmware release and independent material
identity remain unestablished. Startup target240C briefly reached a sampled248.5C
and then stabilized; firmware warnings are retained. No PID/firmware changes were
attempted. The test does not measure dimensions or surface quality.

Two real monitoring defects were exposed: GUI layer count stays0/0 while firmware
reports layers, and remaining time incorrectly subtracts two elapsed durations.
See [follow-ups](validation/hardware-2026-11-04/monitoring-followups.md). Software
acceptance evidence remains unchanged; these hardware UI limitations are now
explicit. No product source changed during this session.

This one T2→A1 success does not establish the cause or general resolution of Dan's
original starting-filament symptom. Multiple-Box, support-first and sequential
QIDI Studio comparisons remain pending. Orca refill controls remain unimplemented. Dan loaded
matching ABS in A2/A3 for the authorized refill comparison; firmware now reports both blue ABS slots in one refill group and auto_reload_detect=1.
The physical colors are intentionally orange/blue; preserve the matching software
metadata. [Refill drafts/evidence](validation/refill-investigation-2026-11-04/README.md)
record the earlier preparation. Dan subsequently authorized the ABS print/runout
session and requested the larger repeat; that authorization persists. Cut timing
for the current run remains unconfirmed. No firmware flash or persistent firmware
configuration change is authorized by this print session.

## Implemented scope and unfinished requirements

Implemented: missing MAX4 materials; persistent Box print temperatures; chamber,
fans, light and speed; physical slot/RFID/material operations; Box/external
telemetry; pre-print mapping/options; LAN submission/monitoring; snapshots;
detection; named object exclusion; QIDI project/placeholder compatibility;
isolated Linux identity. Orca's engine and existing supported tuning are retained.

Unfinished/unsupported: automatic refill, manual drying, QIDI cloud/MQTT/tunnels,
broader physical verification, layer/ETA monitoring fixes, native Wayland acceptance
and other platforms.
Mixed Box/external, multicolor external and experimental multi-device QIDI jobs
are rejected. HTTPS/WSS is not accepted as verified secure transport; use trusted
local HTTP. See [limitations](docs/limitations.md) and [feature checklist](docs/feature-checklist.md).

## Next work

1. Fix the observed layer/remaining-time monitoring defects in a separate change,
   preserving non-QIDI Moonraker behavior. Accept a newly built matching artifact;
   do not transfer70's final evidence to a changed binary.
2. Investigate refill separately: inspect pinned QIDI Studio and read-only firmware
   command/capability evidence, then arrange a sequential QIDI Studio baseline with
   matching ABS in A2/A3. Confirm product/temperatures and a short donor, document
   the concrete session and obtain authorization before inducing runout. Capture
   settings, options, runtime commands and slot transitions; do not guess commands
   or reuse Bambu operations. One reported Box cannot validate multiple-Box cases.
3. Refresh official Orca pins only in a separate maintenance change, retaining70.
   Review shared CLI/import/shutdown/Moonraker/GTK changes and non-QIDI regressions.

Preserve identity distinctions: filament3 is logical2/T2; Box2 slot2 is physical5;
mapping[-1,-1,5] must not become[5], and T2 must not becomeT5. Physical slot is
4*box_index+slot_index. Snapshot all mappings/options before asynchronous upload;
reject missing/malformed mappings and never silently switch to external on lost
telemetry. Support-first preparationT2 and depositionT0 both require mappings.
Preserve copyright, AGPL and dependency notices in all deliverables.
