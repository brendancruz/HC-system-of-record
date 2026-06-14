/* ============================================================================
   Glossary: a shared dictionary that powers (1) inline hover tooltips on
   span.term elements (via their data-term attribute) and (2) the glossary page.
   ========================================================================== */
window.GLOSSARY = [
  ["DNA", "Deoxyribonucleic acid: the double-helix molecule that stores genetic information as a sequence of four bases (A, C, G, T)."],
  ["RNA", "Ribonucleic acid: a single-stranded cousin of DNA. Messenger RNA carries instructions from genes to the protein-making machinery."],
  ["Gene", "A stretch of DNA that codes for a product, usually a protein. Humans have roughly 20,000 protein-coding genes."],
  ["Genome", "The complete set of an organism's DNA, including all genes and the non-coding sequence between them. The human genome is about 3.1 billion base pairs."],
  ["Exome", "The roughly 1-2% of the genome that codes for proteins (all the exons). Whole-exome sequencing reads just this slice."],
  ["Exon", "The protein-coding segments of a gene that remain in the final messenger RNA after the non-coding introns are spliced out."],
  ["Exosome", "A tiny membrane-bound vesicle that cells release into blood and other fluids. Not to be confused with the exome; exosomes carry cargo (including RNA) and are studied as liquid-biopsy analytes."],
  ["Chromosome", "A long, packaged molecule of DNA. Humans have 23 pairs (46 total), including the sex chromosomes X and Y."],
  ["Base pair", "Two complementary bases (A with T, C with G) that bond across the two DNA strands. The genome's length is measured in base pairs."],
  ["Nucleotide", "The building block of DNA or RNA: a base plus a sugar and a phosphate group."],
  ["Allele", "One of the alternative versions of a gene or DNA position. You inherit one allele from each parent."],
  ["Locus", "A fixed position on a chromosome where a particular gene or marker lives."],
  ["SNP", "Single-nucleotide polymorphism: a single-letter difference in the DNA code that is common in the population. The most abundant kind of genetic variation."],
  ["Indel", "A small insertion or deletion of DNA bases."],
  ["CNV", "Copy-number variant: a stretch of DNA that is duplicated or deleted, so the number of copies differs between people."],
  ["Structural variant", "A large-scale rearrangement of DNA: deletions, duplications, inversions, or translocations spanning many bases."],
  ["Genotype", "The specific set of alleles an individual carries at a position or across the genome."],
  ["Phenotype", "The observable trait that results from genotype plus environment: height, eye color, disease status, and so on."],
  ["Germline", "DNA you inherit and carry in every cell, including egg and sperm. Germline variants can be passed to children."],
  ["Somatic", "DNA changes acquired during life in a particular tissue (classically, the mutations that drive a tumor). Somatic variants are not inherited."],
  ["Mutation", "A change in the DNA sequence. It can be harmless, harmful, or beneficial. Increasingly called a 'variant'."],
  ["Variant", "Any difference from the reference genome. The neutral, modern term that has largely replaced 'mutation'."],
  ["VUS", "Variant of uncertain significance: a DNA difference whose effect on health is not yet known. A central challenge of clinical genetics."],
  ["Central dogma", "The flow of genetic information: DNA is transcribed into RNA, which is translated into protein."],
  ["Transcription", "Copying a gene's DNA into messenger RNA."],
  ["Translation", "Reading messenger RNA in three-letter codons to build a protein from amino acids."],
  ["Codon", "A triplet of RNA bases that specifies one amino acid (or a stop signal)."],
  ["Ploidy", "The number of chromosome sets in a cell. Humans are diploid (two sets); eggs and sperm are haploid (one)."],
  ["Haplotype", "A set of variants that sit together on the same chromosome and tend to be inherited as a block."],
  ["Homozygous", "Carrying two identical alleles at a position (one from each parent)."],
  ["Heterozygous", "Carrying two different alleles at a position."],
  ["Penetrance", "The probability that people carrying a given variant actually show the associated trait or disease."],
  ["Expressivity", "How strongly a trait shows up among the people in whom it appears."],
  ["Mendelian", "A trait driven mostly by a single gene, following the inheritance patterns Gregor Mendel described."],
  ["Polygenic", "A trait shaped by many genes each contributing a small effect, usually together with environment."],
  ["GWAS", "Genome-wide association study: scanning many people's genomes to find variants statistically linked to a trait or disease."],
  ["Polygenic risk score", "A single number that sums up the small effects of many variants to estimate a person's genetic predisposition to a trait."],
  ["Heritability", "The share of a trait's variation in a population explained by genetic differences. Often estimated from twin studies."],
  ["Missing heritability", "The gap between heritability estimated from family studies and the much smaller fraction explained by the variants GWAS first identified."],
  ["Epigenetics", "Heritable or stable changes in gene activity that do not alter the DNA sequence itself, such as chemical tags on DNA or its packaging."],
  ["DNA methylation", "A chemical tag (a methyl group) added to DNA, usually at CpG sites, that typically dials gene activity down. A core epigenetic mark."],
  ["Histone", "A spool protein that DNA wraps around. Chemical modifications to histones help switch genes on or off."],
  ["Chromatin", "The combination of DNA and its packaging proteins. How tightly it is packed controls which genes can be read."],
  ["Imprinting", "When a gene is expressed from only the maternal or only the paternal copy, set by epigenetic marks."],
  ["X-inactivation", "The process by which one X chromosome is largely silenced in each cell of females, an example of epigenetics in action."],
  ["Epigenetic clock", "A model that estimates biological age from DNA-methylation patterns, sometimes diverging from chronological age."],
  ["Sequencing", "Determining the exact order of bases in a stretch of DNA or RNA."],
  ["Sanger sequencing", "The original, accurate, one-fragment-at-a-time sequencing method from the 1970s that powered the Human Genome Project."],
  ["NGS", "Next-generation sequencing: massively parallel methods (notably Illumina) that read millions of fragments at once, collapsing cost."],
  ["WGS", "Whole-genome sequencing: reading essentially all 3.1 billion base pairs."],
  ["WES", "Whole-exome sequencing: reading only the protein-coding exome, cheaper than whole-genome sequencing."],
  ["Read", "A single short stretch of sequence produced by a sequencer; reads are assembled or aligned to reconstruct the genome."],
  ["Coverage", "How many times, on average, each base is read. Higher depth means more confident variant calls."],
  ["Reference genome", "A standardized 'consensus' human genome that new sequences are compared against to find variants."],
  ["cfDNA", "Cell-free DNA: fragments of DNA shed from cells into the bloodstream, the raw material of liquid biopsies."],
  ["ctDNA", "Circulating tumor DNA: the fraction of cell-free DNA that comes from cancer cells, carrying tumor-specific (somatic) variants."],
  ["Liquid biopsy", "A blood test that analyzes cell-free DNA or other analytes to detect or monitor disease without cutting tissue."],
  ["MRD", "Molecular (or minimal) residual disease: tiny amounts of cancer left after treatment, detectable via ctDNA before it is visible on scans."],
  ["NIPT", "Non-invasive prenatal testing: a blood test that screens fetal cell-free DNA for chromosomal conditions during pregnancy."],
  ["Carrier screening", "Testing prospective parents for recessive disease variants they could pass on together."],
  ["CRISPR", "A bacterial defense system repurposed as a programmable gene-editing tool that can be aimed at a chosen DNA sequence."],
  ["Cas9", "The DNA-cutting enzyme guided by RNA in the most common CRISPR system."],
  ["Guide RNA", "The short RNA sequence that programs a CRISPR system, steering the Cas enzyme to the matching target site in the genome."],
  ["Base editing", "A precise CRISPR-derived technique that chemically converts one DNA letter to another without cutting both strands."],
  ["Prime editing", "A versatile CRISPR-derived 'search and replace' method that can write a range of edits without double-strand breaks."],
  ["Gene therapy", "Treating disease by adding, replacing, silencing, or editing genes inside a patient's cells."],
  ["Pharmacogenomics", "The study of how a person's genes affect their response to drugs, used to tailor dose and choice."],
  ["Companion diagnostic", "A test that identifies the patients whose biology makes them likely to benefit from a specific targeted drug."],
  ["Proteome", "The full set of proteins expressed by a cell or organism."],
  ["Transcriptome", "The full set of RNA transcripts in a cell, a snapshot of which genes are active."],
  ["Protein folding", "The way a chain of amino acids collapses into the precise 3-D shape that determines a protein's function."],
  ["AlphaFold", "DeepMind's AI system that predicts protein 3-D structure from sequence, a breakthrough at the 2020 CASP contest."],
  ["Transformer", "The neural-network architecture behind modern large language models, now also applied to protein and DNA sequences."],
  ["MCED", "Multi-cancer early detection: a single blood test that screens for signals of many cancers at once, often via DNA methylation."]
];

