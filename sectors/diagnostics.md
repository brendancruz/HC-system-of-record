# Diagnostics - Sector Overview

**Sub-sector:** Diagnostics (cancer screening, liquid biopsy, MRD, genomic/molecular testing)
**Angle:** Reimbursed, recurring molecular testing is re-rating around two TAMs - asymptomatic
screening and minimal residual disease (MRD) - while large-cap medtech sets the take-out floor.
**Overview last updated:** 2026-06-14
**Universe:** the 7 profiled diagnostics names (see [comps](../comps/diagnostics.md)).

This is a sector primer that sits on top of the company profiles and the diagnostics comps
table. Company-level figures are sourced in their own profiles; this note aggregates and
frames them. Broad market-size (TAM) figures that are not bottom-up from the profiled
universe are labeled `[UNSOURCED]` per `_schema.md` - they should be sourced before quoting
externally.

---

## Market size & growth (bottom-up from the profiled universe)

Built from FY2025 reported/guided revenue in [`diagnostics.csv`](../comps/diagnostics.csv):

| Cut | Figure | Note |
|---|---|---|
| Profiled-universe FY2025 revenue | **~$9.3B** | sum of the 7 names below |
| Profiled-universe market cap | **~$79.9B** | sum of mkt caps, as of 2026-06-13 (EXAS pinned at deal price) |
| Revenue-weighted growth | **~+30%** (est.) | weighted by FY2025 revenue across the 7 names |
| Aggregate P/S | **~8.6x** | $79.9B / $9.3B; skewed up by GH/NTRA optionality premiums |

Per-name FY2025 revenue (sourced in comps): Exact Sciences $3.25B, Natera $2.31B, Tempus
$1.27B, Guardant $0.97B, NeoGenomics $0.73B, GeneDx $0.43B, Fulgent $0.32B.

> This is the *profiled coverage universe*, not the total diagnostics market. The broader US
> clinical-lab / molecular-diagnostics TAM (reference labs like Quest/Labcorp, plus the
> screening and MRD opportunity) is far larger and is `[UNSOURCED]` here - add a sourced
> TAM (e.g., screening-eligible population x ASP, MRD-eligible incidence) in a future run.

**Growth is barbelled, not uniform.** The fast cohort (TEM +83% Ambry-inflated/~30% organic,
WGS ~+40%, NTRA +36%, GH +31%) is compounding on screening/MRD/exome demand; the slow cohort
(EXAS +18% scaled-and-profitable, FLGT +14%, NEO +10%) is mature lab volume. The sector's
headline growth narrative is carried by the first group.

---

## Structure & value chain

**Where the money is made:** volume x ASP. A test is ordered (physician or screening
protocol), the sample is run (the lab / assay), a result is reported, and a payor reimburses
(Medicare + commercial). The defensible economics come from three places: **reimbursement
coverage** (a covered CPT/Medicare rate is the moat), **guideline inclusion** (drives ordering
volume), and **menu/scale** (fixed-cost lab leverage). Margin profile in the universe runs
~38% to ~74% gross, widening with molecular mix and scale.

**Four functional layers in the profiled universe:**

1. **Screening (asymptomatic population)** - the largest-TAM bet. Exact Sciences (Cologuard,
   now Abbott) is the scaled, profitable stool-based incumbent in colorectal; Guardant (Shield)
   is the blood-based challenger pricing in optionality. This layer earns the richest multiples.
2. **Precision oncology / liquid biopsy (therapy selection)** - Guardant360, Tempus, Natera.
   Reimbursed advanced-cancer testing; the established commercial core.
3. **MRD / recurrence monitoring** - Natera Signatera (the engine of its +36%), Guardant Reveal.
   Recurring, longitudinal testing per patient; the highest-conviction growth vector after screening.
4. **Genomic / molecular & legacy lab** - GeneDx (exome/genome, +53-55% in that line),
   NeoGenomics and Fulgent (broader/legacy lab menus). Spans a turnaround re-rate (WGS) to
   show-me value (NEO, FLGT).

**Adjacent players that bound the universe (not profiled here):** Roche/Foundation Medicine
(tissue + liquid CGP), Grail (multi-cancer early detection), Quest/Labcorp (reference-lab
scale). Flagged as expansion candidates in `_index.md`.

---

## Key drivers

- **Reimbursement is the moat, and the swing factor.** A covered test with a defensible
  Medicare/commercial rate is the whole game; coverage decisions and ASP are the primary
  catalysts and the primary risk. (See GH Shield payor-coverage build as the live example.)
