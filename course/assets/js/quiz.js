/* ============================================================================
   Knowledge-check engine. Declarative: each question is
   <div class="q" data-answer="2"> with .opt buttons and a .q__explain block.
   data-answer is the 0-based index of the correct option.
   ========================================================================== */
(function () {
  "use strict";
  function letter(i) { return String.fromCharCode(65 + i); }

  function init() {
    document.querySelectorAll(".q").forEach(function (q) {
      var opts = Array.prototype.slice.call(q.querySelectorAll(".opt"));
      var answer = parseInt(q.getAttribute("data-answer"), 10);
      var explain = q.querySelector(".q__explain");
      opts.forEach(function (opt, i) {
        // ensure a letter marker exists
        if (!opt.querySelector(".mark")) {
          var mk = document.createElement("span");
          mk.className = "mark"; mk.textContent = letter(i);
          opt.insertBefore(mk, opt.firstChild);
        }
        opt.addEventListener("click", function () {
          if (q.dataset.done) return;
          q.dataset.done = "1";
          opts.forEach(function (o, j) {
            o.setAttribute("disabled", "");
            if (j === answer) o.classList.add("correct");
            else if (j === i) o.classList.add("wrong");
          });
          if (explain) explain.classList.add("show");
        });
      });
    });
  }
  if (document.readyState !== "loading") init();
  else document.addEventListener("DOMContentLoaded", init);
})();
