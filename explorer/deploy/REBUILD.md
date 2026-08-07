# Rebuilding explorer.cactus-network.net on a fresh machine

This document is written to be handed to a Claude Code session on a brand-new
Linux machine after the original host has died. Work through it top to bottom;
everything scriptable is in this repo, and the few manual steps (Cloudflare
dashboard, router) are marked **[user]**.

## What survives a dead machine, and what doesn't

| Survives | Lost with the machine — how to recreate |
| --- | --- |
| All explorer code + deploy files (this repo, `explorer/`) | Chain DB (~66 GB) — resync the node, or restore a copy if one exists |
| Cloudflare DNS zone + account | Postgres index (~10 GB) — rebuilt from the node DB in ~40 min by backfill |
| This runbook | Cloudflare Origin TLS cert/key — re-issue in the dashboard (step 6) |
|  | Router port-forwards and ufw rules (steps 7–8) |

## Target architecture (single machine)

Cactus full node (mainnet, RPC `:11555` loopback-only) → Postgres `cactus_explorer`
(backfill from the node's sqlite, then a live tail service) → FastAPI/uvicorn on
`127.0.0.1:8000` → nginx with TLS on 443 → Cloudflare proxy →
`explorer.cactus-network.net`. The API is read-only and holds no keys. Never
expose the node RPC or wallet RPC ports publicly.

Reference machine was Ubuntu 22.04, user `sgroiwes`, repo at
`/home/sgroiwes/cactus-blockchain`. **The systemd units and nginx configs in
`explorer/deploy/` hardcode that user and path** — either recreate the same
user/path or edit the copies before installing them.

Disk: ≥120 GB free (node DB ~66 GB and growing, Postgres ~10 GB, plus headroom).

## 1. Node

```bash
git clone https://github.com/Cactus-Network/cactus-blockchain.git
cd cactus-blockchain
sh install.sh              # creates ./venv
. ./activate
cactus init
cactus keys add            # [user] farm/wallet keys only if this box should also farm;
                           #        the explorer itself needs no keys at all
cactus start node
```

Mainnet sync from scratch takes days. The explorer can be built while it syncs —
the backfill pins a snapshot height and the tail follows the node afterwards.

## 2. Explorer Python deps (into the node venv — the indexer imports `cactus`)

```bash
./venv/bin/pip install -r explorer/requirements.txt
./venv/bin/pip check       # must be clean; unpinned installs break the node's pins
```

## 3. Postgres

```bash
sudo apt-get install -y postgresql
sudo -u postgres createuser --superuser "$USER"
createdb cactus_explorer
psql cactus_explorer -f explorer/schema.sql
```

## 4. Index the chain

```bash
cd explorer
../venv/bin/python smoke_test.py             # needs no Postgres; run before backfilling
../venv/bin/python -m indexer.backfill blocks   # ~6k heights/s, resumes from watermark
../venv/bin/python -m indexer.backfill coins    # ~9k heights/s
```

See `explorer/README.md` for parallel backfill over disjoint ranges if in a hurry.

## 5. Services + nginx (port 80 first)

```bash
sudo bash explorer/deploy/install.sh
# installs cactus-explorer-api + cactus-explorer-tail systemd units, nginx site,
# and self-verifies with curl. www-data needs traverse rights:
chmod o+x "$HOME" "$HOME/cactus-blockchain"
```

Note the node itself also needs to start at boot: `deploy/cactus.service` at the
repo root (start `farmer timelord`, not `all`).

## 6. TLS — Cloudflare Origin CA **[user for the dashboard part]**

1. Cloudflare dashboard → SSL/TLS → Origin Server → Create Certificate
   (RSA, `*.cactus-network.net` + apex, 15 years).
2. Save the PEMs as `explorer/deploy/origin.pem` and `origin.key`
   (both are gitignored).
3. `sudo bash explorer/deploy/install-tls.sh` — moves them to
   `/etc/ssl/cactus-explorer/`, shreds the working copies, installs
   `nginx-explorer-tls.conf` (80 → 443 redirect included).
4. Zone encryption mode should already be **Full (strict)**; verify it.

## 7. Network path **[user]**

- Cloudflare DNS: point the `explorer` A record at the new public IP, keep it
  proxied (orange cloud).
- Router: forward TCP 80 + 443 to this machine's **LAN IP address** — on the
  fiber router, forwards must target an IP, not a hostname. Give the machine a
  DHCP reservation or static IP first.

## 8. Firewall

```bash
sudo ufw allow <your-ssh-port>/tcp    # FIRST — original box used 2222, not 22
sudo install -m 755 explorer/deploy/update-cloudflare-ufw /usr/local/sbin/
sudo ln -s /usr/local/sbin/update-cloudflare-ufw /etc/cron.weekly/update-cloudflare-ufw
sudo update-cloudflare-ufw            # allows 80/443 from Cloudflare ranges only
sudo ufw enable
```

## 9. Verify

```bash
curl -s https://explorer.cactus-network.net/api/stats          # index + node peaks
curl -s "https://explorer.cactus-network.net/api/address/<any cac1... address>"
```

Load an address page in a browser from phone data (not LAN) to prove the
port-forward. An address holding FavCoin should show a "FavCoin (FAV)" card —
CAT balances are computed per-address from the wrapped puzzle hash, no extra
indexing involved.

## Gotchas (hard-won; details in README.md / RUNBOOK.md)

- Never call the node's `get_additions_and_removals` RPC for bulk work — it
  starves during sync. The indexer reads the node's sqlite read-only instead.
- `js/app.js` and `css/style.css` are referenced as `?v=N` from `index.html`;
  bump on deploy (nginx caches static files for 5 min).
- The main site embeds the explorer in an iframe; CSP `frame-ancestors` in the
  nginx conf allows cactus-network.net only.
- The FavCoin claim broker (`favcoin/broker/`) is a separate service with its own
  runbook and is NOT part of this rebuild.
