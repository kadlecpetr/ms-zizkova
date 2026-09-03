/* MŠ Žižkova – drobná interaktivita */
(function () {
  "use strict";

  /* --- mobilní menu --- */
  var menu  = document.getElementById("mobilni-menu");
  var open  = document.querySelector("[data-menu-open]");
  var close = document.querySelector("[data-menu-close]");

  function setMenu(show) {
    if (!menu) return;
    menu.hidden = !show;
    menu.classList.toggle("is-open", show);
    if (open) open.setAttribute("aria-expanded", String(show));
    document.body.style.overflow = show ? "hidden" : "";
  }
  if (open)  open.addEventListener("click", function () { setMenu(true); });
  if (close) close.addEventListener("click", function () { setMenu(false); });
  if (menu)  menu.addEventListener("click", function (e) {
    if (e.target.tagName === "A") setMenu(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setMenu(false);
  });

  /* --- zvýraznění aktivní položky v podnavigaci --- */
  var subnav = document.querySelector(".subnav");
  if (subnav) {
    var links = Array.prototype.slice.call(subnav.querySelectorAll("a"));
    var cile  = links.map(function (a) {
      return document.getElementById(a.getAttribute("href").slice(1));
    });
    var tik = false;
    function oznac() {
      tik = false;
      var y = window.scrollY + 160, akt = 0;
      cile.forEach(function (el, i) { if (el && el.offsetTop <= y) akt = i; });
      links.forEach(function (a, i) { a.classList.toggle("is-active", i === akt); });
    }
    window.addEventListener("scroll", function () {
      if (!tik) { tik = true; window.requestAnimationFrame(oznac); }
    }, { passive: true });
    oznac();
  }

  /* --- rok v patičce --- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-rok]"), function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
