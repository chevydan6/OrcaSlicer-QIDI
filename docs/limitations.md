# Remaining limitations and physical verification

No MAX4 is connected to this workstation. All recorded communication tests use
127.0.0.1:19025, whose fixture records and discards requests. A recorded heater,
load, RFID or start request does not prove that a printer accepts or executes it.
The final acceptance record identifies which software revision passed each test.

## Supported scope and gaps

- Public LAN/Moonraker communication is implemented. QIDI account login, cloud
  discovery, proprietary networking, MQTT and remote tunnels are not bundled.
- Single-printer jobs support Box mappings and single-material external-spool
  mode. Mixed Box/external jobs, multicolor external-spool jobs and incomplete
  mappings are rejected. Experimental multi-device submission refuses QIDI jobs
  because that separate path lacks a per-printer mapping snapshot.
- Manual drying and automatic refill are not enabled. Public source evidence did
  not establish an unambiguous active LAN command for both workflows. The
  incompatible Bambu refill/calibration/reset operations are hidden for QIDI.
  Filament Box temperatures used during printing are implemented separately.
- Current Orca process and material tuning is retained where a counterpart
  already exists. Missing QIDI profiles are imported with attribution. Matching
  controls and G-code does not make the engines or print quality identical.
- Native camera uses the reported local HTTP snapshot endpoint. Actual MAX4
  camera URLs, authentication and proxies still need printer-side verification.
- New QIDI-specific interface strings fall back to English when a translation
  catalog has no translation. Some shared upstream monitoring labels still say AMS.
- This deliverable targets Linux x86_64. Other platforms have not been built.
  The Fedora/LXQt host uses the GNOME 50 Flatpak runtime and a private session bus
  for file chooser support. Native AppImage dependencies vary by distribution.
- Official Orca application/preset updates do not include the downstream patches.
  Keep automatic preset updates disabled and rebuild this port for updates.

## Starting filament: what is proven

Software tests preserve logical indices through slicing and submission, including
unused leading filaments. The GUI case selecting filament 3 and physical B2 emits
T2 and sets value_t2 to slot5 before the simulated start. Support-first projects
retain separate preparation and deposition tools, matching QIDI Studio's reference
trace. See filament-mapping.md and the validation records.

The physical cause of the reported MAX4 starting-filament symptom is not proven.
The port explicitly sets Box mode, validates every used tool mapping, and captures
submission options before asynchronous upload. Those software fixes still require
an actual printer comparison with its installed firmware.

## Hardware checks requiring separate authorization

Record the MAX4 firmware version, Box count and slot layout first. Agree on each
physical operation before performing it. Suggested checks include single-material
external mode, sparse logical filament 3 to B2, reversed/multiple-Box mappings,
support-first startup, filament changes, RFID and material sync, chamber/fan
telemetry, camera, and network failure recovery. Heating, feeding, motion and print
starts are never part of an automatic software acceptance run.

No software test suite can guarantee that a GUI will never crash. The control
stability gate covers documented malformed inputs, delayed/failed communication,
dialog lifetimes, repeated actions, recovery and subsequent slicing. Unobserved
hardware responses or platform conditions can still expose defects.
