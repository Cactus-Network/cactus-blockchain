from __future__ import annotations

import os
import sys

from setuptools import setup

dependencies = [
    "aiofiles==23.1.0",  # Async IO for files
    "anyio==3.6.2",
    "blspy==1.0.16",  # Signature library
    "chiavdf==1.0.8",  # timelord and vdf verification
    "chiabip158==1.2",  # bip158-style wallet filters
    "chiapos==1.0.11",  # proof of space
    "clvm==0.9.7",
    "clvm_tools==0.4.6",  # Currying, Program.to, other conveniences
    "chia_rs==0.2.5",
    "clvm-tools-rs==0.1.30",  # Rust implementation of clvm_tools' compiler
    "aiohttp==3.8.4",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==4.0.1",  # Binary data management library
    "colorama==0.4.6",  # Colorizes terminal output
    "colorlog==6.7.0",  # Adds color to logs
    "concurrent-log-handler==0.9.20",  # Concurrently log and rotate logs
    "cryptography==39.0.1",  # Python cryptography library for TLS - keyring conflict
    "filelock==3.9.0",  # For reading and writing config multiprocess and multithread safely  (non-reentrant locks)
    "keyring==23.13.1",  # Store keys in MacOS Keychain, Windows Credential Locker
    "PyYAML==6.0",  # Used for config file format
    "setproctitle==1.3.2",  # Gives the cactus processes readable names
    "sortedcontainers==2.4.0",  # For maintaining sorted mempools
    "click==8.1.3",  # For the CLI
    "dnspython==2.3.0",  # Query DNS seeds
    "watchdog==2.2.0",  # Filesystem event watching - watches keyring.yaml
    "dnslib==0.9.23",  # dns lib
    "typing-extensions==4.5.0",  # typing backports like Protocol and TypedDict
    "zstd==1.5.4.0",
    "packaging==23.0",
    "psutil==5.9.4",
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "build",
    "coverage",
    "diff-cover",
    "pre-commit",
    "py3createtorrent",
    "pylint",
    "pytest",
    # TODO: do not checkpoint to main
    "pytest-asyncio==0.20.3",  # require attribute 'fixture'
    "pytest-cov",
    "pytest-monitor; sys_platform == 'linux'",
    "pytest-xdist",
    "twine",
    "isort",
    "flake8",
    "mypy",
    "black==22.10.0",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
    "pyinstaller==5.8.0",
    "types-aiofiles",
    "types-cryptography",
    "types-pkg_resources",
    "types-pyyaml",
    "types-setuptools",
]

legacy_keyring_dependencies = [
    "keyrings.cryptfile==1.3.9",
]

kwargs = dict(
    name="cactus-blockchain",
    author="Mariano Sorgente",
    author_email="mariano@cactus-network.net",
    description="Cactus blockchain full node, farmer, timelord, and wallet.",
    url="https://cactus-network.net/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="cactus blockchain node",
    install_requires=dependencies,
    extras_require=dict(
        dev=dev_dependencies,
        upnp=upnp_dependencies,
        legacy_keyring=legacy_keyring_dependencies,
    ),
    packages=[
        "build_scripts",
        "cactus",
        "cactus.cmds",
        "cactus.clvm",
        "cactus.consensus",
        "cactus.daemon",
        "cactus.data_layer",
        "cactus.full_node",
        "cactus.timelord",
        "cactus.farmer",
        "cactus.harvester",
        "cactus.introducer",
        "cactus.plot_sync",
        "cactus.plotters",
        "cactus.plotting",
        "cactus.pools",
        "cactus.protocols",
        "cactus.rpc",
        "cactus.seeder",
        "cactus.server",
        "cactus.simulator",
        "cactus.types.blockchain_format",
        "cactus.types",
        "cactus.util",
        "cactus.wallet",
        "cactus.wallet.db_wallet",
        "cactus.wallet.puzzles",
        "cactus.wallet.cat_wallet",
        "cactus.wallet.did_wallet",
        "cactus.wallet.nft_wallet",
        "cactus.wallet.settings",
        "cactus.wallet.trading",
        "cactus.wallet.util",
        "cactus.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "cactus = cactus.cmds.cactus:main",
            "cactus_daemon = cactus.daemon.server:main",
            "cactus_wallet = cactus.server.start_wallet:main",
            "cactus_full_node = cactus.server.start_full_node:main",
            "cactus_harvester = cactus.server.start_harvester:main",
            "cactus_farmer = cactus.server.start_farmer:main",
            "cactus_introducer = cactus.server.start_introducer:main",
            "cactus_crawler = cactus.seeder.start_crawler:main",
            "cactus_seeder = cactus.seeder.dns_server:main",
            "cactus_timelord = cactus.server.start_timelord:main",
            "cactus_timelord_launcher = cactus.timelord.timelord_launcher:main",
            "cactus_full_node_simulator = cactus.simulator.start_simulator:main",
            "cactus_data_layer = cactus.server.start_data_layer:main",
            "cactus_data_layer_http = cactus.data_layer.data_layer_server:main",
        ]
    },
    package_data={
        "cactus": ["pyinstaller.spec"],
        "": ["*.clvm", "*.clvm.hex", "*.clib", "*.clinc", "*.clsp", "py.typed"],
        "cactus.util": ["initial-*.yaml", "english.txt"],
        "cactus.ssl": ["cactus_ca.crt", "cactus_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    project_urls={
        "Source": "https://github.com/Cactus-Network/cactus-blockchain/",
        "Changelog": "https://github.com/Cactus-Network/cactus-blockchain/blob/main/CHANGELOG.md",
    },
)

if "setup_file" in sys.modules:
    # include dev deps in regular deps when run in snyk
    dependencies.extend(dev_dependencies)

if len(os.environ.get("CACTUS_SKIP_SETUP", "")) < 1:
    setup(**kwargs)  # type: ignore
