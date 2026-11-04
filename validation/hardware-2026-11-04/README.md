# MAX4 physical test preflight,2026-11-04

Dan instructed: "go ahead and do a test and use the MAX4". A small test is being
prepared on accepted candidate70. **No physical job has been submitted.**
The earlier user requirement to confirm loaded material/temperature limits and
supervision before active testing remains outstanding. This is not a failed print.

Current read-only checks: printer ready/standby, axes unhomed, all three heater
targets0, nozzle27.5C, bed23.3C, chamber23.95C; configured nozzle0.4mm; one Box.
Runout values indicate A1 present and A2–A4 absent. A1 metadata says yellow
Generic PLA. Saved labels alone do not establish the actual loaded material.
A private camera snapshot was inspected; it is not committed.

Offline draft:10x10x4mm cube, only logical filament3/T2, proposed A1 physical0
mapping[-1,-1,0]. Generic PLA draft uses210C printing/60C bed, chamber/Box0.
The standard MAX4 startup requests240C for BOX_PRINT_START preparation and
performs homing, purge/cleaning and bed preparation. Estimated total9m42s.
These temperatures are proposed for confirmation, not approved operating limits.
The accepted installed AppImage hash was verified before slicing. T2 was retained;
no T0/T1 model deposition or physical-slot tool rewrite was introduced.

Next: Dan confirms actual filament/slot, temperature limits including240C startup,
clear fitted plate and nearby supervision. Finalize/review the job, then perform
the authorized small session and record expected versus observed feeding/startup.
No refill/runout experiment, firmware update or persistent printer configuration
change is included. A QIDI Studio reference comparison remains a separate
sequential step; no competing control session has been started.
