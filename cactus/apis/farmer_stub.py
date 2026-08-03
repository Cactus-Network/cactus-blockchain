from __future__ import annotations

import logging
from typing import ClassVar

from typing_extensions import Protocol

from cactus.protocols import farmer_protocol, harvester_protocol
from cactus.protocols.harvester_protocol import (
    PlotSyncDone,
    PlotSyncPathList,
    PlotSyncPlotList,
    PlotSyncStart,
    RespondPlots,
    RespondSignatures,
)
from cactus.protocols.outbound_message import Message
from cactus.server.api_protocol import ApiMetadata, ApiProtocol
from cactus.server.ws_connection import WSCactusConnection


class FarmerApiStub(ApiProtocol, Protocol):
    """Non-functional API stub for FarmerAPI

    This is a protocol definition only - methods are not implemented and should
    never be called. Use the actual FarmerAPI implementation at runtime.
    """

    log: logging.Logger
    # Create a concrete instance for decorators while keeping the ClassVar type hint for mypy
    metadata: ClassVar[ApiMetadata] = ApiMetadata()

    def ready(self) -> bool:
        """Check if the farmer is ready."""
        ...

    @metadata.request(peer_required=True)
    async def new_proof_of_space(
        self, new_proof_of_space: harvester_protocol.NewProofOfSpace, peer: WSCactusConnection
    ) -> None:
        """Handle new proof of space from harvester."""
        ...

    @metadata.request()
    async def respond_signatures(self, response: RespondSignatures) -> None:
        """Handle signature response from harvester."""
        ...

    @metadata.request()
    async def new_signage_point(self, new_signage_point: farmer_protocol.NewSignagePoint) -> None:
        """Handle new signage point from full node."""
        ...

    @metadata.request()
    async def request_signed_values(self, full_node_request: farmer_protocol.RequestSignedValues) -> Message | None:
        """Handle request for signed values from full node."""
        ...

    @metadata.request(peer_required=True)
    async def farming_info(self, request: farmer_protocol.FarmingInfo, peer: WSCactusConnection) -> None:
        """Handle farming info from full node."""
        ...

    @metadata.request(peer_required=True)
    async def respond_plots(self, _: RespondPlots, peer: WSCactusConnection) -> None:
        """Handle respond plots from harvester."""
        ...

    @metadata.request(peer_required=True)
    async def plot_sync_start(self, message: PlotSyncStart, peer: WSCactusConnection) -> None:
        """Handle plot sync start."""
        ...

    @metadata.request(peer_required=True)
    async def plot_sync_loaded(self, message: PlotSyncPlotList, peer: WSCactusConnection) -> None:
        """Handle plot sync loaded."""
        ...

    @metadata.request(peer_required=True)
    async def plot_sync_removed(self, message: PlotSyncPathList, peer: WSCactusConnection) -> None:
        """Handle plot sync removed."""
        ...

    @metadata.request(peer_required=True)
    async def plot_sync_invalid(self, message: PlotSyncPathList, peer: WSCactusConnection) -> None:
        """Handle plot sync invalid."""
        ...

    @metadata.request(peer_required=True)
    async def plot_sync_keys_missing(self, message: PlotSyncPathList, peer: WSCactusConnection) -> None:
        """Handle plot sync keys missing."""
        ...

    @metadata.request(peer_required=True)
    async def plot_sync_duplicates(self, message: PlotSyncPathList, peer: WSCactusConnection) -> None:
        """Handle plot sync duplicates."""
        ...

    @metadata.request(peer_required=True)
    async def plot_sync_done(self, message: PlotSyncDone, peer: WSCactusConnection) -> None:
        """Handle plot sync done."""
        ...
