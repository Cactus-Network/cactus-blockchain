# Cactus block explorer — indexer + API + frontend

Reads a local Cactus full node and maintains a Postgres index that can answer the
questions an explorer front end asks: blocks by height or hash, coins by id,
balance and history by address, farmer/pool attribution, chain stats, mempool.

`web/` is a build-free vanilla-JS frontend (dashboard, blocks, block/address/coin
detail, charts) served by the same FastAPI app at `/`, with the JSON API under
`/api/`. `deploy/` has the systemd units and nginx config to put it on the
internet.

## How it gets its data

Two sources, chosen per job:

| Job | Source | Why |
| --- | --- | --- |
| Bulk backfill of headers | node's `blockchain_v2_*.sqlite`, read-only | `block_record` blobs are ~460 B and uncompressed; 8.4M of them is a few GB, not a few hundred |
| Bulk backfill of coins | same sqlite, `coin_record` table | already indexed on `puzzle_hash`, and `coinbase` marks reward coins, so address history needs no CLVM execution at all |
| Live tip, netspace, difficulty, mempool | full node RPC (`:11555`) | cheap and current |
| Coin additions/removals per block | node sqlite, by `confirmed_index` / `spent_index` | see the warning below |

**Do not use the `get_additions_and_removals` RPC for this.** It acquires
`blockchain.priority_mutex` at *low* priority
(`cactus/rpc/full_node_rpc_api.py:788`), so while the node is validating or
syncing blocks it starves and eventually fails. The node has already committed
those coin rows; reading them read-only is free and never blocks. Opening the
node's database alongside the running node is safe because the node keeps it in
WAL mode.

## Setup

```bash
# 1. Postgres
sudo apt install postgresql
sudo -u postgres createuser --superuser "$USER"     # or grant narrower rights
createdb cactus_explorer
psql cactus_explorer -f explorer/schema.sql

# 2. Python deps, into the cactus venv (the indexer imports cactus itself)
./venv/bin/pip install -r explorer/requirements.txt
```

Configuration comes from the node's own `config.yaml` — network, RPC port,
database path and address prefix are all read from there. Two env overrides:

- `EXPLORER_DSN` — Postgres DSN (default `postgresql:///cactus_explorer`)
- `CACTUS_ROOT` — node root (default `~/.cactus/mainnet`)

## Running

All commands run from the `explorer/` directory.

```bash
cd explorer

# Backfill headers, then coins.  Both resume from a watermark if interrupted.
../venv/bin/python -m indexer.backfill blocks
../venv/bin/python -m indexer.backfill coins

# Follow the tip from there on
../venv/bin/python -m indexer.tail

# API on :8000
../venv/bin/python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Measured on a 5,001-height slice of mainnet at height ~6.69M: **5,900 heights/s**
for blocks, **9,400 heights/s** for coins, both single-process. A full 8.4M-block
backfill is therefore roughly 24 minutes of blocks plus 15 minutes of coins —
minutes, not days, which is the whole reason this reads sqlite rather than RPC.
Coin density in that slice was 2.14 coins per block, so expect ~18M coin rows
chain-wide and an index in the tens of GB once every table and index is built.

The first backfill run pins a `snapshot_height` (the node's peak at that moment)
and both backfills target it. That keeps the watermarks meaningful while the node
keeps moving. `indexer.tail` picks up from the highest indexed block.

To parallelise a cold backfill, run several processes over disjoint ranges and
keep them from fighting over the watermark:

```bash
../venv/bin/python -m indexer.backfill blocks --start 0       --end 2000000 --no-watermark &
../venv/bin/python -m indexer.backfill blocks --start 2000001 --end 4000000 --no-watermark &
```

Then set the watermark once by running the plain command, which will find the
already-copied ranges present and continue past them.

### Verify before you commit to a full backfill

`smoke_test.py` exercises everything that touches the node — parsing, row
shaping, the spent-height clamp, address round-tripping, the reward schedule —
and needs no Postgres:

```bash
cd explorer && ../venv/bin/python smoke_test.py
```

### Optional: spend detail

`indexer.tail --with-spends` also records puzzle reveals, solutions and parsed
conditions into `spends`. This is off by default because those blobs will
outgrow every other table combined. Coin-level history does not need it.

## API

| Endpoint | Notes |
| --- | --- |
| `GET /stats` | index watermarks, node peak/netspace/sync, emitted supply |
| `GET /blocks?before_height=&limit=` | reverse-height page |
| `GET /block/{height or hash}` | plus addition/removal counts for the height |
| `GET /address/{cac1...}` | balance, totals, blocks won, paged coins |
| `GET /coin/{coin_id}` | coin, children, spend detail if indexed |
| `GET /mempool` | live, straight from the node |
| `GET /search?q=` | dispatches on shape: height, `cac1…`, or 32-byte hash |
| `GET /charts?days=` | daily series: netspace, blocks/day, tx blocks, fees, avg block time; `days=0` = full history |

All endpoints are served under the `/api/` prefix (e.g. `/api/stats`); the
static frontend in `web/` is mounted at `/`.

Amounts are returned as `{"mojo": "...", "cactus": "..."}` **strings**. Mojo
values exceed 2^53, so JSON numbers would lose precision in any browser client.

`/api/charts` estimates netspace exactly the way the node's `get_network_space`
RPC does — `0.78 × (Δweight / Δtotal_iters) × DIFFICULTY_CONSTANT_FACTOR ×
2^prefix_bits` — between the last transaction blocks of consecutive UTC days,
with constants built from `config.yaml` overrides like the node builds its own.
The whole-history rollup is cached in-process for 10 minutes. The newest
(incomplete) day is dropped so blocks/day never undercounts.

## Frontend (`web/`)

No build step: plain ES modules, hash routing (`#/`, `#/blocks`,
`#/block/<h|hash>`, `#/address/<cac1…>`, `#/coin/<id>`, `#/charts`), uPlot
vendored in `web/vendor/` (pinned 1.6.31, the only dependency). Light/dark
themes follow the OS with a manual toggle (persisted); the dashboard
auto-refreshes every 15 s and pauses while the tab is hidden. A banner shows
index/node sync progress whenever the index trails the node's peak.

