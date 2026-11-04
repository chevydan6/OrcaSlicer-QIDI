# Larger ABS refill test — preparation and failed reference

Dan requested a larger print after the 30×30×8mm reference job finished before
filament ran out at the toolhead. This version keeps the 30×30mm footprint and
increases height to32mm: four times the volume,160 layers at0.20mm,100% infill.
QIDI Studio's reviewed export uses11.445m of model filament (about28.6g), versus
2.880m in the completed smaller job. Roughly8.6m of additional model consumption
provides more opportunity for runout after the inlet empties; it cannot guarantee
runout if the donor contains more filament than the entire job consumes.

Official QIDI Studio2.07.02.73 and accepted Orca70 both sliced the larger model.
The official GUI imported, sliced, previewed and exported it. QIDI import selected
Cool Plate by default, so Textured PEI was explicitly restored before final export.
Review confirms160 layers, logical T0 only,250C print/260C preparation/100C bed,
chamber0, and heater-off commands in normal end. Planned map remains[1] (A2), with
A3 as firmware refill partner; both software colors remain blue ABS. No scheduled
tool change is used to imitate refill. Bed leveling On,timelapse/polar Off remain
the intended submission options and must be captured with the next actual job.

QIDI GUI reports41m56s, while its exported G-code estimates51m56s. The last physical
run demonstrated additional startup time; these are estimates, not a guaranteed
duration. Orca's CLI estimate is48m17s. The official reference is to run first.
QIDI startup retains the same stock MZV commands as the previous actual reference;
this does not change accepted Orca's code or upstream pins.

At preparation the camera still showed the completed block on the bed; A2 inlet
was absent while toolhead filament remained reported present. No larger print had yet been
submitted at that preparation checkpoint. Dan was asked to clear the bed when cool. Before a new start, verify the
plate clear and the feed recovered/ready; preserve the existing authorization for
this ABS test rather than asking permission again. Obtain actual uploaded-file
identity and trace for any new run; these prepared files are not physical evidence.

Reproduce with each exact slicer executable and the corresponding JSON files:

```sh
xvfb-run -a QIDI_APPIMAGE --load-settings 'qidi-machine.json;qidi-process.json' \
  --load-filaments qidi-material.json --load-filament-ids 1 --slice 0 \
  --outputdir OUTPUT --export-3mf larger.gcode.3mf refill-block-30x30x32.stl
```

Use isolated XDG_CONFIG_HOME/XDG_DATA_HOME for QIDI. For accepted Orca70 use the
orca-*.json inputs and an isolated --datadir. The qidi-gui-reviewed archive is the
subsequent actual GUI export; reimporting may reset the displayed plate again, so
verify Textured PEI and review any regenerated upload before printing.

Checksums cover the prepared jobs, source STL, profiles, reviews and GUI evidence.
Both applications retain their original engine; no product source changed.

Dan subsequently confirmed the printer ready. The official reference later failed refill acceptance and was cancelled; see [actual submission and runtime evidence](run/README.md). The prepared
archive and actual upload have distinct identities, both retained.
