# Downstream patch series and attribution

Apply patches in lexical order to the Orca revision in `sources.json`.
Every patch uses mail format with the original downstream commit's author/date
metadata. Both `git apply` and `git am` replay have been verified to reproduce the
development source tree; evidence is under `validation/`.
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

29. `0029-default-cli-filament-diameter.patch` fixes an upstream CLI crash found by the baseline regression run. A standalone filament preset may omit diameter; flush calculation runs before full defaults are applied. Create the schema default before that calculation. The existing `cli_malformed_input` test reproduces the crash without this change; the first custom build passes all seven upstream CLI regression tests, including this case.

30. `0030-qidi-integration-build-fixes.patch` resolves full-build and static-check findings: expose Box identity through a const accessor, use the existing AMS collection accessor, select the HTTP string-body overload explicitly, and include the required exception/base-agent headers.

31. `0031-qidi-control-stability.patch` rejects missing/malformed physical slot selections before native load/unload dispatch, defers the object chooser using a weak window reference, prevents duplicate chooser dialogs, and reacquires the selected device after the modal loop. Invalid-control regression cases exercise the agent error boundary without a printer connection.

32. `0032-qidi-material-update-stability.patch` ignores wrongly typed material names while preserving existing tray metadata, skips deferred object chooser work for closing windows, and includes the selected-device manager definition required by the new dialog code. The malformed-name regression failed before the fix and passes afterward in the isolated production-body harness, including AddressSanitizer/UndefinedBehaviorSanitizer execution.

33. `0033-qidi-chamber-telemetry-bounds.patch` rejects corrupt chamber readings before float/integer GUI conversions and bounds reported targets to the supported control range. Invalid independent fields do not discard valid measurements; malformed type and extreme-magnitude cases are covered by the sanitized harness.

34. `0034-qidi-project-import.patch` recognizes QIDI Studio's structured 3MF marker, preserves its model/material metadata, translates QIDI's automatic raft expansion to its actual 2 mm value, and maps MAX4 compatibility names to Orca's existing names. QIDI's product version is represented by a project compatibility baseline of 2.0.0, avoiding both a false newer-Orca rejection and obsolete plate-origin migration. The actual QIDI reference archive is included as an attributed import regression fixture. Compiled import and GUI checks remain pending.

35. `0035-qidi-control-callback-lifetime.patch` removes a raw agent capture from asynchronous G-code completions in the inherited Moonraker path. Callback snapshots carry a shared cancellation flag checked before queuing and delivery, and destruction invalidates that flag. It also reacquires the selected device before new Polar Cooler/eject control actions. Sanitized production-body regressions cover live delivery, queued delivery after destruction, and HTTP completion after destruction; full-app GUI cases remain pending. This lifetime correction also protects ordinary Moonraker agents.

36. `0036-qidi-import-test-accessor.patch` corrects the import regression's use of ModelConfig's non-template option accessor, identified by the changed-line compile/static check.

37. `0037-qidi-local-credentials.patch` applies Moonraker's optional API-key handling to QIDI: do not invent a dummy key, refresh changed credentials from the selected preset, preserve explicit logout/rebind behavior, and protect other agents' saved bindings during discovery. Extends the existing device-access regression cases to QIDI while retaining required-code behavior for other agents. Server authorization remains authoritative; compiled tests and GUI connection checks are pending.

38. `0038-qidi-callback-reset-stability.patch` invalidates queued/delayed callbacks when GUI callback registration changes or a printer connection is reset, as well as at destruction. This respects the application's existing shutdown sequence, which clears callbacks before deleting the agent. Production dispatcher/reset/destructor bodies pass the sanitized isolation harness; full-library cases also cover disconnect and re-registration.

39. `0039-qidi-legacy-slot-validation.patch` rejects corrupt legacy color/material/vendor indexes before integer conversion and validates runout sensor types/range. The original production block reproduced a float-to-int overflow at 1e300; the corrected block passes the sanitizer harness, including the explicit float-cast-overflow check. Full HTTP regression cases cover invalid numeric indexes without a real printer.

40. `0040-qidi-batch-submission-guard.patch` refuses experimental QIDI batch printing before opening its separate submission dialog, because that path lacks per-printer QIDI slot/options snapshots. It directs the user to single-printer submission and preserves other agents' batch behavior. Native GUI verification remains pending; QIDI batch support is a documented limitation.

41. `0041-upstream-gcode-import-compatibility.patch` restores recognition of upstream Orca G-code alongside the custom application banner. Four existing import/preview regressions caught this in the first compiled test run; the settings-import case now exercises upstream, downstream, and legacy headers. Compiled rerun pending.

42. `0042-downstream-window-title.patch` uses the downstream application name in project window titles, distinguishing the fork from an official Orca window without changing translation catalog or project identifiers.

43. `0043-qidi-connection-dialog.patch` gives QIDI a local address/API-key dialog and hides inapplicable PIN binding. It retains blank or arbitrary non-newline API keys, normalizes the selected endpoint, and lets the existing agent perform the connection in its background thread. QIDI no longer starts the legacy detached dialog worker or a verification SendJob. The connection timer is released on dialog destruction. Found during first GUI validation; compiled and control-failure checks pending.

44. `0044-refresh-layout-after-setup.patch` sends a main-window size event after the setup wizard. Both the unmodified upstream and first custom GUI had invisible page controls until a manual resize on the target GTK runtime. The baseline comparison is recorded under `validation/gui-layout`; compiled verification of the correction is pending.

45. `0045-qidi-settings-dialog-stability.patch` replaces Bambu-specific RFID timing/spool instructions and imagery with QIDI Box wording. Shared material/settings actions recheck the selected device before accessing a retained device pointer, including after the material warning modal loop. Settings for other agents retain their labels. Found while exercising native controls; final compiled/device-switch verification is pending.

