from __future__ import annotations

from cactus.server.start_service import Service
from cactus.solver.solver import Solver
from cactus.solver.solver_api import SolverAPI
from cactus.solver.solver_rpc_api import SolverRpcApi

SolverService = Service[Solver, SolverAPI, SolverRpcApi]
