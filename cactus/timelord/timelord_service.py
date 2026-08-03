from __future__ import annotations

from cactus.server.start_service import Service
from cactus.timelord.timelord import Timelord
from cactus.timelord.timelord_api import TimelordAPI
from cactus.timelord.timelord_rpc_api import TimelordRpcApi

TimelordService = Service[Timelord, TimelordAPI, TimelordRpcApi]
