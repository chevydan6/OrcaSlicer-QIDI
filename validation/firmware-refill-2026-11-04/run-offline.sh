#!/bin/bash
set -eu
# First argument: private analysis workspace containing emulator/, runtime/, snapshot/.
# Remaining arguments are passed to the copied ARM Python 3.9 interpreter.
refill_workspace=$(realpath -- "$1")
shift
exec sudo -n unshare -n -- runuser -u "$(id -un)" -- env \
  PYTHONDONTWRITEBYTECODE=1 PYTHONHOME="$refill_workspace/runtime/usr" \
  QEMU_LD_PREFIX="$refill_workspace/runtime" \
  "$refill_workspace/emulator/usr/bin/qemu-aarch64-static" \
  "$refill_workspace/runtime/usr/bin/python3.9" "$@"
