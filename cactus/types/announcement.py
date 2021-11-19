from dataclasses import dataclass

from cactus.types.blockchain_format.sized_bytes import bytes32
from cactus.util.hash import std_hash


@dataclass(frozen=True)
class Announcement:
    origin_info: bytes32
    message: bytes

    def name(self) -> bytes32:
        return std_hash(bytes(self.origin_info + self.message))

    def __str__(self):
        return self.name().decode("utf-8")
