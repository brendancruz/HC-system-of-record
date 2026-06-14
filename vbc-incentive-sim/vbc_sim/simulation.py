"""Simulation runner - MODEL.md Sections 7 to 9.

For a given contract, solve the provider's privately optimal effort per patient
(vectorized grid argmax of mean-variance utility), apply the selection margin,
realize income/cost/quality shocks, and aggregate the output metrics.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import SimConfig
from .contracts import Contract, build_contract, ffs_closed_form_effort
from .model import (
    Patients,
    care_cost,
    draw_patients,
    effort_cost,
    effort_grid,
    health_value,
    social_optimum_effort,
    social_surplus,
    social_welfare,
)


def _solve_effort(
    contract: Contract,
    s: np.ndarray,
    e_grid: np.ndarray,
    psi_grid: np.ndarray,
    cfg: SimConfig,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (e_chosen, U_star) maximizing mean-variance utility over the grid.

    U(e|s) = E[pi] - psi(e) + mu*E[V] - (rho/2)*Var(pi).
    """
    e_pi = contract.expected_income_grid(s, e_grid, cfg)          # (m,G)
    e_v = health_value(e_grid[None, :], s[:, None], cfg)          # (m,G)
    util = e_pi - psi_grid[None, :] + cfg.mu * e_v
    if cfg.rho != 0.0:
        util = util - 0.5 * cfg.rho * contract.income_variance_grid(s, e_grid, cfg)
    idx = np.argmax(util, axis=1)
    rows = np.arange(s.shape[0])
    return e_grid[idx], util[rows, idx]


def run_contract(
    contract: Contract | str,
    patients: Patients,
    eps_c: np.ndarray,
    eps_q: np.ndarray,
    cfg: SimConfig,
    chunk: int = 20_000,
) -> tuple[dict[str, np.ndarray], dict[str, float | str]]:
    """Run one contract over the panel; return per-patient arrays and a summary."""
    if isinstance(contract, str):
        contract = build_contract(contract)

    s = patients.severity
    n = s.shape[0]
    e_grid = effort_grid(cfg)
    psi_grid = effort_cost(e_grid, cfg)

    e_chosen = np.empty(n)
    u_star = np.empty(n)
    for lo in range(0, n, chunk):
        hi = min(lo + chunk, n)
        e_chosen[lo:hi], u_star[lo:hi] = _solve_effort(
            contract, s[lo:hi], e_grid, psi_grid, cfg
        )

    accept = u_star >= cfg.outside_option
    pi_real = contract.realize_income(e_chosen, s, eps_c, eps_q, cfg)

    per_patient = {
        "severity": s,
        "e_star": patients.e_star,
        "e_chosen": e_chosen,
        "u_star": u_star,
        "accept": accept,
        "income": pi_real,
        "welfare": social_welfare(e_chosen, s, cfg),
        "welfare_firstbest": social_welfare(patients.e_star, s, cfg),
        "surplus": social_surplus(e_chosen, s, cfg),
        "surplus_firstbest": social_surplus(patients.e_star, s, cfg),
    }
    summary = _summarize(contract.name, per_patient, cfg)
    return per_patient, summary


