"""Contract structures (the experimental treatments) - MODEL.md Section 6.

Each contract exposes, vectorized over a panel of severities `s` (shape (n,)) and
an effort grid `e_grid` (shape (G,)):

    expected_income_grid(s, e_grid, cfg) -> (n, G)   E[pi(e,s)]
    income_variance_grid(s, e_grid, cfg) -> (n, G)   Var(pi(e,s))
    realize_income(e, s, eps_c, eps_q, cfg) -> (n,)  realized pi at chosen effort

The provider's full utility (effort cost, intrinsic motivation, risk penalty) is
assembled in simulation.py; contracts only supply the income mean/variance, plus
the optional P4P quality overlay which is common to all of them.
"""

from __future__ import annotations

import numpy as np
from scipy.special import ndtr  # standard normal CDF, vectorized

from .config import SimConfig
from .model import care_cost, health_value, social_optimum_effort


SQRT_2PI = np.sqrt(2.0 * np.pi)


def _norm_pdf(x: np.ndarray) -> np.ndarray:
    return np.exp(-0.5 * x * x) / SQRT_2PI


def risk_mult(s: np.ndarray, cfg: SimConfig) -> np.ndarray:
    """Benchmark / risk-adjustment multiplier (MODEL.md 5.6).

    mult(s) = 1 + b_err + b_err_slope*(s - 1), centered at mean severity 1.0:
    `b_err` is the average-level benchmark error; `b_err_slope` is its severity
    gradient. A negative slope under-adjusts the sick (their benchmark/PMPM is
    compressed below true need), which is the realistic risk-adjustment failure
    that drives cream-skimming against high-severity patients. Floored above 0.
    """
    mult = 1.0 + cfg.b_err + cfg.b_err_slope * (s - 1.0)
    return np.maximum(mult, 1e-6)


def _truncated_normal_moments(m: np.ndarray, sigma: float) -> tuple[np.ndarray, np.ndarray]:
    """Mean and variance of max(X, 0) for X ~ Normal(m, sigma^2), vectorized over m.

    E[max(X,0)] = m*Phi(m/s) + s*phi(m/s)
    E[max(X,0)^2] = (m^2+s^2)*Phi(m/s) + m*s*phi(m/s)
    Used for the upside-only shared-savings floor (MODEL.md Section 7).
    """
    if sigma <= 0:
        mx = np.maximum(m, 0.0)
        return mx, np.zeros_like(mx)
    z = m / sigma
    Phi = ndtr(z)
    phi = _norm_pdf(z)
    mean = m * Phi + sigma * phi
    second = (m * m + sigma * sigma) * Phi + m * sigma * phi
    var = np.maximum(second - mean * mean, 0.0)  # clip tiny negative from roundoff
    return mean, var


# --------------------------------------------------------------------------- #
# Base class (handles the common P4P quality overlay)
# --------------------------------------------------------------------------- #
class Contract:
    name = "base"

    # --- income before the overlay (override these) ---
    def _base_expected_income(self, s, e_grid, cfg):  # (n,G)
        raise NotImplementedError

    def _base_income_variance(self, s, e_grid, cfg):  # (n,G)
        raise NotImplementedError

    def _base_realized_income(self, e, s, eps_c, cfg):  # (n,)
        raise NotImplementedError

    # --- public API (adds the optional P4P overlay b_q*(q - q_target)) ---
    def expected_income_grid(self, s, e_grid, cfg):
        inc = self._base_expected_income(s, e_grid, cfg)
        if cfg.b_q != 0.0:
            v = health_value(e_grid[None, :], s[:, None], cfg)  # (n,G)
            inc = inc + cfg.b_q * (v - cfg.q_target)
        return inc

    def income_variance_grid(self, s, e_grid, cfg):
        var = self._base_income_variance(s, e_grid, cfg)
        if cfg.b_q != 0.0:
            var = var + (cfg.b_q ** 2) * (cfg.sigma_q ** 2)  # overlay noise is independent
        return var

    def realize_income(self, e, s, eps_c, eps_q, cfg):
        inc = self._base_realized_income(e, s, eps_c, cfg)
        if cfg.b_q != 0.0:
            q = health_value(e, s, cfg) + eps_q
            inc = inc + cfg.b_q * (q - cfg.q_target)
        return inc


# --------------------------------------------------------------------------- #
# 1. Fee-for-service:  pi = phi0 + phi1*e   (payor bears resource cost)
# --------------------------------------------------------------------------- #
class FeeForService(Contract):
    name = "ffs"

    def _base_expected_income(self, s, e_grid, cfg):
        inc = cfg.phi0 + cfg.phi1 * e_grid              # (G,)
        return np.broadcast_to(inc, (s.shape[0], e_grid.shape[0]))

    def _base_income_variance(self, s, e_grid, cfg):
        return np.zeros((s.shape[0], e_grid.shape[0]))  # provider bears no cost risk

    def _base_realized_income(self, e, s, eps_c, cfg):
        return cfg.phi0 + cfg.phi1 * e


