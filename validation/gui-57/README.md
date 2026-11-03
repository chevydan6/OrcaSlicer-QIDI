# Candidate 57: fresh-setup failure

Build input 0b5a0e57608e4bf261dc5efe6c647a79c7911496, run 41600542116.
AppImage SHA256 7d806251b2bb3e4094db1b78a7ff971b4df052165a3f6acc530794ab412ceb28.
Artifact 13214835461 ZIP SHA256 5f08628ebf4b6b7b91d0e11de1a011f10d7a3d82b694de9d7fdcb7927e756e25
matches GitHub. Packaged manifest checked against all 57 patch hashes and both pins.

Ubuntu 24.04.5, private Xvfb :2, Openbox, GDK_BACKEND=x11,
WAYLAND_DISPLAY removed, fresh research/gui-57/settings datadir.
Wizard: Asia-Pacific, Qidi X-Max 4, material selection, stealth mode,
no proprietary network plugin. Dismissed upstream update notice via Skip this Version.
Prepare remained blank after selecting its tab. Maximizing the window immediately
restored printer/material/process controls and the 3D bed. Screenshots record both.
This disproves patch 44's sufficiency on this host; candidate is not accepted.

Patch 58 forwards the frame size event to the notebook, whose DoSize sizes its
current page. This is an attempted correction requiring fresh compiled validation.
No printer was configured in this GUI and no physical command was sent.

## Fresh connection and material editor

After normal exit (status 0), enabled the printer-agent preference in isolated
settings and restarted. Native address dialog connected to http://127.0.0.1:19025
with blank optional API key/CA. Both Boxes and external telemetry rendered.
The material editor for A2 had an empty dropdown. Saved local_machines contained
printer_type `Qidi X-Max 4`. get_printer_type_display_str only matched vendor
model_id `Qidi-XMax-4`, so the profile lookup received Unknown. Patch 59 adds
QIDI-only model.name matching. The native RGB dialog was entirely on-screen.

A diagnostic settings substitution to the historical model ID was inconclusive:
the editor appeared at 2x5 pixels and could not be resized via the window manager.
That substitution is not the user-facing path and has been reverted; retain this
finding for lifecycle testing rather than calling it a successful workaround.
No real printer address was added to these settings.
