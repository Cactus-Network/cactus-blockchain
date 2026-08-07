#!/bin/bash
set -e
cd "$(dirname "$0")"
cp nginx-explorer-tls.conf /etc/nginx/sites-available/explorer
nginx -t
systemctl reload nginx
curl -sk -H "Host: explorer.cactus-network.net" https://127.0.0.1/api/stats | head -c 100; echo
echo "TLS OK"
