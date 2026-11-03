# Filament identities and MAX4 submission

A project filament, a G-code tool and a physical Box slot are separate identities.
The G-code keeps the project's logical indices. The print dialog supplies the
physical mapping when submitting the job.

| Identity | Sparse-project example |
| --- | --- |
| Filament shown in the slicer | Filament 3 |
| Zero-based logical index | 2 |
| Generated tool command | `T2` |
| Chosen physical location | Box 2, slot 2 |
| Zero-based physical slot | 5 |
| Submission mapping array | `[-1, -1, 5]` |
| Firmware variable assignment | `value_t2 = 'slot5'` |

Do not compact the mapping to `[5]`: that would assign logical tool 0 and leave
tool 2's old firmware mapping untouched. Likewise, do not replace `T2` with `T5`
in the sliced file. A physical slot is `4 * box_index + slot_index`, with both
indices zero-based and in 0–3.

The selected plate's filament IDs are captured in `PrintParams.extra_options`
on the GUI thread. Each used logical ID must have a valid physical mapping before
upload/submission. Missing, noninteger, out-of-range and overflowing entries reject
the complete mapping. Unused entries remain `-1`. The submitted mapping determines
Box mode; a temporary missing Box status must not silently select external mode.

The agent sends `enable_box=1` and the `value_tN` assignments before starting the
uploaded file. External-spool mode sends `enable_box=0` and supports one used
logical filament. QIDI's external telemetry slot 16 maps to Orca's virtual tray
254. It is not a seventeenth Box slot.

## Support-first reference behavior

The saved QIDI support-first project uses logical tool 0 for its raft and logical
tool 2 for its object. QIDI Studio emits `BOX_PRINT_START EXTRUDER=2`, then starts
deposition with `T0` and later changes to `T2`. Both tools need physical mappings.
The preparation tool and first deposition tool therefore need separate checks;
forcing both to the same number would change the reference behavior.

The reference archives and their actual QIDI Studio traces are in
`validation/qidi-reference/`. The isolated downstream tests validate mapping and
submission ordering with recording transports. Compiled slicing, actual GUI
selection and full communication tests are tracked separately in the feature
checklist. Physical feeder behavior remains unverified; these findings do not
prove the cause of the user's original printer-side symptom.
