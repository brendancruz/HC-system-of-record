/* ============================================================================
   GChart - a tiny dependency-free SVG charting library for Genetics 101.
   Renders crisp, themeable SVG (colors come from CSS where possible).
   API: GChart.line / GChart.bars / GChart.scatter / GChart.donut
   Each takes a mount element id and an options object.
   ========================================================================== */
(function (global) {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var PALETTE = ["#283593", "#138a72", "#c2456b", "#b8860b", "#5a6acf", "#2a9d8f"];

  function el(tag, attrs, text) {
    var n = document.createElementNS(NS, tag);
    if (attrs) for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (text != null) n.textContent = text;
    return n;
  }
  function fmtMoney(v) {
    if (v >= 1e9) return "$" + (v / 1e9).toFixed(v % 1e9 ? 1 : 0) + "B";
    if (v >= 1e6) return "$" + Math.round(v / 1e6) + "M";
    if (v >= 1e3) return "$" + Math.round(v / 1e3) + "k";
    return "$" + v;
  }
  function mount(id) {
    var box = document.getElementById(id);
    if (box) box.innerHTML = "";
    return box;
  }
  function svgRoot(box, w, h) {
    var svg = el("svg", { viewBox: "0 0 " + w + " " + h, class: "chart-svg", role: "img" });
    box.appendChild(svg);
    return svg;
  }
  function legend(box, items) {
    var L = document.createElement("div");
    L.className = "legend";
    items.forEach(function (it) {
      var s = document.createElement("span");
      s.innerHTML = '<i style="background:' + it.color + '"></i>' + it.name;
      L.appendChild(s);
    });
    box.appendChild(L);
  }

  /* ---- LINE (linear or log y), multi-series, annotations ----------------- */
  function line(id, o) {
    var box = mount(id); if (!box) return;
    var W = 760, H = o.height || 400, m = { t: 24, r: 26, b: 46, l: 64 };
    var svg = svgRoot(box, W, H);
    var iw = W - m.l - m.r, ih = H - m.t - m.b;

    var all = [];
    o.series.forEach(function (s) { s.data.forEach(function (p) { all.push(p); }); });
    var xs = all.map(function (p) { return p.x; });
    var ys = all.map(function (p) { return p.y; });
    var xmin = o.xMin != null ? o.xMin : Math.min.apply(null, xs);
    var xmax = o.xMax != null ? o.xMax : Math.max.apply(null, xs);
    var log = o.yScale === "log";
    var ymin = o.yMin != null ? o.yMin : Math.min.apply(null, ys);
    var ymax = o.yMax != null ? o.yMax : Math.max.apply(null, ys);
    if (!log) { ymin = Math.min(ymin, 0); }

    function X(v) { return m.l + (v - xmin) / (xmax - xmin) * iw; }
    function Y(v) {
      if (log) {
        var a = Math.log10(ymin), b = Math.log10(ymax);
        return m.t + ih - (Math.log10(v) - a) / (b - a) * ih;
      }
      return m.t + ih - (v - ymin) / (ymax - ymin) * ih;
    }

    // y gridlines + labels
    var yticks = [];
    if (log) {
      var lo = Math.floor(Math.log10(ymin)), hi = Math.ceil(Math.log10(ymax));
      for (var e = lo; e <= hi; e++) yticks.push(Math.pow(10, e));
    } else {
      var step = niceStep((ymax - ymin) / 5);
      for (var v = 0; v <= ymax + 1e-9; v += step) yticks.push(v);
    }
    var grid = el("g", { class: "grid" }); svg.appendChild(grid);
    var axis = el("g", { class: "axis" }); svg.appendChild(axis);
    yticks.forEach(function (t) {
      var y = Y(t);
      grid.appendChild(el("line", { x1: m.l, y1: y, x2: m.l + iw, y2: y }));
      axis.appendChild(el("text", { x: m.l - 10, y: y + 4, "text-anchor": "end", "font-size": 12 },
        o.yFormat === "money" ? fmtMoney(t) : (o.yFormat === "pct" ? t + "%" : shortNum(t))));
    });
    // x labels
    (o.xTicks || []).forEach(function (t) {
      axis.appendChild(el("text", { x: X(t), y: m.t + ih + 26, "text-anchor": "middle", "font-size": 12 }, o.xFormat ? o.xFormat(t) : t));
    });
    axis.appendChild(el("line", { x1: m.l, y1: m.t + ih, x2: m.l + iw, y2: m.t + ih }));

    // series
    o.series.forEach(function (s, i) {
      var color = s.color || PALETTE[i % PALETTE.length];
      var d = s.data.map(function (p, j) { return (j ? "L" : "M") + X(p.x).toFixed(1) + " " + Y(p.y).toFixed(1); }).join(" ");
      svg.appendChild(el("path", { d: d, fill: "none", stroke: color, "stroke-width": s.width || 3,
        "stroke-dasharray": s.dashed ? "7 5" : "0", "stroke-linejoin": "round", "stroke-linecap": "round", opacity: s.dashed ? 0.7 : 1 }));
      if (s.dots !== false) s.data.forEach(function (p) {
        var c = el("circle", { cx: X(p.x), cy: Y(p.y), r: s.dashed ? 0 : 3.4, fill: "#fff", stroke: color, "stroke-width": 2 });
        c.appendChild(el("title", null, (o.xFormat ? o.xFormat(p.x) : p.x) + ": " + (o.yFormat === "money" ? fmtMoney(p.y) : p.y)));
        svg.appendChild(c);
      });
    });

    // annotations (callouts at points)
    (o.annotations || []).forEach(function (a) {
      var x = X(a.x), y = Y(a.y);
      svg.appendChild(el("circle", { cx: x, cy: y, r: 5, fill: a.color || "#c2456b" }));
      var dy = a.up === false ? 22 : -12, anchor = a.anchor || "middle";
      var tx = x + (a.dx || 0);
      a.text.split("\n").forEach(function (ln, k) {
        svg.appendChild(el("text", { x: tx, y: y + dy + k * 14, "text-anchor": anchor, "font-size": 11.5, "font-weight": k ? 400 : 700, fill: a.color || "#9a2f4e" }, ln));
      });
    });

    if (o.yLabel) {
      var t = el("text", { x: 16, y: m.t + ih / 2, "text-anchor": "middle", "font-size": 12, transform: "rotate(-90 16 " + (m.t + ih / 2) + ")", fill: "#6b7384" }, o.yLabel);
      svg.appendChild(t);
    }
    if (o.legend !== false && o.series.length > 1) legend(box, o.series.map(function (s, i) { return { name: s.name, color: s.color || PALETTE[i % PALETTE.length] }; }));
  }

  /* ---- BARS (categorical, single or grouped) ----------------------------- */
  function bars(id, o) {
    var box = mount(id); if (!box) return;
    var W = 760, H = o.height || 400, m = { t: 28, r: 24, b: 64, l: 60 };
    var svg = svgRoot(box, W, H);
    var iw = W - m.l - m.r, ih = H - m.t - m.b;
    var cats = o.categories;
    var series = o.series;
    var ymax = o.yMax != null ? o.yMax : Math.max.apply(null, series.reduce(function (a, s) { return a.concat(s.data); }, []));
    var step = niceStep(ymax / 5); var top = Math.ceil(ymax / step) * step;
    function Y(v) { return m.t + ih - v / top * ih; }

    var grid = el("g", { class: "grid" }); svg.appendChild(grid);
    var axis = el("g", { class: "axis" }); svg.appendChild(axis);
    for (var v = 0; v <= top + 1e-9; v += step) {
      var y = Y(v);
      grid.appendChild(el("line", { x1: m.l, y1: y, x2: m.l + iw, y2: y }));
      axis.appendChild(el("text", { x: m.l - 10, y: y + 4, "text-anchor": "end", "font-size": 12 },
        o.yFormat === "money" ? fmtMoney(v) : (o.yFormat === "pct" ? v + "%" : shortNum(v))));
    }
    axis.appendChild(el("line", { x1: m.l, y1: m.t + ih, x2: m.l + iw, y2: m.t + ih }));

    var bw = iw / cats.length;
    var n = series.length;
    var inner = Math.min(bw * 0.62, 64);
    var gap = 4;
    var each = (inner - gap * (n - 1)) / n;

    cats.forEach(function (cat, ci) {
      var cx = m.l + bw * ci + bw / 2;
      series.forEach(function (s, si) {
        var val = s.data[ci];
        var color = s.colors ? s.colors[ci] : (s.color || PALETTE[si % PALETTE.length]);
        var x = cx - inner / 2 + si * (each + gap);
        var y = Y(val), h = m.t + ih - y;
        var r = el("rect", { x: x, y: y, width: each, height: Math.max(0, h), rx: 4, fill: color, opacity: s.faded && s.faded[ci] ? 0.4 : 1 });
        r.appendChild(el("title", null, cat + " - " + s.name + ": " + (o.yFormat === "money" ? fmtMoney(val) : val)));
        svg.appendChild(r);
        if (o.valueLabels) svg.appendChild(el("text", { x: x + each / 2, y: y - 6, "text-anchor": "middle", "font-size": 11.5, "font-weight": 700, fill: color },
          o.yFormat === "money" ? fmtMoney(val) : (o.yFormat === "pct" ? val + "%" : shortNum(val))));
      });
      // category label (wrap on space if long)
      var label = el("text", { x: cx, y: m.t + ih + 22, "text-anchor": "middle", "font-size": 12 });
      var words = String(cat).split("\n");
      words.forEach(function (w, k) { label.appendChild(el("tspan", { x: cx, dy: k ? 14 : 0 }, w)); });
      svg.appendChild(label);
    });

    if (o.legend && series.length > 1) legend(box, series.map(function (s, i) { return { name: s.name, color: s.color || PALETTE[i % PALETTE.length] }; }));
  }

  /* ---- SCATTER (labeled bubbles) ----------------------------------------- */
  function scatter(id, o) {
    var box = mount(id); if (!box) return;
    var W = 760, H = o.height || 440, m = { t: 26, r: 30, b: 56, l: 64 };
    var svg = svgRoot(box, W, H);
    var iw = W - m.l - m.r, ih = H - m.t - m.b;
    var xs = o.points.map(function (p) { return p.x; }), ys = o.points.map(function (p) { return p.y; });
    var xmin = o.xMin != null ? o.xMin : 0, xmax = o.xMax != null ? o.xMax : Math.max.apply(null, xs) * 1.1;
    var ymin = o.yMin != null ? o.yMin : 0, ymax = o.yMax != null ? o.yMax : Math.max.apply(null, ys) * 1.15;
    function X(v) { return m.l + (v - xmin) / (xmax - xmin) * iw; }
    function Y(v) { return m.t + ih - (v - ymin) / (ymax - ymin) * ih; }

    var grid = el("g", { class: "grid" }); svg.appendChild(grid);
    var axis = el("g", { class: "axis" }); svg.appendChild(axis);
    var xstep = niceStep((xmax - xmin) / 5);
    for (var xv = Math.ceil(xmin / xstep) * xstep; xv <= xmax; xv += xstep) {
      grid.appendChild(el("line", { x1: X(xv), y1: m.t, x2: X(xv), y2: m.t + ih }));
      axis.appendChild(el("text", { x: X(xv), y: m.t + ih + 24, "text-anchor": "middle", "font-size": 12 }, o.xFormat ? o.xFormat(xv) : xv));
    }
    var ystep = niceStep((ymax - ymin) / 5);
    for (var yv = Math.ceil(ymin / ystep) * ystep; yv <= ymax; yv += ystep) {
      grid.appendChild(el("line", { x1: m.l, y1: Y(yv), x2: m.l + iw, y2: Y(yv) }));
      axis.appendChild(el("text", { x: m.l - 10, y: Y(yv) + 4, "text-anchor": "end", "font-size": 12 }, o.yFormat ? o.yFormat(yv) : yv));
    }
    axis.appendChild(el("line", { x1: m.l, y1: m.t + ih, x2: m.l + iw, y2: m.t + ih }));

    if (o.diagonal) {
      var d0 = Math.max(xmin, ymin), d1 = Math.min(xmax, ymax);
      svg.appendChild(el("line", { x1: X(d0), y1: Y(d0), x2: X(d1), y2: Y(d1),
        stroke: "#6b7384", "stroke-width": 1.5, "stroke-dasharray": "6 5", opacity: 0.7 }));
      svg.appendChild(el("text", { x: X(d1) - 6, y: Y(d1) + 16, "text-anchor": "end", "font-size": 11, fill: "#6b7384" }, o.diagonalLabel || "y = x"));
    }

    o.points.forEach(function (p, i) {
      var color = p.color || PALETTE[i % PALETTE.length];
      var r = p.r || 9;
      var c = el("circle", { cx: X(p.x), cy: Y(p.y), r: r, fill: color, opacity: 0.82, stroke: "#fff", "stroke-width": 1.5 });
      c.appendChild(el("title", null, p.label + " (" + (o.xName || "x") + " " + p.x + ", " + (o.yName || "y") + " " + p.y + ")"));
      svg.appendChild(c);
      if (p.label) svg.appendChild(el("text", { x: X(p.x), y: Y(p.y) - r - 5, "text-anchor": "middle", "font-size": 11.5, "font-weight": 700, fill: "#3d4554" }, p.label));
    });
    if (o.xLabel) svg.appendChild(el("text", { x: m.l + iw / 2, y: H - 8, "text-anchor": "middle", "font-size": 12, fill: "#6b7384" }, o.xLabel));
    if (o.yLabel) svg.appendChild(el("text", { x: 16, y: m.t + ih / 2, "text-anchor": "middle", "font-size": 12, transform: "rotate(-90 16 " + (m.t + ih / 2) + ")", fill: "#6b7384" }, o.yLabel));
  }

  /* ---- DONUT ------------------------------------------------------------- */
  function donut(id, o) {
    var box = mount(id); if (!box) return;
    var W = 760, H = o.height || 360;
    var svg = svgRoot(box, W, H);
    var cx = 200, cy = H / 2, R = 130, r = 78;
    var total = o.segments.reduce(function (a, s) { return a + s.value; }, 0);
    var ang = -Math.PI / 2;
    o.segments.forEach(function (s, i) {
      var frac = s.value / total, a2 = ang + frac * 2 * Math.PI;
      var large = frac > 0.5 ? 1 : 0;
      var color = s.color || PALETTE[i % PALETTE.length];
      var p = ["M", cx + R * Math.cos(ang), cy + R * Math.sin(ang),
        "A", R, R, 0, large, 1, cx + R * Math.cos(a2), cy + R * Math.sin(a2),
        "L", cx + r * Math.cos(a2), cy + r * Math.sin(a2),
        "A", r, r, 0, large, 0, cx + r * Math.cos(ang), cy + r * Math.sin(ang), "Z"].join(" ");
      var path = el("path", { d: p, fill: color });
      path.appendChild(el("title", null, s.name + ": " + Math.round(frac * 100) + "%"));
      svg.appendChild(path);
      ang = a2;
    });
    if (o.centerLabel) {
      svg.appendChild(el("text", { x: cx, y: cy - 4, "text-anchor": "middle", "font-size": 22, "font-weight": 800, fill: "#1b1f27" }, o.centerLabel));
      if (o.centerSub) svg.appendChild(el("text", { x: cx, y: cy + 18, "text-anchor": "middle", "font-size": 12, fill: "#6b7384" }, o.centerSub));
    }
    // legend on right
    var ly = cy - o.segments.length * 16;
    o.segments.forEach(function (s, i) {
      var color = s.color || PALETTE[i % PALETTE.length];
      svg.appendChild(el("rect", { x: 400, y: ly + i * 34, width: 16, height: 16, rx: 4, fill: color }));
      svg.appendChild(el("text", { x: 426, y: ly + i * 34 + 9, "font-size": 13.5, "font-weight": 700, fill: "#1b1f27" }, s.name));
      svg.appendChild(el("text", { x: 426, y: ly + i * 34 + 26, "font-size": 12, fill: "#6b7384" },
        Math.round(s.value / total * 100) + "%" + (s.note ? " - " + s.note : "")));
    });
  }

  /* ---- helpers ----------------------------------------------------------- */
  function niceStep(raw) {
    var pow = Math.pow(10, Math.floor(Math.log10(raw)));
    var n = raw / pow;
    var s = n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10;
    return s * pow;
  }
  function shortNum(v) {
    if (Math.abs(v) >= 1e9) return (v / 1e9).toFixed(1).replace(/\.0$/, "") + "B";
    if (Math.abs(v) >= 1e6) return (v / 1e6).toFixed(1).replace(/\.0$/, "") + "M";
    if (Math.abs(v) >= 1e3) return (v / 1e3).toFixed(1).replace(/\.0$/, "") + "k";
    return String(v);
  }

  global.GChart = { line: line, bars: bars, scatter: scatter, donut: donut, fmtMoney: fmtMoney };
})(window);
