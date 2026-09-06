# Web MŠ Žižkova, Brno

Statický web mateřské školy – čistý HTML/CSS/JS, bez frameworků, bez databáze.
Nasadí se na jakýkoli hosting (FTP, Netlify, Vercel, GitHub Pages, i současný Webnode).

---

## Co je hotové

| Stránka | Soubor | Obsah |
|---|---|---|
| Domů | `index.html` | představení školy, motto, filozofie, 3 rychlé odkazy, zaměření, hodnoty, aktuality |
| Škola | `skola.html` | kdo jsme, vybavení, školní zahrada, náš tým, provoz a režim dne |
| Vzdělávání | `vzdelavani.html` | ŠVP, zaměření (polytechnika–ekologie–umění), jak učíme, předškolní příprava |
| Projekty a spolupráce | `projekty.html` | dlouhodobé projekty, odborníci, organizace |
| Pro rodiče | `pro-rodice.html` | noví rodiče a adaptace, dokumenty a platby, stravování, zápis, prázdniny, kroužky |
| Zápis do MŠ | `zapis.html` | postup krok za krokem, kritéria, dokumenty, FAQ |
| Aktuality | `aktuality.html` | fixní „Důležité informace“ nahoře + chronologické novinky |
| Fotogalerie | `fotogalerie.html` | mřížka pro reprezentativní fotky |
| Kontakty | `kontakty.html` | kontaktní údaje, osoby, mapa, doprava, povinně zveřejňované informace |

Hlavní menu má **6 položek** (Domů · Škola · Vzdělávání · Pro rodiče · Aktuality · Kontakty),
**Zápis do MŠ** je vytažený jako výrazné tlačítko v hlavičce a jako první rychlý odkaz na úvodu –
podle doporučení v zadání. Sekce „Akce“ zrušena, vše je sjednocené v Aktualitách.

### Řazení sekcí

Pořadí sekcí i podsekcí odpovídá dokumentu *Struktura webu – verze 2*:

| dokument | kde je na webu |
|---|---|
| 1. Home | `index.html` |
| 2.1–2.5 Kdo jsme · Vybavení · Zahrada · Náš tým · Provoz | `skola.html`, ve stejném pořadí |
| 3.1–3.4 ŠVP · Zaměření · Jak učíme · Předškolní příprava | `vzdelavani.html`, ve stejném pořadí |
| 4.1–4.3 Dlouhodobé projekty · Odborníci · Organizace | `projekty.html` – **samostatná stránka**, ne podsekce |
| 5.1–5.6 Noví rodiče · Dokumenty · Stravování · Zápis · Prázdniny · Kroužky | `pro-rodice.html`, ve stejném pořadí |
| 6.1–6.2 Důležité informace · Novinky a akce | `aktuality.html`, ve stejném pořadí |
| 7. Fotogalerie | `fotogalerie.html` |
| 8.1–8.3 Údaje · Doprava · Povinné informace | `kontakty.html` + kontakty v zápatí |

Dokument uvádí u 2.1 „aplikace Naše MŠ“ – blok o aplikaci je proto na stránce Škola,
ne u rodičů. Adaptace je odrážkou 5.1, takže navazuje hned na „Informace pro nové rodiče“.
Platby (školné a stravné) v dokumentu nejsou samostatně, jsou proto součástí 5.2 Dokumenty.
Zápis má vlastní stránku – to je varianta, kterou dokument sám doporučuje – a v pozici 5.4
na něj vede odkaz, aby pořadí zůstalo zachované.

Menu má strop 6 položek, takže **Projekty** a **Fotogalerie** v něm nejsou (nejsou ani
v menu navrženém v dokumentu). Projekty vedou z rozbalovacího menu Vzdělávání a z patičky,
Fotogalerie z menu Škola a z patičky.

---

## Struktura složek

