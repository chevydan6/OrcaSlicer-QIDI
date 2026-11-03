# Installed 42-patch candidate

AppImage SHA256: 390077ccd362606fab08e51aacc66f0a7d4c056c1520d0f88bfb773a9a68893f.
Installed per-user as io.github.chevydan6.OrcaSlicerQIDI with GNOME 50 and
the private-session-bus option. Existing com.orcaslicer.OrcaSlicer and
com.bambulab.BambuStudio registrations remain present.

The actual installed launcher opens on private Xvfb :99. Fresh setup lists MAX4
and 397 compatible materials. Configuration is created under the separate
~/.var/app/io.github.chevydan6.OrcaSlicerQIDI/config/OrcaSlicer-QIDI directory.
The installed launcher opens a functioning GTK portal file chooser.

Opening the original support-first QIDI project retains three materials, object
assignment and support settings. Slicing with its embedded machine G-code fails
with an unknown chamber_temperatures placeholder, shown in the screenshot. The
GUI presents an error without crashing. Earlier CLI comparison cases replaced
the machine with the Orca MAX4 profile and did not cover embedded QIDI macros.
Patch 50 adds the compatibility alias; two new CLI cases retain embedded G-code.
Final-build slicing and GUI retesting remain pending. No printer was contacted.
