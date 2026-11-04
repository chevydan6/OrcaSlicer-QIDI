# QIDI Studio retry — in progress

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

Current result: startup underway. No automatic refill outcome established yet.
