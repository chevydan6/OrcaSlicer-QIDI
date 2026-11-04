# QIDI Studio retry — completed; refill inconclusive

Dan reported the first donor was too short and requested another print. Preflight
showed A2/A3 present, the blue ABS refill group restored, loaded_slot16, standby,
and all heater targets0. The center of the plate was clear in the camera.

The same official reference GUI submitted MAX4-QIDI-ABS-refill-retry-20261104.gcode.3mf.
Mapping T0→physical1/A2; A3 is the firmware refill partner. Temperatures remain
250C print,260C preparation,100C bed, chamber/Box0. Options remain leveling On,
timelapse/polar Off. No manual refill/Resume command was sent.

Capture covers all TCP ports to this printer and establishes HTTP80: mapping,
Box/polar settings and G31 returned200; timelapse-disable returned200; multipart
upload with print=true and plateindex=1 returned201. WebSocket uses7125.

The initial retry export matched the first job's executable commands. Restoring
Textured PEI before submission and reslicing removed one redundant M140 S100 at
layer2. Inspection of the actual upload during homing established that this is
the only executable difference; initial bed target/wait100 and all other commands
are unchanged. See actual-review.json/diff. Exact upload and hashes are retained.

Result: history00002B confirms completed in1281.33s (21m21s), all40 layers.
Camera showed orange purge and an orange completed block. A2 inlet first sampled
empty at layer38, while the toolhead still detected filament; no slot2/A3 load
transition or toolhead runout occurred during model deposition. The firmware's
reported refill group became empty when the A2 inlet became empty. This is an
inconclusive refill test, not evidence that automatic refill works or fails.

The agent requested the physical cut after stable first-layer deposition. No
reply specified when/where the retry was cut; do not infer that from the request.
The exact sensor transition is retained. The firmware completed normal end with
all heater targets0 and standby. However, loaded_slot remained slot1 and the
toolhead sensor remained true despite UNLOAD_FILAMENT T=0 in the exact job.
Successful unloading is therefore not established. QIDI Studio exited0 and the
lamp was restored Off. The block remains on the bed awaiting removal when cool.

Next: establish cut timing/location and enough remaining model consumption for
runout before completion; restore/recover the donor as needed. Repeat the reference
runout, then compare accepted Orca70 sequentially. No Orca refill print occurred
in this session. All product pins, patches and accepted binary remain unchanged.
See result.json, transitions, sanitized telemetry/messages, exact upload and
HTTP/WebSocket traces. Raw packet captures, connection settings and camera images
remain private; hashes identify retained frames.
