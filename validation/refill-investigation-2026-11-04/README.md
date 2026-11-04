# Refill investigation and proposed ABS comparison

This records the earlier offline investigation. The subsequently authorized QIDI Studio
reference job is now running; see [reference session](../refill-reference-2026-11-04/README.md).
No explicit refill-enable or manual reload command has been sent. Dan loaded physical A2 orange ABS
and A3 blue ABS, deliberately setting both software colors to blue. The agent
preserved that metadata. Read-only telemetry now reports both slots present,
auto_reload_detect=1 and auto_refill=[{type:ABS,color:#2850FF,slot:[1B,1C]}].
This is a firmware-reported refill group; it does not prove successful runout.
A1's yellow PLA is excluded from the planned comparison.

The read-only /printer/gcode/help response advertises SET_ENABLE_AUTO_RELOAD and
AUTO_RELOAD_FILAMENT. No such command was executed. The pinned QIDI Studio
[local dispatcher](https://github.com/QIDITECH/QIDIStudio/blob/403b619d56147160bb883e94f95a7951245bc6d0/src/slic3r/GUI/PrinterTaskDispatcher.cpp#L112)
uses the different spelling SET_ENABLE_AUTO RELOAD for its settings event. The
[UI handler](https://github.com/QIDITECH/QIDIStudio/blob/403b619d56147160bb883e94f95a7951245bc6d0/src/slic3r/GUI/AMSSetting.cpp#L625)
posts EVTSET_AUTO_FILAMENT and returns before its inherited Bambu command path.
Thus copying the latter would not establish QIDI behavior. The currently enabled
firmware/group allows observation without changing that setting. The exact effect,
arguments and persistence of the advertised commands still need protocol evidence.

An official Ubuntu24 QIDI Studio2.07.02.73 AppImage was downloaded and its SHA256
matched GitHub's asset digest (reference-identity.json). This is a runtime reference,
not a change to either integration source pin. Accepted Orca candidate70 is retained.
The archived drafts below were offline preparation. The later reference session
uses an independently reviewed GUI export.

## Concrete draft session

1. Confirm both ABS products tolerate the proposed250C printing,260C preparation,
   100C bed; chamber and Box targets0. Keep the plate clear and operator nearby.
2. Print the30×30×8mm solid block from A2, mapping logical T0 to physical1 ([1]).
   A3 is the firmware's refill partner, not a scheduled slicer tool change.
   Both drafts use0.20mm layers,100% aligned-rectilinear infill and a3mm brim.
   Model consumption is approximately2.9m/7.3g; stock startup adds purge waste.
3. Use a measured short donor that survives startup, or agree that Dan will cut
   only the accessible A2 feed upstream of the Box after stable deposition is
   observed. Do not pull filament, spoof sensors or invoke manual reload commands.
   The remaining path length must be less than the job's remaining consumption.
4. Observe natural runout, firmware event/slot transitions, orange-to-blue material,
   continuation and completion. A manual Resume, Load or forced tool change does
   not count as automatic refill. If it pauses/faults, preserve state and stop the
   experiment rather than mask the failure with a manual intervention.
5. Run QIDI Studio first, then custom Orca sequentially with the same physical
   arrangement and relevant settings, resetting/reloading the donor between jobs.
   One controlling slicer at a time. Record submission/runtime traces and any
   engine/startup differences. The QIDI reference profile removes its two forced
   MZV commands so both jobs preserve existing input-shaper tuning. The official
   QIDI executable is unchanged. Orca starts fan-off commands earlier (see
   startup-differences.diff). Verify normal shutdown and heater targets0.

The approximately18-minute Orca estimate is not a guaranteed physical duration.
The earlier PLA startup exceeded its estimate. The QIDI Studio draft retains its own engine and the normalized startup described
above; generated toolpaths still differ between engines. Dan subsequently instructed autonomous execution of this ABS test and reported
that he had already cut A2. The active session uses that existing cut; remaining
length is unknown, so a startup runout must be distinguished from deposition runout.

## Offline preparation evidence and limits

Both final drafts sliced successfully; hashes and emitted temperature commands
are in draft-reviews.json. No physical refill result exists yet. Initial QIDI CLI
preparation rejected --datadir (unsupported) and rectilinear (converted to cubic,
invalid at100%). Isolated XDG directories, resolved machine profiles and the shared
alignedrectilinear pattern corrected those preparation errors. QIDI's plural
chamber_temperatures key initially retained55C; final review caught it and set0
before any upload. Neither rejected nor unintended-temperature draft was submitted.

Orca's QIDI refill controls remain unimplemented. Existing firmware settings may
provide refill without a slicer-side runtime command; that is a hypothesis to test,
not a verified capability of candidate70. Refill UI/command changes, if needed,
require a new matching software build and acceptance before physical validation.
