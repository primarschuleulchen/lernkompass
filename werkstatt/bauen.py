#!/usr/bin/env python3
"""Baut die Tools der Eulenkiste aus den Originalen der Lehrerin.

  werkstatt/originale/gluecksrad.html  ->  gluecksrad/index.html
  werkstatt/originale/tagesfolie.html  ->  tagesfolie/index.html

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


ZURUECK_CSS = 'a.pill.lk-back{text-decoration:none;color:inherit;display:inline-flex;align-items:center;gap:6px}'

# ---------------------------------------------------------------- Glücksrad
g = Bau('gluecksrad')
schriften(g)
# Knopf zurück zur Eulenkiste, vor «Ton an»
g.rep('<button class="pill" id="sound"',
      '<a class="pill lk-back" href="../">← Eulenkiste</a>\n      <button class="pill" id="sound"')
g.rep('.pill:hover{', ZURUECK_CSS + '\n.pill:hover{')
g.schreibe('gluecksrad/index.html')

# ---------------------------------------------------------------- Tagesfolie
t = Bau('tagesfolie')
schriften(t)
# Knopf zurück zur Eulenkiste, ganz links in der oberen Leiste
t.rep('<div class="top">\n    <div class="tabs"',
      '<div class="top">\n    <a class="pill lk-back" href="../" title="Zurück zur Eulenkiste">←</a>\n    <div class="tabs"')

# Kein Konto, keine Datenbank: alles bleibt auf diesem Gerät (auch wenn die Seite in Claude geöffnet würde)
t.rep('    if (!window.claude?.use) return;\n',
      '    return; // Eulenkiste: kein Konto, keine Datenbank – alles bleibt auf diesem Gerät\n')

# Arbeitsstand und Otterteich gibt es nur im Knobelnest: grau in der Leiste, mit Hinweis beim Darüberfahren oder Antippen
STAND_ICON = ('<rect x="4" y="6" width="24" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="2.4"/>'
              '<path d="M4 13h24M12 6v20M20 6v20" stroke="currentColor" stroke-width="2"/>'
              '<circle cx="8" cy="19" r="2" fill="currentColor"/><circle cx="24" cy="22" r="2" fill="currentColor"/>')
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
  const zeige = b => {
    clearTimeout(zu);
    tip.innerHTML = `<b>🔒 ${esc(KN_TIP)}</b>` + (KN_LINK ? ` <a href="${esc(KN_LINK)}" target="_blank" rel="noopener">Mehr erfahren</a>` : "");
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
  tip.addEventListener("mouseenter", () => clearTimeout(zu));
  tip.addEventListener("mouseleave", weg);
  $("#dock").addEventListener("scroll", () => tip.classList.remove("show"), { passive: true });
})();''')
t.rep('const DOCK = [',
      '''// Nur im Knobelnest erhältlich (grau in der Leiste). KN_LINK: später die Seite auf primarschuleulchen.com, wo man den Zugang bekommt
const KN_NUR = { stand: ["Arbeitsstand", `''' + STAND_ICON + '''`], otter: ["Otterteich", `''' + OTTER_ICON + '''`] };
const KN_TIP = "Nur im Knobelnest – jetzt anmelden und freischalten";
const KN_LINK = "";
const DOCK = [''')
t.rep('.dock .sep{', '''.dock button.locked{color:#9aa39d;cursor:help}
.dock button.locked svg{opacity:.55}
.dock button.locked:hover{background:#f1f2ef}
.kn-tip{position:fixed;left:0;top:0;z-index:300;max-width:250px;background:#1f2421;color:#fff;border-radius:12px;padding:9px 13px;font-size:13px;line-height:1.35;box-shadow:0 6px 20px rgba(0,0,0,.2);opacity:0;pointer-events:none;transition:opacity .15s}
.kn-tip.show{opacity:1;pointer-events:auto}
.kn-tip a{color:#bfe3fb;font-weight:800}
''' + ZURUECK_CSS + '''
.dock .sep{''')
t.schreibe('tagesfolie/index.html')
