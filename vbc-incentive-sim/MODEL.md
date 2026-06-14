# MODEL.md - VBC Incentive Alignment Simulation

**Project:** Monte Carlo / agent-based model of provider behavior under different
value-based care (VBC) contract structures.
**Purpose:** Show empirically where VBC incentives align with social welfare and
where they break. Feeds an honors thesis on healthcare incentive alignment and
information silos (advisor: Tim Liu).
**Theoretical backbone:** the multitask principal-agent problem
(Holmstrom and Milgrom 1991). When one task is measurable (cost) and another is
not (appropriateness / quality), putting high-powered incentives on the
measurable task distorts effort away from the unmeasured one. This model
operationalizes that verbal argument numerically.

**Status:** Spec for review (Step 0). The first build implements contracts 1 to 3
(FFS, capitation, shared savings upside-only) on top of this spec. Read the
"Assumptions and shortcuts" section at the end before trusting any number.

> Convention note: no em dashes anywhere; en dash with spaces for breaks. Dollar
> figures (where they appear) as $xB / $xM / $xk / $xT. Model quantities here are
> in abstract, internally consistent units (see "Units" below), not dollars,
> because the point is relative cross-contract behavior, not a dollar forecast.

---

## 1. Overview and what the model is for

We simulate a single payor (principal) writing a contract, and a provider (agent)
who manages a panel of N patients and chooses a treatment intensity / effort
level `e` for each patient. Patients differ in severity `s`. The provider cannot
be perfectly monitored: the payor observes realized cost and a noisy quality
signal, but not true effort or true patient need (information asymmetry).

For each contract structure we run a Monte Carlo over the patient panel and
measure how the provider's privately optimal behavior compares to the social
optimum `e*`. The social optimum is the single welfare benchmark every contract
is scored against.

The model is deliberately built so that the canonical multitask result can either
appear or fail to appear depending on parameters, rather than being hard-wired.
FFS over-treatment, capitation under-treatment, and shared-savings as an
intermediate case are emergent outcomes of the effort-optimization, not assumed.

---

## 2. Agents

### 2.1 Payor (principal)
- Sets the contract: payment formula, any benchmark, any quality bonus / withhold.
- Cannot observe provider effort `e` or true patient need directly.
- Observes: realized cost `C_real`, and a noisy quality signal `q`.
- In the first build the payor is non-strategic: it posts a contract from a fixed
  menu and does not re-optimize against the provider's response. Endogenizing the
  payor's contract choice is a later extension (see "Next up").

### 2.2 Provider (agent)
- Has a panel of N patients.
- For each patient, chooses effort / treatment intensity `e >= 0`.
- May also decline a patient (the selection / cream-skimming margin), modeled as
  accepting a patient only if the patient's expected utility contribution clears
  an outside option.
- Is risk-averse with mean-variance preferences (parameter `rho`), and may carry
  intrinsic motivation (parameter `mu`) so mission-driven providers can be
  modeled.

---

## 3. Units and primitives

All quantities are in abstract units chosen so the baseline is well-scaled:

- `e` (effort / treatment intensity): dimensionless, `>= 0`. Loosely "intensity
  units" of care delivered to one patient.
- `s` (severity): dimensionless, mean normalized to ~1. Drives baseline cost and
  baseline outcome.
- Health value `V`, care cost `C`, payments, and income are in a common "value
  unit" so that `V - C` (social welfare) is meaningful. One value unit can be
  read as "one normalized PMPY of resource cost" if a dollar scale is wanted
  later; nothing in the model depends on that mapping.

Rationale for abstract units: the thesis claim is about the *direction and
relative size* of incentive distortions across contract types, which is
scale-free. Hard-coding dollars would imply a precision the model does not have.

---

## 4. Patients

Each patient `i` is drawn independently with a severity `s_i`.

- **Severity distribution:** `s ~ Gamma(shape = 2.0, scale = 0.5)`, giving mean
  `E[s] = 1.0` and a right skew.
  - Rationale: healthcare severity and spend are heavily right-skewed (a small
    share of patients drive most cost); Gamma is the standard positive,
    right-skewed, analytically convenient choice.

