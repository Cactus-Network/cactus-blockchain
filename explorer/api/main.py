from __future__ import annotations

import ipaddress
import os
from contextlib import asynccontextmanager
from decimal import Decimal
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional

import asyncpg
from fastapi import APIRouter, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from cactus.full_node.full_node_rpc_client import FullNodeRpcClient
from cactus.protocols.outbound_message import NodeType
from cactus.types.blockchain_format.program import Program
from cactus.wallet.cat_wallet.cat_constants import FAVCOIN_CAT
from cactus.wallet.cat_wallet.cat_utils import CAT_MOD_HASH_HASH, QUOTED_CAT_MOD_HASH
from cactus.wallet.util.curry_and_treehash import curry_and_treehash
from chia_rs.sized_bytes import bytes32
from cactus.util.bech32m import decode_puzzle_hash, encode_puzzle_hash
from chia_rs.sized_ints import uint16

from indexer import db, rewards
from indexer.config import MOJO_PER_CACTUS, Settings

settings = Settings.load()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.pool = await db.create_pool(settings.dsn, max_size=16)
    app.state.rpc = await FullNodeRpcClient.create(
        settings.self_hostname,
        uint16(settings.rpc_port),
        settings.root_path,
        settings.net_config,
    )
    try:
        yield
    finally:
        app.state.rpc.close()
        await app.state.rpc.await_closed()
        await app.state.pool.close()


app = FastAPI(title=f"Cactus Explorer API ({settings.network})", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("EXPLORER_CORS_ORIGINS", "*").split(","),
    allow_methods=["GET"],
    allow_headers=["*"],
)

# JSON endpoints live under /api; the static frontend is mounted at / (bottom of
# this file, after the routes are declared).  Same paths whether uvicorn serves
# everything (dev) or nginx serves web/ directly and proxies only /api/ (prod).
api = APIRouter()


# ---------------------------------------------------------------- formatting


def address_of(puzzle_hash: bytes) -> str:
    return encode_puzzle_hash(bytes32(bytes(puzzle_hash)), settings.address_prefix)


def hex0x(value: Optional[bytes]) -> Optional[str]:
    return None if value is None else f"0x{bytes(value).hex()}"


def amount(mojo: Any) -> Dict[str, str]:
    """Amounts go out as strings.

    Mojo values exceed 2^53, so a JSON number would silently lose precision in
    any browser client.
    """
    value = int(mojo if not isinstance(mojo, Decimal) else mojo.to_integral_value())
    whole, frac = divmod(value, MOJO_PER_CACTUS)
    return {"mojo": str(value), "cactus": f"{whole}.{frac:012d}".rstrip("0").rstrip(".") or "0"}


MOJO_PER_CAT = 1000  # CATs carry 3 decimals, unlike CAC's 12

# CATs shown on address pages.  A CAT coin sits on-chain under the CAT mod
# curried with (asset id, recipient puzzle hash), so for a known asset id the
# wrapped puzzle hash — and therefore the balance — is an ordinary indexed
# lookup in `coins`.  FavCoin only for now.
KNOWN_CATS = [
    {
        "name": FAVCOIN_CAT["name"],
        "symbol": FAVCOIN_CAT["symbol"],
        "asset_id": bytes32.fromhex(FAVCOIN_CAT["asset_id"]),
        "asset_id_hash": Program.to(bytes32.fromhex(FAVCOIN_CAT["asset_id"])).get_tree_hash(),
    }
]


def cat_wrapped_puzzle_hash(asset_id_hash: bytes32, puzzle_hash: bytes) -> bytes:
    # An address's puzzle hash is already the inner puzzle's tree hash, so the
    # outer hash needs no puzzle reveal — only curried-argument hashing.
    return bytes(curry_and_treehash(QUOTED_CAT_MOD_HASH, CAT_MOD_HASH_HASH, asset_id_hash, bytes32(bytes(puzzle_hash))))


def cat_amount(mojo: Any) -> Dict[str, str]:
    value = int(mojo if not isinstance(mojo, Decimal) else mojo.to_integral_value())
    whole, frac = divmod(value, MOJO_PER_CAT)
    return {"mojo": str(value), "tokens": f"{whole}.{frac:03d}".rstrip("0").rstrip(".") or "0"}


