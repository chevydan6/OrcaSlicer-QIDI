# Candidate 70 GUI acceptance: in progress

Build input `7352b62f30804ecbeaa96c7996ff86614fadf7a8`, AppImage SHA-256
`7614dd15d467d0bf08b9e8846111e29940da4c53248a1d238a35d53b1dff35a7`. Matching ZIP digest, source pins and all 70 patch
hashes verified. Ubuntu 24.04.5, private Xvfb :2/Openbox, fresh isolated settings.
No debugger intervention. Every control/upload targets 127.0.0.1:19025; the
fixture records and discards requests and cannot forward them.

Cases.json records only observed checks on this exact binary. Untested cases
remain open; this record does not accept or install the candidate.
Previous failures remain preserved in ../gui-68 and ../gui-69.

Current core assertions pass: sparse T2→slot5, external single-tool mode,
support-first preparation T2/deposition T0 then T2 with reversed Box mappings,
submission ordering, Box temperature persistence, stale guards, twenty editor
reopens, five malformed telemetry cases and delayed editor callbacks.
Timelapse On and Off both reached the fixture. Delayed application shutdown
exited zero before the pending response completed. Restart/storage/final exit
and installation checks remain in progress.

Harness-only interruptions are retained separately: an absent capture directory
caused a fixture upload error; an unmoved dialog required coordinate alignment.
Neither is a product fix or an accepted result for the ineffective actions.

