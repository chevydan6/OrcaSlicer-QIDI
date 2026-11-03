# First-run layout regression

The pinned unmodified upstream AppImage and the 32-patch custom AppImage both
show a blank Prepare page after the setup wizard in the registered GNOME 50
runtime on Fedora 44/X11. Menus and Preferences respond. Resizing/maximizing
the same process restores the sidebar, MAX4 bed and controls.

Reproduction: fresh isolated datadir, choose MAX4/all materials, enable stealth,
skip proprietary plugins, finish, then select Prepare without resizing.
The screenshots show the unmodified upstream build before/after resize.
Neither run contacted a printer; networking was disabled in the sandbox.

Patch 44 queues the normal main-window size event after successful wizard
completion. Its compiled first-run verification remains pending.
