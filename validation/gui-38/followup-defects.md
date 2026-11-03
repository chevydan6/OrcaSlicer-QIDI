# Defects found by actual GUI validation

## Stale object chooser

On the compiled 38-patch application, open Print Options / Skip objects while
fixture.gcode is running, select fixture_cube, change the fixture filename to
different-job.gcode, then confirm after one second. The recording server receives
EXCLUDE_OBJECT NAME=fixture_cube. The GUI's incoming status callback is processed
just after the native dialog returns, so its filename comparison sees old data.

Patch 47 includes the dialog's expected filename in the command and checks it
against the communication layer's latest WebSocket cache. It also requires a
running/paused job and checks that every selected object still exists. Isolated
production-body checks pass with sanitizers; compiled CTest and GUI retest remain
pending. This reduces stale-state errors but cannot make a remote command atomic
with a printer changing jobs; physical verification remains separate.

## Empty material dropdown

On the same application, open the material editor for B2. The dropdown is empty
because it resolves the QIDI model through the Bambu-specific resource catalog.
Patch 48 uses the vendor-profile display name for QIDI in both dropdown creation
and selection lookup. It keeps the shared compatibility rules, allows local user
profiles, labels the dialog for QIDI and omits unsupported Bambu PA/reset actions.
The full build and actual editor retest remain pending.
