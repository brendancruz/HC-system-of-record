# HC Coverage System of Records - Master Index

A version-controlled knowledge base for healthcare coverage prep: diagnostics,
value-based care (VBC), and payor-provider / managed care. Built to compound -
every session adds or refreshes entries. Target use: sounding fluent in HC coverage
conversations (BofA HC group).

**Index last updated:** 2026-06-14
**Conventions & profile template:** see [`_schema.md`](./_schema.md)

---

## Companies

### Diagnostics
| Company | Ticker | Profile | Updated |
|---|---|---|---|
| Exact Sciences (acq. by Abbott) | EXAS | [profile](./companies/exact-sciences.md) | 2026-06-13 |
| Guardant Health | GH | [profile](./companies/guardant-health.md) | 2026-06-13 |
| Tempus AI | TEM | [profile](./companies/tempus-ai.md) | 2026-06-13 |
| Natera | NTRA | [profile](./companies/natera.md) | 2026-06-13 |
| GeneDx | WGS | [profile](./companies/genedx.md) | 2026-06-13 |
| NeoGenomics | NEO | [profile](./companies/neogenomics.md) | 2026-06-13 |
| Fulgent Genetics | FLGT | [profile](./companies/fulgent-genetics.md) | 2026-06-13 |

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
| Deal | Value | Date | Entry |
|---|---|---|---|
| Abbott / Exact Sciences | ~$21B | closed 2026-03-23 | [entry](./deals/2026-03-abbott-exact-sciences.md) |
| Tempus / Ambry Genetics (+ Deep 6 AI, Paige) | ~$600M (+tuck-ins) | closed 2025-02-03 | [entry](./deals/2025-02-tempus-ambry-genetics.md) |

---

## Status (as of 2026-06-13)

**Done (run 1):**
- Scaffolded repo structure; wrote `_schema.md` (template + conventions) and this index.
- 5 full company profiles: Exact Sciences, Guardant Health, Privia Health, agilon health, Tempus AI.
- Diagnostics comps table (7 names) with multiples + outlier reads.

**Done (run 2):**
- Completed the diagnostics universe: added Natera, GeneDx, NeoGenomics, Fulgent profiles
  (all 7 diagnostics names now profiled).
- Promoted flagship deals to dated `/deals/` entries (Abbott-Exact Sciences; Tempus-Ambry + tuck-ins).
- Refreshed diagnostics comps with reported FY2025 actuals (notably NEO $727.3M) and added forward 2026E P/S.

**Key data note:** the connected FMP plan tier only returns company *profiles*
(price, market cap, beta). Statements/ratios/analyst/TTM/batch endpoints are gated
(ACCESS DENIED). So prices + market caps are from FMP; revenue/growth/margins/guidance
are from FY2025 company releases and web search. A higher FMP tier would let future runs
pull EV/EBITDA and balance-sheet data directly.

---

## Next up (queue for future runs)

1. **Build the VBC sub-sector:** profiles for Astrana, P3, plus private Aledade & Innovaccer
   (round/valuation, labeled est.); then a VBC comps table (frame on EV/EBITDA + per-member
   economics + medical margin, not EV/Sales). _(Privia + agilon already profiled.)_
2. **Build payor-provider / managed care:** UnitedHealth/Optum, Humana, Elevance,
   Alignment Healthcare; comps on P/E and EV/EBITDA + MLR trends.
3. **Start `/people/`:** BofA HC coverage bankers and key operators/sponsors
   (Conroy/EXAS, Eltoukhy/GH, Lefkofsky/TEM, Mehrotra/PRVA, Chapman/NTRA, Stueland/WGS).
4. **Refresh data:** replace guidance-based FY2025 revenue with reported actual (WGS);
   verify agilon share count / CEO title; confirm Fabric Genomics (WGS) close/contribution;
   re-pull prices.
5. **If FMP tier is upgraded:** backfill true EV/Sales and EV/EBITDA across comps.
6. **Add new 2026 HC M&A** to `/deals/` as it happens.
