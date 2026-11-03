# Candidate 68 GUI: rejected for misleading unsupported-job state

Build input `8c258d62e15fded96b400782d7e6c5d150b92a07`, AppImage SHA-256
`55726a0482acbb2a1661b4dbaaa46e16e39c735bf126598a36266eb9af01ab78`.
All CI gates pass: 2,916 unit cases without failures/skips, 7 CLI regressions,
72 vendor bundles, 21 MAX4 cases and static checks. Archive/manifest/report
verification is under ../recovery-2026-11-03/{artifact-68,ci-68}.json.

Ubuntu 24.04.5, private Xvfb :2/Openbox, fresh isolated settings, loopback-only
fixture. No debugger intervention or real hardware commands. Cases.json records
partial passes and untested cases; this candidate is not accepted or installed.

Fresh layout, Bambu A1 and MAX4 slicing/preview, 20 repeated material dialogs,
slot colors, native color/material editing, zero/four Boxes, removed-Box guard,
fan/chamber/lamp/speed/RFID/detection controls, stale/fresh exclusion, telemetry
faults, HTTP/WS/camera recovery and delayed editor callbacks passed observed
checks. Original sparse and support-first projects import and submit with correct
logical/physical mappings. GUI save/reload preserves Box temperatures.

**Failed UI behavior:** a derived two-tool PLA job maps both tools to Ext (110).
The QIDI preflight blocks upload, but periodic generic status refresh clears the
explanation and enables Send again (111/112). Repeated clicks appear to do
nothing. No POST/upload/start escaped the refusal (multicolor-result.json).
The input derives from the original support-first project by clearing only
filament_is_support; multicolor-input.json records hashes and purpose.

Patch 69 adds the QIDI-only external restriction to periodic preflight so Send
stays disabled with an explanatory message. Protocol validation remains in place.
A matching new build and complete GUI rerun are required; partial passes here do
not accept the next candidate. Follow-up checks 118–131 verify endpoint restart, batch refusal, sanitized real
telemetry replay, resize/tab recovery and normal imported-project discard/exit.
Delayed shutdown remains inconclusive: this fixture version logged requests
only after the injected delay, so an in-flight arrival was not established.
The candidate remains rejected for the unsupported-job status defect.
