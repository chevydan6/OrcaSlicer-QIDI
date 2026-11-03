# Repeated material-editor regression through patch 52

AppImage artifact 13210653258, integration b55d4d7, run 41592020331.
The application compiles and static checks pass. Five repeated modal opens still
shrink from 370x232 to 354x132 client pixels; the sixth clips Confirm and Close.
The application remains responsive and closes normally, but the proposed maximum
size reset did not fix the layout. Patch 55 uses a fresh editor after each completed
QIDI session and must pass the repeated-open GUI check before acceptance.

Verified artifact ZIP SHA256:
a5e1cd54b46e1ba1d778004fb017c47b0ea01710a37a7a5ca2fbc918450c945e.
The full run was cancelled after packaging because a newer build superseded it.
