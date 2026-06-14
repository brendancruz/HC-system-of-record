#!/usr/bin/env python3
"""Generate an interactive Leaflet map of Greater Boston healthcare companies.

Reads companies.csv (the source-of-truth database) and writes a single,
self-contained map.html (Leaflet from CDN + OpenStreetMap/Carto tiles, company
data embedded inline). No network is needed to *generate* the map - latitude /
longitude are already baked into the CSV.

Usage:
    python3 build_map.py            # regenerate map.html from companies.csv

The two personal pins (work + home) are defined in PLACES below.
"""

import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "companies.csv")
OUT_PATH = os.path.join(HERE, "map.html")

# Segment -> marker color
SEGMENT_COLORS = {
    "Biopharma": "#2563eb",          # blue
    "Medtech/Dx/Tools": "#16a34a",   # green
    "Digital Health": "#ea580c",     # orange
}

# Personal reference pins (the user's work + home).
PLACES = [
    {"label": "Work", "name": "Work - 184 High St", "address": "184 High St, Boston, MA 02110",
     "lat": 42.3551, "lng": -71.0521, "color": "#111827"},
    {"label": "Home", "name": "Home - 25 Portsmouth St", "address": "25 Portsmouth St, Cambridge, MA 02141",
     "lat": 42.3733, "lng": -71.0935, "color": "#be123c"},
]

GREATER_BOSTON_BOUNDS = {"lat": (42.20, 42.60), "lng": (-71.55, -70.85)}


def load_companies():
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                lat = float(r["lat"])
                lng = float(r["lng"])
            except (KeyError, ValueError):
                raise SystemExit(f"Missing/invalid lat/lng for {r.get('name')!r}")
            lo, hi = GREATER_BOSTON_BOUNDS["lat"]
            lo2, hi2 = GREATER_BOSTON_BOUNDS["lng"]
            if not (lo <= lat <= hi and lo2 <= lng <= hi2):
                raise SystemExit(f"Coord out of Greater Boston bounds for {r['name']!r}: {lat},{lng}")
            mc = r.get("market_cap_usd_b", "").strip()
            rows.append({
                "name": r["name"],
                "ticker": r["ticker"],
                "segment": r["segment"],
                "subsegment": r.get("subsegment", ""),
                "ownership": r.get("ownership", ""),
                "address": ", ".join(p for p in [r.get("hq_address", ""), r.get("city", ""),
                                                 r.get("state", ""), r.get("zip", "")] if p),
                "lat": lat,
                "lng": lng,
                "market_cap": float(mc) if mc else None,
                "headcount": r.get("headcount", "").strip(),
                "founded": r.get("founded", "").strip(),
                "website": r.get("website", "").strip(),
                "notes": r.get("notes", "").strip(),
            })
    return rows


