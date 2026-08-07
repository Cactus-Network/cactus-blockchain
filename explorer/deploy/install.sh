#!/bin/bash
# Root-side install for the Cactus explorer: systemd units + nginx (port 80).
# Run:  sudo bash explorer/deploy/install.sh
# TLS (Cloudflare origin cert) is added afterwards — see RUNBOOK.md step 4.
set -euo pipefail
cd "$(dirname "$0")"

echo "== systemd units =="
cp cactus-explorer-api.service cactus-explorer-tail.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now cactus-explorer-api cactus-explorer-tail

echo "== nginx =="
if ! command -v nginx >/dev/null; then
    apt-get update -qq
    apt-get install -y nginx
fi
cp nginx-explorer.conf /etc/nginx/sites-available/explorer
ln -sf /etc/nginx/sites-available/explorer /etc/nginx/sites-enabled/explorer
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "== verify =="
sleep 2
systemctl --no-pager --lines=0 status cactus-explorer-api cactus-explorer-tail | grep -E 'service|Active'
curl -sf http://127.0.0.1:8000/api/stats >/dev/null && echo "API on :8000 OK"
curl -sf -H 'Host: explorer.cactus-network.net' http://127.0.0.1/api/stats >/dev/null && echo "nginx -> API OK"
curl -sf -H 'Host: explorer.cactus-network.net' http://127.0.0.1/ -o /dev/null && echo "nginx frontend OK"
echo "Done."
