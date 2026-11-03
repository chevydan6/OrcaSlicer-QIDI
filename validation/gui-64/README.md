# Candidate 64 GUI: fresh layout failed

Exact AppImage SHA-256: `7361aa78213b45cd087d93128d5481b467329fc22cfa4b5443b6248c7ffca435`.
Integration build input: `9b06cba3424e19e53a4235ce8b3bf9d455ea393a`.
GitHub archive digest, pins and all 64 manifest patch hashes verified; see
../recovery-2026-11-03/artifact-64.json.

Fresh isolated setup on Ubuntu 24.04.5/Xvfb :2 remains blank on Prepare after
idle (11/12). **Patch 63 is disproved.** No debugger intervention preceded these
failure screenshots. No real printer connection was configured.

## Diagnostic session, not acceptance

After recording failure, GDB attached to this process. Both DoShowPage and its
queued callback execute. The callback receives the correct Prepare native handle
and book handle. Queued GTK resize/allocation does not repair this session,
including a repeat from the debugger. Thus the earlier GUI59 intervention was
insufficient evidence for the general correction.

wx reports page rectangle (0,39,1200,727), while GTK's visible page remains 1x1.
Calling gtk_widget_size_allocate with that existing rectangle restores the UI
(18-diagnostic-direct-allocation.png). The pinned wx GTK DoMoveWindow implementation
also performs direct allocation in its native size-event path. Patch 66 applies
this only when a shown current page has mismatching native dimensions, with a
required preferred-size request first. Fresh binary verification remains required.

The diagnostic session exited normally with status 0. This does not establish a
full clean-exit or lifecycle gate. No final acceptance or installation follows.

## Clean restart material checks and removed-Box failure

A subsequent process started normally without debugger attachment. Manual
maximization was used for the control checks. QIDI / PLA Rapido now selects the
correct QIDI PLA Rapido preset (31); ten Box and ten external opens remain usable.

**Failed:** while the A1 editor was open, the fixture published zero Boxes. Confirm
still sent UPDATE_FILAMENT_INFORMATION SLOT=0 (33/34 and stale-material-request.json).
This is a stale GUI selection, not hardware testing. Patch 67 checks the latest
locked protocol snapshot before material/load/unload/eject/RFID dispatch; external
slot 16 remains independent of Box count. Compiled/GUI retesting is pending.

The fan control dialog also opens at 2x5 (46-fan-click.png, fan-geometry.json),
leaving its controls inaccessible. It can be closed via its window manager action.
Patch 68 applies a layout-derived minimum only for QIDI, matching the material
editor correction. Print Options remains usable. On this binary, a chooser opened
for fixture.gcode rejects its selection after replacement.gcode arrives (no
EXCLUDE_OBJECT request); a fresh chooser sends EXCLUDE_OBJECT NAME=fixture_cube.
These exploratory checks must be repeated on the final matching binary.

A subsequent malformed-telemetry sweep covered invalid JSON, wrong Box type,
null product metadata, extreme chamber numbers and partial slot metadata. Each
was followed by a recorded loopback lamp request and a live GUI process
(fault-results.json). The second session exited 0. These remain partial checks
on a rejected binary, not the complete fault/lifecycle gate.
