# Candidate 62 GUI: failed acceptance

Exact AppImage SHA-256: `62f4071879834c2381d605bedcea3eb55f2d2a810c8b906c8a82b81508aa35e2`.
Build input: `b8ef9f8e4f3e27fda362401da9076d453e3cf06b`; pins and all 62 patch hashes match the packaged manifest. See ../recovery-2026-11-03/artifact-62.json and ci-62.json.

Ubuntu 24.04.5, private Xvfb :2/Openbox, native extracted AppImage, isolated fresh settings. All GUI connections were loopback-only. No debugger intervention was used in this session.

Fresh setup still leaves Prepare blank after idle (15/16). **Patch 62 is disproved as a complete correction.** Manual maximization restored the page; all subsequent checks are exploratory, not final acceptance.

Ten Box and ten external material-dialog openings remain usable (material-reopens.json and first/last screenshots), supporting patch 60. Rapid duplicate opening produced one usable editor. Native blank-key connection succeeds. Normal exit status 0 and restart reconnect automatically to the saved scheme/host/port, supporting patch 61.

The first material editor displays Generic PLA for fixture metadata QIDI / PLA Rapido (32-first-material.png). The preset alias is QIDI PLA Rapido; the resolver compared only the product substring. Patch 64 addresses this new mismatch; compiled verification remains required.

A disconnect while the editor was open plus HTTP 503 left the GUI responsive and shutdown returned zero. Confirm still attempted an HTTP request, rejected by the fixture. This is limited lifecycle evidence, not proof that telemetry loss prevents dispatch.

Sanitized real MAX4 telemetry replayed through the fixture renders one Box, A2 blue ABS and three empty slots (44). A fresh-cache replay remains pending because prior two-Box fixture data can persist in the merged cache. No real control requests occurred.

`cases.json` retains untested cases. Passing partial checks from this rejected binary do not accept a future binary. Next candidate must rerun the complete matrix, including fresh setup and metadata selection.
