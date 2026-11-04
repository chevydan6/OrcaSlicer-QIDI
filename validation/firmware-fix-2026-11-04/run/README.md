# Authorized patched-firmware reference repeat — interrupted

Official QIDI Studio2.07.02.73 submitted the same160-layer ABS block used in the
failed reference, with T0 mapped to physical slot1/A2. The uploaded G-code matches
the reviewed export and failed reference byte for byte. A download from printer
storage matches the captured upload. See submitted-job.json for hashes.

The fix is installed with SHA256
4513412930926926dc0d72ae1a0fbcdac3c1eba92e09c7b712171d7db842bd0f;
Klipper service restart returned ready. No whole-machine reboot or MCU flash was
performed. A2 contains orange ABS and A3 blue ABS; both deliberately retain matching
blue software metadata. Unrelated value_t2=slot0 remains present to expose the
original failure. Dan confirmed the bed and feed were ready before submission.

The printer rebooted during startup, before model deposition or refill. The
initiator is pending Dan's clarification. Low host uptime and a new Klipper PID880
confirm a whole-host reboot, rather than merely an application connection loss.
No restart command was sent by the agent after submission. History00002D reports
cancelled with a duration inconsistent with the observed startup; do not treat
that duration as a measured elapsed time. All pre-reboot samples remain layer0.
The correction counter remained0 and the extension remained enabled after boot.
A subsequent printer-side EJECT_FILAMENT_CONTROL SLOT=0 command was observed;
the agent did not send it or submit a second job. Heater targets were initially0
after boot, but later nozzle target222 was observed during that separate operation.
Do not describe the final printer state as heaters off based on the earlier sample.

The isolated QIDI Studio process exited0, and its private display was stopped.
This attempt is inconclusive. Required repeat evidence is preservation of logical
T0 during refill, replacement A3 actually loading, blue deposition, automatic
continuation without manual Resume, and successful completion.
Startup temperature behavior remains a separate unresolved observation.
Candidate70's source, pins and binary are unchanged; an Orca comparison is pending.
