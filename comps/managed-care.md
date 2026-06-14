# Payor-Provider / Managed Care Comps

**Sub-sector:** Managed care - integrated payors and Medicare Advantage operators
**As of:** 2026-06-14 (prices/market caps via FMP; financials from FY2025 releases & 2026 outlooks)
**Source CSV:** [`managed-care.csv`](./managed-care.csv)

Payors value on **P/E (adjusted EPS)**, not EV/Sales or EV/EBITDA - the key operating metric is
the **medical loss ratio (MLR) / benefit ratio** (premium spent on medical care; lower is
better). The MA-insurtech name (ALHC) is the exception - barely GAAP-profitable, so it screens
on EV/EBITDA and growth instead.

| Company | Ticker | Price | Mkt Cap | FY2025 Rev | FY2025 Adj EPS | P/E | 2026E P/E | MLR / Benefit Ratio |
|---|---|---|---|---|---|---|---|---|
| UnitedHealth Group | UNH | $408.52 | ~$371B | ~$450B (est.) | $16.35 | ~25.0x | ~23.0x | 89.1% |
| Elevance Health | ELV | $404.07 | ~$87.7B | $197.6B | ~$30.00 | ~13.5x | n/a | 90.0% |
| Humana | HUM | $379.22 | ~$45.5B | ~$128B | ~$17.00 | ~22.3x | n/a | ~90.3% |
| Alignment Healthcare | ALHC | $19.75 | ~$4.08B | $3.9B | n/m | n/m | n/m | 87.5% (MBR) |

## The 2025 story: MA cost shock, and who handled it
The defining managed-care theme is the Medicare Advantage medical-cost spike and how each name absorbed it:
- **UNH - the bellwether reset.** MCR jumped ~340 bps to 89.1%, adj. EPS fell to $16.35, Stephen
  Hemsley returned as CEO, and DOJ scrutiny of MA practices intensified. Still the richest
  multiple (~25x) on Optum's services growth - but the premium now carries real risk.
- **HUM - the pure-play in the eye of the storm.** Most MA-levered, shed ~425k members to protect
  margin, and is **suing CMS over its 2025 Star Ratings** (a direct hit to 2026 quality bonuses).
  ~22x P/E sits on trough earnings.
- **ELV - the cheap, diversified one.** ~13.5x P/E, roughly half UNH's multiple. Commercial BCBS
  + Medicaid cushion the MA exposure, but Medicaid redeterminations and medical trend pushed the
  benefit ratio to 90.0%. The value/convergence case.
- **ALHC - the counter-narrative.** While incumbents' MLRs rose, Alignment's **MBR fell 130 bps to
  87.5%** as revenue grew ~46% - "MA done right." Trades on growth/EBITDA (~37x mkt-cap/EBITDA),
  not P/E.

## Outliers & reads
- **Multiple spread (UNH ~25x vs. ELV ~13.5x)** is the headline - it is essentially a bet on
  services mix (Optum vs. Carelon) and on whose MA margin recovers fastest. ELV is the value
  side; UNH is quality-at-a-price with overhangs.
- **MLR is the tell.** ALHC (87.5%, falling) is the standout; the big three sit ~89-90% and
  rising - the entire 2025 margin-compression story in one number.
- **ALHC's ~37x EBITDA** is a growth premium, not comparable to the big payors' P/E - keep it in
  its own lane.

## Caveats
- UNH FY2025 revenue (~$450B) is estimated from segment disclosures (UnitedHealthcare $344.9B +
  Optum $270.6B, less intercompany eliminations); confirm consolidated figure next run.
- ELV 2026 guidance cited is a **GAAP** EPS floor (>= $22.30); adjusted EPS guidance is higher -
  confirm the adjusted 2026 figure before quoting a clean forward P/E.
- MLR/benefit-ratio definitions differ slightly by company (consolidated MCR vs. insurance-segment
  benefit ratio vs. MBR); directionally comparable, not identical.

## Next-run TODO
- Confirm UNH consolidated FY2025 revenue and each name's reported (not guidance) MLR.
- Add 2026E adjusted EPS for ELV and HUM to complete the forward P/E row.
- Add MA membership and Star-Ratings status as columns (key MA value drivers).
