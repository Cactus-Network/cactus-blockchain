from __future__ import annotations

import os
import sys

from setuptools import find_packages, setup

dependencies = [
    "aiofiles==23.2.1",  # Async IO for files
    "anyio==4.0.0",
    "boto3==1.34.25",  # AWS S3 for DL s3 plugin
    "chiavdf==1.1.0",  # timelord and vdf verification
    "chiabip158==1.3",  # bip158-style wallet filters
    "chiapos==2.0.3",  # proof of space
    "clvm==0.9.8",
    "clvm_tools==0.4.7",  # Currying, Program.to, other conveniences
    "chia_rs==0.2.15",
    "clvm-tools-rs==0.1.39",  # Rust implementation of clvm_tools' compiler
    "aiohttp==3.9.1",  # HTTP server for full node rpc
    "aiosqlite==0.19.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==4.1.2",  # Binary data management library
    "colorama==0.4.6",  # Colorizes terminal output
    "colorlog==6.7.0",  # Adds color to logs
    "concurrent-log-handler==0.9.24",  # Concurrently log and rotate logs
    "cryptography==41.0.5",  # Python cryptography library for TLS - keyring conflict
    "filelock==3.13.1",  # For reading and writing config multiprocess and multithread safely  (non-reentrant locks)
    "keyring==24.3.0",  # Store keys in MacOS Keychain, Windows Credential Locker
    "PyYAML==6.0.1",  # Used for config file format
    "setproctitle==1.3.3",  # Gives the cactus processes readable names
    "sortedcontainers==2.4.0",  # For maintaining sorted mempools
    "click==8.1.3",  # For the CLI
    "dnspython==2.4.2",  # Query DNS seeds
    "watchdog==2.2.0",  # Filesystem event watching - watches keyring.yaml
    "dnslib==0.9.23",  # dns lib
    "typing-extensions==4.8.0",  # typing backports like Protocol and TypedDict
    "zstd==1.5.5.1",
    "packaging==23.2",
    "psutil==5.9.4",
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "build==1.0.3",
    "coverage==7.3.2",
    "diff-cover==8.0.1",
    "pre-commit==3.5.0",
    "py3createtorrent==1.1.0",
    "pylint==3.0.2",
    "pytest==7.4.3",
    "pytest-cov==4.1.0",
    "pytest-mock==3.12.0",
    "pytest-xdist==3.5.0",
    "pyupgrade==3.15.0",
    "twine==4.0.2",
    "isort==5.12.0",
    "flake8==6.1.0",
    "mypy==1.7.0",
    "black==23.11.0",
    "lxml==4.9.3",
    "aiohttp_cors==0.7.0",  # For blackd
    "pyinstaller==5.13.0",
    "types-aiofiles==23.2.0.0",
    "types-cryptography==3.3.23.2",
    "types-pyyaml==6.0.12.12",
    "types-setuptools==68.2.0.1",
]

legacy_keyring_dependencies = [
    "keyrings.cryptfile==1.3.9",
]

kwargs = dict(
    name="cactus-blockchain",
    author="Dommer",
    author_email="dommer@cactus-network.network.net",
    description="Cactus blockchain full node, farmer, timelord, and wallet.",
    url="https://cactus-network.network.net/",
    license="Apache License",
    python_requires=">=3.8.1, <4",
    keywords="cactus blockchain node",
    install_requires=dependencies,
    extras_require=dict(
        dev=dev_dependencies,
        upnp=upnp_dependencies,
        legacy_keyring=legacy_keyring_dependencies,
    ),
    packages=find_packages(include=["build_scripts", "cactus", "cactus.*", "mozilla-ca"]),
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
            "cactus_data_layer_s3_plugin = cactus.data_layer.s3_plugin_service:run_server",
        ]
    },
    package_data={
        "": ["*.clsp", "*.clsp.hex", "*.clvm", "*.clib", "py.typed"],
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
