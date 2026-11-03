# Candidate 59 GUI acceptance: failed

Build input `cd6d820543ddaabad4846b6eb053b4508e65c448`, 59 patches.
AppImage SHA256 `be664d179a2209cd348fd14d2fb9e30f8f8dde60a0ad59e0d3e4d9f25cc5edc4`.
Ubuntu 24.04.5, private Xvfb :2/Openbox, GTK X11, isolated fresh settings.
Only the non-forwarding loopback fixture at 127.0.0.1:19025 was configured.
Build/static gates passed; this binary is **not accepted** and was not installed.

## Observed on the unmodified packaged binary

- Fresh setup still left Prepare blank (`05-fresh-prepare.png`). A one-pixel
  manual resize restored the interface (`06-one-pixel-reflow.png`). Patch 58
  is disproved on this host; preserve this failed evidence.
- Fresh native address connection with a blank optional API key worked. The
  material list populated without editing the saved model name, verifying the
  observed patch-59 lookup correction (`12-material-list.png`).
- Selecting QIDI PLA Rapido and native RGB #123456 dispatched the expected
  slot-1 metadata update; see material-edit-requests.json and screenshots.
- Repeated completed material sessions failed: eight subsequent alternating
  A1/A3 windows measured 2x5 client pixels. `material-reopens.json` and the
  first/eighth screenshots preserve the failure. A fresh dialog object alone
  (patch 55) is insufficient on this GTK host.
- Normal shutdown before debugger investigation returned zero. Full project
  discard/shutdown, controls, mapping and fault matrix remain untested here.
- A clean restart could remain Connecting until a fresh address connection.
  Discovery replaces the stored endpoint with host-only 127.0.0.1, losing
  port 19025. Abrupt debugger exits did not consistently reproduce this because
  they did not save the overwritten endpoint; they are not persistence passes.

## Diagnostic interventions, not candidate acceptance

GDB traced the 2x5 resize to wxTopLevelWindowGTK::GTKUpdateDecorSize, following
native decoration notification. A debugger-injected minimum (374x259 outer)
kept two repeated Box opens usable (`min2-reopen.png`). A later automated loop
missed the external edit target and closed the app; it is not an eight-cycle pass.
An earlier injection stopped at a nested breakpoint and terminated the debug
inferior; that debugger failure is not an application crash.

For fresh layout, the native GTK tree showed the visible Prepare page and its
children allocated at 1x1 while the book was 1200x766. Reallocating only the
main frame did not help. Queuing resize of the page and allocation of the book
restored the UI (`diagnostic-native-page-allocation.png`). This supports patch
62, but the new compiled binary must repeat fresh setup without intervention.

Proposed follow-ups: patch 60 uses a layout-derived dialog minimum; patch 61
preserves the QIDI endpoint in discovery with an HTTP/HTTPS port regression;
patch 62 allocates newly shown GTK pages and removes patch 58's ineffective
synthetic book resize. All require new matching build and GUI evidence.

No physical printer behavior was tested in these GUI sessions.
