# 51-patch integration results

Run 41590831679 compiled and packaged the application. Unit tests report
2,912 cases, zero failures and zero skips. The seven upstream CLI regressions
and 72 vendor bundles pass. Static checks in run 41590827707 pass.

19 of 21 MAX4 cases pass. Both new original-machine CLI cases reject process
compatibility before slicing (-17): patch 34 replaced the embedded QIDI machine
name with Orca's alias. Patch 54 retains both names. These are failed acceptance
cases, despite the corresponding GUI slice passing. Final compiled rerun required.

Logs artifact 13211340495 verified ZIP SHA256:
65948c39b9cf6cb92a4902ac26ccff2d1e05e9d6a107a6399f3e9fe264075254.
