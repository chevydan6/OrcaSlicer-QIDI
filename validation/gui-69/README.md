# Candidate 69 GUI: rejected for disabled timelapse selection

Build input `f8192f7761bb55275e049e854544393eccbb4485`, AppImage SHA-256
`2bed31d5e66ad36a1cdd56ea0bbe4a500960ce112c23dc778f59f48e72bd5757`.
All CI gates passed: 2,916 unit cases without failures/skips, seven CLI regressions,
72 vendor bundles, all 21 MAX4 cases and static checks. GitHub ZIP/report digests,
all packaged patch hashes and pinned source revisions match.

Fresh isolated settings on Ubuntu 24.04.5, private Xvfb :2/Openbox. No debugger
intervention. Every GUI request targets the non-forwarding 127.0.0.1:19025 fixture.
No physical printer commands. Cases.json records **61 passed and one failed**.

Fresh layout, Bambu A1/MAX4 slicing, twenty material reopens, duplicate-open
refusal, correct slot state, material/color editing, zero/four Boxes, removed-slot
rejection, physical controls, detection/RFID options, stale/fresh exclusion,
malformed telemetry, HTTP/WS/camera recovery and delayed callbacks passed.
Original sparse and support-first imports, exact logical/physical mappings,
Box-temperature save/reload, unsupported mixed/external and batch refusal passed.
The patch69 external-job explanation remains visible with Send disabled.
A request was recorded before shutdown with 15s injected latency; application
exit0 occurred before that response, less than one second after preset discard.
Restart restores the endpoint and reconnects. Both application sessions exit0.
Sanitized real MAX4 telemetry replay and resize/tab recovery also passed.

**Failure:** Timelapse On remains disabled despite the MAX4 profile enabling it
and available printer storage (123–126). The generic capability check reads a
Bambu firmware flag that the QIDI connection never populates. Timelapse Off,
bed-level On/Off (G31/G32) and polar-cooler On/Off requests are recorded correctly.
Patch70 selects QIDI capability from the profile and retains the storage and
sliced-job warning gates. Matching On/Off and storage-failure GUI tests plus a
complete new-candidate rerun are required. This binary was not installed.

The synthetic derived multicolor input changes only filament_is_support in the
reference support-first project; hashes and purpose are in multicolor-input.json.
Request traces, screenshots, application exit codes and focused proof records
belong only to this exact candidate. No historical pass accepts a later binary.
