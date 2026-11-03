# 46-patch integrated build

Integration: 1b660e64f6d625343230aaf311827bf0515886b0.
Run: https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41578941419

Compilation, AppImage packaging, unit tests, seven upstream CLI tests, 72 vendor
profile bundles and 19 MAX4 slicing/persistence cases pass. CTest reports 2,910
cases, zero failures and five missing-locale skips.

Verified log ZIP artifact 13207458474 SHA256:
b85116b36cb30c83601d6ddf9a4f5c01fb67f7fe32b654434083f359958fdbb8.

This run includes the connection/settings/layout fixes through patch 46. It does
not validate later object-selection/material-editor fixes, nor physical hardware.
