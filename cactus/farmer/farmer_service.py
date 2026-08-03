from __future__ import annotations

from cactus.farmer.farmer import Farmer
from cactus.farmer.farmer_api import FarmerAPI
from cactus.farmer.farmer_rpc_api import FarmerRpcApi
from cactus.server.start_service import Service

FarmerService = Service[Farmer, FarmerAPI, FarmerRpcApi]
