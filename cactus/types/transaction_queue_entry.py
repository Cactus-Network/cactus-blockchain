from __future__ import annotations

import asyncio
import dataclasses
from dataclasses import dataclass, field
from typing import ClassVar, Generic, Optional, Tuple, TypeVar, Union

from cactus.server.ws_connection import WSCactusConnection
from cactus.types.blockchain_format.sized_bytes import bytes32
from cactus.types.mempool_inclusion_status import MempoolInclusionStatus
from cactus.types.spend_bundle import SpendBundle
from cactus.util.errors import Err

T = TypeVar("T")


class ValuedEventSentinel:
    pass


@dataclasses.dataclass
class ValuedEvent(Generic[T]):
    _value_sentinel: ClassVar[ValuedEventSentinel] = ValuedEventSentinel()

    _event: asyncio.Event = dataclasses.field(default_factory=asyncio.Event)
    _value: Union[ValuedEventSentinel, T] = _value_sentinel

    def set(self, value: T) -> None:
        if not isinstance(self._value, ValuedEventSentinel):
            raise Exception("Value already set")
        self._value = value
        self._event.set()

    async def wait(self) -> T:
        await self._event.wait()
        if isinstance(self._value, ValuedEventSentinel):
            raise Exception("Value not set despite event being set")
        return self._value


@dataclass(frozen=True)
class TransactionQueueEntry:
    """
    A transaction received from peer. This is put into a queue, and not yet in the mempool.
    """

    transaction: SpendBundle = field(compare=False)
    transaction_bytes: Optional[bytes] = field(compare=False)
    spend_name: bytes32
    peer: Optional[WSCactusConnection] = field(compare=False)
    test: bool = field(compare=False)
    done: ValuedEvent[Tuple[MempoolInclusionStatus, Optional[Err]]] = field(
        default_factory=ValuedEvent,
        compare=False,
    )
