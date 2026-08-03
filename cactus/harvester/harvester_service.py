from __future__ import annotations

from cactus.harvester.harvester import Harvester
from cactus.harvester.harvester_api import HarvesterAPI
from cactus.harvester.harvester_rpc_api import HarvesterRpcApi
from cactus.server.start_service import Service

HarvesterService = Service[Harvester, HarvesterAPI, HarvesterRpcApi]
