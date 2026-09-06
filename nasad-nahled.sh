#!/bin/bash
# Publikuje aktuální web jako veřejný náhled na GitHub Pages.
#   https://kadlecpetr.github.io/ms-zizkova/
set -e
cd "$(dirname "$0")"

echo "1/4  generuji web…"
python3 build.py > /dev/null

echo "2/4  připravuji náhled (noindex)…"
python3 podklady/pripravit_nahled.py /tmp/ms-zizkova-pages > /dev/null

echo "3/4  odesílám na větev gh-pages…"
cd /tmp/ms-zizkova-pages
git init -q -b gh-pages
git add -A
git -c user.name="Petr Kadlec" \
    -c user.email="121253761+kadlecpetr@users.noreply.github.com" \
    commit -q -m "Náhled webu MŠ Žižkova – $(date '+%-d. %-m. %Y %H:%M')"
git remote add origin https://github.com/kadlecpetr/ms-zizkova.git
git push -q --force origin gh-pages

echo "4/4  hotovo – za chvíli naběhne:"
echo "     https://kadlecpetr.github.io/ms-zizkova/"
