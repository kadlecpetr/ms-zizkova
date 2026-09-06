#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor webu MŠ Žižkova, Brno.

Spuštění:  python3 build.py
Výstup:    statické .html soubory v kořeni projektu.

Texty se upravují v tomto souboru (sekce OBSAH níže), společná hlavička
a patička jsou na jednom místě – změna se propíše do všech stránek.
"""
import os, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────
#  ZÁKLADNÍ ÚDAJE ŠKOLY
# ─────────────────────────────────────────────────────────────
SKOLA = dict(
    nazev      = "Mateřská škola, Brno, Žižkova 57, příspěvková organizace",
    kratky     = "MŠ Žižkova, Brno",
    ulice      = "Žižkova 1989/57",
    mesto      = "616 00 Brno-Žabovřesky",
    tel        = "770 696 365",
    tel_link   = "+420770696365",
    tel_stary  = "541 212 062",
    mail       = "reditelka@skolka-zizkova.cz",
    web        = "www.skolka-zizkova.cz",
    ico        = "70874794",
    ds         = "23nkntg",
    reditelka  = "Mgr. Dagmara Hanáková",
    vedouci_sj = "Kateřina Pálková",
    zrizovatel = "Statutární město Brno, městská část Brno-Žabovřesky",
    kapacita   = "71",
    tridy      = "3",
    provoz     = "6.30–16.30",
    lat        = "49.2084792",
    lon        = "16.5876275",
    gdpr_jmeno = "Bc. Jaroslav Kocián",
    gdpr_tel   = "725 654 319",
    gdpr_mail  = "gdpr@jkaccounting.cz",
)

# ─────────────────────────────────────────────────────────────
#  IKONY (inline SVG, 24×24, stroke = currentColor)
# ─────────────────────────────────────────────────────────────
_I = {
 "zapis":'<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="m9 14 2 2 4-4"/>',
 "slunce":'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
 "zvonek":'<path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
 "stit":'<path d="M12 3l7 3v6c0 4.4-3 7.6-7 9-4-1.4-7-4.6-7-9V6z"/><path d="m9 12 2 2 4-4"/>',
 "srdce":'<path d="M20.8 6.6a5 5 0 0 0-7.1 0L12 8.3l-1.7-1.7a5 5 0 1 0-7.1 7.1L12 21l8.8-8.8a5 5 0 0 0 0-7.1Z"/>',
 "jiskra":'<path d="m12 3 1.9 4.6L18.5 9.5l-4.6 1.9L12 16l-1.9-4.6L5.5 9.5l4.6-1.9z"/><path d="m18 15 .9 2.1L21 18l-2.1.9L18 21l-.9-2.1L15 18l2.1-.9z"/>',
 "zprava":'<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 "lide":'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/>',
 "hodiny":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "telefon":'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.4 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
 "mail":'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>',
 "pin":'<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 "dokument":'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>',
 "stahnout":'<path d="M12 3v12"/><path d="m7 12 5 5 5-5"/><path d="M5 21h14"/>',
 "jidlo":'<path d="M4 3v7a3 3 0 0 0 6 0V3"/><path d="M7 3v18"/><path d="M17 3c-1.7 1.5-2.5 3.5-2.5 6 0 1.5.8 2.5 2.5 2.5V21"/>',
 "mobil":'<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
 "sipka":'<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
 "strom":'<path d="M12 22v-6"/><path d="m12 2 6 8h-3l4 6H5l4-6H6z"/>',
 "nota":'<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
 "kostky":'<rect x="3" y="13" width="8" height="8" rx="1.5"/><rect x="13" y="13" width="8" height="8" rx="1.5"/><rect x="8" y="3" width="8" height="8" rx="1.5"/>',
 "kniha":'<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/>',
 "info":'<circle cx="12" cy="12" r="9"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
 "megafon":'<path d="m3 11 15-7v16L3 13Z"/><path d="M8 12v6a2 2 0 0 0 4 0v-3"/>',
 "kalendar":'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 11h18"/>',
 "list":'<path d="M11 20A7 7 0 0 1 4 13c0-6 7-9 16-9 0 9-4 16-9 16Z"/><path d="M4 21c3-6 6-9 11-12"/>',
 "lupa":'<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
 "fotak":'<path d="M3 8a2 2 0 0 1 2-2h2l1.5-2h7L17 6h2a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/><circle cx="12" cy="13" r="3.5"/>',
 "domek":'<path d="m3 10 9-7 9 7v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/><path d="M9 21v-7h6v7"/>',
 "check":'<path d="m5 13 4 4L19 7"/>',
 "voda":'<path d="M12 2.7C15.5 7 19 10.4 19 14a7 7 0 0 1-14 0c0-3.6 3.5-7 7-11.3Z"/>',
}
def ico(name, size=22, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>')

SIPKA = ico("sipka", 16, "btn__arrow")

# ─────────────────────────────────────────────────────────────
#  NAVIGACE
# ─────────────────────────────────────────────────────────────
NAV = [
 ("Domů", "index.html", []),
 ("Škola", "skola.html", [
    ("Kdo jsme", "skola.html#kdo-jsme"),
    ("Aplikace Naše MŠ", "skola.html#nase-ms"),
    ("Vybavení školy", "skola.html#vybaveni"),
    ("Školní zahrada", "skola.html#zahrada"),
    ("Náš tým", "skola.html#tym"),
    ("Provoz školy", "skola.html#provoz"),
    ("Fotogalerie", "fotogalerie.html"),
 ]),
 ("Vzdělávání", "vzdelavani.html", [
    ("Školní vzdělávací program", "vzdelavani.html#svp"),
    ("Zaměření školy", "vzdelavani.html#zamereni"),
    ("Jak učíme", "vzdelavani.html#jak-ucime"),
    ("Předškolní příprava", "vzdelavani.html#predskolaci"),
    ("Projekty a spolupráce", "projekty.html"),
 ]),
 ("Pro rodiče", "pro-rodice.html", [
    ("Informace pro nové rodiče", "pro-rodice.html#novi-rodice"),
    ("Dokumenty ke stažení", "pro-rodice.html#dokumenty"),
    ("Stravování", "pro-rodice.html#stravovani"),
    ("Zápis do MŠ", "zapis.html"),
    ("Provoz o prázdninách", "pro-rodice.html#prazdniny"),
    ("Nadstandardní aktivity", "pro-rodice.html#aktivity"),
 ]),
 ("Aktuality", "aktuality.html", [
    ("Důležité informace", "aktuality.html#dulezite"),
    ("Novinky a akce", "aktuality.html#novinky"),
 ]),
 ("Kontakty", "kontakty.html", [
    ("Kontaktní údaje", "kontakty.html#udaje"),
    ("Jak se k nám dostanete", "kontakty.html#doprava"),
    ("Povinně zveřejňované informace", "kontakty.html#povinne"),
 ]),
]

def header(active):
    items = []
    for label, href, subs in NAV:
        cur = ' aria-current="page"' if href == active else ""
        if subs:
            panel = "".join(f'<a href="{h}">{t}</a>' for t, h in subs)
            caret = ('<svg class="nav__caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" '
                     'stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="m2 4.5 4 4 4-4"/></svg>')
            items.append(f'<div class="nav__item"><a class="nav__link" href="{href}"{cur}>{label}{caret}</a>'
                         f'<div class="nav__panel">{panel}</div></div>')
        else:
            items.append(f'<div class="nav__item"><a class="nav__link" href="{href}"{cur}>{label}</a></div>')
    nav = "".join(items)

    mob = []
    for label, href, subs in NAV:
        sub = "".join(f'<a href="{h}">{t}</a>' for t, h in subs)
        sub = f'<div class="mobile__sub">{sub}</div>' if sub else ""
        mob.append(f'<div class="mobile__group"><a href="{href}">{label}</a>{sub}</div>')
    mobile = "".join(mob)

    return f'''<a class="skip" href="#obsah">Přeskočit na obsah</a>
<div class="topbar"><div class="wrap topbar__in">
  <div class="topbar__set">
    <span class="topbar__item">{ico("pin",14)} {SKOLA["ulice"]}, {SKOLA["mesto"]}</span>
    <span class="topbar__item">{ico("hodiny",14)} Provoz {SKOLA["provoz"]}</span>
  </div>
  <div class="topbar__set">
    <a class="topbar__item" href="tel:{SKOLA["tel_link"]}">{ico("telefon",14)} {SKOLA["tel"]}</a>
    <a class="topbar__item" href="mailto:{SKOLA["mail"]}">{ico("mail",14)} {SKOLA["mail"]}</a>
  </div>
</div></div>

<header class="header"><div class="wrap header__in">
  <a class="logo" href="index.html"><img src="assets/img/logo.svg" width="236" height="64" alt="{SKOLA["kratky"]}"></a>
  <nav class="nav" aria-label="Hlavní navigace">{nav}</nav>
  <a class="btn btn--primary btn--sm header__cta" href="zapis.html">{ico("zapis",16)} Zápis do MŠ</a>
  <button class="burger" type="button" aria-label="Otevřít menu" aria-expanded="false" data-menu-open><span></span></button>
</div></header>

<div class="mobile" id="mobilni-menu" hidden>
  <div class="wrap" style="padding:0">
    <div class="mobile__top">
      <a class="logo" href="index.html"><img src="assets/img/logo.svg" width="236" height="64" alt="{SKOLA["kratky"]}"></a>
      <button class="mobile__close" type="button" aria-label="Zavřít menu" data-menu-close>&times;</button>
    </div>
    {mobile}
    <div class="mobile__cta">
      <a class="btn btn--primary" href="zapis.html">{ico("zapis",16)} Zápis do MŠ</a>
      <a class="btn btn--ghost" href="tel:{SKOLA["tel_link"]}">{ico("telefon",16)} {SKOLA["tel"]}</a>
    </div>
  </div>
</div>'''

def footer():
    return f'''<footer class="footer"><div class="wrap">
  <div class="footer__grid">
    <div>
      <div class="footer__logo"><img src="assets/img/logo-inverzni.svg" width="236" height="64" alt="{SKOLA["kratky"]}"></div>
      <p class="footer__note">{SKOLA["nazev"]}<br>
      Zřizovatel: {SKOLA["zrizovatel"]}<br>
      IČ: {SKOLA["ico"]} &middot; datová schránka: {SKOLA["ds"]}</p>
    </div>
    <div>
      <h4>Kontakt</h4>
      <ul class="footer__list">
        <li>{SKOLA["ulice"]}<br>{SKOLA["mesto"]}</li>
        <li><a href="tel:{SKOLA["tel_link"]}">{SKOLA["tel"]}</a></li>
        <li><a href="mailto:{SKOLA["mail"]}">{SKOLA["mail"]}</a></li>
        <li>{SKOLA["reditelka"]}<br><span style="opacity:.7">ředitelka školy</span></li>
      </ul>
    </div>
    <div>
      <h4>Rychlé odkazy</h4>
      <ul class="footer__list">
        <li><a href="zapis.html">Zápis do MŠ</a></li>
        <li><a href="pro-rodice.html#prazdniny">Provoz o prázdninách</a></li>
        <li><a href="pro-rodice.html#dokumenty">Dokumenty ke stažení</a></li>
        <li><a href="pro-rodice.html#stravovani">Jídelníček a stravování</a></li>
        <li><a href="aktuality.html">Aktuality</a></li>
        <li><a href="fotogalerie.html">Fotogalerie</a></li>
      </ul>
    </div>
    <div>
      <h4>Povinné informace</h4>
      <ul class="footer__list">
        <li><a href="assets/dokumenty/gdpr-informacni-memorandum.pdf">Informační memorandum GDPR</a></li>
        <li><a href="assets/dokumenty/vyrocni-zprava-2025.doc">Výroční zpráva</a></li>
        <li><a href="assets/dokumenty/zrizovaci-listina.pdf">Zřizovací listina</a></li>
        <li><a href="assets/dokumenty/rozpocet-2026.docx">Rozpočet a střednědobý výhled</a></li>
        <li><a href="kontakty.html#povinne">Vše na jednom místě</a></li>
      </ul>
    </div>
  </div>
  <div class="footer__bottom">
    <span>&copy; <span data-rok>2026</span> {SKOLA["nazev"]}</span>
    <span>Pověřenec pro ochranu osobních údajů: {SKOLA["gdpr_jmeno"]}, <a href="mailto:{SKOLA["gdpr_mail"]}">{SKOLA["gdpr_mail"]}</a></span>
  </div>
</div></footer>'''

JSONLD = f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Preschool",
"name":"{SKOLA["nazev"]}","alternateName":"{SKOLA["kratky"]}",
"url":"https://{SKOLA["web"]}/","telephone":"+420 770 696 365","email":"{SKOLA["mail"]}",
"address":{{"@type":"PostalAddress","streetAddress":"{SKOLA["ulice"]}","addressLocality":"Brno-Žabovřesky","postalCode":"616 00","addressCountry":"CZ"}},
"geo":{{"@type":"GeoCoordinates","latitude":{SKOLA["lat"]},"longitude":{SKOLA["lon"]}}},
"openingHours":"Mo-Fr 06:30-16:30"}}
</script>'''

def page(slug, title, description, body, active, jsonld=False):
    html = f'''<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#4A72AC">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:locale" content="cs_CZ">
<meta property="og:image" content="https://{SKOLA["web"]}/assets/img/foto/budova.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:site_name" content="{SKOLA["kratky"]}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/znacka.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
{JSONLD if jsonld else ""}
</head>
<body>
{header(active)}
<main id="obsah">
{body}
</main>
{footer()}
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
        f.write(html)
    return slug

# ─────────────────────────────────────────────────────────────
#  STAVEBNÍ PRVKY
# ─────────────────────────────────────────────────────────────
def pagehead(nadpis, perex, drobecky):
    cr = ' <span aria-hidden="true">/</span> '.join(
        [f'<a href="{h}">{t}</a>' if h else f'<span>{t}</span>' for t, h in drobecky])
    return f'''<section class="pagehead"><div class="wrap pagehead__in">
  <nav class="crumbs" aria-label="Drobečková navigace">{cr}</nav>
  <h1>{nadpis}</h1>
  <p class="lead">{perex}</p>
</div></section>'''

def subnav(items):
    links = "".join(f'<a href="#{h}">{t}</a>' for t, h in items)
    return f'<nav class="subnav" aria-label="Obsah stránky"><div class="wrap subnav__in">{links}</div></nav>'

def head(eyebrow, nadpis, perex="", center=False, level=2):
    c = " section-head--center" if center else ""
    p = f'<p class="lead">{perex}</p>' if perex else ""
    e = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    return f'<div class="section-head{c}">{e}<h{level}>{nadpis}</h{level}>{p}</div>'

def foto(soubor, alt, sirka, vyska, lazy=True):
    """Skutečná fotografie – nahrazuje zástupnou plochu ph()."""
    l = ' loading="lazy" decoding="async"' if lazy else ""
    return (f'<img src="assets/img/foto/{soubor}" width="{sirka}" height="{vyska}" alt="{alt}"'
            f'{l} style="width:100%;height:100%;object-fit:cover;display:block">')

def ph(popis, aspect=None):
    st = f' style="aspect-ratio:{aspect}"' if aspect else ""
    return f'<div class="ph"{st}><span>{popis}</span></div>'

def ticks(items, blue=False):
    cls = "ticks ticks--blue" if blue else "ticks"
    return f'<ul class="{cls}">' + "".join(f'<li>{i}</li>' for i in items) + '</ul>'

def cta(nadpis, text, tlacitko, href):
    return f'''<section class="section section--tight"><div class="wrap"><div class="cta">
  <div><h2>{nadpis}</h2><p>{text}</p></div>
  <div><a class="btn" href="{href}">{tlacitko} {SIPKA}</a></div>
</div></div></section>'''


# ─────────────────────────────────────────────────────────────
#  DĚTSKÉ VÝKRESY
#  Fotky výkresů zpracovává podklady/uprav_vykresy.py.
#  Popisky doplní školka – jména dětí jsou vidět přímo v kresbách.
# ─────────────────────────────────────────────────────────────
VYKRESY = [
 ("01", "Naše školka", "kresba pastelkou"),
 ("02", "Naše školka",  "kresba pastelkou"),
 ("03", "Naše školka",  "kresba pastelkou"),
 ("04", "Naše školka",  "kresba pastelkou"),
 ("05", "Naše děti",    "společná kresba třídy"),
 ("06", "Naše školka",  "kresba pastelkou"),
 ("07", "Naše školka",  "kresba pastelkou"),
 ("08", "Naše školka",  "kresba pastelkou"),
 ("09", "Naše školka",  "kresba pastelkou"),
 ("10", "Naše školka",  "kresba pastelkou"),
 ("11", "Naše školka",  "kresba pastelkou"),
 ("12", "Naše školka",  "kresba pastelkou"),
 ("13", "Naše školka",  "kresba pastelkou"),
 ("14", "Naše školka",  "kresba pastelkou"),
]

def vykres(cislo, nazev, popis, lazy=True):
    l = ' loading="lazy" decoding="async"' if lazy else ""
    return f'''<figure class="vykres">
  <img src="assets/img/vykresy/vykres-{cislo}-nahled.jpg" width="640" height="480"
       alt="Dětská kresba – {nazev}"{l}>
  <figcaption>„{nazev}“<span>{popis}</span></figcaption>
</figure>'''

def vykresy_mrizka(vyber=None):
    polozky = VYKRESY if vyber is None else [v for v in VYKRESY if v[0] in vyber]
    return '<div class="vykresy">' + "".join(vykres(*v) for v in polozky) + '</div>'

def vykres_pas(cislo, nazev, poznamka):
    return f'''<figure class="vykres-pas">
  <img src="assets/img/vykresy/vykres-{cislo}.jpg" width="1400" height="613"
       alt="Dětská kresba – {nazev}" loading="lazy" decoding="async">
  <figcaption><span>„{nazev}“ – kresba dětí z naší školky</span><span>{poznamka}</span></figcaption>
</figure>'''

# ═════════════════════════════════════════════════════════════
#  OBSAH – ÚVODNÍ STRÁNKA
# ═════════════════════════════════════════════════════════════
PILIRE = [
 ("blue", "kostky", "Polytechnika", "malí stavitelé a inženýři",
  "Děti objevují, jak věci fungují. Hravě zkoumají technické jevy, staví, experimentují a učí se přemýšlet v souvislostech.",
  ["konstrukční hry a stavebnicové projekty",
   "technické pokusy – voda, světlo, materiály",
   "práce s dřevěným ponkem a bezpečnými nástroji",
   "jednoduché stroje, magnety, světlo a stín",
   "spolupráce s FAST VUT"]),
 ("green", "list", "Ekologie", "malí badatelé a ochránci přírody",
  "Děti se učí, že i malé kroky mají velký dopad. Pozorují přírodu, pečují o zahradu a rozvíjejí ohleduplný vztah k prostředí.",
  ["zahradní laboratoř a pěstování rostlin",
   "ovocné a zeleninové záhonky, kompostování",
   "péče o hmyzí domečky",
   "pozorování přírody lupou a mikroskopem",
   "třídění odpadu a recyklace",
   "výpravy a projekty s Lipkou a Otevřenou zahradou"]),
 ("teal", "nota", "Umění", "malí hudebníci",
  "Hudba je u nás přirozenou součástí dne. Pomáhá dětem vyjadřovat emoce, rozvíjí rytmus, soustředění i tvořivost.",
  ["zpěv, rytmizace a hra na nástroje",
   "hudební improvizace",
   "propojení hudby s pohybem a příběhem",
   "zvuky přírody a hudební experimenty",
   "spolupráce se ZUŠ Veveří – Hudbík, projekty, koncerty"]),
]

def pilire_html(odkaz=True):
    out = []
    for barva, ikona, nazev, podtitul, popis, body in PILIRE:
        out.append(f'''<article class="pillar pillar--{barva}">
  <div class="pillar__top">
    <h3>{nazev}</h3>
    <span class="pillar__tag">{podtitul}</span>
    <p class="pillar__sub">{popis}</p>
  </div>
  <div class="pillar__body">{ticks(body)}</div>
</article>''')
    return '<div class="grid grid-3">' + "".join(out) + '</div>'

DUVODY = [
 ("stit",  "Bezpečné a laskavé prostředí",
  "Děti se u nás cítí jistě, vítaně a respektovaně. Podporujeme jejich tempo, potřeby i jedinečnost."),
 ("srdce", "Individuální přístup",
  "Každé dítě je pro nás důležité. Vnímáme jeho silné stránky, osobnost i způsob učení."),
 ("jiskra","Moderní vzdělávání",
  "Techniku, přírodu a hudbu propojujeme do jednoho celku. Děti se učí přirozeně – experimentem, hrou, tvořením a pozorováním."),
 ("zprava","Otevřená komunikace s rodiči",
  "Rodiče jsou naši partneři. Informace sdílíme srozumitelně, včas a s respektem."),
 ("lide",  "Spolupráce s odborníky a komunitou",
  "FAST VUT, ZUŠ Veveří, Lipka, Otevřená zahrada nebo divadlo Husa na provázku – děti získávají podněty z reálného světa."),
]

HODNOTY = [
 ("Respekt a bezpečí", "Každé dítě je u nás přijímané, vnímáme jeho tempo i potřeby. Respektující přístup je základem všech vztahů – mezi dětmi, pedagogy i rodiči."),
 ("Laskavá a odborná péče", "Děti vítají známé tváře, které je podporují, motivují a provázejí jejich růstem. Stabilní tým je základní pilíř bezpečí."),
 ("Otevřená a partnerská komunikace", "Rodiče jsou naši partneři. Sdílíme informace srozumitelně, včas a s ohledem na jejich potřeby."),
 ("Moderní a tvořivé vzdělávání", "Podporujeme zvídavost, kreativitu a radost z objevování. Polytechnické, ekologické a hudební projekty otevírají dětem svět praktických dovedností."),
 ("Samostatnost a zodpovědnost", "Děti vedeme k tomu, aby si věřily, spolupracovaly a přebíraly odpovědnost za své chování i rozhodnutí."),
 ("Přátelská atmosféra a spolupráce", "Vytváříme mateřskou školu, kde se dobře cítí děti, rodiče i pedagogové. Společná práce a dobré vztahy jsou pro nás klíčové."),
 ("Respekt k přírodě a okolnímu světu", "Učíme děti ekologickému myšlení, ohleduplnosti a aktivnímu vztahu k prostředí. Hudba a umění jim pomáhají vnímat svět citlivěji."),
]

def index_page():
    duvody = "".join(f'''<article class="card"><div class="card__icon">{ico(i)}</div>
    <h3>{t}</h3><p>{p}</p></article>''' for i, t, p in DUVODY)

    hodnoty = "".join(f'''<div class="value"><div class="value__num">{n+1}</div>
    <div><h4>{t}</h4><p>{p}</p></div></div>''' for n, (t, p) in enumerate(HODNOTY))

    body = f'''
<section class="hero"><div class="wrap hero__in">
  <div class="hero__copy">
    <span class="hero__motto">{ico("slunce",16)} Radostně objevujeme svět</span>
    <h1>Mateřská škola, kde děti <em>objevují, tvoří a rostou</em></h1>
    <p class="hero__text">Jsme moderní mateřská škola v srdci Žabovřesk. Nabízíme bezpečné prostředí,
      respektující přístup, kvalitní vzdělávání a úzkou spolupráci s rodinou.</p>
    <div class="hero__actions">
      <a class="btn btn--primary" href="zapis.html">{ico("zapis",17)} Zápis do MŠ</a>
      <a class="btn btn--ghost" href="skola.html">Poznejte naši školku {SIPKA}</a>
    </div>
    <a class="hero__link" href="assets/dokumenty/jidelnicek-aktualni.pdf" target="_blank" rel="noopener">
      <span class="hero__link-ico">{ico("jidlo",18)}</span>
      <span>
        <span class="hero__link-title">Jídelníček na tento týden {SIPKA}</span>
        <span class="hero__link-note">PDF &middot; aktualizujeme každý týden</span>
      </span>
    </a>
  </div>
  <div class="hero__media">
    <div class="hero__photo">{foto("budova-hero.jpg",
      "Budova mateřské školy Žižkova – vstup s balkonem", 960, 720, lazy=False)}</div>
    <div class="hero__badge">
      <div><b>{SKOLA["tridy"]}</b><span>třídy</span></div>
      <div><b>{SKOLA["kapacita"]}</b><span>dětí</span></div>
      <div><b>{SKOLA["provoz"]}</b><span>provozní doba</span></div>
    </div>
  </div>
</div></section>

<section class="quick"><div class="wrap"><div class="quick__grid">
  <a class="quick__card" href="zapis.html">
    <span class="quick__icon">{ico("zapis")}</span>
    <h3>Zápis do MŠ</h3>
    <p>Termíny, kritéria, potřebné dokumenty a postup krok za krokem.</p>
    <span class="quick__more">Vše o zápisu {SIPKA}</span></a>
  <a class="quick__card quick__card--green" href="pro-rodice.html#prazdniny">
    <span class="quick__icon">{ico("slunce")}</span>
    <h3>Provoz o prázdninách</h3>
    <p>Aktuální informace o prázdninovém provozu, náhradních školkách a přihláškách.</p>
    <span class="quick__more">Zobrazit informace {SIPKA}</span></a>
  <a class="quick__card quick__card--sand" href="aktuality.html">
    <span class="quick__icon">{ico("megafon")}</span>
    <h3>Aktuality</h3>
    <p>Důležitá oznámení, novinky ze tříd a přehled nadcházejících akcí.</p>
    <span class="quick__more">Co je u nás nového {SIPKA}</span></a>
</div></div></section>

<section class="section section--pattern">
  <div class="wrap">
    {head("Proč právě my", "Proč zvolit MŠ Žižkova", "Pět věcí, na kterých u nás stojí každý den.", center=True)}
    <div class="grid grid-3">{duvody}</div>
  </div>
</section>

<section class="section section--mint">
  <div class="wrap wrap--narrow center">
    <p class="eyebrow eyebrow--center" style="justify-content:center">Naše filozofie</p>
    <p style="font-family:var(--font-display);font-size:clamp(1.25rem,1.05rem + .9vw,1.72rem);line-height:1.45;color:var(--ink)">
      „Naším cílem je vytvářet bezpečné, podnětné a laskavé prostředí, kde děti mohou svobodně objevovat svět,
      rozvíjet své schopnosti a učit se hrou. Každé dítě vnímáme jako jedinečnou osobnost a provázíme ho
      s respektem, odborností a porozuměním.“</p>
    <p class="muted small" style="margin-top:1.4em">{SKOLA["reditelka"]}, ředitelka mateřské školy</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head("Zaměření", "Naše tři oblasti zaměření",
          "Polytechnika, ekologie a umění se u nás přirozeně propojují. Děti staví, zkoumají, zpívají, tvoří a pečují o přírodu.", center=True)}
    {pilire_html()}
    <div class="center" style="margin-top:34px">
      <a class="btn btn--ghost" href="vzdelavani.html#zamereni">Jak konkrétně učíme {SIPKA}</a>
    </div>
  </div>
</section>

<section class="section section--blue">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:start">
      <div>
        {head("Výjimečnost", "Co dělá naši školku výjimečnou")}
        <div class="stack">
          <div class="card card--green"><div class="card__icon">{ico("strom")}</div>
            <h3>Propojujeme techniku, přírodu a hudbu</h3>
            <p>Děti staví z přírodních materiálů, zkoumají technické jevy venku, tvoří hudební nástroje
               z přírodnin a objevují svět všemi smysly.</p></div>
          <div class="card"><div class="card__icon">{ico("lupa")}</div>
            <h3>Učení hrou, experimentem a zážitkem</h3>
            <p>Děti měří, porovnávají, zkoumají, tvoří, zpívají, pozorují a přemýšlejí. Učí se přirozeně –
               tak, jak je to pro předškolní věk nejlepší.</p></div>
          <div class="card card--teal"><div class="card__icon">{ico("lide")}</div>
            <h3>Projekty propojené s komunitou</h3>
            <p>FAST VUT, Lipka, Otevřená zahrada, ZUŠ Veveří, divadlo Husa na provázku i ZŠ Sirotkova –
               děti získávají zkušenosti z reálného světa.</p></div>
        </div>
      </div>
      <div>
        {head("Hodnoty", "Hodnoty, na kterých stojíme")}
        <div class="stack-sm" style="display:grid;gap:18px">{hodnoty}</div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head("Aktuality", "Co je u nás nového")}
    <div class="stack">
      <div class="alert">
        <span class="alert__ico">{ico("info",20)}</span>
        <div><h3>Provozní doba od 1. 9. 2026</h3>
        <p>Mateřská škola je v provozu každý všední den od 6.30 do 16.30 hodin.</p></div>
      </div>
      <div class="grid grid-3">
        <a class="post" href="aktuality.html#novinky">
          <span class="post__date">28. 8. 2026</span>
          <h3>Provoz MŠ od 1. 9. 2026</h3>
          <p>Od začátku školního roku je školka otevřená od 6.30 do 16.30 hodin.</p></a>
        <a class="post" href="aktuality.html#novinky">
          <span class="post__date">1. 9. 2026</span>
          <h3>Změna telefonního čísla</h3>
          <p>Nové telefonní číslo mateřské školy je {SKOLA["tel"]}.</p></a>
        <a class="post" href="pro-rodice.html#prazdniny">
          <span class="post__date">Prázdninový provoz</span>
          <h3>Provoz o prázdninách</h3>
          <p>Přehled prázdninového a náhradního provozu mateřských škol v Žabovřeskách.</p></a>
      </div>
    </div>
    <div class="center" style="margin-top:30px"><a class="btn btn--ghost" href="aktuality.html">Všechny aktuality {SIPKA}</a></div>
  </div>
</section>

<section class="section section--sand section--tight">
  <div class="wrap">
    {head("Praktické informace", "Nejčastěji hledáme", center=True)}
    <div class="grid grid-4">
      <a class="card card--plain" href="skola.html#provoz" style="text-decoration:none">
        <div class="card__icon">{ico("hodiny")}</div><h3>Provoz a režim dne</h3>
        <p class="small muted">Provozní doba {SKOLA["provoz"]}, organizace dne a adaptace nových dětí.</p></a>
      <a class="card card--plain card--green" href="pro-rodice.html#stravovani" style="text-decoration:none">
        <div class="card__icon">{ico("jidlo")}</div><h3>Stravování a jídelníček</h3>
        <p class="small muted">Vlastní kuchyně, čerstvé suroviny a celodenní pitný režim.</p></a>
      <a class="card card--plain card--teal" href="skola.html#nase-ms" style="text-decoration:none">
        <div class="card__icon">{ico("mobil")}</div><h3>Aplikace Naše MŠ</h3>
        <p class="small muted">Omluvenky, platby, přihlašování na akce a zprávy ze tříd na jednom místě.</p></a>
      <a class="card card--plain" href="pro-rodice.html#dokumenty" style="text-decoration:none">
        <div class="card__icon">{ico("dokument")}</div><h3>Dokumenty ke stažení</h3>
        <p class="small muted">Školní vzdělávací program, školní řád, řád školní jídelny a další.</p></a>
    </div>
  </div>
</section>

<section class="section section--mint" style="padding-block:clamp(48px,6vw,84px)">
  <div class="wrap">
    {head("Očima dětí", "Takhle naši školku vidí děti",
          "Žlutá budova, modrá okna a sluníčko nad ní. Výkresy, které vznikly ve třídách, "
          "jsou pro nás tou nejlepší vizitkou.", center=True)}
    {vykresy_mrizka(["01","04","05","08"])}
    <div class="center" style="margin-top:32px">
      <a class="btn btn--ghost" href="fotogalerie.html">Celá galerie výkresů {SIPKA}</a>
    </div>
  </div>
</section>

{cta("Přijďte se k nám podívat",
     "Zápis do mateřské školy probíhá každý rok na jaře. Najdete u nás termíny, kritéria i seznam dokumentů – a rádi vám odpovíme na cokoli dalšího.",
     "Vše o zápisu", "zapis.html")}
'''
    return page("index.html",
        f'{SKOLA["kratky"]} – mateřská škola, kde děti objevují, tvoří a rostou',
        "Moderní mateřská škola v Brně-Žabovřeskách. Bezpečné prostředí, respektující přístup, "
        "polytechnika, ekologie a hudba. Informace o zápisu, provozu i stravování.",
        body, "index.html", jsonld=True)

# ═════════════════════════════════════════════════════════════
#  ŠKOLA
# ═════════════════════════════════════════════════════════════
TYM = [
 ("#4A72AC", "Třída A – Zajíčci", [
    ("Jana Kociánová", "učitelka"),
    ("Romana Tomšejová", "učitelka"),
    ("Mgr. Martina Eliášová Babinská", "asistentka pedagoga"),
    ("Zuzana Illnerová", "provozní pracovnice")]),
 ("#6E9C87", "Třída B – Ježečci", [
    ("Olga Janková", "učitelka"),
    ("Lea Křivánková", "učitelka"),
    ("Veronika Struhařová", "asistentka pedagoga"),
    ("Zuzana Illnerová", "provozní pracovnice")]),
 ("#4E8E9B", "Třída C – Veverky", [
    ("Mgr. Dagmara Hanáková", "ředitelka školy, učitelka"),
    ("Hana Machatková", "učitelka"),
    ("Eliška Řeháčková", "asistentka pedagoga"),
    ("Mariia Oros", "provozní pracovnice")]),
]

REZIM = [
 ("6.30 – 8.30",  "Scházení dětí, spontánní hry a činnosti podle vlastní volby, individuální práce s dětmi"),
 ("8.30 – 9.00",  "Komunitní kruh, ranní cvičení a pohybové chvilky"),
 ("9.00 – 9.20",  "Dopolední svačina"),
 ("9.20 – 10.00", "Řízené činnosti, projekty, experimenty a tvoření"),
 ("10.00 – 11.45","Pobyt venku – školní zahrada, vycházky a výpravy do okolí"),
 ("11.45 – 12.30","Oběd, hygiena, příprava na odpočinek"),
 ("12.30 – 14.15","Odpočinek, čtení pohádky, klidové a individuální činnosti předškoláků"),
 ("14.15 – 14.45","Odpolední svačina"),
 ("14.45 – 16.30","Odpolední zájmové činnosti, pobyt na zahradě, vyzvedávání dětí"),
]

def skola_page():
    tym = "".join(f'''<div class="team__class">
  <h3><span class="team__dot" style="background:{barva}"></span>{nazev}</h3>
  <ul class="people">''' + "".join(f'<li><b>{j}</b><span>{r}</span></li>' for j, r in lide) + '</ul></div>'
  for barva, nazev, lide in TYM)

    rezim = "".join(f'<li><time>{t}</time><span>{p}</span></li>' for t, p in REZIM)

    body = pagehead("Naše škola",
        "Mateřská škola s rozlehlou zahradou v klidném prostředí rodinné zástavby v Brně-Žabovřeskách. "
        "Tři smíšené třídy, vlastní kuchyně a stabilní tým, který se o děti stará s respektem a laskavostí.",
        [("Domů","index.html"),("Škola",None)]) + subnav([
        ("Kdo jsme","kdo-jsme"),("Vybavení","vybaveni"),("Školní zahrada","zahrada"),
        ("Náš tým","tym"),("Provoz školy","provoz")]) + f'''

<section class="section" id="kdo-jsme">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center">
      <div>
        {head("Kdo jsme", "Školka v klidném srdci Žabovřesk")}
        <p>Mateřská škola se nachází v účelové budově v klidném prostředí rodinné zástavby a obklopuje ji
          rozlehlá školní zahrada. Součástí školy je vlastní školní kuchyně.</p>
        <p>Škola je trojtřídní – třídy <strong>Zajíčků, Ježečků a Veverek</strong> – a navštěvuje ji
          <strong>{SKOLA["kapacita"]} dětí</strong> ve věku od 3 do 6, případně 7 let. Třídy jsou smíšené,
          takže se děti přirozeně učí spolupracovat a pomáhat si napříč věkem.</p>
        <p>Zřizovatelem školy je <strong>{SKOLA["zrizovatel"]}</strong>. Díky vstřícnosti zřizovatele dochází
          každoročně k potřebným opravám a vylepšením budovy i zahrady.</p>
        <div class="tagrow" style="margin-top:1.4em">
          <span class="tag">{SKOLA["tridy"]} smíšené třídy</span>
          <span class="tag">Kapacita {SKOLA["kapacita"]} dětí</span>
          <span class="tag tag--green">Vlastní školní kuchyně</span>
          <span class="tag tag--green">Rozlehlá zahrada</span>
        </div>
      </div>
      <div style="border-radius:var(--r-xl);overflow:hidden;box-shadow:var(--shadow-md);aspect-ratio:16/10">
        {foto("budova.jpg", "Budova mateřské školy Žižkova a přilehlá zahrada", 1600, 720)}</div>
    </div>
  </div>
</section>

<section class="section section--tight" id="nase-ms">
  <div class="wrap">
    <div class="cta" style="background:linear-gradient(140deg,var(--euca-700),var(--euca-600) 60%,var(--teal-600))">
      <div>
        <p class="eyebrow" style="color:rgba(255,255,255,.85)">Aplikace Naše MŠ</p>
        <h2>Komunikace se školkou na jednom místě</h2>
        <p>Přes aplikaci <strong>Naše MŠ</strong> omlouváte děti, sledujete platby, přihlašujete se na akce
          a nadstandardní aktivity a dostáváte zprávy z třídy i z vedení školy. Doporučujeme mít ji nainstalovanou
          po celou dobu docházky dítěte – většinu agendy díky ní vyřídíte z mobilu během chvilky.</p>
      </div>
      <div><a class="btn" href="kontakty.html">{ico("info",16)} Potřebuji pomoct s přihlášením</a></div>
    </div>
  </div>
</section>

<section class="section section--blue section--pattern" id="vybaveni">
  <div class="wrap">
    {head("Vybavení školy", "Prostor, který dětem sedne")}
    <div class="grid grid-3">
      <article class="card"><div class="card__icon">{ico("domek")}</div>
        <h3>Herny, ložnice a šatny</h3>
        <p>Dětem jsou k dispozici tři samostatné herny, dvě ložnice, sociální zařízení a šatny.
           V hernách je vytvořeno několik hracích koutů – relaxační, kuchyňský nebo výtvarný.</p></article>
      <article class="card card--green"><div class="card__icon">{ico("jiskra")}</div>
        <h3>Sportovní vybavení</h3>
        <p>Nadstandardně jsme vybaveni pomůckami pro tělovýchovné a sportovní aktivity – akupresurní podložky,
           padák, švédská bedna a další nářadí i náčiní pro pravidelné cvičení dětí.</p></article>
      <article class="card card--teal"><div class="card__icon">{ico("stit")}</div>
        <h3>Bezpečnost</h3>
        <p>Všechny hračky a vybavení tříd splňují bezpečnostní požadavky. Vybavení hračkami, didaktickým
           materiálem a pomůckami průběžně doplňujeme a obnovujeme.</p></article>
    </div>
    <p class="small muted" style="margin-top:30px;margin-bottom:14px">
      Jak naši školku vidí děti ze tříd:</p>
    {vykresy_mrizka(["03","07","10"])}
  </div>
</section>

<section class="section" id="zahrada">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center">
      <div>{vykres("14", "Naše školka", "zahrada očima dětí", lazy=True)}</div>
      <div>
        {head("Školní zahrada", "Zahrada jako druhá třída")}
        <p>Rozlehlá školní zahrada je jedním z největších bohatství naší školky. Děti tu tráví každý den
          podstatnou část dopoledne i odpoledne – hrají si, zkoumají, pěstují a pozorují proměny přírody.</p>
        {ticks([
          "tři pískoviště a hrací prvek se skluzavkou",
          "mlhoviště pro horké dny",
          "hrací pryžový chodník",
          "bylinkové a zeleninové záhonky",
          "kompost a hmyzí domečky",
          "zázemí pro venkovní hry a tvoření",
        ])}
        <p style="margin-top:1.2em">Zahrada je zároveň hlavním prostorem pro environmentální výchovu –
          zahradní laboratoř, pozorování lupou a mikroskopem i eko-technické projekty.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--mint" id="tym">
  <div class="wrap">
    {head("Náš tým", "Lidé, kteří tu pro děti jsou",
      "Stabilní tým je základní pilíř bezpečí. Děti u nás vítají známé tváře, které je podporují, motivují a provázejí jejich růstem.")}
    <div class="team">{tym}</div>
    <div style="margin-top:clamp(22px,2.6vw,34px)">
      {vykres_pas("05", "Naše děti", "Třída si nakreslila sama sebe – i se jmény.")}
    </div>
    <div class="grid grid-2" style="margin-top:16px">
      <div class="card"><div class="card__icon">{ico("srdce")}</div>
        <h3>Školní asistentka</h3>
        <p>{SKOLA["vedouci_sj"]} – podpora dětí i pedagogů v běžném dni mateřské školy.</p></div>
      <div class="card card--green"><div class="card__icon">{ico("jidlo")}</div>
        <h3>Stravovací provoz</h3>
        <p><strong>{SKOLA["vedouci_sj"]}</strong> – vedoucí stravovacího provozu<br>
           Michaela Hašková a Gabriela Víšková – kuchařky</p></div>
    </div>
  </div>
</section>

<section class="section" id="provoz">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:start;gap:clamp(28px,4vw,56px)">
      <div>
        {head("Provoz školy", "Provozní doba a režim dne")}
        <div class="alert" style="margin-bottom:26px">
          <span class="alert__ico">{ico("hodiny",20)}</span>
          <div><h3>Provozní doba {SKOLA["provoz"]}</h3>
          <p>Mateřská škola je otevřená každý všední den. Děti prosím přiveďte nejpozději do 8.30 hodin.</p></div>
        </div>
        <h3>Adaptace nových dětí</h3>
        <p>Nástup do mateřské školy je velká změna – pro dítě i pro rodiče. Postupujeme individuálně,
          podle tempa každého dítěte, a rodičům dáváme jasnou oporu i konkrétní doporučení.</p>
        <p><a href="pro-rodice.html#adaptace">Jak zvládnout první týdny ve školce {SIPKA}</a></p>
      </div>
      <div class="card">
        <h3>Orientační režim dne</h3>
        <p class="small muted">Denní řád je pružný – umožňuje reagovat na potřeby dětí i na aktuální dění a počasí.</p>
        <ul class="daily">{rezim}</ul>
      </div>
    </div>
  </div>
</section>

{cta("Chcete se přijít podívat?",
     "Domluvte si s námi návštěvu nebo se zeptejte na cokoli, co vás zajímá. Rádi vám školku ukážeme.",
     "Kontaktovat školku", "kontakty.html")}
'''
    return page("skola.html", f'Naše škola – {SKOLA["kratky"]}',
        "Trojtřídní mateřská škola v Brně-Žabovřeskách: vybavení, rozlehlá školní zahrada, tým učitelek, "
        "provozní doba 6.30–16.30 a režim dne.",
        body, "skola.html")

# ═════════════════════════════════════════════════════════════
#  VZDĚLÁVÁNÍ
# ═════════════════════════════════════════════════════════════
PROPOJENI = [
 ("kostky", "Stavíme z přírodních materiálů", "Dřevo, šišky, kameny, klacíky – děti tvoří, zkoumají a učí se o přírodě."),
 ("voda",   "Technika v přírodě", "Pumpa, stín, voda, vítr – technické jevy venku, v reálném prostředí."),
 ("list",   "Eko-technické projekty", "Ptačí budky, hmyzí domečky, zavlažování zahrady."),
 ("lupa",   "Mini vědecké dny", "Den Země, Den recyklace, eko dny v Björnsonově sadu, New Generation VUT."),
 ("nota",   "Hudba v přírodě a technice", "Zvuky materiálů, rytmus přírodních jevů, hudební improvizace venku."),
]

ORGANIZACE = ["ZŠ Sirotkova", "ZUŠ Veveří", "FAST VUT", "Lipka", "Rozmarýnek", "Otevřená zahrada",
              "Divadlo Husa na provázku", "Divadelní studio „V“", "Kulturní dům Rubín",
              "Knihovna Jiřího Mahena – Žabovřesky", "Úřad městské části Brno-Žabovřesky",
              "Pedagogicko-psychologická poradna Brno", "Speciálně pedagogické centrum"]

def vzdelavani_page():
    propojeni = "".join(f'''<article class="card"><div class="card__icon">{ico(i)}</div>
      <h3>{t}</h3><p class="small muted">{p}</p></article>''' for i, t, p in PROPOJENI)

    body = pagehead("Vzdělávání",
        "Učíme podle školního vzdělávacího programu „Radostně objevujeme svět“. Techniku, přírodu a hudbu "
        "propojujeme do jednoho celku – tak, aby děti chápaly svět v jeho přirozených souvislostech.",
        [("Domů","index.html"),("Vzdělávání",None)]) + subnav([
        ("Školní vzdělávací program","svp"),("Zaměření školy","zamereni"),("Jak učíme","jak-ucime"),
        ("Předškolní příprava","predskolaci")]) + f'''

<section class="section" id="svp">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:start;gap:clamp(28px,4vw,56px)">
      <div>
        {head("Školní vzdělávací program", "„Radostně objevujeme svět“")}
        <p>Děti se vzdělávají podle školního vzdělávacího programu, který splňuje požadavky Rámcového
          vzdělávacího programu pro předškolní vzdělávání. Program zohledňuje přirozené potřeby dětí,
          vede k jejich všestrannému rozvoji a přispívá k vytvoření pohodového a inspirujícího prostředí.</p>
        <p>Umožňuje učitelkám využít poznatků o každém dítěti při individualizaci nabídky činností a přibližovat
          děti ke klíčovým kompetencím předškolního vzdělávání.</p>
        <p><a class="btn btn--ghost btn--sm" href="assets/dokumenty/skolni-vzdelavaci-program.docx">
          {ico("stahnout",16)} Stáhnout celý ŠVP</a></p>
      </div>
      <div class="card">
        <h3>Hlavní cíle a principy</h3>
        {ticks([
          "rozvíjet každé dítě podle jeho možností a tempa",
          "vytvářet bezpečné, podnětné a laskavé prostředí",
          "učit hrou, prožitkem a vlastní zkušeností",
          "vést děti k samostatnosti a zodpovědnosti",
          "budovat pozitivní vztah k přírodě a okolnímu světu",
          "spolupracovat s rodinou jako s rovnocenným partnerem",
        ])}
      </div>
    </div>
  </div>
</section>

<section class="section section--mint section--pattern" id="zamereni">
  <div class="wrap">
    {head("Zaměření školy", "Polytechnika &middot; ekologie &middot; umění",
      "Tři oblasti, které dětem otevírají svět v jeho přirozených souvislostech. "
      "Partneři: FAST VUT, ZUŠ Veveří, Lipka, Otevřená zahrada, divadlo Husa na provázku a ZŠ Sirotkova.", center=True)}
    {pilire_html()}
    <div style="margin-top:clamp(34px,4vw,54px)">
      {head("Unikátní koncept", "Propojení polytechniky, ekologie a umění", center=True)}
      <div class="grid grid-3">{propojeni}</div>
    </div>
    <div style="margin-top:26px">
      {vykresy_mrizka(["02","11","12"])}
    </div>
    <div class="card" style="margin-top:26px">
      <h3>Další oblasti, které u nás mají pevné místo</h3>
      <div class="grid grid-2" style="margin-top:14px">
        {ticks(["výtvarné a keramické tvoření","pohyb a zdravý životní styl","práce s knihou a čtenářská pregramotnost"], blue=True)}
        {ticks(["lidové tradice a práce s přírodními materiály","estetika školního prostředí","divadelní a hudební představení"], blue=True)}
      </div>
    </div>
  </div>
</section>

<section class="section" id="jak-ucime">
  <div class="wrap">
    {head("Jak učíme", "Učení, které dává dětem smysl")}
    <div class="grid grid-2">
      <div class="card"><div class="card__icon">{ico("jiskra")}</div>
        <h3>Hra jako hlavní nástroj učení</h3>
        <p>Spontánní hru maximálně využíváme – je pro předškolní věk nejpřirozenější cestou k poznání.
          Vyvážený poměr spontánních a řízených činností udržujeme po celý den.</p></div>
      <div class="card card--green"><div class="card__icon">{ico("lupa")}</div>
        <h3>Prožitkové učení</h3>
        <p>Děti měří, porovnávají, zkoumají, tvoří a přemýšlejí. Zkušenost si odnášejí z vlastní činnosti,
          ne z výkladu.</p></div>
      <div class="card card--teal"><div class="card__icon">{ico("lide")}</div>
        <h3>Týmová spolupráce dětí</h3>
        <p>Týmové a tandemové učení vede děti k naslouchání, domlouvání a společnému hledání řešení.</p></div>
      <div class="card"><div class="card__icon">{ico("srdce")}</div>
        <h3>Individualizace a respekt</h3>
        <p>Vnímáme silné stránky i tempo každého dítěte. Používáme popisný jazyk a respektující přístup –
          k dětem i mezi sebou.</p></div>
    </div>
  </div>
</section>

<section class="section section--blue" id="predskolaci">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:start;gap:clamp(28px,4vw,56px)">
      <div>
        {head("Předškolní příprava", "Připravujeme děti na školu bez stresu")}
        <p>Každé předškolní dítě má svůj šanon s individuální nabídkou úkolů podle diagnostikované potřeby,
          s vizuálním označením. Každý týden plní předškoláci tematicky zaměřený týdenní úkol – kdykoli
          během týdne, podle vlastního rozhodnutí.</p>
        {ticks([
          "individuální portfolia a formativní hodnocení",
          "dobrovolné úkoly a grafomotorické listy",
          "podpora vzájemné spolupráce a respektu",
          "úzká spolupráce se ZŠ Sirotkova a ZUŠ Veveří",
          "edukativně stimulační skupiny na základních školách v městské části",
        ], blue=True)}
      </div>
      <div class="card">
        <h3>„Funkce“ pro předškoláky</h3>
        <p class="small muted">Pro rozvoj samostatnosti, řešení problémů a schopnosti dokončit úkol mají
          předškoláci na určité období viditelně označené role:</p>
        <ul class="daily" style="margin-top:14px">
          <li><time>písař</time><span>kontrola psacího náčiní a kreslicího koutku</span></li>
          <li><time>meteorolog</time><span>sledování a zaznamenávání změn počasí</span></li>
          <li><time>číšník</time><span>kontrola a doplňování ubrousků na stolech</span></li>
          <li><time>lékař</time><span>kontrola umytých rukou</span></li>
          <li><time>kuchař</time><span>kontrola stavu dětské kuchyňky</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

{cta("Nejsme na to sami",
     "Dlouhodobé projekty, spolupráce s odborníky a s organizacemi v Žabovřeskách i v celém Brně – "
     "díky nim děti zažijí techniku, přírodu a umění v reálném světě.",
     "Projekty a spolupráce", "projekty.html")}
'''
    return page("vzdelavani.html", f'Vzdělávání – {SKOLA["kratky"]}',
        "Školní vzdělávací program „Radostně objevujeme svět“, zaměření na polytechniku, ekologii a hudbu, "
        "předškolní příprava a projekty MŠ Žižkova v Brně.",
        body, "vzdelavani.html")


# ═════════════════════════════════════════════════════════════
#  PROJEKTY A SPOLUPRÁCE  (sekce 4 dle návrhu struktury)
# ═════════════════════════════════════════════════════════════
def projekty_page():
    organizace = "".join(f'<span class="tag">{o}</span>' for o in ORGANIZACE)
    body = pagehead("Projekty a spolupráce",
        "Dlouhodobé projekty, spolupráce s odborníky a s organizacemi v Žabovřeskách i v celém Brně. "
        "Díky nim děti zažijí techniku, přírodu a umění v reálném světě.",
        [("Domů","index.html"),("Vzdělávání","vzdelavani.html"),("Projekty a spolupráce",None)]) + subnav([
        ("Dlouhodobé projekty","dlouhodobe"),("Spolupráce s odborníky","odbornici"),
        ("Spolupráce s organizacemi","organizace")]) + f'''
<section class="section" id="dlouhodobe">
  <div class="wrap">
    {head("Dlouhodobé projekty", "Projekty, které nás provázejí celý rok")}
    <div class="grid grid-2" style="align-items:start">
      <div class="card card--green"><div class="card__icon">{ico("list")}</div>
        <h3>Zapojení školy</h3>
        {ticks([
          "<strong>Mrkvička</strong> – síť jihomoravských škol se zájmem o ekologickou výchovu",
          "<strong>Recyklohraní aneb Ukliďme si svět</strong> – sběr vysloužilých baterií",
          "<strong>Se Sokolem do života</strong> – pohybová gramotnost dětí",
          "<strong>Celé Česko čte dětem</strong> – čtenářská pregramotnost a „čtecí babičky“",
          "<strong>Erasmus+</strong> – členství v konsorciu statutárního města Brna",
          "<strong>MAP Brno V</strong> – místní akční plán rozvoje vzdělávání",
        ])}</div>
      <div>{vykresy_mrizka(["06","13"])}
        <p class="small muted" style="margin-top:14px">
          <a href="assets/dokumenty/plakat-map-brno-v.pdf">{ico("dokument",15)} Plakát MAP Brno V (PDF)</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section section--blue" id="odbornici">
  <div class="wrap">
    {head("Spolupráce s odborníky", "Odborná péče nad rámec běžného dne")}
    <div class="grid grid-4">
      <article class="card"><div class="card__icon">{ico("stit")}</div>
        <h3>Fyzioterapeut</h3>
        <p class="small muted">Vyšetření dětí zaměřené na správné držení těla a pohybový vývoj.</p></article>
      <article class="card"><div class="card__icon">{ico("lupa")}</div>
        <h3>Screening zraku</h3>
        <p class="small muted">Vyšetření zraku ve spolupráci se zdravotnickým zařízením PrimaVizus.</p></article>
      <article class="card"><div class="card__icon">{ico("srdce")}</div>
        <h3>Dentální hygiena</h3>
        <p class="small muted">Studenti zubního lékařství LF MU seznamují děti s pravidly dentální hygieny.</p></article>
      <article class="card"><div class="card__icon">{ico("lide")}</div>
        <h3>Speciální pedagogové</h3>
        <p class="small muted">Spolupráce se speciálními pedagogy a výchovnými poradci podle potřeb dětí.</p></article>
    </div>
  </div>
</section>

<section class="section" id="organizace">
  <div class="wrap">
    {head("Spolupráce s organizacemi", "S kým se ve školním roce potkáváme",
      "Děti díky partnerům zažijí techniku, přírodu i umění v reálném světě.")}
    <div class="tagrow">{organizace}</div>
  </div>
</section>


{cta("Zajímá vás, jak u nás vypadá běžný den?",
     "Podívejte se na režim dne, vybavení školky a zahradu, kde děti tráví většinu dopoledne.",
     "Prohlédnout školku", "skola.html")}
'''
    return page("projekty.html", f'Projekty a spolupráce – {SKOLA["kratky"]}',
        "Dlouhodobé projekty MŠ Žižkova (Mrkvička, Recyklohraní, Se Sokolem do života, Celé Česko čte dětem), "
        "spolupráce s odborníky a s organizacemi v Brně.",
        body, "vzdelavani.html")

# ═════════════════════════════════════════════════════════════
#  PRO RODIČE
# ═════════════════════════════════════════════════════════════
DOKUMENTY = [
 ("Školní vzdělávací program", "„Radostně objevujeme svět“ · DOCX", "skolni-vzdelavaci-program.docx"),
 ("Školní řád", "platný od 1. 9. 2024 · DOCX", "skolni-rad.docx"),
 ("Dodatek ke školnímu řádu", "PDF", "dodatek-ke-skolnimu-radu.pdf"),
 ("Řád školní jídelny", "školní rok 2026/2027 · DOCX", "rad-skolni-jidelny-2026-2027.docx"),
 ("Úplata za předškolní vzdělávání", "školné 2026/2027 · PDF", "uplata-skolne-2026-2027.pdf"),
 ("Úplata za stravování", "stravné 2026/2027 · DOCX", "uplata-stravne-2026-2027.docx"),
 ("Potvrzení o zaplacení školného", "formulář · DOC", "potvrzeni-o-zaplaceni-skolneho.doc"),
 ("Spádové obvody mateřských škol", "PDF", "spadove-obvody-ms.pdf"),
 ("Dítě do MŠ jen když je zdravé", "doporučení pro rodiče · PDF", "dite-do-ms-jen-kdyz-je-zdrave.pdf"),
 ("Prázdninový provoz 2026", "přehled náhradních školek · XLSX", "prazdninovy-provoz-2026.xlsx"),
 ("Informační memorandum GDPR", "zpracování osobních údajů · PDF", "gdpr-informacni-memorandum.pdf"),
 ("Zřizovací listina", "PDF", "zrizovaci-listina.pdf"),
 ("Výroční zpráva za rok 2025", "podle zákona 106/1999 Sb. · DOC", "vyrocni-zprava-2025.doc"),
 ("Rozpočet 2026", "DOCX", "rozpocet-2026.docx"),
 ("Střednědobý výhled rozpočtu", "2026–2028 · PDF", "strednedoby-vyhled-rozpoctu-2026-2028.pdf"),
]

def docs_html(vyber=None):
    polozky = DOKUMENTY if vyber is None else [d for d in DOKUMENTY if d[2] in vyber]
    return '<div class="docs">' + "".join(
        f'''<a class="doc" href="assets/dokumenty/{soubor}">
        <span class="doc__ico">{ico("dokument",18)}</span>
        <span><b>{nazev}</b><small>{popis}</small></span></a>''' for nazev, popis, soubor in polozky) + '</div>'

def pro_rodice_page():
    body = pagehead("Pro rodiče",
        "Vše podstatné na jednom místě – co dítě do školky potřebuje, jak probíhá adaptace, "
        "dokumenty ke stažení, stravování, platby i prázdninový provoz.",
        [("Domů","index.html"),("Pro rodiče",None)]) + subnav([
        ("Informace pro nové rodiče","novi-rodice"),("Dokumenty ke stažení","dokumenty"),
        ("Stravování","stravovani"),("Zápis do MŠ","zapis"),
        ("Provoz o prázdninách","prazdniny"),("Nadstandardní aktivity","aktivity")]) + f'''

<section class="section" id="novi-rodice">
  <div class="wrap">
    {head("Noví rodiče", "Než dítě nastoupí do školky")}
    <div class="grid grid-2" style="align-items:start">
      <div class="card">
        <div class="card__icon">{ico("check")}</div>
        <h3>Co dítě potřebuje</h3>
        {ticks([
          "pohodlné oblečení do třídy a náhradní oblečení do skříňky",
          "oblečení a obuv na zahradu, které se může umazat",
          "bačkorky s pevnou patou (ne pantofle)",
          "pyžamo na odpočinek",
          "hygienické potřeby podle pokynů třídní učitelky",
          "vše prosím podepsané nebo označené značkou dítěte",
        ])}
      </div>
      <div class="card card--green">
        <div class="card__icon">{ico("kalendar")}</div>
        <h3>První dny v mateřské škole</h3>
        {ticks([
          "první dny doporučujeme kratší pobyt – jen na dopoledne",
          "délku pobytu prodlužujeme postupně, podle toho, jak se dítě cítí",
          "s třídní učitelkou se domluvíte na individuálním plánu adaptace",
          "dítě může mít s sebou plyšáka nebo drobnost z domova",
          "zavedený rituál při loučení dětem velmi pomáhá",
        ])}
      </div>
    </div>
  </div>
</section>

<section class="section section--mint section--pattern" id="adaptace">
  <div class="wrap">
    {head("Adaptace", "První týdny ve školce: jak ustát loučení")}
    <div class="grid grid-2" style="align-items:start">
      <div class="stack">
        <p class="lead">Nástup dítěte do mateřské školy bývá nezřídka těžší pro rodiče než pro dítě samotné.
          Děti velmi dobře vycítí skutečné emoce svých rodičů – rychle pochytí jejich váhání, nervozitu i stres.
          Proto je pro ně důležité vidět, že rodiče jsou klidní a jistí.</p>
        <details class="acc"><summary>Co konkrétně dělat</summary><div class="acc__body">
          <p>Působte klidně a uvolněně, když dítě přivádíte. Nepůsobte rozrušeně a neomlouvejte se dítěti,
            že „už musí“. Nejlepší je prezentovat celou věc věcně a samozřejmě:</p>
          <p><em>„Mám tě rád a rád s tebou trávím čas, ale teď je třeba jít do školky. Já s tebou do třídy
            nepůjdu, ale vrátím se pro tebe později.“</em></p>
          <p>Pokud má dítě velký strach, může pomoci, když mu necháte něco svého: „Tady máš můj šátek,
            můžeš mi ho pohlídat a vrátit mi ho, až tě zase vyzvednu.“</p>
        </div></details>
        <details class="acc"><summary>Čemu se naopak vyhnout</summary><div class="acc__body">
          <p>Neodkládejte odchod kvůli tomu, že dítě pláče. Nevyjednávejte s ním a neslibujte, že „mu to
            vynahradíte“. Pokud jste už řekli, že odcházíte, nezůstávejte a nevracejte se – dítě by bylo
            jen zmatenější a rozrušenější.</p>
          <p>Nenuťte dítě podávat ruku, zdravit nebo objímat učitelku, pokud to samo nechce. Rozhodně nás
            to neurazí – když pozdravíte vy, dítě vaše jednání časem rádo zkopíruje.</p>
        </div></details>
        <details class="acc"><summary>Vyhněte se „milosrdným lžím“</summary><div class="acc__body">
          <p>„Za minutku jsem zpátky“ nebo „budu sedět na chodbě“ dítěti krátkodobě uleví, ale nabourají
            důvěru. Mnohem užitečnější je naučit dítě, že se může spolehnout na to, co říkáte – i když by
            v tu chvíli raději slyšelo něco jiného. Stejně tak se nesnažte „odplížit“, když se dítě nedívá.</p>
          <p>Tím, že se rozloučíte, můžete sice vyvolat pláč, zároveň ale posilujete důvěru a jistotu dítěte
            a investujete do budoucna.</p>
        </div></details>
        <details class="acc"><summary>Zavedení rituálu</summary><div class="acc__body">
          <p>Mnoha dětem pomáhá jednoduchý rituál, který budete opakovat každý den – objetí a tři pusy
            na rozloučenou, plácnutí, zamávání z okna nebo cokoli jiného, co se dítěti líbí a do čeho se zapojí.</p>
        </div></details>
      </div>
      <div>{vykres("09", "Naše školka", "kresba pastelkou", lazy=True)}</div>
    </div>
  </div>
</section>

<section class="section section--blue" id="dokumenty">
  <div class="wrap">
    {head("Dokumenty", "Dokumenty ke stažení",
      "Školní vzdělávací program, školní řád, řády, formuláře a povinně zveřejňované informace.")}
    {docs_html()}
  </div>
</section>

<section class="section" id="platby">
  <div class="wrap">
    {head("Platby", "Školné a stravné")}
    <div class="grid grid-2">
      <div class="card"><div class="card__icon">{ico("dokument")}</div>
        <h3>Úplata za předškolní vzdělávání</h3>
        <p>Výši školného pro školní rok 2026/2027 stanovuje ředitelka školy. Aktuální částku a splatnost
          najdete v dokumentu níže a v aplikaci Naše MŠ.</p>
        {docs_html(["uplata-skolne-2026-2027.pdf","potvrzeni-o-zaplaceni-skolneho.doc"])}</div>
      <div class="card card--green"><div class="card__icon">{ico("jidlo")}</div>
        <h3>Úplata za stravování</h3>
        <p>Stravné se hradí podle věkové kategorie dítěte a rozsahu odebrané stravy. Podrobnosti najdete
          v řádu školní jídelny.</p>
        {docs_html(["uplata-stravne-2026-2027.docx","rad-skolni-jidelny-2026-2027.docx"])}</div>
    </div>
  </div>
</section>

<section class="section" id="stravovani">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:start;gap:clamp(28px,4vw,56px)">
      <div>
        {head("Stravování", "Vaříme si sami, ve vlastní kuchyni")}
        <p>Mateřská škola má vlastní kuchyni, zkušenou vedoucí stravovacího provozu a stabilní provozní personál.
          Řídíme se pravidly spotřebního koše a zásadami zdravé výživy.</p>
        {ticks([
          "vaříme z čerstvých surovin",
          "dodržujeme spotřební koš a zásady zdravého stravování",
          "podporujeme zdravé stravovací návyky dětí",
          "děti mají celodenní pitný režim neslazených nápojů",
          "jídelníček zveřejňujeme týden dopředu",
        ])}
        <div class="contact-card" style="margin-top:26px">
          <h3 style="margin-top:0">Kontakt na stravovací provoz</h3>
          <ul class="contact-list">
            <li><span class="ico">{ico("lide",17)}</span><div><b>Vedoucí stravovacího provozu</b>
              <span>{SKOLA["vedouci_sj"]}</span></div></li>
            <li><span class="ico">{ico("telefon",17)}</span><div><b>Telefon</b>
              <a href="tel:{SKOLA["tel_link"]}">{SKOLA["tel"]}</a></div></li>
            <li><span class="ico">{ico("mail",17)}</span><div><b>E-mail</b>
              <a href="mailto:{SKOLA["mail"]}">{SKOLA["mail"]}</a></div></li>
          </ul>
        </div>
      </div>
      <div class="card">
        <div class="card__icon">{ico("jidlo")}</div>
        <h3>Aktuální jídelníček</h3>
        <p class="small muted">Jídelníček na aktuální týden najdete na nástěnce v šatně a ke stažení zde.</p>
        <p style="margin-top:18px"><a class="btn btn--green btn--sm" href="assets/dokumenty/jidelnicek-aktualni.pdf">
          {ico("stahnout",16)} Stáhnout jídelníček</a></p>
        <hr style="border:0;border-top:1px solid var(--line);margin:26px 0">
        <h3>Řády a úplaty</h3>
        {docs_html(["rad-skolni-jidelny-2026-2027.docx","uplata-stravne-2026-2027.docx"])}
      </div>
    </div>
  </div>
</section>

<section class="section" id="zapis">
  <div class="wrap">
    {head("Zápis do MŠ", "Zápis do mateřské školy")}
    <div class="cta">
      <div>
        <h2 style="font-size:clamp(1.4rem,1.1rem + 1.1vw,1.9rem)">Termíny, kritéria a postup krok za krokem</h2>
        <p>Zápis probíhá každoročně na jaře, elektronicky přes portál zápisů města Brna.
          Na samostatné stránce najdete postup, seznam potřebných dokumentů i odpovědi
          na nejčastější dotazy rodičů.</p>
      </div>
      <div><a class="btn" href="zapis.html">{ico("zapis",16)} Vše o zápisu {SIPKA}</a></div>
    </div>
  </div>
</section>

<section class="section section--sand" id="prazdniny">
  <div class="wrap">
    {head("Prázdninový provoz", "Provoz o prázdninách")}
    <div class="grid grid-2" style="align-items:start">
      <div>
        <p>O hlavních prázdninách je provoz mateřských škol v městské části organizován tak, aby rodiče měli
          k dispozici náhradní školku i v období, kdy je naše MŠ uzavřená. Termíny uzavření i seznam
          náhradních mateřských škol zveřejňujeme vždy s dostatečným předstihem – na této stránce,
          na nástěnce a v aplikaci Naše MŠ.</p>
        {ticks([
          "termíny prázdninového provozu zveřejňujeme nejpozději v dubnu",
          "přihlášku podáváte na konkrétní náhradní mateřskou školu",
          "úplata za prázdninový provoz se hradí zvlášť",
          "kapacita náhradních školek je omezená – přihlaste se včas",
        ])}
      </div>
      <div class="card">
        <h3>Aktuální dokumenty</h3>
        {docs_html(["prazdninovy-provoz-2026.xlsx","spadove-obvody-ms.pdf"])}
        <p class="small muted" style="margin-top:16px">Máte-li k prázdninovému provozu jakýkoli dotaz,
          ozvěte se nám na <a href="tel:{SKOLA["tel_link"]}">{SKOLA["tel"]}</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--mint" id="aktivity">
  <div class="wrap">
    {head("Nadstandardní aktivity", "Kroužky nad rámec běžného dne",
      "Nadstandardní aktivity probíhají v průběhu školního roku. Přihlašování řešíme přes aplikaci Naše MŠ.")}
    <div class="grid grid-3">
      <article class="card"><div class="card__icon">{ico("voda")}</div>
        <h3>Plavání</h3>
        <p>Pravidelný plavecký kurz pro starší děti pod vedením zkušených instruktorů.</p></article>
      <article class="card card--green"><div class="card__icon">{ico("kostky")}</div>
        <h3>Keramika</h3>
        <p>Práce s keramickou hlínou navazuje na dlouholeté výtvarné zaměření naší školky.</p></article>
      <article class="card card--teal"><div class="card__icon">{ico("zprava")}</div>
        <h3>Logopedická péče</h3>
        <p>Podpora správné výslovnosti a rozvoje řeči ve spolupráci s odborníky.</p></article>
    </div>
    <div class="alert alert--green" style="margin-top:24px">
      <span class="alert__ico">{ico("mobil",20)}</span>
      <div><h3>Přihlašování přes aplikaci Naše MŠ</h3>
      <p>Aktuální nabídku aktivit, termíny i ceny najdete vždy v aplikaci. Tam se také závazně přihlásíte.</p></div>
    </div>
  </div>
</section>

{cta("Nenašli jste, co jste hledali?",
     "Napište nám nebo zavolejte. Rádi vám poradíme s čímkoli kolem docházky, plateb i adaptace.",
     "Přejít na kontakty", "kontakty.html")}
'''
    return page("pro-rodice.html", f'Pro rodiče – {SKOLA["kratky"]}',
        "Informace pro rodiče: adaptace, co dítě potřebuje, dokumenty ke stažení, stravování a jídelníček, "
        "kroužky, platby a prázdninový provoz.",
        body, "pro-rodice.html")

# ═════════════════════════════════════════════════════════════
#  ZÁPIS
# ═════════════════════════════════════════════════════════════
def zapis_page():
    kroky = [
      ("Ověřte si spádovost", "Podle místa trvalého pobytu dítěte zjistíte, do jakého spádového obvodu patříte. "
       "Přihlásit se můžete i do nespádové školky – spádovost je ale jedním z kritérií přijetí."),
      ("Vygenerujte si přihlášku", "Elektronickou přihlášku vyplníte na portálu zápisů do mateřských škol "
       "města Brna. Systém vám vygeneruje přihlášku s unikátním číslem."),
      ("Nechte potvrdit očkování", "Přihlášku si nechte potvrdit dětským lékařem. Potvrzení nepotřebují děti, "
       "pro které je předškolní vzdělávání povinné (děti, které do 31. 8. dovrší 5 let)."),
      ("Podejte přihlášku", "Vyplněnou a potvrzenou přihlášku doručíte do mateřské školy ve stanoveném termínu – "
       "osobně, poštou, datovou schránkou nebo e-mailem s uznávaným elektronickým podpisem."),
      ("Sledujte výsledky", "Rozhodnutí o přijetí zveřejníme pod registračním číslem na webu a na vývěsce školy. "
       "Zákonní zástupci nepřijatých dětí obdrží rozhodnutí písemně."),
    ]
    kroky_html = "".join(f'''<div class="value"><div class="value__num">{n+1}</div>
      <div><h4>{t}</h4><p>{p}</p></div></div>''' for n, (t, p) in enumerate(kroky))

    body = pagehead("Zápis do mateřské školy",
        "Zápis do naší mateřské školy probíhá každoročně na jaře, elektronicky přes portál zápisů města Brna. "
        "Níže najdete postup krok za krokem, kritéria i potřebné dokumenty.",
        [("Domů","index.html"),("Zápis do MŠ",None)]) + f'''

<section class="section section--tight">
  <div class="wrap">
    <div class="alert">
      <span class="alert__ico">{ico("kalendar",20)}</span>
      <div><h3>Termín zápisu na školní rok 2027/2028</h3>
      <p>Přesné termíny stanovuje zřizovatel – zveřejníme je zde a v aplikaci Naše MŠ nejpozději v průběhu
        března. Zápisy do brněnských mateřských škol probíhají tradičně v první polovině května.</p></div>
    </div>
  </div>
</section>

<section class="section section--pattern" style="padding-top:0">
  <div class="wrap">
    {head("Postup", "Zápis krok za krokem")}
    <div class="grid grid-2" style="align-items:start;gap:clamp(28px,4vw,52px)">
      <div style="display:grid;gap:22px">{kroky_html}</div>
      <div class="card">
        <div class="card__icon">{ico("dokument")}</div>
        <h3>Co budete potřebovat</h3>
        {ticks([
          "vyplněnou přihlášku z portálu zápisů",
          "rodný list dítěte",
          "průkaz totožnosti zákonného zástupce",
          "doklad o trvalém pobytu dítěte (pokud se liší od pobytu zákonného zástupce)",
          "potvrzení dětského lékaře o očkování",
        ])}
        <hr style="border:0;border-top:1px solid var(--line);margin:24px 0">
        <h3>Dokumenty ke stažení</h3>
        {docs_html(["spadove-obvody-ms.pdf","skolni-rad.docx","uplata-skolne-2026-2027.pdf"])}
      </div>
    </div>
  </div>
</section>

<section class="section section--blue">
  <div class="wrap">
    {head("Kritéria", "Podle čeho přijímáme děti")}
    <div class="grid grid-2">
      <div class="card">
        <h3>Kritéria pro přijetí</h3>
        <p class="small muted">Kritéria vycházejí ze školského zákona a z pravidel stanovených zřizovatelem.
          Aktuální znění pro daný školní rok zveřejňujeme spolu s termínem zápisu.</p>
        {ticks([
          "děti, pro které je předškolní vzdělávání povinné (dovrší 5 let do 31. 8.)",
          "věk dítěte – přednost mají starší děti",
          "trvalý pobyt dítěte ve spádovém obvodu mateřské školy",
          "sourozenec, který již mateřskou školu navštěvuje",
        ], blue=True)}
      </div>
      <div class="card card--green">
        <h3>Přijímáme děti od 3 let</h3>
        <p>Naši mateřskou školu navštěvuje {SKOLA["kapacita"]} dětí ve věku od 3 do 6, případně 7 let,
          ve třech smíšených třídách.</p>
        <p>Nabízíme celodenní provoz {SKOLA["provoz"]}, vlastní školní kuchyni, rozlehlou zahradu a vzdělávání
          zaměřené na polytechniku, ekologii a hudbu.</p>
        <p style="margin-top:18px"><a class="btn btn--ghost btn--sm" href="skola.html">Prohlédnout školku {SIPKA}</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow">
    {head("Časté dotazy", "Na co se rodiče nejčastěji ptají", center=True)}
    <details class="acc"><summary>Musí dítě umět na nočník?</summary><div class="acc__body">
      Ano, děti by měly být při nástupu do mateřské školy bez plen a zvládat základní hygienické návyky.
      Drobné nehody se ale stávají a nikdo z nich nedělá vědu – proto vždy prosíme o náhradní oblečení.
    </div></details>
    <details class="acc"><summary>Můžeme přijít na návštěvu ještě před zápisem?</summary><div class="acc__body">
      Ano. Termín návštěvy si domluvte telefonicky na <a href="tel:{SKOLA["tel_link"]}">{SKOLA["tel"]}</a>
      nebo e-mailem na <a href="mailto:{SKOLA["mail"]}">{SKOLA["mail"]}</a>.
    </div></details>
    <details class="acc"><summary>Kdy se dozvíme výsledek?</summary><div class="acc__body">
      Seznam přijatých dětí zveřejňujeme pod registračními čísly na webu školy a na vývěsce, obvykle
      do 30 dnů od podání přihlášky. Rozhodnutí o nepřijetí zasíláme písemně.
    </div></details>
    <details class="acc"><summary>Co když dítě nepřijmete?</summary><div class="acc__body">
      Přihlášku podáváte v elektronickém systému města Brna, který pracuje i s dalšími mateřskými školami,
      které jste uvedli. Pokud nevyjde ani jedna, ozvěte se nám – poradíme, jak dál.
    </div></details>
    <details class="acc"><summary>Je docházka od 5 let povinná?</summary><div class="acc__body">
      Ano. Pro děti, které do 31. 8. dovrší pěti let, je předškolní vzdělávání povinné v rozsahu
      4 souvislých hodin denně v pracovních dnech.
    </div></details>
  </div>
</section>

{cta("Máte k zápisu otázku?",
     "Ozvěte se nám telefonicky nebo e-mailem. Ráda vám vše vysvětlím a domluvíme si i osobní návštěvu školky.",
     "Kontaktovat ředitelku", "kontakty.html")}
'''
    return page("zapis.html", f'Zápis do MŠ – {SKOLA["kratky"]}',
        "Zápis do MŠ Žižkova v Brně-Žabovřeskách: termíny, kritéria, potřebné dokumenty a postup krok za krokem.",
        body, "zapis.html")

# ═════════════════════════════════════════════════════════════
#  AKTUALITY
# ═════════════════════════════════════════════════════════════
DULEZITE = [
 ("kalendar", False, "Zápis do MŠ na školní rok 2027/2028",
  "Termíny zveřejníme v průběhu března. Kompletní informace, kritéria a postup najdete na stránce "
  '<a href="zapis.html">Zápis do MŠ</a>.'),
 ("slunce", True, "Provoz o prázdninách",
  "Přehled prázdninového a náhradního provozu mateřských škol v městské části najdete v sekci "
  '<a href="pro-rodice.html#prazdniny">Provoz o prázdninách</a>.'),
 ("hodiny", False, "Provozní doba 6.30–16.30",
  "Od 1. 9. 2026 je mateřská škola v provozu každý všední den od 6.30 do 16.30 hodin."),
 ("telefon", True, "Nové telefonní číslo školy",
  f'Od 1. 9. 2026 nás zastihnete na čísle <a href="tel:{SKOLA["tel_link"]}"><strong>{SKOLA["tel"]}</strong></a>. '
  f'Původní číslo {SKOLA["tel_stary"]} již nepoužívejte.'),
]

NOVINKY = [
 ("1. 9. 2026", "Změna telefonního čísla mateřské školy",
  f"Od 1. 9. 2026 má škola nové telefonní číslo {SKOLA['tel']}. Prosíme rodiče, aby si číslo aktualizovali "
  "v kontaktech i v aplikaci Naše MŠ."),
 ("28. 8. 2026", "Provoz MŠ od 1. 9. 2026",
  "Provoz mateřské školy je od 1. 9. 2026 stanoven na 6.30–16.30 hodin. Děti prosím přiveďte "
  "nejpozději do 8.30 hodin."),
 ("Průběžně", "Prázdninový provoz 2026",
  "Přehled náhradního provozu mateřských škol v Žabovřeskách o hlavních prázdninách je ke stažení "
  "v sekci pro rodiče."),
]

def aktuality_page():
    dulezite = "".join(f'''<div class="alert{' alert--green' if g else ''}">
      <span class="alert__ico">{ico(i,20)}</span>
      <div><h3>{t}</h3><p>{p}</p></div></div>''' for i, g, t, p in DULEZITE)
    novinky = "".join(f'''<article class="post">
      <span class="post__date">{d}</span><h3>{t}</h3><p>{p}</p></article>''' for d, t, p in NOVINKY)

    body = pagehead("Aktuality",
        "Důležitá oznámení máme vždy nahoře, pod nimi najdete novinky a akce chronologicky. "
        "Vše podstatné posíláme zároveň do aplikace Naše MŠ.",
        [("Domů","index.html"),("Aktuality",None)]) + subnav([
        ("Důležité informace","dulezite"),("Novinky a akce","novinky")]) + f'''

<section class="section" id="dulezite">
  <div class="wrap">
    {head("Fixní informace", "Důležité informace")}
    <div class="stack">{dulezite}</div>
  </div>
</section>

<section class="section section--mint section--pattern" id="novinky">
  <div class="wrap">
    {head("Chronologicky", "Novinky a akce",
      "Výlety, divadla, dílny, focení a projekty – co se u nás děje.")}
    <div class="grid grid-3">{novinky}</div>
    <div class="alert" style="margin-top:30px">
      <span class="alert__ico">{ico("mobil",20)}</span>
      <div><h3>Podrobnosti k akcím najdete v aplikaci Naše MŠ</h3>
      <p>Přihlašování na akce, souhlasy i platby řešíme přes aplikaci. Na webu zveřejňujeme jen to nejdůležitější.</p></div>
    </div>
  </div>
</section>

{cta("Chcete mít přehled?",
     "Nejrychleji se k vám informace dostanou přes aplikaci Naše MŠ. Pokud s přihlášením potřebujete pomoct, ozvěte se nám.",
     "Kontaktovat školku", "kontakty.html")}
'''
    return page("aktuality.html", f'Aktuality – {SKOLA["kratky"]}',
        "Důležitá oznámení, novinky a akce MŠ Žižkova v Brně-Žabovřeskách.",
        body, "aktuality.html")

# ═════════════════════════════════════════════════════════════
#  FOTOGALERIE
# ═════════════════════════════════════════════════════════════
def fotogalerie_page():
    body = pagehead("Fotogalerie",
        "Nejdřív to nejcennější – jak naši školku nakreslily samy děti. Fotografie budovy "
        "a zahrady doplňujeme postupně, po profesionálním focení.",
        [("Domů","index.html"),("Fotogalerie",None)]) + f'''
<section class="section">
  <div class="wrap">
    {head("Očima dětí", "Naše školka na dětských výkresech",
          "Kresby vznikly ve třídách Zajíčků, Ježečků a Veverek. Skoro každé dítě si vybralo "
          "stejný motiv – žlutou budovu se spoustou oken.")}
    {vykresy_mrizka()}
  </div>
</section>

<section class="section section--blue">
  <div class="wrap">
    {head("Fotografie", "Budova a zahrada")}
    <div class="grid grid-2" style="align-items:center;gap:clamp(24px,3vw,40px)">
      <figure style="margin:0;border-radius:var(--r-xl);overflow:hidden;box-shadow:var(--shadow-md);aspect-ratio:4/3">
        {foto("budova-hero.jpg", "Budova mateřské školy Žižkova – vstup s balkonem", 960, 720)}</figure>
      <div class="card">
        <div class="card__icon">{ico("fotak")}</div>
        <h3>Fotogalerii postupně doplňujeme</h3>
        <p>Připravujeme profesionální fotografie heren, školní zahrady, keramické dílny
          a dalších míst, kde děti tráví den. Fotografie dětí na webu záměrně nezveřejňujeme –
          ukazujeme prostředí, detaily a ruce při práci.</p>
        <p style="margin-top:16px"><a class="btn btn--ghost btn--sm" href="kontakty.html">
          Chcete se přijít podívat naživo? {SIPKA}</a></p>
      </div>
    </div>
  </div>
</section>
{cta("Nejlepší je vidět školku naživo",
     "Domluvte si návštěvu – ukážeme vám třídy, zahradu i to, jak u nás vypadá běžný den.",
     "Domluvit návštěvu", "kontakty.html")}
'''
    return page("fotogalerie.html", f'Fotogalerie – {SKOLA["kratky"]}',
        "Fotogalerie MŠ Žižkova v Brně: budova, třídy, vybavení a školní zahrada.",
        body, "fotogalerie.html")

# ═════════════════════════════════════════════════════════════
#  KONTAKTY
# ═════════════════════════════════════════════════════════════
def kontakty_page():
    lat, lon = SKOLA["lat"], SKOLA["lon"]
    bbox = f"{float(lon)-0.006},{float(lat)-0.003},{float(lon)+0.006},{float(lat)+0.003}"
    body = pagehead("Kontakty",
        "Rádi vám odpovíme na cokoli kolem docházky, zápisu i stravování. Nejrychleji nás zastihnete telefonicky.",
        [("Domů","index.html"),("Kontakty",None)]) + subnav([
        ("Kontaktní údaje","udaje"),("Jak se k nám dostanete","doprava"),
        ("Povinně zveřejňované informace","povinne")]) + f'''

<section class="section" id="udaje">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:start;gap:clamp(26px,3.5vw,44px)">
      <div class="contact-card">
        <h3 style="margin-top:0">{SKOLA["nazev"]}</h3>
        <ul class="contact-list">
          <li><span class="ico">{ico("pin",17)}</span><div><b>Adresa</b>
            <span>{SKOLA["ulice"]}, {SKOLA["mesto"]}</span></div></li>
          <li><span class="ico">{ico("telefon",17)}</span><div><b>Telefon</b>
            <a href="tel:{SKOLA["tel_link"]}">{SKOLA["tel"]}</a></div></li>
          <li><span class="ico">{ico("mail",17)}</span><div><b>E-mail</b>
            <a href="mailto:{SKOLA["mail"]}">{SKOLA["mail"]}</a></div></li>
          <li><span class="ico">{ico("hodiny",17)}</span><div><b>Provozní doba</b>
            <span>Po–Pá {SKOLA["provoz"]}</span></div></li>
          <li><span class="ico">{ico("dokument",17)}</span><div><b>IČ / datová schránka</b>
            <span>{SKOLA["ico"]} &middot; {SKOLA["ds"]}</span></div></li>
        </ul>
      </div>
      <div class="contact-card">
        <h3 style="margin-top:0">Kontaktní osoby</h3>
        <ul class="contact-list">
          <li><span class="ico">{ico("lide",17)}</span><div><b>Ředitelka školy</b>
            <span>{SKOLA["reditelka"]}</span><br>
            <a href="tel:{SKOLA["tel_link"]}">{SKOLA["tel"]}</a> &middot;
            <a href="mailto:{SKOLA["mail"]}">{SKOLA["mail"]}</a></div></li>
          <li><span class="ico">{ico("jidlo",17)}</span><div><b>Vedoucí stravovacího provozu</b>
            <span>{SKOLA["vedouci_sj"]}</span><br>
            <a href="tel:{SKOLA["tel_link"]}">{SKOLA["tel"]}</a></div></li>
          <li><span class="ico">{ico("stit",17)}</span><div><b>Pověřenec pro ochranu osobních údajů</b>
            <span>{SKOLA["gdpr_jmeno"]}</span><br>
            <a href="tel:+420{SKOLA["gdpr_tel"].replace(" ","")}">{SKOLA["gdpr_tel"]}</a> &middot;
            <a href="mailto:{SKOLA["gdpr_mail"]}">{SKOLA["gdpr_mail"]}</a></div></li>
        </ul>
        <p class="small muted" style="margin-top:20px">Zřizovatel: {SKOLA["zrizovatel"]}</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--blue section--pattern" id="doprava">
  <div class="wrap">
    {head("Kudy k nám", "Jak se k nám dostanete")}
    <div class="grid grid-2" style="align-items:stretch;gap:clamp(24px,3vw,38px)">
      <div class="map">
        <iframe title="Mapa – {SKOLA["ulice"]}, {SKOLA["mesto"]}" loading="lazy"
          src="https://www.openstreetmap.org/export/embed.html?bbox={bbox}&amp;layer=mapnik&amp;marker={lat},{lon}"></iframe>
      </div>
      <div class="stack">
        <div class="card"><div class="card__icon">{ico("pin")}</div>
          <h3>Adresa</h3>
          <p>{SKOLA["ulice"]}, {SKOLA["mesto"]}<br>
          <a href="https://mapy.cz/zakladni?q=%C5%BDi%C5%BEkova%201989%2F57%20Brno" target="_blank" rel="noopener">
            Otevřít v Mapy.cz {SIPKA}</a></p></div>
        <div class="card card--green"><div class="card__icon">{ico("lide")}</div>
          <h3>Městskou hromadnou dopravou</h3>
          <p>Nejbližší zastávky jsou v docházkové vzdálenosti několika minut. Aktuální spojení
            si nejlépe ověříte v <a href="https://idsjmk.cz" target="_blank" rel="noopener">vyhledávači IDS JMK</a>.</p></div>
        <div class="card card--teal"><div class="card__icon">{ico("domek")}</div>
          <h3>Parkování</h3>
          <p>V okolí školy lze parkovat v režimu rezidentního parkování Brno. Pro krátké zastavení
            při předávání dětí využijte prosím ohleduplně místa v přilehlých ulicích.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="povinne">
  <div class="wrap">
    {head("Povinné informace", "Povinně zveřejňované informace")}
    {docs_html(["zrizovaci-listina.pdf","gdpr-informacni-memorandum.pdf","vyrocni-zprava-2025.doc",
                "rozpocet-2026.docx","strednedoby-vyhled-rozpoctu-2026-2028.pdf","skolni-rad.docx"])}
    <div class="grid grid-2" style="margin-top:26px">
      <div class="card card--plain"><h3>Žádosti o informace</h3>
        <p class="small muted">Žádosti podle zákona č. 106/1999 Sb., o svobodném přístupu k informacím,
          přijímáme písemně na adrese školy, e-mailem na <a href="mailto:{SKOLA["mail"]}">{SKOLA["mail"]}</a>
          nebo do datové schránky <strong>{SKOLA["ds"]}</strong>.</p></div>
      <div class="card card--plain"><h3>Ochrana osobních údajů</h3>
        <p class="small muted">Informace o zpracování osobních údajů najdete v informačním memorandu.
          S dotazy se obracejte na pověřence {SKOLA["gdpr_jmeno"]},
          <a href="mailto:{SKOLA["gdpr_mail"]}">{SKOLA["gdpr_mail"]}</a>.</p></div>
    </div>
  </div>
</section>
'''
    return page("kontakty.html", f'Kontakty – {SKOLA["kratky"]}',
        f'Kontakty na MŠ Žižkova v Brně-Žabovřeskách: {SKOLA["ulice"]}, telefon {SKOLA["tel"]}, '
        f'{SKOLA["mail"]}. Mapa, doprava a povinně zveřejňované informace.',
        body, "kontakty.html", jsonld=True)

# ═════════════════════════════════════════════════════════════
#  DOPROVODNÉ SOUBORY
# ═════════════════════════════════════════════════════════════
JS = r'''/* MŠ Žižkova – drobná interaktivita */
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
'''

def assets():
    with open(os.path.join(ROOT, "assets/js/main.js"), "w", encoding="utf-8") as f:
        f.write(JS)

def sitemap(stranky):
    dnes = datetime.date.today().isoformat()
    url = "".join(
        f'  <url><loc>https://{SKOLA["web"]}/{"" if s == "index.html" else s}</loc>'
        f'<lastmod>{dnes}</lastmod></url>\n' for s in stranky)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + url + '</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: https://{SKOLA['web']}/sitemap.xml\n")

def main():
    stranky = [
        index_page(), skola_page(), vzdelavani_page(), projekty_page(),
        pro_rodice_page(), zapis_page(), aktuality_page(),
        fotogalerie_page(), kontakty_page(),
    ]
    assets()
    sitemap(stranky)
    print("Hotovo – vygenerováno %d stránek:" % len(stranky))
    for s in stranky:
        print("  ", s)

if __name__ == "__main__":
    main()
