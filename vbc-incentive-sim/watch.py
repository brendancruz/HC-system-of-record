#!/usr/bin/env python3
"""Watch the VBC simulation run.

Two ways to watch:
  - GIF replay (default): renders an animation of the Monte Carlo converging -
    effort clouds forming against e*, plus running efficiency/income/treatment
    metrics. Works headless; play the GIF in any browser/viewer.
  - Live terminal mode (--live): streams the running metrics to the console as
    patients accumulate (nice over SSH).

Usage:
    python watch.py                          # write outputs/simulation.gif
    python watch.py --live                   # stream metrics in the terminal
    python watch.py --config config/default.yaml --frames 80 --fps 15
"""

from __future__ import annotations

import argparse

from vbc_sim.animation import animate_simulation, watch_live
from vbc_sim.config import load_config
from vbc_sim.simulation import run_all


def main() -> None:
    ap = argparse.ArgumentParser(description="Watch the VBC simulation")
    ap.add_argument("--config", default=None, help="YAML config (defaults if omitted)")
    ap.add_argument("--out", default="outputs/simulation.gif", help="GIF output path")
    ap.add_argument("--frames", type=int, default=60, help="animation frames")
    ap.add_argument("--fps", type=int, default=12, help="animation frames per second")
    ap.add_argument("--sample", type=int, default=2500, help="scatter points to reveal")
    ap.add_argument("--live", action="store_true", help="stream metrics in the terminal instead")
    ap.add_argument("--steps", type=int, default=25, help="live mode: number of updates")
    ap.add_argument("--delay", type=float, default=0.15, help="live mode: seconds between updates")
    args = ap.parse_args()

    cfg = load_config(args.config)
    print(f"Running simulation: {cfg.n_patients:,} patients x {len(cfg.contracts)} contracts ...")
    _, details = run_all(cfg)

    if args.live:
        watch_live(details, cfg, steps=args.steps, delay=args.delay)
    else:
        path = animate_simulation(
            details, cfg, outpath=args.out,
            n_frames=args.frames, sample=args.sample, fps=args.fps,
        )
        print(f"Animation written: {path}")


if __name__ == "__main__":
    main()
