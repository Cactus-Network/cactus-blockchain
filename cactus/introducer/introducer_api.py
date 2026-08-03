from __future__ import annotations

import logging
from typing import TYPE_CHECKING, ClassVar

from chia_rs.sized_ints import uint64

from cactus.introducer.introducer import Introducer
from cactus.protocols.introducer_protocol import RequestPeersIntroducer, RespondPeersIntroducer
from cactus.protocols.outbound_message import Message, make_msg
from cactus.protocols.protocol_message_types import ProtocolMessageTypes
from cactus.rpc.rpc_server import StateChangedProtocol
from cactus.server.api_protocol import ApiMetadata
from cactus.server.ws_connection import WSCactusConnection
from cactus.types.peer_info import TimestampedPeerInfo


class IntroducerAPI:
    if TYPE_CHECKING:
        from cactus.apis.introducer_stub import IntroducerApiStub

        # Verify this class implements the IntroducerApiStub protocol
        def _protocol_check(self: IntroducerAPI) -> IntroducerApiStub:
            return self

    log: logging.Logger
    introducer: Introducer
    metadata: ClassVar[ApiMetadata] = ApiMetadata()

    def __init__(self, introducer: Introducer) -> None:
        self.log = logging.getLogger(__name__)
        self.introducer = introducer

    def ready(self) -> bool:
        return True

    def _set_state_changed_callback(self, callback: StateChangedProtocol) -> None:
        pass

    @metadata.request(peer_required=True)
    async def request_peers_introducer(
        self,
        request: RequestPeersIntroducer,
        peer: WSCactusConnection,
    ) -> Message | None:
        max_peers = self.introducer.max_peers_to_send
        if self.introducer.server is None or self.introducer.server.introducer_peers is None:
            return None
        rawpeers = self.introducer.server.introducer_peers.get_peers(
            max_peers * 5, True, self.introducer.recent_peer_threshold
        )

        peers = []
        for r_peer in rawpeers:
            if r_peer.vetted <= 0:
                continue

            if r_peer.host == peer.peer_info.host and r_peer.port == peer.peer_server_port:
                continue
            peer_without_timestamp = TimestampedPeerInfo(
                r_peer.host,
                r_peer.port,
                uint64(0),
            )
            peers.append(peer_without_timestamp)

            if len(peers) >= max_peers:
                break

        if len(peers) < max_peers:
            peers_needed = max_peers - len(peers)
            self.introducer.log.info(f"Querying dns servers for {peers_needed} peers")
            extra_peers = await self.introducer.get_peers_from_dns(peers_needed)
            self.introducer.log.info(f"Received {len(extra_peers)} peers from dns server")
            peers.extend(extra_peers)

        self.introducer.log.info(f"Sending vetted {peers}")

        msg = make_msg(ProtocolMessageTypes.respond_peers_introducer, RespondPeersIntroducer(peers))
        return msg