def block_json(row: asyncpg.Record) -> Dict[str, Any]:
    return {
        "height": row["height"],
        "header_hash": hex0x(row["header_hash"]),
        "prev_hash": hex0x(row["prev_hash"]),
        "timestamp": row["timestamp"],
        "is_transaction_block": row["is_transaction_block"],
        "weight": str(row["weight"]),
        "total_iters": str(row["total_iters"]),
        "signage_point_index": row["signage_point_index"],
        "farmer_puzzle_hash": hex0x(row["farmer_puzzle_hash"]),
        "farmer_address": address_of(row["farmer_puzzle_hash"]),
        "pool_puzzle_hash": hex0x(row["pool_puzzle_hash"]),
        "pool_address": address_of(row["pool_puzzle_hash"]),
        "fees": None if row["fees"] is None else amount(row["fees"]),
        "required_iters": row["required_iters"],
        "deficit": row["deficit"],
        "overflow": row["overflow"],
        "sub_slot_iters": str(row["sub_slot_iters"]),
        "farmer_reward": amount(row["farmer_reward"]),
        "pool_reward": amount(row["pool_reward"]),
    }


def coin_json(row: asyncpg.Record) -> Dict[str, Any]:
    return {
        "coin_name": hex0x(row["coin_name"]),
        "confirmed_height": row["confirmed_height"],
        "spent_height": None if row["spent_height"] == 0 else row["spent_height"],
        "spent": row["spent_height"] != 0,
        "coinbase": row["coinbase"],
        "puzzle_hash": hex0x(row["puzzle_hash"]),
        "address": address_of(row["puzzle_hash"]),
        "parent_coin_name": hex0x(row["parent_coin_name"]),
        "amount": amount(row["amount"]),
        "timestamp": row["timestamp"],
    }


def cat_coin_json(row: asyncpg.Record) -> Dict[str, Any]:
    # The generic renderer encodes the wrapped puzzle hash as a cac1... address,
    # which is not where a wallet shows the coin — drop it rather than mislead.
    result = coin_json(row)
    result["amount"] = cat_amount(row["amount"])
    del result["address"]
    return result


def parse_hash(value: str) -> bytes:
    raw = value[2:] if value.startswith("0x") else value
    try:
        decoded = bytes.fromhex(raw)
    except ValueError:
        raise HTTPException(status_code=400, detail="not a hex hash")
    if len(decoded) != 32:
        raise HTTPException(status_code=400, detail="expected a 32-byte hash")
    return decoded


# ---------------------------------------------------------------- endpoints


@api.get("/stats")
async def stats() -> Dict[str, Any]:
    async with app.state.pool.acquire() as conn:
        indexed_tip = await db.max_block_height(conn)
        tail_height = await db.get_state(conn, "tail_height")
        blocks_mark = await db.get_state(conn, "blocks_backfilled_to")
        coins_mark = await db.get_state(conn, "coins_backfilled_to")
        # reltuples is an estimate maintained by autovacuum.  An exact COUNT(*)
        # over hundreds of millions of coins would take minutes.
        coin_estimate = await conn.fetchval("SELECT reltuples::bigint FROM pg_class WHERE relname = 'coins'")

    node: Dict[str, Any] = {}
    try:
        # The client unwraps the "blockchain_state" envelope; peak is a BlockRecord.
        state = await app.state.rpc.get_blockchain_state()
        peak = state["peak"]
        node = {
            "peak_height": None if peak is None else int(peak.height),
            "difficulty": state["difficulty"],
            "average_block_time": state["average_block_time"],
            "space_bytes": str(state["space"]),
            "space_pib": round(state["space"] / 2**50, 3),
            "synced": state["sync"]["synced"],
            "sync_progress_height": state["sync"]["sync_progress_height"],
            "sync_tip_height": state["sync"]["sync_tip_height"],
            "mempool_size": state["mempool_size"],
        }
    except Exception as exc:  # node down or RPC unreachable — index still serves
        node = {"error": f"full node RPC unavailable: {exc}"}

    supply_height = indexed_tip if indexed_tip is not None else 0
    return {
        "network": settings.network,
        "address_prefix": settings.address_prefix,
        "index": {
            "tip_height": indexed_tip,
            "tail_height": tail_height,
            "blocks_backfilled_to": blocks_mark,
            "coins_backfilled_to": coins_mark,
            "coins_estimate": None if coin_estimate is None else int(coin_estimate),
        },
        "node": node,
        # Emitted, not circulating: unclaimed rewards count, fees do not.
        "emitted_supply": amount(rewards.emitted_supply(supply_height)),
    }


