import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("CACTUS_ROOT", "~/.cactus/mainnet"))).resolve()
STANDALONE_ROOT_PATH = Path(
    os.path.expanduser(os.getenv("CACTUS_STANDALONE_WALLET_ROOT", "~/.cactus/standalone_wallet"))
).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("CACTUS_KEYS_ROOT", "~/.cactus_keys"))).resolve()
