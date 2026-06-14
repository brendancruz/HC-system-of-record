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

## Geography - Boston map
A local, geographic lens: notable Greater Boston healthcare companies plotted on
an interactive map, with personal reference pins for work and home.

| Artifact | What it is | Updated |
|---|---|---|
| [boston/companies.csv](./boston/companies.csv) | Database - 54 companies (biopharma, medtech/dx/tools, digital health) | 2026-06-14 |
| [boston/map.html](./boston/map.html) | Self-contained interactive Leaflet map (open in a browser) | 2026-06-14 |
| [boston/README.md](./boston/README.md) | Overview, clusters, method, how to regenerate | 2026-06-14 |

Regenerate the map after editing the CSV: `python3 boston/build_map.py`.

---

## Status (as of 2026-06-14)

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

**Done (run 4 - "Boston map"):**
- Added a geographic lens in `/boston/`: a curated database of 54 Greater Boston
  healthcare companies (biopharma, medtech/dx/tools, digital health) with HQ addresses
  and coordinates, plus a self-contained interactive Leaflet map (`map.html`) and a
  stdlib generator (`build_map.py`). Includes personal pins for work (184 High St,
  Boston) and home (25 Portsmouth St, Cambridge).
- Note: this run's data was gathered via web search; the FMP / Apollo connectors and
  geocoding APIs were unreachable from the environment, so market caps are dated web
  estimates (captured for the largest names only) and coordinates were assigned from
  verified HQ addresses (building/block precision).

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
