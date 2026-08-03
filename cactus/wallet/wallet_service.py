from __future__ import annotations

from cactus.server.start_service import Service
from cactus.wallet.wallet_node import WalletNode
from cactus.wallet.wallet_node_api import WalletNodeAPI
from cactus.wallet.wallet_rpc_api import WalletRpcApi

WalletService = Service[WalletNode, WalletNodeAPI, WalletRpcApi]
