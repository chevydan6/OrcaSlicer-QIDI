# MAX4 and QIDI Box feature-port checklist

Status describes source implementation, not completion or printer certification.
The full integrated build and dedicated validation phase remain open.

| Workflow | Existing Orca | Downstream implementation | Validation / remaining work |
| --- | --- | --- | --- |
| MAX4 machine profiles | Four nozzle sizes and machine limits | Preserve profiles; height guards; pre-print capability | Structure passes; runtime load pending |
| MAX4 materials | 234 of QIDI's 247 files | 13 missing files; Orca IDs and inheritance | All 268 relevant profile entries resolve; tuning differences under review |
| Process profiles | All 16 source files have counterparts | Preserve current Orca tuning | Compare resolved differences and actual slicing |
| Chamber heat | Profile temperatures and start macros | Native command translation and live current/target telemetry | Isolated protocol checks pass; GUI and hardware pending |
| Box temperature during printing | JSON values ignored by core | Persistent settings/UI; logical VT indices in generated code | CTests added; full slicing execution pending |
| Box/external selection | Physical-slot mapping exists | Explicit enable_box before job; abort on empty Box map | Recording-transport submission order and stop-on-failure pass |
| Initial filament | Logical tool placeholders and mapping exist | Preserve sparse indices | Dedicated slicing/submission regression and physical check pending |
| Load/unload | Native UI lacks QIDI translation | QIDI macros, selected physical slot | Isolated command checks pass; GUI/hardware pending |
| Eject | Missing | QIDI-only control; hidden for box_v2 identity | Command checks pass; GUI/hardware pending |
| RFID refresh | Dedicated agent method unsupported | Route native refresh to READ_RFID | Isolated checks pass; no real RFID requests sent |
| RFID settings | Native preferences lack QIDI translation | Insert/boot macros and telemetry flags | Source tests added; no printer settings changed |
| Slot material/color editing | Native editor lacks QIDI translation | RGB/vendor/product command, guarded string literals | Isolated checks pass; re-sync/GUI pending |
| Box monitoring | Filament sync only | Temperature/humidity; preserve tray metadata | Nested/flat firmware formats checked in isolation |
| Start/end/change G-code | MAX4 macros present | Height guards and Box thermal preamble | Engine-generated G-code tests pending |
| LAN printing | Moonraker upload, 3MF selected plate | Ordered Box mode/mapping/options before start | Full HTTP integration pending; no printer contacted |
| Bed leveling option | QIDI option ineffective/hidden | MAX4 G31/G32 selection | Recording-transport check passes |
| Timelapse option | UI and frame macros exist | QIDI Moonraker settings request | Recording-transport check passes; actual HTTP pending |
| Polar cooler | QIDI flag not recognized | Firmware-gated print option and job snapshot | Offline dispatch checks pass; manual status-page toggle still pending |
| Auto refill | Native Bambu UI only | Incompatible dialog hidden | QIDI local dispatcher has an ambiguous command spelling; verify before porting |
| Manual drying | Shared upstream Bambu classes | Not enabled for QIDI | Active QIDI source path and firmware protocol need verification |
| QIDI cloud/MQTT | Different network architecture | Not implemented | Proprietary QIDI networking library/auth integration not bundled |
| Coexistence | Upstream application identity | Linux default datadir, wrapper and desktop entry isolated | Compiled GUI coexistence test pending |
| Reproducible source | Official commits pinned | Ordered patches; temporary-index tree verification | Patch tree verification passes; rerun after changes |
| Installable Linux artifact | Build infrastructure available | AppImage CI and per-user installer | Builds running; no successful artifact yet |

## Acceptance cases for the dedicated validation phase

1. Load all four MAX4 nozzles and the newly added materials; save/reload printer and
   filament settings in an isolated datadir.
2. Slice single-material and multicolor models, including a project with unused
   leading filaments, reversed slots, slots on multiple Boxes, support-first
   printing, and external-spool mode.
3. Trace each logical initial tool through BOX_PRINT_START, T commands and the
   print dialog's physical slot map. Check first-layer and change temperatures.
4. Reject malformed/out-of-range mappings instead of silently using stale mappings.
   Investigate numeric overflow and partial mapping validation in the inherited code.
5. Use localhost HTTP/WebSocket fixtures for upload, mapping, pre-print options,
   selected 3MF plate, failure handling and telemetry updates. Do not use a real
   printer in automated software tests.
6. Run full compilation, targeted and broader CTests, actual CLI slices, profile
   checks, GUI persistence and coexistence checks; retain logs and artifact hashes.
7. Only with explicit authorization: inspect the actual printer firmware/version
   and perform separately agreed physical checks. Do not conflate those checks
   with software validation or start an unsolicited print.
