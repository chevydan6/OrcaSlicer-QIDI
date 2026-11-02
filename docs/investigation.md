# Initial investigation

## Environment

Host: Fedora 44 x86_64, approximately 3.7 GiB RAM and 17 GiB available disk at start.
Git, GitHub CLI, CMake, Ninja and GCC are present. Several GUI/build development
packages are missing; noninteractive sudo is unavailable. Assess a GitHub Actions
Linux build before requiring privileged host package installation.

## Sources

- https://github.com/OrcaSlicer/OrcaSlicer — main; clone in progress.
- https://github.com/QIDITECH/QIDIStudio — main, observed HEAD
  `403b619d56147160bb883e94f95a7951245bc6d0`; clone in progress.

## Findings requiring further verification

QIDI's MAX4 is named `X-Max 4` in its profiles, under `resources/profiles/X 4 Series`.
The 0.4 mm profile has explicit Box support, chamber control, MQTT/3MF capability,
multi-box, polar cooler and timelapse flags. Its start G-code invokes
`BOX_PRINT_START EXTRUDER=[initial_no_support_extruder]` and later `T[initial_tool]`.
These placeholders must be traced through the slicing engine before conversion.

`src/slic3r/GUI/Jobs/PrintJob.cpp` passes `ams_mapping`, `ams_mapping2`,
`ams_mapping_info`, nozzle mapping and `enable_multi_box` into QIDI print parameters.
Thus the physical slot may depend on submission metadata as well as G-code.
No root cause or fix for the user's starting-filament bug is established yet.

`src/slic3r/Utils/NetworkAgent.cpp` dynamically loads `libqidi_networking.so` on
Linux and resolves `qidi_network_*` functions. Its implementation, distribution
terms, ABI availability and alternatives need investigation before shipping a
network-enabled port. Preserve Orca's existing network backends.

## Validation status

Only source inspection and build-environment inspection have occurred. No
compilation, profile loading, persistence, slicing, protocol mock, or physical
printer tests have passed yet. No printer has been contacted.
