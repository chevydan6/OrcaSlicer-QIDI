# Using the custom Linux build

Launch **OrcaSlicer QIDI (Custom)** from the application menu, or run
`~/.local/bin/orca-slicer-qidi`. The custom application keeps its own settings.
Your existing OrcaSlicer and Bambu Studio installations remain separate.
The accepted native installation uses X11/XWayland (--extract --x11); native
Wayland is not accepted. MAX4 0.4, QIDI materials and printer agents are already
configured on the recovered computer. No test or real printer connection is saved.

Select the Qidi vendor and the MAX4 nozzle size in the setup wizard. Existing
Orca machine/process tuning is retained; the port adds missing QIDI materials
and QIDI Box settings. Imported QIDI projects can carry their own machine G-code
and material settings. Review any compatibility notice when opening one.

## Native QIDI controls

In **Preferences → Developer**, enable **Use printer agents instead of print
hosts**. This selects the native QIDI agent and its job-mapping path. The legacy
print-host path does not provide the port's full Box workflow.

With a QIDI printer profile selected, **Device → printer selector → Connect by
address** accepts a Moonraker endpoint such as `http://printer-address:7125`.
Use the actual address and port from your printer/network. An API key is optional
unless the server requires one. The dialog accepts a CA file for HTTP requests,
but the inherited secure WebSocket path disables certificate verification.
HTTPS/WSS is not accepted as a verified secure transport for this milestone;
current acceptance targets a trusted local HTTP connection. Connecting is not
necessary for offline slicing. No actual printer address was configured by the
software validation work.

The Device panel adapts to reported Box slots and capabilities. It exposes the
supported load/unload/eject/RFID, material/color, chamber, fan, light, camera and
print-option operations. Those controls send real commands when connected to a
real printer. Box Settings changes the printer's insertion/startup RFID flags.
Unsupported Bambu-specific calibration/reset/refill operations are hidden.

## Filament mapping

Assign each object/support to its intended logical filament before slicing. In
the single-printer submission dialog, map every used filament to its physical
Box slot. Box B slot 2 is physical slot 5 internally; slicer filament 3 remains
logical tool 2. The port sends the mapping and Box mode before the print start.
See [filament-mapping.md](filament-mapping.md) for sparse and support-first cases.

Choose external-spool mode for a single-material external spool job. Mixed
external/Box jobs and incomplete or invalid mappings are rejected. Experimental
multi-device QIDI submission is disabled. The software trace is validated. One physical sparse T2→A1 print completed on
Dan's MAX4; other mappings and support-first behavior still need hardware testing.
The current Device layer/time readouts are inaccurate; use printer state/history
for progress and completion until the documented monitoring fixes are accepted.

## Updates and recovery

Keep automatic preset bundle updates disabled. Official Orca updates do not
include these patches. Use the pinned integration repository and its workflow to
produce updates, retaining the previous AppImage and custom settings backup.

The native installation stores settings in `~/.config/OrcaSlicer-QIDI` (or
`$XDG_CONFIG_HOME/OrcaSlicer-QIDI` when configured). The optional historical
Flatpak mode stores them in
`~/.var/app/io.github.chevydan6.OrcaSlicerQIDI/config/OrcaSlicer-QIDI`.
The checksum-based installation directories are under
`~/.local/opt/orca-slicer-qidi`. Reinstall a retained custom AppImage with the same
installer options to roll back. Do not substitute another slicer's settings directory.

See [build.md](build.md) for installation/reproduction and
[limitations.md](limitations.md) for unsupported features and hardware validation.
