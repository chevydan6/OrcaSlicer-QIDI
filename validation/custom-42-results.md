# 42-patch integrated build

Integration commit: 5314b5df14012266bd514c707fc90d92a748fcfa.
Run: https://github.com/chevydan6/OrcaSlicer-QIDI/actions/runs/41574937523
The workflow completed successfully, including compiler-cache archival.

Compilation and AppImage packaging pass. CTest reports 2,910 tests, zero failures
and five skipped tests. The four G-code import regressions from earlier custom
builds are resolved. All seven upstream CLI regressions, 72 vendor profile
bundles and 19 MAX4 slicing/persistence cases pass.

Verified log artifact 13205623033 SHA256:
2008544bea9350b5a1b35b1056c576952348b9447355b318c29d0eb172ebcdda.

Verified AppImage ZIP artifact 13205910848 SHA256:
cfc4b9a3b5dd76c26c2d87dce56e6ffcf922d520e1874fc4c6d87ddbfe3de4bb.
The five skips require an installed comma-decimal locale; the final workflow
now generates German and French UTF-8 locales before running tests.

This validates patches 1–42 only. Later GUI changes, final installation and
physical MAX4/Box behavior are not covered by this run. No hardware was contacted.
