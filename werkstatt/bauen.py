#!/usr/bin/env python3
"""Baut die Tools der Eulenkiste aus den Originalen der Lehrerin.

  werkstatt/originale/gluecksrad.html  ->  gluecksrad/index.html
  werkstatt/originale/tagesfolie.html  ->  tagesfolie/index.html
  werkstatt/originale/otterteich.html  ->  otterteich/index.html
  werkstatt/originale/pinnwand.html    ->  pinnwand/index.html

Neue Version eines Tools: Datei in werkstatt/originale/ ersetzen und
  python3 werkstatt/bauen.py
ausführen. Jede Änderung ersetzt eine genau festgelegte Textstelle. Hat sich die
Stelle im Original verändert, bricht das Skript mit «Anzahl 0 statt 1» ab; dann
die Stelle hier anpassen (die Absicht steht jeweils im Kommentar).
"""
import os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(HIER)


class Bau:
    def __init__(self, name):
        self.name = name
        self.s = open(os.path.join(HIER, 'originale', name + '.html'), encoding='utf-8').read()

    def rep(self, alt, neu, anzahl=1):
        n = self.s.count(alt)
        if n != anzahl:
            sys.exit(f'{self.name}: Anzahl {n} statt {anzahl}: {alt[:90]!r}')
        self.s = self.s.replace(alt, neu)

    def rex(self, muster, neu, anzahl=1):
        treffer = re.findall(muster, self.s)
        if len(treffer) != anzahl:
            sys.exit(f'{self.name}: Anzahl {len(treffer)} statt {anzahl}: {muster[:90]!r}')
        self.s = re.sub(muster, lambda m: neu, self.s)

    def schreibe(self, ziel):
        pfad = os.path.join(WURZEL, ziel)
        os.makedirs(os.path.dirname(pfad), exist_ok=True)
        alt = open(pfad, encoding='utf-8').read() if os.path.exists(pfad) else None
        open(pfad, 'w', encoding='utf-8').write(self.s)
        print(f'{ziel}: {"gleich" if alt == self.s else "neu geschrieben"}')


# Gemeinsam: Schriften aus der Eulenkiste statt von Google (keine Daten an fremde Dienste)
def schriften(b):
    if '<link rel="preconnect" href="https://fonts.googleapis.com">' in b.s:
        b.rep('<link rel="preconnect" href="https://fonts.googleapis.com">\n', '')
    b.rex(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">',
          '<link rel="stylesheet" href="../schriften/schriften.css">\n<meta name="referrer" content="no-referrer">\n<link rel="icon" type="image/png" href="../eulenkiste-icon.png">')


# Knopf oben links zurück zur Eulenkiste: Pfeil und das runde Eulen-Logo
ZURUECK = ('<a class="lk-back" href="../" title="Zurück zur Eulenkiste" aria-label="Zurück zur Eulenkiste">'
           '<span aria-hidden="true">←</span><img src="../eulenkiste.webp" alt="" width="36" height="36"></a>')
ZURUECK_CSS = ('a.lk-back{display:inline-flex;align-items:center;gap:6px;padding:3px 4px 3px 13px;border-radius:999px;background:#fff;'
               'color:#1f2421;text-decoration:none;font:700 19px/1 system-ui,sans-serif;box-shadow:0 4px 14px rgba(63,120,168,.2);flex:none}'
               'a.lk-back:hover{box-shadow:0 6px 18px rgba(63,120,168,.3)}a.lk-back img{width:36px;height:36px;display:block}')

# ---------------------------------------------------------------- Glücksrad
g = Bau('gluecksrad')
schriften(g)
# Knopf zurück zur Eulenkiste, vor «Ton an»
g.rep('''  <header>
    <div>
      <div class="eyebrow">Wer ist dran? Was machen wir?</div>
      <h1>Glücksrad</h1>
    </div>
    <div class="tools">''', '''  <header>
    ''' + ZURUECK + '''
    <div class="tools">''')
# Titel in der Mitte über dem Rad
g.rep('''    <section class="card wheel-card">
''', '''    <section class="card wheel-card">
      <div class="titel-mitte"><div class="eyebrow">Wer ist dran? Was machen wir?</div><h1>Glücksrad</h1></div>
''')
g.rep('header{display:flex;align-items:flex-end;', '.titel-mitte{text-align:center;margin-bottom:-4px}\nheader{display:flex;align-items:center;')
g.rep('.pill:hover{', ZURUECK_CSS + '\n.pill:hover{')
g.schreibe('gluecksrad/index.html')

# ---------------------------------------------------------------- Tagesfolie
# Die Tagesfolie entsteht in der Klassenkiste (Repo knobelnest, werkstatt/einbau/tagesfolie/). Original hier = deren
# fertige tagesfolie.html. Ohne Klassenkiste läuft sie ohne Konto; hier kommen nur die Eulenkiste-Sachen dazu.
t = Bau('tagesfolie')
t.rep('<link rel="stylesheet" href="schriften/schriften.css">',
      '<link rel="stylesheet" href="../schriften/schriften.css">\n<link rel="icon" type="image/png" href="../eulenkiste-icon.png">')
# Knopf zurück zur Eulenkiste, ganz links in der oberen Leiste
t.rep('    <button class="pill kn-back" id="knBack" aria-label="Zurück zur Klassenkiste" title="Zurück zur Klassenkiste" style="display:none"><span aria-hidden="true">←</span><img src="bilder/eule.webp" alt="" width="34" height="34"></button>',
      '    ' + ZURUECK)

# Kein Konto, keine Datenbank: alles bleibt auf diesem Gerät (auch wenn die Seite in Claude geöffnet würde)
t.rep('    if (!window.claude?.use) return;\n',
      '    return; // Eulenkiste: kein Konto, keine Datenbank – alles bleibt auf diesem Gerät\n')

# Arbeitsstand und Otterteich gibt es nur im Knobelnest: grau in der Leiste, mit Hinweis beim Darüberfahren oder Antippen
STAND_ICON = ('<rect x="4" y="6" width="24" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="2.4"/>'
              '<path d="M4 13h24M12 6v20M20 6v20" stroke="currentColor" stroke-width="2"/>'
              '<circle cx="8" cy="19" r="2" fill="currentColor"/><circle cx="24" cy="22" r="2" fill="currentColor"/>')
HEFT_ICON = ('<rect x="7" y="4" width="18" height="24" rx="2.5" fill="none" stroke="currentColor" stroke-width="2.4"/>'
             '<path d="M11 10h10M11 15h10M11 20h6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>')