Severity drives both baseline expected cost and baseline outcome through the
`V` and `C` functions below.

---

## 5. Core mechanics (functional forms)

### 5.1 Health value `V(e, s)`
Concave and increasing in effort up to an interior peak, then declining
(over-treatment harms the patient beyond a point):

```
V(e, s) = alpha * s * e  -  beta * e^2
```

- `alpha * s * e`: marginal health value of effort is higher for sicker patients
  (treating a sick patient yields more health than treating a well one).
- `-beta * e^2`: over-treatment harm (iatrogenic harm, side effects,
  complications of unnecessary intervention). This is what creates an interior
  social optimum rather than "more is always better".
- Concavity in `e` requires `beta > 0`. Marginal health value
  `dV/de = alpha*s - 2*beta*e`.

Modeling shortcut (flagged): a single severity scalar `s` enters `V` linearly.
Real "appropriateness" is multidimensional. This is the deliberate reduction of
the unmeasured task to one index, which is exactly the Holmstrom-Milgrom setup.

### 5.2 Care cost `C(e, s)`
Increasing in effort and severity:

```
C(e, s) = c_base * s  +  c_eff * s * e
```

- `c_base * s`: baseline cost of having a patient of severity `s` on the panel,
  independent of effort (sicker patients cost more even at minimal care).
- `c_eff * s * e`: marginal resource cost of treatment intensity, scaling with
  severity (an extra unit of intensity costs more in a sicker patient).
- Rationale for the `s` interaction on the effort term: interventions in sicker
  patients consume more real resources per unit of intensity.

### 5.3 Provider's private effort cost `psi(e)`
Convex disutility of effort, separate from resource cost:

```
psi(e) = (gamma / 2) * e^2
```

- Rationale: convex effort cost is the standard agency assumption (the marginal
  burden of working harder rises). Captures provider time, attention, hassle.

### 5.4 Social optimum `e*`
The welfare benchmark. Per the project definition, `e*` maximizes health value
net of resource cost, `V - C` (it does **not** net out the provider's private
effort cost `psi`; see the flagged assumption in Section 12):

```
W_social(e, s) = V(e, s) - C(e, s) = alpha*s*e - beta*e^2 - c_base*s - c_eff*s*e
d/de = alpha*s - 2*beta*e - c_eff*s = 0
=>  e*(s) = s * (alpha - c_eff) / (2*beta)
```

- Interior and positive whenever `alpha > c_eff` (marginal health value of effort
  exceeds its marginal resource cost at the margin). With baseline defaults
  `e*(s) = 0.6 * s`, i.e. the first-best intensity scales linearly with severity.
- This closed form is used directly in code as the benchmark; the provider's
  chosen effort is solved separately (Section 7) and compared against it.

### 5.5 Noise / what the payor can and cannot see
- Realized care cost: `C_real = C(e, s) + eps_c`, with `eps_c ~ Normal(0, sigma_c^2)`.
  - Rationale: cost is realized with random shocks (complications, utilization
    luck). The payor observes `C_real`, not `C(e, s)` and not `e`.
- Quality signal: `q = V(e, s) + eps_q`, with `eps_q ~ Normal(0, sigma_q^2)`.
  - Rationale: the payor gets only an imperfect, noisy read on appropriateness /
    quality, never true effort. This is the unmeasured (or poorly measured) task.
  - In the baseline contracts 1 to 3 the quality signal is reported but not paid
    on; it becomes active under the optional P4P overlay (Section 6.5).

### 5.6 Risk adjustment and the benchmark
The benchmark is the payor's risk-adjusted estimate of what a patient "should"
cost. It is deliberately imperfect:

```
benchmark(s) = risk_mult(s) * C_ref(s)
risk_mult(s) = 1 + b_err + b_err_slope * (s - 1)   (floored above 0)
```

where `C_ref(s)` is a reference expected cost for severity `s` (the costing basis
differs by contract, see Section 6), `b_err` is the average-level benchmark error
(centered at mean severity `s = 1`), and `b_err_slope` is the severity gradient of
that error.

