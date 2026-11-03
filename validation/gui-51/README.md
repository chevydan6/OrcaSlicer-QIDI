# Embedded project and shutdown regressions through patch 51

AppImage artifact 13209569666, run 41590831679, integration f3336e3.
Verified artifact ZIP SHA256: 51ab5519ee85ee31593a0bd9bfa1daa06463cc4e7067c7fd1783386232121ee6.

The GUI opened the original QIDI support-first-project.3mf without replacing its
embedded machine or G-code. After acknowledging compatibility/custom-preset
notices, Slice completed and Preview displayed model/support filament 3/1.
Closing and choosing Discard exited normally with status 0. The earlier chamber
placeholder error and shutdown validation/watchdog failure did not recur.
These checks ran on the private Xvfb display. No printer commands were sent.
The repeated material-dialog sizing fix is in the subsequent build.
