from __future__ import annotations

import json

from cactus.cmds.cmd_classes import CactusCliContext
from cactus.cmds.cmds_util import get_any_service_client
from cactus.solver.solver_rpc_client import SolverRpcClient


async def get_state(
    ctx: CactusCliContext,
    solver_rpc_port: int | None = None,
) -> None:
    """Get solver state via RPC."""
    try:
        async with get_any_service_client(SolverRpcClient, ctx.root_path, solver_rpc_port) as (client, _):
            response = await client.get_state()
            print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"Failed to get solver state: {e}")