- This is the most important lever in the model. With `b_err = b_err_slope = 0`
  the benchmark is unbiased.
- Direction matters, and the sign is subtle. Because `C_ref(s)` is convex in
  severity (the effort-cost term scales as `s^2`), a purely *multiplicative*
  level error (`b_err` alone) does **not** reliably disadvantage the sick - it can
  actually overpay them. The realistic risk-adjustment failure - benchmarks that
  *under-adjust* for the sickest, i.e. their payment is compressed below true need
  - is captured by a **negative `b_err_slope`**: that is the lever that makes high
  severity unprofitable and drives cream-skimming against the sick (and the
  mirror-image upcoding incentive, since coding a patient as sicker raises the
  benchmark). A positive slope over-pays the sick and would skim the healthy.
- Baseline: `b_err = 0`, `b_err_slope = 0` (unbiased), so the baseline isolates
  pure incentive distortion from benchmark gaming. The benchmark-error sweep
  (queued) turns these on, with `b_err_slope < 0` as the canonical cream-skimming
  case.

---

## 6. Contract structures (the experimental treatments)

Notation: per-patient provider **net income** `pi`. The provider's objective
(Section 7) is mean-variance in `pi`. Payments and the share of resource cost the
provider bears are baked into each `pi` below.

### 6.1 Fee-for-service (FFS)
```
pi_FFS = phi0 + phi1 * e
```
- Provider is reimbursed per unit of intensity; the payor bears resource cost.
- `phi0`: base / visit payment (level only, does not affect the effort margin).
- `phi1`: marginal fee per unit intensity. The over-treatment driver: more `e`
  means more revenue, checked only by the provider's own convex effort cost.
- Income variance from the provider's view is ~0 (the provider does not bear cost
  risk). FFS is low-risk, high-volume-incentive.

### 6.2 Capitation
```
pi_CAP = K(s) - C_real
```
- Fixed risk-adjusted PMPM `K(s)`, provider bears 100% of realized resource cost.
- `K(s) = (1 + b_err) * C(e*, s)`: capitation is priced off the *appropriate*
  (social-optimum) cost for that severity.
  - Rationale: a well-designed capitation pays the expected cost of appropriate
    care. Using `e*` as the costing basis is the normative-benchmark choice and is
    stated as such. With perfect risk adjustment (`b_err = 0`) the provider breaks
    even on a patient treated at `e*`, so there is no *mechanical* selection
    incentive at baseline; the under-treatment incentive (every unit of `e` is a
    cost the provider eats) remains.
- Income variance = `sigma_c^2` (full cost-shock risk borne by provider). This is
  the risk-transfer that risk-averse providers dislike.

### 6.3 Shared savings, upside-only
```
pi_SS = phi0 + phi1 * e  +  s_share * max(benchmark(s) - C_real, 0)
```
- FFS underneath (provider still paid per intensity and does not directly bear
  resource cost), plus a bonus equal to `s_share` of cost coming in under
  benchmark, floored at zero (no downside).
- `benchmark(s) = (1 + b_err) * C(e_FFS, s)`: benchmark is built off *historical
  FFS practice cost*, i.e. the cost the provider would have incurred under
  unmanaged FFS.
  - Rationale: real shared-savings programs (e.g. MSSP) benchmark off historical
    spend, which embeds prior over-treatment. This makes the benchmark "loose"
    and savings relatively easy, a feature worth showing.
- `s_share`: shared-savings rate (one-sided programs run ~40% to 50%).
- The savings term pulls effort *down* (less intensity means lower cost means
  bigger bonus); the fee term pulls effort *up*. Net effort lands between FFS and
  capitation. Income variance is positive but bounded below at the FFS level by
  the zero floor (asymmetric, capped downside).

### 6.4 Two-sided risk (implemented, not in baseline run)
```
pi_2S = phi0 + phi1 * e  +  s_share * (benchmark(s) - C_real)
```
- Same as shared savings but with no floor: the provider shares both savings and
  losses. Symmetric, higher-variance, stronger cost-control incentive.
