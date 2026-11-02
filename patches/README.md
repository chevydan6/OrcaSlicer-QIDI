# Downstream patch series and attribution

Apply patches in lexical order to the Orca revision in `sources.json`.
The application remains AGPL-3.0; retain both projects' licenses and source notices.
QIDI reference revision: `403b619d56147160bb883e94f95a7951245bc6d0`.

| Patch | Change | QIDI source reference |
| --- | --- | --- |
| 0001 | MAX4 height guards; preserve Orca same-tool guard | X 4 Series machine 0.4 mm profile |
| 0002 | Box temperature settings, UI, G-code and persistence/slicing tests | PrintConfig, Preset, Tab, GCode |
| 0003 | Thirteen missing MAX4 filament files with Orca IDs/inheritance | X 4 Series filament profiles |
| 0004 | Explicit Box/external submission mode; sparse logical indices | SelectMachine local submission |
| 0005 | Chamber control/telemetry and RFID command translation | PrinterTaskDispatcher, QDSDeviceManager |
| 0006 | Native RFID and load/unload UI wiring with physical slot selection | PrinterTaskDispatcher local Box macros |

Profile content and protocol behavior are adapted from QIDI Studio. Core changes
integrate that behavior into current Orca's existing architecture. Tests and Linux
integration tooling are downstream additions. The checklist records validation
separately from implementation; a patch's presence does not certify hardware use.
