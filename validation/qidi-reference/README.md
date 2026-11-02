# Offline QIDI Studio reference

`results.json` records actual slices using the official Ubuntu24 release,
verified against GitHub's SHA-256 asset digest. This validates reference software
behavior only. Orca comparisons and all physical-printer checks remain separate.

The input projects contain a locally generated 10 × 10 × 4 mm cube and resolved
MAX4 0.4 mm / QIDI PLA Rapido source settings. Starting from the single-material
QIDI export, the unused-leading fixture duplicates per-filament settings to three
entries, sets logical self-indices to 1/2/3, maps all three to the single nozzle,
and assigns the object to filament 3. Box temperatures are 35/40/45°C and initial
nozzle temperatures 200/210/220°C. The support-first fixture additionally uses
three raft layers with support and interface filament 1, marked as support.
The fixtures do not contain physical Box-slot assignments.

Run either input with the official release's extracted `AppRun`:

```sh
AppRun --slice 0 --outputdir NEW_OUTPUT --export-3mf out.3mf sparse-project.3mf
AppRun --slice 0 --outputdir NEW_OUTPUT --export-3mf out.3mf support-first-project.3mf
```

On this Fedora host the release runs through the already-installed GNOME Flatpak
runtime. Use `flatpak run --unshare=network --filesystem=PROJECT_DIRECTORY
--command=ABSOLUTE_APP_RUN org.gnome.Platform//50 ...`, with XDG configuration,
cache and data directories redirected into the validation workspace. The QIDI
release does not accept Orca's `--datadir` option. No existing slicer profile or
printer connection is needed. GUI/thumbnail rendering is not validated here.

Unused-leading expected startup: `BOX_TEMP_SET VT2=45`,
`BOX_PRINT_START EXTRUDER=2`, then `T2`.
Support-first expected startup: `BOX_TEMP_SET VT0=35 VT2=45`,
`BOX_PRINT_START EXTRUDER=2`, then `T0`, followed later by `T2`.
Both logical indices need valid physical mappings at print submission.

Profile/G-code content derives from QIDI Studio under AGPL-3.0; see the root
LICENSE, sources.json and patch attribution. The cube is generated test geometry.
