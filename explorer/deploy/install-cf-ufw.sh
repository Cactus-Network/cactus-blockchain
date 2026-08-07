#!/bin/bash
# One-time install: Cloudflare-only ufw allowlist for 80/443 + weekly refresh.
# Run:  sudo bash explorer/deploy/install-cf-ufw.sh
set -euo pipefail
cd "$(dirname "$0")"

install -m 755 -o root -g root update-cloudflare-ufw /usr/local/sbin/update-cloudflare-ufw
ln -sf /usr/local/sbin/update-cloudflare-ufw /etc/cron.weekly/update-cloudflare-ufw

/usr/local/sbin/update-cloudflare-ufw

echo "== resulting rules for 80,443 =="
ufw status | grep -E '80,443|Status'
echo "Done."
