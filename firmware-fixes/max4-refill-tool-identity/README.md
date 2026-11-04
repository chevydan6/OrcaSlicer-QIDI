# MAX4 Box v1 inlet-refill tool identity fix

This reversible Klipper extension preserves the active logical tool when the
installed firmware's inlet-runout handler writes the replacement's physical index
to extrude_state. It retains vendor selection, mapping updates, flushing, loading,
resume and failure paths. The original .so files are unchanged.

The extension wraps only AUTO_RELOAD_FUNC SLOT handlers and intercepts the erroneous
write during that handler. It verifies the active logical tool maps to the donor,
the new mapping matches the replacement, and the replacement inlet is present.
Malformed/inconsistent states pause and report an error. Nested refill is rejected;
all other saved-variable writes pass through. get_status exposes enabled/version,
correction count, last correction and last error.

It is pinned to the exact three installed vendor module hashes in the Python file.
An unsupported firmware update fails configuration until this extension is removed
or revalidated. It is not a general replacement for vendor firmware.

## Validation

The isolated ARM/Python3.9 replay executes the actual copied vendor Cython methods.
The fixed flow passes 25 cases, including the recorded mismatch, sparse T2,
reversed slots, multiple Boxes, high logical indices, no replacement, invalid state,
replacement presence/mapping guards, duplicate entry, unrelated writes, firmware
hash rejection, failed flushing, successful load through RESUME_PRINT, and failed
load without resume. Hardware and motion are fakes. These checks do not constitute
a physical refill pass. See validation/firmware-fix-2026-11-04.

From the repository root, using the private copied runtime/modules:

```sh
bash validation/firmware-refill-2026-11-04/run-offline.sh \
  research/firmware-refill-2026-11-04 \
  firmware-fixes/max4-refill-tool-identity/test_firmware.py \
  --module-dir research/firmware-refill-2026-11-04/snapshot/home/qidi/klipper/klippy/extras \
  --output validation/firmware-fix-2026-11-04/offline-tests.json
```

## Installation and rollback

Back up Klipper, its Python runtime, printer configuration and service definition
before deployment. Retain the private archive both on the printer and a separate
computer, verify SHA256 and archive integrity, and exclude credentials/configuration
archives from GitHub. This backs up host firmware/runtime/configuration, not MCU
flash; the extension does not modify MCU firmware.

With the printer idle and heaters off, copy qidi_refill_tool_identity.py to
/home/qidi/klipper/klippy/extras/ and qidi_refill_tool_identity.cfg to
/home/qidi/printer_data/config/. Add this line before printer.cfg's SAVE_CONFIG block:

```ini
[include qidi_refill_tool_identity.cfg]
```

Restart the Klipper service, verify the printer reaches ready, and query the
qidi_refill_tool_identity status object. enabled must be true, corrected_count zero,
and last_error null before testing. A startup failure must be rolled back.

Rollback: remove that exact include line, remove the added .py/.cfg files (after
retaining their identity/evidence), then restart Klipper. Vendor modules were never
replaced. The deployment records retain the original and installed printer.cfg
hashes; restore the original whole file only if no later edits need preserving.
The full private archive also retains the original configuration and runtime.

Dan explicitly authorized backup, installation and repeat testing. The repeat uses
one controlling slicer at a time and captures actual mapping, firmware correction,
feeder state, deposition and automatic continuation. A manual Resume or tool change
must not be counted as automatic refill. Slicer candidate70 and its pins are unchanged.
