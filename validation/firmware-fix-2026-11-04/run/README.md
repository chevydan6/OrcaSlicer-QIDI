# Authorized patched-firmware reference repeat — in progress

Official QIDI Studio2.07.02.73 submitted the same160-layer ABS block used in the
failed reference, with T0 mapped to physical slot1/A2. The uploaded G-code matches
the reviewed export and failed reference byte for byte. A download from printer
storage matches the captured upload. See submitted-job.json for hashes.

The fix is installed with SHA256
4513412930926926dc0d72ae1a0fbcdac3c1eba92e09c7b712171d7db842bd0f;
Klipper service restart returned ready. No whole-machine reboot or MCU flash was
performed. A2 contains orange ABS and A3 blue ABS; both deliberately retain matching
blue software metadata. Unrelated value_t2=slot0 remains present to expose the
original failure. Dan confirmed the bed and feed were ready before submission.

This is a live test, not an acceptance result. Required evidence is preservation
of logical T0 during refill, replacement A3 actually loading, blue deposition,
automatic continuation without manual Resume, and successful completion.
Startup temperature behavior remains a separate unresolved observation.
Candidate70's source, pins and binary are unchanged; an Orca comparison is pending.
