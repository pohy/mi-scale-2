#!/usr/bin/env bash
set -eux

.venv/bin/activate

# If --watch flag has been passed, use inotify to re-run tests on file changes
if [[ $* == *--watch* ]]; then
    ptw --verbose
else
    pytest ./
fi