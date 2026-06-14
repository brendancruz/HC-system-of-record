"""Configuration for the VBC incentive-alignment simulation.

Every field carries a one-line rationale (see MODEL.md Section 11 for the full
table). The config is a plain dataclass so parameters can be tweaked without
touching core logic; it can also be loaded from / dumped to YAML.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from typing import Any

import yaml


@dataclass
class SimConfig:
    # --- Patient severity distribution (Gamma) -------------------------------
    sev_shape: float = 2.0   # right-skewed severity/spend; Gamma shape
    sev_scale: float = 0.5   # sets E[s] = shape*scale = 1.0 (normalized)

    # --- Health value V(e,s) = alpha*s*e - beta*e^2 --------------------------
    alpha: float = 1.0       # marginal health value of effort per unit severity
    beta: float = 0.5        # over-treatment curvature; creates interior e*

    # --- Care cost C(e,s) = c_base*s + c_eff*s*e -----------------------------
    c_base: float = 0.5      # cost of a severity-s patient at minimal care
    c_eff: float = 0.4       # marginal resource cost of intensity; < alpha => e* > 0

    # --- Provider private effort cost psi(e) = (gamma/2)*e^2 -----------------
    gamma: float = 0.3       # convex private disutility of effort

    # --- Provider preferences -------------------------------------------------
    mu: float = 0.5          # intrinsic motivation; keeps capitation interior
    rho: float = 0.0         # risk aversion; 0 isolates the incentive channel

    # --- Noise ----------------------------------------------------------------
    sigma_c: float = 0.3     # idiosyncratic cost-realization noise SD
    sigma_q: float = 0.3     # imperfect quality-measurement noise SD

    # --- Contract parameters --------------------------------------------------
    phi0: float = 0.3        # FFS base / visit payment (no effort-margin effect)
    phi1: float = 0.4        # FFS marginal fee per intensity; tuned so FFS over-treats
    s_share: float = 0.5     # shared-savings rate (one-sided ~50%)
    b_err: float = 0.0       # benchmark level error (centered at mean severity)
    b_err_slope: float = 0.0  # severity gradient of benchmark error; <0 under-adjusts the sick (cream-skimming lever)
    b_q: float = 0.0         # P4P power on noisy quality signal; overlay off at baseline
    q_target: float = 0.0    # quality target / reference point for P4P overlay
    outside_option: float = 0.0  # accept a patient iff U* >= outside_option

    # --- Monte Carlo ----------------------------------------------------------
    n_patients: int = 100_000  # tight summary stats, runs in seconds
    n_panel: int = 2_000       # ~ ACO attributed-lives scale for panel variance
    e_grid_max: float = 6.0    # effort grid upper bound (covers e* and e_FFS tails)
    e_grid_points: int = 600   # effort grid resolution
    seed: int = 12345          # reproducibility

    # contracts to run in the baseline (two_sided implemented but queued)
    contracts: list[str] = field(
        default_factory=lambda: ["ffs", "capitation", "shared_savings"]
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "SimConfig":
        known = {f.name for f in fields(cls)}
        unknown = set(d) - known
        if unknown:
            raise ValueError(f"Unknown config keys: {sorted(unknown)}")
        return cls(**d)

    def replace(self, **overrides: Any) -> "SimConfig":
        """Return a copy with the given fields overridden (for sweeps)."""
        d = self.to_dict()
        d.update(overrides)
        return SimConfig.from_dict(d)

    def dump_yaml(self, path: str) -> None:
        with open(path, "w") as fh:
            yaml.safe_dump(self.to_dict(), fh, sort_keys=False)


def load_config(path: str | None = None, **overrides: Any) -> SimConfig:
    """Load a config from YAML (or defaults if path is None), then apply overrides."""
    if path is None:
        cfg = SimConfig()
    else:
        with open(path) as fh:
            data = yaml.safe_load(fh) or {}
        cfg = SimConfig.from_dict(data)
    if overrides:
        cfg = cfg.replace(**overrides)
    return cfg
