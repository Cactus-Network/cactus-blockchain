from __future__ import annotations

import click

from cactus.cmds.cmd_classes import CactusCliContext


@click.group("solver", help="Manage your solver")
def solver_cmd() -> None:
    pass


@solver_cmd.command("get_state", help="Get current solver state")
@click.option(
    "-sp",
    "--solver-rpc-port",
    help="Set the port where the Solver is hosting the RPC interface. See the rpc_port under solver in config.yaml",
    type=int,
    default=None,
    show_default=True,
)
@click.pass_context
def get_state_cmd(
    ctx: click.Context,
    solver_rpc_port: int | None,
) -> None:
    import asyncio

    from cactus.cmds.solver_funcs import get_state

    asyncio.run(get_state(CactusCliContext.set_default(ctx), solver_rpc_port))
