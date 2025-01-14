from __future__ import annotations

from typing import List, Tuple

import pytest

from cactus._tests.util.setup_nodes import OldSimulatorsAndWallets
from cactus.cmds.units import units
from cactus.server.server import CactusServer
from cactus.simulator.block_tools import BlockTools
from cactus.simulator.full_node_simulator import FullNodeSimulator
from cactus.types.peer_info import PeerInfo
from cactus.util.ints import uint64
from cactus.wallet.util.tx_config import DEFAULT_TX_CONFIG
from cactus.wallet.wallet_node import WalletNode


@pytest.mark.anyio
@pytest.mark.parametrize(argnames="count", argvalues=[0, 1, 2, 5, 10])
@pytest.mark.parametrize(argnames="guarantee_transaction_blocks", argvalues=[False, True])
async def test_simulation_farm_blocks_to_puzzlehash(
    count: int,
    guarantee_transaction_blocks: bool,
    simulator_and_wallet: Tuple[List[FullNodeSimulator], List[Tuple[WalletNode, CactusServer]], BlockTools],
) -> None:
    [[full_node_api], _, _] = simulator_and_wallet

    # Starting at the beginning.
    assert full_node_api.full_node.blockchain.get_peak_height() is None

    await full_node_api.farm_blocks_to_puzzlehash(
        count=count, guarantee_transaction_blocks=guarantee_transaction_blocks
    )

    # The requested number of blocks had been processed.
    expected_height = None if count == 0 else count
    assert full_node_api.full_node.blockchain.get_peak_height() == expected_height


@pytest.mark.anyio
@pytest.mark.parametrize(argnames="count", argvalues=[0, 1, 2, 5, 10])
async def test_simulation_farm_blocks_to_wallet(
    count: int,
    simulator_and_wallet: Tuple[List[FullNodeSimulator], List[Tuple[WalletNode, CactusServer]], BlockTools],
) -> None:
    [[full_node_api], [[wallet_node, wallet_server]], _] = simulator_and_wallet

    await wallet_server.start_client(PeerInfo("127.0.0.1", full_node_api.server.get_port()), None)

    # Avoiding an attribute error below.
    assert wallet_node.wallet_state_manager is not None

    wallet = wallet_node.wallet_state_manager.main_wallet

    # Starting at the beginning.
    assert full_node_api.full_node.blockchain.get_peak_height() is None

    rewards = await full_node_api.farm_blocks_to_wallet(count=count, wallet=wallet)

    # The expected rewards have been received and confirmed.
    unconfirmed_balance = await wallet.get_unconfirmed_balance()
    confirmed_balance = await wallet.get_confirmed_balance()
    assert [unconfirmed_balance, confirmed_balance] == [rewards, rewards]


@pytest.mark.anyio
@pytest.mark.parametrize(
    argnames=["amount", "coin_count"],
    argvalues=[
        [0, 0],
        [1, 2],
        [(2 * units["cactus"]) - 1, 2],
        [2 * units["cactus"], 2],
        [(2 * units["cactus"]) + 1, 4],
        [3 * units["cactus"], 4],
        [10 * units["cactus"], 10],
    ],
)
async def test_simulation_farm_rewards_to_wallet(
    amount: int,
    coin_count: int,
    simulator_and_wallet: Tuple[List[FullNodeSimulator], List[Tuple[WalletNode, CactusServer]], BlockTools],
) -> None:
    [[full_node_api], [[wallet_node, wallet_server]], _] = simulator_and_wallet

    await wallet_server.start_client(PeerInfo("127.0.0.1", full_node_api.server.get_port()), None)

    # Avoiding an attribute error below.
    assert wallet_node.wallet_state_manager is not None

    wallet = wallet_node.wallet_state_manager.main_wallet

    rewards = await full_node_api.farm_rewards_to_wallet(amount=amount, wallet=wallet)

    # At least the requested amount was farmed.
    assert rewards >= amount

    # The rewards amount is both received and confirmed.
    unconfirmed_balance = await wallet.get_unconfirmed_balance()
    confirmed_balance = await wallet.get_confirmed_balance()
    assert [unconfirmed_balance, confirmed_balance] == [rewards, rewards]

    # The expected number of coins were received.
    all_coin_records = await wallet.wallet_state_manager.coin_store.get_unspent_coins_for_wallet(wallet.id())
    assert len(all_coin_records) == coin_count


