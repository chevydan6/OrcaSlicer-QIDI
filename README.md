# OrcaSlicer QIDI MAX4 / Box port

Personal downstream integration project. Work in progress: no validated installable build yet.

The source baseline is current official OrcaSlicer main. QIDI Studio is the reference
for MAX4 profiles, Box workflows and communication. Local source checkouts are
excluded from this integration repository; pinned revisions and reviewable patches
will make the resulting build reproducible without duplicating upstream history.

## Scope and acceptance checklist

- [x] Pin both source baselines and inventory their licenses.
- [x] Inventory printer/material/process profiles and inherited differences.
- [ ] Review remaining tuning and workflow differences.
- [ ] Port missing machine settings, chamber and Box controls.
- [ ] Port filament selection, persistent slot mapping and Box operations.
- [ ] Integrate start/end/change G-code and placeholder compatibility.
- [ ] Integrate network submission, monitoring and supporting interface changes.
- [ ] Build the general integration before the dedicated bug-fixing phase.
- [ ] Compare equivalent QIDI Studio workflows and fix initial-filament selection.
- [ ] Validate compilation, profile loading, persistence, slicing and generated G-code.
- [ ] Validate communication using mocks and read-only checks where available.
- [ ] Package Linux build with isolated settings and application identity.
- [ ] Document reproducible builds, attribution and remaining limitations.
- [ ] Obtain separately authorized physical-printer verification.

## Safety boundary

No firmware flashes, printer configuration writes, heater activation, hardware
movement or print starts are authorized. Software tests must not submit jobs to
real printers. Hardware verification will be reported separately from software tests.

## Progress

See [investigation notes](docs/investigation.md). This repository is a progress
backup, not a claim that the port is complete.
