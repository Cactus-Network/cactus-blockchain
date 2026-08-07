from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from cactus.util.config import load_config, selected_network_address_prefix
from cactus.util.default_root import DEFAULT_ROOT_PATH

MOJO_PER_CACTUS = 1_000_000_000_000

DEFAULT_DSN = "postgresql:///cactus_explorer"


@dataclass(frozen=True)
class Settings:
    """Everything the indexer and API need, derived from the node's own config.yaml.

    Overridable via environment:
      CACTUS_ROOT   node root (default ~/.cactus/mainnet, honoured by cactus itself)
      EXPLORER_DSN  postgres DSN for the explorer index
    """

    root_path: Path
    net_config: Dict[str, Any]
    network: str
    node_db_path: Path
    dsn: str
    address_prefix: str
    self_hostname: str
    rpc_port: int

    @classmethod
    def load(cls) -> Settings:
        root_env = os.environ.get("CACTUS_ROOT")
        root_path = Path(root_env).expanduser().resolve() if root_env else DEFAULT_ROOT_PATH
        net_config = load_config(root_path, "config.yaml")
        network = net_config["selected_network"]

        # e.g. "db/blockchain_v2_CHALLENGE.sqlite" -> "db/blockchain_v2_mainnet.sqlite"
        db_rel = net_config["full_node"]["database_path"].replace("CHALLENGE", network)

        return cls(
            root_path=root_path,
            net_config=net_config,
            network=network,
            node_db_path=root_path / db_rel,
            dsn=os.environ.get("EXPLORER_DSN", DEFAULT_DSN),
            address_prefix=selected_network_address_prefix(net_config),
            self_hostname=net_config["self_hostname"],
            rpc_port=int(net_config["full_node"]["rpc_port"]),
        )
