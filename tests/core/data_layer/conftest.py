import contextlib
import os
import pathlib
import subprocess
import sys
import sysconfig
import time
from typing import Any, AsyncIterable, Awaitable, Callable, Dict, Iterator, List

import aiosqlite
import pytest
import pytest_asyncio

# https://github.com/pytest-dev/pytest/issues/7469
from _pytest.fixtures import SubRequest

from cactus.data_layer.data_layer_util import NodeType, Status
from cactus.data_layer.data_store import DataStore
from cactus.types.blockchain_format.tree_hash import bytes32
from cactus.util.db_wrapper import DBWrapper
from tests.core.data_layer.util import (
    CactusRoot,
    Example,
    add_0123_example,
    add_01234567_example,
    create_valid_node_values,
)

# TODO: These are more general than the data layer and should either move elsewhere or
#       be replaced with an existing common approach.  For now they can at least be
#       shared among the data layer test files.


@pytest.fixture(name="scripts_path", scope="session")
def scripts_path_fixture() -> pathlib.Path:
    scripts_string = sysconfig.get_path("scripts")
    if scripts_string is None:
        raise Exception("These tests depend on the scripts path existing")

    return pathlib.Path(scripts_string)


@pytest.fixture(name="cactus_root", scope="function")
def cactus_root_fixture(tmp_path: pathlib.Path, scripts_path: pathlib.Path) -> CactusRoot:
    root = CactusRoot(path=tmp_path.joinpath("cactus_root"), scripts_path=scripts_path)
    root.run(args=["init"])
    root.run(args=["configure", "--set-log-level", "INFO"])

    return root


@contextlib.contextmanager
def closing_cactus_root_popen(cactus_root: CactusRoot, args: List[str]) -> Iterator[None]:
    environment = {**os.environ, "CACTUS_ROOT": os.fspath(cactus_root.path)}

    with subprocess.Popen(args=args, env=environment) as process:
        try:
            yield
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()


@pytest.fixture(name="cactus_daemon", scope="function")
def cactus_daemon_fixture(cactus_root: CactusRoot) -> Iterator[None]:
    with closing_cactus_root_popen(cactus_root=cactus_root, args=[sys.executable, "-m", "cactus.daemon.server"]):
        # TODO: this is not pretty as a hard coded time
        # let it settle
        time.sleep(5)
        yield


@pytest.fixture(name="cactus_data", scope="function")
def cactus_data_fixture(cactus_root: CactusRoot, cactus_daemon: None, scripts_path: pathlib.Path) -> Iterator[None]:
    with closing_cactus_root_popen(cactus_root=cactus_root, args=[os.fspath(scripts_path.joinpath("cactus_data_layer"))]):
        # TODO: this is not pretty as a hard coded time
        # let it settle
        time.sleep(5)
        yield


@pytest.fixture(name="create_example", params=[add_0123_example, add_01234567_example])
def create_example_fixture(request: SubRequest) -> Callable[[DataStore, bytes32], Awaitable[Example]]:
    # https://github.com/pytest-dev/pytest/issues/8763
    return request.param  # type: ignore[no-any-return]


@pytest_asyncio.fixture(name="db_connection", scope="function")
async def db_connection_fixture() -> AsyncIterable[aiosqlite.Connection]:
    async with aiosqlite.connect(":memory:") as connection:
        # make sure this is on for tests even if we disable it at run time
        await connection.execute("PRAGMA foreign_keys = ON")
        yield connection


@pytest.fixture(name="db_wrapper", scope="function")
def db_wrapper_fixture(db_connection: aiosqlite.Connection) -> DBWrapper:
    return DBWrapper(db_connection)


@pytest.fixture(name="tree_id", scope="function")
def tree_id_fixture() -> bytes32:
    base = b"a tree id"
    pad = b"." * (32 - len(base))
    return bytes32(pad + base)


@pytest_asyncio.fixture(name="raw_data_store", scope="function")
async def raw_data_store_fixture(db_wrapper: DBWrapper) -> DataStore:
    return await DataStore.create(db_wrapper=db_wrapper)


@pytest_asyncio.fixture(name="data_store", scope="function")
async def data_store_fixture(raw_data_store: DataStore, tree_id: bytes32) -> AsyncIterable[DataStore]:
    await raw_data_store.create_tree(tree_id=tree_id, status=Status.COMMITTED)

    await raw_data_store.check()
    yield raw_data_store
    await raw_data_store.check()


@pytest.fixture(name="node_type", params=NodeType)
def node_type_fixture(request: SubRequest) -> NodeType:
    return request.param  # type: ignore[no-any-return]


@pytest_asyncio.fixture(name="valid_node_values")
async def valid_node_values_fixture(
    data_store: DataStore,
    tree_id: bytes32,
    node_type: NodeType,
) -> Dict[str, Any]:
    await add_01234567_example(data_store=data_store, tree_id=tree_id)
    node_a = await data_store.get_node_by_key(key=b"\x02", tree_id=tree_id)
    node_b = await data_store.get_node_by_key(key=b"\x04", tree_id=tree_id)

    return create_valid_node_values(node_type=node_type, left_hash=node_a.hash, right_hash=node_b.hash)


@pytest.fixture(name="bad_node_type", params=range(2 * len(NodeType)))
def bad_node_type_fixture(request: SubRequest, valid_node_values: Dict[str, Any]) -> int:
    if request.param == valid_node_values["node_type"]:
        pytest.skip("Actually, this is a valid node type")

    return request.param  # type: ignore[no-any-return]