OTTER_ICON = ('<ellipse cx="16" cy="22" rx="12" ry="5" fill="none" stroke="currentColor" stroke-width="2.4"/>'
              '<circle cx="16" cy="12" r="6" fill="none" stroke="currentColor" stroke-width="2.4"/>'
              '<circle cx="11" cy="7.5" r="1.8" fill="currentColor"/><circle cx="21" cy="7.5" r="1.8" fill="currentColor"/>'
              '<circle cx="16" cy="13.5" r="1.3" fill="currentColor"/>')
t.rep('''$("#dock").innerHTML = DOCK.map(k => k === "|" ? `<span class="sep"></span>` : `<button data-add="${k}"><svg viewBox="0 0 32 32" aria-hidden="true">${TYPES[k].icon}</svg>${TYPES[k].lab}</button>`).join("");''',
      '''$("#dock").innerHTML = DOCK.map(k => k === "|" ? `<span class="sep"></span>` : `<button data-add="${k}"><svg viewBox="0 0 32 32" aria-hidden="true">${TYPES[k].icon}</svg>${TYPES[k].lab}</button>`).join("")
  + `<span class="sep"></span>` + Object.entries(KN_NUR).map(([k, [lab, icon]]) => `<button class="locked" data-locked="${k}" aria-disabled="true" aria-label="${lab}: ${KN_TIP}"><svg viewBox="0 0 32 32" aria-hidden="true">${icon}</svg>${lab}</button>`).join("");
// Nur im Knobelnest: Hinweis über dem grauen Knopf
(() => {
  const tip = document.createElement("div"); tip.className = "kn-tip"; tip.setAttribute("role", "tooltip"); APP.appendChild(tip);
  let zu = 0;
  const zeige = (b, text) => {
    clearTimeout(zu);
    tip.innerHTML = text ? `<b>💡 ${esc(text)}</b>` : `<b>🔒 ${esc(KN_TIP)}</b>` + (KN_LINK ? ` <a href="${esc(KN_LINK)}" target="_blank" rel="noopener">Mehr erfahren</a>` : "");
    tip.classList.add("show");
    const r = b.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
    tip.style.left = Math.max(8, Math.min(innerWidth - w - 8, r.left + r.width / 2 - w / 2)) + "px";
    tip.style.top = Math.max(8, r.top - h - 10) + "px";
  };
  const weg = () => { zu = setTimeout(() => tip.classList.remove("show"), 250); };
  $("#dock").querySelectorAll("[data-locked]").forEach(b => {
    b.addEventListener("mouseenter", () => zeige(b));
    b.addEventListener("mouseleave", weg);
    b.addEventListener("focus", () => zeige(b));
    b.addEventListener("blur", weg);
    b.addEventListener("click", () => { zeige(b); clearTimeout(zu); zu = setTimeout(() => tip.classList.remove("show"), 3500); });
  });
  // Zufallsname und Gruppen funktionieren hier auch, im Knobelnest gibt es aber mehr: Hinweis beim Darüberfahren
  $("#dock").querySelectorAll('[data-add="random"],[data-add="groups"]').forEach(b => {
    b.addEventListener("mouseenter", () => zeige(b, KN_KLASSE));
    b.addEventListener("mouseleave", weg);
  });
  tip.addEventListener("mouseenter", () => clearTimeout(zu));
  tip.addEventListener("mouseleave", weg);
  $("#dock").addEventListener("scroll", () => tip.classList.remove("show"), { passive: true });
})();''')
t.rep('const DOCK = [',
      '''// Nur im Knobelnest erhältlich (grau in der Leiste). KN_LINK: später die Seite auf primarschuleulchen.com, wo man den Zugang bekommt
const KN_NUR = { stand: ["Arbeitsstand", `''' + STAND_ICON + '''`], otter: ["Lautstärke", `''' + OTTER_ICON + '''`], heft: ["Hausaufgaben", `''' + HEFT_ICON + '''`] };
const KN_TIP = "Nur in der Klassenkiste – jetzt anmelden und freischalten";
const KN_LINK = "";
const KN_KLASSE = "In der Klassenkiste ist deine Klassenliste fix eingetragen, und du kannst Vorlagen speichern.";
const DOCK = [''')
t.rep('.dock .sep{width:1px', '''.dock button.locked{color:#9aa39d;cursor:help}
.dock button.locked svg{opacity:.55}
.dock button.locked:hover{background:#f1f2ef}
.kn-tip{position:fixed;left:0;top:0;z-index:300;max-width:250px;background:#1f2421;color:#fff;border-radius:12px;padding:9px 13px;font-size:13px;line-height:1.35;box-shadow:0 6px 20px rgba(0,0,0,.2);opacity:0;pointer-events:none;transition:opacity .15s}
.kn-tip.show{opacity:1;pointer-events:auto}
.kn-tip a{color:#bfe3fb;font-weight:800}
''' + ZURUECK_CSS + '''
.dock .sep{width:1px''')
# Zweiter Start-Bildschirm heisst «Halbklasse» und ist so angeordnet, wie die Lehrerin ihn eingerichtet hat
t.rep('''      { id: "s-lektion", name: "10 – 12 Uhr", bg: "", widgets: [
        W("title", 24, 0, 42, 18, { text: "10 – 12 Uhr", color: TITLE_COLORS[2] }),
        W("date", 76, 1, 15, 26),
        W("list", 4, 24, 28, 40, { heading: "Deutsch", items: mkItems(["Lesekartei","Arbeitsheft S. 24"]) }),
        W("list", 35, 24, 28, 40, { heading: "Mathe", items: mkItems(["Plusaufgaben bis 100","Rechenkartei"]) }),
        W("material", 4, 60, 40, 30, { keys: ["bleistift","radiergummi","lineal","heft"] }),
        W("timer", 68, 34, 28, 28, { total: 1200, left: 1200 }),
        W("traffic", 86, 66, 7, 26)
      ]}''', '''      { id: "s-lektion", name: "Halbklasse", bg: "", widgets: [
        W("title", 26, 4, 42, 18, { text: "Halbklasse" }),
        W("list", 5, 28, 29, 22, { heading: "Deutsch", items: mkItems(["Lesekartei","Arbeitsheft S. 24"]) }),
        W("list", 36, 28, 31, 22, { heading: "Mathe", items: mkItems(["Plusaufgaben bis 100","Rechenkartei"]) }),
        W("date", 71, 26, 15, 26),
        W("material", 5, 61, 39, 27, { keys: ["bleistift","radiergummi","lineal","heft"] }),
        W("timer", 46.5, 62, 27.5, 22.5, { total: 1200, left: 1200 }),
        W("traffic", 77, 63, 7, 21)
      ]}''')
t.rep('  s.bgs = s.bgs.map(b => typeof b === "string" ? { src: b, pal: null } : b);',
      '  s.bgs = s.bgs.map(b => typeof b === "string" ? { src: b, pal: null } : b);\n  s.screens.forEach(sc => { if (sc.id === "s-lektion" && sc.name === "10 – 12 Uhr") sc.name = "Halbklasse"; }); // Eulenkiste: Vorlage umbenannt')
