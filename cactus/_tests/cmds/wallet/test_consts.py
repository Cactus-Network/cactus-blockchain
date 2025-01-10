from __future__ import annotations

from cactus_rs import Coin, G2Element

from cactus.types.blockchain_format.sized_bytes import bytes32
from cactus.util.ints import uint32, uint64
from cactus.wallet.conditions import ConditionValidTimes
from cactus.wallet.signer_protocol import KeyHints, SigningInstructions, TransactionInfo, UnsignedTransaction
from cactus.wallet.transaction_record import TransactionRecord
from cactus.wallet.util.transaction_type import TransactionType
from cactus.wallet.wallet_spend_bundle import WalletSpendBundle

FINGERPRINT: str = "123456"
FINGERPRINT_ARG: str = f"-f{FINGERPRINT}"
CAT_FINGERPRINT: str = "789101"
CAT_FINGERPRINT_ARG: str = f"-f{CAT_FINGERPRINT}"
WALLET_ID: int = 1
WALLET_ID_ARG: str = f"-i{WALLET_ID}"
bytes32_hexstr = "0x6262626262626262626262626262626262626262626262626262626262626262"


def get_bytes32(bytes_index: int) -> bytes32:
    return bytes32([bytes_index] * 32)


STD_TX = TransactionRecord(
    confirmed_at_height=uint32(1),
    created_at_time=uint64(1234),
    to_puzzle_hash=get_bytes32(1),
    amount=uint64(12345678),
    fee_amount=uint64(1234567),
    confirmed=False,
    sent=uint32(0),
    spend_bundle=WalletSpendBundle([], G2Element()),
    additions=[Coin(get_bytes32(1), get_bytes32(2), uint64(12345678))],
    removals=[Coin(get_bytes32(2), get_bytes32(4), uint64(12345678))],
    wallet_id=uint32(1),
    sent_to=[],
    trade_id=None,
    type=uint32(TransactionType.OUTGOING_TX.value),
    name=get_bytes32(2),
    memos=[(get_bytes32(3), [bytes([4] * 32)])],
    valid_times=ConditionValidTimes(),
)


STD_UTX = UnsignedTransaction(TransactionInfo([]), SigningInstructions(KeyHints([], []), []))
