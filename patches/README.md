# Patch series

Apply numbered patches in lexical order to the Orca commit in `sources.json`.

`0001-max4-height-guards.patch`: ports QIDI Studio's MAX4 maximum-Z guards for
filament changes, timelapse lifts and end G-code. Keeps Orca's same-tool-change
guard and existing profile identities. Other nozzle sizes inherit the 0.4 mm
machine profile. Increments the Qidi bundle version.

Source: QIDITECH/QIDIStudio at `403b619d56147160bb883e94f95a7951245bc6d0`,
`resources/profiles/X 4 Series/machine/Qidi X-Max 4 0.4 nozzle.json`.
This derived profile content retains the upstream AGPL-3.0 licensing; see the
source repository's LICENSE and attribution. The numbered patch is not yet a
validated general feature port and does not claim to fix starting-filament selection.
