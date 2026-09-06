#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Připraví kopii webu pro veřejný náhled na GitHub Pages.

Oproti ostré verzi navíc:
  • <meta name="robots" content="noindex,nofollow"> – náhled nesmí konkurovat
    skutečné doméně školky ve vyhledávání,
  • robots.txt se zákazem indexace,
  • úzký pruh nahoře, aby bylo jasné, že jde o náhled.

Spuštění:  python3 podklady/pripravit_nahled.py [cílová složka]
"""
import os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIL  = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ms-zizkova-pages"

PRUH_CSS = """<style>
.nahled-pruh{background:#EAF5EF;border-bottom:1px solid #D5EADF;color:#4F7C68;
  font-family:Outfit,system-ui,sans-serif;font-size:.86rem;font-weight:500}
.nahled-pruh__in{display:flex;flex-wrap:wrap;gap:.3em 1.4em;align-items:center;
  justify-content:space-between;padding-block:.65em}
.nahled-pruh b{color:#1E3350;font-weight:600}
.nahled-pruh span{color:#6E7F8B;font-weight:400;font-family:Inter,system-ui,sans-serif;font-size:.83rem}
</style>"""

PRUH = """<div class="nahled-pruh"><div class="wrap nahled-pruh__in">
  <b>Náhled nového webu MŠ Žižkova</b>
  <span>Pracovní verze pro připomínkování &middot; fotografie interiérů zatím doplňujeme</span>
</div></div>"""

def main():
    if os.path.isdir(CIL):
        shutil.rmtree(CIL)
    os.makedirs(CIL)

    for polozka in os.listdir(ROOT):
        if polozka.startswith((".", "_")) or polozka in ("podklady", "nahled", "build.py",
                                                         "build_preview.py", "README.md"):
            continue
        zdroj, cil = os.path.join(ROOT, polozka), os.path.join(CIL, polozka)
        (shutil.copytree if os.path.isdir(zdroj) else shutil.copy2)(zdroj, cil)

    pocet = 0
    for soubor in os.listdir(CIL):
        if not soubor.endswith(".html"):
            continue
        cesta = os.path.join(CIL, soubor)
        s = open(cesta, encoding="utf-8").read()
        s = s.replace('<meta name="theme-color"',
                      '<meta name="robots" content="noindex,nofollow">\n<meta name="theme-color"', 1)
        s = s.replace("</head>", PRUH_CSS + "\n</head>", 1)
        s = s.replace('<a class="skip"', PRUH + '\n<a class="skip"', 1)
        open(cesta, "w", encoding="utf-8").write(s)
        pocet += 1

    with open(os.path.join(CIL, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("# Náhled – nesmí se indexovat, ostrý web běží na vlastní doméně.\n"
                "User-agent: *\nDisallow: /\n")
    os.remove(os.path.join(CIL, "sitemap.xml"))
    open(os.path.join(CIL, ".nojekyll"), "w").close()

    print(f"Náhled připraven v {CIL} – {pocet} stránek, indexace zakázaná.")

if __name__ == "__main__":
    main()
