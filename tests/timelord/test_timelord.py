from __future__ import annotations

import pytest

from cactus.server.start_service import Service
from cactus.timelord.timelord import Timelord
from cactus.timelord.timelord_api import TimelordAPI


@pytest.mark.anyio
async def test_timelord_has_no_server(timelord_service: Service[Timelord, TimelordAPI]) -> None:
    timelord_server = timelord_service._node.server
    assert timelord_server.webserver is None
