# Native connection dialog through patch 54

Verified AppImage artifact 13210384847, integration c9aaf84, run 41592928800.
Artifact ZIP SHA256 13e60e10c50dd52056b340f89a8cf2081b4725b21f34c50fd5bf11542fbf6419.

The native dialog shows complete address, optional API-key/CA and action controls.
Connect is disabled for an empty address. Entering http://127.0.0.1:19025 with an
empty API key enables Connect and returns to live fixture telemetry (one subscribed
client). Reopening has visible controls; Cancel returns to Device and a lamp request
still works. All traffic goes to the recording fixture, never a printer.
The next build adds the fresh material-editor lifecycle fix.
