# Candidate 64 GUI: fresh layout failed

Exact AppImage SHA-256: `7361aa78213b45cd087d93128d5481b467329fc22cfa4b5443b6248c7ffca435`.
Integration build input: `9b06cba3424e19e53a4235ce8b3bf9d455ea393a`.
GitHub archive digest, pins and all 64 manifest patch hashes verified; see
../recovery-2026-11-03/artifact-64.json.

Fresh isolated setup on Ubuntu 24.04.5/Xvfb :2 remains blank on Prepare after
idle (11/12). **Patch 63 is disproved.** No debugger intervention preceded these
failure screenshots. No real printer connection was configured.

## Diagnostic session, not acceptance

After recording failure, GDB attached to this process. Both DoShowPage and its
queued callback execute. The callback receives the correct Prepare native handle
and book handle. Queued GTK resize/allocation does not repair this session,
including a repeat from the debugger. Thus the earlier GUI59 intervention was
insufficient evidence for the general correction.

wx reports page rectangle (0,39,1200,727), while GTK's visible page remains 1x1.
Calling gtk_widget_size_allocate with that existing rectangle restores the UI
(18-diagnostic-direct-allocation.png). The pinned wx GTK DoMoveWindow implementation
also performs direct allocation in its native size-event path. Patch 66 applies
this only when a shown current page has mismatching native dimensions, with a
required preferred-size request first. Fresh binary verification remains required.

The diagnostic session exited normally with status 0. This does not establish a
full clean-exit or lifecycle gate. No final acceptance or installation follows.
