# Greater Boston Healthcare Map

An interactive map of notable Greater Boston healthcare companies - a local,
geographic lens on top of the sector deep-dives in the rest of this repo. Built
to understand the local landscape and spot networking nodes near work and home.

**Last updated:** 2026-06-14

## What's here

| File | What it is |
|---|---|
| [`companies.csv`](./companies.csv) | The database - source of truth (54 companies). |
| [`map.html`](./map.html) | Self-contained interactive Leaflet map. Open it in any browser. |
| [`build_map.py`](./build_map.py) | Stdlib-only generator: reads `companies.csv`, writes `map.html`. |

## The map

- **54 companies** across three segments: Biopharma (26), Medtech / Dx / Tools (16),
  Digital Health (12). Hospitals, academic medical centers, and payors are
  intentionally excluded for now (an easy future layer).
- Two personal reference pins (gold/red stars): **Work - 184 High St, Boston**
  (Financial District) and **Home - 25 Portsmouth St, Cambridge** (East Cambridge).
- Markers are colored by segment, filled for public companies and faded for
  private / subsidiary, and sized by market cap where known.
- Toggle segments on/off with the control (top-right); click any marker for
  ticker, ownership, address, market cap, headcount, and notes.

### Clusters that jump out

- **Kendall Square, Cambridge** - the densest node (18 Cambridge names): Moderna,
  Biogen, Alnylam, Sarepta, Takeda, Beam, Agios, Relay, and more, all within a few
  blocks - and the closest cluster to the home pin.
- **Seaport, Boston** - Vertex, Foundation Medicine, Ginkgo Bioworks, 908 Devices -
  a short walk from the work pin in the Financial District.
- **The 128 belt** - the large-cap medtech / tools campuses sit out west:
  Thermo Fisher and Repligen (Waltham), Boston Scientific and Hologic (Marlborough),
  Bruker and Quanterix (Billerica), plus Burlington, Bedford, and Acton names.

## How to use

Open the map (no build step needed to view):

```
open boston/map.html        # macOS
xdg-open boston/map.html     # Linux
```

Regenerate the map after editing the database:

```
python3 boston/build_map.py
```

`build_map.py` reads `companies.csv` and re-emits `map.html`. It validates that
every row has coordinates inside the Greater Boston bounding box and fails loudly
if not. The two personal pins live in `PLACES` near the top of the script.

## Data & method notes

- **Scope:** Greater Boston - Boston + Cambridge + the inner 128 belt (Waltham,
  Watertown, Somerville, Marlborough, Burlington, Bedford, Billerica, Wilmington,
  Acton, Danvers, Framingham). Curated, high-signal set, not exhaustive.
- **Sources:** company names, HQ addresses, ownership, and headcount were compiled
  and verified via web search (company IR pages, Craft.co, Dun & Bradstreet, press)
  on 2026-06-14. Market caps are dated web estimates and only captured for a handful
  of the largest names; treat all figures as `(est.)` and refresh before quoting.
- **Coordinates** are derived from each company's known HQ building / block. The
  geocoding APIs (Nominatim, US Census, Photon) and the FMP / Apollo connectors were
  unreachable from this environment (egress blocked), so lat/lng were assigned from
  the verified street address rather than an automated geocoder. They are accurate to
  the building / block - fine for a city-scale map. If a geocoder becomes available,
  `build_map.py` could be extended with an optional `--geocode` pass.
- **Recent corporate changes captured:** Blueprint Medicines is now part of Sanofi
  (closed Jul 2025); bluebird bio was taken private by Carlyle / SK Capital (closed
  Jun 2025); athenahealth moved its HQ from Watertown to Boston Landing; Foundation
  Medicine (Roche) consolidated into a new Seaport HQ; Abiomed is a J&J subsidiary;
  Nuance is a Microsoft subsidiary.

## Next up

- Add hospitals / academic medical centers (Mass General Brigham, Dana-Farber,
  Boston Children's, Beth Israel) and payors (Point32Health, BCBS-MA) as a toggleable layer.
- Refresh market caps across all public names (ideally via FMP once the connector is reachable).
- Expand the curated set toward comprehensive coverage (Apollo pull by HQ location + industry).
