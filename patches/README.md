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
| 0007 | MAX4 pre-print leveling and QIDI timelapse settings | SelectMachine, OctoPrint local options |
| 0008 | Box temperature/humidity telemetry and enclosure display | QDSDeviceManager, QDSPrinterWebView |
| 0009 | Material editing, RFID preferences and generation-aware eject | PrinterTaskDispatcher, AMSMaterialsSetting, AMSControl |
| 0010 | Capture submission capabilities with the job | Downstream threading integration |
| 0011 | Linux default data isolation and fork identification | Downstream packaging |
| 0012 | Case-light control and separate named fan telemetry | PrinterTaskDispatcher, QDSDeviceManager |
| 0013 | Polar Cooler availability and print option | QDSDeviceManager, SelectMachine, public MAX4 proc_stats |
| 0014 | Hide incompatible Bambu auto-refill dialog on QIDI | Downstream UI integration |
| 0015 | Native fan/speed controls and LAN snapshot camera | PrinterTaskDispatcher, QDSPrinterWebView |

Profile content and protocol behavior are adapted from QIDI Studio. Core changes
integrate that behavior into current Orca's existing architecture. Tests and Linux
integration tooling are downstream additions. The checklist records validation
separately from implementation; a patch's presence does not certify hardware use.

16. `0016-qidi-detection-controls.patch` connects existing spaghetti and foreign-object detection controls to QIDI Studio's `SetPrintOptions` LAN commands and saved-variable telemetry. Sensitivity converts between Orca lowercase and firmware uppercase.

17. `0017-qidi-chamber-capabilities.patch` exposes a reported QIDI chamber heater to native monitor display/edit controls, with a 0–65°C range and without the unrelated Bambu air-duct prompt.
18. `0018-qidi-manual-cooler.patch` adds the QIDI Studio output-pin control and reported state to Print Options. It appears only when both installed-accessory and output-pin telemetry are available.

19. `0019-qidi-http-validation.patch` adds a loopback HTTP fixture for the actual upload and submission transports, API-key headers, selected 3MF plate, ordered setup and stop-on-error. These full-library tests require the integrated build; the isolated helper harness is not evidence that they ran.

20. `0020-max4-bed-types.patch` imports QIDI's unsupported-plate metadata and canonical enum matching for plate selectors while retaining older label-based profile compatibility. Qidi bundle version becomes 02.04.00.25.

21. `0021-qidi-desktop-integration.patch` namespaces optional Linux desktop/icon/protocol entry filenames with `-qidi`; installation continues to use the dedicated wrapper and does not register file associations.

22. `0022-qidi-modern-slot-status.patch` adapts QDSDevice::updateBoxDataByJson nested/flat decoded slot presence/material/color for explicit filament sync, bounds Box counts before allocation, and reports the loaded physical slot (including external slot16). Temperature-only updates retain tray metadata.

23. `0023-qidi-live-materials.patch` applies QIDI Studio decoded Box material/presence reports to native slots as partial updates, preserving explicit-sync identities when the material stays the same. Type resolution requires a compatible visible type; unknown materials remain placeholders. RFID changes can update the monitor without deleting other trays.
