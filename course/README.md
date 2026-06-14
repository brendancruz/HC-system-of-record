# Genetics 101 - An Interactive Course

A self-contained, self-paced course on genetics and genomics, built as a small
static website. No build step, no server, no dependencies, no internet required.

## How to open it

Open **`index.html`** in any modern web browser (double-click it, or drag it into a
browser window). That is the whole setup. Everything runs locally from the files in
this folder.

## What is inside

Fifteen modules across six parts, from the structure of DNA to the AI systems now
designing medicine:

- **Part I - Foundations:** orientation, the molecule and the central dogma, and a
  terminology lexicon.
- **Part II - Reading & Mapping the Genome:** sequencing technology and the Human
  Genome Project.
- **Part III - Hype, Reality & the Market:** the genomics bubble and who actually won.
- **Part IV - Beyond the Sequence:** epigenetics, applied genomics, CRISPR, and
  pharmacogenomics.
- **Part V - Genomics in Society & the Clinic:** consumer genomics, ethics, the
  diagnostics industry, and a Natera case study.
- **Part VI - The AI Frontier:** AlphaFold, biological language models, and the new
  AI-for-biology companies.

## Features

- **Interactive charts** rendered as crisp SVG (hover for values).
- **Glossary tooltips:** dotted terms reveal a definition on hover or tap; a full
  searchable glossary lives at `glossary.html`.
- **Knowledge checks:** each module ends with a short quiz that gives instant feedback.
- **Reading progress, an auto-built section outline, and keyboard navigation**
  (left/right arrow keys move between modules).
- **Print-friendly:** use your browser's Print to PDF for a textbook-style export.

## Structure

```
course/
  index.html            Cover and table of contents (start here)
  glossary.html         Searchable glossary
  modules/01..15-*.html The fifteen course modules
  assets/
    css/theme.css       The design system
    js/                 charts, data, quiz, glossary, and navigation logic
```

## Notes on sourcing

Scientific and historical claims reflect the public record as of mid-2026. Company
figures in the diagnostics and Natera modules draw on this repository's own
healthcare knowledge base (`companies/natera.md`, `comps/diagnostics.md`). The course
is for learning; it is not medical or investment advice.