# Musik: kein YouTube (keine fremden Dienste), eigene Datei nur klein (Speicher dieses Geräts)
t.rep('''    <h3 class="sh3">YouTube-Link</h3><div class="addrow"><input type="text" id="mus-yt" placeholder="https://www.youtube.com/watch?v=…" aria-label="YouTube-Link"><button class="sbtn rose" data-myt>Übernehmen</button></div>
    <h3 class="sh3">Oder Audiodatei hochladen</h3>''', '''    <h3 class="sh3">Audiodatei hochladen</h3><p class="hint">Höchstens 3 MB, sie wird auf diesem Gerät gespeichert.</p>''')
t.rep('if (f.size > 6e6) {', 'if (f.size > 3e6) {')
t.schreibe('tagesfolie/index.html')

# ---------------------------------------------------------------- Otterteich (Lautstärkenregler)
o = Bau('otterteich')
# Das Original lädt nichts nach (Schriften eingebaut). Nur das Eulen-Logo aus der Eulenkiste zusätzlich erlauben.
# Die gespeicherte Datei beginnt mit einer Hülle aus Claude (eigene <head>/<body>): weg damit, sonst ignoriert der Browser die Sicherheitsregeln
o.rex(r'^<!doctype html><html><head><meta charset=utf8>.*?</style></head><body>\n', '')
o.rep("img-src data:;", "img-src data: 'self';")
o.rep('<title>Otterteich</title>', '<title>Lautstärkenregler – Otterteich</title>\n<link rel="icon" type="image/png" href="../eulenkiste-icon.png">')
# Knopf oben links zurück zur Eulenkiste; der Otter-Zähler rutscht darunter
o.rep('<canvas id="cv" aria-label="Animierter Otterteich"></canvas>',
      '<canvas id="cv" aria-label="Animierter Otterteich"></canvas>\n<div class="ot-back">' + ZURUECK + '</div>')
o.rep('.pill{background:var(--pill);', ZURUECK_CSS + '\n.ot-back{position:fixed;z-index:35;top:max(14px,env(safe-area-inset-top,0px));left:max(14px,env(safe-area-inset-left,0px))}'
      '\n.count{margin-top:56px}\n.pill{background:var(--pill);')
o.schreibe('otterteich/index.html')

# ---------------------------------------------------------------- Pinnwand (Klassen-Pinnwand)
# Dieselbe Pinnwand gibt es in der Klassenkiste (Repo knobelnest, werkstatt/einbau/pinnwand/). Die Korrekturen
# unter «Gemeinsam mit der Klassenkiste» stehen dort in pin_fixes.py: bei Änderungen beide anpassen.
p = Bau('pinnwand')
schriften(p)
p.rep('<title>Klassen-Pinnwand</title>', '<title>Klassen-Pinnwand – Eulenkiste</title>')
# Knopf zurück zur Eulenkiste, links vom Titel
p.rep('    <h1>Klassen-Pinnwand</h1>', '    ' + ZURUECK + '\n    <h1>Klassen-Pinnwand</h1>')
# Kein Konto, keine Datenbank: die Pinnwand speichert alles im Browser dieses Geräts (localStorage)
p.rep('/* ---------- Start ---------- */', """/* ---------- Eulenkiste: Speicher nur auf diesem Gerät ---------- */
if (!window.claude || !window.claude.use) {
  const KEY = "eulenkiste-pinnwand";
  let D; try { D = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch { D = {}; }
  for (const c of ["boards", "ideas", "settings", "votes"]) if (!D[c] || typeof D[c] !== "object") D[c] = {};
  const subs = new Set(), copy = v => JSON.parse(JSON.stringify(v));
  const snapColl = c => ({ docs: Object.keys(D[c]).map(id => ({ id, exists: true, data: () => copy(D[c][id]) })) });
  const snapDoc = (c, id) => ({ id, exists: D[c][id] != null, data: () => D[c][id] == null ? null : copy(D[c][id]) });
  const save = () => {
    try { localStorage.setItem(KEY, JSON.stringify(D)); }
    catch { const e = new Error("voll"); e.code = "quota_exceeded"; throw e; }
    subs.forEach(f => f()); // sofort: eine neue Pinnwand muss schon da sein, wenn sie geöffnet wird
  };
  const watch = f => { subs.add(f); setTimeout(f, 0); return () => subs.delete(f); };
  const merge = (a, b) => { const r = copy(a || {}); for (const k in b) r[k] = b[k] && typeof b[k] === "object" && !Array.isArray(b[k]) && r[k] && typeof r[k] === "object" && !Array.isArray(r[k]) ? merge(r[k], b[k]) : b[k]; return r; };
  const db = {
    collection: c => ({
      add: async obj => { const id = "i" + Date.now().toString(36) + Math.random().toString(36).slice(2, 7); D[c][id] = copy(obj); save(); return { id }; },
      onSnapshot: cb => watch(() => cb(snapColl(c)))
    }),
    doc: path => { const [c, id] = String(path).split("/"); return {
      get: async () => snapDoc(c, id),
      set: async obj => { D[c][id] = copy(obj); save(); },
      update: async patch => { D[c][id] = merge(D[c][id], patch); save(); },
      delete: async () => { delete D[c][id]; save(); },
      onSnapshot: cb => watch(() => cb(snapDoc(c, id)))
    }; }
  };
  window.claude = { use: async n => n === "db" ? db : n === "user" ? { me: async () => ({ id: "lp", isOwner: true, canEdit: true }) } : null };
}
/* ---------- Start ---------- */""")
p.rep('st.lastElementChild.textContent = S.live ? "Live" : "Vorschau – wird nicht gespeichert";',
      'st.lastElementChild.textContent = S.live ? "Auf diesem Gerät gespeichert" : "Wird geladen …";')
# Hinweis: Kinder an eigenen Geräten gibt es nur in der Klassenkiste
p.rep('    <span class="status" id="status"><i></i><span>Verbinde …</span></span>',
      '    <span class="status" id="status"><i></i><span>Verbinde …</span></span>\n'
      '    <a class="kk-hint" href="https://klassenkiste.primarschuleulchen.com/" target="_blank" rel="noopener" title="In der Klassenkiste schreiben und stimmen die Kinder an ihren eigenen Geräten mit.">🔒 Kinder an eigenen Geräten: nur in der Klassenkiste</a>')