46. `0046-layout-event-include.patch` includes the wx window declaration used by the deferred layout event. The no-precompiled-header check passes through patch 46.

47. `0047-guard-object-exclusion-against-current-job.patch` validates the object chooser's job and object names against the communication cache. A native modal loop can delay GUI status delivery; the offline GUI reproduced an old selection being sent after the job changed. Compiled GUI regression remains pending.

48. `0048-qidi-material-editor-profile-lookup.patch` resolves QIDI material choices through the printer's vendor display name and hides Bambu pressure-calibration/reset actions. The offline GUI exposed an empty material list. Final compiled GUI verification remains pending.

49. `0049-status-snapshot-access.patch` provides a protected, locked copy of Moonraker status for the stale-selection check, preserving private cache ownership. The static check caught direct access to private members in patch 47.

50. `0050-qidi-chamber-placeholder-compatibility.patch` preserves QIDI's chamber-temperature placeholder spelling as a vector alias during G-code generation. The installed GUI reproduced a parsing error when slicing an original QIDI project with its embedded machine G-code; prior CLI checks replaced the machine profile and missed that path. A slicing unit regression checks implicit and explicit vector access, and two additional integration cases retain the embedded machine. Compiled rerun is pending.

51. `0051-no-validation-dialogs-during-shutdown.patch` skips print-preset validation once shutdown is committed. Closing the installed candidate after importing a QIDI support project opened a belt/raft warning during preset reset, then the existing 30-second watchdog exited with status 1. This shared upstream reset path must not open new modal validation dialogs while closing. Compiled close/discard regression remains pending.

52. `0052-qidi-material-dialog-sizing.patch` clears the stale GTK fixed-dialog maximum before fitting the QIDI material editor on reopening. Repeated GUI opens clipped its action buttons by shrinking the window each time. Also hides the unrelated pressure-advance wiki link. Compiled repeated-open regression is required.

53. `0053-qidi-native-connection-dialog.patch` uses standard native address/key/CA and connect/cancel controls for QIDI. The shared custom inputs rendered clipped on the target GTK runtime. This path skips legacy Bambu dialog widgets and workers, validates the current agent, and retains the asynchronous local connection behavior. Compiled connection/cancellation verification is required.

54. `0054-preserve-embedded-qidi-compatibility.patch` retains the original MAX4 name when adding Orca compatibility aliases. The new no-override CLI cases exposed that replacement allowed a new Orca machine but rejected the original embedded QIDI machine. The import regression checks both names; unrelated printers remain constrained.

55. `0055-qidi-fresh-material-editor.patch` replaces a completed QIDI slot editor with a fresh window for Box and external slots. Runtime testing disproved patch 52's maximum-size hypothesis: five openings still shrank 25 pixels each. The new editor lifecycle avoids reuse of the affected GTK window and its old slot state; duplicate opening while shown is refused. Other agents keep their existing editor lifecycle.

56. `0056-qidi-native-slot-color-dialog.patch` uses a native single-RGB chooser for QIDI slot metadata, revalidating the selected device before/after the modal loop. The shared palette opened off-screen when the material editor appeared at the left edge in GUI55. Other agents retain the shared multicolor palette.

57. `0057-qidi-color-data-include.patch` directly includes the header defining `wxColourData`, as required by the failed 56-patch include-cleaner run. Runtime behavior is unchanged; a new matching integration/static build is required before acceptance.

58. `0058-gtk-notebook-layout-after-setup.patch` forwards a GTK frame size notification to the notebook so its current page is sized even when the book dimensions have not changed. GUI57 disproved patch 44 alone: fresh setup left Prepare blank until manual maximization. This correction needs compiled fresh-setup and normal-resize acceptance; it affects shared GTK layout.

59. `0059-qidi-bound-model-name.patch` resolves QIDI vendor model names as well as model IDs when displaying the bound printer type. Fresh native address connections store `Qidi X-Max 4`, whereas the older lookup recognized only `Qidi-XMax-4` and returned Unknown, leaving the material list empty. Other agents retain their lookup behavior. Compiled fresh-connection material editing remains required.

60. `0060-qidi-material-minimum-size.patch` sets a layout-derived minimum for QIDI material editors. GUI59 still produced 2x5 windows despite patch 55; native decoration handling caused the shrink. A debugger minimum prevented the observed shrink, but compiled repeated-open/lifecycle acceptance is pending.

61. `0061-qidi-persist-connection-endpoint.patch` retains the complete QIDI endpoint in discovery so the bound address keeps its port and HTTP/HTTPS scheme after restart. A protocol regression covers both schemes with a custom port; the existing non-QIDI discovery regression remains unchanged. Compiled restart acceptance is pending.

62. `0062-gtk-native-page-allocation.patch` queues native allocation when showing a GTK notebook page. GUI59's visible Prepare page retained a 1x1 GTK allocation; a diagnostic native page/book allocation restored it without changing window dimensions. Removes patch 58's ineffective synthetic event forwarding. Shared GTK startup/tab/resize behavior needs compiled verification.

63. `0063-defer-gtk-page-allocation.patch` defers native allocation until notebook selection and its callbacks finish, reacquiring the current page at delivery. GUI62 disproved patch 62 alone. The book owns the callback; removed pages are not captured. Compiled fresh setup, rapid tab switching and shutdown verification remain required.

64. `0064-qidi-vendor-product-material.patch` resolves a reported QIDI / PLA Rapido against the full preset alias QIDI PLA Rapido and replaces a previously generic tray ID when complete product metadata arrives. Adds visible/compatible/type/fallback regressions. GUI62 selected Generic PLA; compiled material synchronization and editor verification remain required.
