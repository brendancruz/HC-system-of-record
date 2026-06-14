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
| Astrana Health | ASTH | [profile](./companies/astrana-health.md) | 2026-06-14 |
| P3 Health Partners | PIII | [profile](./companies/p3-health-partners.md) | 2026-06-14 |
| Aledade | Private | [profile](./companies/aledade.md) | 2026-06-14 |
| Innovaccer | Private | [profile](./companies/innovaccer.md) | 2026-06-14 |

### Payor-provider / managed care
| Company | Ticker | Profile | Updated |
|---|---|---|---|
| UnitedHealth (Optum) | UNH | [profile](./companies/unitedhealth-group.md) | 2026-06-14 |
| Humana | HUM | [profile](./companies/humana.md) | 2026-06-14 |
| Elevance Health | ELV | [profile](./companies/elevance-health.md) | 2026-06-14 |
| Alignment Healthcare | ALHC | [profile](./companies/alignment-healthcare.md) | 2026-06-14 |

---

## Sector overviews & research notes
| Sub-sector | Artifact | Updated |
|---|---|---|
| Diagnostics | **[research note (assembled)](./sectors/diagnostics-note.md)** | 2026-06-14 |
| Diagnostics | [overview](./sectors/diagnostics.md) | 2026-06-14 |
| Diagnostics | [competitive landscape](./sectors/diagnostics-landscape.md) | 2026-06-14 |
| Diagnostics | [ideas shortlist](./sectors/diagnostics-ideas.md) | 2026-06-14 |
| Diagnostics | [slide pack (.pptx)](./sectors/diagnostics-deck.pptx) ([generator](./sectors/build_diagnostics_deck.py)) | 2026-06-14 |

---

## Comps tables
| Sub-sector | Table | Updated |
|---|---|---|
| Diagnostics | [csv](./comps/diagnostics.csv) / [rendered](./comps/diagnostics.md) | 2026-06-13 |
| VBC | [csv](./comps/vbc.csv) / [rendered](./comps/vbc.md) | 2026-06-14 |
| Payor-provider / managed care | [csv](./comps/managed-care.csv) / [rendered](./comps/managed-care.md) | 2026-06-14 |

---

## People
| File | Contents | Updated |
|---|---|---|
| [operators.md](./people/operators.md) | CEOs across all 17 profiled companies | 2026-06-14 |

Queue: BofA HC coverage bankers and key sponsors (VBC-focused PE / strategics).

## Deals
| Deal | Value | Date | Entry |
|---|---|---|---|
| Abbott / Exact Sciences | ~$21B | closed 2026-03-23 | [entry](./deals/2026-03-abbott-exact-sciences.md) |
| Tempus / Ambry Genetics (+ Deep 6 AI, Paige) | ~$600M (+tuck-ins) | closed 2025-02-03 | [entry](./deals/2025-02-tempus-ambry-genetics.md) |

---

## Status (as of 2026-06-14)

**Done (run 4 - diagnostics market-research package):**
- Added a new `/sectors/` artifact type and wrote the **Diagnostics sector overview**
  (market size bottom-up from the profiled universe, structure/value chain, drivers,
  why-now, and the one-screen name sort).
- Added the **Diagnostics competitive landscape** (battlegrounds, positioning map,
  adjacent players, recent moves) and the **Diagnostics ideas shortlist** (4 thesis
  hooks + 1 watch).
- Assembled the **Diagnostics research note** - the finished, standalone deliverable
  with an executive summary that consolidates overview + landscape + comps + ideas.
  The full market-researcher package for diagnostics is now complete.
- Built a 7-slide **Diagnostics deck** (`sectors/diagnostics-deck.pptx`) from a reproducible
  generator script (`sectors/build_diagnostics_deck.py`, python-pptx; generic template).
  All artifacts wired into this index.



**Done (run 1):**
- Scaffolded repo structure; wrote `_schema.md` (template + conventions) and this index.
- 5 full company profiles: Exact Sciences, Guardant Health, Privia Health, agilon health, Tempus AI.
- Diagnostics comps table (7 names) with multiples + outlier reads.

**Done (run 2):**
- Completed the diagnostics universe: added Natera, GeneDx, NeoGenomics, Fulgent profiles
  (all 7 diagnostics names now profiled).
- Promoted flagship deals to dated `/deals/` entries (Abbott-Exact Sciences; Tempus-Ambry + tuck-ins).
- Refreshed diagnostics comps with reported FY2025 actuals (notably NEO $727.3M) and added forward 2026E P/S.

**Done (run 3 - "finish"):**
- Built the **VBC sub-sector**: profiles for Astrana, P3, Aledade (private), Innovaccer (private),
  plus a VBC comps table framed on EV/EBITDA + risk model (not EV/Sales).
- Built the **payor-provider / managed care** sub-sector: UnitedHealth, Humana, Elevance,
  Alignment, plus a managed-care comps table framed on P/E + MLR.
- Seeded `/people/operators.md` (CEOs across all 17 profiled companies).
- **All seed-universe names are now profiled (17 companies, 3 comps tables, 2 deals, 1 people file).**

**Key data note:** the connected FMP plan tier only returns company *profiles*
(price, market cap, beta). Statements/ratios/analyst/TTM/batch endpoints are gated
(ACCESS DENIED). So prices + market caps are from FMP; revenue/growth/margins/guidance
are from FY2025 company releases and web search. A higher FMP tier would let future runs
pull EV/EBITDA and balance-sheet data directly.

---

## Next up (queue for future runs)

The full seed universe is now built out. Next runs should deepen and maintain:

1. **Add `/people/` bankers & sponsors:** BofA HC coverage team and recent BofA-led HC deals;
   key PE/growth sponsors and strategics active in the space.
2. **Expand the universe (beyond seed):** e.g. Caris Life Sciences (dx/data), Devoted/Clover
   (MA insurtech), CVS/Aetna & Cigna (managed care), Health Catalyst/Arcadia (VBC data),
   Quest/Labcorp (reference labs).
3. **Refresh data (the maintenance loop):** replace guidance-based revenue with reported actuals
   (WGS); verify agilon share count / CEO title and P3 share count; confirm Fabric Genomics (WGS);
   refresh stale private marks (Aledade June 2023); confirm UNH consolidated revenue and ELV
   adjusted 2026 EPS; re-pull all prices.
4. **Deepen the comps:** add net debt to convert P/S -> true EV/Sales (dx) and firm up EV/EBITDA
   (VBC); add per-member/PMPM + Star-Ratings columns for MA names.
5. **If FMP tier is upgraded:** backfill statements-based metrics (EV/EBITDA, balance sheet) across all comps.
6. **Add new 2026 HC M&A** to `/deals/` as it happens.