- Implemented in code for completeness but excluded from the first baseline run
  per the project plan (contracts 1 to 3 first). It is first in the "Next up"
  queue.

### 6.5 Optional quality bonus / withhold (P4P overlay)
Any contract above can carry an additive overlay on the noisy quality signal `q`:
```
pi := pi + b_q * (q - q_target)
```
- `b_q`: pay-for-performance power on the *measured* quality signal.
- Rationale: real VBC blends cost incentives with P4P. Critically, because `q` is
  noisy and only a proxy for true `V`, a high `b_q` rewards the signal, not the
  truth - this is the multitask distortion made explicit and is a key thing to
  sweep. Baseline `b_q = 0` (overlay off) so contracts 1 to 3 are clean.

---

## 7. Provider's optimization

For each patient the provider chooses effort `e >= 0` to maximize mean-variance
utility, with optional intrinsic motivation:

```
U(e | s) = E[pi(e, s)]  -  psi(e)  +  mu * E[V(e, s)]  -  (rho / 2) * Var(pi(e, s))
```

- `E[pi]`: expected net income under the contract.
- `psi(e) = (gamma/2) e^2`: private effort cost.
- `mu * E[V]`: intrinsic motivation / mission. A provider with `mu > 0` partly
  internalizes patient health value directly. Baseline `mu` is set positive but
  modest (see defaults) so capitation yields an interior under-treatment level
  rather than the degenerate "zero care" corner; the intrinsic-motivation sweep
  varies it.
- `(rho/2) Var(pi)`: risk penalty. `rho` is the coefficient of risk aversion.
  Baseline `rho = 0` (risk-neutral) so the baseline isolates the incentive /
  multitask distortion from the risk-transfer channel; the risk-aversion sweep
  turns it on, at which point capitation and two-sided risk are penalized for
  their income variance.

**Solution method.** Rather than rely on hand-derived first-order conditions for
every contract (the zero floor in shared savings makes that messy), the code
evaluates `U(e | s)` on a fine grid of `e` for every patient (vectorized) and
takes the argmax, respecting the `e >= 0` floor. For FFS and capitation this grid
solution is cross-checked against the closed-form optima:

```
e_FFS = (phi1 + mu*alpha*s) / (gamma + 2*mu*beta)
e_CAP = max( s*(mu*alpha - c_eff) / (gamma + 2*mu*beta), 0 )
```

The expected value of the shared-savings floor term uses the closed-form
truncated-normal expectation `E[max(m + Z, 0)] = m*Phi(m/sigma) + sigma*phi(m/sigma)`
with `m = benchmark - E[C]`, `Z ~ Normal(0, sigma_c^2)`, so the savings incentive
is exact, not simulated, inside the optimizer.

**Selection / cream-skimming.** After computing the per-patient optimum `U*(s)`,
the provider accepts the patient only if `U*(s) >= outside_option` (default 0).
The set of declined patients, and how decline correlates with severity, is the
cream-skimming output. At baseline (`b_err = 0`) selection should be near zero;
the benchmark-error sweep is what activates it.

---

## 8. Monte Carlo structure

One simulation run = one draw of a panel. For the baseline we pool a large number
of independent patient draws:

1. Draw `N_patients` severities `s_i` from the Gamma.
2. For each contract, solve the provider's optimal effort `e_i` and acceptance
   decision (Section 7), deterministically given `s_i` and parameters.
3. Draw one cost shock `eps_c,i` and one quality shock `eps_q,i` per patient and
   realize `C_real`, `q`, `pi`, and welfare. (One patient = one Monte Carlo
   trial; with `N_patients` in the 1e5 range this gives tight summary statistics.)
4. Aggregate the outputs in Section 9 per contract.

- Baseline `N_patients = 100000`. Rationale: large enough that reported means /
  rates are Monte Carlo-stable to ~3 significant figures, cheap enough to run in
  seconds.
