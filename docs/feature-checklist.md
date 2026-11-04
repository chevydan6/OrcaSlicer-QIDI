# MAX4 and QIDI Box feature-port checklist

Status describes source implementation, not completion or printer certification.
The candidate70 software milestone is accepted within the documented Linux backend scope.
Read-only LAN inspection of Dan's MAX4 is recorded in
[the recovery evidence](../validation/recovery-2026-11-03/printer-readonly.json).
One authorized sparse T2→A1 print completed on2026-11-04; see
[hardware evidence](../validation/hardware-2026-11-04/README.md). Real GUI layer/time
displays need fixes. Other physical workflows remain unverified. Automated communication tests
use only the non-forwarding loopback fixture.

Current acceptance: candidate70 (`7352b62`) passed compilation, 2,916 unit cases
without failures/skips, seven CLI regressions,72 vendor bundles,21 MAX4 cases,
static checks and63 GUI cases on the matching binary. Installed launcher/menu,
settings, chooser, slice/preview and exits passed using X11/XWayland. Native
Wayland remains unaccepted. See [GUI70](../validation/gui-70/README.md),
[installation70](../validation/install-70/README.md) and [exact identity](../validation/accepted-70.json).
The following tables distinguish the accepted software scope from hardware and
unfinished requirements.

| Current gate | Candidate70 result |
| --- | --- |
| Fresh setup, connection/cancel/reopen, blank key | Passed |
| Material/color edit,20 reopens,slot switching,duplicates,disconnect/callback lifetime | Passed |
| Load/unload/eject/RFID,chamber,three fans,light,speed,detection,polar controls | Expected fixture requests; GUI usable |
| Zero/four Boxes,external spool,box_v2 eject visibility | Passed |
| Sparse T2→slot5,reversed multi-Box mappings,support-first T2 preparation/T0 deposition | Original projects slice/preview and ordered simulated submission pass |
| Box print temperature persistence,project save/reload,placeholder compatibility | Passed |
| Missing/mixed/multicolor external mappings and experimental QIDI batch | Rejected before dispatch |
| Timelapse On/Off,bed leveling/polar job options,storage availability guard | Passed |
| Stale/fresh object exclusion,malformed telemetry,HTTP/delay/WebSocket/camera recovery | Passed |
| Post-control slicing,non-QIDI A1,normal/pending shutdown | Passed |
| Installed identity,menu/launcher,chooser,settings,actual GNOME/XWayland rendering | Passed; no loopback connection delivered |
| Physical T2→A1 print, real camera, normal end/heaters off | One20-layer cube completed; layer/time UI defects recorded |
| Automatic refill,manual drying,cloud/MQTT/tunnels,broader hardware cases | Unfinished/unverified |

The stability fixes include typed telemetry validation, bounded chamber numbers,
callback lifetime guards, stale dialog selection checks and QIDI-specific
connection/settings text. Native controls require the printer-agent preference
documented in the build guide. Source checks alone do not validate GUI behavior.

| Workflow | Existing Orca | Downstream implementation | Validation / remaining work |
| --- | --- | --- | --- |
| MAX4 machine profiles | Four nozzle sizes and machine limits | Preserve profiles; height guards; pre-print capability | All 72 vendor bundles and four nozzle-size slicing cases pass |
| MAX4 materials | 234 of QIDI's 247 files | 13 missing files; Orca IDs and inheritance | All 268 relevant profile entries resolve; tuning differences under review |
| Process profiles | All 16 source files have counterparts | Preserve current Orca tuning | Compare resolved differences and actual slicing |
| Fan and speed controls | QIDI part-fan number mismatch; speed selection ignored | Named fan commands; speed commands/telemetry | Offline command checks pass; hardware pending |
| Camera | No QIDI native stream mode | Local web-proxy snapshot endpoint | Offline GUI JPEG display, malformed frame, HTTP failure and recovery pass; real MAX4 native GUI snapshots verified; authentication/other proxies pending |
| Chamber heat | Profile temperatures and start macros | Native command translation, heater capability and live current/target telemetry | Protocol and offline GUI target/telemetry checks pass; hardware pending |
| Box temperature during printing | JSON values ignored by core | Persistent settings/UI; logical VT indices in generated code | Candidate70 compiled slicing and GUI save/reload pass; physical temperatures unverified |
| Box/external selection | Physical-slot mapping exists | Explicit enable_box; active-tool snapshot; reject missing/malformed mappings | Recording-transport submission order and stop-on-failure pass |
| External spool monitoring | Generic virtual-tray interface | QIDI external material/color report and exact type resolution | Decoder/partial-update checks and external-spool GUI display pass; hardware pending |
| Initial filament | Logical tool placeholders and mapping exist | Preserve sparse indices | Candidate70 sparse T2→slot5 submission passes; one physical T2→A1 print completed; original general symptom/comparison unresolved |
| QIDI saved projects | Unrecognized application marker; incompatible MAX4 names and automatic raft value | Recognize structured metadata; retain object/material assignments; migrate known settings | Candidate70 original sparse and support-first import/slice/preview pass |
| Load/unload | Native UI lacks QIDI translation | QIDI macros, selected physical slot | Candidate70 expected slot requests recorded; hardware unverified |
| Eject | Missing | QIDI-only control; hidden for box_v2 identity | Candidate70 physical-slot request and box_v2 hiding pass; hardware unverified |
| RFID refresh | Dedicated agent method unsupported | Route native refresh to READ_RFID | Protocol and offline GUI refresh pass; no real RFID requests sent |
| RFID settings | Native preferences lack QIDI translation | Insert/boot macros and telemetry flags | Candidate70 insertion/boot fixture requests pass; no real settings changed |
| Slot material/color editing | Native editor lacks QIDI translation | RGB/vendor/product command, guarded string literals | Candidate70 material/RGB edits and20 reopens pass; previous failed sizing evidence retained |
| Box monitoring | Filament sync only | Temperature/humidity/loaded physical slot; modern nested/flat slot sync and live material/presence updates; preserve partial metadata | Nested/flat firmware formats checked in isolation |
| Start/end/change G-code | MAX4 macros present | Height guards and Box thermal preamble | All21 MAX4 slicing/persistence cases pass, including original embedded machines |
| LAN printing | Moonraker upload, 3MF selected plate | Ordered Box mode/mapping/options before start | Candidate70 fixture jobs pass; physical T2→A1 upload/options/start and completed print verified |
| Experimental batch/multi-device printing | Separate upstream submission path | QIDI entry point refuses the job because this path lacks per-printer slot/options snapshots | Candidate70 compiled and GUI refusal before dispatch verified |
| Bed leveling option | QIDI option ineffective/hidden | MAX4 G31/G32 selection | Recording-transport check passes |
| Timelapse option | UI and frame macros exist | QIDI Moonraker settings request | Candidate70 On/Off request and storage-failure/recovery GUI checks pass; hardware unverified |
| Object skipping | Bambu numeric-ID interface only | QIDI named-object chooser and EXCLUDE_OBJECT translation | Candidate70 stale selection rejects dispatch and fresh selection sends exactly once |
| Detection settings | Existing spaghetti/FOD controls | QIDI variable commands, sensitivity and reported settings | Protocol and offline GUI toggles/sensitivity pass; hardware pending |
| Polar cooler | QIDI flag not recognized | Firmware-gated print option and job snapshot | Offline dispatch and native Print Options toggle pass; hardware pending |
| Auto refill | Native Bambu UI only | Incompatible dialog hidden | QIDI local dispatcher has an ambiguous command spelling; verify before porting |
| Manual drying | Shared upstream Bambu classes | Not enabled for QIDI | Active QIDI source path and firmware protocol need verification |
| QIDI cloud/MQTT | Different network architecture | Not implemented | Proprietary QIDI networking library/auth integration not bundled |
| Coexistence | Upstream application identity | Linux default datadir, wrapper and desktop entry isolated | Installed native identity/settings/menu verified separate; no other slicer settings changed |
| Reproducible source | Official commits pinned | Ordered patches; temporary-index tree verification | Patch tree verification passes; rerun after changes |
| Installable Linux artifact | Build infrastructure available | AppImage CI and per-user installer | Accepted70 AppImage installed with --extract --x11; no supported Flatpak package here |

