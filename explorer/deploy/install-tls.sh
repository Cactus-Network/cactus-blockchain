#!/bin/bash
# Installs the Cloudflare Origin CA cert + TLS nginx config.
# Prereq: origin.pem and origin.key present next to this script
# (written there before running; they are moved to /etc/ssl and locked down).
# Run:  sudo bash explorer/deploy/install-tls.sh
set -euo pipefail
cd "$(dirname "$0")"

[ -f origin.pem ] && [ -f origin.key ] || { echo "origin.pem / origin.key not found next to this script"; exit 1; }

install -d -m 755 /etc/ssl/cactus-explorer
install -m 644 -o root -g root origin.pem /etc/ssl/cactus-explorer/origin.pem
install -m 600 -o root -g root origin.key /etc/ssl/cactus-explorer/origin.key
shred -u origin.key
rm -f origin.pem

cp nginx-explorer-tls.conf /etc/nginx/sites-available/explorer
nginx -t
systemctl reload nginx

echo "== verify =="
curl -sfk -H 'Host: explorer.cactus-network.net' https://127.0.0.1/api/stats >/dev/null && echo "TLS api OK"
curl -sf -H 'Host: explorer.cactus-network.net' http://127.0.0.1/ -o /dev/null -w '%{http_code}\n' | grep -q 301 && echo "HTTP->HTTPS redirect OK"
echo "Done."
