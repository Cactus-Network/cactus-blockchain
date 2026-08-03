from __future__ import annotations

from cactus.full_node.full_node import FullNode
from cactus.full_node.full_node_api import FullNodeAPI
from cactus.full_node.full_node_rpc_api import FullNodeRpcApi
from cactus.server.start_service import Service

FullNodeService = Service[FullNode, FullNodeAPI, FullNodeRpcApi]
