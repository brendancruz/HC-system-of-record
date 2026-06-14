"""Watchable replay of the Monte Carlo - an animation of the simulation evolving.

The heavy compute (per-patient effort, income, welfare) is already done by
`run_all`; this module just *reveals* patients incrementally so you can watch the
clouds of chosen effort form against the social optimum and the running metrics
converge. Renders to an animated GIF (works headless; no ffmpeg needed).
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

from .config import SimConfig
from .model import social_optimum_effort
from .plotting import LABELS, _color, _label


def _running_metrics(pp: dict[str, np.ndarray], k: int) -> dict[str, float]:
    """Cumulative metrics on the first k patients (the 'so far' view)."""
    e = pp["e_chosen"][:k]
    es = pp["e_star"][:k]
    surplus = pp["surplus"][:k]
    surplus_fb = pp["surplus_firstbest"][:k]
    income = pp["income"][:k]
    tol = 1e-6
    gap = e - es
    fb = surplus_fb.mean()
    return {
        "efficiency": surplus.mean() / fb if fb else float("nan"),
        "income_mean": float(income.mean()),
        "income_sd": float(income.std()),
        "over": float(np.mean(gap > tol)),
        "under": float(np.mean(gap < -tol)),
    }


def animate_simulation(
    details: dict[str, dict[str, np.ndarray]],
    cfg: SimConfig,
    outpath: str = "outputs/simulation.gif",
    n_frames: int = 60,
    sample: int = 2500,
    fps: int = 12,
) -> str:
    """Render an animated replay of the simulation to `outpath` (GIF)."""
    names = list(details)
    n_total = len(details[names[0]]["severity"])
    # fixed scatter sample (reveal order = draw order, already iid/random)
    sample = min(sample, n_total)
    sidx = np.linspace(0, n_total - 1, sample).astype(int)

    # cumulative reveal schedule (ease-in: a little slow at the very start)
    fracs = np.linspace(0.02, 1.0, n_frames) ** 0.85

    s_scatter = {n: details[n]["severity"][sidx] for n in names}
    e_scatter = {n: details[n]["e_chosen"][sidx] for n in names}

    # severity grid for the e* line and axis limits
    s_lo, s_hi = 0.0, float(np.quantile(details[names[0]]["severity"], 0.995))
    sgrid = np.linspace(s_lo, s_hi, 100)
    e_hi = max(np.quantile(e_scatter[n], 0.995) for n in names) * 1.05

    fig = plt.figure(figsize=(12, 6.5))
    gs = fig.add_gridspec(3, 2, width_ratios=[1.55, 1.0], hspace=0.55, wspace=0.28)
    ax_sc = fig.add_subplot(gs[:, 0])
    ax_eff = fig.add_subplot(gs[0, 1])
    ax_inc = fig.add_subplot(gs[1, 1])
    ax_tx = fig.add_subplot(gs[2, 1])
    ax_tx.axis("off")
    fig.suptitle("VBC simulation replay - provider effort vs the social optimum",
                 fontsize=13, fontweight="bold")

    # static scatter axis furniture
    ax_sc.plot(sgrid, social_optimum_effort(sgrid, cfg), "k--", lw=2,
               label="Social optimum e*(s)", zorder=5)
    scatters = {
        n: ax_sc.scatter([], [], s=9, alpha=0.30, color=_color(n), label=_label(n))
        for n in names
    }
    ax_sc.set_xlim(s_lo, s_hi)
    ax_sc.set_ylim(0, e_hi)
    ax_sc.set_xlabel("Patient severity s")
    ax_sc.set_ylabel("Chosen treatment intensity e")
    ax_sc.legend(loc="upper left", fontsize=8, framealpha=0.9)

    xpos = np.arange(len(names))
    colors = [_color(n) for n in names]

    def draw_metric_frame(k: int):
        m = {n: _running_metrics(details[n], k) for n in names}

        ax_eff.clear()
        ax_eff.bar(xpos, [m[n]["efficiency"] for n in names], color=colors)
        ax_eff.axhline(1.0, ls="--", color="black", lw=1)
        ax_eff.set_ylim(0, 1.05)
        ax_eff.set_xticks(xpos)
        ax_eff.set_xticklabels([n.upper()[:4] for n in names], fontsize=8)
        ax_eff.set_title("Efficiency vs first-best (running)", fontsize=9)
        for x, n in zip(xpos, names):
            ax_eff.text(x, m[n]["efficiency"] + 0.02, f"{m[n]['efficiency']*100:.0f}%",
                        ha="center", fontsize=8)

        ax_inc.clear()
        ax_inc.bar(xpos, [m[n]["income_mean"] for n in names],
                   yerr=[m[n]["income_sd"] for n in names], capsize=4, color=colors,
                   error_kw={"ecolor": "black", "lw": 1})
        ax_inc.set_xticks(xpos)
        ax_inc.set_xticklabels([n.upper()[:4] for n in names], fontsize=8)
        ax_inc.set_title("Provider income mean +/- SD (running)", fontsize=9)

        ax_tx.clear()
        ax_tx.axis("off")
        lines = [f"patients processed:  {k:,} / {n_total:,}", ""]
        for n in names:
            lines.append(
                f"{_label(n):<24} over {m[n]['over']*100:5.1f}%  under {m[n]['under']*100:5.1f}%"
            )
        ax_tx.text(0.0, 0.95, "\n".join(lines), va="top", ha="left",
                   family="monospace", fontsize=9, transform=ax_tx.transAxes)

    def update(frame: int):
        frac = fracs[frame]
        k = max(2, int(frac * n_total))
        m_scatter = max(1, int(frac * sample))
        for n in names:
            xy = np.column_stack([s_scatter[n][:m_scatter], e_scatter[n][:m_scatter]])
            scatters[n].set_offsets(xy)
        draw_metric_frame(k)
        return list(scatters.values())

    anim = FuncAnimation(fig, update, frames=n_frames, blit=False)
    os.makedirs(os.path.dirname(outpath) or ".", exist_ok=True)
    anim.save(outpath, writer=PillowWriter(fps=fps))
    plt.close(fig)
    return outpath


def watch_live(details: dict[str, dict[str, np.ndarray]], cfg: SimConfig,
               steps: int = 25, delay: float = 0.15) -> None:
    """Stream the running metrics to the terminal (a console 'watch' mode)."""
    import sys
    import time

    names = list(details)
    n_total = len(details[names[0]]["severity"])
    header = f"{'patients':>10} | " + " | ".join(f"{n.upper()[:4]:>22}" for n in names)
    sub = f"{'':>10} | " + " | ".join(f"{'eff   inc    over':>22}" for _ in names)
    for step in range(1, steps + 1):
        k = max(2, int(n_total * step / steps))
        cells = []
        for n in names:
            m = _running_metrics(details[n], k)
            cells.append(f"{m['efficiency']*100:4.0f}% {m['income_mean']:5.2f} {m['over']*100:4.0f}%")
        if step == 1:
            print(header)
            print(sub)
            print("-" * len(header))
        line = f"{k:>10,} | " + " | ".join(f"{c:>22}" for c in cells)
        sys.stdout.write("\r" + line)
        sys.stdout.flush()
        if delay:
            time.sleep(delay)
    print()  # final newline
