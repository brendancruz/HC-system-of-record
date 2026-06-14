# FINDINGS.md - Baseline run (contracts 1 to 3)

**What this is:** the read on the first baseline Monte Carlo (100,000 patients,
default config in `config/default.yaml`, seed 12345). FFS, capitation, and
shared-savings (upside-only) only. Two-sided risk is implemented but queued.
Numbers below are reproducible with `python run_baseline.py`. See MODEL.md for
the spec and every parameter rationale.

> Baseline is deliberately risk-neutral (`rho = 0`) and benchmark-unbiased
> (`b_err = 0`), so this run isolates the pure incentive / multitask distortion.
> The risk and selection channels are switched off here on purpose and are the
> next sweeps.

---

## Headline numbers

| Contract | Social surplus / patient | Efficiency vs first-best | Over-treat | Under-treat | Mean effort gap (e - e*) | Provider income (mean) | Income risk (SD) |
|---|---|---|---|---|---|---|---|
| First-best `e*` | 0.271 | 100% | - | - | 0 | - | - |
| Fee-for-service | 0.133 | 49% | 100% | 0% | +0.53 | 0.751 | 0.177 |
| Capitation | 0.101 | 37% | 0% | 99.9% | -0.48 | 0.284 | 0.527 |
| Shared savings (upside) | 0.197 | 73% | 94% | 5% | +0.35 | 0.783 | 0.221 |

"Surplus" = social welfare measured above the no-treatment baseline (the part
effort actually moves; the fixed per-patient baseline cost is netted out so the
efficiency ratio is interpretable). Efficiency = surplus captured / first-best
surplus.

---

## Five observations, framed for the thesis

**1. The Holmstrom-Milgrom prediction reproduces cleanly and emergently.** Nobody
told the providers to over- or under-treat. Each one just maximized private
utility under the contract. Yet FFS lands every patient on the over-treatment
side of `e*` (mean intensity +0.53 above optimum) and capitation lands 99.9% of
patients on the under-treatment side (-0.48 below). When the payor can write a
high-powered incentive only on the measurable task (cost / volume) and not on the
unmeasured one (appropriateness), provider effort distorts toward whatever the
contract actually pays for. This is the verbal multitask argument turned into
numbers, which is the point of the model.

**2. Shared savings is the most efficient of the three, but not because it is
"balanced" - because it is loose.** Upside-only shared savings captures 73% of
first-best surplus versus 49% (FFS) and 37% (capitation). It does best because it
keeps the FFS fee (which pulls effort up) while adding a savings bonus (which
pulls effort down), landing closer to `e*`. But the benchmark is built off
historical FFS practice cost, i.e. off the over-treatment baseline, so savings are
easy and the provider still over-treats 94% of patients - just less than under
pure FFS. The efficiency gain is real but it is partly an artifact of a generous
benchmark, which is exactly the critique to make of real upside-only ACO design.

**3. FFS does not over-treat everyone - it over-serves the easy and under-serves
the sick.** The intensity-vs-severity plot shows the FFS line crossing the `e*`
line: FFS over-treats low and mid-severity patients (where the flat fee dominates
need) but actually under-treats the most complex patients (the fee does not scale
steeply enough with severity). So "FFS causes over-treatment" is too coarse. The
sharper claim the model supports: volume-based payment mis-allocates effort toward
low-need patients and away from high-need ones. That maldistribution, not just the
average level, is the welfare loss.

**4. The risk that capitation transfers is visible and large.** Provider income
SD is 0.53 under capitation versus 0.18 under FFS - roughly 3x the income
volatility - because the capitated provider eats the full cost shock while the FFS
provider bears none. At baseline this risk does not yet bend behavior (`rho = 0`),
but the gap is the whole reason a risk-averse provider would demand a premium to
accept capitation, and it is why small practices cannot hold full risk. The
risk-aversion sweep will turn this latent risk into a behavioral and welfare cost.

**5. No cream-skimming yet - and that is the correct baseline result, not a null
finding.** With an unbiased, severity-adjusted benchmark (`b_err = 0`), every
patient clears the provider's participation constraint under all three contracts
(acceptance 100%, cream-skim index 0). This confirms the selection channel is
driven by benchmark error, not by contract type per se. It sets up the key
experiment: re-run with a benchmark that under-adjusts for severity and watch
capitation (and two-sided risk) start declining the sick. Selection is a
benchmark-design failure, which is the more useful and more defensible claim than
"capitation causes cream-skimming."

---

## One-line takeaway

Under these defaults, none of the three contracts reaches the social optimum;
upside-only shared savings gets closest (73%) by softening FFS rather than by
aligning incentives, FFS mis-allocates effort toward low-need patients, and
capitation under-treats while loading risk onto the provider - all emergent from
private optimization, exactly as the multitask principal-agent model predicts.

---

## Next up (queue)

1. **Two-sided risk** into the comparison (class implemented).
2. **Benchmark-error / cream-skimming sweep** (`b_err_slope < 0`, under-adjusting
   the sick) - the experiment that should activate patient selection and upcoding.
3. **Risk-aversion sweep** (`rho`) - price the capitation/two-sided risk premium
   and show its welfare cost.
4. **Intrinsic-motivation sweep** (`mu`) - mission-driven providers as a
   substitute for contract power.
5. **P4P overlay** (`b_q`) - the multitask distortion of paying on a noisy
   quality signal.
