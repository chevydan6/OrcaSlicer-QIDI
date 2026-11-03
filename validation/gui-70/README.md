# Candidate 70 GUI gate: passed

Build input `7352b62f30804ecbeaa96c7996ff86614fadf7a8`; AppImage SHA-256
`7614dd15d467d0bf08b9e8846111e29940da4c53248a1d238a35d53b1dff35a7`.
All **63 GUI cases passed** on this binary after its complete CI pass.
Ubuntu 24.04.5, private Xvfb :2/Openbox, fresh isolated settings; no debugger.
Every GUI request/upload targets the non-forwarding loopback fixture.
No real printer controls were used. Installation passed separately with the X11 backend; see ../install-70.

See `cases.json` for individual evidence, `core-checks.json` for measured command,
mapping, G-code, persistence and callback assertions, and `gate-result.json` for
binary/fixture identity. Both GUI processes exited0. Delayed shutdown completed
before the response arrived. Twenty material reopens retained usable layout and
selected-slot colors. Original sparse and support-first projects imported and
sliced without editing their embedded machine definitions.

Timelapse On/Off dispatch, unavailable-storage rejection and recovery all pass.
Bed leveling/polar options are captured with each job. Mixed and multicolor
external jobs and experimental QIDI batch submission are explicitly rejected.
The sanitized real-MAX4 telemetry is only replayed against the fixture.

Harness interruptions remain visible: moving preliminary test data removed the
fixture capture directory, causing an upload error; added early timelapse tests
left the Send dialog at a different position, requiring replay alignment.
Their failed/ineffective actions are preserved with harness-specific names and
are not used as positive assertions. No product changes were needed.
The preliminary wizard run was interrupted by the harness before this fresh
acceptance session; it was not an application crash or acceptance pass.
Previous product failures remain preserved in ../gui-68 and ../gui-69.
