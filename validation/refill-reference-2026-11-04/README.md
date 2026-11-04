# QIDI Studio physical ABS refill reference — first attempt failed during loading

Dan authorized autonomous execution and reported A2 already cut. A2 is physically
orange ABS and A3 blue ABS; both intentionally remain blue in software. Firmware
reports automatic refill enabled and group 1B/1C. No manual reload, forced tool
change or Resume has been sent. This is the official QIDI Studio reference, not
physical refill validation of Orca candidate70.

The official QIDI Studio 2.07.02.73 GUI submitted
`MAX4-QIDI-ABS-refill-A2-A3-20261104.gcode.3mf` on 2026-11-04.
Logical T0 maps to physical slot1/A2. The block is 30×30×8mm, 40 layers, approximately
2.9m of model filament. Printing250C, startup260C, bed100C, chamber/Box0C;
bed leveling enabled, timelapse and polar cooler disabled. The plate was clear.

The imported custom machine did not preserve removal of the two stock MZV
input-shaper commands: QIDI Studio's GUI restored them. The submitted reference
therefore uses standard QIDI startup including those commands. Firmware reported
X MZV48.8 and Y ZV39.6 before the second command changed Y to MZV39.6. No persistent
firmware configuration was edited. This runtime difference must be recorded in
the later Orca comparison; the offline normalized draft is not the actual upload.

The actual uploaded archive was retrieved read-only from the printer and its
executable commands match the reviewed GUI export. See submission-plan.json and
actual-upload.3mf. Archive SHA256:
07413d522e356168d2c5ad38c0806217ffd163d6c761a24f1f80c8ea6391b03d.
G-code SHA256:
999a5df1ba1b12ac66135327391d5ec2048ae9f1cce66c9459d034c31b6c97c8.

Capture limitation: initial packet capture covered7125, but the QIDI HTTP submission
used a different port; it did not capture those HTTP requests/responses. Firmware's
timestamped command store records mapping/options and SDCARD_PRINT_FILE. An80-port
capture was added after startup. Do not claim a complete submission packet trace.
Private captures, settings and camera images are excluded from GitHub.

Result: initial loading failed before layer1 with QDE_004_006 at1793781906.85.
A2 was selected, its inlet changed to absent, and the extruder sensor never reported
filament. No A3 transition occurred. Dan confirmed the cut donor was too short and
requested a retry. This is not a valid printing-stage automatic refill comparison.
The GUI cancelled the job (history00002A:cancelled). Bed remained targeted100C in
the initial cancelled snapshot; the agent's GUI interaction sent explicit bed
TARGET=0 at1793781976.93. Subsequent standby telemetry confirms all targets0.
The lamp was turned off and QIDI Studio exited0. Do not claim cancellation alone
verified heater shutdown. A2 was subsequently restored by Dan for the retry.

[The restored-donor retry](retry/README.md) is now running in the same official reference.
