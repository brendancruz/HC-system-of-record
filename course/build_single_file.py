#!/usr/bin/env python3
"""Bundle the multi-file Genetics 101 course into ONE self-contained HTML file.

Reads the existing course assets and emits course/genetics-101.html with all CSS,
JS, module content, the cover, and the glossary inlined. Navigation between modules
is handled by an in-page hash router instead of separate page loads, so the single
file works by double-clicking it (file://), fully offline.
"""
import re, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()

MODULES = [
    ("m01", "01-orientation",        "Orientation: The Big Map"),
    ("m02", "02-foundations",        "The Molecule, the Message, and the Machine"),
    ("m03", "03-lexicon",            "Speaking Genomics: The Lexicon"),
    ("m04", "04-sequencing",         "Reading the Code"),
    ("m05", "05-hgp",                "The Human Genome Project"),
    ("m06", "06-bubble",             "Hype, Reality, and the Genomics Bubble"),
    ("m07", "07-epigenetics",        "Epigenetics: Beyond the Sequence"),
    ("m08", "08-applied-genomics",   "Applied Genomics"),
    ("m09", "09-crispr",             "CRISPR and the Age of Gene Editing"),
    ("m10", "10-pharmacogenomics",   "Pharmacogenomics &amp; Precision Medicine"),
    ("m11", "11-consumer",           "Consumer &amp; Ancestry Genomics"),
    ("m12", "12-ethics",             "Ethics, Society &amp; the Shadow of Eugenics"),
    ("m13", "13-clinic",             "Genomics in the Clinic"),
    ("m14", "14-natera",             "Case Study: Natera"),
    ("m15", "15-ai-revolution",      "The AI Revolution: AlphaFold and Beyond"),
]

def extract_hero(doc):
    m = re.search(r'<div class="hero reveal">(.*?)</div>\s*<div class="module-grid">', doc, re.S)
    return '<div class="hero reveal">' + m.group(1) + '</div>'

def extract_article(doc):
    m = re.search(r'<article class="article">(.*?)</article>', doc, re.S)
    return m.group(1)

def extract_inline_scripts(doc):
    return re.findall(r'<script>(.*?)</script>', doc, re.S)

def namespace_ids(content, mid):
    """Prefix element ids (and their #/url references) with the module id so they
    are unique in the single document. Skip chart mounts (fig-*), which the inline
    render scripts reference by their exact, already-unique names."""
    ids = sorted(set(re.findall(r'id="([^"]+)"', content)), key=len, reverse=True)
    for i in ids:
        if i.startswith("fig-"):
            continue
        new = mid + "-" + i
        content = content.replace('id="%s"' % i, 'id="%s"' % new)
        content = content.replace('url(#%s)' % i, 'url(#%s)' % new)
        content = content.replace('"#%s"' % i, '"#%s"' % new)
        content = content.replace("'#%s'" % i, "'#%s'" % new)
    return content

# ---- build module views, with prev/next feet ----
def make_foot(idx):
    prev_html = '<a class="pn pn--prev pn--disabled" href="#home"><small>Course home</small><b>Contents</b></a>'
    next_html = '<a class="pn pn--next" href="#home"><small>Finish &rarr;</small><b>Back to the contents</b></a>'
    if idx > 0:
        pmid, _, ptitle = MODULES[idx - 1]
        prev_html = '<a class="pn pn--prev" href="#%s"><small>&larr; Previous</small><b>%s</b></a>' % (pmid, ptitle)
    if idx < len(MODULES) - 1:
        nmid, _, ntitle = MODULES[idx + 1]
        next_html = '<a class="pn pn--next" href="#%s"><small>Next &rarr;</small><b>%s</b></a>' % (nmid, ntitle)
    return '<nav class="module-foot">%s%s</nav>' % (prev_html, next_html)

# rebuild views with correct feet
render_blocks = []
views = []
for idx, (mid, fname, title) in enumerate(MODULES):
    doc = rd(os.path.join("modules", fname + ".html"))
    hero = extract_hero(doc)
    article = extract_article(doc)
    article = namespace_ids(article, mid)
    for s in extract_inline_scripts(doc):
        render_blocks.append(s.strip())
    views.append(
        '<section class="view" id="%s">\n%s\n<div class="module-grid"><aside class="toc"></aside>'
        '<article class="article">%s</article></div>\n%s\n</section>'
        % (mid, hero, article, make_foot(idx))
    )