## Acceptance cases for the dedicated validation phase

1. Load all four MAX4 nozzles and the newly added materials; save/reload printer and
   filament settings in an isolated datadir.
2. Slice single-material and multicolor models, including a project with unused
   leading filaments, reversed slots, slots on multiple Boxes, support-first
   printing, and external-spool mode.
3. Trace each logical initial tool through BOX_PRINT_START, T commands and the
   print dialog's physical slot map. Check first-layer and change temperatures.
4. Reject malformed/out-of-range mappings instead of silently using stale mappings.
   Source guards and isolated checks now cover numeric overflow and partial mappings; candidate70 transport/GUI acceptance is recorded above.
5. Use localhost HTTP/WebSocket fixtures for upload, mapping, pre-print options,
   selected 3MF plate, failure handling and telemetry updates. Do not use a real
   printer in automated software tests.
6. Run full compilation, targeted and broader CTests, actual CLI slices, profile
   checks, GUI persistence and coexistence checks; retain logs and artifact hashes.
7. Only with explicit authorization: inspect the actual printer firmware/version
   and perform separately agreed physical checks. Do not conflate those checks
   with software validation or start an unsolicited print.

## Required GUI stability gate

The user explicitly requires QIDI controls to be stable in the slicer GUI. Run
these cases against the compiled custom application with isolated settings and
a loopback-only printer simulator. Commands must be recorded by the simulator;
it must never forward requests or execute G-code. The table defines the gate completed by candidate70. Earlier partial records
in validation/gui-32 and validation/gui-38 remain historical evidence only.

| Case | Required behavior |
| --- | --- |
| No configured or connected printer | QIDI controls are hidden/disabled or safely refuse an action; no crash |
| Experimental multi-device action | QIDI jobs have complete per-device mapping/options or are refused before submission |
| Box absent, external spool, zero/four Boxes | Slot display remains consistent and unsupported operations are unavailable |
| Empty, malformed, removed or out-of-range slot selection | No command is sent for an unintended slot; no uncaught exception |
| Load/unload/eject, RFID, material/color, chamber/fan/light and print-option controls | Expected request is recorded by the simulator; GUI remains responsive |
| Repeated clicks and opening/closing dialogs | No duplicate object chooser, stale-window callback or process exit |
| Disconnect/reconnect or switch/remove the selected device while a dialog is open | Action is cancelled or revalidated against the current device; no stale-pointer access |
| New job/status arrives while object chooser is open | Old selection is not applied to a different job |
| Missing, partial, wrong-type and malformed telemetry | Invalid data is rejected without crashing; valid subsequent updates still work |
| HTTP error, timeout and dropped WebSocket | Error is handled, controls recover, and the GUI remains usable |
| Save/reload profiles and restart | QIDI settings persist and other slicer settings remain untouched |
| Slice and preview after using controls | Slicing and GUI rendering continue to work |
| Existing non-QIDI workflow | Existing profile loading, slicing and controls retain their prior behavior |

Record the build/artifact hash, exact cases, screenshots and failures. Source
inspection and isolated helper checks do not satisfy this GUI gate. Hardware
compatibility, actual motion/heating and print behavior remain separate checks.