def _summarize(name: str, pp: dict[str, np.ndarray], cfg: SimConfig) -> dict[str, float | str]:
    """Aggregate the MODEL.md Section 9 outputs. Welfare/income on accepted panel."""
    acc = pp["accept"]
    s = pp["severity"]
    e = pp["e_chosen"]
    es = pp["e_star"]

    a_e, a_es, a_s = e[acc], es[acc], s[acc]
    welfare = pp["welfare"][acc]
    welfare_fb = pp["welfare_firstbest"][acc]
    surplus = pp["surplus"][acc]
    surplus_fb = pp["surplus_firstbest"][acc]
    income = pp["income"][acc]

    # over / under treatment (small tolerance to ignore grid discretization)
    tol = cfg.e_grid_max / cfg.e_grid_points
    gap = a_e - a_es
    over = float(np.mean(gap > tol))
    under = float(np.mean(gap < -tol))

    # cream-skimming: acceptance gap between low- and high-severity quartiles
    q1, q3 = np.quantile(s, [0.25, 0.75])
    acc_low = float(np.mean(acc[s <= q1]))
    acc_high = float(np.mean(acc[s >= q3]))

    mean_welfare = float(np.mean(welfare))
    mean_fb = float(np.mean(welfare_fb))
    mean_surplus = float(np.mean(surplus))
    mean_surplus_fb = float(np.mean(surplus_fb))
    return {
        "contract": name,
        "accept_rate": float(np.mean(acc)),
        "accept_low_sev_q": acc_low,
        "accept_high_sev_q": acc_high,
        "cream_skim_index": acc_low - acc_high,   # >0 => skimming against the sick
        # surplus = welfare above the no-treatment baseline (effort-movable part)
        "mean_surplus": mean_surplus,
        "mean_surplus_firstbest": mean_surplus_fb,
        "welfare_gap": mean_surplus_fb - mean_surplus,   # deadweight loss vs first best
        "efficiency_ratio": mean_surplus / mean_surplus_fb if mean_surplus_fb != 0 else float("nan"),
        # true social welfare V - C (carries the fixed baseline cost; level only)
        "mean_welfare": mean_welfare,
        "mean_welfare_firstbest": mean_fb,
        "mean_income": float(np.mean(income)),
        "sd_income": float(np.std(income)),
        "over_treat_rate": over,
        "under_treat_rate": under,
        "mean_effort_gap": float(np.mean(gap)),           # E[e - e*]
        "mean_effort_ratio": float(np.mean(a_e / np.maximum(a_es, 1e-9))),
        "mean_abs_effort_dev": float(np.mean(np.abs(gap))),
    }


def run_all(cfg: SimConfig) -> tuple[pd.DataFrame, dict[str, dict[str, np.ndarray]]]:
    """Run every contract in cfg.contracts with common random numbers.

    Returns (summary_df, details) where details[name] holds the per-patient arrays.
    """
    rng = np.random.default_rng(cfg.seed)
    patients = draw_patients(cfg, rng)
    # common random numbers across contracts (variance reduction)
    eps_c = rng.normal(0.0, cfg.sigma_c, size=len(patients))
    eps_q = rng.normal(0.0, cfg.sigma_q, size=len(patients))

    summaries: list[dict] = []
    details: dict[str, dict[str, np.ndarray]] = {}
    for name in cfg.contracts:
        pp, summ = run_contract(name, patients, eps_c, eps_q, cfg)
        summaries.append(summ)
        details[name] = pp

    summary_df = pd.DataFrame(summaries).set_index("contract")
    _validate(details, cfg)
    return summary_df, details


def _validate(details: dict[str, dict[str, np.ndarray]], cfg: SimConfig) -> None:
    """Cross-check grid optima against closed forms (MODEL.md Section 7).

    Raises AssertionError if the grid solver disagrees with the FFS/capitation
    closed forms by more than one grid step, which would indicate a bug.
    """
    step = cfg.e_grid_max / cfg.e_grid_points
    if "ffs" in details:
        s = details["ffs"]["severity"]
        cf = ffs_closed_form_effort(s, cfg)
        cf = np.clip(cf, 0.0, cfg.e_grid_max)
        assert np.max(np.abs(details["ffs"]["e_chosen"] - cf)) <= 2 * step, "FFS grid vs closed form"
    if "capitation" in details:
        s = details["capitation"]["severity"]
        cf = s * (cfg.mu * cfg.alpha - cfg.c_eff) / (cfg.gamma + 2 * cfg.mu * cfg.beta)
        cf = np.clip(cf, 0.0, cfg.e_grid_max)
        assert np.max(np.abs(details["capitation"]["e_chosen"] - cf)) <= 2 * step, "CAP grid vs closed form"
