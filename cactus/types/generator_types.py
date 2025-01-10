from __future__ import annotations

from dataclasses import dataclass
from typing import List

from cactus.types.blockchain_format.serialized_program import SerializedProgram
from cactus.util.streamable import Streamable, streamable


@streamable
@dataclass(frozen=True)
class BlockGenerator(Streamable):
    program: SerializedProgram
    generator_refs: List[bytes]
