from setuptools import setup

dependencies = [
    "aiofiles==0.7.0",  # Async IO for files
    "blspy==1.0.15",  # Signature library
    "chiavdf==1.0.6",  # timelord and vdf verification
    "chiabip158==1.1",  # bip158-style wallet filters
    "chiapos==1.0.10",  # proof of space
    "clvm==0.9.7",
    "clvm_tools==0.4.5",  # Currying, Program.to, other conveniences
    "chia_rs==0.1.10",
    "clvm-tools-rs==0.1.19",  # Rust implementation of clvm_tools' compiler
    "aiohttp==3.8.1",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.9",  # Binary data management library
    "colorama==0.4.5",  # Colorizes terminal output
    "colorlog==6.6.0",  # Adds color to logs
    "concurrent-log-handler==0.9.19",  # Concurrently log and rotate logs
    "cryptography==36.0.2",  # Python cryptography library for TLS - keyring conflict
    "filelock==3.7.1",  # For reading and writing config multiprocess and multithread safely  (non-reentrant locks)
    "keyring==23.6.0",  # Store keys in MacOS Keychain, Windows Credential Locker
    "keyrings.cryptfile==1.3.4",  # Secure storage for keys on Linux (Will be replaced)
    #  "keyrings.cryptfile==1.3.8",  # Secure storage for keys on Linux (Will be replaced)
    #  See https://github.com/frispete/keyrings.cryptfile/issues/15
    "PyYAML==6.0",  # Used for config file format
    "setproctitle==1.2.3",  # Gives the cactus processes readable names
    "sortedcontainers==2.4.0",  # For maintaining sorted mempools
    # TODO: when moving to click 8 remove the pinning of black noted below
    "click==7.1.2",  # For the CLI
    "dnspython==2.2.0",  # Query DNS seeds
    "watchdog==2.1.9",  # Filesystem event watching - watches keyring.yaml
    "dnslib==0.9.17",  # dns lib
    "typing-extensions==4.3.0",  # typing backports like Protocol and TypedDict
    "zstd==1.5.0.4",
    "packaging==21.3",
    "psutil==5.9.1",
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    # TODO: remove after https://github.com/PyCQA/pylint/issues/7425 is resolved
    "astroid!=2.12.6, !=2.12.7",
    "build",
    "coverage",
    "pre-commit",
    "py3createtorrent",
    "pylint",
    "pytest",
    "pytest-asyncio>=0.18.1",  # require attribute 'fixture'
    "pytest-monitor; sys_platform == 'linux'",
    "pytest-xdist",
    "twine",
    "isort",
    "flake8",
    "mypy",
    # TODO: black 22.1.0 requires click>=8, remove this pin after updating to click 8
    "black==21.12b0",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
    "pyinstaller==5.3",
    "types-aiofiles",
    "types-click~=7.1",
    "types-cryptography",
    "types-pkg_resources",
    "types-pyyaml",
    "types-setuptools",
]

kwargs = dict(
    name="cactus-blockchain",
    author="Dommer",
    author_email="dommer@cactus-network.net",
    description="Cactus blockchain full node, farmer, timelord, and wallet.",
    url="https://cactus-network.net/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="cactus blockchain node",
    install_requires=dependencies,
    extras_require=dict(
        uvloop=["uvloop"],
        dev=dev_dependencies,
        upnp=upnp_dependencies,
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


if __name__ == "__main__":
    setup(**kwargs)  # type: ignore
