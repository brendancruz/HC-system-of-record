# VBC Incentive Alignment Simulation

A Monte Carlo / agent-based model of provider behavior under different
value-based care (VBC) contract structures, built to show empirically where VBC
incentives align with social welfare and where they break. Feeds an honors thesis
on healthcare incentive alignment and information silos.

Theoretical backbone: the multitask principal-agent problem (Holmstrom and
Milgrom 1991). When one task is measurable (cost) and another is not
(appropriateness / quality), high-powered incentives on the measurable task
distort effort. This model operationalizes that argument numerically.

- **Spec and assumptions:** [`MODEL.md`](./MODEL.md) - read this first.
- **Baseline read:** [`FINDINGS.md`](./FINDINGS.md) - one-page, thesis-framed.

## Run it interactively (Colab - no install)

The easiest front door: an interactive notebook with parameter sliders. Open it
in Google Colab, drag sliders, click **Run simulation**, and the summary table +
plots (and optionally the GIF) render inline. Nothing to install locally.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/brendancruz/hc-system-of-record/blob/main/vbc-incentive-sim/notebooks/vbc_explorer.ipynb)

Notebook: [`notebooks/vbc_explorer.ipynb`](./notebooks/vbc_explorer.ipynb)

- The badge above works once this is merged to `main`. **Before merge** (or any
  time the badge misbehaves on a slashed branch name), open it via Colab directly:
  `colab.research.google.com` -> **File -> Open notebook -> GitHub** -> enter
  `brendancruz/hc-system-of-record` -> pick the branch -> choose
  `vbc-incentive-sim/notebooks/vbc_explorer.ipynb`.
- **Private repo:** the first Setup cell clones the repo. If it is private, add a
  GitHub token once via Colab **Secrets** (key icon) named `GH_TOKEN`; the cell
  picks it up automatically. Public repo needs no token.
- Run the Setup cell once per session, then the Explorer cell to get the sliders.

## Quick start (local)

```bash
pip install -r requirements.txt
python run_baseline.py                 # uses built-in defaults
python run_baseline.py --config config/default.yaml --outdir outputs
```

Outputs land in `outputs/`: `baseline_summary.csv`, the resolved
`baseline_config.yaml`, and four plots (welfare, income mean/SD, intensity vs
`e*`, selection by severity).

## Watch it run

```bash
python watch.py                 # renders outputs/simulation.gif (play in any viewer)
python watch.py --live          # streams running metrics in the terminal
python watch.py --frames 80 --fps 15 --out outputs/simulation.gif
```

The GIF replays the Monte Carlo converging: effort clouds forming against the
social optimum `e*`, with running efficiency, provider income mean/SD, and
over/under-treatment counters as patients accumulate. `--live` is a console view
for watching over SSH.

## Layout

```
MODEL.md            formal model + every parameter rationale (Step 0)
FINDINGS.md         baseline findings, plain language
config/default.yaml editable defaults (config-driven; no need to touch core code)
run_baseline.py     entry point: runs contracts 1-3, writes CSV + plots
vbc_sim/
  config.py         SimConfig dataclass + YAML load/dump
  model.py          patients, V(e,s), C(e,s), psi(e), social optimum e*
  contracts.py      FFS / capitation / shared-savings / two-sided (+ P4P overlay)
  simulation.py     provider effort solver, Monte Carlo runner, metrics
  sweep.py          parameter-sweep harness (for the queued experiments)
  plotting.py       the four baseline plots
outputs/            generated results + figures
```

## What the baseline shows (defaults, 100k patients)

| Contract | Efficiency vs first-best | Effort vs e* | Provider income (mean / SD) |
|---|---|---|---|
| Fee-for-service | 49% | over-treats (under-serves the sickest) | 0.75 / 0.18 |
| Capitation | 37% | under-treats | 0.28 / 0.53 |
| Shared savings (upside) | 73% | mild over-treatment | 0.78 / 0.22 |

All emergent from private optimization, not assumed. See `FINDINGS.md`.

## Extending it

Everything is config-driven. To run an experiment, sweep any parameter:

```python
from vbc_sim import SimConfig, sweep
df = sweep(SimConfig(), {"b_err": [-0.2, 0.0, 0.2], "rho": [0.0, 1.0]})
```

Queued sweeps: two-sided risk in the baseline, benchmark-error / cream-skimming,
risk aversion, intrinsic motivation, P4P overlay (see `FINDINGS.md`).

## Conventions

Abstract internally-consistent units (relative cross-contract behavior is the
point, not a dollar forecast). No em dashes; en dash with spaces for breaks.
Every assumption and shortcut is labeled in `MODEL.md`.
