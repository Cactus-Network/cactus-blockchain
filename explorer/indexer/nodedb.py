from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Optional, Tuple

from chia_rs import BlockRecord
from chia_rs.sized_bytes import bytes32

# Row shape yielded by coins_confirmed_in_range / coins_spent_at:
#   (coin_name, confirmed_index, spent_index, coinbase, puzzle_hash, coin_parent, amount, timestamp)
_COIN_COLUMNS = "coin_name, confirmed_index, spent_index, coinbase, puzzle_hash, coin_parent, amount, timestamp"


@contextmanager
def open_node_db(path: Path) -> Iterator[sqlite3.Connection]:
    """Open the full node's own database read-only.

    Safe to do while the node is running and syncing: the node keeps this file in
    WAL mode, so an independent reader does not block writers or get blocked by
    them.  query_only is belt-and-braces on top of mode=ro.
    """
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=60.0)
    try:
        conn.execute("PRAGMA query_only = ON")
        yield conn
    finally:
        conn.close()


def peak_height(conn: sqlite3.Connection) -> Optional[int]:
    """Height of the node's current peak, via the single-row current_peak table."""
    row = conn.execute("SELECT hash FROM current_peak WHERE key = 0").fetchone()
    if row is None:
        return None
    rec = conn.execute("SELECT block_record FROM full_blocks WHERE header_hash = ?", (row[0],)).fetchone()
    if rec is None:
        return None
    return int(BlockRecord.from_bytes(rec[0]).height)


def block_record_at(conn: sqlite3.Connection, height: int) -> Optional[BlockRecord]:
    """The main-chain BlockRecord at `height`, or None if the node has no such block."""
    row = conn.execute(
        "SELECT block_record FROM full_blocks WHERE in_main_chain = 1 AND height = ?",
        (height,),
    ).fetchone()
    return None if row is None else BlockRecord.from_bytes(row[0])


def block_records_in_range(conn: sqlite3.Connection, start: int, end: int) -> Iterator[BlockRecord]:
    """Main-chain BlockRecords for heights start..end inclusive, in height order.

    Reads only the `block_record` blob (~460 bytes, uncompressed) and never the
    `block` blob (~3.4 KB, zstd-compressed), which is what makes a full-chain
    header backfill cheap.  The WHERE clause is shaped to hit the node's partial
    `main_chain` index on (height, in_main_chain) WHERE in_main_chain = 1.
    """
    cursor = conn.execute(
        "SELECT block_record FROM full_blocks "
        "WHERE in_main_chain = 1 AND height >= ? AND height <= ? ORDER BY height",
        (start, end),
    )
    for row in cursor:
        yield BlockRecord.from_bytes(row[0])


def coins_confirmed_in_range(conn: sqlite3.Connection, start: int, end: int) -> Iterator[Tuple]:
    """Raw coin_record rows created between heights start..end inclusive."""
    cursor = conn.execute(
        f"SELECT {_COIN_COLUMNS} FROM coin_record WHERE confirmed_index >= ? AND confirmed_index <= ?",
        (start, end),
    )
    yield from cursor


def coins_confirmed_at(conn: sqlite3.Connection, height: int) -> List[Tuple]:
    return list(coins_confirmed_in_range(conn, height, height))


def coins_spent_at(conn: sqlite3.Connection, height: int) -> List[bytes]:
    """Coin ids spent at `height`.

    Deliberately reads the node's coin_record instead of calling the
    get_additions_and_removals RPC.  That endpoint takes blockchain.priority_mutex
    at *low* priority (cactus/rpc/full_node_rpc_api.py:788), so while the node is
    validating blocks it can starve for minutes and then fail outright.  The node
    has already computed and committed these rows; reading them is free.
    """
    cursor = conn.execute("SELECT coin_name FROM coin_record WHERE spent_index = ?", (height,))
    return [row[0] for row in cursor]


def decode_amount(blob: bytes) -> int:
    """coin_record.amount is a big-endian 8-byte uint64 (see cactus/full_node/coin_store.py)."""
    return int.from_bytes(blob, "big", signed=False)


def header_hash_at(conn: sqlite3.Connection, height: int) -> Optional[bytes32]:
    rec = block_record_at(conn, height)
    return None if rec is None else rec.header_hash
