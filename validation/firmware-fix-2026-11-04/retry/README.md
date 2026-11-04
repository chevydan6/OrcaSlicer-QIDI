# Patched MAX4 refill retry after PLA jam recovery — in progress

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
The slicer candidate70 is unchanged. This running attempt is not a refill pass.
