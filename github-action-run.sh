#!/bin/sh

# Locally run job test of CI workflow in .github/workflows/test.yml. Helpful for debugging.
act -j test --container-architecture linux/amd64 -P ubuntu-latest=catthehacker/ubuntu:act-latest --action-offline-mode --container-daemon-socket -