import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("CACTUS_ROOT", "~/.cactus/mainnet"))).resolve()
