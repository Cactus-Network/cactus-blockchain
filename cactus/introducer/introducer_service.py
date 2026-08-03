from __future__ import annotations

from cactus.full_node.full_node_rpc_api import FullNodeRpcApi
from cactus.introducer.introducer import Introducer
from cactus.introducer.introducer_api import IntroducerAPI
from cactus.server.start_service import Service

IntroducerService = Service[Introducer, IntroducerAPI, FullNodeRpcApi]