- A panel grouping `N_panel` (default 2000, ~ order of a Medicare ACO's attributed
  lives) is available for panel-level income-variance reporting, which is the
  relevant unit when the risk-aversion channel is switched on.

The harness is config-driven (all of Section 11 lives in a config object / YAML),
so parameters can be swept without touching core logic. The parameter-sweep module
re-runs the Monte Carlo across a grid of any parameter(s) and collects summaries.

---

## 9. Outputs measured (per contract, across the Monte Carlo)

1. **Social welfare:** mean of `V(e, s) - C(e, s)` at chosen effort (expected and
   realized). The headline alignment number.
2. **First-best welfare and welfare gap:** mean `W_social(e*, s)` and the
   deadweight loss `W_social(e*) - W_social(e_chosen)` = allocative inefficiency.
3. **Allocative efficiency ratio:** achieved welfare / first-best welfare.
4. **Provider income:** mean and standard deviation of realized `pi` (the SD is
   the risk the provider bears, which is what couples to `rho`).
5. **Over- vs under-treatment:** fraction with `e_chosen > e*` (over) and
   `< e*` (under), plus the mean signed gap `E[e_chosen - e*]` and `E[e_chosen/e*]`.
6. **Patient selection / cream-skimming:** overall acceptance rate, acceptance
   rate by severity quartile, and a cream-skimming index (acceptance-rate gap
   between the lowest and highest severity quartiles).
7. **Distance from social optimum:** mean `|e_chosen - e*|`, complementing the
   welfare gap as a pure-behavior (non-welfare-weighted) measure.

---

## 10. Plots (first build)

- Social welfare by contract (bar).
- Provider income mean +/- SD by contract (bar with error bars).
- Treatment intensity vs `e*`: mean chosen `e` against severity, per contract,
  with the `e*(s)` first-best line overlaid.
- Bonus: acceptance rate by severity quartile, per contract (selection view).

---

## 11. Parameters and defaults (each with a one-line rationale)

| Param | Symbol | Default | Rationale |
|---|---|---|---|
| Severity shape | `sev_shape` | 2.0 | Right-skewed severity/spend; Gamma shape. |
| Severity scale | `sev_scale` | 0.5 | Sets `E[s] = shape*scale = 1.0` (normalized). |
| Health value slope | `alpha` | 1.0 | Marginal health value of effort per unit severity. |
| Over-treatment curvature | `beta` | 0.5 | Penalty on excess intensity; creates interior `e*`. |
| Baseline cost slope | `c_base` | 0.5 | Cost of a severity-`s` patient at minimal care. |
| Effort cost slope (care) | `c_eff` | 0.4 | Marginal resource cost of intensity; `< alpha` so `e* > 0`. |
| Provider effort cost | `gamma` | 0.3 | Convex private disutility of effort. |
| Intrinsic motivation | `mu` | 0.5 | Mission weight; keeps capitation interior, not zero-care. |
| Risk aversion | `rho` | 0.0 | Baseline risk-neutral to isolate incentive channel. |
| Cost shock SD | `sigma_c` | 0.3 | Idiosyncratic cost realization noise. |
| Quality signal SD | `sigma_q` | 0.3 | Imperfect, noisy quality measurement. |
| FFS base payment | `phi0` | 0.3 | Visit/base level (no effort-margin effect). |
| FFS marginal fee | `phi1` | 0.4 | Per-intensity fee; tuned so FFS over-treats vs `e*`. |
| Shared-savings rate | `s_share` | 0.5 | One-sided MSSP-style ~50% share. |
| Benchmark level error | `b_err` | 0.0 | Average benchmark error (centered at mean severity); unbiased baseline. |
| Benchmark error slope | `b_err_slope` | 0.0 | Severity gradient of benchmark error; `< 0` under-adjusts the sick = cream-skimming lever. |
| P4P power | `b_q` | 0.0 | Overlay off at baseline; multitask-distortion lever. |
| Quality target | `q_target` | 0.0 | Reference point for P4P overlay. |
| Outside option | `outside_option` | 0.0 | Accept patient iff `U* >= 0`. |
| Patients (MC) | `n_patients` | 100000 | Tight summary stats, runs in seconds. |
| Panel size | `n_panel` | 2000 | ~ ACO attributed-lives scale for panel-variance view. |
| Seed | `seed` | 12345 | Reproducibility. |

