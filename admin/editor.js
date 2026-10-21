/* Editor webu MŠ Žižkova
 *
 * Stránky jsou statické. Editor načte skutečnou stránku do rámu, nechá v ní psát přímo do textů
 * a měnit fotky a změny uloží do souboru content.json v repozitáři na GitHubu. Po uložení se web
 * sám znovu vygeneruje (GitHub Actions, viz .github/workflows/publish.yml).
 *
 * content.json: { texts:{klíč:html}, images:{klíč:cesta}, alts:{klíč:popis}, novinky:[{d,t,p}] }
 * Klíče vznikají v build.py (data-ek u textů, data-ei u obrázků).
 */
(function () {
  'use strict';

  var REPO = 'kadlecpetr/ms-zizkova';
  var BRANCH = 'main';
  var STRANKY = [
    ['index.html', 'Úvodní stránka'], ['skola.html', 'Škola'], ['vzdelavani.html', 'Vzdělávání'],
    ['projekty.html', 'Projekty a spolupráce'], ['pro-rodice.html', 'Pro rodiče'], ['zapis.html', 'Zápis do MŠ'],
    ['aktuality.html', 'Aktuality'], ['fotogalerie.html', 'Fotogalerie'], ['kontakty.html', 'Kontakty']
  ];

  var $ = function (id) { return document.getElementById(id); };
  var token = '';
  var rezim = 'github';            // 'github' | 'offline'
  var state = { texts: {}, images: {}, alts: {}, novinky: null };
  var puvodniStav = '';            // JSON stavu ze serveru (kvůli zjištění neuložených změn)
  var soubory = {};                // cesta v repozitáři -> base64 nově nahraných fotek
  var nahledy = {};                // klíč obrázku -> dataURL (pro zobrazení ještě nepublikované fotky)
  var puvodniSrc = {};             // klíč obrázku -> src, jak byl při načtení stránky
  var vybranyObrazek = null;       // klíč
  var frame = $('ramec');
  var aktualniStranka = 'index.html';

  /* ───────── pomocné ───────── */
  function hlaska(text, chyba) {
    var t = $('toast');
    t.textContent = text; t.className = 'toast' + (chyba ? ' is-err' : ''); t.hidden = false;
    clearTimeout(hlaska._t);
    hlaska._t = setTimeout(function () { t.hidden = true; }, chyba ? 7000 : 3500);
  }
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function b64Text(b64) { // base64 -> UTF-8 text
    var bin = atob(b64.replace(/\s/g, ''));
    return new TextDecoder().decode(Uint8Array.from(bin, function (c) { return c.charCodeAt(0); }));
  }
  function jsonStav() {
    var o = { texts: state.texts, images: state.images, alts: state.alts };
    if (state.novinky) o.novinky = state.novinky;
    return JSON.stringify(o, null, 2) + '\n';
  }
  function jeZmena() { return JSON.stringify(JSON.parse(jsonStav())) !== puvodniStav; }
  function obnovStav() {
    var z = jeZmena(), el = $('stav');
    el.textContent = z ? 'Neuložené změny' : (el.dataset.ok ? el.dataset.ok : 'Žádné změny');
    el.className = 'bar__stav' + (z ? ' is-dirty' : (el.dataset.ok ? ' is-ok' : ''));
    if (z) delete el.dataset.ok;
    $('btnPublikovat').disabled = !z;
  }
  function zmena() { delete $('stav').dataset.ok; obnovStav(); }

  /* ───────── GitHub API ───────── */
  function gh(cesta, volby) {
    volby = volby || {};
    return fetch('https://api.github.com/repos/' + REPO + cesta, {
      method: volby.method || 'GET',
      headers: { 'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json' },
      body: volby.body ? JSON.stringify(volby.body) : undefined
    }).then(function (r) {
      if (r.status === 404 && volby.ok404) return null;
      if (!r.ok) {
        return r.text().then(function (t) {
          var e = new Error(r.status === 401 ? 'Přístupový klíč není platný nebo vypršel.' :
            r.status === 403 ? 'Klíč nemá právo zapisovat do repozitáře (Contents: Read and write).' :
            'GitHub odpověděl chybou ' + r.status + ' ' + t.slice(0, 160));
          e.status = r.status; throw e;
        });
      }
      return r.json();
    });
  }
  function nactiObsah() {
    if (rezim === 'offline') return Promise.resolve({});
    return gh('/contents/content.json?ref=' + BRANCH, { ok404: true }).then(function (d) {
      if (!d) return {};
      try { return JSON.parse(b64Text(d.content)); } catch (e) { return {}; }
    });
  }
  function publikovat() {
    var json = jsonStav();
    if (rezim === 'offline') {
      var a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([json], { type: 'application/json' }));
      a.download = 'content.json'; a.click();
      hlaska('Zkušební režim: změny se neodeslaly, stáhl se jen soubor content.json.');
      return Promise.resolve();
    }
    var btn = $('btnPublikovat'); btn.disabled = true; btn.textContent = 'Odesílám…';
    var base, commitSha;
    return gh('/git/ref/heads/' + BRANCH).then(function (ref) {
      base = ref.object.sha;
      return gh('/git/commits/' + base);
    }).then(function (c) {
      var cesty = Object.keys(soubory);
      // jen fotky, které jsou v obsahu opravdu použité
      var pouzite = {}; Object.keys(state.images).forEach(function (k) { pouzite[state.images[k]] = 1; });
      cesty = cesty.filter(function (p) { return pouzite[p]; });
      var sliby = [gh('/git/blobs', { method: 'POST', body: { content: json, encoding: 'utf-8' } }).then(function (b) {
        return { path: 'content.json', mode: '100644', type: 'blob', sha: b.sha };
      })];
      cesty.forEach(function (p) {
        sliby.push(gh('/git/blobs', { method: 'POST', body: { content: soubory[p], encoding: 'base64' } }).then(function (b) {
          return { path: p, mode: '100644', type: 'blob', sha: b.sha };
        }));
      });
      return Promise.all(sliby).then(function (tree) {
        return gh('/git/trees', { method: 'POST', body: { base_tree: c.tree.sha, tree: tree } });
      });
    }).then(function (t) {
      return gh('/git/commits', { method: 'POST', body: { message: 'Úpravy webu z editoru', tree: t.sha, parents: [base] } });
    }).then(function (c) {
      commitSha = c.sha;
      return gh('/git/refs/heads/' + BRANCH, { method: 'PATCH', body: { sha: c.sha } });
    }).then(function () {
      puvodniStav = JSON.stringify(JSON.parse(json));
      soubory = {};
      btn.textContent = 'Publikovat';
      hlaska('Změny jsou uložené. Web se za chvíli přegeneruje.');
      sledujNasazeni(commitSha);
      obnovStav();
    }).catch(function (e) {
      btn.textContent = 'Publikovat'; obnovStav();
      hlaska('Publikace se nezdařila: ' + e.message, true);
    });
  }
  function sledujNasazeni(sha) {
    var el = $('stav'), pokusu = 0;
    el.className = 'bar__stav'; el.textContent = 'Web se přegenerovává…';
    (function dotaz() {
      pokusu++;
      gh('/actions/runs?head_sha=' + sha, { ok404: true }).then(function (d) {
        var run = d && d.workflow_runs && d.workflow_runs[0];
        if (run && run.status === 'completed') {
          if (run.conclusion === 'success') { el.dataset.ok = 'Hotovo – změny jsou na webu ✓'; }
          else { el.textContent = 'Nasazení selhalo – ozvěte se správci webu'; el.className = 'bar__stav is-dirty'; return; }
          obnovStav(); return;
        }
        if (pokusu < 40) setTimeout(dotaz, 6000);
        else { el.dataset.ok = 'Odesláno – změny se objeví do několika minut'; obnovStav(); }
      }).catch(function () {
        el.dataset.ok = 'Odesláno – změny se objeví do několika minut'; obnovStav();
      });
    })();
  }

  /* ───────── úklid HTML z contenteditable ───────── */
  function cistyHtml(el) {
    var out = '';
    (function walk(n) {
      n.childNodes.forEach(function (c) {
        if (c.nodeType === 3) { out += esc(c.nodeValue).replace(/ /g, '&nbsp;'); return; }
        if (c.nodeType !== 1) return;
        var t = c.tagName.toLowerCase();
        if (t === 'br') { out += '<br>'; }
        else if (t === 'b' || t === 'strong') { out += '<strong>'; walk(c); out += '</strong>'; }
        else if (t === 'i' || t === 'em') { out += '<em>'; walk(c); out += '</em>'; }
        else if (t === 'small') { out += '<small>'; walk(c); out += '</small>'; }
        else if (t === 'a') {
          var h = c.getAttribute('href') || '';
          if (/^(https?:|mailto:|tel:|#|[\w./-]+(\.html)?(#[\w-]*)?$)/i.test(h)) { out += '<a href="' + esc(h) + '">'; walk(c); out += '</a>'; }
          else walk(c);
        }
        else if (t === 'div' || t === 'p') { if (out && !/<br>$/.test(out)) out += '<br>'; walk(c); }
        else { walk(c); }   // span a další z vloženého textu: jen obsah
      });
    })(el);
    return out.replace(/(<br>)+$/, '').trim();
  }

  /* ───────── rám se stránkou ───────── */
  var EDIT_CSS =
    '[data-ek]{outline:2px dashed transparent;outline-offset:3px;border-radius:4px;transition:outline-color .15s;cursor:text}' +
    '[data-ek]:hover{outline-color:#F29A7A}' +
    '[data-ek]:focus{outline:2px solid #245B63;background:rgba(246,214,109,.2)}' +
    'img[data-ei]{cursor:pointer}' +
    'img[data-ei]:hover{outline:4px solid #F29A7A;outline-offset:-4px}' +
    'img.is-vybrany{outline:4px solid #245B63!important;outline-offset:-4px}' +
    '[data-novinky] .post{cursor:default}' +
    '*{scroll-behavior:auto!important}';

  function nactiStranku(soubor) {
    aktualniStranka = soubor;
    $('nacitani').hidden = false;
    var znacka = 'editor=' + Date.now();
    frame.src = '../' + soubor + '?' + znacka;
    // upravit stránku hned, jak je načtený obsah – nečekat na fonty a obrázky (událost load)
    (function cekej(i) {
      var d; try { d = frame.contentDocument; } catch (e) { d = null; }
      if (d && d.location.href.indexOf(znacka) > -1 && d.readyState !== 'loading' && d.body) { priNacteni(); }
      else if (i < 400) setTimeout(function () { cekej(i + 1); }, 40);
    })(0);
  }

  function renderNovinky(d) {
    if (!state.novinky) return;
    d.querySelectorAll('[data-novinky]').forEach(function (box) {
      var domu = box.getAttribute('data-novinky') === '3';
      var seznam = domu ? state.novinky.slice(0, 3) : state.novinky;
      box.innerHTML = seznam.map(function (n) {
        var vnitrek = '<span class="post__date">' + esc(n.d) + '</span><h3>' + esc(n.t) + '</h3><p>' + (n.p || '') + '</p>';
        return domu ? '<a class="post" href="aktuality.html#novinky">' + vnitrek + '</a>' : '<article class="post">' + vnitrek + '</article>';
      }).join('');
    });
  }

  function pouzijNepublikovane(d) {
    Object.keys(state.texts).forEach(function (k) {
      d.querySelectorAll('[data-ek="' + k + '"]').forEach(function (el) {
        if (cistyHtml(el) !== state.texts[k]) el.innerHTML = state.texts[k];
      });
    });
    Object.keys(state.images).forEach(function (k) {
      d.querySelectorAll('img[data-ei="' + k + '"]').forEach(function (img) {
        img.removeAttribute('srcset');
        img.src = nahledy[k] || ('../' + state.images[k]);
      });
    });
    Object.keys(state.alts).forEach(function (k) {
      d.querySelectorAll('img[data-ei="' + k + '"]').forEach(function (img) { img.alt = state.alts[k]; });
    });
    renderNovinky(d);
  }

  function priNacteni() {
    var d = frame.contentDocument;
    if (!d || !d.body || d.__upraveno) return;
    d.__upraveno = true;
    $('nacitani').hidden = true;
    var st = d.createElement('style'); st.textContent = EDIT_CSS; d.head.appendChild(st);

    d.querySelectorAll('img[data-ei]').forEach(function (img) {
      var k = img.getAttribute('data-ei');
      if (!(k in puvodniSrc)) puvodniSrc[k] = img.getAttribute('src');
    });
    pouzijNepublikovane(d);

    d.querySelectorAll('[data-ek]').forEach(function (el) { el.contentEditable = 'true'; el.spellcheck = true; });

    // odkazy a formuláře uvnitř náhledu nikam nevedou
    d.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a');
      if (a) e.preventDefault();
      var img = e.target.closest && e.target.closest('img[data-ei]');
      if (img) vyberObrazek(img);
    }, true);
    d.addEventListener('submit', function (e) { e.preventDefault(); }, true);

    d.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.target.closest && e.target.closest('[data-ek]')) {
        e.preventDefault(); d.execCommand('insertLineBreak');
      }
    });
    d.addEventListener('paste', function (e) {
      if (!(e.target.closest && e.target.closest('[data-ek]'))) return;
      e.preventDefault();
      var t = (e.clipboardData || window.clipboardData).getData('text/plain').replace(/\r?\n+/g, ' ');
      d.execCommand('insertText', false, t);
    });
    d.addEventListener('input', function (e) { zapisText(e.target.closest && e.target.closest('[data-ek]')); });

    var cekej;
    function plovouci() {
      clearTimeout(cekej);
      cekej = setTimeout(function () {
        var s = d.getSelection();
        var tb = $('ftb');
        if (!s || s.isCollapsed || !s.anchorNode) { tb.hidden = true; return; }
        var uzel = s.anchorNode.nodeType === 1 ? s.anchorNode : s.anchorNode.parentElement;
        if (!uzel || !uzel.closest('[data-ek]')) { tb.hidden = true; return; }
        var r = s.getRangeAt(0).getBoundingClientRect(), f = frame.getBoundingClientRect();
        tb.hidden = false;
        tb.style.left = Math.max(8, f.left + r.left + r.width / 2 - tb.offsetWidth / 2) + 'px';
        tb.style.top = Math.max(8, f.top + r.top - tb.offsetHeight - 8) + 'px';
      }, 60);
    }
    d.addEventListener('mouseup', plovouci);
    d.addEventListener('keyup', plovouci);
    d.addEventListener('scroll', function () { $('ftb').hidden = true; }, true);
    $('obrPanel').hidden = true; vybranyObrazek = null;
  }

  function zapisText(el) {
    if (!el) return;
    var k = el.getAttribute('data-ek'), html = cistyHtml(el), d = frame.contentDocument;
    state.texts[k] = html;
    d.querySelectorAll('[data-ek="' + k + '"]').forEach(function (o) {
      if (o !== el && cistyHtml(o) !== html) o.innerHTML = html;
    });
    zmena();
  }

  // plovoucí lišta
  $('ftb').addEventListener('mousedown', function (e) { e.preventDefault(); });
  $('ftb').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var d = frame.contentDocument, cmd = b.dataset.cmd;
    var el = d.activeElement && d.activeElement.closest ? d.activeElement.closest('[data-ek]') : null;
    if (cmd === 'link') {
      var s = d.getSelection(), range = s.rangeCount ? s.getRangeAt(0).cloneRange() : null;
      var url = window.prompt('Adresa odkazu (např. https://… , mailto:… , tel:… nebo zapis.html):', 'https://');
      if (!url || url === 'https://') return;
      if (range) { s.removeAllRanges(); s.addRange(range); }
      d.execCommand('createLink', false, url.trim());
    } else {
      d.execCommand(cmd, false, null);
    }
    if (el) zapisText(el);
    $('ftb').hidden = true;
  });

  /* ───────── fotky ───────── */
  function vyberObrazek(img) {
    var d = frame.contentDocument;
    d.querySelectorAll('img.is-vybrany').forEach(function (o) { o.classList.remove('is-vybrany'); });
    img.classList.add('is-vybrany');
    vybranyObrazek = img.getAttribute('data-ei');
    $('obrNahled').src = img.currentSrc || img.src;
    $('obrAlt').value = img.getAttribute('alt') || '';
    $('obrPanel').hidden = false;
    prepniTab('upravy');
  }
  function vsechnyObrazky(k) { return frame.contentDocument.querySelectorAll('img[data-ei="' + k + '"]'); }

  $('obrAlt').addEventListener('input', function () {
    if (!vybranyObrazek) return;
    state.alts[vybranyObrazek] = this.value;
    var v = this.value;
    vsechnyObrazky(vybranyObrazek).forEach(function (i) { i.alt = v; });
    zmena();
  });
  $('obrVratit').addEventListener('click', function () {
    if (!vybranyObrazek) return;
    var k = vybranyObrazek;
    delete state.images[k]; delete state.alts[k]; delete nahledy[k];
    vsechnyObrazky(k).forEach(function (i) { i.src = '../' + puvodniSrc[k]; });
    $('obrNahled').src = '../' + puvodniSrc[k];
    zmena();
  });
  $('obrSoubor').addEventListener('change', function () {
    var f = this.files[0]; this.value = '';
    if (!f || !vybranyObrazek) return;
    var k = vybranyObrazek;
    zmensiFotku(f).then(function (v) {
      var cesta = 'assets/img/nahrane/' + Date.now().toString(36) + '-' + v.nazev;
      soubory[cesta] = v.base64; nahledy[k] = v.dataUrl; state.images[k] = cesta;
      vsechnyObrazky(k).forEach(function (i) { i.removeAttribute('srcset'); i.src = v.dataUrl; });
      $('obrNahled').src = v.dataUrl;
      zmena();
    }).catch(function () { hlaska('Tuto fotku se nepodařilo načíst. Zkuste JPG nebo PNG.', true); });
  });
  function zmensiFotku(file) {
    return new Promise(function (ok, ne) {
      var url = URL.createObjectURL(file), im = new Image();
      im.onload = function () {
        var MAX = 1600, w = im.naturalWidth, h = im.naturalHeight, s = Math.min(1, MAX / w);
        var c = document.createElement('canvas'); c.width = Math.round(w * s); c.height = Math.round(h * s);
        c.getContext('2d').drawImage(im, 0, 0, c.width, c.height);
        var png = file.type === 'image/png';
        var dataUrl = c.toDataURL(png ? 'image/png' : 'image/jpeg', 0.86);
        URL.revokeObjectURL(url);
        var zaklad = (file.name || 'foto').replace(/\.[^.]+$/, '').toLowerCase()
          .normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'foto';
        ok({ dataUrl: dataUrl, base64: dataUrl.split(',')[1], nazev: zaklad + (png ? '.png' : '.jpg') });
      };
      im.onerror = ne; im.src = url;
    });
  }

  /* ───────── aktuality ───────── */
  function plainZHtml(p) {
    var t = document.createElement('div'); t.innerHTML = String(p || '').replace(/<br\s*\/?>/gi, '\n');
    return t.textContent;
  }
  function htmlZPlain(t) { return esc(t).replace(/\n/g, '<br>'); }
  function dnes() { var n = new Date(); return n.getDate() + '. ' + (n.getMonth() + 1) + '. ' + n.getFullYear(); }

  function vychoziNovinky() {
    return fetch('../aktuality.html?x=' + Date.now()).then(function (r) { return r.text(); }).then(function (h) {
      var d = new DOMParser().parseFromString(h, 'text/html');
      return Array.prototype.map.call(d.querySelectorAll('[data-novinky="all"] .post'), function (a) {
        return {
          d: (a.querySelector('.post__date') || {}).textContent || '',
          t: (a.querySelector('h3') || {}).textContent || '',
          p: htmlZPlain((a.querySelector('p') || {}).textContent || '')
        };
      });
    });
  }
  function zajistiNovinky() {
    if (state.novinky) return Promise.resolve();
    return vychoziNovinky().then(function (n) {
      state.novinky = n;
      // výchozí aktuality patří do výchozího stavu, jinak by otevření záložky hlásilo „změny“
      var zaklad = JSON.parse(puvodniStav); zaklad.novinky = JSON.parse(JSON.stringify(n));
      puvodniStav = JSON.stringify(zaklad);
    });
  }
  function kresliAktuality() {
    var box = $('aktualityList'); box.innerHTML = '';
    (state.novinky || []).forEach(function (n, i, arr) {
      var w = document.createElement('div'); w.className = 'akt';
      w.innerHTML =
        '<label>Datum</label><input type="text" data-f="d" value="' + esc(n.d) + '">' +
        '<label>Nadpis</label><input type="text" data-f="t" value="' + esc(n.t) + '">' +
        '<label>Text</label><textarea data-f="p">' + esc(plainZHtml(n.p)) + '</textarea>' +
        '<div class="akt__tl"><button type="button" data-a="nahoru"' + (i === 0 ? ' disabled' : '') + '>↑ Výš</button>' +
        '<button type="button" data-a="dolu"' + (i === arr.length - 1 ? ' disabled' : '') + '>↓ Níž</button>' +
        '<button type="button" class="smazat" data-a="smazat">Smazat</button></div>';
      w.addEventListener('input', function (e) {
        var f = e.target.dataset.f; if (!f) return;
        n[f] = f === 'p' ? htmlZPlain(e.target.value) : e.target.value;
        renderNovinky(frame.contentDocument); zmena();
      });
      w.addEventListener('click', function (e) {
        var a = e.target.dataset.a; if (!a) return;
        if (a === 'smazat') { if (!confirm('Opravdu smazat aktualitu „' + (n.t || '') + '“?')) return; state.novinky.splice(i, 1); }
        if (a === 'nahoru') { state.novinky.splice(i - 1, 0, state.novinky.splice(i, 1)[0]); }
        if (a === 'dolu') { state.novinky.splice(i + 1, 0, state.novinky.splice(i, 1)[0]); }
        kresliAktuality(); renderNovinky(frame.contentDocument); zmena();
      });
      box.appendChild(w);
    });
    if (!(state.novinky || []).length) box.innerHTML = '<p class="drobne">Zatím žádné aktuality.</p>';
  }
  $('btnNovaAktualita').addEventListener('click', function () {
    zajistiNovinky().then(function () {
      state.novinky.unshift({ d: dnes(), t: 'Nadpis aktuality', p: '' });
      kresliAktuality(); renderNovinky(frame.contentDocument); zmena();
      var t = $('aktualityList').querySelector('input[data-f="t"]'); if (t) { t.focus(); t.select(); }
    });
  });

  /* ───────── záložky, zařízení, stránky ───────── */
  function prepniTab(nazev) {
    document.querySelectorAll('.panel__tabs button').forEach(function (b) { b.classList.toggle('is-on', b.dataset.tab === nazev); });
    document.querySelectorAll('.panel__body').forEach(function (p) { p.hidden = p.dataset.pane !== nazev; });
    if (nazev === 'aktuality') zajistiNovinky().then(kresliAktuality);
  }
  document.querySelector('.panel__tabs').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (b) prepniTab(b.dataset.tab);
  });
  document.querySelector('.bar__dev').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    document.querySelectorAll('.bar__dev button').forEach(function (x) { x.classList.toggle('is-on', x === b); });
    frame.style.width = b.dataset.w;
    $('ramec').parentNode.classList.toggle('is-narrow', b.dataset.w !== '100%');
  });
  STRANKY.forEach(function (s) {
    var o = document.createElement('option'); o.value = s[0]; o.textContent = s[1]; $('stranka').appendChild(o);
  });
  $('stranka').addEventListener('change', function () { nactiStranku(this.value); });
  frame.addEventListener('load', priNacteni);

  $('btnPublikovat').addEventListener('click', publikovat);
  $('btnZahodit').addEventListener('click', function () {
    if (jeZmena() && !confirm('Opravdu zahodit všechny neuložené změny?')) return;
    start();
  });
  window.addEventListener('beforeunload', function (e) {
    if (!$('work').hidden && jeZmena()) { e.preventDefault(); e.returnValue = ''; }
  });

  /* ───────── start a přihlášení ───────── */
  function start() {
    return nactiObsah().then(function (c) {
      state = { texts: c.texts || {}, images: c.images || {}, alts: c.alts || {}, novinky: Array.isArray(c.novinky) ? c.novinky : null };
      puvodniStav = JSON.stringify(JSON.parse(jsonStav()));
      soubory = {}; nahledy = {};
      $('login').hidden = true; $('bar').hidden = false; $('work').hidden = false;
      obnovStav(); prepniTab('upravy');
      nactiStranku($('stranka').value || 'index.html');
    });
  }
  function prihlasit() {
    var k = $('klic').value.trim(), chyba = $('loginChyba');
    chyba.textContent = '';
    if (!k) { chyba.textContent = 'Vložte přístupový klíč.'; return; }
    token = k; rezim = 'github';
    $('btnPrihlasit').disabled = true;
    gh('').then(function (r) {
      if (r.permissions && r.permissions.push === false) throw new Error('Klíč nemá právo zapisovat do repozitáře.');
      try { localStorage.setItem('msz_token', k); } catch (e) { /* soukromé okno */ }
      return start();
    }).catch(function (e) {
      chyba.textContent = e.message || 'Přihlášení se nezdařilo.';
    }).then(function () { $('btnPrihlasit').disabled = false; });
  }
  $('btnPrihlasit').addEventListener('click', prihlasit);
  $('klic').addEventListener('keydown', function (e) { if (e.key === 'Enter') prihlasit(); });
  $('btnOffline').addEventListener('click', function () { rezim = 'offline'; token = ''; start(); });

  try { var ulozeny = localStorage.getItem('msz_token'); if (ulozeny) { $('klic').value = ulozeny; } } catch (e) { /* nic */ }
  window.__editor = { state: function () { return state; }, jsonStav: jsonStav, zapisText: zapisText };
})();
