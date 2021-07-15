from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "cactus_harvester cactus_timelord_launcher cactus_timelord cactus_farmer cactus_full_node cactus_wallet".split(),
    "node": "cactus_full_node".split(),
    "harvester": "cactus_harvester".split(),
    "farmer": "cactus_harvester cactus_farmer cactus_full_node cactus_wallet".split(),
    "farmer-no-wallet": "cactus_harvester cactus_farmer cactus_full_node".split(),
    "farmer-only": "cactus_farmer".split(),
    "timelord": "cactus_timelord_launcher cactus_timelord cactus_full_node".split(),
    "timelord-only": "cactus_timelord".split(),
    "timelord-launcher-only": "cactus_timelord_launcher".split(),
    "wallet": "cactus_wallet cactus_full_node".split(),
    "wallet-only": "cactus_wallet".split(),
    "introducer": "cactus_introducer".split(),
    "simulator": "cactus_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