**Baseline calibration check (by construction):** with these defaults,
`e*(s) = 0.6*s`, `e_FFS(s) = (0.4 + 0.5*s)/0.8 = 0.5 + 0.625*s` (over-treats, and
*most* for low-severity patients where the flat fee dominates need), and
`e_CAP(s) = 0.125*s` (under-treats). Shared savings lands between. So the
canonical FFS-over / capitation-under / shared-savings-intermediate ordering is
an emergent baseline result, not an assumption, and the build is expected to
reproduce it. Any failure to do so is a bug or a miscalibration to investigate.

---

## 12. Assumptions and modeling shortcuts (read before trusting numbers)

1. **Static, single-period.** No dynamics, no learning, no patient health
   trajectory across years. VBC's multi-year benchmark ratchet (this year's
   savings lower next year's benchmark) is out of scope for the first build.
2. **One-dimensional appropriateness.** The unmeasured task is collapsed to the
   scalar `V`. This is the intended Holmstrom-Milgrom reduction, but real quality
   is multidimensional; do not read `V` as any single clinical measure.
3. **Social optimum excludes provider effort cost.** Per the project definition,
   `e*` maximizes `V - C`, not `V - C - psi`. Including `psi` would lower `e*`
   slightly. The choice is defensible (psi is a private hassle cost, not a
   resource the payor buys) but it is a choice; an alternative welfare benchmark
   `V - C - psi` is a trivial switch and is noted as a sensitivity.
4. **Payor is non-strategic.** Contracts come from a fixed menu; the payor does
   not solve for an optimal contract against the provider's response. Endogenous
   contract design is a later extension.
5. **Provider optimizes patient-by-patient.** Effort on patient `i` does not
   depend on the rest of the panel (no shared budget, no capacity constraint).
   This keeps the optimization separable and transparent; a panel-budget version
   is a possible extension.
6. **Risk enters only through income variance, baseline risk-neutral.** At
   `rho = 0` the variance term is inert; income SD is still *reported* so the
   risk story is visible, but it does not bend effort until the risk-aversion
   sweep turns `rho` on.
7. **Normal cost/quality shocks.** Additive Gaussian noise is analytically
   convenient (closed-form truncated-normal savings expectation) but allows
   negative draws in the tails; magnitudes are small relative to means at
   baseline, so this is a minor approximation, flagged.
8. **Capitation and shared-savings costing bases differ by design** (`e*` for
   capitation, historical-FFS `e_FFS` for shared savings). This is intentional
   and realistic, but it means the two contracts are not scored against an
   identical benchmark; cross-contract welfare comparison is always made against
   the *single* social optimum `e*`, not against each contract's own benchmark.
9. **Declined patients are externalized.** Cream-skimmed patients leave the
   provider's welfare accounting; the model flags the selection rate rather than
   tracking those patients' downstream welfare. Quantifying the welfare loss from
   selection is a later extension.

---

## 13. Next up (queue after the first baseline build)

1. **Two-sided risk** into the baseline comparison (class already implemented).
2. **Benchmark-error / cream-skimming sweep:** vary `b_err` and especially
   `b_err_slope` (negative = under-adjust the sick) to trace selection and
   upcoding incentives.
3. **Risk-aversion sweep:** turn on `rho`, show how risk transfer penalizes
   capitation and two-sided risk for high-`mu`/low-`mu` providers.
4. **Intrinsic-motivation sweep:** vary `mu`, show mission-driven providers
   resisting both over- and under-treatment, and how that substitutes for
   contract power.
5. **P4P overlay analysis:** vary `b_q`, show the multitask distortion where
   paying on the noisy quality signal pulls effort toward the measure, not the
   truth.
6. Later: dynamic benchmark ratchet; endogenous payor contract choice; panel
   budget / capacity constraints; welfare accounting for selected-out patients.
