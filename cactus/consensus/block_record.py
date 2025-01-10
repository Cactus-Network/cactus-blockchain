from __future__ import annotations

from typing import Optional

import cactus_rs
from typing_extensions import Protocol

from cactus.types.blockchain_format.sized_bytes import bytes32
from cactus.util.ints import uint32, uint64

BlockRecord = cactus_rs.BlockRecord


class BlockRecordProtocol(Protocol):
    @property
    def header_hash(self) -> bytes32: ...

    @property
    def height(self) -> uint32: ...

    @property
    def timestamp(self) -> Optional[uint64]: ...

    @property
    def prev_transaction_block_height(self) -> uint32: ...

    @property
    def prev_transaction_block_hash(self) -> Optional[bytes32]: ...

    @property
    def is_transaction_block(self) -> bool:
        return self.timestamp is not None
