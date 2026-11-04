# Larger QIDI Studio reference — running

Dan confirmed the printer ready after requesting the larger test. Preflight camera
showed the plate clear. A2/A3 were present with matching blue ABS metadata and
firmware refill enabled/group1B/1C. Printer standby,loaded_slot16,toolhead sensor
false. Existing nozzle222C and bed100C targets were observed before this job; these
were not set by the agent during preparation.

The official QIDI Studio2.07.02.73 GUI submitted
MAX4-QIDI-ABS-refill-large-20261104.gcode.3mf. Model30×30×32mm,160 layers,
~11.5m model ABS. T0 maps to physical1/A2; A3 is firmware refill partner.
Printing250C,preparation260C,bed100C,chamber/Box0. Leveling On,timelapse/polar Off.
No manual tool change,Resume or refill-enable command was used.

HTTP80 commands returned200 and print=true upload returned201. Downloaded actual
job is byte-identical to capture extraction; executable commands match the
pre-submission GUI export. One redundant bed100C command at layer2 differs from
the earlier prepared export, reviewed before submission. Exact hashes and upload
are retained. This is reference runtime evidence, not a custom-Orca refill pass.

Current checkpoint: layer 31/160, printing from A2 with orange deposition visible.
A2 inlet and toolhead still report filament present; A3 transfer has not occurred.
The toolhead runout sensor is enabled during printing. Outcome remains pending.

Read-only firmware configuration shows pause_on_runout=true and invokes
AUTO_RELOAD_FILAMENT when enable_box and the saved auto_reload_detect flag are 1.
Both flags are 1 during this job. A transient pause is therefore not by itself a
refill failure; observe the automatic slot transition and resumed deposition.
No sensor state, refill command or Resume has been injected.

Startup unexpectedly targeted 280C despite the reviewed HOTENDTEMP=260 argument.
It returned to 250C before model deposition. This runtime discrepancy is retained;
its cause is unresolved. No independent heater override appears in the captured
client commands. The sensor was disabled during startup and enabled for printing.

Cut timing/location for this larger attempt has not been confirmed by Dan. Do not
infer the time of cutting from an instruction or the earlier smaller attempt.
