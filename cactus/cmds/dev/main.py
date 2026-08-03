from __future__ import annotations

import click

from cactus.cmds.dev.data import data_group
from cactus.cmds.dev.gh import gh_group
from cactus.cmds.dev.installers import installers_group
from cactus.cmds.dev.mempool import mempool_cmd
from cactus.cmds.dev.sim import sim_cmd


@click.group("dev", help="Developer commands and tools")
@click.pass_context
def dev_cmd(ctx: click.Context) -> None:
    pass


dev_cmd.add_command(sim_cmd)
dev_cmd.add_command(installers_group)
dev_cmd.add_command(gh_group)
dev_cmd.add_command(mempool_cmd)
dev_cmd.add_command(data_group)
