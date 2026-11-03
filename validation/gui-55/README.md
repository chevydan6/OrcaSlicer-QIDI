# GUI checks through patch 55

Run 41593288187, integration 2922327. AppImage SHA256:
d8e960c695f0d9585f45e8d7177a543bbf81d4e3cc9034ed93b92a7dc8394a49.
Artifact 13211610660 ZIP SHA256:
5a61b2baf783c3f72d44c12f76c11ce0b6bc67bcfa424e45279340b3af75dbb9.

Five material editor reopenings retain the same 370x232 client size. QIDI PLA
Rapido remains selectable and Confirm sends the correct B2 SLOT=5 metadata.
The shared color palette opens outside the left edge when the editor is at the
screen edge; patch 56 replaces this QIDI path with a native RGB dialog.
Fault recovery completed before the user requested a pause. See `faults.json`:
malformed WebSocket JSON, null material name, extreme chamber numbers, invalid
Box object types and complete-status recovery leave the lamp control responsive.
HTTP 500 is handled; four delayed requests are recorded while Prepare/Device
navigation remains responsive; WebSocket reconnection restores the lamp control.
These are software checks against a recording/discarding loopback fixture only.
They do not establish crash freedom or physical printer behavior.

On pause, normal empty-project shutdown completed with exit code 0; see `exit.json`.
