import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("CACTUS_ROOT", "~/.cactus/mainnet"))).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("CACTUS_KEYS_ROOT", "~/.cactus_keys"))).resolve()