```
ms-zizkova/
├── index.html … kontakty.html   ← vygenerované stránky (needitovat ručně, viz níže)
├── build.py                     ← generátor: TEXTY A OBSAH SE MĚNÍ TADY
├── sitemap.xml, robots.txt
└── assets/
    ├── css/style.css            ← kompletní design systém
    ├── js/main.js               ← mobilní menu, podnavigace, rok v patičce
    ├── img/                     ← logo, značka, favicon, podkres
    └── dokumenty/               ← všechny PDF/DOCX stažené ze starého webu
```

### Jak měnit obsah

Stránky se generují z `build.py`. Postup:

```bash
# 1) uprav texty v build.py
# 2) přegeneruj web
python3 build.py
```

Nejčastější úpravy v `build.py`:

| Co | Kde v `build.py` |
|---|---|
| telefon, e-mail, adresa, jména, kapacita | slovník `SKOLA` (úplně nahoře) |
| položky menu a podmenu | seznam `NAV` |
| nová aktualita | seznam `NOVINKY` |
| důležité info (fixní blok nahoře) | seznam `DULEZITE` |
| tři oblasti zaměření | seznam `PILIRE` |
| hodnoty školy | seznam `HODNOTY` |
| tým / třídy | seznam `TYM` |
| režim dne | seznam `REZIM` |
| dokumenty ke stažení | seznam `DOKUMENTY` |

Kdyby build skript vadil, jde ho zahodit a editovat `.html` přímo – jsou to obyčejné statické
soubory. Pak se ale hlavička/patička musí měnit na osmi místech.

---

## Logo

Podle připomínky, že současné logo je příliš vysoké a nepůsobí moderně, vznikla nová
**nízká vodorovná verze**. Značka je **písmeno „O“ z původního nápisu MŠ ŽIŽKOVA** –
to, ve kterém sedí zajíček, veverka a ježeček, tedy tři třídy školky. Vyříznuté,
zvektorizované a přebarvené do přechodu modrá → eukalypt; vedle něj wordmark v písmu Outfit.
Poměr stran zhruba 3,7:1, takže se vejde do úzké hlavičky webu.

Celou rodinu log sestaví skript – po změně stačí spustit:

```bash
python3 podklady/udelej_logo.py     # potřebuje: brew install imagemagick potrace
```

Vyřízne O z `podklady/logo-puvodni-1000.png`, převede na vektor a poskládá všechny verze.

| Soubor | Použití |
|---|---|
| `assets/img/logo.svg` | web, světlé pozadí |
| `assets/img/logo-inverzni.svg` | tmavé pozadí (patička, prezentace) |
| `assets/img/logo-jednobarevne.svg` | jednobarevný tisk, razítko, faxová kvalita |
| `assets/img/logo-hlavickovy-papir.svg` | **hlavičkový papír** – plný název + adresní řádek |
| `assets/img/znacka.svg` | samotná značka (avatar, razítko, sociální sítě) |
| `assets/img/favicon.svg` | ikona v prohlížeči |
| `*.png` (`@4x`, `@8x`) | tytéž verze v PNG s průhledným pozadím pro Word, Canva apod. |

Písmo je v SVG **vložené** (embedded woff2), takže se logo zobrazí správně i na počítači,
kde Outfit nainstalovaný není.

Barvy značky:

```
modrá     #4A72AC      tmavá modrá   #1E3350
eukalypt  #6E9C87      mint          #A9CDBB
teal      #4E8E9B      papír         #FCFCFA
```

---

## Fotografie budovy

`assets/img/foto/` – upravená fotka budovy školy (originál v `podklady/foto-original/`).
Barevná korekce: srovnaná bílá, sytější zeleň a modrá oblohy, vytažené žluté průčelí,
zvednuté stíny, doostřeno.

