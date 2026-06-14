/* ============================================================================
   GData - all datasets inlined (so charts work from file:// with no fetch).
   Figures sourced from: NHGRI sequencing-cost program, CASP results, published
   GWAS/heritability literature, and this repo's own diagnostics comps
   (companies/natera.md, comps/diagnostics.csv). Illustrative/stylized series
   are labeled as such in the figure captions.
   ========================================================================== */
window.GData = {

  /* Cost to sequence one human genome vs a Moore's-law reference line.
     Approximate NHGRI "Cost per Genome" values; Moore's line halves every 2 yrs
     from the 2001 starting point. */
  seqCost: {
    years: [2001, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2023],
    actual: [100000000, 20000000, 10000000, 3000000, 50000, 7700, 4000, 1500, 1100, 1000, 600, 200],
    moore:  [100000000, 35355339, 17677670, 8838835, 4419417, 2209709, 1104854, 552427, 276214, 138107, 69053, 48828]
  },

  /* Genomics stock bubble - a STYLIZED index (1998-2003) capturing the run-up
     and crash of the genomics names (Celera, Human Genome Sciences, Incyte,
     Millennium). Not actual prices; shape and events are the teaching point. */
  bubble: {
    points: [
      { x: 1998.0, y: 100 }, { x: 1998.5, y: 130 }, { x: 1999.0, y: 180 },
      { x: 1999.5, y: 320 }, { x: 1999.9, y: 620 }, { x: 2000.2, y: 980 },
      { x: 2000.25, y: 700 }, { x: 2000.5, y: 560 }, { x: 2000.8, y: 470 },
      { x: 2001.2, y: 360 }, { x: 2001.7, y: 250 }, { x: 2002.2, y: 150 },
      { x: 2002.8, y: 110 }, { x: 2003.2, y: 95 }
    ],
    annotations: [
      { x: 2000.2, y: 980, text: "Early 2000: peak", dx: -8, anchor: "end" },
      { x: 2000.25, y: 700, text: "Mar 14 2000:\nClinton-Blair\nfree-access statement", dx: 70, up: false, anchor: "start" },
      { x: 2003.2, y: 95, text: "2003: HGP\n'complete'", dx: -6, anchor: "end", up: false }
    ]
  },

  /* "Missing heritability" - share of trait variance explained, height example.
     Twin-study heritability ~80%; the first GWAS hits (2007-2010) explained only
     a few percent; genome-wide common variation explains far more. Approximate. */
  heritability: {
    categories: ["Twin-study\nheritability", "Early GWAS\nhits (2010)", "All common\nvariants (later)", "Still\nunexplained"],
    values: [80, 5, 50, 30],
    colors: ["#283593", "#c2456b", "#138a72", "#b8b3a0"]
  },

  /* Protein-structure prediction accuracy at CASP (median GDT_TS on the hardest
     targets, approximate). The jump: AlphaFold (2018) then AlphaFold2 (2020). */
  casp: {
    years: ["2008", "2012", "2014", "2016", "2018\nAlphaFold", "2020\nAlphaFold2"],
    gdt: [35, 38, 40, 42, 58, 92],
    highlight: [false, false, false, false, true, true]
  },

  /* Epigenetic clock: DNA-methylation predicted age vs chronological age.
     Tracks the y=x line closely (Horvath-style clock), with a few accelerated
     and decelerated individuals. Illustrative points. */
  epiClock: [
    { x: 22, y: 24 }, { x: 28, y: 27 }, { x: 31, y: 35 }, { x: 35, y: 33 },
    { x: 40, y: 41 }, { x: 44, y: 52 }, { x: 49, y: 47 }, { x: 53, y: 55 },
    { x: 58, y: 56 }, { x: 61, y: 68 }, { x: 66, y: 64 }, { x: 70, y: 72 },
    { x: 74, y: 71 }, { x: 79, y: 83 }
  ],

  /* Natera revenue, FY2021-FY2025 (USD millions). FY2024/2025 from this repo's
     natera.md; earlier years from company filings. */
  nateraRevenue: {
    years: ["FY21", "FY22", "FY23", "FY24", "FY25"],
    values: [625.5, 820.9, 1082.5, 1696.9, 2306.1]
  },

  /* Natera's three franchises - approximate, ILLUSTRATIVE split to show the
     structure (the repo does not break out exact segment revenue). */
  nateraSplit: [
    { name: "Women's health", value: 44, color: "#283593", note: "Panorama / Horizon" },
    { name: "Oncology (Signatera)", value: 43, color: "#138a72", note: "MRD - growth engine" },
    { name: "Organ health", value: 13, color: "#b8860b", note: "Prospera" }
  ],

  /* Diagnostics comp set - P/S vs revenue growth, from comps/diagnostics.csv
     (as of 2026-06-13). The "you are paying for growth" scatter. */
  dxComps: [
    { label: "Natera", x: 36, y: 13.2, color: "#283593", r: 12 },
    { label: "Guardant", x: 31, y: 17.9, color: "#138a72", r: 10 },
    { label: "Tempus", x: 83, y: 6.6, color: "#c2456b", r: 10 },
    { label: "Exact Sci.", x: 18, y: 6.2, color: "#b8860b", r: 11 },
    { label: "GeneDx", x: 40, y: 4.2, color: "#5a6acf", r: 9 },
    { label: "NeoGenomics", x: 10, y: 2.0, color: "#2a9d8f", r: 8 },
    { label: "Fulgent", x: 14, y: 1.6, color: "#8a7fb0", r: 8 }
  ]
};
