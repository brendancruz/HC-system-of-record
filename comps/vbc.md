# VBC (Value-Based Care) Comps

**Sub-sector:** Value-based care - physician enablement, risk-bearing care delivery, and enabling data/tech
**As of:** 2026-06-14 (public prices/market caps via FMP; financials from FY2025 releases; private valuations from web search, labeled est.)
**Source CSV:** [`vbc.csv`](./vbc.csv)

VBC does **not** value on EV/Sales - for full-risk models (agilon, P3) revenue is mostly
pass-through insurance premium, so the sales multiple is meaningless. The right frames are
**EV/EBITDA**, **adj. EBITDA margin**, **risk model**, and **per-member economics / medical
margin**. Enabling-software names (Innovaccer) screen on **ARR multiples** instead.

| Company | Ticker | Price | Mkt Cap | FY2025 Rev | FY2025 Adj EBITDA | EBITDA Margin | EV/EBITDA | Risk model |
|---|---|---|---|---|---|---|---|---|
| Privia Health | PRVA | $23.43 | ~$2.95B | $2.12B | $125.5M | 5.9% | ~19.7x | Capital-light (upside shared-savings) |
| Astrana Health | ASTH | $38.62 | ~$1.91B | $3.18B | $205.4M | 6.5% | ~9-11x | Delegated risk + owned delivery + tech |
| agilon health | AGL | n/a* | ~$1.9B | $5.93B | -$296M | neg. | n/m | Full-risk Medicare Advantage |
| P3 Health Partners | PIII | $12.23 | ~$0.04B | $1.46B | -$161.3M | neg. | n/m | Full-risk Medicare Advantage (distressed) |
| Aledade | Private | n/a | ~$3.5B (est.) | ~$0.75B (est.) | n/a | n/a | Capital-light ACO / shared-savings |
| Innovaccer | Private | n/a | ~$3.5B (est.) | ~$0.25B ARR (est.) | n/a | n/a | Enabling data/AI software |

\* agilon price/share-count from FMP looked unreliable on 2026-06-13; market cap ~$1.9B used.

## The central read: risk structure drives valuation
The single most useful VBC framing - structure determines who makes money:
- **Capital-light upside-share (Privia, Aledade):** take shared-savings *upside* without full
  insurance downside. Result: positive, stable EBITDA and premium multiples. Privia at ~19.7x
  EV/EBITDA with net cash is the public exemplar.
- **Delegated/diversified risk + owned delivery (Astrana):** more risk than Privia but
  diversified across payer lines and vertically integrated; profitable and the cheapest
  profitable name (~9-11x). The "roll-up that works."
- **Full-risk Medicare Advantage (agilon, P3):** take total-cost-of-care risk. When MA cost
  trend runs hot, medical margin goes negative fast - both are EBITDA-negative; P3 is in
  going-concern distress. High operating leverage, both directions.
- **Enabling software (Innovaccer):** not risk-bearing at all - recurring ARR, valued on a
  software multiple (~14x ARR est.), structurally above the care-delivery names.

## Outliers & reads
- **P3 - distressed bookend.** Going concern, 1-for-50 reverse split, ~$40M market cap. A
  special-situations name, not a clean comp.
- **agilon - negative-EBITDA turnaround.** Large revenue (pass-through premium) but -$296M
  EBITDA; the value is an option on medical-margin recovery.
- **Astrana - the value pick among profitable names.** ~46% cheaper than Privia on EV/EBITDA
  despite faster (acquisition-fueled) growth; the gap is the acquisition leverage and execution risk.
- **Privia - quality premium.** Net cash, GAAP-profitable, ~39% EBITDA growth justify the top multiple.
- **Innovaccer - the software outlier.** ARR multiple, not EBITDA - belongs in the conversation
  as the data/tech layer, not as a care-delivery comp.

## Caveats
- EV/EBITDA uses market cap +/- net debt where known. Astrana shown as mkt-cap/EBITDA (~9.3x);
  true EV/EBITDA ~11x with Prospect acquisition debt (balance-sheet data not on current FMP tier).
- Privia EV reflects ~$480M net cash. agilon/P3 EBITDA negative -> EV/EBITDA n/m.
- Private valuations (Aledade June 2023, Innovaccer Jan 2025) are last-round marks and likely stale.

## Next-run TODO
- Add net debt for ASTH (and agilon) to firm up EV/EBITDA.
- Add per-member / medical-margin columns (PMPM economics) for the full-risk names.
- Refresh private marks (Aledade especially - 2023 is old) and any IPO filings.
