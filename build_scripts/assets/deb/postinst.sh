#!/usr/bin/env bash
# Post install script for the UI .deb to place symlinks in places to allow the CLI to work similarly in both versions

set -e

ln -s /usr/lib/cactus-blockchain/resources/app.asar.unpacked/daemon/cactus /usr/bin/cactus || true
ln -s /usr/lib/cactus-blockchain/resources/app.asar.unpacked/daemon /opt/cactus || true
