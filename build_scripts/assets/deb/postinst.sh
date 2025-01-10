#!/usr/bin/env bash
# Post install script for the UI .deb to place symlinks in places to allow the CLI to work similarly in both versions

set -e

chown -f root:root /opt/cactus/chrome-sandbox || true
chmod -f 4755 /opt/cactus/chrome-sandbox || true
ln -s /opt/cactus/resources/app.asar.unpacked/daemon/cactus /usr/bin/cactus || true
ln -s /opt/cactus/cactus-blockchain /usr/bin/cactus-blockchain || true