@api.get("/blocks")
async def recent_blocks(
    before_height: Optional[int] = Query(None, description="return blocks strictly below this height"),
    limit: int = Query(25, ge=1, le=200),
) -> Dict[str, Any]:
    async with app.state.pool.acquire() as conn:
        if before_height is None:
            rows = await conn.fetch("SELECT * FROM blocks ORDER BY height DESC LIMIT $1", limit)
        else:
            rows = await conn.fetch(
                "SELECT * FROM blocks WHERE height < $1 ORDER BY height DESC LIMIT $2", before_height, limit
            )
    return {"blocks": [block_json(row) for row in rows]}


@api.get("/block/{ident}")
async def block(ident: str) -> Dict[str, Any]:
    async with app.state.pool.acquire() as conn:
        if ident.isdigit():
            row = await conn.fetchrow("SELECT * FROM blocks WHERE height = $1", int(ident))
        else:
            row = await conn.fetchrow("SELECT * FROM blocks WHERE header_hash = $1", parse_hash(ident))
        if row is None:
            raise HTTPException(status_code=404, detail="block not indexed")

        height = row["height"]
        coin_summary = await conn.fetchrow(
            "SELECT COUNT(*) AS additions, COALESCE(SUM(amount::numeric), 0) AS added_value "
            "FROM coins WHERE confirmed_height = $1",
            height,
        )
        removals = await conn.fetchval("SELECT COUNT(*) FROM coins WHERE spent_height = $1", height)

    result = block_json(row)
    result["coins"] = {
        "additions": coin_summary["additions"],
        "added_value": amount(coin_summary["added_value"]),
        "removals": removals,
    }
    return result


@api.get("/address/{address}")
async def address_detail(
    address: str,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> Dict[str, Any]:
    try:
        puzzle_hash = bytes(decode_puzzle_hash(address))
    except ValueError:
        raise HTTPException(status_code=400, detail=f"not a valid {settings.address_prefix}1... address")

    async with app.state.pool.acquire() as conn:
        totals = await conn.fetchrow(
            "SELECT COALESCE(SUM(amount::numeric) FILTER (WHERE spent_height = 0), 0) AS balance, "
            "       COALESCE(SUM(amount::numeric), 0) AS total_received, "
            "       COUNT(*) AS coin_count, "
            "       COUNT(*) FILTER (WHERE spent_height = 0) AS unspent_count, "
            "       COUNT(*) FILTER (WHERE coinbase) AS reward_count "
            "FROM coins WHERE puzzle_hash = $1",
            puzzle_hash,
        )
        coins = await conn.fetch(
            "SELECT * FROM coins WHERE puzzle_hash = $1 ORDER BY confirmed_height DESC LIMIT $2 OFFSET $3",
            puzzle_hash,
            limit,
            offset,
        )
        farmed = await conn.fetchval("SELECT COUNT(*) FROM blocks WHERE farmer_puzzle_hash = $1", puzzle_hash)
        pooled = await conn.fetchval("SELECT COUNT(*) FROM blocks WHERE pool_puzzle_hash = $1", puzzle_hash)

        tokens: List[Dict[str, Any]] = []
        for cat in KNOWN_CATS:
            wrapped = cat_wrapped_puzzle_hash(cat["asset_id_hash"], puzzle_hash)
            cat_totals = await conn.fetchrow(
                "SELECT COALESCE(SUM(amount::numeric) FILTER (WHERE spent_height = 0), 0) AS balance, "
                "       COALESCE(SUM(amount::numeric), 0) AS total_received, "
                "       COUNT(*) AS coin_count, "
                "       COUNT(*) FILTER (WHERE spent_height = 0) AS unspent_count "
                "FROM coins WHERE puzzle_hash = $1",
                wrapped,
            )
            if cat_totals["coin_count"] == 0:
                continue
            cat_coins = await conn.fetch(
                "SELECT * FROM coins WHERE puzzle_hash = $1 ORDER BY confirmed_height DESC LIMIT 50", wrapped
            )
            tokens.append(
                {
                    "name": cat["name"],
                    "symbol": cat["symbol"],
                    "asset_id": hex0x(cat["asset_id"]),
                    "wrapped_puzzle_hash": hex0x(wrapped),
                    "balance": cat_amount(cat_totals["balance"]),
                    "total_received": cat_amount(cat_totals["total_received"]),
                    "coin_count": cat_totals["coin_count"],
                    "unspent_count": cat_totals["unspent_count"],
                    "coins": [cat_coin_json(row) for row in cat_coins],
                }
            )

    return {
        "address": address,
        "puzzle_hash": hex0x(puzzle_hash),
        "balance": amount(totals["balance"]),
        "total_received": amount(totals["total_received"]),
        "coin_count": totals["coin_count"],
        "unspent_count": totals["unspent_count"],
        "reward_coin_count": totals["reward_count"],
        "blocks_won_as_farmer": farmed,
        "blocks_won_as_pool": pooled,
        "coins": [coin_json(row) for row in coins],
        "tokens": tokens,
        "paging": {"limit": limit, "offset": offset},
    }


@api.get("/coin/{coin_id}")
async def coin(coin_id: str) -> Dict[str, Any]:
    name = parse_hash(coin_id)
    async with app.state.pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM coins WHERE coin_name = $1", name)
        if row is None:
            raise HTTPException(status_code=404, detail="coin not indexed")
        children = await conn.fetch(
            "SELECT * FROM coins WHERE parent_coin_name = $1 ORDER BY confirmed_height LIMIT 200", name
        )
        spend = await conn.fetchrow(
            "SELECT height, puzzle_reveal, solution, conditions FROM spends WHERE coin_name = $1", name
        )

    result = coin_json(row)
    result["children"] = [coin_json(child) for child in children]
    if spend is not None:
        result["spend"] = {
            "height": spend["height"],
            "puzzle_reveal": hex0x(spend["puzzle_reveal"]),
            "solution": hex0x(spend["solution"]),
            "conditions": spend["conditions"],
        }
    return result


@api.get("/mempool")
async def mempool(limit: int = Query(50, ge=1, le=500)) -> Dict[str, Any]:
    try:
        items = await app.state.rpc.get_all_mempool_items()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"full node RPC unavailable: {exc}")

    entries: List[Dict[str, Any]] = []
    for tx_id, item in list(items.items())[:limit]:
        entries.append(
            {
                "tx_id": hex0x(tx_id),
                "cost": item.get("cost"),
                "fee": None if item.get("fee") is None else amount(item["fee"]),
                "spend_count": len(item.get("spend_bundle", {}).get("coin_spends", [])),
            }
        )
    return {"count": len(items), "items": entries}


