from __future__ import annotations

import argparse
import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Tuple

import asyncpg

from cactus.full_node.full_node_rpc_client import FullNodeRpcClient
from chia_rs.sized_bytes import bytes32
from chia_rs.sized_ints import uint16

from . import db, nodedb
from .config import Settings

log = logging.getLogger("tail")

TAIL_HEIGHT = "tail_height"
MAX_REORG_DEPTH = 1000


async def _open_rpc(settings: Settings) -> FullNodeRpcClient:
    return await FullNodeRpcClient.create(
        settings.self_hostname,
        uint16(settings.rpc_port),
        settings.root_path,
        settings.net_config,
    )


def _serialize_conditions(conditions: List[Any]) -> str:
    out = []
    for cond in conditions:
        opcode = cond.opcode
        out.append(
            {
                "opcode": f"0x{bytes(opcode).hex()}",
                "name": getattr(opcode, "name", None),
                "vars": [var.hex() for var in cond.vars],
            }
        )
    return json.dumps(out)


async def _find_fork_point(conn: asyncpg.Connection, node_conn, height: int) -> int:
    """Walk back from `height` until our stored header hash matches the node's.

    Returns the highest height we agree on.  Everything above it is orphaned and
    has to come back out of the index.
    """
    floor = max(height - MAX_REORG_DEPTH, 0)
    h = height
    while h >= floor:
        ours = await db.header_hash_at(conn, h)
        theirs = nodedb.header_hash_at(node_conn, h)
        if ours is None or (theirs is not None and ours == bytes(theirs)):
            return h
        h -= 1
    raise RuntimeError(
        f"no common ancestor within {MAX_REORG_DEPTH} blocks of height {height}; "
        f"the index is too far diverged to repair automatically"
    )


async def _apply_height(
    conn: asyncpg.Connection,
    node_conn,
    rpc: Optional[FullNodeRpcClient],
    height: int,
) -> None:
    rec = nodedb.block_record_at(node_conn, height)
    assert rec is not None  # caller checked

    added = [db.coin_to_row(row) for row in nodedb.coins_confirmed_at(node_conn, height)]
    removed = nodedb.coins_spent_at(node_conn, height)

    spend_rows: List[Tuple[Any, ...]] = []
    if rpc is not None and rec.timestamp is not None:
        # Only transaction blocks can contain spends.  This endpoint is safe to
        # call (unlike get_additions_and_removals, which contends on the
        # blockchain mutex), but it is the slowest part of the loop.
        spends = await rpc.get_block_spends_with_conditions(bytes32(rec.header_hash))
        for entry in spends or []:
            cs = entry.coin_spend
            spend_rows.append(
                (
                    bytes(cs.coin.name()),
                    height,
                    bytes(cs.puzzle_reveal),
                    bytes(cs.solution),
                    _serialize_conditions(entry.conditions),
                )
            )

    # One transaction per height: either the block and all of its coin effects
    # land together, or the watermark does not move.
    async with conn.transaction():
        await db.upsert_block(conn, db.block_to_row(rec))
        await db.upsert_coins(conn, added)
        await db.mark_spent(conn, removed, height)
        await db.insert_spends(conn, spend_rows)
        await db.set_state(conn, TAIL_HEIGHT, height)


async def run(args: argparse.Namespace) -> None:
    settings = Settings.load()
    pool = await db.create_pool(settings.dsn, max_size=4)
    rpc = await _open_rpc(settings)

    try:
        with nodedb.open_node_db(settings.node_db_path) as node_conn:
            async with pool.acquire() as conn:
                watermark = await db.get_state(conn, TAIL_HEIGHT)
                if watermark is None:
                    watermark = await db.max_block_height(conn)
                if watermark is None:
                    watermark = -1

                coins_mark = await db.get_state(conn, "coins_backfilled_to")
                if coins_mark is not None and coins_mark < watermark:
                    log.warning(
                        "coins are only backfilled to %s but blocks reach %s — "
                        "spends below %s may reference coins that are not indexed yet",
                        f"{coins_mark:,}",
                        f"{watermark:,}",
                        f"{watermark:,}",
                    )

                log.info("tailing from height %s", f"{watermark + 1:,}")

                while True:
                    # The client unwraps the "blockchain_state" envelope and
                    # returns peak as a BlockRecord, not a dict.
                    state = await rpc.get_blockchain_state()
                    peak = state["peak"]
                    if peak is None:
                        log.info("node has no peak yet; waiting")
                        await asyncio.sleep(args.poll)
                        continue

                    target = int(peak.height)
                    if args.stop_at is not None:
                        target = min(target, args.stop_at)

                    while watermark < target:
                        height = watermark + 1
                        rec = nodedb.block_record_at(node_conn, height)
                        if rec is None:
                            # Node reports a higher peak than it has committed to
                            # its main chain yet; come back next poll.
                            break

                        if height > 0:
                            ours = await db.header_hash_at(conn, height - 1)
                            if ours is not None and ours != bytes(rec.prev_hash):
                                fork = await _find_fork_point(conn, node_conn, height - 1)
                                log.warning("reorg detected at %s; rolling back to %s", f"{height:,}", f"{fork:,}")
                                await db.rollback_to(conn, fork)
                                watermark = fork
                                continue

                        await _apply_height(conn, node_conn, rpc if args.with_spends else None, height)
                        watermark = height
                        if height % 100 == 0 or height == target:
                            log.info("indexed height %s (node peak %s)", f"{height:,}", f"{target:,}")

                    if args.stop_at is not None and watermark >= args.stop_at:
                        log.info("reached --stop-at %s", f"{args.stop_at:,}")
                        return

                    if not state["sync"]["synced"]:
                        sync = state["sync"]
                        log.info(
                            "node still syncing: %s/%s",
                            f"{sync['sync_progress_height']:,}",
                            f"{sync['sync_tip_height']:,}",
                        )

                    await asyncio.sleep(args.poll)
    finally:
        rpc.close()
        await rpc.await_closed()
        await pool.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Follow the chain tip and keep the explorer index current.")
    parser.add_argument("--poll", type=float, default=5.0, help="seconds between peak checks (block time is ~19s)")
    parser.add_argument(
        "--with-spends",
        action="store_true",
        help="also record puzzle reveals, solutions and conditions (much larger index, slower)",
    )
    parser.add_argument("--stop-at", type=int, default=None, help="exit once this height is indexed (for testing)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    try:
        asyncio.run(run(args))
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
