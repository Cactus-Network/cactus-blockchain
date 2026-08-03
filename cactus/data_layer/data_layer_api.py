from __future__ import annotations

import logging
from typing import TYPE_CHECKING, ClassVar, cast

from cactus.data_layer.data_layer import DataLayer
from cactus.server.api_protocol import ApiMetadata
from cactus.server.server import CactusServer


class DataLayerAPI:
    if TYPE_CHECKING:
        from cactus.server.api_protocol import ApiProtocol

        _protocol_check: ClassVar[ApiProtocol] = cast("DataLayerAPI", None)

    log: logging.Logger
    data_layer: DataLayer
    metadata: ClassVar[ApiMetadata] = ApiMetadata()

    def __init__(self, data_layer: DataLayer) -> None:
        self.log = logging.getLogger(__name__)
        self.data_layer = data_layer

    # def _set_state_changed_callback(self, callback: StateChangedProtocol) -> None:
    #     self.full_node.state_changed_callback = callback

    @property
    def server(self) -> CactusServer:
        return self.data_layer.server

    def ready(self) -> bool:
        return self.data_layer.initialized