@api.get("/peers")
async def peers() -> Dict[str, Any]:
    """Full nodes currently connected to our node — live peers a farmer can add."""
    try:
        connections = await app.state.rpc.get_connections(NodeType.FULL_NODE)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"full node RPC unavailable: {exc}")

    entries: List[Dict[str, Any]] = []
    seen = set()
    for con in connections:
        host = con["peer_host"]
        # Inbound connections arrive from an ephemeral port; peer_server_port is
        # the port the peer actually listens on, which is what a farmer needs.
        port = con.get("peer_server_port") or con["peer_port"]
        try:
            if not ipaddress.ip_address(host).is_global:
                continue  # LAN/loopback peers are unreachable for outside farmers
        except ValueError:
            pass  # hostname, not an IP — keep it
        if (host, port) in seen:
            continue
        seen.add((host, port))
        entries.append(
            {
                "host": host,
                "port": port,
                "connected_since": con.get("creation_time"),
                "last_message_time": con.get("last_message_time"),
                "bytes_read": con.get("bytes_read"),
                "bytes_written": con.get("bytes_written"),
            }
        )

    # Longest-lived connections first: they have proven themselves reachable.
    entries.sort(key=lambda p: p["connected_since"] or float("inf"))
    return {"count": len(entries), "peers": entries}


@api.get("/search")
async def search(q: str = Query(..., min_length=1)) -> Dict[str, Any]:
    """Dispatch a single search box by the shape of the input."""
    query = q.strip()

    if query.isdigit():
        return {"kind": "block", "result": await block(query)}

    if query.startswith(f"{settings.address_prefix}1"):
        # Pass limit/offset explicitly: calling an endpoint function directly
        # hands it FastAPI's Query() default objects rather than ints, which
        # asyncpg then rejects as bind parameters.
        return {"kind": "address", "result": await address_detail(query, limit=50, offset=0)}

    raw = parse_hash(query)
    async with app.state.pool.acquire() as conn:
        height = await conn.fetchval("SELECT height FROM blocks WHERE header_hash = $1", raw)
    if height is not None:
        return {"kind": "block", "result": await block(str(height))}

    return {"kind": "coin", "result": await coin(query)}


# ---------------------------------------------------------------- wiring

from api import charts  # noqa: E402  (needs `app` defined for pool access)

api.include_router(charts.router)
app.include_router(api, prefix="/api")

# The static frontend.  html=True serves web/index.html at /; the SPA uses hash
# routing so no server-side fallback rewrites are needed.
app.mount("/", StaticFiles(directory=Path(__file__).parent.parent / "web", html=True), name="web")
