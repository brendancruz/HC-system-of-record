# Diagnostics Comps

**Sub-sector:** Diagnostics (cancer screening, liquid biopsy, genomic/molecular testing)
**As of:** 2026-06-13 (prices & market caps via FMP; revenue/growth/margin from FY2025
company releases and guidance)
**Source CSV:** [`diagnostics.csv`](./diagnostics.csv)

Multiple shown is **Price/Sales (market cap / FY2025 revenue)** as a proxy for EV/Sales.
True EV/Sales needs net debt/cash, which the current FMP plan tier does not expose - so
net-cash/net-debt distortions are flagged in Notes (most important: FLGT).

| Company | Ticker | Price | Mkt Cap | FY2025 Rev | Rev Growth | Gross Margin | P/S | 2026E P/S |
|---|---|---|---|---|---|---|---|---|
| Natera | NTRA | $212.07 | ~$30.4B | $2.31B | +36% | ~65% | 13.2x | n/a |
| Exact Sciences* | EXAS | $104.91 | ~$20.0B | $3.25B | +18% | ~73% (adj) | 6.2x | n/a |
| Guardant Health | GH | $131.62 | ~$17.45B | ~$0.97B | +31% | ~64-65% | 17.9x | 13.3x |
| Tempus AI | TEM | $47.82 | ~$8.35B | $1.27B | +83% | ~52% (est) | 6.6x | 5.3x |
| GeneDx | WGS | $59.92 | ~$1.78B | ~$0.43B | ~+40% | ~74% (adj) | 4.2x | n/a |
| NeoGenomics | NEO | $11.15 | ~$1.43B | ~$0.74B | +11% | ~47% | 1.9x | n/a |
| Fulgent Genetics | FLGT | $18.68 | ~$0.53B | $0.32B | +14% | ~38% (est) | 1.6x | n/a |

\* **Exact Sciences is no longer freely traded** - acquired by Abbott (~$21B equity,
$105/share, closed 2026-03-23). Price is pinned near the deal price; multiple shown is
effectively the take-out multiple (~6.2-6.5x sales).

**Summary stats (P/S):** median ~6.2x, mean ~7.4x, range 1.6x (FLGT) to 17.9x (GH).

## Outliers & reads

- **GH - highest multiple (17.9x trailing / ~13x fwd).** The market is paying for Shield
  blood-based CRC screening optionality on top of a 25%+ growing oncology base, despite
  negative EBITDA. This is the "screening TAM premium" anchor.
- **NTRA - biggest name, rich at 13.2x on +36% growth.** Signatera MRD is the engine.
  Premium is growth-justified rather than optionality-driven.
- **EXAS - the take-out benchmark (~6.2-6.5x).** A profitable, scaled screening
  franchise cleared at ~6x sales - the reference point for what a strategic pays for
  cash-generative diagnostics vs. the double-digit multiples on pre-profit growth.
- **TEM - fastest grower (+83%) yet only ~6.6x.** Growth is Ambry-inflated (~30%
  organic); the data/Insights business is the potential re-rate catalyst.
- **WGS - turnaround re-rate (4.2x).** Exome/genome revenue +53-55% with ~74% adj. GM;
  cheaper than the growth leaders, room to converge if growth holds.
- **NEO - low-multiple value/legacy (1.9x).** Slower growth, lower margin, mid-NGS-mix
  transition. The "show me" name.
- **FLGT - cheapest on EV, and the P/S is misleading.** Post-COVID net cash exceeds its
  market cap, so true **EV/Sales is near zero**. Do not read 1.6x P/S as expensive - the
  story is cash-on-balance-sheet plus a small, slow-growing core.

## Caveats
- P/S uses market cap, not EV. Convertible/term debt (GH, NTRA, TEM) lifts true EV/Sales
  modestly; large net cash (FLGT) cuts it sharply.
- NEO market cap is computed from price x shares because the FMP market-cap field looked
  internally inconsistent on 2026-06-13.
- WGS and NEO FY2025 revenue use the latest company guidance midpoints; refresh to
  reported actuals next run.
- Gross margins mix GAAP and adjusted/non-GAAP across companies (labeled where adj.).

## Next-run TODO
- Replace guidance-based revenue with reported FY2025 actuals (NEO, WGS).
- Add net debt/cash to convert P/S -> true EV/Sales once a higher FMP tier or balance-sheet source is available.
- Consider adding EV/EBITDA for the (few) EBITDA-positive names.
