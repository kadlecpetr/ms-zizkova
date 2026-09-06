#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sestaví z hotového webu JEDEN samostatný HTML soubor pro klientský náhled.

Všechny stránky jsou v něm jako sekce, přepínají se JavaScriptem přes hash
(#skola, #pro-rodice/stravovani). CSS, JS i obrázky jsou inlinované, odkazy
na dokumenty míří na CDN starého webu, aby fungovaly i v náhledu.

Spuštění:  python3 build_preview.py   →  nahled/ms-zizkova-nahled.html
"""
import os, re, base64

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "nahled")

STRANKY = [
    ("index.html",       "Domů"),
    ("skola.html",       "Škola"),
    ("vzdelavani.html",  "Vzdělávání"),
    ("projekty.html",    "Projekty a spolupráce"),
    ("pro-rodice.html",  "Pro rodiče"),
    ("zapis.html",       "Zápis do MŠ"),
    ("aktuality.html",   "Aktuality"),
    ("fotogalerie.html", "Fotogalerie"),
    ("kontakty.html",    "Kontakty"),
]
SLUG = {f: f[:-5] for f, _ in STRANKY}

# dokumenty → CDN starého webu, ať jsou v náhledu funkční
CDN = "https://7fd136a065.clvaw-cdnwnd.com/2d96c8637c5d218c5e87d3d1d35a264a"
DOKUMENTY = {
 "skolni-vzdelavaci-program.docx": "/200000006-445c4445c6/SVP_1.9.2024.docx",
 "skolni-rad.docx": "/200000007-df410df412/Skolni_rad_od_1.9.2024.docx",
 "dodatek-ke-skolnimu-radu.pdf": "/200000153-7cf487cf4a/Dodatek%20ke%20%C5%A1koln%C3%ADmu%20%C5%99%C3%A1du.pdf",
 "rad-skolni-jidelny-2026-2027.docx": "/200000228-251f0251f3/%C5%98%C3%81D%20%C5%A0KOLN%C3%8D%20J%C3%8DDELNY%202026-2027.docx",
 "uplata-skolne-2026-2027.pdf": "/200000201-266a1266a3/Uplata_za_predskolni_vzdelavani_skolni_rok_2026-2027-0.pdf",
 "uplata-stravne-2026-2027.docx": "/200000227-ba3ebba3ed/%C3%9Aplata%202026-2027.docx",
 "potvrzeni-o-zaplaceni-skolneho.doc": "/200000008-0dbf50dc04/Potvrzeni_o_zaplaceni_skolneho_za_predskolni_vzdelavani.doc",
 "spadove-obvody-ms.pdf": "/200000011-0fde50fde7/Spadove_obvody_materskych_skol.pdf",
 "dite-do-ms-jen-kdyz-je-zdrave.pdf": "/200000012-7a4217a422/Dite_nechodi_do_MS_porad_jen_kdyz_je_zdrave.pdf",
 "gdpr-informacni-memorandum.pdf": "/200000013-ad9b8ad9bb/GDPR_Memorandum_2019.pdf",
 "zrizovaci-listina.pdf": "/200000015-29cbf29cd1/ZL_MS_Zizkova_57.pdf",
 "vyrocni-zprava-2025.doc": "/200000184-342d1342d3/V%C3%BDro%C4%8Dn%C3%AD%20zpr%C3%A1va%20za%20rok%202025.doc",
 "rozpocet-2026.docx": "/200000203-1d8341d836/Rozpo%C4%8Det%202026.docx",
 "strednedoby-vyhled-rozpoctu-2026-2028.pdf": "/200000204-7ce7b7ce7d/Strednedoby_vyhled_rozpoctu_2026-2028.pdf",
 "prazdninovy-provoz-2026.xlsx": "/200000208-e90cee90d0/Pr%C3%A1zdninov%C3%BD%20provoz%202026.xlsx",
 "plakat-map-brno-v.pdf": "/200000224-1e7591e75b/Plak%C3%A1t%20MAP%20V-2.pdf",
 "jidelnicek-aktualni.pdf": "/200000226-118db118de/J%C3%8DDELN%C3%8D%C4%8CEK.PDF",
}

def cti(cesta):
    with open(os.path.join(ROOT, cesta), encoding="utf-8") as f:
        return f.read()

def data_uri(cesta, mime="image/svg+xml"):
    with open(os.path.join(ROOT, cesta), "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

def inline_obrazky(html):
    """Nahradí src="assets/img/..." data-URI, aby náhled fungoval bez souborů okolo."""
    def obr(m):
        cesta = m.group(1)
        mime = "image/jpeg" if cesta.lower().endswith((".jpg", ".jpeg")) else "image/svg+xml"
        try:
            return f'src="{data_uri(cesta, mime)}"'
        except FileNotFoundError:
            return m.group(0)
    return re.sub(r'src="(assets/img/[^"]+)"', obr, html)

def prelozit_odkazy(html, slug):
    """href na stránky → hash router, href na dokumenty → CDN."""
    def odkaz(m):
        h = m.group(1)
        if h.startswith("#"):                       # kotva uvnitř stránky
            return f'href="#{slug}/{h[1:]}"'
        if h.startswith("assets/dokumenty/"):
            soubor = h.split("/")[-1]
            if soubor in DOKUMENTY:      # leží na CDN starého webu → v náhledu funguje
                return f'href="{CDN}{DOKUMENTY[soubor]}?ph=7fd136a065" target="_blank" rel="noopener"'
            # nové dokumenty zatím nikde online nejsou – odkaz se v náhledu nedá otevřít
            return ('data-bez-souboru="1" title="Soubor bude ke stažení až po nasazení '
                    'webu na doménu školky"')
        for soubor, s in SLUG.items():
            if h == soubor:
                return f'href="#{s}"'
            if h.startswith(soubor + "#"):
                return f'href="#{s}/{h.split("#",1)[1]}"'
        return m.group(0)
    return re.sub(r'href="([^"]+)"', odkaz, html)

def main():
    os.makedirs(OUT, exist_ok=True)
    index = cti("index.html")

    # --- CSS s inlinovaným podkresem ---
    css = cti("assets/css/style.css")
    css = css.replace('url("../img/podkres.svg")', f'url("{data_uri("assets/img/podkres.svg")}")')

    # --- hlavička a patička (společné pro všechny stránky) ---
    hlavicka = re.search(r'(<a class="skip".*?</div>\s*)(?=<main)', index, re.S).group(1)
    paticka  = re.search(r'(<footer class="footer">.*?</footer>)', index, re.S).group(1)
    for cesta, soubor in [("assets/img/logo.svg", "logo"), ("assets/img/logo-inverzni.svg", "logo-inverzni")]:
        uri = data_uri(cesta)
        hlavicka = hlavicka.replace(f'src="{cesta}"', f'src="{uri}"')
        paticka  = paticka.replace(f'src="{cesta}"', f'src="{uri}"')
    hlavicka = prelozit_odkazy(hlavicka, "index")
    paticka  = prelozit_odkazy(paticka, "index")

    # --- těla jednotlivých stránek ---
    sekce = []
    for soubor, _ in STRANKY:
        s = cti(soubor)
        telo = re.search(r'<main id="obsah">(.*?)</main>', s, re.S).group(1)
        slug = SLUG[soubor]
        telo = prelozit_odkazy(telo, slug)
        telo = inline_obrazky(telo)
        # OSM iframe nelze v náhledu vložit → nahradí ho odkaz na mapu
        telo = re.sub(
            r'<div class="map">.*?</div>',
            '<a class="map map--odkaz" href="https://mapy.cz/zakladni?q=%C5%BDi%C5%BEkova%201989%2F57%20Brno"'
            ' target="_blank" rel="noopener"><span><strong>Žižkova 1989/57, 616 00 Brno-Žabovřesky</strong>'
            '<em>Otevřít mapu v novém okně</em></span></a>', telo, flags=re.S)
        skryto = "" if slug == "index" else " hidden"
        sekce.append(f'<section class="page" data-page="{slug}"{skryto}>{telo}</section>')

    js = cti("assets/js/main.js")
    js = re.sub(r'  /\* --- zvýraznění aktivní položky v podnavigaci.*?(?=  /\* --- rok v patičce)',
                '', js, flags=re.S)

    router = r'''
/* --- přepínání stránek v jednosouborovém náhledu --- */
(function () {
  "use strict";
  var stranky = Array.prototype.slice.call(document.querySelectorAll(".page"));
  var odkazy  = Array.prototype.slice.call(document.querySelectorAll('a[href^="#"]'));

  function zobraz(slug, kotva, plynule) {
    var cil = stranky.filter(function (s) { return s.dataset.page === slug; })[0] || stranky[0];
    stranky.forEach(function (s) { s.hidden = s !== cil; });

    document.querySelectorAll("[data-nav]").forEach(function (a) {
      if (a.dataset.nav === cil.dataset.page) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });

    var y = 0;
    if (kotva) {
      var el = cil.querySelector("#" + CSS.escape(kotva));
      if (el) y = el.getBoundingClientRect().top + window.scrollY - 104;
    }
    window.scrollTo({ top: Math.max(0, y), behavior: plynule ? "smooth" : "auto" });
    document.dispatchEvent(new CustomEvent("stranka:zmena"));
  }

  function zRouty(plynule) {
    var h = decodeURIComponent(location.hash.replace(/^#/, ""));
    var cast = h.split("/");
    zobraz(cast[0] || "index", cast[1], plynule);
  }

  odkazy.forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var nova = a.getAttribute("href");
      if (location.hash === nova) { zRouty(true); return; }
      location.hash = nova;
    });
  });

  window.addEventListener("hashchange", function () { zRouty(true); });

  /* zvýraznění aktivní položky v podnavigaci aktivní stránky */
  var tik = false;
  function oznacPodnav() {
    tik = false;
    var sub = document.querySelector(".page:not([hidden]) .subnav");
    if (!sub) return;
    var links = Array.prototype.slice.call(sub.querySelectorAll("a"));
    var y = window.scrollY + 170, akt = 0;
    links.forEach(function (a, i) {
      var id = a.getAttribute("href").split("/").pop();
      var el = document.getElementById(id);
      if (el && el.offsetTop <= y) akt = i;
    });
    links.forEach(function (a, i) { a.classList.toggle("is-active", i === akt); });
  }
  window.addEventListener("scroll", function () {
    if (!tik) { tik = true; window.requestAnimationFrame(oznacPodnav); }
  }, { passive: true });
  document.addEventListener("stranka:zmena", oznacPodnav);

  zRouty(false);
})();
'''

    # označení položek hlavní navigace pro zvýraznění aktivní stránky
    def oznac(m):
        return m.group(0).replace('<a class="nav__link" href="#', '<a class="nav__link" data-nav-tmp href="#')
    hlavicka = re.sub(r'<a class="nav__link" href="#[a-z\-]+"', 
                      lambda m: m.group(0).replace('href="#', 'data-nav="') .replace('"', '"', 1), hlavicka)
    hlavicka = re.sub(r'<a class="nav__link" data-nav="([a-z\-]+)"',
                      r'<a class="nav__link" data-nav="\1" href="#\1"', hlavicka)
    hlavicka = re.sub(r'\s+aria-current="page"', '', hlavicka)

    doplnkove_css = '''
/* --- pruh náhledu a náhrada mapy (jen v tomto souboru) --- */
.nahled-pruh{
  background:var(--mint-100);border-bottom:1px solid var(--mint-200);
  color:var(--euca-700);font-family:var(--font-display);font-size:.86rem;font-weight:500
}
.nahled-pruh__in{display:flex;flex-wrap:wrap;gap:.3em 1.4em;align-items:center;justify-content:space-between;padding-block:.65em}
.nahled-pruh b{color:var(--ink);font-weight:600}
.nahled-pruh span{color:var(--muted);font-weight:400;font-family:var(--font-body);font-size:.83rem}
.doc[data-bez-souboru]{opacity:.62;cursor:default}
.doc[data-bez-souboru]:hover{border-color:var(--line);background:#fff;transform:none}
.doc[data-bez-souboru] small::after{content:" · v náhledu nedostupné";color:var(--muted)}
.map--odkaz{
  display:grid;place-items:center;text-align:center;text-decoration:none;
  background:linear-gradient(150deg,var(--blue-100),var(--mint-100));padding:36px
}
.map--odkaz:hover{text-decoration:none;border-color:var(--blue-400)}
.map--odkaz strong{display:block;font-family:var(--font-display);font-size:1.08rem;color:var(--ink);margin-bottom:.4em}
.map--odkaz em{font-style:normal;font-size:.92rem;color:var(--blue-700)}
'''

    html = f'''<title>MŠ Žižkova, Brno</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@400;500;600;700&display=swap">
<style>
{css}
{doplnkove_css}
</style>

<div class="nahled-pruh"><div class="wrap nahled-pruh__in">
  <b>Náhled nového webu MŠ Žižkova</b>
  <span>Fotografie jsou zatím zástupné &middot; podkres nahradíme mozaikou dětských výkresů</span>
</div></div>

{hlavicka}
<main id="obsah">
{"".join(sekce)}
</main>
{paticka}

<script>
{js}
{router}
</script>
'''
    cesta = os.path.join(OUT, "ms-zizkova-nahled.html")
    with open(cesta, "w", encoding="utf-8") as f:
        f.write(html)
    print("Hotovo:", cesta, "–", round(len(html.encode()) / 1024), "kB")

if __name__ == "__main__":
    main()
