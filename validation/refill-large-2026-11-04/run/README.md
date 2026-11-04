# Larger QIDI Studio reference — refill failure, cancelled

Official QIDI Studio 2.07.02.73 submitted the authorized larger ABS reference.
Natural donor exhaustion triggered automatic reload, but the sequence activated
physical slot 0 (A1, yellow PLA) instead of the intended physical slot 2 (A3, blue
ABS). The agent cancelled at layer 61/160 before any resumed model deposition was
observed. This does not pass refill acceptance and is not an Orca runtime result.

## Exact job and setup

Dan confirmed ready after requesting the larger test. Camera preflight showed a
clear bed; A2/A3 were present, both deliberately identified as blue Generic ABS,
with auto_reload_detect=1 and the firmware group [1B,1C]. A2 is physically orange;
A3 physically blue. A1 remains yellow PLA. Initially loaded_slot=slot16 and the
toolhead sensor was false. Existing nozzle222C/bed100C targets were observed before
submission; these were not set by the agent during preparation.

Job: MAX4-QIDI-ABS-refill-large-20261104.gcode.3mf. Model30×30×32mm,160 layers,
~11.5m ABS. Only logical T0 maps to physical1/A2 ([1]); A3 is the refill partner.
Requested printing250C,preparation260C,bed100C,chamber/Box0. Leveling On;
timelapse/polar Off. The actual uploaded archive SHA256 is
368200e6fe59e419d7dafa517104e936f8ed5f7594d1b225716bd8e01e1ad72f.

HTTP80 option/mapping commands returned200; print=true upload returned201.
Downloaded actual job is byte-identical to capture extraction and its executable
commands match the pre-submission GUI export. One redundant bed100C command at
layer2 differs from the earlier prepared export; it was reviewed before submission.
No scheduled tool change, manual load, Resume, refill-enable or reload command was
sent. The official profile retains stock MZV startup commands, unlike Orca.

## Observed sequence

Times in telemetry are Unix seconds; firmware log lines retain the printer clock.

- A2 inlet first absent at1793785933.1485, layer35,2956.54mm reported consumption.
  Its displayed refill group became empty, but matching slot metadata remained.
- Firmware logged slot1 exhausted at09:56:17 and Start executing auto reload at
  09:58:30. It paused at layer61,4814.31mm consumed; toolhead filament was still
  present at the initial pause. No controller command initiated that pause.
- The toolhead sensor first sampled false at1793786421.6197. Firmware logged
  auto_reloading_successful at10:00:41. The saved logical mapping changed from
  value_t0/value_t1=slot1 to slot2; value_t2 remained slot0.
- At10:00:56 the firmware log enabled stepper=slot0. Telemetry first reported
  loaded_slot=slot0 at1793786466.6555 and toolhead filament present again at
  1793786488.6765. QIDI's GUI displayed the yellow A1 feed path. Post-run variables
  report last_load_slot=slot0 and last_load_filament_id=QFA90 (PLA).
- The printer remained paused at layer61; no blue model deposition or automatic
  continuation was observed. The agent cancelled through QIDI's normal GUI.
  History00002C confirms cancelled after1709.94s, not completed.

This establishes a wrong-feeder reference sequence, not a proven root cause.
A physical-slot/logical-tool indirection error is a testable hypothesis: the new
physical slot index2 also names logical T2, whose retained assignment is slot0.
No physical actuation of T2 was requested by this job. Do not rewrite T0 to T2,
compact mappings, or clear unrelated assignments merely to conceal the behavior.

## Shutdown and other findings

Cancellation initially retained nozzle250C/bed100C targets. GUI target0 commands
were captured, but an immediate query still showed the old targets. The agent then
sent TURN_OFF_HEATERS; standby and every nozzle/bed/chamber/Box target0 were verified.
The lamp was restored Off. The reference GUI exited0; its private display and
capture were stopped. Loaded-slot telemetry remains slot0; successful unload is
not claimed. The block remains on the bed and the feed requires inspection/reset
before another print.

Startup unexpectedly targeted280C despite HOTENDTEMP=260; the maximum sampled
nozzle temperature was286C, above the reported ABS maximum280C. It subsequently
returned to250C before model deposition. Cause is unresolved; no independent
client heater override was captured. Do not describe this as verified temperature
compliance. No PID, firmware or persistent printer-configuration change was made.

Read-only config establishes pause_on_runout=true and an AUTO_RELOAD_FILAMENT call
when Box/refill flags are enabled. This run also shows automatic reload may begin
before the toolhead sensor empties; the sensor macro alone is not the whole flow.
The sensor was disabled during startup/pause and enabled while printing.

## Evidence and next investigation

result.json, mapping-sensor-events.json, telemetry-sanitized.jsonl, selected live
configuration/status, filtered firmware events, job history, upload identity and
HTTP/WebSocket command traces are retained. Camera frames/raw captures remain
private; frame hashes identify retained images. The upload and evidence checksums
are in SHA256SUMS. Cut timing/location was not confirmed; the observed inlet
exhaustion and automatic-reload log are direct evidence independent of that detail.

The official QIDI_MAX4 public tree at47fc14cefe064dbd30b90582429fe650883ae900
contains box_config.py but does not expose the multi_color_controller/box_extras
reload implementation. It cannot establish the loaded firmware's root cause.
The live printer reports software_version="?"; MCU versions are separately recorded
in the hardware evidence. No firmware update is proposed as an unverified fix.

Next: obtain/inspect the exact executing refill implementation or a more detailed
firmware trace; distinguish replacement selection from the subsequent load command.
Keep sparse logical mappings intact. A future controlled comparison needs the bed
cleared and donor/feed reset, plus a reviewed response to the temperature mismatch.
Accepted Orca70, its source pins and software acceptance remain unchanged. Its
physical refill comparison and refill controls are still unfinished.

## Subsequent read-only diagnosis

The later [installed-firmware replay](../../firmware-refill-2026-11-04/README.md)
reproduced the previously hypothesized indirection bug: cmd_detect_auto_reload_func
writes physical replacement2 to extrude_state, while try_resume_print_box1 reads
value_t2 and loads slot0. Seven offline cases and two diagnostic call-site probes
passed against copies matching the loaded modules. This updates the earlier
"unproven" interpretation above while retaining the original physical evidence.
No live firmware correction or additional print occurred.
