# OrcaSlicer QIDI MAX4 / Box port

Personal downstream integration project. Integration builds pass; final GUI fixes
and Linux release acceptance are still in progress.

Start with [HANDOFF.md](HANDOFF.md) for the current candidate, build links,
known failures, validation evidence and exact next steps.

The source baseline is a pinned official OrcaSlicer main revision. QIDI Studio is the reference
for MAX4 profiles, Box workflows and communication. Local source checkouts are
excluded from this integration repository; pinned revisions and reviewable patches
make the resulting source reproducible without duplicating upstream history.

## Scope and acceptance checklist

- [x] Pin both source baselines and inventory their licenses.
- [x] Inventory printer/material/process profiles and inherited differences.
- [ ] Review remaining tuning and workflow differences.
- [ ] Port missing machine settings, chamber and Box controls.
- [ ] Port filament selection, persistent slot mapping and Box operations.
- [ ] Integrate start/end/change G-code and placeholder compatibility.
- [ ] Integrate network submission, monitoring and supporting interface changes.
- [x] Build the general integration before the dedicated bug-fixing phase.
- [ ] Compare equivalent QIDI Studio workflows and fix initial-filament selection.
- [x] Validate compilation, profile loading, persistence, slicing and generated G-code on the 42-patch build.
- [x] Validate communication with loopback HTTP/WebSocket and native GUI tests; final-build retest pending.
- [ ] Package Linux build with isolated settings and application identity.
- [ ] Document reproducible builds, attribution and remaining limitations.
- [ ] Obtain separately authorized physical-printer verification.

## Safety boundary

No firmware flashes, printer configuration writes, heater activation, hardware
movement or print starts are authorized. Software tests must not submit jobs to
real printers. Hardware verification will be reported separately from software tests.

## Progress

See the [feature checklist](docs/feature-checklist.md), [investigation notes](docs/investigation.md), [dependency inventory](docs/dependencies.md),
[build/install instructions](docs/build.md) and [upstream maintenance procedure](docs/maintenance.md). This repository is a progress
backup, not a claim that the port is complete.
