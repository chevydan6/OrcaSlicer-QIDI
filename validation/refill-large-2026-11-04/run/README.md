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

Current status: accepted by printer and startup underway. Outcome pending.