(function () {
  "use strict";
  function norm(s) { return String(s || "").toLowerCase().replace(/[^a-z0-9]/g, ""); }
  var MAP = {};
  window.GLOSSARY.forEach(function (e) { MAP[norm(e[0])] = e[1]; });

  // ---- inline tooltips ----
  function tip() {
    var t = document.getElementById("term-tip");
    if (!t) { t = document.createElement("div"); t.id = "term-tip"; document.body.appendChild(t); }
    return t;
  }
  function show(span) {
    var key = norm(span.getAttribute("data-term") || span.textContent);
    var def = MAP[key]; if (!def) return;
    var t = tip();
    t.innerHTML = "<b>" + (span.getAttribute("data-term") || span.textContent) + "</b>" + def;
    t.classList.add("show");
    var r = span.getBoundingClientRect();
    var tw = Math.min(320, window.innerWidth - 24);
    t.style.maxWidth = tw + "px";
    var left = Math.min(Math.max(8, r.left), window.innerWidth - tw - 8);
    var top = r.bottom + 8;
    if (top + 90 > window.innerHeight) top = r.top - t.offsetHeight - 8;
    t.style.left = left + "px"; t.style.top = top + "px";
  }
  function hide() { var t = document.getElementById("term-tip"); if (t) t.classList.remove("show"); }

  function initTerms() {
    document.querySelectorAll(".term").forEach(function (s) {
      s.setAttribute("tabindex", "0");
      s.addEventListener("mouseenter", function () { show(s); });
      s.addEventListener("mouseleave", hide);
      s.addEventListener("focus", function () { show(s); });
      s.addEventListener("blur", hide);
      s.addEventListener("click", function () { show(s); });
    });
    window.addEventListener("scroll", hide, { passive: true });
  }

  // ---- glossary page ----
  function initPage() {
    var list = document.getElementById("glossary-list");
    if (!list) return;
    var search = document.getElementById("glossary-search");
    var entries = window.GLOSSARY.slice().sort(function (a, b) { return a[0].toLowerCase() < b[0].toLowerCase() ? -1 : 1; });

    function render(filter) {
      list.innerHTML = "";
      var f = norm(filter);
      var shown = 0, lastLetter = "";
      entries.forEach(function (e) {
        if (f && norm(e[0] + e[1]).indexOf(f) === -1) return;
        shown++;
        var letter = e[0][0].toUpperCase();
        if (letter !== lastLetter) {
          var h = document.createElement("h3"); h.className = "gloss-letter"; h.textContent = letter;
          list.appendChild(h); lastLetter = letter;
        }
        var d = document.createElement("div"); d.className = "gloss-entry";
        d.innerHTML = "<dt>" + e[0] + "</dt><dd>" + e[1] + "</dd>";
        list.appendChild(d);
      });
      var empty = document.getElementById("glossary-empty");
      if (empty) empty.style.display = shown ? "none" : "block";
    }
    render("");
    if (search) search.addEventListener("input", function () { render(search.value); });
  }

  function init() { initTerms(); initPage(); }
  if (document.readyState !== "loading") init();
  else document.addEventListener("DOMContentLoaded", init);
})();
