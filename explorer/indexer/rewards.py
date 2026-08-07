from __future__ import annotations

from cactus.consensus.block_rewards import calculate_base_farmer_reward, calculate_pool_reward
from chia_rs.sized_ints import uint32

# Halving boundary from cactus/consensus/block_rewards.py: 32 * 6 * 24 * 365.
BLOCKS_PER_YEAR = 1_681_920

# Era boundaries the reward schedule switches on.  Height 0 is its own era (the
# 210000 CAC premine), then a step every three years.
_ERA_STARTS = [0, 1, 3 * BLOCKS_PER_YEAR, 6 * BLOCKS_PER_YEAR, 9 * BLOCKS_PER_YEAR, 12 * BLOCKS_PER_YEAR]


def farmer_reward(height: int) -> int:
    """1/8 of the block reward, paid to the farmer's puzzle hash."""
    return int(calculate_base_farmer_reward(uint32(height)))


def pool_reward(height: int) -> int:
    """7/8 of the block reward.  A solo farmer acts as their own pool and takes it."""
    return int(calculate_pool_reward(uint32(height)))


def block_reward(height: int) -> int:
    return farmer_reward(height) + pool_reward(height)


def emitted_supply(height: int) -> int:
    """Total mojo created by block rewards through `height`, inclusive.

    This is emitted supply, not circulating supply: rewards that no farmer ever
    claimed still count here, and transaction fees are recycled rather than
    created.  Treat it as an upper bound.

    Summed per era instead of per block so /stats stays O(1) rather than looping
    over eight million heights.
    """
    if height < 0:
        return 0

    total = 0
    for i, start in enumerate(_ERA_STARTS):
        if height < start:
            break
        end = _ERA_STARTS[i + 1] - 1 if i + 1 < len(_ERA_STARTS) else height
        end = min(end, height)
        total += block_reward(start) * (end - start + 1)
    return total
