# Candidate 69 GUI acceptance: rejected for disabled timelapse selection

Build input `f8192f7761bb55275e049e854544393eccbb4485`, AppImage SHA-256
`2bed31d5e66ad36a1cdd56ea0bbe4a500960ce112c23dc778f59f48e72bd5757`. Matching ZIP digest, source pins and all 69 patch
hashes verified. Ubuntu 24.04.5, private Xvfb :2/Openbox, fresh isolated settings.
No debugger intervention. Every control/upload targets 127.0.0.1:19025; the
fixture records and discards requests and cannot forward them.

Cases.json records only observed checks on this exact binary. Untested cases
remain open; this candidate is rejected and was not installed.
The previous candidate 68 failure remains preserved in ../gui-68.

Expanded pre-print option testing found Timelapse On disabled despite the MAX4
profile enabling it and the connection having available storage (123–126).
The generic capability check reads a Bambu firmware flag that QIDI never sets.
Patch 70 uses QIDI profile capability and preserves the Moonraker storage gate.
All CI gates passed; this GUI failure still requires a matching new build and
complete rerun. Earlier passes do not accept candidate 70.