`js/app.js` is referenced as `?v=1` from `index.html` — bump the version when
deploying changed assets so the 5-minute nginx cache never serves a stale app.

## Things worth knowing before you extend it

- **Timestamps only exist on transaction blocks.** `blocks.timestamp` and
  `blocks.fees` are NULL otherwise. Do not coalesce them to zero; show the
  inherited value or nothing.
- **`spent_height = 0` means unspent**, matching the node's own convention in
  `coin_record.spent_index`.
- **Addresses are not stored.** A `cac1…` text column would add ~62 bytes to
  every coin row — on the order of a gigabyte, for data that is a pure function
  of `puzzle_hash`. Puzzle hashes are stored raw and converted at the API edge
  with `encode_puzzle_hash` / `decode_puzzle_hash` (`cactus/util/bech32m.py`).
- **`SUM(amount)` must be cast to numeric.** Per-coin amounts fit in `BIGINT`,
  but emitted supply (~1.4e19 mojo) exceeds it. Every aggregate in `api/main.py`
  uses `amount::numeric`.
- **`/stats` coin count is an estimate** from `pg_class.reltuples`, because an
  exact `COUNT(*)` gets slow as `coins` grows.
- **`weight` and `total_iters` are `uint128` on the node but `BIGINT` here.**
  At height 6.7M they are 4.4e10 and 1.1e13 against a `BIGINT` ceiling of 9.2e18,
  so there is a very wide margin — but they are stored as strings in API
  responses for the same precision reason as amounts.
- **Installing FastAPI unpinned will break your node's venv.** cactus 2.5.0 pins
  `typing-extensions==4.11.0`; current pydantic-core needs 4.15+. Use
  `requirements.txt` as written, and confirm with `./venv/bin/pip check`.
- **Rewards** come from `cactus/consensus/block_rewards.py` — 7/8 pool, 1/8
  farmer, halving every 3 × 1,681,920 blocks. Past height 5,045,760 the block
  reward is 1 CAC, not 2. `indexer/rewards.py` sums per era so `/stats` stays
  O(1).
- **Reorgs** are handled by comparing each new block's `prev_hash` against the
  stored header hash, walking back to the fork point, and deleting above it in
  one transaction (`db.rollback_to`). The walk-back is capped at 1000 blocks;
  deeper divergence needs a manual re-backfill.

## Deployment

Run the indexer on the same host as the node and **never expose the node's RPC
port publicly** — it is a privileged API that includes `push_tx`, and the same
private CA fronts the wallet RPC. Expose only this explorer, behind nginx/TLS.
The API is read-only and holds no keys; uvicorn binds 127.0.0.1 only.

Everything needed is in `deploy/`:

```bash
# 1. services: tail indexer + uvicorn
sudo cp deploy/cactus-explorer-{tail,api}.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now cactus-explorer-tail cactus-explorer-api
curl -s localhost:8000/api/stats   # sanity check

# 2. nginx site (see the header of the file for the permissions note)
sudo cp deploy/nginx-explorer.conf /etc/nginx/sites-available/explorer
sudo ln -s /etc/nginx/sites-available/explorer /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 3. DNS + TLS: point explorer.cactus-network.net (A record) at this machine's
#    public IP, forward ports 80+443 to it, then:
sudo certbot --nginx -d explorer.cactus-network.net
```

Firewall: open 80/443 only. Ports 8000 (uvicorn) and 11555 (node RPC) stay
loopback-only.

### Embedding in www.cactus-network.net

The nginx config sends `Content-Security-Policy: frame-ancestors 'self'
https://www.cactus-network.net https://cactus-network.net`, so the main site —
and only the main site — can iframe the explorer:

```html
<iframe src="https://explorer.cactus-network.net/"
        style="width:100%;height:90vh;border:0" title="Cactus Explorer"></iframe>
```

A plain nav link to the subdomain works too and is simpler. If the main site
should ever fetch the JSON API directly (widgets on its own pages), the allowed
origins are set via `EXPLORER_CORS_ORIGINS` in `cactus-explorer-api.service`.

## Not covered yet

CAT / NFT / DID decoding, singleton tracking, pool membership, per-address
transaction grouping (coins are grouped by block, not by spend bundle), and
price data. All of them build on the tables here.
