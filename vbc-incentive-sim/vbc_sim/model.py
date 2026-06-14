"""Core model primitives: patients, health value, care cost, social optimum.

These are the contract-independent pieces of MODEL.md Sections 4 and 5. All
functions are vectorized over numpy arrays of severity `s` and effort `e`.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .config import SimConfig


@dataclass
class Patients:
    """A drawn panel of patients, each with a severity and its first-best effort."""

    severity: np.ndarray      # s_i, shape (n,)
    e_star: np.ndarray        # social-optimum effort e*(s_i), shape (n,)

    def __len__(self) -> int:
        return self.severity.shape[0]


def draw_patients(cfg: SimConfig, rng: np.random.Generator) -> Patients:
    """Draw n_patients severities from the Gamma and attach their first-best effort."""
    s = rng.gamma(shape=cfg.sev_shape, scale=cfg.sev_scale, size=cfg.n_patients)
    return Patients(severity=s, e_star=social_optimum_effort(s, cfg))


def health_value(e: np.ndarray, s: np.ndarray, cfg: SimConfig) -> np.ndarray:
    """V(e, s) = alpha*s*e - beta*e^2  (concave, interior peak: over-treatment harms)."""
    return cfg.alpha * s * e - cfg.beta * e**2


def care_cost(e: np.ndarray, s: np.ndarray, cfg: SimConfig) -> np.ndarray:
    """C(e, s) = c_base*s + c_eff*s*e  (rises with severity and intensity)."""
    return cfg.c_base * s + cfg.c_eff * s * e


def effort_cost(e: np.ndarray, cfg: SimConfig) -> np.ndarray:
    """psi(e) = (gamma/2)*e^2  (convex private disutility of effort)."""
    return 0.5 * cfg.gamma * e**2


def social_welfare(e: np.ndarray, s: np.ndarray, cfg: SimConfig) -> np.ndarray:
    """Social welfare per patient = V(e,s) - C(e,s) (the benchmark objective)."""
    return health_value(e, s, cfg) - care_cost(e, s, cfg)


def social_surplus(e: np.ndarray, s: np.ndarray, cfg: SimConfig) -> np.ndarray:
    """Effort-movable welfare = W(e,s) - W(0,s) = alpha*s*e - beta*e^2 - c_eff*s*e.

    Equals social welfare measured above the no-treatment (e=0) baseline. The
    fixed baseline cost c_base*s (incurred regardless of effort, unrelated to the
    agency problem) cancels, so surplus is 0 at e=0, maximized at e*, and gives an
    interpretable efficiency ratio. Surplus gaps equal welfare gaps exactly.
    """
    return health_value(e, s, cfg) - cfg.c_eff * s * e


def social_optimum_effort(s: np.ndarray, cfg: SimConfig) -> np.ndarray:
    """e*(s) = s*(alpha - c_eff)/(2*beta), floored at 0.

    Closed form from maximizing V - C in e (MODEL.md 5.4). Positive iff alpha > c_eff.
    """
    e = s * (cfg.alpha - cfg.c_eff) / (2.0 * cfg.beta)
    return np.maximum(e, 0.0)


def effort_grid(cfg: SimConfig) -> np.ndarray:
    """The shared effort grid the provider optimizes over (e >= 0)."""
    return np.linspace(0.0, cfg.e_grid_max, cfg.e_grid_points)
