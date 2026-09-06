#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Úprava fotek dětských výkresů pro web.

Co dělá s každou fotkou:
  1. otočí do správné orientace (fotky jsou na výšku, kresby na šířku),
  2. odřízne dřevěný stůl kolem papíru – rozpozná ho podle toho, že je
     teplý (R výrazně > B) a zároveň tmavší než papír, takže se nesplete
     se žlutou pastelkou,
  3. srovná bílou (papír má být papírový, ne narůžovělý od žárovky),
  4. zvýrazní barvy pastelek a doostří,
  5. uloží webovou velikost + náhled + odbarvenou dlaždici do podkresu.

Spuštění:  python3 podklady/uprav_vykresy.py
"""
import os, subprocess, json

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZDROJ  = os.path.join(ROOT, "podklady/vykresy-original")
CIL    = os.path.join(ROOT, "assets/img/vykresy")
OTOCIT = "-90"          # fotky jsou otočené o 90°

KROK       = 8          # po kolika pixelech se okraj odkrajuje
MAX_PODIL  = 0.09       # nikdy neodřízne víc než 9 % strany
TEPLOTA    = 0.115      # R - B, nad tím je to dřevo (0-1)
JAS_DREVA  = 0.82       # dřevo je zároveň tmavší než papír

def magick(*args):
    return subprocess.run(["magick", *args], capture_output=True, text=True).stdout.strip()

def pas(soubor, geom):
    """Vrátí (teplota, jas) vodorovného/svislého pásu."""
    v = magick(soubor, "-crop", geom, "+repage", "-format",
               "%[fx:mean.r] %[fx:mean.b] %[fx:mean]", "info:")
    r, b, m = (float(x) for x in v.split())
    return r - b, m

def orez(soubor, w, h):
    """Kolik odříznout z jednotlivých stran, aby zmizel stůl."""
    limit_v, limit_h = int(h * MAX_PODIL), int(w * MAX_PODIL)
    rezy = {}
    for strana in ("nahore", "dole", "vlevo", "vpravo"):
        rez, limit = 0, (limit_v if strana in ("nahore", "dole") else limit_h)
        while rez < limit:
            if strana == "nahore":  geom = f"{w}x{KROK}+0+{rez}"
            elif strana == "dole":  geom = f"{w}x{KROK}+0+{h-rez-KROK}"
            elif strana == "vlevo": geom = f"{KROK}x{h}+{rez}+0"
            else:                   geom = f"{KROK}x{h}+{w-rez-KROK}+0"
            teplo, jas = pas(soubor, geom)
            if teplo > TEPLOTA and jas < JAS_DREVA:
                rez += KROK
            else:
                break
        rezy[strana] = rez + (KROK if rez else 6)   # kousek navíc na stín okraje
    return rezy

def main():
    os.makedirs(CIL, exist_ok=True)
    tmp = "/tmp/_vykres_rot.png"
    prehled = []

    for soubor in sorted(os.listdir(ZDROJ)):
        if not soubor.lower().endswith((".jpeg", ".jpg")):
            continue
        cislo = os.path.splitext(soubor)[0]
        zdroj = os.path.join(ZDROJ, soubor)

        subprocess.run(["magick", zdroj, "-rotate", OTOCIT, tmp], check=True)
        w, h = (int(x) for x in magick(tmp, "-format", "%w %h", "info:").split())
        r = orez(tmp, w, h)
        nw = w - r["vlevo"] - r["vpravo"]
        nh = h - r["nahore"] - r["dole"]
        crop = f"{nw}x{nh}+{r['vlevo']}+{r['nahore']}"

        uprava = [
            "-crop", crop, "+repage",
            # srovnání bílé – jen horní konec, aby se nekrušily stíny pastelek
            "-channel", "RGB", "-contrast-stretch", "0%x0.15%", "+channel",
            "-modulate", "101,136,100",          # sytější pastelky
            "-brightness-contrast", "1x7",
            "-unsharp", "0x1.1+0.6+0.02",
        ]
        vystup = os.path.join(CIL, f"vykres-{cislo}.jpg")
        subprocess.run(["magick", tmp, *uprava, "-resize", "1400x",
                        "-quality", "84", "-strip", vystup], check=True)
        subprocess.run(["magick", tmp, *uprava, "-resize", "640x",
                        "-quality", "80", "-strip",
                        os.path.join(CIL, f"vykres-{cislo}-nahled.jpg")], check=True)

        prehled.append({"soubor": f"vykres-{cislo}.jpg", "orez": r,
                        "rozmer": f"{nw}x{nh}"})
        print(f"  {cislo}: ořez {r}  →  {nw}x{nh}")

    with open(os.path.join(CIL, "prehled.json"), "w", encoding="utf-8") as f:
        json.dump(prehled, f, ensure_ascii=False, indent=2)
    print(f"\nHotovo – {len(prehled)} výkresů v {CIL}")

if __name__ == "__main__":
    main()