@pytest.mark.anyio
async def test_wait_transaction_records_entered_mempool(
    simulator_and_wallet: Tuple[List[FullNodeSimulator], List[Tuple[WalletNode, CactusServer]], BlockTools],
) -> None:
    repeats = 50
    tx_amount = 1
    [[full_node_api], [[wallet_node, wallet_server]], _] = simulator_and_wallet

    await wallet_server.start_client(PeerInfo("127.0.0.1", full_node_api.server.get_port()), None)

    # Avoiding an attribute hint issue below.
    assert wallet_node.wallet_state_manager is not None

    wallet = wallet_node.wallet_state_manager.main_wallet

    # generate some coins for repetitive testing
    await full_node_api.farm_rewards_to_wallet(amount=repeats * tx_amount, wallet=wallet)
    coins = await full_node_api.create_coins_with_amounts(amounts=[uint64(tx_amount)] * repeats, wallet=wallet)
    assert len(coins) == repeats

    # repeating just to try to expose any flakiness
    for coin in coins:
        async with wallet.wallet_state_manager.new_action_scope(DEFAULT_TX_CONFIG, push=True) as action_scope:
            await wallet.generate_signed_transaction(
                amount=uint64(tx_amount),
                puzzle_hash=await wallet_node.wallet_state_manager.main_wallet.get_new_puzzlehash(),
                action_scope=action_scope,
                coins={coin},
            )

        [tx] = action_scope.side_effects.transactions
        await full_node_api.wait_transaction_records_entered_mempool(records=action_scope.side_effects.transactions)
        assert tx.spend_bundle is not None
        assert full_node_api.full_node.mempool_manager.get_spendbundle(tx.spend_bundle.name()) is not None


@pytest.mark.anyio
async def test_process_transaction_records(
    simulator_and_wallet: Tuple[List[FullNodeSimulator], List[Tuple[WalletNode, CactusServer]], BlockTools],
) -> None:
    repeats = 50
    tx_amount = 1
    [[full_node_api], [[wallet_node, wallet_server]], _] = simulator_and_wallet

    await wallet_server.start_client(PeerInfo("127.0.0.1", full_node_api.server.get_port()), None)

    # Avoiding an attribute hint issue below.
    assert wallet_node.wallet_state_manager is not None

    wallet = wallet_node.wallet_state_manager.main_wallet

    # generate some coins for repetitive testing
    await full_node_api.farm_rewards_to_wallet(amount=repeats * tx_amount, wallet=wallet)
    coins = await full_node_api.create_coins_with_amounts(amounts=[uint64(tx_amount)] * repeats, wallet=wallet)
    assert len(coins) == repeats

    # repeating just to try to expose any flakiness
    for coin in coins:
        async with wallet.wallet_state_manager.new_action_scope(DEFAULT_TX_CONFIG, push=True) as action_scope:
            await wallet.generate_signed_transaction(
                amount=uint64(tx_amount),
                puzzle_hash=await wallet_node.wallet_state_manager.main_wallet.get_new_puzzlehash(),
                action_scope=action_scope,
                coins={coin},
            )

        await full_node_api.process_transaction_records(records=action_scope.side_effects.transactions)
        assert full_node_api.full_node.coin_store.get_coin_record(coin.name()) is not None


@pytest.mark.anyio
@pytest.mark.parametrize(
    argnames="amounts",
    argvalues=[
        *[pytest.param([uint64(1)] * n, id=f"1 mojo x {n}") for n in [0, 1, 10, 49, 51, 103]],
        *[
            pytest.param(list(uint64(x) for x in range(1, n + 1)), id=f"incrementing x {n}")
            for n in [1, 10, 49, 51, 103]
        ],
    ],
)
async def test_create_coins_with_amounts(
    self_hostname: str, amounts: List[uint64], simulator_and_wallet: OldSimulatorsAndWallets
) -> None:
    [[full_node_api], [[wallet_node, wallet_server]], _] = simulator_and_wallet
    await wallet_server.start_client(PeerInfo(self_hostname, full_node_api.server.get_port()), None)
    # Avoiding an attribute hint issue below.
    assert wallet_node.wallet_state_manager is not None
    wallet = wallet_node.wallet_state_manager.main_wallet
    await full_node_api.farm_rewards_to_wallet(amount=sum(amounts), wallet=wallet)
    # Get some more coins.  The creator helper doesn't get you all the coins you
    # need yet.
    await full_node_api.farm_blocks_to_wallet(count=2, wallet=wallet, timeout=30)
    coins = await full_node_api.create_coins_with_amounts(amounts=amounts, wallet=wallet, timeout=60)
    assert sorted(coin.amount for coin in coins) == sorted(amounts)


@pytest.mark.anyio
@pytest.mark.parametrize(
    argnames="amounts",
    argvalues=[
        [0],
        [5, -5],
        [4, 0],
    ],
    ids=lambda amounts: ", ".join(str(amount) for amount in amounts),
)
async def test_create_coins_with_invalid_amounts_raises(
    amounts: List[int],
    simulator_and_wallet: Tuple[List[FullNodeSimulator], List[Tuple[WalletNode, CactusServer]], BlockTools],
) -> None:
    [[full_node_api], [[wallet_node, wallet_server]], _] = simulator_and_wallet

    await wallet_server.start_client(PeerInfo("127.0.0.1", full_node_api.server.get_port()), None)

    # Avoiding an attribute hint issue below.backoff_times
    assert wallet_node.wallet_state_manager is not None

    wallet = wallet_node.wallet_state_manager.main_wallet

    with pytest.raises(Exception, match="Coins must have a positive value"):
        # Passing integers since the point is to test invalid values including
        # negatives that will not fit in a uint64.
        await full_node_api.create_coins_with_amounts(
            amounts=amounts,  # type: ignore[arg-type]
            wallet=wallet,
        )