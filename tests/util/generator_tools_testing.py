from __future__ import annotations

from typing import List, Tuple

from cactus.consensus.constants import ConsensusConstants
from cactus.consensus.default_constants import DEFAULT_CONSTANTS
from cactus.full_node.mempool_check_conditions import get_name_puzzle_conditions
from cactus.types.blockchain_format.coin import Coin
from cactus.types.blockchain_format.sized_bytes import bytes32
from cactus.types.full_block import FullBlock
from cactus.types.generator_types import BlockGenerator
from cactus.util.generator_tools import tx_removals_and_additions
from cactus.util.ints import uint32


def run_and_get_removals_and_additions(
    block: FullBlock,
    max_cost: int,
    *,
    height: uint32,
    constants: ConsensusConstants = DEFAULT_CONSTANTS,
    mempool_mode=False,
) -> Tuple[List[bytes32], List[Coin]]:
    removals: List[bytes32] = []
    additions: List[Coin] = []

    assert len(block.transactions_generator_ref_list) == 0
    if not block.is_transaction_block():
        return [], []

    if block.transactions_generator is not None:
        npc_result = get_name_puzzle_conditions(
            BlockGenerator(block.transactions_generator, [], []),
            max_cost,
            mempool_mode=mempool_mode,
            height=height,
            constants=constants,
        )
        assert npc_result.error is None
        rem, add = tx_removals_and_additions(npc_result.conds)
        # build removals list
        removals.extend(rem)
        additions.extend(add)

    rewards = block.get_included_reward_coins()
    additions.extend(rewards)
    return removals, additions