p.rep('/* Erweiterungen */', '/* Erweiterungen */\n' + ZURUECK_CSS + '\nheader.top a.lk-back{margin-right:4px}'
      '\n.kk-hint{font-size:12.5px;font-weight:700;color:var(--muted);background:rgba(255,255,255,.75);padding:3px 10px;border-radius:999px;text-decoration:none}'
      '\n.kk-hint:hover{color:var(--ink)}\n@media (max-width:700px){.kk-hint{display:none}}')

# Gemeinsam mit der Klassenkiste (pin_fixes.py):
# a) Beim Tippen auf eine Einstellung springt die Seite nicht mehr nach oben:
#    vor dem Neuzeichnen die Scroll-Positionen (Seite und Seitenleiste) merken und danach wiederherstellen.
p.rep('''  $("#app").innerHTML = !S.board ?''', '''  const scrSame = window.__pwScr === S.board + "|" + S.view; window.__pwScr = S.board + "|" + S.view;
  const scrPath = el => { const p = []; while (el && el.id !== "app") { p.unshift([...el.parentNode.children].indexOf(el)); el = el.parentNode; } return p; };
  const scrKeep = [], scrY = scrollY; if (scrSame) document.querySelectorAll("#app *").forEach(el => { if (el.scrollTop > 0) scrKeep.push([scrPath(el), el.scrollTop]); });
  $("#app").innerHTML = !S.board ?''')
p.rep('''  for (const k in keep) { const el = document.getElementById(k); if (el) el.value = keep[k]; }''', '''  for (const k in keep) { const el = document.getElementById(k); if (el) el.value = keep[k]; }
  if (scrSame) {
    for (const [p, t] of scrKeep) { let el = $("#app"); for (const i of p) el = el && el.children[i]; if (el) el.scrollTop = t; }
    if (Math.abs(scrollY - scrY) > 1) scrollTo(0, scrY);
  }''')
# b) Grössere Schrift auf den Zetteln
p.rep('.note .txt{font-family:var(--hand);font-size:1.5rem;', '.note .txt{font-family:var(--hand);font-size:1.9rem;')
p.rep('#app[data-font="klar"] .note .txt{font-size:1.2rem}', '#app[data-font="klar"] .note .txt{font-size:1.55rem}')
p.rep('.present-on .note .txt{font-size:2rem}', '.present-on .note .txt{font-size:2.5rem}')
# Klassenkiste-Stil: Patrick Hand, helles Blau, Gold-Akzente ✦ ✧ ✦ (gleiche Datei wie in der Klassenkiste:
# knobelnest werkstatt/einbau/pinnwand/pin_stil.py; bei Änderungen beide anpassen). Die Eule steckt schon im Zurück-Knopf.
rep = p.rep; EULE = ''; SCHRIFT = ''
exec(open(os.path.join(HIER, 'pin_stil.py'), encoding='utf-8').read())
# Hinweis: eigene Vorlagen (bearbeiten, löschen, erstellen) gibt es in der Klassenkiste
p.rep('esc(t.icon) + " Erstellen"}</button></div></section>`;', '''esc(t.icon) + " Erstellen"}</button></div>
    <div class="vl-hint"><span class="vl-stern" aria-hidden="true">✦</span><p><b>Eigene Vorlagen?</b> In der Klassenkiste können Sie Vorlagen bearbeiten, löschen und eigene erstellen, dazu viele weitere Werkzeuge für Ihre Klasse.</p><a class="btn vl-btn" href="https://klassenkiste.primarschuleulchen.com/" target="_blank" rel="noopener">✦ Hol dir jetzt den Zugang</a></div></section>`;''')
p.schreibe('pinnwand/index.html')

# ---------------------------------------------------------------- Wort des Tages (Lernspiel)
w = Bau('wort-des-tages')
# Schrift und Eule sind im Original eingebaut. Die Eule oben links wird zum Knopf zurück zur Eulenkiste.
w.rex(r'<header class="kopf">\n    <img src="data:image/webp;base64,[^"]+"[^>]*>',
      '<header class="kopf">\n    ' + ZURUECK)
w.rep('<title>Wort des Tages</title>', '<title>Wort des Tages</title>\n<link rel="icon" type="image/png" href="../eulenkiste-icon.png">')
w.rep('.kopf img{width:46px;height:46px;flex:none}', ZURUECK_CSS + '\n.kopf .lk-back{box-shadow:none;background:var(--sky-soft)}')
w.rep('.kopf img{width:38px;height:38px}', '.kopf .lk-back img{width:30px;height:30px}')
w.schreibe('wort-des-tages/index.html')

# ---------------------------------------------------------------- Knobelspiele aus der Klassenkiste (Lernspiele)
# Die Spiele entstehen im Knobelnest (werkstatt/spiele/knobelspiele/bauen.py → knobelspiele/<spiel>.html).
# Neue Version: die Datei aus knobelspiele/ nach werkstatt/originale/spiele/ kopieren und dieses Skript laufen lassen.
# Hier laufen sie ohne Klassenkiste: Stand (Ton, Rekorde) nur im localStorage des Geräts, keine Sterne.
KNOBELSPIELE = ['rechen-rakete', 'uhr-lesen', 'kiosk', 'wort-raten', 'der-die-das', 'silben-puzzle',
                'bilderraetsel', 'eulen-weg', 'bilder-sudoku', 'wasser-weg',
                'zahlenmauer', 'kloetzli-turm', 'kisten-packen', 'laternen', 'schiebe-bild', 'geheimcode', 'irrgarten',
                'waage', 'spiegelbild', 'zahlen-pfad',
                'brueche', 'muster-reihe', 'lichtstrahl',
                # Englisch (eigener Ordner englisch/index.html): Kleiderschrank kommt aus knobelspiele/, Owl Town aus englisch/owl-town.html
                'kleiderschrank', 'owl-town']
# Zurück führt in die Knobelkiste (knobelkiste/index.html), zum Fach des Spiels
FACH = {'rechen-rakete': 'mathematik', 'uhr-lesen': 'mathematik', 'kiosk': 'mathematik', 'wort-raten': 'deutsch', 'der-die-das': 'deutsch',
        'silben-puzzle': 'deutsch', 'bilderraetsel': 'knobeln', 'eulen-weg': 'knobeln', 'bilder-sudoku': 'knobeln', 'wasser-weg': 'knobeln',
        'zahlenmauer': 'mathematik', 'kloetzli-turm': 'knobeln', 'kisten-packen': 'knobeln', 'laternen': 'knobeln',
        'schiebe-bild': 'knobeln', 'geheimcode': 'knobeln', 'irrgarten': 'knobeln',
        'waage': 'mathematik', 'spiegelbild': 'knobeln', 'zahlen-pfad': 'knobeln',
        'brueche': 'mathematik', 'muster-reihe': 'knobeln', 'lichtstrahl': 'knobeln',
        'kleiderschrank': 'englisch', 'owl-town': 'englisch'}
