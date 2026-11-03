# Compiled GUI checks through patch 49

AppImage artifact 13209234796 from run 41589611367, integration af04fa58.
All requests went only to the recording/discarding loopback fixture. Xvfb :99
and a private D-Bus session kept automation off the user desktop.

- Material choices are populated, including QIDI PLA Rapido; Confirm on B2 sends
  SLOT=5 with the expected vendor, product and RGB. Bambu calibration/reset is hidden.
- Opening object selection for fixture.gcode, changing the fixture to another job,
  and confirming rejects the stale selection with -19 before HTTP dispatch.
  Opening a fresh chooser sends exactly EXCLUDE_OBJECT NAME=fixture_cube.
- Turning off RFID startup preserves insertion-read enabled and sends both flags.
- Disconnect/reconnect with the material dialog open does not exit the application.
  Closing and reopening still works, but repeated opens shrink the dialog and clip
  its buttons. Patch 52 addresses this; this build does not pass that GUI case.
- The empty project closes normally with process status 0.

See results.json for the exact recorded commands and stale-job rejection.
No physical printer behavior is validated.
