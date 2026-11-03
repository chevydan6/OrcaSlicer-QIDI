# New-host recovery (2026-11-03)

Recovered integration 70d58fc17f0132d926424a5a74144bf80cb1dcfd using existing GitHub keyring credentials.
Ubuntu 24.04.5 x86_64, GNOME Wayland with X display :0, GCC 13.3,
24 logical CPUs, 14 GiB RAM, 23 GiB swap, 279 GiB free disk. Xvfb,
Openbox and xdotool are installed. Build parallelism remains 2 for memory headroom.

All 56 patches apply and reproduce the previously recorded tree
20f0b1398164ca1b5ab5bd44c6ecd6071aaaad3e. The local recovery commit
482bb670 has new commit metadata but the identical downstream tree.

Integration run 41595285772 passed; static run 41595289239 failed with:

```
AMSMaterialsSetting.cpp:1123:9: error: no header providing "wxColourData" is directly included
[misc-include-cleaner,-warnings-as-errors] (add #include <wx/colourdata.h>)
```

Patch 57 supplies exactly that header. Its tree is
0e97b1e9b901311fc5b8cd40f3d5330ef70f1888. This is an attempted correction
until matching CI completes, and requires its own GUI acceptance.

Downloaded integration report artifact 13212568130: SHA256
9cfb23d0c8b104dc5e7c5d14701a4ea22eef3321036164004412d56971e84b79,
matching GitHub's artifact digest. CTest XML: 2912 cases, zero failures,
errors or skips. MAX4 results: 21 passing cases, including original embedded
sparse and support-first projects. No final-build GUI or hardware claim.
