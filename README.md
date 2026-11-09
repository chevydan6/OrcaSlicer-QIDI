# OrcaSlicer QIDI MAX4 / Box port

The main source includes the QIDI Auto Refill control, layer/progress reporting,
ETA that excludes preparation, a neutral camera placeholder and a 10 FPS
snapshot viewer. All 75 patches are applied by the normal Linux build; printer
addresses remain user settings entered through **Connect by address**.


Personal Linux x86_64 build based on pinned official OrcaSlicer, with QIDI Studio's
MAX4/Box LAN functionality. **Candidate70 is software-accepted and installed using
X11/XWayland.** Automatic refill and broader physical validation remain unfinished.

[Download the accepted build and source](https://github.com/chevydan6/OrcaSlicer-QIDI/releases/tag/qidi-linux-2026-11-03-c70) ·
[Exact acceptance record](validation/accepted-70.json) ·
[Current handoff](HANDOFF.md) · [Build/install](docs/build.md) ·
[Using the build](docs/using-the-build.md)

Compilation, 2,916 unit cases, seven CLI regressions, 72 vendor bundles, 21 MAX4
cases, static checks and 63 exact-binary GUI cases passed. Actual launcher/menu,
settings persistence, file chooser, slicing/preview and clean exit were verified.
An authorized sparse T2→A1 physical print completed all20 layers on the MAX4.
[Hardware evidence](validation/hardware-2026-11-04/README.md) also records inaccurate
GUI layer/time displays; broader hardware behavior remains unverified.

This is an integration kit, not a checked-in Orca source tree. `sources.json` pins
both official baselines; `patches/` holds70 ordered patches. The release includes
the matching patched source archive, manifest, checksums, reports and evidence.
Orca's engine and supported existing behavior remain the base. Original AGPL,
copyright and dependency notices are preserved.

Implemented controls, verified scope and gaps are distinguished in the
[feature checklist](docs/feature-checklist.md) and [limitations](docs/limitations.md).
Refill, manual drying, QIDI cloud/MQTT/tunnels and native Wayland acceptance are
unfinished. Mixed Box/external, multicolor external and QIDI batch jobs are rejected.
No supported Flatpak package was produced for this Ubuntu milestone.

The authorized small print session is complete. Further runout/thermal experiments
require a concrete agreed [supervised session](docs/hardware-validation-plan.md).
The general port is not claimed complete.
