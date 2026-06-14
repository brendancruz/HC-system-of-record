"""Plotting - MODEL.md Section 10.

Three required baseline plots plus a selection view:
  1. social welfare by contract (bar)
  2. provider income mean +/- SD by contract (bar with error bars)
  3. treatment intensity vs e* (mean chosen effort by severity, with first-best line)
  4. acceptance rate by severity quartile (selection view)
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")  # headless / file output
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .config import SimConfig
from .model import social_optimum_effort

# stable label / color per contract
LABELS = {
    "ffs": "Fee-for-service",
    "capitation": "Capitation",
    "shared_savings": "Shared savings (upside)",
    "two_sided": "Two-sided risk",
}
COLORS = {
    "ffs": "#d1495b",
    "capitation": "#30638e",
    "shared_savings": "#00798c",
    "two_sided": "#edae49",
}


def _label(name: str) -> str:
    return LABELS.get(name, name)


def _color(name: str) -> str:
    return COLORS.get(name, "#666666")


def plot_welfare(summary: pd.DataFrame, outdir: str) -> str:
    contracts = list(summary.index)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    welfare = summary["mean_surplus"].values
    fb = summary["mean_surplus_firstbest"].iloc[0]  # same first-best across contracts
    ax.bar(range(len(contracts)), welfare, color=[_color(c) for c in contracts])
    ax.axhline(fb, ls="--", color="black", lw=1, label=f"First-best surplus ({fb:.3f})")
    ax.set_xticks(range(len(contracts)))
    ax.set_xticklabels([_label(c) for c in contracts], rotation=15, ha="right")
    ax.set_ylabel("Mean social surplus per patient  (welfare above no-treatment)")
    ax.set_title("Social surplus by contract vs the first-best benchmark")
    for i, w in enumerate(welfare):
        ax.text(i, w, f"{w:.3f}", ha="center", va="bottom", fontsize=9)
    ax.legend()
    fig.tight_layout()
    path = os.path.join(outdir, "welfare_by_contract.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_income(summary: pd.DataFrame, outdir: str) -> str:
    contracts = list(summary.index)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    mean = summary["mean_income"].values
    sd = summary["sd_income"].values
    ax.bar(
        range(len(contracts)),
        mean,
        yerr=sd,
        capsize=6,
        color=[_color(c) for c in contracts],
        error_kw={"ecolor": "black", "lw": 1.2},
    )
    ax.set_xticks(range(len(contracts)))
    ax.set_xticklabels([_label(c) for c in contracts], rotation=15, ha="right")
    ax.set_ylabel("Provider net income per patient  (mean +/- 1 SD)")
    ax.set_title("Provider income level and risk by contract")
    for i, (m, s) in enumerate(zip(mean, sd)):
        ax.text(i, m, f"mean {m:.3f}\nSD {s:.3f}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    path = os.path.join(outdir, "income_by_contract.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_intensity_vs_optimum(
    details: dict[str, dict[str, np.ndarray]], cfg: SimConfig, outdir: str, n_bins: int = 25
) -> str:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    # severity bins shared across contracts (use first contract's draws)
    any_name = next(iter(details))
    s_all = details[any_name]["severity"]
    edges = np.quantile(s_all, np.linspace(0, 1, n_bins + 1))
    centers = 0.5 * (edges[:-1] + edges[1:])

    for name, pp in details.items():
        s = pp["severity"]
        e = pp["e_chosen"]
        idx = np.clip(np.digitize(s, edges[1:-1]), 0, n_bins - 1)
        mean_e = np.array([e[idx == b].mean() if np.any(idx == b) else np.nan for b in range(n_bins)])
        ax.plot(centers, mean_e, marker="o", ms=3, lw=1.5, color=_color(name), label=_label(name))

    e_star = social_optimum_effort(centers, cfg)
    ax.plot(centers, e_star, ls="--", lw=2, color="black", label="Social optimum e*(s)")
    ax.set_xlabel("Patient severity s")
    ax.set_ylabel("Mean chosen treatment intensity e")
    ax.set_title("Treatment intensity vs the social optimum, by contract")
    ax.legend()
    fig.tight_layout()
    path = os.path.join(outdir, "intensity_vs_optimum.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_selection(summary: pd.DataFrame, outdir: str) -> str:
    contracts = list(summary.index)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = np.arange(len(contracts))
    w = 0.38
    ax.bar(x - w / 2, summary["accept_low_sev_q"].values, w, label="Lowest severity quartile", color="#8ecae6")
    ax.bar(x + w / 2, summary["accept_high_sev_q"].values, w, label="Highest severity quartile", color="#fb8500")
    ax.set_xticks(x)
    ax.set_xticklabels([_label(c) for c in contracts], rotation=15, ha="right")
    ax.set_ylabel("Patient acceptance rate")
    ax.set_ylim(0, 1.05)
    ax.set_title("Patient selection by severity (cream-skimming view)")
    ax.legend()
    fig.tight_layout()
    path = os.path.join(outdir, "selection_by_severity.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def make_all_plots(summary: pd.DataFrame, details: dict, cfg: SimConfig, outdir: str) -> list[str]:
    os.makedirs(outdir, exist_ok=True)
    return [
        plot_welfare(summary, outdir),
        plot_income(summary, outdir),
        plot_intensity_vs_optimum(details, cfg, outdir),
        plot_selection(summary, outdir),
    ]