- **Guideline inclusion converts TAM into volume.** Screening adoption tracks guideline
  endorsement (USPSTF / society guidelines) more than clinical novelty.
- **Two structural TAMs are re-rating the group:** (1) blood-based **screening** of large
  asymptomatic populations, and (2) **MRD** - recurring per-patient monitoring. These are why
  pre-profit names (GH ~18x, NTRA ~13x P/S) trade above scaled-profitable ones.
- **Scale + profitability, not just growth, is what clears M&A.** Abbott paid ~6.5x sales /
  ~52x adj. EBITDA for Exact Sciences - a cash-generative recurring franchise - *below* the
  double-digit sales multiples on pre-profit growth peers.
- **Data/AI optionality as a second act.** Tempus (data/Insights) is the cleanest example of
  a testing franchise trying to re-rate on a data layer rather than test volume alone.

---

## What's changed / why now (2026)

- **Abbott / Exact Sciences (~$21B equity, $105/sh, closed 2026-03-23)** is the marquee deal
  of the cycle. It reframes dx M&A: large-cap medtech will pay up for **cash-generative,
  reimbursed, recurring screening at ~6-7x sales**, setting a floor/anchor for the screening
  field and validating the scarcity value of reimbursed franchises. See
  [deal entry](../deals/2026-03-abbott-exact-sciences.md).
- **The valuation framework has bifurcated.** Two coherent anchors now exist side by side: a
  **take-out anchor** (~6-7x sales for profitable scale, EXAS) and a **screening/MRD TAM
  premium** (double-digit sales for pre-profit optionality, GH/NTRA). Any name can be placed
  against those two poles.
- **Consolidation is active around data + menu**, e.g. Tempus / Ambry Genetics (+ Deep 6 AI,
  Paige), closed 2025-02-03 - genomics menu plus a data/AI thesis. See
  [deal entry](../deals/2025-02-tempus-ambry-genetics.md).
- **The growth leaders are now real-revenue businesses, not concepts** - Natera at $2.3B,
  Tempus at $1.27B - so the debate has moved from "is the test real" to "what multiple does
  recurring molecular revenue deserve."

---

## How the names sort (the one-screen read)

- **High-multiple optionality anchor:** Guardant (GH) ~18x trailing / ~13x fwd - Shield
  screening on a 25%+ oncology base; the "screening TAM premium" name.
- **Largest, growth-justified premium:** Natera (NTRA) 13.2x on +36% - Signatera MRD engine.
- **Take-out benchmark:** Exact Sciences (EXAS) ~6.5x - what a strategic pays for profitable
  scale; no longer freely traded.
- **Fastest grower, cheap optically:** Tempus (TEM) +83% / ~6.6x - Ambry-inflated; data
  business is the re-rate wildcard.
- **Turnaround re-rate:** GeneDx (WGS) 4.2x - exome/genome +53-55%, ~74% adj. GM.
- **Show-me value / legacy:** NeoGenomics (NEO) ~2x, Fulgent (FLGT) ~1.6x - and FLGT's P/S is
  misleading (net cash exceeds market cap, so true EV/Sales is ~0).

---

## Why it matters for HC coverage (the banker read)

Diagnostics is the sub-sector where the *valuation question* is sharpest: the same income
statement (high-growth, often pre-profit, reimbursement-dependent) gets a 1.6x or an 18x sales
multiple depending entirely on which TAM story (legacy lab vs. screening/MRD optionality) the
market believes. The two 2026 anchors - Abbott/EXAS on the take-out side and GH/NTRA on the
optionality side - let you place any dx name on a single spectrum in one sentence, which is the
fluent-sounding move in a coverage conversation. The recurring tell to watch is reimbursement
and guideline news, not assay novelty.

---

## Sources

- [`comps/diagnostics.md`](../comps/diagnostics.md) and [`comps/diagnostics.csv`](../comps/diagnostics.csv)
  - prices/market caps (FMP, 2026-06-13); FY2025 revenue/growth/margin from company releases.
- Company profiles in [`/companies/`](../companies/) for the 7 names (per-figure sourcing there).
- [`deals/2026-03-abbott-exact-sciences.md`](../deals/2026-03-abbott-exact-sciences.md) and
  [`deals/2025-02-tempus-ambry-genetics.md`](../deals/2025-02-tempus-ambry-genetics.md).
- Aggregates (universe revenue ~$9.3B, market cap ~$79.9B, weighted growth ~+30%) computed in
  this note from the comps CSV (2026-06-14).
- Broad diagnostics-market TAM figures are deliberately omitted as `[UNSOURCED]` pending a
  sourced top-down estimate.
