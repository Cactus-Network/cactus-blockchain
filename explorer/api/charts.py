"""Daily chart series aggregated from the blocks table.

One whole-history SQL rollup, cached in-process for CACHE_TTL seconds, sliced
per request.  Netspace is estimated exactly the way the node's
get_network_space RPC does (cactus/rpc/full_node_rpc_api.py):

    space = UI_ACTUAL_SPACE_CONSTANT_FACTOR            # 0.78
          * (delta_weight / delta_total_iters)         # between two blocks
          * DIFFICULTY_CONSTANT_FACTOR                 # from consensus constants
          * 2 ** calculate_prefix_bits(constants, newer_height)

using the last transaction block of each UTC day as the boundary pair, so each
point smooths over roughly a day's worth of blocks (the node itself smooths
over 4608 blocks — comparable).
"""

from __future__ import annotations

import time
from typing import Any, Dict, List

from fastapi import APIRouter, Query, Request

from cactus.consensus.constants import replace_str_to_bytes
from cactus.consensus.default_constants import DEFAULT_CONSTANTS
from cactus.consensus.pos_quality import UI_ACTUAL_SPACE_CONSTANT_FACTOR
from chia_rs import PlotParam

from cactus.types.blockchain_format.proof_of_space import calculate_prefix_bits

from indexer.config import Settings

router = APIRouter()

settings = Settings.load()
# Build constants exactly like the node does (cactus/server/start_full_node.py):
# defaults patched with this network's overrides from config.yaml.
_overrides = settings.net_config["network_overrides"]["constants"][settings.network]
CONSTANTS = replace_str_to_bytes(DEFAULT_CONSTANTS, **_overrides)

CACHE_TTL = 600.0  # seconds; charts don't need to move block-by-block

# Last transaction block of each UTC day (only transaction blocks carry
# timestamps).  Counting blocks via day-boundary height deltas counts *all*
# blocks, including timestamp-less ones, without touching them directly.
DAILY_SQL = """
WITH tx AS (
  SELECT timestamp / 86400 AS day, height, weight, total_iters, fees
  FROM blocks WHERE timestamp IS NOT NULL
),
bounds AS (
  SELECT DISTINCT ON (day) day, height, weight, total_iters
  FROM tx ORDER BY day, height DESC
),
daily AS (
  SELECT day, COUNT(*) AS tx_blocks, COALESCE(SUM(fees::numeric), 0) AS fees
  FROM tx GROUP BY day
)
SELECT b.day, b.height, b.weight, b.total_iters, d.tx_blocks, d.fees
FROM bounds b JOIN daily d USING (day) ORDER BY b.day
"""

_cache: Dict[str, Any] = {"ts": 0.0, "payload": None}


def netspace_bytes(delta_weight: int, delta_iters: int, height: int) -> int:
    if delta_iters <= 0:
        return 0
    prefix_bits = calculate_prefix_bits(CONSTANTS, height, PlotParam.make_v1(32))
    return int(
        UI_ACTUAL_SPACE_CONSTANT_FACTOR
        * (delta_weight / delta_iters)
        * int(CONSTANTS.DIFFICULTY_CONSTANT_FACTOR)
        * 2**prefix_bits
    )


async def build_series(pool: Any) -> Dict[str, List[Any]]:
    async with pool.acquire() as conn:
        rows = await conn.fetch(DAILY_SQL)

    days: List[int] = []
    netspace: List[str] = []
    blocks: List[int] = []
    tx_blocks: List[int] = []
    fees: List[str] = []
    avg_block_time: List[float] = []

    # The first day has no prior boundary to delta against, and the newest day
    # is still accumulating blocks (its bucket is incomplete until the day
    # rolls over), so both ends are dropped.
    for prev, cur in zip(rows[:-1], rows[1:-1]):
        d_height = cur["height"] - prev["height"]
        if d_height <= 0:
            continue
        days.append(cur["day"] * 86400)  # UTC midnight, epoch seconds
        netspace.append(
            str(
                netspace_bytes(
                    int(cur["weight"]) - int(prev["weight"]),
                    int(cur["total_iters"]) - int(prev["total_iters"]),
                    cur["height"],
                )
            )
        )
        blocks.append(d_height)
        tx_blocks.append(cur["tx_blocks"])
        fees.append(str(int(cur["fees"])))
        avg_block_time.append(round(86400 / d_height, 2))

    return {
        "days": days,
        "netspace_bytes": netspace,  # strings: values exceed 2^53
        "blocks": blocks,
        "tx_blocks": tx_blocks,
        "fees_mojo": fees,
        "avg_block_time": avg_block_time,
    }


@router.get("/charts")
async def charts(request: Request, days: int = Query(365, ge=0)) -> Dict[str, Any]:
    """Daily series; days=0 returns the full history."""
    now = time.monotonic()
    if _cache["payload"] is None or now - _cache["ts"] > CACHE_TTL:
        _cache["payload"] = await build_series(request.app.state.pool)
        _cache["ts"] = now

    payload: Dict[str, List[Any]] = _cache["payload"]
    if days and len(payload["days"]) > days:
        payload = {key: series[-days:] for key, series in payload.items()}
    return payload
