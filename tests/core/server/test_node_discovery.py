from __future__ import annotations

from logging import Logger
from typing import Tuple

import pytest

from cactus.full_node.full_node_api import FullNodeAPI
from cactus.server.node_discovery import FullNodeDiscovery
from cactus.server.peer_store_resolver import PeerStoreResolver
from cactus.server.server import CactusServer
from cactus.simulator.block_tools import BlockTools
from cactus.util.default_root import SIMULATOR_ROOT_PATH


@pytest.mark.asyncio
async def test_enable_private_networks(
    two_nodes: Tuple[FullNodeAPI, FullNodeAPI, CactusServer, CactusServer, BlockTools],
) -> None:
    cactus_server = two_nodes[2]

    # Missing `enable_private_networks` config entry in introducer_peer should default to False for back compat
    discovery0 = FullNodeDiscovery(
        cactus_server,
        0,
        PeerStoreResolver(
            SIMULATOR_ROOT_PATH,
            cactus_server.config,
            selected_network=cactus_server.config["selected_network"],
            peers_file_path_key="peers_file_path",
            legacy_peer_db_path_key="db/peer_table_node.sqlite",
            default_peers_file_path="db/peers.dat",
        ),
        {"host": "introducer.cactus-network.net", "port": 11444},
        [],
        0,
        cactus_server.config["selected_network"],
        None,
        Logger("node_discovery_tests"),
    )
    assert discovery0 is not None
    assert discovery0.enable_private_networks is False
    await discovery0.initialize_address_manager()
    assert discovery0.address_manager is not None
    assert discovery0.address_manager.allow_private_subnets is False

    # Test with enable_private_networks set to False in Config
    discovery1 = FullNodeDiscovery(
        cactus_server,
        0,
        PeerStoreResolver(
            SIMULATOR_ROOT_PATH,
            cactus_server.config,
            selected_network=cactus_server.config["selected_network"],
            peers_file_path_key="peers_file_path",
            legacy_peer_db_path_key="db/peer_table_node.sqlite",
            default_peers_file_path="db/peers.dat",
        ),
        {"host": "introducer.cactus-network.net", "port": 11444, "enable_private_networks": False},
        [],
        0,
        cactus_server.config["selected_network"],
        None,
        Logger("node_discovery_tests"),
    )
    assert discovery1 is not None
    assert discovery1.enable_private_networks is False
    await discovery1.initialize_address_manager()
    assert discovery1.address_manager is not None
    assert discovery1.address_manager.allow_private_subnets is False

    # Test with enable_private_networks set to True in Config
    discovery2 = FullNodeDiscovery(
        cactus_server,
        0,
        PeerStoreResolver(
            SIMULATOR_ROOT_PATH,
            cactus_server.config,
            selected_network=cactus_server.config["selected_network"],
            peers_file_path_key="peers_file_path",
            legacy_peer_db_path_key="db/peer_table_node.sqlite",
            default_peers_file_path="db/peers.dat",
        ),
        {"host": "introducer.cactus-network.net", "port": 11444, "enable_private_networks": True},
        [],
        0,
        cactus_server.config["selected_network"],
        None,
        Logger("node_discovery_tests"),
    )
    assert discovery2 is not None
    assert discovery2.enable_private_networks is True
    await discovery2.initialize_address_manager()
    assert discovery2.address_manager is not None
    assert discovery2.address_manager.allow_private_subnets is True
