# Explorer go-live runbook — explorer.cactus-network.net

State as of 2026-08-03: explorer code, deploy files, and DNS (Cloudflare-proxied)
are done. Nothing is installed or running yet — public URL returns Cloudflare 523.
Postgres `cactus_explorer` is indexed to height 7,450,157; node peak is ~7,851,725
and the node itself is ~93% synced (target ~8,426,574). Machine: 192.168.1.238,
user `sgroiwes`, repo at /home/sgroiwes/cactus-blockchain.

## 1. Catch the index up (~2 min of backfill, resumes from watermark)

```bash
cd /home/sgroiwes/cactus-blockchain/explorer
../venv/bin/python -m indexer.backfill blocks
../venv/bin/python -m indexer.backfill coins
```

Both resume from their watermark; ~400k blocks at ~6k heights/s is a couple of
minutes. The node is still syncing — the tail service (step 2) follows the peak
from here on, so the explorer stays as fresh as the node is.

## 2. Install and start the systemd services

```bash
cd /home/sgroiwes/cactus-blockchain/explorer
sudo cp deploy/cactus-explorer-api.service deploy/cactus-explorer-tail.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now cactus-explorer-api cactus-explorer-tail
```

Verify:

```bash
curl -s http://127.0.0.1:8000/api/stats
systemctl status cactus-explorer-api cactus-explorer-tail --no-pager
journalctl -u cactus-explorer-tail -n 20 --no-pager   # should show heights advancing
```

## 3. nginx

```bash
sudo apt-get update && sudo apt-get install -y nginx
sudo cp deploy/nginx-explorer.conf /etc/nginx/sites-available/explorer
sudo ln -s /etc/nginx/sites-available/explorer /etc/nginx/sites-enabled/explorer
sudo rm -f /etc/nginx/sites-enabled/default
# www-data must be able to traverse to explorer/web:
chmod o+x /home/sgroiwes /home/sgroiwes/cactus-blockchain
sudo nginx -t && sudo systemctl reload nginx
curl -s -H 'Host: explorer.cactus-network.net' http://127.0.0.1/ | head -5   # expect index.html
curl -s -H 'Host: explorer.cactus-network.net' http://127.0.0.1/api/stats
```

## 4. TLS — Cloudflare Origin CA cert (recommended; the subdomain is proxied)

In the Cloudflare dashboard (manual, needs the user's browser):

1. SSL/TLS → Origin Server → **Create Certificate** — defaults are fine
   (RSA, `*.cactus-network.net` + `cactus-network.net`, 15 years).
2. Save the two PEM blocks on this machine:
   - cert → `/etc/ssl/cactus-explorer/origin.pem`
   - key  → `/etc/ssl/cactus-explorer/origin.key`  (chmod 600, root-owned)
3. SSL/TLS → Overview → set encryption mode to **Full (strict)**.
   (If the apex/www site currently relies on Flexible, set the mode per-hostname
   with a Configuration Rule for explorer.cactus-network.net instead of flipping
   the whole zone.)

Then add the TLS server block — duplicate the existing `server` block in
`/etc/nginx/sites-available/explorer`, and in the copy replace the two `listen`
lines with:

```
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    ssl_certificate     /etc/ssl/cactus-explorer/origin.pem;
    ssl_certificate_key /etc/ssl/cactus-explorer/origin.key;
```

and reduce the original port-80 block to a redirect:

```
server {
    listen 80;
    listen [::]:80;
    server_name explorer.cactus-network.net;
    return 301 https://$host$request_uri;
}
```

```bash
sudo nginx -t && sudo systemctl reload nginx
```

(Alternative if Origin CA is undesirable: temporarily grey-cloud the DNS record,
`sudo apt-get install certbot python3-certbot-nginx && sudo certbot --nginx -d
explorer.cactus-network.net`, then re-enable the proxy. Origin CA is less moving
parts and never expires on you.)

## 5. Router port-forward (manual, user)

Forward TCP **443** (and **80** for the redirect) on the router to
**192.168.1.238**. Cloudflare only needs to reach the origin on 443 once the
mode is Full (strict). If the router supports it, restrict the source to
[Cloudflare's IP ranges](https://www.cloudflare.com/ips/); otherwise plain
forwarding is fine — nginx only serves this one site.

## 6. Cloudflare tuning (manual, dashboard)

- Cache Rule: bypass cache for `explorer.cactus-network.net/api/*`
  (nginx already sends `Cache-Control: no-store`, this is belt-and-braces).
- Leave the record orange-cloud (proxied).

## 7. Verify from outside

```bash
curl -s https://explorer.cactus-network.net/api/stats
curl -s -o /dev/null -w '%{http_code}\n' https://explorer.cactus-network.net/
```

Expect 200s; check a block page and an address page in a browser, on phone data
(not LAN) to prove the port-forward.

## 8. Embed on the main site

Add a link or iframe on www.cactus-network.net:

```html
<iframe src="https://explorer.cactus-network.net/" style="width:100%;height:80vh;border:0"></iframe>
```

The explorer's CSP (`frame-ancestors`) already allows framing from
cactus-network.net and www.cactus-network.net only.

## Notes / gotchas

- The node is still syncing; until it finishes, the explorer's tip lags the real
  chain tip. No action needed — tail follows automatically.
- Don't `pip install` anything unpinned into the node venv (breaks cactus 2.5.0
  pins — see explorer/README.md).
- The July 22–25, 2022 near-stall in the charts (~100 blocks/day, netspace crash)
  is real chain history, not an indexing bug.
- If `api.service` fails at boot before Postgres is up, it retries every 5 s
  (`Restart=always`) — no action needed.