def build_html(companies):
    data = json.dumps(companies)
    places = json.dumps(PLACES)
    colors = json.dumps(SEGMENT_COLORS)
    n = len(companies)
    counts = {}
    for c in companies:
        counts[c["segment"]] = counts.get(c["segment"], 0) + 1
    counts_json = json.dumps(counts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Greater Boston Healthcare Map</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
  integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
  integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<style>
  html, body {{ margin: 0; height: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
  #map {{ position: absolute; top: 0; bottom: 0; left: 0; right: 0; }}
  .panel {{ background: rgba(255,255,255,0.95); padding: 10px 12px; border-radius: 8px;
           box-shadow: 0 1px 5px rgba(0,0,0,0.3); line-height: 1.35; font-size: 13px; }}
  .panel h1 {{ font-size: 15px; margin: 0 0 4px; }}
  .panel .sub {{ color: #555; font-size: 12px; }}
  .legend i {{ width: 12px; height: 12px; display: inline-block; margin-right: 6px;
              border-radius: 50%; vertical-align: middle; }}
  .legend .row {{ margin: 3px 0; }}
  .legend .star {{ font-size: 14px; margin-right: 4px; vertical-align: middle; }}
  .popup b {{ font-size: 13px; }}
  .popup .meta {{ color: #444; font-size: 12px; }}
  .place-pin {{ font-size: 22px; line-height: 22px; text-align: center; text-shadow: 0 0 3px #fff, 0 0 3px #fff; }}
</style>
</head>
<body>
<div id="map"></div>
<script>
const COMPANIES = {data};
const PLACES = {places};
const COLORS = {colors};
const COUNTS = {counts_json};

const map = L.map('map', {{ scrollWheelZoom: true }});
L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
  attribution: '&copy; OpenStreetMap &copy; CARTO',
  subdomains: 'abcd', maxZoom: 19
}}).addTo(map);

const layers = {{}};
for (const seg of Object.keys(COLORS)) {{ layers[seg] = L.layerGroup(); }}

function esc(s) {{ return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }}

const allLatLng = [];
for (const c of COMPANIES) {{
  const color = COLORS[c.segment] || '#666';
  const isPublic = (c.ownership || '').toLowerCase() === 'public';
  let radius = 7;
  if (c.market_cap) radius = Math.min(7 + Math.sqrt(c.market_cap) * 1.6, 28);
  const marker = L.circleMarker([c.lat, c.lng], {{
    radius: radius, color: color, weight: 2,
    fillColor: color, fillOpacity: isPublic ? 0.80 : 0.30
  }});
  const cap = c.market_cap ? ('$' + c.market_cap + 'B mkt cap (est.)') : '';
  const tickerLine = (c.ticker && c.ticker !== 'Private') ? (c.ticker + ' &middot; ') : '';
  const web = c.website ? `<a href="https://${{esc(c.website)}}" target="_blank" rel="noopener">${{esc(c.website)}}</a>` : '';
  marker.bindPopup(
    `<div class="popup"><b>${{esc(c.name)}}</b><br>` +
    `<span class="meta">${{tickerLine}}${{esc(c.ownership)}} &middot; ${{esc(c.segment)}}</span><br>` +
    (c.subsegment ? `<span class="meta">${{esc(c.subsegment)}}</span><br>` : '') +
    `<span class="meta">${{esc(c.address)}}</span><br>` +
    (cap ? `<span class="meta">${{cap}}</span><br>` : '') +
    (c.headcount ? `<span class="meta">~${{esc(c.headcount)}} employees${{c.founded ? ' &middot; founded ' + esc(c.founded) : ''}}</span><br>` : (c.founded ? `<span class="meta">Founded ${{esc(c.founded)}}</span><br>` : '')) +
    (web ? `<span class="meta">${{web}}</span><br>` : '') +
    (c.notes ? `<br><span class="meta">${{esc(c.notes)}}</span>` : '') +
    `</div>`
  );
  marker.addTo(layers[c.segment] || (layers[c.segment] = L.layerGroup()));
  allLatLng.push([c.lat, c.lng]);
}}
for (const seg of Object.keys(layers)) {{ layers[seg].addTo(map); }}

// Personal pins (work + home) as star markers.
const placeLayer = L.layerGroup().addTo(map);
for (const p of PLACES) {{
  const icon = L.divIcon({{ className: '', html: `<div class="place-pin" style="color:${{p.color}}">&#9733;</div>`,
                            iconSize: [22,22], iconAnchor: [11,11] }});
  L.marker([p.lat, p.lng], {{ icon: icon, zIndexOffset: 1000 }})
    .bindPopup(`<div class="popup"><b>${{esc(p.name)}}</b><br><span class="meta">${{esc(p.address)}}</span></div>`)
    .addTo(placeLayer);
  allLatLng.push([p.lat, p.lng]);
}}

map.fitBounds(allLatLng, {{ padding: [40, 40] }});

// Layer toggle control.
const overlays = {{}};
for (const seg of Object.keys(COLORS)) {{
  overlays[`<span style="color:${{COLORS[seg]}}">&#9679;</span> ${{seg}} (${{COUNTS[seg]||0}})`] = layers[seg];
}}
overlays['&#9733; Work / Home'] = placeLayer;
L.control.layers(null, overlays, {{ collapsed: false, position: 'topright' }}).addTo(map);

// Title panel.
const title = L.control({{ position: 'topleft' }});
title.onAdd = function() {{
  const d = L.DomUtil.create('div', 'panel');
  d.innerHTML = `<h1>Greater Boston Healthcare Map</h1>` +
    `<div class="sub">{n} companies &middot; biopharma, medtech/dx/tools, digital health</div>` +
    `<div class="sub">Source of record: HC-system-of-record &middot; as of 2026-06-14</div>`;
  return d;
}};
title.addTo(map);

// Legend.
const legend = L.control({{ position: 'bottomright' }});
legend.onAdd = function() {{
  const d = L.DomUtil.create('div', 'panel legend');
  let html = '<div class="row"><b>Segments</b></div>';
  for (const seg of Object.keys(COLORS)) {{
    html += `<div class="row"><i style="background:${{COLORS[seg]}}"></i>${{seg}}</div>`;
  }}
  html += '<div class="row" style="margin-top:6px"><b>Reference</b></div>';
  html += '<div class="row"><span class="star" style="color:#111827">&#9733;</span>Work (184 High St)</div>';
  html += '<div class="row"><span class="star" style="color:#be123c">&#9733;</span>Home (25 Portsmouth St)</div>';
  html += '<div class="row" style="margin-top:6px;color:#555;font-size:11px">Filled = public &middot; faded = private/subsidiary<br>Marker size scales with market cap where known</div>';
  return d.innerHTML = html, d;
}};
legend.addTo(map);
</script>
</body>
</html>
"""


def main():
    companies = load_companies()
    html = build_html(companies)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {OUT_PATH} with {len(companies)} companies + {len(PLACES)} personal pins.")


if __name__ == "__main__":
    main()
