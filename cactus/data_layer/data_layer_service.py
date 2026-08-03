from __future__ import annotations

from cactus.data_layer.data_layer import DataLayer
from cactus.data_layer.data_layer_api import DataLayerAPI
from cactus.data_layer.data_layer_rpc_api import DataLayerRpcApi
from cactus.server.start_service import Service

DataLayerService = Service[DataLayer, DataLayerAPI, DataLayerRpcApi]