# --------------------------------------------------------------------------- #
# 2. Capitation:  pi = K(s) - C_real,  K(s) = (1+b_err)*C(e*, s)
# --------------------------------------------------------------------------- #
class Capitation(Contract):
    name = "capitation"

    def _pmpm(self, s, cfg):
        """Risk-adjusted PMPM: priced off the appropriate (social-optimum) cost."""
        e_star = social_optimum_effort(s, cfg)
        return risk_mult(s, cfg) * care_cost(e_star, s, cfg)

    def _base_expected_income(self, s, e_grid, cfg):
        k = self._pmpm(s, cfg)[:, None]                 # (n,1)
        cbar = care_cost(e_grid[None, :], s[:, None], cfg)  # (n,G)
        return k - cbar

    def _base_income_variance(self, s, e_grid, cfg):
        # provider bears the full cost shock; variance is effort-independent
        return np.full((s.shape[0], e_grid.shape[0]), cfg.sigma_c ** 2)

    def _base_realized_income(self, e, s, eps_c, cfg):
        k = self._pmpm(s, cfg)
        return k - (care_cost(e, s, cfg) + eps_c)


# --------------------------------------------------------------------------- #
# 3. Shared savings, upside-only:
#    pi = phi0 + phi1*e + s_share*max(B(s) - C_real, 0),  B = (1+b_err)*C(e_FFS, s)
# --------------------------------------------------------------------------- #
class SharedSavingsUpside(Contract):
    name = "shared_savings"

    def _benchmark(self, s, cfg):
        """Benchmark built off historical FFS-practice cost (MODEL.md 6.3)."""
        e_ffs = ffs_closed_form_effort(s, cfg)
        return risk_mult(s, cfg) * care_cost(e_ffs, s, cfg)

    def _base_expected_income(self, s, e_grid, cfg):
        b = self._benchmark(s, cfg)[:, None]            # (n,1)
        cbar = care_cost(e_grid[None, :], s[:, None], cfg)  # (n,G)
        m = b - cbar                                    # expected savings (n,G)
        mean_sav, _ = _truncated_normal_moments(m, cfg.sigma_c)
        return cfg.phi0 + cfg.phi1 * e_grid[None, :] + cfg.s_share * mean_sav

    def _base_income_variance(self, s, e_grid, cfg):
        b = self._benchmark(s, cfg)[:, None]
        cbar = care_cost(e_grid[None, :], s[:, None], cfg)
        m = b - cbar
        _, var_sav = _truncated_normal_moments(m, cfg.sigma_c)
        return (cfg.s_share ** 2) * var_sav

    def _base_realized_income(self, e, s, eps_c, cfg):
        b = self._benchmark(s, cfg)
        c_real = care_cost(e, s, cfg) + eps_c
        savings = np.maximum(b - c_real, 0.0)
        return cfg.phi0 + cfg.phi1 * e + cfg.s_share * savings


# --------------------------------------------------------------------------- #
# 4. Two-sided risk (implemented; queued for the next analysis pass):
#    pi = phi0 + phi1*e + s_share*(B(s) - C_real)   (no floor, symmetric risk)
# --------------------------------------------------------------------------- #
class TwoSidedRisk(SharedSavingsUpside):
    name = "two_sided"

    def _base_expected_income(self, s, e_grid, cfg):
        b = self._benchmark(s, cfg)[:, None]
        cbar = care_cost(e_grid[None, :], s[:, None], cfg)
        m = b - cbar                                    # symmetric: E[savings] = m
        return cfg.phi0 + cfg.phi1 * e_grid[None, :] + cfg.s_share * m

    def _base_income_variance(self, s, e_grid, cfg):
        # Var(s_share*(B - C_real)) = s_share^2 * sigma_c^2 (B, Cbar deterministic in e)
        return np.full((s.shape[0], e_grid.shape[0]), (cfg.s_share ** 2) * cfg.sigma_c ** 2)

    def _base_realized_income(self, e, s, eps_c, cfg):
        b = self._benchmark(s, cfg)
        c_real = care_cost(e, s, cfg) + eps_c
        return cfg.phi0 + cfg.phi1 * e + cfg.s_share * (b - c_real)


def ffs_closed_form_effort(s: np.ndarray, cfg: SimConfig) -> np.ndarray:
    """Closed-form FFS optimum e_FFS = (phi1 + mu*alpha*s)/(gamma + 2*mu*beta).

    Used as the historical-practice basis for the shared-savings benchmark and as
    a cross-check on the grid solver (MODEL.md Section 7).
    """
    return (cfg.phi1 + cfg.mu * cfg.alpha * s) / (cfg.gamma + 2.0 * cfg.mu * cfg.beta)


CONTRACTS = {
    "ffs": FeeForService,
    "capitation": Capitation,
    "shared_savings": SharedSavingsUpside,
    "two_sided": TwoSidedRisk,
}


def build_contract(name: str) -> Contract:
    if name not in CONTRACTS:
        raise ValueError(f"Unknown contract {name!r}; choose from {sorted(CONTRACTS)}")
    return CONTRACTS[name]()