# ---- cover (home) from index.html ----
idx_doc = rd("index.html")
def grab(pattern):
    m = re.search(pattern, idx_doc, re.S)
    return m.group(1) if m else ""
cover = grab(r'(<section class="cover">.*?</section>)')
stats = grab(r'(<section class="stats reveal">.*?</section>)')
modules_sec = grab(r'(<section id="modules">.*?</section>)')
home_inner = cover + "\n" + stats + "\n" + modules_sec
# rewrite links to hashes
home_inner = re.sub(r'href="modules/(\d{2})-[^"]+\.html"', r'href="#m\1"', home_inner)
home_inner = re.sub(r'href="glossary\.html"', 'href="#glossary"', home_inner)
home_inner = re.sub(r'href="index\.html"', 'href="#home"', home_inner)
home_inner = re.sub(r'href="#modules"', 'href="#home"', home_inner)

# ---- glossary view ----
glossary_view = (
    '<section class="view" id="glossary">'
    '<div class="hero reveal"><p class="hero__eyebrow">Reference</p>'
    '<h1 class="hero__title">The Genetics 101 Glossary</h1>'
    '<p class="hero__sub">Every key term in the course, defined in plain language. '
    'Throughout the modules, <span class="term" data-term="DNA">dotted terms</span> like this one '
    'reveal their definition on hover or tap. Search below to jump to any concept.</p></div>'
    '<div class="article" style="max-width:760px">'
    '<input id="glossary-search" class="gloss-search" type="search" placeholder="Search terms and definitions..." aria-label="Search glossary">'
    '<p id="glossary-empty" style="display:none;color:var(--ink-faint);font-family:var(--sans)">No terms match your search.</p>'
    '<dl id="glossary-list"></dl></div>'
    '<nav class="module-foot"><a class="pn pn--prev" href="#home"><small>&larr; Back</small><b>All modules</b></a></nav>'
    '</section>'
)

# ---- assets ----
css = rd("assets/css/theme.css")
css += "\n/* single-file view router */\n.view{display:none}\n.view.active{display:block}\n"
js_data = rd("assets/js/data.js")
js_charts = rd("assets/js/charts.js")
js_glossary = rd("assets/js/glossary.js")
js_quiz = rd("assets/js/quiz.js")

ORDER_JS = ",".join('"%s"' % m[0] for m in MODULES)

