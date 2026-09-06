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
ZELEN = "#6E9C87"     # eukalypt – podtitul
MINT  = "#A9CDBB"

def sh(*a, **kw):
    return subprocess.run(a, check=True, capture_output=True, text=True, **kw).stdout

def vektorizuj():
    """Vyřízne O, ořízne na těsno a převede na vektorovou cestu."""
    sh("magick", PUVODNI, "-background", "white", "-flatten",
       "-crop", VYREZ, "+repage", "-colorspace", "gray",
       "-resize", "800%", "-threshold", "62%",
       "-trim", "+repage", f"pbm:{TMP}.pbm")
    sh("potrace", f"{TMP}.pbm", "-s", "-o", f"{TMP}.svg",
       "--alphamax", "1.0", "--opttolerance", "0.2", "--turdsize", "12")
    svg = open(f"{TMP}.svg", encoding="utf-8").read()
    w, h = (float(x) for x in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
    telo = re.search(r"(<g transform=.*?</g>)", svg, re.S).group(1)
    telo = telo.replace('fill="#000000"', 'fill="FILL"')
    return telo, w, h

TELO, VB_W, VB_H = vektorizuj()
POMER = VB_W / VB_H          # značka je na výšku, cca 0,68

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

    # --- vodorovné logo ---
    def vodorovne(uid, barva_nazvu, barva_podtitulu, barva_znacky=None):
        text_x = sirka_znacky + 17
        return ("<defs>" + gradient(uid) + "</defs>" + FONT
                + znacka(uid, 64, 0, 0, barva_znacky)
                + f'<text class="n" x="{text_x:.1f}" y="33.5" font-size="34" '
                  f'letter-spacing="-0.4" fill="{barva_nazvu}">MŠ Žižkova</text>'
                + f'<text class="n" x="{text_x+.5:.1f}" y="51.5" font-size="12" '
                  f'letter-spacing="2.6" fill="{barva_podtitulu}">BRNO &#183; ŽABOVŘESKY</text>')

    sirka = sirka_znacky + 17 + 174
    zapis("logo.svg",           svg(f"0 0 {sirka:.0f} 64", vodorovne("a", INK, ZELEN),   int(sirka), 64))
    zapis("logo-inverzni.svg",  svg(f"0 0 {sirka:.0f} 64", vodorovne("b", "#FFFFFF", MINT, "#FFFFFF"), int(sirka), 64))
    zapis("logo-jednobarevne.svg", svg(f"0 0 {sirka:.0f} 64", vodorovne("d", INK, INK, INK), int(sirka), 64))

    # --- hlavičkový papír ---
    zn_h = 60
    zn_w = zn_h * POMER
    tx = zn_w + 16
    hlavicka = ("<defs>" + gradient("h") + "</defs>" + FONT + znacka("h", zn_h, 0, 2)
        + f'<text class="n" x="{tx:.1f}" y="30" font-size="26" letter-spacing="-0.3" '
          f'fill="{INK}">Mateřská škola, Brno, Žižkova 57</text>'
        + f'<text class="n" x="{tx+.5:.1f}" y="49" font-size="10.5" letter-spacing="2.2" '
          f'fill="{ZELEN}">PŘÍSPĚVKOVÁ ORGANIZACE</text>'
        + '<line x1="0" y1="70" x2="700" y2="70" stroke="#DDE4EA" stroke-width="1.5"/>'
        + '<text class="n" x="0" y="87" font-size="10" letter-spacing="0.35" fill="#6E7F8B">'
          'ŽIŽKOVA 1989/57, 616 00 BRNO-ŽABOVŘESKY &#160;&#183;&#160; 770 696 365 &#160;&#183;&#160; '
          'REDITELKA@SKOLKA-ZIZKOVA.CZ &#160;&#183;&#160; IČ 70874794</text>')
    zapis("logo-hlavickovy-papir.svg",
          svg("0 0 700 96", hlavicka, 700, 96,
              "Mateřská škola, Brno, Žižkova 57, příspěvková organizace"))

    print(f"\nZnačka má poměr {POMER:.3f} (š:v), logo je {sirka:.0f}×64.")

if __name__ == "__main__":
    main()
