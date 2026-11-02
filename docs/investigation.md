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
- Qidi profile version check: passed, bundle 02.04.00.20 to 02.04.00.23.
- The first six numbered patches reproduce the local downstream Git tree exactly.
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
