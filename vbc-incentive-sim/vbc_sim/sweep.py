"""Parameter-sweep harness - MODEL.md Section 8 / Section 13.

Re-runs the Monte Carlo across a grid of one or more parameters and collects the
per-contract summaries into a tidy DataFrame, without touching core logic. Used
for the queued benchmark-error, risk-aversion, and intrinsic-motivation sweeps.
"""

from __future__ import annotations

import itertools
from typing import Any, Iterable, Mapping

import pandas as pd

from .config import SimConfig
from .simulation import run_all


def sweep(base: SimConfig, grid: Mapping[str, Iterable[Any]]) -> pd.DataFrame:
    """Cartesian-product sweep over `grid` (param name -> values).

    Example:
        sweep(cfg, {"b_err": [-0.2, 0.0, 0.2], "rho": [0.0, 1.0]})

    Returns one row per (parameter combination x contract) with the swept
    parameter values plus every summary metric.
    """
    names = list(grid)
    rows: list[dict] = []
    for combo in itertools.product(*(grid[n] for n in names)):
        overrides = dict(zip(names, combo))
        cfg = base.replace(**overrides)
        summary_df, _ = run_all(cfg)
        for metrics in summary_df.reset_index().to_dict("records"):
            rows.append({**overrides, **metrics})
    return pd.DataFrame(rows)
