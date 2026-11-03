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

24. `0024-qidi-mapping-validation.patch` snapshots used logical filament IDs with the job and validates every active mapping before HTTP submission. Invalid types/ranges/unsigned overflow reject the entire mapping; unused holes retain logical positions. Box/external mixing and multiple-material external change assist are rejected because no QIDI equivalent is implemented.

25. `0025-qidi-object-exclusion.patch` ports PrinterTaskDispatcher's EXCLUDE_OBJECT operation using firmware-reported names. Native Print Options offers a named-object chooser during printing; already excluded names are omitted. Command strings are validated before dispatch. This avoids assuming Bambu numeric object IDs match Klipper object names.

26. `0026-qidi-external-materials.patch` ports multi_color_controller.extra.filament_info to the native external spool, independent of Box count. Box/external resolution shares exact compatible type/name matching. Modern composite types are preserved; unknown materials no longer silently fall back to the first visible material.

27. `0027-qidi-native-wiring.patch` makes reported QIDI capabilities expose the Print Options entry point, makes the submitted slot selection determine Box mode, rejects conflicting physical-slot/external-mode requests, and normalizes trailing slashes before removing the Moonraker camera port.

28. `0028-qidi-nested-status-cache.patch` adds an opt-in cache merge policy for QIDI multi_color_controller only. Nested partial temperature updates retain the reported Box count and material fields; other Moonraker agents keep their existing field replacement semantics. Production cache-body isolation checks and full-library regression cases cover both policies.

29. `0029-default-cli-filament-diameter.patch` fixes an upstream CLI crash found by the baseline regression run. A standalone filament preset may omit diameter; flush calculation runs before full defaults are applied. Create the schema default before that calculation. The existing `cli_malformed_input` test reproduces the crash without this change; compiled verification of the fix remains pending.

30. `0030-qidi-integration-build-fixes.patch` resolves full-build and static-check findings: expose Box identity through a const accessor, use the existing AMS collection accessor, select the HTTP string-body overload explicitly, and include the required exception/base-agent headers.

31. `0031-qidi-control-stability.patch` rejects missing/malformed physical slot selections before native load/unload dispatch, defers the object chooser using a weak window reference, prevents duplicate chooser dialogs, and reacquires the selected device after the modal loop. Invalid-control regression cases exercise the agent error boundary without a printer connection.
