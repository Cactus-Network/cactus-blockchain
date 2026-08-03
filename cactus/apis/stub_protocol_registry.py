from __future__ import annotations

from cactus.apis.farmer_stub import FarmerApiStub
from cactus.apis.full_node_stub import FullNodeApiStub
from cactus.apis.harvester_stub import HarvesterApiStub
from cactus.apis.introducer_stub import IntroducerApiStub
from cactus.apis.solver_stub import SolverApiStub
from cactus.apis.timelord_stub import TimelordApiStub
from cactus.apis.wallet_stub import WalletNodeApiStub
from cactus.protocols.outbound_message import NodeType
from cactus.server.api_protocol import ApiMetadata

StubMetadataRegistry: dict[NodeType, ApiMetadata] = {
    NodeType.FULL_NODE: FullNodeApiStub.metadata,
    NodeType.WALLET: WalletNodeApiStub.metadata,
    NodeType.INTRODUCER: IntroducerApiStub.metadata,
    NodeType.TIMELORD: TimelordApiStub.metadata,
    NodeType.FARMER: FarmerApiStub.metadata,
    NodeType.HARVESTER: HarvesterApiStub.metadata,
    NodeType.SOLVER: SolverApiStub.metadata,
}
