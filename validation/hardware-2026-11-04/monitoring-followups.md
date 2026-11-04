# Monitoring issues observed on candidate70

During the authorized T2-to-A1 test, the Device panel displayed Layer0/0 while
Moonraker print_stats.info.total_layer reported20. This shared Moonraker adapter
currently does not forward current_layer/total_layer into the device payload.

The remaining-time display is not a reliable estimate: the adapter computes
(total_duration - print_duration)/60. Both are elapsed durations in the observed
firmware response, so their difference is startup/non-print time, not the time
remaining to finish. Preserve this failed physical UI evidence; the fixture GUI
pass established rendering and request behavior, not real-printer estimate accuracy.

Follow-up should use the appropriate firmware metadata/progress estimate and
forward validated layer counters, with non-QIDI Moonraker regression coverage.
No product source was changed during the physical test. Any fix requires a new
matching build and affected/full acceptance as appropriate; candidate70 evidence
must not be silently transferred to the new binary.
