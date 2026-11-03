# Candidate70 installation: X11 backend accepted

The actual installed AppImage, launcher and desktop entry were verified. See
`result.json` for identity, options, settings isolation and rollback locations.
The launcher selects `GDK_BACKEND=x11`; on GNOME Wayland this uses XWayland.
Private Xvfb :3 checks cover launcher/menu launch, persisted MAX4/material/agent
settings, disabled automatic preset updates, native export chooser, slicing,
preview and exit0. No fixture connection or test recent project is delivered.
The real GNOME desktop additionally opened the installed launcher, rendered the
MAX4 profile/3D bed and exited0. Crops exclude unrelated desktop content.
Full fault/control acceptance remains the exact-binary X11 gate in ../gui-70.

Native Wayland is not accepted. In isolated Weston13/llvmpipe, setup and file
selection worked but main-window clicks did not reliably switch tabs, maximize
or slice. The failed attempt is retained. Its exit1 came from the harness's
Alt+F4 closing the outer compositor; the broken display pipe is not an app crash.
The explicit native installer --x11 option avoids that unaccepted backend and
changes no application code or upstream pins. No Fedora Flatpak/private-bus
workaround was carried over. No Flatpak package was built for this host.

This was the first custom installation on this computer. Settings were backed
up before changing the launcher backend and after acceptance. Candidate69 is
retained as a rejected comparison binary; there is no earlier accepted local
installation. The accepted70 checksum directory is the future rollback baseline.