for name in KNOBELSPIELE:
    if FACH[name] == 'englisch':
        ZURUECK_SPIEL = ZURUECK.replace('href="../"', 'href="../englisch/"').replace('Zurück zur Eulenkiste', 'Zurück zur Englischkiste')
    else:
        ZURUECK_SPIEL = ZURUECK.replace('href="../"', 'href="../knobelkiste/#' + FACH[name] + '"').replace('Zurück zur Eulenkiste', 'Zurück zur Knobelkiste')
    k = Bau('spiele/' + name)
    # Startseite des Spiels: oben links der Knopf zurück zur Knobelkiste
    k.rep("""'<div class="top"><span style="flex:1"></span>' + sndBtn() + '</div><div class="kopf">""",
          """'<div class="top">""" + ZURUECK_SPIEL.replace("'", "\\'") + """<span style="flex:1"></span>' + sndBtn() + '</div><div class="kopf">""")
    if name in ('kleiderschrank', 'owl-town'):
        # Kleiderschrank und Owl Town haben eine eigene Startseite (Stufen-Pfad «pf-top»): dort auch der Zurück-Knopf
        k.rep("""'<div class="top pf-top"><span style="flex:1"></span>' + sndBtn() + '</div><div class="kopf">""",
              """'<div class="top pf-top">""" + ZURUECK_SPIEL.replace("'", "\\'") + """<span style="flex:1"></span>' + sndBtn() + '</div><div class="kopf">""")
        k.rep('.pf-top .pill{pointer-events:auto}', '.pf-top .pill,.pf-top .lk-back{pointer-events:auto}')
    k.rep('</style>', ZURUECK_CSS + '</style>\n<link rel="icon" type="image/png" href="../eulenkiste-icon.png">\n<meta name="referrer" content="no-referrer">')
    if name == 'owl-town':
        # Die 3D-Bibliothek (three.js, MIT-Lizenz) liegt lokal in bibliothek/three/ statt auf einem fremden Server
        k.rep('"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.min.js"', '"three":"../bibliothek/three/build/three.module.min.js"')
        k.rep('"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"', '"three/addons/":"../bibliothek/three/examples/jsm/"')
    k.schreibe('spiele/' + name + '.html')

# ---------------------------------------------------------------- Live-Quiz (aus der Klassenkiste, ohne Datenbank)
# Original = quiz.html der Klassenkiste (Repo knobelnest). Hier: Quiz erstellen und am Beamer spielen (Vorschau-Modus),
# nichts wird gespeichert (nur im Speicher der offenen Seite). Mitspielen per QR-Code, Speichern, Ordner der Kinder
# und KI gibt es nur in der Klassenkiste: Knöpfe zeigen dann einen Hinweis (kkNur).
q = Bau('quiz')
# Bilder und Schrift aus der Eulenkiste
q.rep('bilder/kacheln/quiz-buzzer.webp', 'quiz-buzzer.webp', 9)
q.rep('bilder/eule.webp', '../eulenkiste.webp', 3)
q.rep('url(schriften/patrick-hand.woff2)', 'url(../schriften/patrick-hand.woff2)')
q.rep('aria-label="Zurück zur Klassenkiste" title="Zurück zur Klassenkiste"', 'aria-label="Zurück zur Eulenkiste" title="Zurück zur Eulenkiste"', 2)
q.rep('<title>', '<link rel="icon" type="image/png" href="../eulenkiste-icon.png">\n<meta name="referrer" content="no-referrer">\n<title>')
# Ersatz für die Brücke der Klassenkiste: alles nur im Speicher dieser Seite
QUIZ_SHIM = r"""<script>
/* Eulenkiste: Ersatz für window.knQuiz der Klassenkiste. Nichts wird gespeichert, alles verschwindet beim Schliessen. */
(function () {
  var M = { liste: { list: [], ordner: [] }, quiz: {} }, kopie = function (x) { return JSON.parse(JSON.stringify(x)); };
  var nein = function () { return Promise.reject(new Error('Nur in der Klassenkiste')); };
  window.EK_QUIZ = {
    mode: 'teacher',
    list: function () { return Promise.resolve(kopie(M.liste)); },
    saveList: function (d) { M.liste = kopie(d); return Promise.resolve(); },
    load: function (id) { return Promise.resolve(M.quiz[id] ? kopie(M.quiz[id]) : null); },
    save: function (id, q) { M.quiz[id] = kopie(q); return Promise.resolve(); },
    remove: function (id) { delete M.quiz[id]; return Promise.resolve(); },
    back: function () { location.href = '../'; }, home: function () { location.href = '../'; },
    kidClasses: function () { return Promise.resolve([]); }, kidList: function () { return Promise.resolve([]); },
    kidGet: nein, kidSave: nein, kidDelete: nein, kidToggle: nein, kidNew: nein, kidMembers: nein,
    open: nein, host: nein, step: nein, close: nein, kick: nein, join: nein, state: nein, answer: nein,
    qr: nein, joinUrl: function () { return ''; }
  };
  window.addEventListener('beforeunload', function (e) { if (M.liste.list.length) { e.preventDefault(); e.returnValue = ''; } });
  // Hinweis: Diese Funktion gibt es nur in der Klassenkiste
  window.kkNur = function (was) {
    var d = document.getElementById('kkNur');
    if (!d) { d = document.createElement('div'); d.id = 'kkNur'; d.className = 'kk-nur'; document.body.appendChild(d);
      d.addEventListener('click', function (e) { if (e.target === d || e.target.closest('[data-zu]')) d.hidden = true; }); }
    d.innerHTML = '<div class="kk-nur-box" role="dialog" aria-label="Nur in der Klassenkiste"><b>🔒 ' + was + '</b>' +
      '<p>Das gibt es nur in der Klassenkiste. Dort spielen die Kinder mit ihren eigenen Geräten per QR-Code mit, deine Quiz bleiben gespeichert, und die KI erstellt Quiz aus Arbeitsblättern.</p>' +
      '<p class="klein">Hier in der Eulenkiste kannst du Quiz erstellen und am Beamer mit der Klasse spielen. Gespeichert wird nichts.</p>' +
      '<div class="kk-nur-kn"><a class="btn gold" href="https://klassenkiste.primarschuleulchen.com/" target="_blank" rel="noopener">Zur Klassenkiste ✦</a><button class="btn" data-zu>Schliessen</button></div></div>';
    d.hidden = false;
  };
})();
</script>
"""
q.rep('<script>\n(function () {\n  \'use strict\';\n  var B = null;', QUIZ_SHIM + '<script>\n(function () {\n  \'use strict\';\n  var B = null;')
q.rep("""  try { B = window.parent && window.parent !== window && window.parent.knQuiz; } catch (e) { B = null; }""", """  B = window.EK_QUIZ;""")
q.rep('</style>', """.kk-nur{position:fixed;inset:0;z-index:100;display:grid;place-items:center;padding:20px;background:rgba(31,36,33,.35)}
.kk-nur[hidden]{display:none}
.kk-nur-box{max-width:460px;background:#fff;border-radius:24px;padding:24px 26px;box-shadow:0 18px 50px rgba(0,0,0,.25);display:flex;flex-direction:column;gap:10px}
.kk-nur-box b{font-size:24px;font-weight:400}
.kk-nur-box .klein{color:var(--soft,#5f6963);font-size:16px}
.kk-nur-kn{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}
.btn.kk-zu{opacity:.75}
.eule-hinweis{margin:-6px 0 14px;padding:10px 16px;border-radius:16px;background:#fbf3dc;border:1.5px dashed #d6ad45;font-size:16px;color:#4a3d1a}
</style>""", 1)
# Ordner «Von den Kindern» gibt es hier nicht
q.rep(".concat([['kinder', '✦ Von den Kindern', null]])", '')
# Knöpfe: «Am Beamer spielen» (= Vorschau) statt Live; QR-Code und KI nur in der Klassenkiste
q.rep("""'<div class="qc-main"><button class="btn gold" data-a="live" data-id="' + h(x.id) + '"' + (x.n ? '' : ' disabled') + '>▶ Live spielen</button><button class="btn" data-a="vor" data-id="' + h(x.id) + '"' + (x.n ? '' : ' disabled') + '>👁 Vorschau</button></div>'""",
      """'<div class="qc-main"><button class="btn gold" data-a="vor" data-id="' + h(x.id) + '"' + (x.n ? '' : ' disabled') + '>▶ Am Beamer spielen</button><button class="btn kk-zu" data-a="live" data-id="' + h(x.id) + '">🔒 QR-Code</button></div>'""")
