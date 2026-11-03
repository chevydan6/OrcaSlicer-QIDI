# Candidate 66 targeted checks

Build input `d1a35c855fd968125d39830f48328fdbd9eaf6b1`, AppImage SHA-256
`1483484b4b5db7ccf3b1e305f4f0c80c0850932a86658597c65000a8b692f854`.
Archive digest and all manifest patches verified in ../recovery-2026-11-03/artifact-66.json.
Ubuntu 24.04.5, Xvfb :2/Openbox, isolated initially empty settings, loopback-only fixture.
No debugger intervention. This is targeted evidence, not full acceptance; patches
67/68 address additional known defects and require a new matching binary.

- Fresh setup opens a populated Prepare page before any manual resize (04).
  Maximization, later Prepare/Preview/Device switches and slicing remain usable.
- Native connection with blank API key succeeds (07).
- Original unmodified sparse reference imports, slices and previews (12), and
  finds the QIDI fixture in Send (13). Third filament mapped to B2 (15) sends
  value_t2='slot5'. Captured upload retains BOX_TEMP_SET VT2=45,
  BOX_PRINT_START EXTRUDER=2 and T2. No physical-tool rewrite/compaction occurs.
- Original unmodified support-first reference imports, slices and previews (23).
  Send is disabled while its support material is unmapped (24). The reference
  declares filament_is_support=1 on PLA, represented by the UI as PLA-S/Sup.PLA.
  After fixture B2 reports PLA-S, it can map this support material. With T0 -> B2
  and T2 -> A1 (30), recorded assignment is value_t0='slot5', value_t2='slot0'.
  Upload retains BOX_TEMP_SET VT2=45 VT0=35, preparation EXTRUDER=2, first T0,
  and subsequent T2. Both tools have mappings; preparation and deposition differ.
- Closing the imported project, discarding modified presets and shutdown return exit 0 (32/33, exits.jsonl).
- Requests are recorded and discarded by the fixture. No real printer operations.

See sanitized submission requests and captured upload hashes/tool excerpts.
These checks must be repeated on the final candidate; no aggregate acceptance.
