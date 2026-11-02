# Source inventory and validation status

Both official repositories are cloned. Exact revisions and URLs are pinned in
`sources.json`; this integration repository stores the ordered patches and build
workflow. Both projects use AGPL-3.0; their licenses and existing notices remain
in the source trees. The root LICENSE is copied from QIDI Studio.

## Existing Orca support

The pinned Orca already has MAX4 machine profiles for 0.2/0.4/0.6/0.8 mm nozzles,
all 16 MAX4 process profiles, 234 of the 247 QIDI MAX4 filament files, the QIDI
printer agent, Moonraker LAN upload/monitoring, 3MF plate selection and Box slot
synchronization. The port extends those paths rather than replacing Orca networking.

`validation/max4-profile-inventory.json` compares inherited source values after
porting the 13 missing filament files: 268 model/machine/process/filament entries,
no missing counterparts or unresolved inheritance. Differences include deliberate
Orca schema adaptations and tuning. This report does not evaluate engine defaults
or certify equal print quality. Fan, speed, cooling and prime tower differences
still require review; wholesale replacement would change existing Orca behavior.

## Initial-filament path

Both engines export logical filament indices through `initial_tool` and
`initial_no_support_extruder`. The MAX4 start macro uses those indices, while
submission saves `value_tN = 'slotM'` to translate logical N to physical M.
Unused indices must stay in place: `[-1,-1,5]` means logical filament 2 uses slot 5.

QIDI Studio explicitly sets `enable_box` before saving mappings. Upstream Orca
omits that mode selection. The port adds it and distinguishes external-spool jobs.
This is a candidate contributor to the reported failure, not a hardware-confirmed
root cause. Complete slicing/submission regression coverage is pending.

The public MAX4 firmware reference at QIDITECH/QIDI_MAX4 revision
`47fc14cefe064dbd30b90582429fe650883ae900` shows that a local
`/printer/print/start` request does not consume the cloud-only `consumable` field.
Local mappings therefore remain explicit SAVE_VARIABLE commands, ordered before
print start. Firmware source inspection is not evidence of the installed version.

## Network dependencies

QIDI Studio dynamically loads `libqidi_networking.so` for its proprietary network
API. Its public source also implements LAN operations directly via Moonraker.
This port uses the existing Orca HTTP/WebSocket backend and those local protocols;
it does not bundle the QIDI network binary. QIDI account/cloud printing and its
MQTT/tunnel stack are not implemented. Existing Orca backends remain available.

## Software validation to date

- All-vendor profile structural check: 72 bundles, zero errors/warnings.
- Qidi profile version check: passed, bundle 02.04.00.20 to 02.04.00.25.
- The numbered patches reproduce the local downstream Git tree exactly.
- Production protocol helper bodies compile in isolation with C++17 and warnings
  treated as errors; sparse mappings, Box mode, chamber, RFID and load/unload
  assertions pass. This harness does not compile the full application.
- Full baseline and patched Linux builds are running on GitHub Actions. No full
  compilation, CTest, GUI profile loading/persistence or actual slicing success
  is recorded yet. HTTP integration tests and packaging validation are pending.

No printer has been contacted. Physical slot selection, filament motion, heating,
printing and firmware compatibility remain unverified and require authorization.

Additional general-port patches connect MAX4 bed leveling and QIDI timelapse
submission options, and show Box temperature/humidity in the native enclosure
display. The latter reuses QIDI Studio's enclosed four-slot UI classification;
remote drying is not enabled by that classification. These patches are not yet
in the running six-patch build.

Case-light commands, three named fan channels and the Polar Cooler submission
option are now implemented. Polar Cooler availability follows the firmware's
`notify_proc_stat_update.config_items["printing.polar_cooler"]` field. The public
MAX4 proc_stats implementation confirms that notification; its GET endpoint does
not include those configuration items, so it is not used as a substitute.

Auto-refill remains unimplemented: the public QIDI dispatcher spells its command
`SET_ENABLE_AUTO RELOAD`. A community report describes `SET_ENABLE_AUTO_RELOAD`
in printer HELP output, but the corresponding official firmware implementation
is not available in the inspected tree. The native Bambu replacement-material
dialog is hidden on QIDI instead of offering an ineffective operation.

## Profile differences retained deliberately

The resolved MAX4 0.4 mm machine start sequence matches QIDI Studio apart from
Orca's `chamber_temperature` spelling and QIDI's two forced `SET_INPUT_SHAPER`
MZV assignments. The port retains Orca's choice not to force a shaping algorithm.
End G-code and height guards match; filament-change G-code retains Orca's
same-logical-tool guard. Machine limit arrays keep Orca's existing second mode.
These are source comparisons, not generated-G-code or physical validation.

Many differences in the inventory are inherited values absent from Orca preset
JSON, even though Orca already defines the corresponding setting. In particular,
additional-fan layer controls, cooling before the tower, tower interface extrusion,
and fast-flush temperatures have Orca implementations. They are not missing
features merely because the source JSON report contains `null` on one side.
Orca intentionally treats `internal_bridge_support_thickness`,
`overhang_totally_speed`, `smooth_coefficient` and `silent_mode` as obsolete import
keys. The general port does not reintroduce those obsolete algorithms or replace
Orca's engine. MAX4 process speeds/accelerations, prime-tower sizing and some
material tuning still differ between the two slicers and require print-quality
comparison; no tuning-equivalence claim is made.

Detection controls reuse the existing native spaghetti/FOD interface. Only
reported QIDI saved variables enable their controls; commands translate to
`enable_noodle_detection`, `enable_pre_print_model_check` and uppercase
`noodle_sensitivity_level`. The manual Polar Cooler toggle is in Print Options,
using the same output pin as QIDI Studio; its job-start preference remains a
separate setting, as in QIDI Studio.

Modern slot synchronization now queries the complete multi_color_controller object and consumes QIDI Studio's box_inserted and decoded filament/color fields before legacy variables. Count validation prevents corrupt firmware values allocating unbounded slots. Live loaded-slot telemetry uses physical slot names, independent of logical tool numbers. Automatic RFID-driven material refresh remains a separate integration item; explicit Sync refreshes materials.