ROUTER = r"""
(function(){
  "use strict";
  var ORDER = [__ORDER__];
  function isView(id){ var el=document.getElementById(id); return el && el.classList.contains('view'); }
  function updateProgress(){ var b=document.querySelector('.progress'); if(!b) return;
    var h=document.documentElement, max=h.scrollHeight-h.clientHeight;
    b.style.width=(max>0? h.scrollTop/max*100 : 0)+'%'; }
  function revealIn(view){ view.querySelectorAll('.reveal').forEach(function(e){ e.classList.add('in'); }); }
  function buildToc(view){
    var toc=view.querySelector('.toc'); if(!toc) return;
    var heads=view.querySelectorAll('.article h2[id]');
    if(!heads.length){ toc.innerHTML=''; toc.style.display='none'; return; }
    toc.style.display='';
    var html='<h4>On this page</h4>';
    heads.forEach(function(h,i){ html+='<a href="#" data-i="'+i+'">'+(h.getAttribute('data-short')||h.textContent)+'</a>'; });
    html+='<h4 style="margin-top:1.4rem">Course</h4><a href="#home">All modules</a><a href="#glossary">Glossary</a>';
    toc.innerHTML=html;
    var links=toc.querySelectorAll('a[data-i]');
    links.forEach(function(a){ a.addEventListener('click',function(e){ e.preventDefault();
      heads[+a.getAttribute('data-i')].scrollIntoView({behavior:'smooth',block:'start'});
      toc.classList.remove('open'); }); });
    if(view._spy) view._spy.disconnect();
    if('IntersectionObserver' in window){
      view._spy=new IntersectionObserver(function(es){ es.forEach(function(en){ if(en.isIntersecting){
        links.forEach(function(l){ l.classList.remove('active'); });
        var idx=Array.prototype.indexOf.call(heads,en.target); if(links[idx]) links[idx].classList.add('active');
      } }); }, {rootMargin:'-20% 0px -70% 0px'});
      heads.forEach(function(h){ view._spy.observe(h); });
    }
  }
  function show(id){
    if(!isView(id)) id='home';
    var target=document.getElementById(id);
    document.querySelectorAll('.view').forEach(function(v){
      var on=(v===target); v.style.display=on?'block':'none'; v.classList.toggle('active',on);
    });
    window.scrollTo(0,0);
    buildToc(target); revealIn(target); updateProgress();
    var t=document.getElementById('term-tip'); if(t) t.classList.remove('show');
  }
  function onHash(){
    var h=(location.hash||'').replace(/^#/,'');
    if(!h){ show('home'); return; }
    if(isView(h)) show(h);   // in-section anchors are left to the browser
  }
  function curView(){ var v=document.querySelector('.view.active'); return v?v.id:'home'; }
  document.addEventListener('keydown',function(e){
    if(/^(input|textarea|select)$/i.test(e.target.tagName)) return;
    var i=ORDER.indexOf(curView());
    if(e.key==='ArrowRight' && i>-1 && i<ORDER.length-1) location.hash='#'+ORDER[i+1];
    if(e.key==='ArrowLeft'  && i>0) location.hash='#'+ORDER[i-1];
  });
  var mb=document.querySelector('.menu-btn');
  if(mb) mb.addEventListener('click',function(){ var v=document.querySelector('.view.active');
    var toc=v&&v.querySelector('.toc'); if(toc) toc.classList.toggle('open'); });
  window.addEventListener('scroll',updateProgress,{passive:true});
  window.addEventListener('hashchange',onHash);
  onHash();
})();
""".replace("__ORDER__", ORDER_JS)

render_combined = "\n".join(render_blocks)

OUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Genetics 101 - An Interactive Course</title>
<meta name="description" content="A self-paced, interactive course on genetics and genomics, from DNA to the Human Genome Project, the genomics bubble, epigenetics, the diagnostics industry, and the AI revolution in biology.">
<style>
{css}
</style>
</head>
<body>
<div class="progress"></div>
<header class="topbar">
  <a class="topbar__brand" href="#home"><span class="dot"></span> Genetics 101</a>
  <div class="topbar__spacer"></div>
  <a class="topbar__link" href="#home">Modules</a>
  <a class="topbar__link" href="#glossary">Glossary</a>
  <button class="menu-btn" aria-label="Sections">&#9776;</button>
</header>

<main class="layout">
<section class="view active" id="home">
{home_inner}
</section>

{views}

{glossary_view}
</main>

<p class="footer-note">
  Genetics 101 - a self-paced, self-contained course. For learning purposes; not medical or investment advice.<br>
  Use your browser's Print to PDF to export. Company figures draw on a healthcare diagnostics knowledge base; scientific and historical claims reflect the public record as of mid-2026.
</p>

<script>
{js_data}
</script>
<script>
{js_charts}
</script>
<script>
{js_glossary}
</script>
<script>
{js_quiz}
</script>
<script>
{router}
</script>
<script>
/* per-module chart render calls (containers exist in the DOM even while hidden) */
try {{
{render_combined}
}} catch (e) {{ if (window.console) console.error('chart render error', e); }}
</script>
</body>
</html>
""".format(css=css, home_inner=home_inner, views="\n\n".join(views),
           glossary_view=glossary_view, js_data=js_data, js_charts=js_charts,
           js_glossary=js_glossary, js_quiz=js_quiz, router=ROUTER, render_combined=render_combined)

with open(os.path.join(ROOT, "genetics-101.html"), "w", encoding="utf-8") as f:
    f.write(OUT)

print("Wrote genetics-101.html (%d KB)" % (len(OUT.encode("utf-8")) // 1024))
print("Views: %d modules + home + glossary" % len(MODULES))
print("Render blocks inlined: %d" % len(render_blocks))
