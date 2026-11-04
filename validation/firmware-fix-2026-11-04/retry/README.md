# Patched MAX4 refill retry after PLA jam recovery — cancelled before refill

Dan reported the PLA jam cleared and instructed proceeding. Preflight telemetry
showed loaded_slot16, an empty toolhead sensor, A1 absent, A2/A3 present, no Box
warnings, and all heater targets0. The camera showed no printed model on the bed.
The front cover appeared removed; Dan said it was fine and to proceed after that
observation. Do not describe reassembly as visually verified.

Official QIDI Studio2.07.02.73 submitted
MAX4-QIDI-ABS-refill-fixed-retry-20261104.gcode.3mf. T0 maps to physical slot1/A2
orange ABS, with blue ABS in A3 as the refill candidate. Both retain matching blue
software metadata. Retained value_t2=slot0 remains untouched. The original donor
cut must wait for steady model deposition. No manual Resume or forced refill is
part of this test.

The exported and actual uploaded G-code matches the failed reference byte for
byte. The captured archive matches a download from printer storage; hashes are in
submitted-job.json. Same model160 layers, printing250C/requested preparation260C,
bed100C, chamber/Box0, levelingOn, timelapseOff, polar coolerOff.
The known stock startup temperature discrepancy remains separately unresolved.

Firmware correction SHA256:
4513412930926926dc0d72ae1a0fbcdac3c1eba92e09c7b712171d7db842bd0f.
Enabled after the earlier full reboot, correction count0 before this attempt.
The slicer candidate70 is unchanged.

## Outcome

History00002E reports cancelled at1050.85 seconds; the last observed layer was22.
SDCARD_RESET_FILE arrived from the printer side, not this agent. A2's inlet and
toolhead sensor remained present throughout; no automatic refill event occurred
and correction_count remained0. Dan replied “ok” to the donor-cut instruction,
but physical tail length/cut position was not measured.

The lowered-bed camera showed no formed block, only small traces of orange
material. During printing the toolhead obscured the model area. The earlier
statement that steady deposition was established was unsupported: reported layer
advancement and filament use do not establish extrusion or adhesion. The actual
feed/adhesion failure awaits Dan's observation. This run neither passes nor
disproves the unexercised refill correction.

Cancellation retained250/100C heater targets. TURN_OFF_HEATERS was acknowledged
and all targets0 verified. A subsequent printer-side A2 eject operation heated
the nozzle again, with280C target observed; this was not agent-driven retry or
proof that heaters remained off. No new print was sent. The reference GUI exited0,
private display was stopped, and capture closed. Sanitized HTTP/WS commands,
telemetry, history and camera hashes are retained. Raw frames/capture stay private.
