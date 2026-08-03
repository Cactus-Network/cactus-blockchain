from __future__ import annotations

import pytest

from cactus import __version__
from cactus.daemon.client import connect_to_daemon
from cactus.daemon.server import WebSocketServer
from cactus.simulator.block_tools import BlockTools


@pytest.mark.anyio
async def test_get_version_rpc(get_daemon: WebSocketServer, bt: BlockTools) -> None:
    ws_server = get_daemon
    config = bt.config
    client = await connect_to_daemon(
        config["self_hostname"],
        config["daemon_port"],
        50 * 1000 * 1000,
        bt.get_daemon_ssl_context(),
        heartbeat=config["daemon_heartbeat"],
    )
    response = await client.get_version()

    assert response["data"]["success"]
    assert response["data"]["version"] == __version__
    await ws_server.stop()
