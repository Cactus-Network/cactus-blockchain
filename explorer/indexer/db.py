from __future__ import annotations

from typing import Any, Iterable, List, Optional, Sequence, Tuple

import asyncpg

from chia_rs import BlockRecord

from .nodedb import decode_amount
from .rewards import farmer_reward, pool_reward

BLOCK_COLUMNS: Tuple[str, ...] = (
    "height",
    "header_hash",
    "prev_hash",
    "timestamp",
    "is_transaction_block",
    "weight",
    "total_iters",
    "signage_point_index",
    "farmer_puzzle_hash",
    "pool_puzzle_hash",
    "fees",
    "required_iters",
    "deficit",
    "overflow",
    "sub_slot_iters",
    "farmer_reward",
    "pool_reward",
)

COIN_COLUMNS: Tuple[str, ...] = (
    "coin_name",
    "confirmed_height",
    "spent_height",
    "coinbase",
    "puzzle_hash",
    "parent_coin_name",
    "amount",
    "timestamp",
)


async def create_pool(dsn: str, *, min_size: int = 1, max_size: int = 8) -> asyncpg.Pool:
    pool = await asyncpg.create_pool(dsn, min_size=min_size, max_size=max_size)
    assert pool is not None
    return pool


def block_to_row(rec: BlockRecord) -> Tuple[Any, ...]:
    """Flatten a BlockRecord into a BLOCK_COLUMNS-ordered row.

    timestamp and fees stay None on non-transaction blocks — that is the signal
    the UI needs to render them differently, so do not substitute zero.
    """
    height = int(rec.height)
    return (
        height,
        bytes(rec.header_hash),
        bytes(rec.prev_hash),
        None if rec.timestamp is None else int(rec.timestamp),
        rec.timestamp is not None,  # is_transaction_block
        int(rec.weight),
        int(rec.total_iters),
        int(rec.signage_point_index),
        bytes(rec.farmer_puzzle_hash),
        bytes(rec.pool_puzzle_hash),
        None if rec.fees is None else int(rec.fees),
        int(rec.required_iters),
        int(rec.deficit),
        bool(rec.overflow),
        int(rec.sub_slot_iters),
        farmer_reward(height),
        pool_reward(height),
    )


def coin_to_row(row: Sequence[Any], *, clamp_spent_above: Optional[int] = None) -> Tuple[Any, ...]:
    """Convert a raw node coin_record row into a COIN_COLUMNS-ordered row.

    `clamp_spent_above` exists for the backfill.  The node's coin_record reflects
    the node's *current* peak, which runs ahead of the height we have blocks for.
    Recording spent_height above our watermark would claim a spend in a block we
    have not indexed yet, so we store the coin as unspent and let the tail apply
    the spend when it reaches that height.
    """
    coin_name, confirmed_index, spent_index, coinbase, puzzle_hash, coin_parent, amount, timestamp = row
    spent = int(spent_index)
    if clamp_spent_above is not None and spent > clamp_spent_above:
        spent = 0
    return (
        bytes(coin_name),
        int(confirmed_index),
        spent,
        bool(coinbase),
        bytes(puzzle_hash),
        bytes(coin_parent),
        decode_amount(amount),
        None if timestamp is None else int(timestamp),
    )


async def get_state(conn: asyncpg.Connection, key: str) -> Optional[int]:
    value = await conn.fetchval("SELECT value FROM sync_state WHERE key = $1", key)
    return None if value is None else int(value)


async def set_state(conn: asyncpg.Connection, key: str, value: int) -> None:
    await conn.execute(
        "INSERT INTO sync_state (key, value) VALUES ($1, $2) "
        "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
        key,
        value,
    )


async def copy_blocks(conn: asyncpg.Connection, rows: Iterable[Tuple[Any, ...]]) -> None:
    await conn.copy_records_to_table("blocks", records=rows, columns=list(BLOCK_COLUMNS))


async def copy_coins(conn: asyncpg.Connection, rows: Iterable[Tuple[Any, ...]]) -> None:
    await conn.copy_records_to_table("coins", records=rows, columns=list(COIN_COLUMNS))


async def upsert_block(conn: asyncpg.Connection, row: Tuple[Any, ...]) -> None:
    placeholders = ", ".join(f"${i}" for i in range(1, len(BLOCK_COLUMNS) + 1))
    updates = ", ".join(f"{c} = EXCLUDED.{c}" for c in BLOCK_COLUMNS if c != "height")
    await conn.execute(
        f"INSERT INTO blocks ({', '.join(BLOCK_COLUMNS)}) VALUES ({placeholders}) "
        f"ON CONFLICT (height) DO UPDATE SET {updates}",
        *row,
    )


async def upsert_coins(conn: asyncpg.Connection, rows: Sequence[Tuple[Any, ...]]) -> None:
    if not rows:
        return
    placeholders = ", ".join(f"${i}" for i in range(1, len(COIN_COLUMNS) + 1))
    updates = ", ".join(f"{c} = EXCLUDED.{c}" for c in COIN_COLUMNS if c != "coin_name")
    await conn.executemany(
        f"INSERT INTO coins ({', '.join(COIN_COLUMNS)}) VALUES ({placeholders}) "
        f"ON CONFLICT (coin_name) DO UPDATE SET {updates}",
        rows,
    )


async def mark_spent(conn: asyncpg.Connection, coin_names: Sequence[bytes], height: int) -> None:
    if not coin_names:
        return
    await conn.execute(
        "UPDATE coins SET spent_height = $2 WHERE coin_name = ANY($1::bytea[])",
        [bytes(name) for name in coin_names],
        height,
    )


async def insert_spends(conn: asyncpg.Connection, rows: Sequence[Tuple[Any, ...]]) -> None:
    if not rows:
        return
    await conn.executemany(
        "INSERT INTO spends (coin_name, height, puzzle_reveal, solution, conditions) "
        "VALUES ($1, $2, $3, $4, $5) ON CONFLICT (coin_name) DO NOTHING",
        rows,
    )


async def header_hash_at(conn: asyncpg.Connection, height: int) -> Optional[bytes]:
    value = await conn.fetchval("SELECT header_hash FROM blocks WHERE height = $1", height)
    return None if value is None else bytes(value)


async def max_block_height(conn: asyncpg.Connection) -> Optional[int]:
    value = await conn.fetchval("SELECT MAX(height) FROM blocks")
    return None if value is None else int(value)


async def rollback_to(conn: asyncpg.Connection, height: int) -> None:
    """Undo everything strictly above `height` after a reorg.

    Order matters only for readability here (no FKs), but the whole thing must be
    one transaction: a half-applied rollback would leave coins attributed to
    blocks that no longer exist.
    """
    async with conn.transaction():
        await conn.execute("DELETE FROM coins WHERE confirmed_height > $1", height)
        await conn.execute("UPDATE coins SET spent_height = 0 WHERE spent_height > $1", height)
        await conn.execute("DELETE FROM spends WHERE height > $1", height)
        await conn.execute("DELETE FROM blocks WHERE height > $1", height)
        await set_state(conn, "tail_height", height)
