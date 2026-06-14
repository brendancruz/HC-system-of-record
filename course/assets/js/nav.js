/* ============================================================================
   Shared UX layer for every page: reading-progress bar, auto-built section TOC
   with scroll-spy, mobile TOC drawer, scroll-reveal, and keyboard navigation.
   ========================================================================== */
(function () {
  "use strict";

  /* ---- reading progress bar ---- */
  function progress() {
    var bar = document.querySelector(".progress");
    if (!bar) return;
    function upd() {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
    }
    window.addEventListener("scroll", upd, { passive: true });
    window.addEventListener("resize", upd);
    upd();
  }

  /* ---- auto-build the on-this-page TOC from h2[id] ---- */
  function buildToc() {
    var toc = document.getElementById("toc");
    var article = document.querySelector(".article");
    if (!toc || !article) return;
    var heads = article.querySelectorAll("h2[id]");
    if (!heads.length) { toc.style.display = "none"; return; }
    var html = '<h4>On this page</h4>';
    heads.forEach(function (h) {
      html += '<a href="#' + h.id + '" data-tt="' + h.id + '">' + (h.getAttribute("data-short") || h.textContent) + "</a>";
    });
    html += '<h4 style="margin-top:1.4rem">Course</h4>' +
            '<a href="../index.html">All modules</a>' +
            '<a href="../glossary.html">Glossary</a>';
    toc.innerHTML = html;

    // scroll-spy
    var links = {};
    toc.querySelectorAll("a[data-tt]").forEach(function (a) { links[a.getAttribute("data-tt")] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          Object.values(links).forEach(function (l) { l.classList.remove("active"); });
          if (links[e.target.id]) links[e.target.id].classList.add("active");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px", threshold: 0 });
    heads.forEach(function (h) { spy.observe(h); });
  }

  /* ---- mobile TOC drawer ---- */
  function mobileMenu() {
    var btn = document.querySelector(".menu-btn");
    var toc = document.getElementById("toc");
    if (!btn || !toc) return;
    btn.addEventListener("click", function () { toc.classList.toggle("open"); });
    toc.addEventListener("click", function (e) { if (e.target.tagName === "A") toc.classList.remove("open"); });
  }

  /* ---- scroll-reveal ---- */
  function reveal() {
    var els = document.querySelectorAll(".reveal");
    if (!els.length) return;
    if (!("IntersectionObserver" in window)) { els.forEach(function (e) { e.classList.add("in"); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.08 });
    els.forEach(function (e) { io.observe(e); });
  }

  /* ---- keyboard prev/next ---- */
  function keys() {
    document.addEventListener("keydown", function (e) {
      if (e.target.matches("input, textarea, select")) return;
      if (e.key === "ArrowRight") { var n = document.querySelector(".pn--next:not(.pn--disabled)"); if (n) location.href = n.getAttribute("href"); }
      if (e.key === "ArrowLeft") { var p = document.querySelector(".pn--prev:not(.pn--disabled)"); if (p) location.href = p.getAttribute("href"); }
    });
  }

  function init() { progress(); buildToc(); mobileMenu(); reveal(); keys(); }
  if (document.readyState !== "loading") init();
  else document.addEventListener("DOMContentLoaded", init);
})();
