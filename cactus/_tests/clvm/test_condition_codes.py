from __future__ import annotations

import importlib_resources
from clvm.casts import int_from_bytes

from cactus.types.condition_opcodes import ConditionOpcode


def test_condition_codes_is_complete() -> None:
    condition_codes_path = importlib_resources.files("cactus.wallet.puzzles").joinpath("condition_codes.clib")
    contents = condition_codes_path.read_text(encoding="utf-8")
    for name, value in ConditionOpcode.__members__.items():
        assert f"(defconstant {name} {int_from_bytes(value)})" in contents
