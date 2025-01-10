from __future__ import annotations

from cactus.data_layer.data_layer import DataLayer
from cactus.data_layer.data_layer_api import DataLayerAPI
from cactus.farmer.farmer import Farmer
from cactus.farmer.farmer_api import FarmerAPI
from cactus.full_node.full_node import FullNode
from cactus.full_node.full_node_api import FullNodeAPI
from cactus.harvester.harvester import Harvester
from cactus.harvester.harvester_api import HarvesterAPI
from cactus.introducer.introducer import Introducer
from cactus.introducer.introducer_api import IntroducerAPI
from cactus.rpc.crawler_rpc_api import CrawlerRpcApi
from cactus.rpc.data_layer_rpc_api import DataLayerRpcApi
from cactus.rpc.farmer_rpc_api import FarmerRpcApi
from cactus.rpc.full_node_rpc_api import FullNodeRpcApi
from cactus.rpc.harvester_rpc_api import HarvesterRpcApi
from cactus.rpc.timelord_rpc_api import TimelordRpcApi
from cactus.rpc.wallet_rpc_api import WalletRpcApi
from cactus.seeder.crawler import Crawler
from cactus.seeder.crawler_api import CrawlerAPI
from cactus.server.start_service import Service
from cactus.timelord.timelord import Timelord
from cactus.timelord.timelord_api import TimelordAPI
from cactus.wallet.wallet_node import WalletNode
from cactus.wallet.wallet_node_api import WalletNodeAPI

CrawlerService = Service[Crawler, CrawlerAPI, CrawlerRpcApi]
DataLayerService = Service[DataLayer, DataLayerAPI, DataLayerRpcApi]
FarmerService = Service[Farmer, FarmerAPI, FarmerRpcApi]
FullNodeService = Service[FullNode, FullNodeAPI, FullNodeRpcApi]
HarvesterService = Service[Harvester, HarvesterAPI, HarvesterRpcApi]
IntroducerService = Service[Introducer, IntroducerAPI, FullNodeRpcApi]
TimelordService = Service[Timelord, TimelordAPI, TimelordRpcApi]
WalletService = Service[WalletNode, WalletNodeAPI, WalletRpcApi]
