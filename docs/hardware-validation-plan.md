# Proposed MAX4 comparison session

This is a reviewable plan, not authorization to operate the printer. Complete
software acceptance first. Dan must explicitly authorize the grouped active
operations below and supervise the session. Do not flash firmware or change
persistent printer configuration without separate authorization.

## Existing read-only evidence

The authorized LAN inspection reported one box_v1, main MCU 02.01.01.12 and Box
MCU 02.03.01.21. A2 (physical slot 1) reported blue Generic ABS present; the other
slots reported absent. The loaded path was slot16 (external). Camera GET returned
a valid 1920x1080 JPEG. These are reported values, not confirmation of the physical
spools, overall release version or temperature limits. Sanitized evidence is in
`validation/recovery-2026-11-03/printer-readonly.json`.

Before an active session, Dan should confirm the overall MAX4/Box firmware
versions, actual Box count, nozzle and build plate, every loaded material/slot,
and the material manufacturers' nozzle, bed, chamber and Box limits. Confirm
the printer is idle and the plate is clear. Authentication is currently not
required for the read-only endpoints; never commit any later credentials.

## First supervised session

1. Refresh read-only telemetry and camera. Record firmware, slot arrangement,
   current/target temperatures and whether another client is controlling a job.
2. Prepare a small single-material cube with only slicer filament 3 used. With
   the currently reported one-Box arrangement, map logical T2 to confirmed A2
   (physical slot 1). B2/slot5 requires a second Box and cannot be physically
   verified with this arrangement. Review the sliced start/change macros and
   selected temperatures before agreeing to any heat or motion.
3. With Dan's explicit permission for heating, homing/motion, filament feeding
   and the small print, run the QIDI Studio reference job first. Record which
   slot feeds, preparation tool, first-deposition tool and expected/observed
   temperatures. Stop if the selected path or material is wrong.
4. After that job is finished/cancelled and the printer is idle, close its control
   session. Run the accepted custom Orca job with the same model, material and
   relevant settings. Record differences in G-code, request order and behavior.
   Never submit both jobs together or maintain competing control sessions.
5. Confirm completion/stop, unload or cool only as explicitly agreed, and record
   final state. Success of this one test does not verify refill or multicolor.

## Follow-up sessions with the necessary materials

- Support-first: two confirmed compatible materials/slots and a small raft case.
  Preserve preparation tool2 and first deposition tool0; map both explicitly.
- Reversed and multiple-Box mappings: record all connected Boxes and loaded slots
  first. Use a small sequential comparison with the same mapping in both apps.
- Box temperature: compare the configured logical VT indices, reported targets
  and actual behavior during a print, within the confirmed material limits.
- Material/RFID and recovery: agree separately to any metadata writes or RFID
  reads. Start with an idle-printer reconnect test; do not deliberately interrupt
  a physical print or its network without explicit agreement.
- Automatic refill: remains unsupported. First compare QIDI Studio's public
  implementation and authorized sanitized traces to establish its configuration,
  submission/runtime commands and matching-spool prerequisites. The observed
  auto_reload_detect=1 and empty auto_refill array do not prove it is enabled.
  Do not guess commands, reuse Bambu operations or provoke runout until the
  protocol and supervised test conditions are agreed.

## Evidence

For every comparison, record the exact slicer/artifact hash, model/settings,
firmware, physical slot/material map, expected versus observed behavior, and
sanitized request/response times. Remove authentication, serial identifiers,
unrelated filenames and personal camera images before publishing. Keep software
simulation results, read-only hardware observations and active physical tests
separate in the handoff.
