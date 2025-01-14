from __future__ import annotations

import pathlib
import sys
from typing import Any, Dict, Optional, Set

from cactus.consensus.constants import ConsensusConstants, replace_str_to_bytes
from cactus.consensus.default_constants import DEFAULT_CONSTANTS
from cactus.harvester.harvester import Harvester
from cactus.harvester.harvester_api import HarvesterAPI
from cactus.rpc.harvester_rpc_api import HarvesterRpcApi
from cactus.server.outbound_message import NodeType
from cactus.server.signal_handlers import SignalHandlers
from cactus.server.start_service import RpcInfo, Service, async_run
from cactus.types.aliases import HarvesterService
from cactus.types.peer_info import UnresolvedPeerInfo
from cactus.util.cactus_logging import initialize_service_logging
from cactus.util.config import get_unresolved_peer_infos, load_config, load_config_cli
from cactus.util.default_root import DEFAULT_ROOT_PATH

# See: https://bugs.python.org/issue29288
"".encode("idna")

SERVICE_NAME = "harvester"


def create_harvester_service(
    root_path: pathlib.Path,
    config: Dict[str, Any],
    consensus_constants: ConsensusConstants,
    farmer_peers: Set[UnresolvedPeerInfo],
    connect_to_daemon: bool = True,
) -> HarvesterService:
    service_config = config[SERVICE_NAME]

    overrides = service_config["network_overrides"]["constants"][service_config["selected_network"]]
    updated_constants = replace_str_to_bytes(consensus_constants, **overrides)

    harvester = Harvester(root_path, service_config, updated_constants)
    peer_api = HarvesterAPI(harvester)
    network_id = service_config["selected_network"]
    rpc_info: Optional[RpcInfo[HarvesterRpcApi]] = None
    if service_config["start_rpc_server"]:
        rpc_info = (HarvesterRpcApi, service_config["rpc_port"])
    return Service(
        root_path=root_path,
        config=config,
        node=harvester,
        peer_api=peer_api,
        node_type=NodeType.HARVESTER,
        advertised_port=None,
        service_name=SERVICE_NAME,
        connect_peers=farmer_peers,
        network_id=network_id,
        rpc_info=rpc_info,
        connect_to_daemon=connect_to_daemon,
    )


async def async_main() -> int:
    # TODO: refactor to avoid the double load
    config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    service_config = load_config_cli(DEFAULT_ROOT_PATH, "config.yaml", SERVICE_NAME)
    config[SERVICE_NAME] = service_config
    initialize_service_logging(service_name=SERVICE_NAME, config=config)
    farmer_peers = get_unresolved_peer_infos(service_config, NodeType.FARMER)
    service = create_harvester_service(DEFAULT_ROOT_PATH, config, DEFAULT_CONSTANTS, farmer_peers)
    async with SignalHandlers.manage() as signal_handlers:
        await service.setup_process_global_state(signal_handlers=signal_handlers)
        await service.run()

    return 0


def main() -> int:
    return async_run(async_main())


if __name__ == "__main__":
    sys.exit(main())
