# _schema.md - Profile Template & Conventions

This file defines the structure and writing conventions for the HC Coverage
System of Records. Every future run should read this first and follow it so
entries stay consistent and the knowledge base compounds cleanly.

Last updated: 2026-06-13

---

## Purpose

A version-controlled knowledge base for healthcare coverage prep, focused on
diagnostics, value-based care (VBC), and payor-provider / managed care names.
Built to help sound fluent in HC coverage conversations (target: BofA HC group).
Every session adds or refreshes entries.

---

## Repo structure

```
/companies/   one markdown profile per company (filename: kebab-case, e.g. exact-sciences.md)
/comps/       comps tables by sub-sector (a .csv source + a rendered .md view)
/people/      bankers, sponsors, operators worth knowing
/deals/       notable recent M&A / financings, dated (filename: YYYY-MM-acquirer-target.md)
/_index.md    master index, links to everything, last-updated dates, "next up" queue
/_schema.md   this file - the template + conventions
```

---

## Company profile schema

Every company profile uses these sections, in this order:

```markdown
# <Company Name> (<TICKER or "Private">)

**Sub-sector:** <Diagnostics | VBC | Payor-Provider / Managed Care | ...>
**One-liner:** <one sentence on what they do>
**Profile last updated:** <YYYY-MM-DD>

## Business model / how it makes money
<How revenue is generated. Reimbursement model where relevant - test
volume x ASP for dx; capitation / full-risk / shared-savings for VBC;
premium - medical cost for payors.>

## Key financials
<Rev, growth, gross margin, EBITDA or path to it. Public cos: pull via FMP
connector. Private cos: last known round + valuation from web search,
explicitly labeled (est.). Every figure dated. Use a small table where it helps.>

## Valuation snapshot
<Relevant multiple(s) vs. peers - EV/Sales and/or EV/EBITDA for dx;
EV/EBITDA or per-member for VBC. State the as-of date and the share price
/ market cap used. Flag if the company is acquired / no longer freely traded.>

## Competitive position
<Where they sit in the market + 2-3 named competitors.>

## Recent deal / news (dated)
<Most recent material M&A, financing, regulatory, or coverage event, dated.>

## Why it matters for HC coverage
<1-2 sentences, my own angle - the banker read, not a recap.>

## Sources
<Bulleted list with dates. Note which figures came from FMP vs. web vs. filings.>
```

---

## Comps table conventions

- One sub-sector per table. Source of truth is a `.csv`; the `.md` is a
  rendered, annotated view (with an "outliers / reads" section).
- Standard columns for diagnostics: Company, Ticker, Price, Market Cap,
  FY Revenue, Rev Growth %, Gross Margin %, Price/Sales (mkt cap / sales),
  2026E P/S where guidance exists, Notes.
- True EV/Sales needs net debt/cash. If the data source tier does not
  expose balance-sheet data, use Price/Sales (market cap / sales) as the
  proxy and explicitly note net-cash/net-debt situations that distort it
  (e.g. a cash-heavy name where EV << market cap).
- Always flag outliers and say *why* (growth, optionality, takeout, legacy mix).

---

## Data sources & tooling

- **FMP connector** (Financial Modeling Prep MCP): use for public-co prices,
  market caps, and - where the plan tier allows - statements/ratios.
  - As of 2026-06-13 the connected FMP plan only exposes **company profiles**
    (price, market cap, beta, sector, description). Statements, ratios, TTM,
    analyst, and batch endpoints return ACCESS DENIED on this tier.
  - Practical implication: pull price + market cap from FMP, pull
    revenue / growth / margins / guidance from company press releases,
    SEC 8-K exhibits, and web search. Cross-check FMP market-cap fields
    against price x shares; a few were internally inconsistent (see below).
  - Known FMP data quirks observed 2026-06-13: AGL price field looked stale
    /mis-scaled; NEO market-cap field implied too few shares. Verify VBC and
    smaller names against a second source before quoting.
- **Web search**: primary source for financials given the FMP tier limit,
  plus private-co rounds, M&A, regulatory/coverage events. Prefer company IR,
  SEC filings (8-K exhibits), and reputable trade press.

---

## Writing conventions (strict)

- **Never use em dashes.** Use an en dash with spaces ( - ) for breaks.
- **Dollar figures:** `$xT` / `$xB` / `$xM` / `$xk` (capital T/B/M, lowercase k).
  Examples: `$21B`, `$3.25B`, `$400M`, `$87k tests`.
- **Label every estimate and assumption** with `(est.)` or a clear caveat.
- **Date every fact** - either inline (`FY2025`, `as of 2026-06-13`) or in Sources.
- **Built to grow:** keep a "next up" queue in `_index.md`. Leave entries
  refreshable - note the as-of date so the next run knows what is stale.
- Keep the banker angle ("Why it matters") sharp and opinionated, not a recap.
