# Compiled GUI checks through patch 38

The verified AppImage from integration commit 93f7fca runs in a registered GNOME
50 Flatpak runtime with an isolated datadir. Requests go only to the recording
fixture at 127.0.0.1:19025. The fixture never executes or forwards commands.
The GUI was subsequently moved to Xvfb :99 to avoid interfering with the desktop.

Observed cases:

- Restart retained the fixture profile and printer-agent preference.
- Box B slot 2 eject sends SLOT=5. RFID insertion preference sends the QIDI flags.
- Four Boxes render; selecting D4 and Load sends SLOT=15.
- Replacing status with zero Boxes removes the Box slots, retains the external
  spool, and disables unselected load/unload operations.
- Chamber target 50 sends SET_HEATER_TEMPERATURE HEATER=chamber TARGET=50.
- Sport speed while the fixture reports printing sends M220 S124.
- Parts and auxiliary fan toggles send the corresponding named fan commands.
- Malformed WebSocket JSON, null material name, extreme chamber values and a
  wrong-type Box object do not exit the application. A lamp request succeeds
  after every case; subsequent valid telemetry is accepted.
- HTTP 500 is logged as a failed send. A three-second server delay with four
  repeated lamp clicks leaves navigation usable. Dropping the WebSocket leads
  to another subscription and an active fixture client within three seconds.
- Returning to Prepare after controls displays the bed and settings.

The simulator acknowledges requests without changing its own state automatically;
observed values therefore require an explicit status update. A command appearing
here proves GUI routing, not printer acceptance or physical execution.

A private-display file-opening attempt waited inside gtk_native_dialog_run with
no file chooser displayed because the desktop portal was unavailable. The
backtrace identified the GTK file-dialog wait. The disposable test instance was
terminated, then relaunched with the project as a command-line argument. This
run is not evidence of successful file-dialog operation or clean shutdown.

The complete GUI path for a sparse logical filament selection also passes:
filament 3 produces EXTRUDER=2/T2, selecting B2 sends value_t2=slot5 before
the simulated start, and the submitted 3MF contains the identical sliced G-code.
See starting-filament-submission.json and the mapping/preview screenshots.

Further final-build GUI checks, additional submission cases, disconnected-dialog
lifetime checks and physical MAX4 verification remain open.
