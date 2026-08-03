# Package: utils

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("CACTUS_ROOT", "~/.cactus/mainnet"))).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("CACTUS_KEYS_ROOT", "~/.cactus_keys"))).resolve()

SIMULATOR_ROOT_PATH = Path(os.path.expanduser(os.getenv("CACTUS_SIMULATOR_ROOT", "~/.cactus/simulator"))).resolve()


def resolve_root_path(*, override: Path | None) -> Path:
    candidates = [
        override,
        os.environ.get("CACTUS_ROOT"),
        "~/.cactus/mainnet",
    ]

    for candidate in candidates:
        if candidate is not None:
            return Path(candidate).expanduser().resolve()

    raise RuntimeError("unreachable: last candidate is hardcoded to be found")
