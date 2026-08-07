from __future__ import annotations

import argparse
import asyncio
import time
from typing import List, Optional, Tuple

from . import db, nodedb
from .config import Settings

BLOCKS_WATERMARK = "blocks_backfilled_to"
COINS_WATERMARK = "coins_backfilled_to"
SNAPSHOT = "snapshot_height"


async def _resolve_snapshot(conn, node_conn) -> int:
    """Height the backfill targets, pinned on first run.

    The node's peak moves while we work (and during initial sync it moves fast).
    Backfilling against a moving target makes the coin watermark meaningless, so
    the first run records one height and every later run reuses it.
    """
    existing = await db.get_state(conn, SNAPSHOT)
    if existing is not None:
        return existing
    peak = nodedb.peak_height(node_conn)
    if peak is None:
        raise SystemExit("node database has no peak yet — is the node running and past genesis?")
    await db.set_state(conn, SNAPSHOT, peak)
    return peak


def _progress(label: str, done: int, total: int, started: float) -> None:
    elapsed = max(time.monotonic() - started, 1e-6)
    rate = done / elapsed
    remaining = (total - done) / rate if rate > 0 else float("inf")
    pct = 100.0 * done / total if total else 100.0
    print(
        f"{label}: {done:,}/{total:,} ({pct:5.1f}%)  {rate:,.0f} heights/s  eta {remaining / 60:,.1f} min",
        flush=True,
    )


async def backfill_blocks(args: argparse.Namespace) -> None:
    settings = Settings.load()
    pool = await db.create_pool(settings.dsn, max_size=2)

    with nodedb.open_node_db(settings.node_db_path) as node_conn:
        async with pool.acquire() as conn:
            snapshot = await _resolve_snapshot(conn, node_conn)
            end = args.end if args.end is not None else snapshot
            if args.start is not None:
                start = args.start
            else:
                mark = await db.get_state(conn, BLOCKS_WATERMARK)
                start = 0 if mark is None else mark + 1

            if start > end:
                print(f"blocks: nothing to do (start {start:,} > end {end:,})")
                return
            print(f"blocks: {start:,}..{end:,} from {settings.node_db_path}", flush=True)

            started = time.monotonic()
            for chunk_start in range(start, end + 1, args.chunk):
                chunk_end = min(chunk_start + args.chunk - 1, end)
                rows = [db.block_to_row(rec) for rec in nodedb.block_records_in_range(node_conn, chunk_start, chunk_end)]

                async with conn.transaction():
                    # Makes re-running an already-copied range idempotent.
                    await conn.execute("DELETE FROM blocks WHERE height >= $1 AND height <= $2", chunk_start, chunk_end)
                    await db.copy_blocks(conn, rows)
                    if not args.no_watermark:
                        await db.set_state(conn, BLOCKS_WATERMARK, chunk_end)

                _progress("blocks", chunk_end - start + 1, end - start + 1, started)

    await pool.close()


async def backfill_coins(args: argparse.Namespace) -> None:
    settings = Settings.load()
    pool = await db.create_pool(settings.dsn, max_size=2)

    with nodedb.open_node_db(settings.node_db_path) as node_conn:
        async with pool.acquire() as conn:
            snapshot = await _resolve_snapshot(conn, node_conn)
            end = args.end if args.end is not None else snapshot
            if args.start is not None:
                start = args.start
            else:
                mark = await db.get_state(conn, COINS_WATERMARK)
                start = 0 if mark is None else mark + 1

            if start > end:
                print(f"coins: nothing to do (start {start:,} > end {end:,})")
                return
            print(f"coins: confirmed_height {start:,}..{end:,}", flush=True)

            started = time.monotonic()
            for chunk_start in range(start, end + 1, args.chunk):
                chunk_end = min(chunk_start + args.chunk - 1, end)
                rows = [
                    db.coin_to_row(row, clamp_spent_above=snapshot)
                    for row in nodedb.coins_confirmed_in_range(node_conn, chunk_start, chunk_end)
                ]

                async with conn.transaction():
                    await conn.execute(
                        "DELETE FROM coins WHERE confirmed_height >= $1 AND confirmed_height <= $2",
                        chunk_start,
                        chunk_end,
                    )
                    await db.copy_coins(conn, rows)
                    if not args.no_watermark:
                        await db.set_state(conn, COINS_WATERMARK, chunk_end)

                _progress("coins", chunk_end - start + 1, end - start + 1, started)

    await pool.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bulk-load the explorer index from the full node's own sqlite database.",
        epilog=(
            "Parallelism: run several processes over disjoint ranges with --start/--end "
            "--no-watermark, then set the watermark once at the end with the highest height copied."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name, handler, default_chunk in (("blocks", backfill_blocks, 5000), ("coins", backfill_coins, 2000)):
        p = sub.add_parser(name, help=f"backfill {name}")
        p.add_argument("--start", type=int, default=None, help="first height (default: resume from watermark)")
        p.add_argument("--end", type=int, default=None, help="last height (default: pinned snapshot height)")
        p.add_argument("--chunk", type=int, default=default_chunk, help="heights per transaction")
        p.add_argument("--no-watermark", action="store_true", help="do not advance the resume watermark")
        p.set_defaults(handler=handler)

    args = parser.parse_args()
    try:
        asyncio.run(args.handler(args))
    except KeyboardInterrupt:
        print("\ninterrupted — re-run the same command to resume from the last committed chunk")


if __name__ == "__main__":
    main()
