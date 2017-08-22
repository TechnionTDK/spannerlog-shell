#!/usr/bin/env bash
# logging-with-ts -- Logs stdin to a file with timestamp on each line
set -eu
if [[ $# -gt 0 ]]; then
    for f; do mkdir -p "$(dirname "$f")"; done
    exec ts "%F %H:%M:%.S" | tee -a "$@"
else
    exec ts "%F %H:%M:%.S"
fi