| soubor | rozměr | kde se používá |
|---|---|---|
| `budova-hero.jpg` | 960 × 720 (4:3) | hero na úvodní straně, dlaždice ve fotogalerii |
| `budova.jpg` | 1600 × 720 (2,2:1) | Škola → Kdo jsme, `og:image` pro sdílení odkazu |
| `budova-nahled.jpg` | 640 × 480 | menší varianta do mřížky |

> **Pozor na rozlišení:** předloha měla jen 1600 px na šířku (stažená z původního webu),
> takže na retina displejích je fotka měkčí. Až bude focení s p. Dvořákem, vyplatí se
> nahradit ji originálem – stačí přepsat soubory pod stejnými názvy.

## Dětské výkresy

Ve složce `assets/img/vykresy/` je 14 výkresů dětí ze školky. Zpracovává je skript
`podklady/uprav_vykresy.py` z fotek v `podklady/vykresy-original/`:

```bash
python3 podklady/uprav_vykresy.py
```

Co skript dělá: otočí fotku do správné orientace, **rozpozná dřevěný stůl kolem papíru
a odřízne ho** (podle toho, že je teplý a zároveň tmavší než papír, takže se nesplete
se žlutou pastelkou), srovná bílou, zvýrazní barvy pastelek a doostří. Z každého výkresu
uloží webovou velikost (1400 px) a náhled (640 px).

Nové výkresy stačí nahrát do `podklady/vykresy-original/`, spustit skript a přidat řádek
do seznamu `VYKRESY` v `build.py`.

Kde jsou na webu – **výkresy zastupují všechna místa, kde ještě nejsou fotky**,
takže na webu není jediná šedá zástupná plocha:

| stránka | co tam je |
|---|---|
| Úvodní strana | sekce „Takhle naši školku vidí děti“ – čtyři výkresy |
| Škola → Vybavení | tři výkresy místo fotek heren |
| Škola → Školní zahrada | jeden výkres |
| Škola → Náš tým | široký pás se společnou kresbou „Naše děti“ |
| Vzdělávání → Zaměření | tři výkresy |
| Pro rodiče → Adaptace | jeden výkres |
| Fotogalerie | všech 14 jako hlavní sekce |

Až dorazí profesionální fotky, nahradí se ve `build.py` volání `vykres(...)` /
`vykresy_mrizka(...)` funkcí `foto(...)` – výkresy zůstanou v galerii a na úvodní straně.

Chybějící fotky, na které se čeká: herny Zajíčků / Ježečků / Veverek, vstup a šatna,
školní zahrada, pískoviště a herní prvky, bylinkové záhonky, keramická dílna,
technická dílna s ponkem, detail dětských rukou při tvoření, certifikáty a projekty.

> **K rozhodnutí pro školku:** v kresbách jsou vidět křestní jména dětí (ISABELLA, JOHANA,
> MEDA…). Vzhledem k tomu, že fotky dětí na web záměrně nedáváme, je na místě potvrdit,
> že jména přímo v kresbách jsou v pořádku.

## Grafický podkres

`assets/img/podkres.svg` je bezešvá dlaždice 520 × 520 px s jemnou mozaikou dětských kreseb
(sluníčko, domeček, kytka, loďka, notička, ozubené kolo, lupa, list…) v barvách palety.
Používá se v hero sekci, na hlavičkách podstránek a ve vybraných sekcích.

K dispozici jsou **dvě varianty** a přepínají se jedním blokem v `assets/css/style.css`:

| varianta | soubor | jak působí |
|---|---|---|
| **1 – linkové kresbičky** (výchozí) | `podkres.svg` | čistší, bezešvá, funguje v každé velikosti |
| **2 – mozaika dětských výkresů** | `podkres-vykresy.jpg` | přesně podle zadání klientky, autentičtější, o něco živější |

Ve `style.css` je varianta 2 připravená jako zakomentované tři řádky hned pod výchozím
nastavením – stačí je odkomentovat.

Obecně platí, že podkres se řídí třemi proměnnými:

```css
:root{
  --pattern: url("../img/podkres-vykresy.png");  /* vlastní mozaika */
  --pattern-size: 520px;      /* velikost dlaždice */
  --pattern-opacity: .22;     /* jak moc má prosvítat */
}
```

Nic dalšího se měnit nemusí – podkres se propíše na všech místech najednou.

---

## Co je potřeba doplnit od školky

1. **Profesionální fotografie** – místo šedých zástupných ploch (`FOTO: …`).
   Podle zadání bez identifikovatelných dětí – budova, zahrada, herny, detaily, ruce při práci.
   Fotky nahrát do `assets/img/foto/` a v `build.py` nahradit volání `ph("…")` funkcí
   `foto("soubor.jpg", "popis", šířka, výška)` – budova školy už je hotová takhle.
2. **Skeny dětských výkresů** na podkres (viz výše).
3. **Termíny zápisu 2027/2028** a aktuální kritéria – `zapis_page()` v `build.py`.
4. **Ověření týmu** – jmenný seznam je 1 : 1 převzatý ze stránky *Zaměstnanci* na starém webu
   (ověřeno 6. 9. 2026). Jediné úpravy: „asistent pedagoga“ → „asistentka pedagoga“ a
   „vedoucí školní jídelny“ → „vedoucí stravovacího provozu“ (přejmenování si vyžádala
   klientka v dokumentu). Přesto se hodí, aby školka seznam potvrdila – na starém webu
   nemusí být aktuální. Seznam je `TYM` v `build.py`.
5. **Režim dne** – vložený rozvrh je obvyklý rámec pro MŠ, ne oficiální dokument školy.
   Potřebuje potvrdit / upravit (`REZIM` v `build.py`).
6. **Jídelníček** – `assets/dokumenty/jidelnicek-aktualni.pdf`. Při týdenní aktualizaci se jen
   přepíše soubor pod stejným názvem, na webu se nic měnit nemusí.
7. **Odkaz na aplikaci Naše MŠ** – zatím vede na kontakty; až bude k dispozici přihlašovací
   URL školy, doplní se.

---

## Poznámka k obsahu

V podkladech byly dvě různé polohy školy:

* starší profilace ze současného webu – **výtvarné a keramické činnosti, pohyb, práce s knihou**,
* nový dokument *Hodnoty – vize – zaměření* (30. 6. 2026) – **polytechnika, ekologie, umění**.

Web staví na **nové** vizi (tři oblasti zaměření = hlavní sdělení), zároveň ale nezahazuje
dosavadní profilaci – ta je na stránce *Vzdělávání* v bloku „Další oblasti, které u nás mají
pevné místo“. Název ŠVP *„Radostně objevujeme svět“* je zachovaný jako motto webu.

Z dokumentu *Vize a hodnoty* byla použita **kratší varianta pro web** (30. 6. 2026); delší verze
s důrazem na bezpečí a stabilitu je promítnutá do sekce Hodnoty.

---

## Lokální náhled

```bash
cd ms-zizkova
python3 -m http.server 8000
# → http://localhost:8000
```

## Nasazení

Nahrát obsah složky na hosting (FTP / rsync / git). Žádný build na serveru není potřeba.
Před ostrým nasazením zkontrolovat:

* doménu v `sitemap.xml` a `robots.txt` (`SKOLA["web"]` v `build.py`),
* přesměrování starých URL (`/o-skolce/` → `/skola.html`, `/akce/` → `/aktuality.html` atd.).

---

## Přístupnost a technika

* sémantické HTML, `lang="cs"`, přeskočení na obsah, viditelný focus
* mobilní menu ovladatelné klávesnicí, zavírá se Escapem
* respektuje `prefers-reduced-motion`
* strukturovaná data schema.org `Preschool` (Google – mapa, otevírací doba)
* mapa přes OpenStreetMap – bez cookies třetích stran a bez API klíče
* vlastní styl pro tisk
