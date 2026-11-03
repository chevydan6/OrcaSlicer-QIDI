# MAX4 and QIDI Box feature-port checklist

Status describes source implementation, not completion or printer certification.
The full integrated build and dedicated validation phase remain open.
No MAX4 is connected during this work; communication tests use local fixtures,
and printer-specific protocol/physical verification remains pending.

Build update: compiled AppImages exist through patch 38. All 19 MAX4 slicing
and persistence cases pass locally on that binary, including both original QIDI
Studio projects. All seven upstream CLI regressions and 72 vendor profile bundles
passed in CI. Four G-code import unit failures are addressed by patch 41; full
builds containing that fix and later GUI changes are running. Changed-line C++
checks passed through patch 43. Checks for patches 44/45 found a missing direct
window header, corrected by patch 46; its checks are running.

Actual GUI tests through patch 38 exercise Box load/unload/eject/RFID, four-Box and
zero-Box transitions, external-spool display, lamp, chamber, fan, speed and print
options against the loopback simulator. Malformed telemetry, HTTP failure,
delayed requests and WebSocket reconnection leave the tested GUI usable. See
[the recorded GUI evidence](../validation/gui-38/README.md). Final-build acceptance,
complete GUI submission mapping and hardware verification remain open.

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
| Camera | No QIDI native stream mode | Local web-proxy snapshot endpoint | URL cases checked; actual video, authentication and custom proxy behavior pending |
| Chamber heat | Profile temperatures and start macros | Native command translation, heater capability and live current/target telemetry | Isolated protocol checks pass; GUI and hardware pending |
| Box temperature during printing | JSON values ignored by core | Persistent settings/UI; logical VT indices in generated code | Compiled slicing and save/reload pass; final-build rerun pending |
| Box/external selection | Physical-slot mapping exists | Explicit enable_box; active-tool snapshot; reject missing/malformed mappings | Recording-transport submission order and stop-on-failure pass |
| External spool monitoring | Generic virtual-tray interface | QIDI external material/color report and exact type resolution | Isolated decoder/partial-update checks pass; GUI/hardware pending |
| Initial filament | Logical tool placeholders and mapping exist | Preserve sparse indices | Dedicated slicing/submission regression and physical check pending |
| QIDI saved projects | Unrecognized application marker; incompatible MAX4 names and automatic raft value | Recognize structured metadata; retain object/material assignments; migrate known settings | Both original QIDI projects import and slice on patch 38; GUI comparison ongoing |
| Load/unload | Native UI lacks QIDI translation | QIDI macros, selected physical slot | Isolated command checks pass; GUI/hardware pending |
| Eject | Missing | QIDI-only control; hidden for box_v2 identity | Command checks pass; GUI/hardware pending |
| RFID refresh | Dedicated agent method unsupported | Route native refresh to READ_RFID | Isolated checks pass; no real RFID requests sent |
| RFID settings | Native preferences lack QIDI translation | Insert/boot macros and telemetry flags | Source tests added; no printer settings changed |
| Slot material/color editing | Native editor lacks QIDI translation | RGB/vendor/product command, guarded string literals | Isolated checks pass; re-sync/GUI pending |
| Box monitoring | Filament sync only | Temperature/humidity/loaded physical slot; modern nested/flat slot sync and live material/presence updates; preserve partial metadata | Nested/flat firmware formats checked in isolation |
| Start/end/change G-code | MAX4 macros present | Height guards and Box thermal preamble | 19 compiled slicing cases pass with generated G-code checks |
| LAN printing | Moonraker upload, 3MF selected plate | Ordered Box mode/mapping/options before start | Compiled loopback HTTP tests pass; end-to-end GUI submission still pending |
| Experimental batch/multi-device printing | Separate upstream submission path | QIDI entry point refuses the job because this path lacks per-printer slot/options snapshots | Single-printer submission supported; batch limitation is explicit; compiled refusal/GUI check pending |
| Bed leveling option | QIDI option ineffective/hidden | MAX4 G31/G32 selection | Recording-transport check passes |
| Timelapse option | UI and frame macros exist | QIDI Moonraker settings request | Recording-transport check passes; actual HTTP pending |
| Object skipping | Bambu numeric-ID interface only | QIDI named-object chooser and EXCLUDE_OBJECT translation | Isolated name/telemetry checks pass; GUI/hardware pending |
| Detection settings | Existing spaghetti/FOD controls | QIDI variable commands, sensitivity and reported settings | Isolated command checks pass; full GUI/hardware pending |
| Polar cooler | QIDI flag not recognized | Firmware-gated print option and job snapshot | Offline dispatch checks pass; manual toggle in Print Options; actual GUI and hardware pending |
| Auto refill | Native Bambu UI only | Incompatible dialog hidden | QIDI local dispatcher has an ambiguous command spelling; verify before porting |
| Manual drying | Shared upstream Bambu classes | Not enabled for QIDI | Active QIDI source path and firmware protocol need verification |
| QIDI cloud/MQTT | Different network architecture | Not implemented | Proprietary QIDI networking library/auth integration not bundled |
| Coexistence | Upstream application identity | Linux default datadir, wrapper and desktop entry isolated | Compiled GUI coexistence test pending |
| Reproducible source | Official commits pinned | Ordered patches; temporary-index tree verification | Patch tree verification passes; rerun after changes |
| Installable Linux artifact | Build infrastructure available | AppImage CI and per-user installer | Earlier 32-patch AppImage built; current build and release acceptance remain pending |

## Acceptance cases for the dedicated validation phase

1. Load all four MAX4 nozzles and the newly added materials; save/reload printer and
   filament settings in an isolated datadir.
2. Slice single-material and multicolor models, including a project with unused
   leading filaments, reversed slots, slots on multiple Boxes, support-first
   printing, and external-spool mode.
3. Trace each logical initial tool through BOX_PRINT_START, T commands and the
   print dialog's physical slot map. Check first-layer and change temperatures.
4. Reject malformed/out-of-range mappings instead of silently using stale mappings.
   Source guards and isolated checks now cover numeric overflow and partial mappings; integrated transport/GUI validation remains required.
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
it must never forward requests or execute G-code. The table defines the final-build gate. Partial results on earlier compiled
revisions are recorded in validation/gui-32 and validation/gui-38; they do not
complete this gate.

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
