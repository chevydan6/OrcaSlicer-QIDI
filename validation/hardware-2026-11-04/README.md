# MAX4 sparse starting-filament test, 2026-11-04

Dan authorized a printer test and then delegated the small test choices with
"no it didnt do as you please". Candidate70 submitted the job through its actual
native GUI using an isolated test datadir. The earlier draft and preflight remain
in Git history. **The printer history reports completed (781.57s, about13m02s). All20 layers
were printed; the camera showed a finished yellow cube attached to the plate.**
Normal end processing unloaded to slot16 and all nozzle/bed/chamber/Box targets
returned to0. Firmware then reset its live print_stats to standby; the matching
job-history entry supplies the completion acknowledgment. Dan subsequently
reported clearing the bed. The test GUI exited0 and the lamp was restored Off.

The test uses a 10×10×4mm cube, only slicer filament3/logical T2, mapped to A1
physical0: [-1,-1,0]. The real printer reports one box_v1 and A1 yellow Generic PLA
present, with a stored 190–240C range; A2–A4 are absent. This is reported metadata,
not an independent material identification. The illuminated camera showed a
fitted clear plate. Printing targets are210C nozzle/60C bed, chamber/Box0. Stock
MAX4 startup requests240C for Box preparation, purges, cleans and levels the bed.
Bed leveling is On; timelapse and polar cooler are Off.

The exact uploaded project is retained as MAX4-A1-T2-test-20261104.gcode.3mf.
Its G-code differs from the earlier CLI draft in generated timestamp, thumbnails
and serialized configuration comments, but all executable commands are identical.
T2 is retained; no T0/T1 model deposition or physical-slot tool rewrite occurred.
The stock startup purges substantially more filament than the0.38g model estimate.

Captured HTTP requests show upload201, Box enable plus value_t2='slot0', G31,
timelapse disable, polar disable and print/start, each successfully acknowledged.
Firmware subsequently reported loaded_slot='slot0', and yellow purge/deposition
was visible through the camera. No QIDI Studio session competed for control.
Raw packet captures, device settings and camera frames remain private/ignored;
only reviewed request/response fields and selected telemetry are committed.

There are real monitoring defects: layer counters remain0/0 in Orca despite the
firmware's20-layer report, and remaining time uses elapsed-duration subtraction.
See monitoring-followups.md. Firmware startup warnings are preserved separately;
no warning is silently treated as a failed print or dismissed as fixed.

This one-slot small test does not establish the cause or general resolution of
Dan's original starting-filament symptom. Multiple Boxes, support-first changes,
QIDI Studio comparison, automatic refill, runout, heated Box behavior, RFID,
material writes and network recovery remain outside this physical session.
No firmware flashing or configuration-file editing was performed. Ordinary job
submission changes Box mapping/options through the firmware's SAVE_VARIABLE API;
these are recorded explicitly in request-trace-sanitized.json.

The highest sampled nozzle temperature was248.5C during the240C startup target;
firmware emitted an unstable-temperature warning and subsequently stabilized.
The test did not pause or abort. Several invalid print-substatus warnings were
also logged. These messages and the original firmware settings were preserved;
no PID tuning or firmware changes were attempted. Print quality/dimensions were
not measured from the camera. The reported filament_used value is affected by
startup purge and end retraction and is not a calibrated consumption result.
