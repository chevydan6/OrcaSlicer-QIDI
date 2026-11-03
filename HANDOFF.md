# Project handoff

Updated 2026-11-03. **Candidate70 is software-accepted and installed for personal
Linux x86_64 use with the X11 backend (XWayland on GNOME).** The general port is
not complete: automatic refill and physical print validation remain unfinished.

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

Only authorized read-only inspection of Dan's MAX4 was performed: connectivity,
capabilities/telemetry, slot metadata and a valid1920x1080 camera JPEG. Reported
main MCU02.01.01.12, Box MCU02.03.01.21, one box_v1, blue Generic ABS present in A2;
other slots absent; loaded path external16. Overall firmware release and actual
materials/temperature limits need Dan's confirmation. Existing bed/chamber targets
were observed unchanged. No heating, feeding, motion, RFID refresh, configuration
writes or print starts were sent to real hardware. Sanitized traces are in
validation/recovery-2026-11-03; credentials/raw camera images are not committed.

Software evidence does not establish that the physical starting-filament symptom
is fixed. Automatic refill is **not enabled**; auto_reload_detect=1 and an empty
auto_refill array do not establish the firmware prerequisites or command protocol.

## Implemented scope and unfinished requirements

Implemented: missing MAX4 materials; persistent Box print temperatures; chamber,
fans, light and speed; physical slot/RFID/material operations; Box/external
telemetry; pre-print mapping/options; LAN submission/monitoring; snapshots;
detection; named object exclusion; QIDI project/placeholder compatibility;
isolated Linux identity. Orca's engine and existing supported tuning are retained.

Unfinished/unsupported: automatic refill, manual drying, QIDI cloud/MQTT/tunnels,
physical operation/print verification, native Wayland acceptance and other platforms.
Mixed Box/external, multicolor external and experimental multi-device QIDI jobs
are rejected. HTTPS/WSS is not accepted as verified secure transport; use trusted
local HTTP. See [limitations](docs/limitations.md) and [feature checklist](docs/feature-checklist.md).

## Next work

1. Review [the concrete supervised hardware plan](docs/hardware-validation-plan.md)
   with Dan. Confirm firmware, loaded materials/slots and temperature limits, then
   obtain explicit authorization for grouped heating/motion/feed/print operations.
   One reported Box cannot validate B2; begin with confirmed A2 if appropriate.
   Compare QIDI Studio and accepted Orca sequentially using identical inputs.
2. Investigate refill separately from this stable milestone: trace QIDI Studio's
   active implementation and authorized protocol evidence. Determine configuration,
   job options and runtime commands; do not guess or reuse Bambu operations.
3. Refresh official Orca pins only in a separate maintenance change, retaining70.
   Review shared CLI/import/shutdown/Moonraker/GTK changes and non-QIDI regressions.

Preserve identity distinctions: filament3 is logical2/T2; Box2 slot2 is physical5;
mapping[-1,-1,5] must not become[5], and T2 must not becomeT5. Physical slot is
4*box_index+slot_index. Snapshot all mappings/options before asynchronous upload;
reject missing/malformed mappings and never silently switch to external on lost
telemetry. Support-first preparationT2 and depositionT0 both require mappings.
Preserve copyright, AGPL and dependency notices in all deliverables.
