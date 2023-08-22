from __future__ import annotations

from cactus.consensus.cost_calculator import NPCResult
from cactus.consensus.default_constants import DEFAULT_CONSTANTS
from cactus.full_node.bundle_tools import simple_solution_generator
from cactus.full_node.mempool_check_conditions import get_name_puzzle_conditions
from cactus.types.blockchain_format.program import INFINITE_COST
from cactus.types.generator_types import BlockGenerator
from cactus.types.spend_bundle import SpendBundle


def cost_of_spend_bundle(spend_bundle: SpendBundle) -> int:
    program: BlockGenerator = simple_solution_generator(spend_bundle)
    # always use the post soft-fork2 semantics
    npc_result: NPCResult = get_name_puzzle_conditions(
        program,
        INFINITE_COST,
        mempool_mode=True,
        height=DEFAULT_CONSTANTS.SOFT_FORK2_HEIGHT,
        constants=DEFAULT_CONSTANTS,
    )
    return npc_result.cost
