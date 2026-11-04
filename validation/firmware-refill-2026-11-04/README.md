# MAX4 refill diagnosis — reproduced in the installed firmware

The larger QIDI Studio reference failed because the inlet-runout handler confused
a physical replacement-slot index with a logical G-code tool index. This diagnosis
uses copies of the printer's actual compiled modules, not a reconstructed slicer
implementation. No live firmware/configuration write, restart, heating, feeding,
motion or print was performed during this investigation.

## Failure chain

The reference job used logical T0 mapped to physical slot1 (A2 orange ABS). Matching
replacement ABS was in physical slot2 (A3 blue). Both intentionally had blue software
metadata. The retained unrelated assignment value_t2='slot0' pointed to A1 yellow
PLA. That assignment was not part of this job and should never have been consulted
as the replacement's tool identity.

| Stage | Installed firmware behavior | Consequence |
| --- | --- | --- |
| Inlet exhaustion | BoxExtras._execute_auto_reload issues AUTO_RELOAD_FUNC SLOT=slot1 | Runs the donor's inlet-runout handler |
| Replacement selection | BoxExtruderStepper.switch_next_slot finds physical slot2 and rewrites mappings that pointed to slot1 | value_t0 and value_t1 correctly become slot2; value_t2 remains slot0 |
| Refill handoff | cmd_detect_auto_reload_func saves extrude_state=2, using the physical replacement index | A physical slot number is stored where resume expects a logical tool |
| Resume | Live RESUME macro calls TRY_RESUME_PRINT; BoxExtras.try_resume_print_box1 reads value_t{extrude_state} | Reads value_t2='slot0' |
| Loading | Resume calls slot0.extruder_load_single_func | Selects A1 PLA instead of A3 ABS |

The "auto_reloading_successful" sub-status is emitted before loading the new
filament. It cannot independently establish a successful transfer. The handler
then issues RESUME automatically; no manual Resume was sent by the agent.

Cython's retained debug information identifies these execution sites:

- box_extras.py:1660 — dispatch AUTO_RELOAD_FUNC.
- box_stepper.py:1158 — save the physical index as extrude_state.
- box_stepper.py:1161 — issue RESUME.
- box_extras.py:1438 — read the logical value_t mapping using extrude_state.
- box_extras.py:1444 — call the resolved physical feeder's load method.

These are embedded source positions recovered through controlled exception stacks
from the compiled modules. The original Python sources are not present in the
installed extras directory; these numbers are not links to files in this repository.

## Identity and read-only access

Read-only SSH/SFTP copied the relevant installed modules. Authentication material
is excluded. /proc/174130/maps showed the same paths/inodes as the copied files;
remote SHA256 hashes matched the local copies. See running-module-identity.json
and snapshot-manifest.json. Firmware source/module files remain private/ignored.

- box_stepper.so SHA256: 58ee8c61bffc3d4e18edc9e56a326495b6a218348bbfb13f7a012a946039b0a5
- box_extras.so SHA256: 0878b5b9d48d71e6bb1a83792776a7f59a529239cc1ca35e9a55102721bde2a6
- multi_color_controller.so SHA256: b7e3bc21156fb9df9f5eea07f2c596a17c7ea5db852a36139ba9773160e43592

The process uses /home/qidi/klippy-env/bin/python, resolving to ARM64 Python3.9.2.
The firmware API reports software_version="?". This diagnosis applies to these
installed modules; it does not assert that every firmware release has the same bug.
MCU/toolhead/Box version observations are preserved in the earlier hardware record.

## Offline verification

replay.py executes the copied Cython functions under QEMU aarch64 in a fresh Linux
network namespace. There is no connection to the MAX4. Hardware imports and printer
objects are fakes; flushing is simulated as successful, and physical loading is
intercepted before execution. Selection, mapping updates, the wrong extrude_state
write, and resume lookup execute the actual firmware methods. Live RESUME/TRY_RESUME
routing is represented explicitly by the harness, using resume-macros.json.

Seven assertions passed:

| Case | Physical feeder requested |
| --- | --- |
| Recorded T0→A2, retained T2→A1, intended refill A3 | A1: reproduces the defect |
| Destination's matching logical tool also points to A3 | A3: accidental success masks the defect |
| Sparse T2→A2, then A3 replacement | A3: selection updates T2, so this case happens to work |
| Logical T2→physical5, replacement6, retained T6→physical0 | Physical0: same defect with another Box |
| No matching replacement material/color | No load request |
| Offline counterfactual preserving logical T0 | A3 |
| Offline counterfactual preserving logical T2 for physical5→6 | Physical6 |

Two additional diagnostic interceptions locate the offending write and resume
mapping read in the compiled functions. Full event sequences and call stacks are
in replay-results.json. These are software reproductions, not new physical tests.
The two counterfactuals replace only the fake saved state immediately before resume;
they are not an installed firmware patch or an accepted hardware fix.

The real [reference telemetry and firmware logs](../refill-large-2026-11-04/run/README.md)
corroborate the sequence: automatic-reload start, logical mapping changed to slot2,
slot0 stepper activated, slot0 loaded, toolhead filament returned, no resumed model
deposition, then cancellation. Post-run extrude_state=2 and last_load_slot=slot0
were independently read from the printer. The original inconclusive/failed evidence
is retained.

## Reproduction

Keep the private analysis workspace outside version control. Copy the installed
module files by read-only SFTP and verify the hashes above. The emulator needs the
printer's /usr/bin/python3.9, /usr/lib/python3.9, dynamic loader and required shared
libraries under runtime/, plus qemu-aarch64-static under emulator/usr/bin/.
This session extracted Ubuntu's qemu-user-static package locally; no host package
installation or printer package change was required.

From the integration repository root:

```sh
bash validation/firmware-refill-2026-11-04/run-offline.sh \
  research/firmware-refill-2026-11-04 \
  validation/firmware-refill-2026-11-04/replay.py \
  --module-dir research/firmware-refill-2026-11-04/snapshot/home/qidi/klipper/klippy/extras \
  --output validation/firmware-refill-2026-11-04/replay-results.json
```

The launcher creates an isolated network namespace and drops back to the invoking
user before running the emulator. It requires local permission for that namespace;
there is no authentication or network client in the replay script.

## Corrective direction and remaining limits

Keep the active logical tool identity through the refill operation, while updating
its logical-to-physical assignment to the replacement. Resume must resolve that
logical tool once. An alternative implementation may carry an explicitly physical
replacement slot through a separate load path. In either case, preserve sparse and
aliased mappings and validate the replacement before motion.

Do not "fix" this by compacting mappings, changing T0 to T2, or overwriting unrelated
value_t entries. Such changes conceal the bug and can break other jobs. A source-level
firmware correction is preferable to a blind binary patch. Full load/flush/error/
retry/resume behavior still needs validation before an installed correction.

No firmware patch has been installed. Accepted Orca70 and both source pins are
unchanged. Orca refill controls and its physical refill comparison remain unfinished.
The reference startup temperature discrepancy remains a separate unresolved issue.
The printer was finally verified idle with all heater targets zero and lamp Off.
