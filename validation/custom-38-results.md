# 38-patch compiled validation

Integration source: 93f7fca02c0fe575b3d964542980af6f375f2113.
Run: https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41569816164
Verified log artifact: 13203762631.

Compilation/AppImage packaging succeeded. The unit results retain exactly the
four upstream G-code header regressions corrected by patch 41. QIDI project
import, protocol/HTTP, credential and callback tests did not fail.

18 of 19 MAX4 slicing cases pass. Both original QIDI Studio projects now import
and slice: sparse selection retains T2/220 C and VT2=45; support-first retains
T0/200 C before later T2, with VT0=35 and VT2=45. These are generated G-code
values, not heater commands sent to a printer. The remaining standalone CLI
fixture lacked explicit support flags; the integration script now supplies them.
See custom-38-slicing.json for per-case traces.

Local rerun with the corrected fixture: all 19/19 cases pass on the verified
38-patch AppImage (see custom-38-local-slicing.json).

GUI validation and final-build checks remain pending. No hardware was contacted.
