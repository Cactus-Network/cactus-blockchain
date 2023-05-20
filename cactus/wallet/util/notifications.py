from __future__ import annotations

from cactus.types.blockchain_format.program import Program
from cactus.types.blockchain_format.sized_bytes import bytes32
from cactus.util.ints import uint64
from cactus.wallet.puzzles.load_clvm import load_clvm_maybe_recompile

NOTIFICATION_MOD = load_clvm_maybe_recompile("notification.clsp")


def construct_notification(target: bytes32, amount: uint64) -> Program:
    return NOTIFICATION_MOD.curry(target, amount)
