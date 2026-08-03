from __future__ import annotations

from chia_rs import SpendBundle
from chia_rs.sized_ints import uint64

from cactus._tests.util.get_name_puzzle_conditions import NPCResult, get_name_puzzle_conditions
from cactus.consensus.default_constants import DEFAULT_CONSTANTS
from cactus.full_node.bundle_tools import simple_solution_generator
from cactus.types.blockchain_format.program import INFINITE_COST
from cactus.types.generator_types import BlockGenerator


def cost_of_spend_bundle(spend_bundle: SpendBundle) -> int:
    program: BlockGenerator = simple_solution_generator(spend_bundle)
    # always use the post soft-fork2 semantics
    npc_result: NPCResult = get_name_puzzle_conditions(
        program,
        INFINITE_COST,
        mempool_mode=True,
        height=DEFAULT_CONSTANTS.HARD_FORK_HEIGHT,
        constants=DEFAULT_CONSTANTS,
    )
    return uint64(0 if npc_result.conds is None else npc_result.conds.cost)
