# Feature and dependency inventory

This port keeps Orca's build recipes and native interfaces. It introduces no new
linked runtime library. QIDI source paths below refer to the revision in
`sources.json`; corresponding implementation files are identified by the numbered
patches and feature checklist.

| Area | QIDI Studio source | Orca integration / dependency |
| --- | --- | --- |
| MAX4 machine/material/process profiles | `resources/profiles/Qidi` | Existing preset inheritance, OrcaFilamentLibrary IDs and profile validator |
| Persistent Box settings and thermal G-code | `libslic3r/PrintConfig`, `Preset`, `GCode` | Orca static/dynamic config, serialization, invalidation and logical-tool ordering |
| Print options and physical slot assignment | `GUI/SelectMachine`, `GUI/Jobs/PrintJob` | Existing Orca print dialog/job; immutable used-tool/options snapshot |
| LAN commands | `GUI/PrinterTaskDispatcher`, QIDI print-host code | `Utils/QidiPrinterAgent` over existing `MoonrakerPrinterAgent` and `Http` |
| Box/RFID/chamber/fan/accessory status | `GUI/QDSDeviceManager`, `GUI/QDSPrinterWebView` | Existing Moonraker status stream; QIDI adapters into native DeviceCore models |
| Filament controls and material editing | QIDI native `Widgets/AMSControl` and webview wiring | Existing Orca AMS widgets, device commands and exact compatible preset resolution |
| Camera | QIDI printer webview snapshot URL | Existing Orca HTTP snapshot viewer; native web/media dependencies retained |
| Object exclusion | `PrinterTaskDispatcher` EXCLUDE_OBJECT operation | Native named-object chooser using reported Klipper names |
| Account/cloud networking | Dynamically loaded `libqidi_networking.so` and QIDI network headers | Not included; current Orca backends remain intact; LAN implementation is independent |

## Existing library dependencies inspected

| Dependency | Source evidence and port decision |
| --- | --- |
| Boost | Both recipes select 1.84.0 with the same archive checksum. Reuse Orca Asio/Beast for transport and loopback tests. |
| nlohmann JSON | Both checked-in headers report 3.10.4. Adapter code and isolated checks use Orca's header; recursive cache merging avoids newer-library-only APIs. |
| wxWidgets | QIDI's recipe follows `bambulab/wxWidgets` master; Orca pins `OrcaSlicer/Orca-deps-wxWidgets` at `b44c39c100975a0ac0e46f937aa3f3eae5e18631`. Retain Orca's fork and port behavior into its current widgets. |
| libcurl | Both recipes select curl 7.75.0 with the same archive checksum. Reuse Orca's Http wrapper, API-key handling and timeouts. |
| TLS | Retain Orca's existing OpenSSL/system dependency selection; do not substitute QIDI binaries or libraries. The final CMake log records the selected implementation. |
| WebSocketPP | QIDI has a 0.8.2 recipe. No additional copy is needed for this port's existing Orca Moonraker transport. |
| GTK/WebKit/OpenGL | Keep official Orca Linux dependencies. The Fedora host uses its installed GNOME 50 runtime for extracted AppDirs; rendering still requires runtime validation. |
| Geometry/engine/Python dependencies | Keep current Orca recipes, algorithms and plugin runtime. QIDI functionality is adapted without replacing the engine or downgrading these dependencies. |

Build tooling is CMake/Ninja, Clang with lld, ccache and Xvfb in the Ubuntu 24.04
workflow. `-j 2` limits compile parallelism; dependency-level `-J` stays at its
default of one. Catch2 and the existing engine/utility targets supply full-library
tests. Python scripts perform profile inventory, patch reproduction, offline CLI
slicing and installation. Pillow/python-xlib are local GUI-validation tools only;
they are not application dependencies.

Recipes and source pins are reproducible inputs; runner images and package
repositories are not bit-for-bit frozen. Preserve upstream third-party license
notices with the package and corresponding source, as described in maintenance.md.
