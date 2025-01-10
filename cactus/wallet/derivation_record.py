from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from cactus_rs import G1Element

from cactus.types.blockchain_format.sized_bytes import bytes32
from cactus.util.ints import uint32
from cactus.wallet.util.wallet_types import WalletType


@dataclass(frozen=True)
class DerivationRecord:
    """
    These are records representing a puzzle hash, which is generated from a
    public key, derivation index, and wallet type. Stored in the puzzle_store.
    """

    index: uint32
    puzzle_hash: bytes32
    _pubkey: Union[G1Element, bytes]
    wallet_type: WalletType
    wallet_id: uint32
    hardened: bool

    @property
    def pubkey(self) -> G1Element:
        assert isinstance(self._pubkey, G1Element)
        return self._pubkey
