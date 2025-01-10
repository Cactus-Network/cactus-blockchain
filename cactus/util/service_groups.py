from __future__ import annotations

from typing import Dict, Generator, Iterable, KeysView

SERVICES_FOR_GROUP: Dict[str, list[str]] = {
    "all": [
        "cactus_harvester",
        "cactus_timelord_launcher",
        "cactus_timelord",
        "cactus_farmer",
        "cactus_full_node",
        "cactus_wallet",
        "cactus_data_layer",
        "cactus_data_layer_http",
    ],
    "daemon": [],
    # TODO: should this be `data_layer`?
    "data": ["cactus_wallet", "cactus_data_layer"],
    "data_layer_http": ["cactus_data_layer_http"],
    "node": ["cactus_full_node"],
    "harvester": ["cactus_harvester"],
    "farmer": ["cactus_harvester", "cactus_farmer", "cactus_full_node", "cactus_wallet"],
    "farmer-no-wallet": ["cactus_harvester", "cactus_farmer", "cactus_full_node"],
    "farmer-only": ["cactus_farmer"],
    "timelord": ["cactus_timelord_launcher", "cactus_timelord", "cactus_full_node"],
    "timelord-only": ["cactus_timelord"],
    "timelord-launcher-only": ["cactus_timelord_launcher"],
    "wallet": ["cactus_wallet"],
    "introducer": ["cactus_introducer"],
    "simulator": ["cactus_full_node_simulator"],
    "crawler": ["cactus_crawler"],
    "seeder": ["cactus_crawler", "cactus_seeder"],
    "seeder-only": ["cactus_seeder"],
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups: Iterable[str]) -> Generator[str, None, None]:
    for group in groups:
        yield from SERVICES_FOR_GROUP[group]


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