q.rep("""(B.mode === 'kid' ? '' : '<button class="btn gold" data-a="edLive">▶ Live spielen</button>')""",
      """'<button class="btn kk-zu" data-a="edLive">🔒 QR-Code</button>'""")
q.rep("""<button class="btn" data-a="edVor">👁 ' + (B.mode === 'kid' ? 'Ausprobieren' : 'Vorschau') + '</button>'""",
      """<button class="btn gold" data-a="edVor">▶ Am Beamer spielen</button>'""")
q.rep("""  ACT.live = async function (el) {""", """  ACT.live = async function (el) { return kkNur('Live spielen per QR-Code');""")
q.rep("""  ACT.edLive = async function () {""", """  ACT.edLive = async function () { return kkNur('Live spielen per QR-Code');""")
q.rep("""  ACT.kiOpen = function () {""", """  ACT.kiOpen = function () { return kkNur('Quiz mit KI erstellen');""")
q.rep("""'<button class="new ki" data-a="kiOpen"><span>✨</span>Mit KI erstellen<small class="muted">aus einem PDF oder Arbeitsblatt</small></button>'""",
      """'<button class="new ki kk-zu" data-a="kiOpen"><span>🔒</span>Mit KI erstellen<small class="muted">nur in der Klassenkiste</small></button>'""")
# Hinweis «gespeichert» passt hier nicht
q.rep("""(L.dirty ? 'wird gespeichert …' : '✓ gespeichert')""", """'nur bis zum Schliessen'""")
q.rep("'✓ gespeichert'", "'nur bis zum Schliessen'", 2)
# Willkommen: was hier geht und was die Klassenkiste kann
q.rep("""<h1>Live-Quiz mit der ganzen Klasse</h1>' +
      '<p>Fragen erstellen, an der Wandtafel starten, die Kinder scannen den QR-Code und spielen alle gleichzeitig mit.</p></div></div>'""",
      """<h1>Quiz mit der ganzen Klasse</h1>' +
      '<p>Fragen erstellen und am Beamer mit der Klasse spielen. Gratis und ohne Anmeldung.</p></div></div>' +
      '<p class="eule-hinweis">Hier wird nichts gespeichert: Beim Schliessen der Seite sind die Quiz weg. In der <a href="https://klassenkiste.primarschuleulchen.com/" target="_blank" rel="noopener">Klassenkiste</a> bleiben sie gespeichert, die Kinder spielen per QR-Code mit ihren Geräten mit, und die KI erstellt Quiz aus Arbeitsblättern.</p>'""")
q.rep('data-a="kiOpen">✨ Fragen mit KI', 'data-a="kiOpen">🔒 Fragen mit KI')
q.schreibe('quiz/index.html')

