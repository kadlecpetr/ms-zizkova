/* MŠ Žižkova – interaktivita webu
 * Zdroj: podklady/main.js, build.py ho kopíruje do assets/js/main.js.
 * Vše je vylepšení: bez JavaScriptu zůstává web plně čitelný a použitelný.
 */
(function () {
  "use strict";

  var doc = document, root = doc.documentElement;
  var EDITOR = /[?&]editor=/.test(location.search);        // uvnitř editoru webu zůstává stránka klidná
  var REDUCED = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); };
  root.classList.add("js");

  /* ───────── mobilní menu ───────── */
  var menu  = doc.getElementById("mobilni-menu");
  var open  = doc.querySelector("[data-menu-open]");
  var close = doc.querySelector("[data-menu-close]");
  function setMenu(show) {
    if (!menu) return;
    menu.hidden = !show;
    menu.classList.toggle("is-open", show);
    if (open) open.setAttribute("aria-expanded", String(show));
    doc.body.style.overflow = show ? "hidden" : "";
  }
  if (open)  open.addEventListener("click", function () { setMenu(true); });
  if (close) close.addEventListener("click", function () { setMenu(false); });
  if (menu)  menu.addEventListener("click", function (e) { if (e.target.tagName === "A") setMenu(false); });

  /* ───────── zvýraznění aktivní položky v podnavigaci ───────── */
  var subnav = doc.querySelector(".subnav");
  var oznacPodnav = function () {};
  if (subnav) {
    var links = $$("a", subnav);
    var cile = links.map(function (a) { return doc.getElementById(a.getAttribute("href").slice(1)); });
    oznacPodnav = function () {
      var y = window.scrollY + 160, akt = 0;
      cile.forEach(function (el, i) { if (el && el.offsetTop <= y) akt = i; });
      links.forEach(function (a, i) { a.classList.toggle("is-active", i === akt); });
    };
    oznacPodnav();
  }

  /* ───────── rok v patičce ───────── */
  $$("[data-rok]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ───────── scroll: stín hlavičky, ukazatel postupu, nahoru, paralaxa ilustrací ───────── */
  var header = doc.querySelector(".header");
  var bar, nahoru;
  if (!EDITOR) {
    bar = doc.createElement("div"); bar.className = "progress"; bar.setAttribute("aria-hidden", "true");
    doc.body.appendChild(bar);
    nahoru = doc.createElement("button");
    nahoru.type = "button"; nahoru.className = "totop"; nahoru.setAttribute("aria-label", "Zpět nahoru");
    nahoru.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 15 6-6 6 6"/></svg>';
    nahoru.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: REDUCED ? "auto" : "smooth" }); });
    doc.body.appendChild(nahoru);
  }
  var tik = false;
  function priScrollu() {
    tik = false;
    var y = window.scrollY, h = doc.documentElement.scrollHeight - window.innerHeight;
    if (header) header.classList.toggle("is-scrolled", y > 8);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (nahoru) nahoru.classList.toggle("is-on", y > 700);
    if (!REDUCED) root.style.setProperty("--par", Math.round(y * -0.12) + "px");
    oznacPodnav();
  }
  window.addEventListener("scroll", function () {
    if (!tik) { tik = true; window.requestAnimationFrame(priScrollu); }
  }, { passive: true });
  priScrollu();

  /* ───────── postupné objevování prvků při rolování ───────── */
  if (!EDITOR && !REDUCED && "IntersectionObserver" in window) {
    var cileObj = $$(".section-head, .card, .post, .pillar, .quick__card, .team__class, .doc, .vykres, .vykres-pas, .alert, .plakat__obr, .map, .gallery figure, .cta, .acc");
    var io = new IntersectionObserver(function (zaznamy) {
      zaznamy.forEach(function (z) {
        if (z.isIntersecting) { z.target.classList.add("is-in"); io.unobserve(z.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    cileObj.forEach(function (el) {
      // zpoždění podle pořadí mezi sourozenci, aby karty naskakovaly za sebou
      var poradi = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.setProperty("--d", Math.min(poradi, 6) * 70 + "ms");
      el.classList.add("reveal");
      io.observe(el);
    });
  }

  /* ───────── počítání čísel v odznáčku (3 třídy, 71 dětí) ───────── */
  if (!EDITOR && !REDUCED && "IntersectionObserver" in window) {
    var cisla = $$(".hero__badge b").filter(function (b) { return /^\d+$/.test(b.textContent.trim()); });
    cisla.forEach(function (b) {
      var cil = parseInt(b.textContent, 10);
      b.textContent = "0";
      setTimeout(function () { if (b.textContent === "0") b.textContent = String(cil); }, 4000);
      var obs = new IntersectionObserver(function (z) {
        if (!z[0].isIntersecting) return;
        obs.disconnect();
        var start = null, dur = 900;
        (function krok(t) {
          if (start === null) start = t;
          var p = Math.min(1, (t - start) / dur);
          b.textContent = Math.round(cil * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(krok);
        })(performance.now());
      });
      obs.observe(b);
    });
  }

  /* ───────── je školka právě otevřená? + aktuální část dne ───────── */
  function praha() {
    // aktuální čas v Praze bez ohledu na pásmo návštěvníka
    var p = new Intl.DateTimeFormat("en-GB", {
      timeZone: "Europe/Prague", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false
    }).formatToParts(new Date()), o = {};
    p.forEach(function (x) { o[x.type] = x.value; });
    var den = { Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6, Sun: 0 }[o.weekday];
    return { den: den, min: (parseInt(o.hour, 10) % 24) * 60 + parseInt(o.minute, 10) };
  }
  function hm(t) { var m = String(t).match(/(\d{1,2})[.:](\d{2})/); return m ? parseInt(m[1], 10) * 60 + parseInt(m[2], 10) : null; }
  function fmt(min) { return Math.floor(min / 60) + "." + ("0" + (min % 60)).slice(-2); }

  var stav = doc.querySelector("[data-stav]");
  var OD = 6 * 60 + 30, DO = 16 * 60 + 30;
  if (stav) { OD = hm(stav.getAttribute("data-od")) || OD; DO = hm(stav.getAttribute("data-do")) || DO; }
  var ted;
  try { ted = praha(); } catch (e) { ted = null; }
  var pracovni = ted && ted.den >= 1 && ted.den <= 5;
  var otevreno = !!(pracovni && ted.min >= OD && ted.min < DO);

  if (stav && ted) {
    var text, trida;
    if (otevreno) { text = "Právě je otevřeno – do " + fmt(DO); trida = "is-open"; }
    else if (pracovni && ted.min < OD) { text = "Zavřeno – dnes otevíráme v " + fmt(OD); trida = "is-closed"; }
    else {
      var dalsi = ted.den === 5 ? "v pondělí" : (ted.den === 6 ? "v pondělí" : (ted.den === 0 ? "zítra" : "zítra"));
      text = "Zavřeno – otevíráme " + dalsi + " v " + fmt(OD); trida = "is-closed";
    }
    stav.textContent = text; stav.classList.add(trida); stav.hidden = false;
    stav.title = "Podle běžné provozní doby. Svátky a prázdninový provoz najdete v aktualitách.";
  }

  $$(".daily").forEach(function (seznam) {
    var polozky = $$("li", seznam), casy = polozky.map(function (li) {
      var t = li.querySelector("time"); return t ? hm(t.textContent) : null;
    });
    if (!casy.length || casy.some(function (c) { return c === null; })) return;   // jen seznamy s hodinami
    seznam.classList.add("daily--live");
    if (!ted || !otevreno) return;
    var akt = -1;
    casy.forEach(function (c, i) { if (c <= ted.min) akt = i; });
    if (akt < 0) return;
    polozky[akt].classList.add("is-now");
    var stitek = doc.createElement("em"); stitek.className = "daily__now"; stitek.textContent = "právě teď";
    polozky[akt].querySelector("span").insertBefore(stitek, polozky[akt].querySelector("span").firstChild);
  });

  /* ───────── lightbox pro výkresy a fotografie ───────── */
  if (!EDITOR) {
    var skup = $$(".vykres img, .vykres-pas img, .gallery img");
    var plakat = $$(".plakat__obr a");
    var polozkyLb = [];
    var otevri = function () {};
    function zaregistruj(el, plny, popis) {
      var idx = polozkyLb.push({ el: el, src: plny, popis: popis, alt: el.alt || "" }) - 1;
      el.setAttribute("tabindex", "0"); el.setAttribute("role", "button");
      el.setAttribute("aria-label", "Zvětšit: " + (el.alt || "obrázek"));
      el.style.cursor = "zoom-in";
      el.addEventListener("click", function (e) { e.preventDefault(); otevri(idx); });
      el.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); otevri(idx); } });
    }
    skup.forEach(function (img) {
      var fig = img.closest("figure"), cap = fig && fig.querySelector("figcaption");
      zaregistruj(img, img.getAttribute("src").replace("-nahled.", "."), cap ? cap.textContent.trim() : "");
    });
    plakat.forEach(function (a) {
      var img = a.querySelector("img");
      zaregistruj(a, a.getAttribute("href"), img ? img.alt : "");
    });

    if (polozkyLb.length) {
      var lb = doc.createElement("div");
      lb.className = "lb"; lb.hidden = true; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-modal", "true"); lb.setAttribute("aria-label", "Zvětšený obrázek");
      lb.innerHTML = '<button type="button" class="lb__x" aria-label="Zavřít">&times;</button>' +
        '<button type="button" class="lb__p lb__prev" aria-label="Předchozí">&#8249;</button>' +
        '<figure class="lb__fig"><img alt=""><figcaption></figcaption></figure>' +
        '<button type="button" class="lb__p lb__next" aria-label="Další">&#8250;</button>';
      doc.body.appendChild(lb);
      var lbImg = lb.querySelector("img"), lbCap = lb.querySelector("figcaption"), akt = 0, naposled = null;
      function zobraz(i) {
        akt = (i + polozkyLb.length) % polozkyLb.length;
        var p = polozkyLb[akt];
        lbImg.classList.remove("is-in");
        lbImg.onload = function () { lbImg.classList.add("is-in"); };
        lbImg.src = p.src; lbImg.alt = p.alt; lbCap.textContent = p.popis;
        lb.classList.toggle("lb--single", polozkyLb.length < 2);
      }
      otevri = function (i) {
        naposled = doc.activeElement; zobraz(i);
        lb.hidden = false; doc.body.style.overflow = "hidden";
        lb.querySelector(".lb__x").focus();
      };
      function zavri() {
        lb.hidden = true; doc.body.style.overflow = "";
        if (naposled && naposled.focus) naposled.focus();
      }
      lb.addEventListener("click", function (e) {
        if (e.target.closest(".lb__x") || e.target === lb) zavri();
        else if (e.target.closest(".lb__prev")) zobraz(akt - 1);
        else if (e.target.closest(".lb__next")) zobraz(akt + 1);
      });
      doc.addEventListener("keydown", function (e) {
        if (lb.hidden) return;
        if (e.key === "Escape") zavri();
        else if (e.key === "ArrowLeft") zobraz(akt - 1);
        else if (e.key === "ArrowRight") zobraz(akt + 1);
        else if (e.key === "Tab") {                       // focus zůstává uvnitř okna
          var b = $$("button", lb).filter(function (x) { return x.offsetParent !== null; });
          if (!b.length) return;
          var prvni = b[0], posl = b[b.length - 1];
          if (e.shiftKey && doc.activeElement === prvni) { e.preventDefault(); posl.focus(); }
          else if (!e.shiftKey && doc.activeElement === posl) { e.preventDefault(); prvni.focus(); }
        }
      });
      var x0 = null;
      lb.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
      lb.addEventListener("touchend", function (e) {
        if (x0 === null) return;
        var dx = e.changedTouches[0].clientX - x0; x0 = null;
        if (Math.abs(dx) > 50) zobraz(akt + (dx < 0 ? 1 : -1));
      });
    }
  }

  /* ───────── hledání v dokumentech ke stažení ───────── */
  if (!EDITOR) {
    $$(".docs").forEach(function (seznam, n) {
      var docs = $$(".doc", seznam);
      if (docs.length < 6) return;
      var id = "hledat-dok-" + n;
      var wrap = doc.createElement("div"); wrap.className = "hledani";
      wrap.innerHTML = '<label class="sr" for="' + id + '">Hledat v dokumentech</label>' +
        '<input id="' + id + '" type="search" placeholder="Hledat dokument (např. řád, GDPR, rozpočet)…" autocomplete="off">' +
        '<p class="hledani__nic" hidden>Nic jsme nenašli. Zkuste jiné slovo.</p>';
      seznam.parentNode.insertBefore(wrap, seznam);
      var inp = wrap.querySelector("input"), nic = wrap.querySelector(".hledani__nic");
      function bez(s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
      inp.addEventListener("input", function () {
        var q = bez(inp.value.trim()), nalez = 0;
        docs.forEach(function (d) {
          var ok = !q || bez(d.textContent).indexOf(q) > -1;
          d.hidden = !ok; if (ok) nalez++;
        });
        nic.hidden = nalez > 0;
      });
    });

    /* rozbalit / sbalit všechny odpovědi */
    var skupiny = [];
    $$("details.acc").forEach(function (d) {
      var rodic = d.parentNode;
      if (skupiny.indexOf(rodic) < 0) skupiny.push(rodic);
    });
    skupiny.forEach(function (rodic) {
      var ds = $$("details.acc", rodic);
      if (ds.length < 3) return;
      var b = doc.createElement("button");
      b.type = "button"; b.className = "acc__all"; b.textContent = "Rozbalit vše";
      b.addEventListener("click", function () {
        var vse = ds.every(function (d) { return d.open; });
        ds.forEach(function (d) { d.open = !vse; });
        b.textContent = vse ? "Rozbalit vše" : "Sbalit vše";
      });
      rodic.insertBefore(b, ds[0]);
      ds.forEach(function (d) {
        d.addEventListener("toggle", function () {
          b.textContent = ds.every(function (x) { return x.open; }) ? "Sbalit vše" : "Rozbalit vše";
        });
      });
    });
  }

  /* ───────── kontaktní formulář (otevře e-mail s připravenou zprávou) ───────── */
  $$("form.form[data-mailto]").forEach(function (f) {
    var stavEl = f.querySelector(".form__stav");
    function chyba(pole, text) {
      pole.setAttribute("aria-invalid", "true");
      var m = pole.nextElementSibling;
      if (!m || !m.classList.contains("form__err")) { m = doc.createElement("span"); m.className = "form__err"; pole.insertAdjacentElement("afterend", m); }
      m.textContent = text;
    }
    function ciste() {
      $$("[aria-invalid]", f).forEach(function (p) { p.removeAttribute("aria-invalid"); });
      $$(".form__err", f).forEach(function (m) { m.remove(); });
    }
    f.addEventListener("input", function (e) {
      if (e.target.hasAttribute("aria-invalid")) {
        e.target.removeAttribute("aria-invalid");
        var m = e.target.nextElementSibling; if (m && m.classList.contains("form__err")) m.remove();
      }
    });
    f.addEventListener("submit", function (e) {
      e.preventDefault(); ciste(); stavEl.textContent = ""; stavEl.className = "form__stav";
      var jmeno = f.elements.jmeno, mail = f.elements.email, tema = f.elements.tema, zprava = f.elements.zprava, souhlas = f.elements.souhlas;
      var prvniChyba = null;
      function zle(p, t) { chyba(p, t); if (!prvniChyba) prvniChyba = p; }
      if (!jmeno.value.trim()) zle(jmeno, "Napište prosím své jméno.");
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail.value.trim())) zle(mail, "Zadejte e-mail ve tvaru jmeno@domena.cz.");
      if (zprava.value.trim().length < 10) zle(zprava, "Zpráva je příliš krátká.");
      if (!souhlas.checked) zle(souhlas, "Bez souhlasu zprávu připravit nemůžeme.");
      if (prvniChyba) { prvniChyba.focus(); return; }
      var predmet = "Dotaz z webu: " + tema.value;
      var telo = zprava.value.trim() + "\n\n— " + jmeno.value.trim() + " (" + mail.value.trim() + ")";
      location.href = "mailto:" + f.getAttribute("data-mailto") + "?subject=" + encodeURIComponent(predmet) + "&body=" + encodeURIComponent(telo);
      stavEl.className = "form__stav is-ok";
      stavEl.textContent = "Otevřeli jsme váš e-mailový program s připravenou zprávou. Stačí ji odeslat. Pokud se nic neotevřelo, napište nám na " + f.getAttribute("data-mailto") + ".";
    });
  });

  /* ───────── kopírování e-mailu / telefonu ───────── */
  $$("[data-kopirovat]").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = b.getAttribute("data-kopirovat"), puvodni = b.textContent;
      function hotovo() { b.textContent = "Zkopírováno ✓"; setTimeout(function () { b.textContent = puvodni; }, 1800); }
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(hotovo, function () {});
    });
  });

  /* Esc zavírá mobilní menu */
  doc.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
})();
