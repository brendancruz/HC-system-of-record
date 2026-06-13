# HC Coverage System of Records - Master Index

A version-controlled knowledge base for healthcare coverage prep: diagnostics,
value-based care (VBC), and payor-provider / managed care. Built to compound -
every session adds or refreshes entries. Target use: sounding fluent in HC coverage
conversations (BofA HC group).

**Index last updated:** 2026-06-13
**Conventions & profile template:** see [`_schema.md`](./_schema.md)

---

## Companies

### Diagnostics
| Company | Ticker | Profile | Updated |
|---|---|---|---|
| Exact Sciences (acq. by Abbott) | EXAS | [profile](./companies/exact-sciences.md) | 2026-06-13 |
| Guardant Health | GH | [profile](./companies/guardant-health.md) | 2026-06-13 |
| Tempus AI | TEM | [profile](./companies/tempus-ai.md) | 2026-06-13 |
| Natera | NTRA | _queued_ | - |
| GeneDx | WGS | _queued_ | - |
| NeoGenomics | NEO | _queued_ | - |
| Fulgent Genetics | FLGT | _queued_ | - |

### VBC / value-based care
| Company | Ticker | Profile | Updated |
|---|---|---|---|
| Privia Health | PRVA | [profile](./companies/privia-health.md) | 2026-06-13 |
| agilon health | AGL | [profile](./companies/agilon-health.md) | 2026-06-13 |
| Astrana Health | ASTH | _queued_ | - |
| P3 Health Partners | PIII | _queued_ | - |
| Aledade | Private | _queued_ | - |
| Innovaccer | Private | _queued_ | - |

### Payor-provider / managed care
| Company | Ticker | Profile | Updated |
|---|---|---|---|
| UnitedHealth (Optum) | UNH | _queued_ | - |
| Humana | HUM | _queued_ | - |
| Elevance Health | ELV | _queued_ | - |
| Alignment Healthcare | ALHC | _queued_ | - |

---

## Comps tables
| Sub-sector | Table | Updated |
|---|---|---|
| Diagnostics | [csv](./comps/diagnostics.csv) / [rendered](./comps/diagnostics.md) | 2026-06-13 |
| VBC | _queued_ | - |
| Payor-provider / managed care | _queued_ | - |

---

## People
_None yet._ Queue: BofA HC bankers, key sponsors (e.g. VBC-focused PE), notable
operators (Conroy/EXAS, Eltoukhy/GH, Lefkofsky/TEM, Mehrotra/PRVA).

## Deals
_None yet as standalone entries._ Captured inline in profiles so far:
- **Abbott / Exact Sciences** - ~$21B, $105/share, closed 2026-03-23.
- **Tempus / Ambry Genetics** - ~$600M, closed 2025-02-03.
- **Tempus / Deep 6 AI** - 2025-03. **Tempus / Paige** - ~$81.2M, 2025-08.

Next run: promote these to dated `/deals/` entries (filename `YYYY-MM-acquirer-target.md`).

---

## Status (as of 2026-06-13)

**Done this run:**
- Scaffolded repo structure; wrote `_schema.md` (template + conventions) and this index.
- 5 full company profiles: Exact Sciences, Guardant Health, Privia Health, agilon health, Tempus AI.
- Diagnostics comps table (7 names) with multiples + outlier reads.

**Key data note:** the connected FMP plan tier only returns company *profiles*
(price, market cap, beta). Statements/ratios/analyst/TTM/batch endpoints are gated
(ACCESS DENIED). So prices + market caps are from FMP; revenue/growth/margins/guidance
are from FY2025 company releases and web search. A higher FMP tier would let future runs
pull EV/EBITDA and balance-sheet data directly.

---

## Next up (queue for future runs)

1. **Finish the diagnostics universe:** profiles for Natera, GeneDx, NeoGenomics, Fulgent.
2. **Build the VBC sub-sector:** profiles for Astrana, P3, plus private Aledade & Innovaccer
   (round/valuation, labeled est.); then a VBC comps table (frame on EV/EBITDA + per-member
   economics + medical margin, not EV/Sales).
3. **Build payor-provider / managed care:** UnitedHealth/Optum, Humana, Elevance,
   Alignment Healthcare; comps on P/E and EV/EBITDA + MLR trends.
4. **Promote deals to `/deals/`:** Abbott-Exact Sciences, the three Tempus deals; add any
   new 2026 HC M&A.
5. **Start `/people/`:** BofA HC coverage bankers and key operators/sponsors.
6. **Refresh data:** replace guidance-based revenue with FY2025 actuals (NEO, WGS); verify
   agilon share count / CEO title; re-pull prices.
7. **If FMP tier is upgraded:** backfill true EV/Sales and EV/EBITDA across comps.
