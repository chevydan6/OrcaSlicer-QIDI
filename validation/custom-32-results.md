# First custom build validation

Build source: integration commit 4d9dac7588c2acebbf127c2587e8c8e0cbb44414 (32 patches).
GitHub run: https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41567417124
Artifact 13201824977 verified SHA-256: fed8e5c27d94bae22d8c6b1d15baeb8c0d84db23c08cf573814f41ba01760e96.

- Compilation and AppImage packaging passed.
- All seven upstream CLI regressions passed, including the previously crashing malformed-input test.
- All 72 profile bundles passed the profile tool.
- Four of 2906 unit cases failed: empty-list G-code settings, exclusion-volume preview, manual tool-change comments, and belt preview. Each rejects upstream G-code after the application name changed. Patch 41 preserves both upstream and downstream banners; compiled confirmation pending.
- Original MAX4 run: 16/19 passed. Sparse standalone CLI fixture omitted the per-filament support column; after supplying explicit false entries, the identical binary passes 17/19, including unused leading logical tools and temperature persistence. The remaining two are original QIDI 3MF projects; patch 34 adds recognition and scoped migration. Their compiled checks are pending.
- First GUI launch succeeds using the registered GNOME 50 runtime with an isolated data directory and networking disabled. Controls and restart tests are not yet complete.
- The runner ran out of space archiving ccache after tests; the workflow now removes completed ephemeral build trees after retaining artifacts and before cache archival.

No printer was contacted. No physical behavior is verified.
