#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sestaví logo MŠ Žižkova ze značky „O“ z původního loga školy.

Písmeno O v původním nápisu MŠ ŽIŽKOVA obsahuje zajíčka, veverku a ježečka –
tři třídy školky. Skript ho vyřízne z původního obrázku, zvektorizuje (potrace)
a poskládá z něj celou rodinu log.

Potřebuje:  brew install imagemagick potrace
Spuštění:   python3 podklady/udelej_logo.py
"""
import os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG  = os.path.join(ROOT, "assets/img")
TMP  = "/tmp/_znacka"

# původní logo školy a poloha písmene O v něm (zjištěno z profilu inkoustu)
PUVODNI = os.path.join(ROOT, "podklady/logo-puvodni-1000.png")
VYREZ   = "139x205+646+45"

INK   = "#1E3350"     # tmavá modrá – text
MODRA = "#4A72AC"     # firemní modrá – barva loga
ZELEN = "#6E9C87"     # eukalypt – podtitul
MINT  = "#A9CDBB"

def sh(*a, **kw):
    return subprocess.run(a, check=True, capture_output=True, text=True, **kw).stdout

def vektorizuj(vyrez=None, zvetseni="800%", jmeno="a"):
    """Vyřízne část loga, ořízne na těsno a převede na vektorovou cestu."""
    prikaz = ["magick", PUVODNI, "-background", "white", "-flatten"]
    if vyrez:
        prikaz += ["-crop", vyrez, "+repage"]
    prikaz += ["-colorspace", "gray", "-resize", zvetseni, "-threshold", "62%",
               "-trim", "+repage", f"pbm:{TMP}{jmeno}.pbm"]
    sh(*prikaz)
    sh("potrace", f"{TMP}{jmeno}.pbm", "-s", "-o", f"{TMP}{jmeno}.svg",
       "--alphamax", "1.0", "--opttolerance", "0.2", "--turdsize", "12")
    svg = open(f"{TMP}{jmeno}.svg", encoding="utf-8").read()
    w, h = (float(x) for x in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
    telo = re.search(r"(<g transform=.*?</g>)", svg, re.S).group(1)
    telo = telo.replace('fill="#000000"', 'fill="FILL"')
    return telo, w, h

# samotná značka „O“ (do faviconu a čtvercových míst)
TELO, VB_W, VB_H = vektorizuj(VYREZ, jmeno="o")
POMER = VB_W / VB_H          # značka je na výšku, cca 0,71

# celý nápis MŠ ŽIŽKOVA i se zvířátky v O
NAPIS, NAP_W, NAP_H = vektorizuj(None, "400%", jmeno="n")
NAP_POMER = NAP_W / NAP_H    # cca 4,2 : 1

def znacka(uid, vyska, x=0, y=0, barva=None):
    """Značka „O“ vysoká `vyska`, levý horní roh na (x, y)."""
    fill = barva or f"url(#g{uid})"
    s = vyska / VB_H
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5f})">'
            + TELO.replace("FILL", fill) + "</g>")

def gradient(uid, c1="#4A72AC", c2="#4E8E9B"):
    return (f'<linearGradient id="g{uid}" gradientUnits="objectBoundingBox" '
            f'x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>'
            f'</linearGradient>')

# vložené písmo, aby se logo vysázelo správně i bez nainstalovaného Outfitu
P = "/private/tmp/claude-501/-Users-petrkadlec/fdfb3e19-1e98-4e82-818d-186ac3032544/scratchpad/"
try:
    EXT = open(P + "o700ext.b64").read(); LAT = open(P + "o700lat.b64").read()
    FONT = ("<style>"
      "@font-face{font-family:'Outfit MS';font-weight:700;font-style:normal;"
      f"src:url(data:font/woff2;base64,{EXT}) format('woff2');"
      "unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,"
      "U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,"
      "U+2C60-2C7F,U+A720-A7FF;}"
      "@font-face{font-family:'Outfit MS';font-weight:700;font-style:normal;"
      f"src:url(data:font/woff2;base64,{LAT}) format('woff2');"
      "unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,"
      "U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;}"
      ".n{font-family:'Outfit MS',Outfit,Poppins,'Trebuchet MS',sans-serif;font-weight:700}"
      "</style>")
except FileNotFoundError:
    FONT = "<style>.n{font-family:Outfit,Poppins,'Trebuchet MS',sans-serif;font-weight:700}</style>"

def svg(vb, telo, w=None, h=None, titulek="MŠ Žižkova, Brno"):
    rozmer = f' width="{w}" height="{h}"' if w else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{rozmer} '
            f'role="img" aria-label="{titulek}"><title>{titulek}</title>{telo}</svg>\n')

def zapis(jmeno, obsah):
    with open(os.path.join(IMG, jmeno), "w", encoding="utf-8") as f:
        f.write(obsah)
    print("  ", jmeno)

def main():
    sirka_znacky = 64 * POMER

    # --- samotná značka (čtvercový rám, značka vycentrovaná) ---
    for jmeno, uid in (("znacka.svg", "z"), ("favicon.svg", "f")):
        x = (64 - 60 * POMER) / 2
        zapis(jmeno, svg("0 0 64 64", f"<defs>{gradient(uid)}</defs>"
                         + znacka(uid, 60, x, 2), 64, 64, "MŠ Žižkova"))

    # --- vodorovné logo = původní nápis MŠ ŽIŽKOVA ---
    def napis(barva, vyska=64, x=0, y=0):
        s = vyska / NAP_H
        return (f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.6f})">'
                + NAPIS.replace("FILL", barva) + "</g>")

    sirka = 64 * NAP_POMER
    vb = f"0 0 {sirka:.0f} 64"
    zapis("logo.svg",              svg(vb, napis(MODRA),     int(sirka), 64))
    zapis("logo-inverzni.svg",     svg(vb, napis("#FFFFFF"), int(sirka), 64))
    zapis("logo-jednobarevne.svg", svg(vb, napis(INK),       int(sirka), 64))

    # --- hlavičkový papír ---
    hlavicka = (FONT + napis(MODRA, 46, 0, 4)
        + f'<text class="n" x="0" y="70" font-size="11" letter-spacing="1.9" '
          f'fill="{ZELEN}">MATEŘSKÁ ŠKOLA, BRNO, ŽIŽKOVA 57, PŘÍSPĚVKOVÁ ORGANIZACE</text>'
        + '<line x1="0" y1="82" x2="700" y2="82" stroke="#DDE4EA" stroke-width="1.5"/>'
        + '<text class="n" x="0" y="99" font-size="10" letter-spacing="0.35" fill="#6E7F8B">'
          'ŽIŽKOVA 1989/57, 616 00 BRNO-ŽABOVŘESKY &#160;&#183;&#160; 770 696 365 &#160;&#183;&#160; '
          'REDITELKA@SKOLKA-ZIZKOVA.CZ &#160;&#183;&#160; IČ 70874794</text>')
    zapis("logo-hlavickovy-papir.svg",
          svg("0 0 700 108", hlavicka, 700, 108,
              "Mateřská škola, Brno, Žižkova 57, příspěvková organizace"))

    print(f"\nZnačka „O“ má poměr {POMER:.3f}, nápis {NAP_POMER:.2f} : 1, logo {sirka:.0f}×64.")

if __name__ == "__main__":
    main()
