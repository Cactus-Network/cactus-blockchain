from __future__ import annotations

import logging
from typing import ClassVar

from typing_extensions import Protocol

from cactus.protocols import harvester_protocol
from cactus.protocols.harvester_protocol import PlotSyncResponse
from cactus.protocols.outbound_message import Message
from cactus.protocols.protocol_message_types import ProtocolMessageTypes
from cactus.server.api_protocol import ApiMetadata, ApiProtocol
from cactus.server.ws_connection import WSCactusConnection


class HarvesterApiStub(ApiProtocol, Protocol):
    """Non-functional API stub for HarvesterAPI

    This is a protocol definition only - methods are not implemented and should
    never be called. Use the actual HarvesterAPI implementation at runtime.
    """

    log: logging.Logger
    metadata: ClassVar[ApiMetadata] = ApiMetadata()

    def ready(self) -> bool:
        """Check if the harvester is ready."""
        ...

    @metadata.request(peer_required=True)
    async def harvester_handshake(
        self, harvester_handshake: harvester_protocol.HarvesterHandshake, peer: WSCactusConnection
    ) -> None:
        """Handshake between the harvester and farmer."""
        ...

    @metadata.request(peer_required=True)
    async def new_signage_point_harvester(
        self, new_challenge: harvester_protocol.NewSignagePointHarvester2, peer: WSCactusConnection
    ) -> None:
        """Handle new signage point from farmer."""
        ...

    @metadata.request(reply_types=[ProtocolMessageTypes.respond_signatures])
    async def request_signatures(self, request: harvester_protocol.RequestSignatures) -> Message | None:
        """Handle signature request from farmer."""
        ...

    @metadata.request()
    async def request_plots(self, _: harvester_protocol.RequestPlots) -> Message:
        """Handle request for plot information."""
        ...

    @metadata.request()
    async def plot_sync_response(self, response: PlotSyncResponse) -> None:
        """Handle plot sync response."""
        ...
