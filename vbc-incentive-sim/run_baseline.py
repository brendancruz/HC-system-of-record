#!/usr/bin/env python3
"""Baseline Monte Carlo run for the VBC incentive-alignment simulation.

Runs contracts 1 to 3 (FFS, capitation, shared savings upside-only) with the
default config, writes the per-contract summary CSV, and produces the baseline
plots. See MODEL.md for the spec and FINDINGS.md for the read on the output.

Usage:
    python run_baseline.py [--config config/default.yaml] [--outdir outputs]
"""

from __future__ import annotations

import argparse
import os

import pandas as pd

from vbc_sim.config import load_config
from vbc_sim.plotting import make_all_plots
from vbc_sim.simulation import run_all


def main() -> None:
    ap = argparse.ArgumentParser(description="VBC incentive-alignment baseline run")
    ap.add_argument("--config", default=None, help="YAML config (defaults if omitted)")
    ap.add_argument("--outdir", default="outputs", help="output directory")
    args = ap.parse_args()

    cfg = load_config(args.config)
    os.makedirs(args.outdir, exist_ok=True)

    summary, details = run_all(cfg)

    # persist results
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", 50)
    csv_path = os.path.join(args.outdir, "baseline_summary.csv")
    summary.to_csv(csv_path)
    cfg.dump_yaml(os.path.join(args.outdir, "baseline_config.yaml"))
    plots = make_all_plots(summary, details, cfg, args.outdir)

    # console report
    cols = [
        "accept_rate", "mean_surplus", "mean_surplus_firstbest", "welfare_gap",
        "efficiency_ratio", "mean_income", "sd_income",
        "over_treat_rate", "under_treat_rate", "mean_effort_gap", "cream_skim_index",
    ]
    print("\n=== Baseline summary (contracts 1 to 3) ===\n")
    print(summary[cols].round(4).to_string())
    print(f"\nSummary CSV : {csv_path}")
    print("Plots       :")
    for p in plots:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
