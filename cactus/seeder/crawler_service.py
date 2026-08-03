from __future__ import annotations

from cactus.seeder.crawler import Crawler
from cactus.seeder.crawler_api import CrawlerAPI
from cactus.seeder.crawler_rpc_api import CrawlerRpcApi
from cactus.server.start_service import Service

CrawlerService = Service[Crawler, CrawlerAPI, CrawlerRpcApi]