# ---------------------------------------------------------------- Umfrage (aus dem Portal der Klassenkiste herausgelöst, ohne Datenbank)
# Die Umfrage ist in der Klassenkiste kein eigenes Werkzeug, sondern steckt in app.js (Modul U) und style.css.
# Originale: werkstatt/originale/klassenkiste-app.js und klassenkiste-style.css (Kopien aus dem Repo knobelnest).
# Hier: Umfragen erstellen und am Beamer zeigen; die Kinder antworten nacheinander am selben Gerät («＋ Antwort eintragen»).
# Nichts wird gespeichert. Mitmachen mit eigenen Geräten (Klasse/QR-Code) und Speichern nur in der Klassenkiste.
def umfrage():
    app = open(os.path.join(HIER, 'originale', 'klassenkiste-app.js'), encoding='utf-8').read()
    css = open(os.path.join(HIER, 'originale', 'klassenkiste-style.css'), encoding='utf-8').read()
    def stueck(start, ende):
        a = app.find(start); b = app.find(ende, a)
        if a < 0 or b < 0: sys.exit('umfrage: Stelle nicht gefunden: ' + (start if a < 0 else ende)[:60])
        return app[a:b]
    teil = stueck('  var UMF_TYPES = [', '  // ===================================================================\n  // Gedächtniskiste')
    teil += stueck('  // Eingabe für eine Frage. dr = Entwurf des Kindes', '  K.umfQ = function')
    teil += stueck('  function kuSendState()', '  ACT.kuSend = async function')
    u = Bau.__new__(Bau); u.name = 'umfrage'; u.s = teil
    # Bilder aus der Eulenkiste
    u.rep("'bilder/kacheln/umfrage-urne.webp'", "'umfrage-urne.webp'", u.s.count("'bilder/kacheln/umfrage-urne.webp'"))
    u.rep('src="bilder/kacheln/umfrage-urne.webp"', 'src="umfrage-urne.webp"', u.s.count('src="bilder/kacheln/umfrage-urne.webp"'))
    # Keine Klasse: «Klasse …» fällt weg (U.cls.name = «am Beamer»)
    n = u.s.count("Klasse ' + h(U.cls.name)"); u.rep("Klasse ' + h(U.cls.name)", "' + h(U.cls.name)", n)
    # Kopf der Live-Ansicht: statt «Mitmachen mit Code» Knopf zum Eintragen und gesperrter QR-Code
    u.rep("""        : '<div class="us-join">Mitmachen: ' + h(C.PORTAL_NAME) + ' öffnen und auf <b>«Umfrage»</b> tippen · Code <b>' + h(U.cls.code || '') + '</b></div>') +""",
          """        : '<div class="us-join ek-join"><button class="board-btn hot" data-a="ekAnt">＋ Antwort eintragen</button><button class="board-btn" data-a="ekQr">🔒 Mitmachen per QR-Code</button></div>') +""")
    # Liste: Text der Klassenkiste anpassen, Hinweis auf die Klassenkiste
    u.rep("""<p>Stellen Sie der Klasse Fragen: Abstimmungen, Wortwolken, Quiz, Schätzfragen und mehr. Die Kinder antworten am iPad, die Ergebnisse erscheinen live an der Wandtafel.</p>' +
      '<p class="muted small">Ihre Umfragen gelten für alle Ihre Klassen. Die Antworten werden pro Klasse gespeichert.</p></div>'""",
          """<p>Stelle der Klasse Fragen: Abstimmungen, Wortwolken, Quiz, Schätzfragen und mehr. Am Beamer zeigen, die Kinder tippen ihre Antwort nacheinander am selben Gerät ein, und das Ergebnis erscheint sofort.</p>' +
      '<p class="eule-hinweis">Hier wird nichts gespeichert: Beim Schliessen der Seite sind die Umfragen weg. In der <a href="https://klassenkiste.primarschuleulchen.com/" target="_blank" rel="noopener">Klassenkiste</a> bleiben sie gespeichert, und die Kinder antworten gleichzeitig mit ihren eigenen Geräten, mit Klassen-Login oder per QR-Code.</p></div>'""")
    u.rep("toast('Die Umfrage läuft. Die Kinder tippen auf «Umfrage».');", "toast('Die Umfrage läuft. Mit «＋ Antwort eintragen» geben die Kinder ihre Antwort ein.');")
    # Als Vorlage speichern geht hier nicht dauerhaft
    u.rep("""'<button class="btn sm" data-a="uAsTpl" data-id="' + sv.id + '" title="Als Vorlage speichern">⭐ Als Vorlage</button>' +""", "")
    # Speichern gibt es hier nicht
    u.rep("(U.st ? 'Wird gespeichert …' : '✓ Gespeichert')", "'nur bis zum Schliessen'")
    u.rep("""'<button class="btn" data-a="uAsTpl" data-id="' + sv.id + '">⭐ Als Vorlage speichern</button>""", "'")
    u.rep("toast('Umfrage beendet. Die Antworten bleiben gespeichert.')", "toast('Umfrage beendet. Die Antworten bleiben bis zum Schliessen der Seite.')")
    js = u.s
    rumpf = css.replace('url(schriften/patrick-hand.woff2)', 'url(../schriften/patrick-hand.woff2)')
    html = '''<!DOCTYPE html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Umfrage – Eulenkiste</title>
<meta name="referrer" content="no-referrer">
<link rel="icon" type="image/png" href="../eulenkiste-icon.png">
<link rel="stylesheet" href="../schriften/schriften.css">
<style>
/* Gestaltung der Klassenkiste (style.css aus dem Repo knobelnest) */
''' + rumpf + '''
/* Eulenkiste */
.eule-hinweis{margin-top:4px;padding:10px 16px;border-radius:16px;background:#fbf3dc;border:1.5px dashed #d6ad45;font-size:16px;color:#4a3d1a}
.ek-join{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.ek-ant{width:min(720px,100%)}
.ek-ant h2{font-size:30px}
.ek-n{color:var(--soft);font-size:16px}
.kk-nur-box{max-width:480px}
</style>
</head>
<body class="lp">
<div id="app"></div>
<div id="toast" class="toast" role="status" aria-live="polite"></div>
<script>
(function () {
  'use strict';
  var app = document.getElementById('app');
  // ---------- Hilfsfunktionen wie im Portal der Klassenkiste ----------
  function h(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function plural(n, one, many) { return n === 1 ? '1 ' + one : n + ' ' + many; }
  function hash(s) { var x = 0; s = String(s); for (var i = 0; i < s.length; i++) x = (x * 31 + s.charCodeAt(i)) >>> 0; return x; }
  var KID_TINTS = ['#F6C9A8', '#CFDDF0', '#CFE5C6', '#D3F1E4', '#E3D5F0', '#F3E2A6'];
  function kidColor(name) { return KID_TINTS[hash(name) % KID_TINTS.length]; }
  function medal(n) { return n === 1 ? '🥇' : n === 2 ? '🥈' : n === 3 ? '🥉' : n + '.'; }
  function shortUrl(u) { return u.replace(/^https?:\\/\\//, ''); }
  function klassBild() { return 'umfrage-urne.webp'; }
  function qrSvg() { return Promise.reject(new Error('Nur in der Klassenkiste')); }
  var toastTimer;
  function toast(msg) { var t = document.getElementById('toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(function () { t.classList.remove('show'); }, 3200); }
  function errMsg(e) { return (e && e.message) || String(e); }
  function paint(html) {
    var a = document.activeElement, id = a && a.id, s = null, e = null;
    try { s = a.selectionStart; e = a.selectionEnd; } catch (x) {}
    app.innerHTML = html;
    if (id) { var n = document.getElementById(id); if (n) { n.focus(); try { if (s != null) n.setSelectionRange(s, e); } catch (x) {} } }
  }
  function backBtn() { return '<a class="kn-back" href="../" aria-label="Zurück zur Eulenkiste" title="Zurück zur Eulenkiste"><span aria-hidden="true">←</span><img src="../eulenkiste.webp" alt="" width="34" height="34" draggable="false"></a>'; }
  var timers = []; function every(ms, fn) { timers.push(setInterval(fn, ms)); }
  var ACT = {};
  function run(fn, el, ev) { if (!fn) return; Promise.resolve().then(function () { return fn(el, ev); }).catch(function (err) { console.error(err); toast(errMsg(err)); }); }
  document.addEventListener('click', function (e) { var el = e.target.closest('[data-a]'); if (!el || el.tagName === 'FORM') return; if (el.tagName === 'A' && !el.getAttribute('href')) e.preventDefault(); run(ACT[el.dataset.a], el, e); });
  document.addEventListener('submit', function (e) { var f = e.target.closest('form[data-a]'); if (!f) return; e.preventDefault(); run(ACT[f.dataset.a], f, e); });
  document.addEventListener('change', function (e) { var el = e.target.closest('[data-change]'); if (el) run(ACT[el.dataset.change], el, e); });
  document.addEventListener('input', function (e) { var el = e.target.closest('[data-input]'); if (el) run(ACT[el.dataset.input], el, e); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeOverlays(); });
  var UI = { confirm: null, view: 'umfrage' };
  var confirmTimer;
  function armed(key) { if (UI.confirm === key) { UI.confirm = null; return true; } UI.confirm = key; clearTimeout(confirmTimer); confirmTimer = setTimeout(function () { if (UI.confirm === key) { UI.confirm = null; U.render(); } }, 4000); return false; }
  function overlay(html) { closeOverlays(); var o = document.createElement('div'); o.className = 'overlay'; o.innerHTML = html; o.addEventListener('click', function (e) { if (e.target === o) closeOverlays(); }); document.body.appendChild(o); var f = o.querySelector('input,button'); if (f) f.focus(); return o; }
  function closeOverlays() { Array.prototype.forEach.call(document.querySelectorAll('.overlay'), function (o) { o.remove(); }); }
  ACT.closeOverlay = function () { closeOverlays(); };
  ACT.wallFull = function () { if (document.fullscreenElement) document.exitFullscreen(); else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen(); };
  // ---------- Speicher nur im Speicher dieser Seite (nichts wird verschickt) ----------
  var MEM = {};
  var DB = {
    storeGet: function (k) { return Promise.resolve(MEM[k] ? JSON.parse(JSON.stringify(MEM[k])) : null); },
    storeSet: function (k, v) { MEM[k] = JSON.parse(JSON.stringify(v)); return Promise.resolve(); },
    sharedGet: function () { return Promise.resolve(null); },
    sharedSet: function () { return Promise.reject(new Error('Nur in der Klassenkiste')); },
    umfragePut: function (cid, live, clear, sec) { var now = Date.now(); return Promise.resolve({ now: now, until: live && live.sec ? now + live.sec * 1000 : null }); }
  };
  var K = { U: null };

''' + js + '''
  // ---------- Eulenkiste: Start ohne Klasse, ohne Datenbank ----------
  U.cls = { name: 'am Beamer', bild: '', code: '' }; U.ckids = []; U.list = []; U.tv = { eigene: [], weg: [] }; U.tshared = []; U.admin = false; U.tvWeg = false;
  U.docs = { klasse: { live: null, ans: {} }, offen: null }; U.cid = 'beamer'; U.off = 0;
  U.use('klasse'); U.view = 'list';
  U.poll = function () {};
  U.save = function () { clearTimeout(U.st); U.st = null; var m = document.getElementById('ueSaved'); if (m) m.textContent = 'nur bis zum Schliessen'; return Promise.resolve(); };
  // Starten: direkt am Beamer (kein «Wer macht mit?»)
  ACT.uStart = async function (el) {
    var sv = U.find(el.dataset.id); if (!sv) return;
    var bad = umfCheck(sv); if (bad) { if (U.view !== 'edit') { U.eid = sv.id; U.qi = 0; U.add = false; U.view = 'edit'; U.render(); } return toast(bad); }
    return ACT.uGo({ dataset: { id: sv.id, neu: '1' } });
  };
  // Antworten am selben Gerät eintragen (Eingabe wie bei den Kindern)
  var NR = 0;
  K.umfQ = function () { var l = U.doc.live; if (!l || !l.on) return null; var qs = l.qs || []; return qs[U.idx()] || qs[0]; };
  K.umfDr = function (q) { if (K.U.dr[q.id] === undefined) K.U.dr[q.id] = umfDraft0(q); return K.U.dr[q.id]; };
  K.render = function () {
    var q = K.umfQ(), box = document.getElementById('ekAntBox'); if (!q || !box) return;
    box.innerHTML = '<span class="ek-n">' + umfType(q.type)[2] + ' ' + h(umfType(q.type)[1]) + '</span><h2>' + h(q.text) + '</h2>' + umfInput(q, K.umfDr(q)) +
      '<div class="row" style="justify-content:flex-end;margin-top:12px"><button class="btn" data-a="closeOverlay">Fertig</button><button class="btn primary" data-a="kuSend">Antwort abgeben ✦</button></div>';
    kuSendState();
  };
  ACT.ekAnt = function () {
    var l = U.doc.live, q = K.umfQ(); if (!q) return;
    if (q.type === 'info') return toast('Bei einer Infofolie gibt es nichts zu beantworten.');
    if (!l.open) return toast('Die Abstimmung ist geschlossen. Zuerst «🔓 Öffnen».');
    K.U = { dr: {}, edit: {}, i: 0 };
    overlay('<div class="card stack ek-ant kidv" id="ekAntBox"></div>'); K.render();
  };
  ACT.kuSend = function () {
    var q = K.umfQ(); if (!q) return; var v = umfVal(q, K.umfDr(q)); if (v == null) return;
    if (!U.doc.live.open) { closeOverlays(); return toast('Die Abstimmung ist geschlossen.'); }
    var id = 'g' + (++NR); U.ckids.push({ id: id, name: 'Antwort ' + NR }); U.use('klasse');
    (U.doc.ans[q.id] = U.doc.ans[q.id] || {})[id] = v;
    K.U.dr = {}; U.render(); K.render(); toast('Danke! Die nächste Person ist dran.');
  };
  // Hinweis: nur in der Klassenkiste
  ACT.ekQr = function () {
    overlay('<div class="card stack kk-nur-box"><h2>🔒 Mitmachen per QR-Code</h2><p>Das gibt es nur in der Klassenkiste. Dort antworten alle Kinder gleichzeitig mit ihren eigenen Geräten, mit dem Klassen-Login oder per QR-Code, und die Umfragen bleiben gespeichert.</p>' +
      '<p class="muted small">Hier in der Eulenkiste tippen die Kinder ihre Antwort nacheinander am selben Gerät ein. Gespeichert wird nichts.</p>' +
      '<div class="row"><a class="btn primary" href="https://klassenkiste.primarschuleulchen.com/" target="_blank" rel="noopener">Zur Klassenkiste ✦</a><button class="btn" data-a="closeOverlay">Schliessen</button></div></div>');
  };
  window.addEventListener('beforeunload', function (e) { if (U.list.length) { e.preventDefault(); e.returnValue = ''; } });
  U.render();
  every(500, U.tick);
})();
</script>
</body>
</html>
'''
    ziel = os.path.join(WURZEL, 'umfrage', 'index.html')
    alt = open(ziel, encoding='utf-8').read() if os.path.exists(ziel) else None
    open(ziel, 'w', encoding='utf-8').write(html)
    print('umfrage/index.html: ' + ('gleich' if alt == html else 'neu geschrieben'))
umfrage()
