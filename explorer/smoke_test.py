"""Validate the node-side half of the indexer without needing Postgres.

Checks that we can parse the running node's own database, shape rows the way the
schema expects, and round-trip addresses.  Run from the explorer/ directory:

    ../venv/bin/python smoke_test.py
"""

from __future__ import annotations

import sys

from cactus.util.bech32m import decode_puzzle_hash, encode_puzzle_hash
from chia_rs.sized_bytes import bytes32

from indexer import db, nodedb, rewards
from indexer.config import MOJO_PER_CACTUS, Settings

FAILURES: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    status = "ok  " if condition else "FAIL"
    print(f"[{status}] {label}{f' — {detail}' if detail else ''}")
    if not condition:
        FAILURES.append(label)


def main() -> int:
    settings = Settings.load()
    print(f"network={settings.network} prefix={settings.address_prefix} db={settings.node_db_path}")
    print(f"rpc={settings.self_hostname}:{settings.rpc_port} dsn={settings.dsn}\n")

    check("node database exists", settings.node_db_path.is_file(), str(settings.node_db_path))
    if not settings.node_db_path.is_file():
        return 1

    with nodedb.open_node_db(settings.node_db_path) as conn:
        peak = nodedb.peak_height(conn)
        check("read peak height", peak is not None, f"{peak:,}" if peak else "none")
        assert peak is not None

        # Header path: parse a range and shape it for COPY.
        start = max(peak - 200, 0)
        records = list(nodedb.block_records_in_range(conn, start, peak))
        check("read block records", len(records) > 0, f"{len(records)} records at {start:,}..{peak:,}")

        rows = [db.block_to_row(rec) for rec in records]
        check(
            "block rows match BLOCK_COLUMNS width",
            all(len(row) == len(db.BLOCK_COLUMNS) for row in rows),
            f"{len(db.BLOCK_COLUMNS)} columns",
        )
        check("all block row values are pg-safe types", all(_pg_safe(row) for row in rows))

        tx_blocks = [rec for rec in records if rec.timestamp is not None]
        check(
            "transaction blocks carry timestamps, others do not",
            0 < len(tx_blocks) < len(records),
            f"{len(tx_blocks)}/{len(records)} are transaction blocks",
        )

        # Chain linkage: every record's prev_hash must be the previous header hash.
        linked = all(
            bytes(records[i].prev_hash) == bytes(records[i - 1].header_hash)
            for i in range(1, len(records))
            if records[i].height == records[i - 1].height + 1
        )
        check("prev_hash chain is contiguous (reorg check basis)", linked)

        # Coin path.
        sample_height = next((rec.height for rec in reversed(tx_blocks)), peak)
        coin_rows = nodedb.coins_confirmed_at(conn, int(sample_height))
        shaped = [db.coin_to_row(row, clamp_spent_above=peak) for row in coin_rows]
        check("read coins for a height", len(shaped) > 0, f"{len(shaped)} coins at height {sample_height:,}")
        check(
            "coin rows match COIN_COLUMNS width",
            all(len(row) == len(db.COIN_COLUMNS) for row in shaped),
            f"{len(db.COIN_COLUMNS)} columns",
        )
        check("all coin amounts fit BIGINT", all(0 <= row[6] < 2**63 for row in shaped))
        check("all coin row values are pg-safe types", all(_pg_safe(row) for row in shaped))

        rewards_found = [row for row in shaped if row[3]]
        check("reward coins are flagged coinbase", len(rewards_found) > 0, f"{len(rewards_found)} coinbase coins")

        # The clamp must never record a spend above our watermark.
        clamped = [db.coin_to_row(row, clamp_spent_above=sample_height - 1) for row in coin_rows]
        check(
            "clamp_spent_above suppresses future spends",
            all(row[2] == 0 or row[2] <= sample_height - 1 for row in clamped),
        )

        # Address round-trip on real puzzle hashes.
        ph = bytes(records[-1].farmer_puzzle_hash)
        addr = encode_puzzle_hash(bytes32(ph), settings.address_prefix)
        check(
            "puzzle hash <-> address round-trips",
            bytes(decode_puzzle_hash(addr)) == ph,
            addr,
        )

        # Rewards: at this height the 2 CAC era is over.
        height = int(peak)
        total = rewards.block_reward(height)
        check(
            "block reward split is 7/8 pool + 1/8 farmer",
            rewards.pool_reward(height) == total * 7 // 8 and rewards.farmer_reward(height) == total * 1 // 8,
            f"{total / MOJO_PER_CACTUS:g} CAC at height {height:,}",
        )
        check(
            "emitted supply covers the premine and both eras",
            rewards.emitted_supply(0) == 210_000 * MOJO_PER_CACTUS
            and rewards.emitted_supply(height) > rewards.emitted_supply(0),
            f"{rewards.emitted_supply(height) / MOJO_PER_CACTUS:,.0f} CAC emitted by height {height:,}",
        )

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) failed: {', '.join(FAILURES)}")
        return 1
    print("all checks passed")
    return 0


def _pg_safe(row: tuple) -> bool:
    """asyncpg wants plain builtins; cactus's uint/bytes32 subclasses should already be unwrapped."""
    return all(value is None or type(value) in (int, str, bytes, bool) for value in row)


if __name__ == "__main__":
    sys.exit(main())
