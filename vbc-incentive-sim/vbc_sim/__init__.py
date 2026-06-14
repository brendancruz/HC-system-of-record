"""VBC Incentive Alignment Simulation.

A Monte Carlo / agent-based model of provider behavior under different
value-based care (VBC) contract structures. See MODEL.md for the full spec and
the rationale behind every parameter default.
"""

from .config import SimConfig, load_config
from .model import Patients, social_optimum_effort, health_value, care_cost
from .contracts import CONTRACTS, build_contract
from .simulation import run_contract, run_all
from .sweep import sweep
from .animation import animate_simulation, watch_live

__all__ = [
    "SimConfig",
    "load_config",
    "Patients",
    "social_optimum_effort",
    "health_value",
    "care_cost",
    "CONTRACTS",
    "build_contract",
    "run_contract",
    "run_all",
    "sweep",
    "animate_simulation",
    "watch_live",
]
