# Eulenkiste – Arbeitsanleitung für Claude

Übersichtsseite von Primarschuleulchen mit digitalen Tools. Adresse: https://eulenkiste.primarschuleulchen.com/ (Repository heisst noch `lernkompass`; GitHub Pages, Branch `main`, eigene Adresse über die Datei `CNAME`; DNS bei WordPress.com: CNAME `eulenkiste` → `primarschuleulchen.github.io`). Die Klassenkiste ist unter https://klassenkiste.primarschuleulchen.com/.
Die Benutzerin ist Lehrerin, keine Programmiererin: Antworten auf Deutsch in Schweizer Schreibweise («ss», «…»), kurz und ohne Fachjargon.

## Grundregel: keine Daten
- Keine Anmeldung, keine Datenbank, kein Supabase, keine KI-Dienste, keine Statistik, keine Cookies, keine externen Skripte oder Schriften.
- Alles läuft im Browser. Speichern höchstens in `localStorage` des eigenen Geräts.
- Was Daten braucht, gehört ins Knobelnest (eigenes Repository `primarschuleulchen/knobelnest`), nicht hierher.

## Aufbau
- `index.html` Übersicht mit Tool-Karten (`.karte` + Farbe `blau|rosa|gruen|gelb`, Hinweis `login|bald|frei`).
- Kleine Tools kommen als eigener Ordner dazu, z. B. `gluecksrad/index.html`, und nutzen `../style.css` bzw. die Schriften in `schriften/`.
- Tools aus Originalen der Lehrerin: Original nach `werkstatt/originale/<tool>.html`, dann `python3 werkstatt/bauen.py` (ersetzt genau festgelegte Textstellen, bricht bei «Anzahl 0 statt 1» ab). Änderungen an Tools immer im Skript machen, nicht nur in der fertigen Datei.
  - `gluecksrad/` und `tagesfolie/`: Schriften lokal (`schriften/schriften.css`), Knopf oben links zurück zur Eulenkiste (Pfeil + Eulen-Logo, `ZURUECK` in bauen.py), Tagesfolie ohne Konto/Datenbank.
  - `otterteich/` = Karte «Lautstärkenregler» (Bild `lautstaerke-bild.webp`). Original hat eigene strenge Sicherheitsregeln (CSP); `img-src` erlaubt zusätzlich `'self'` für das Logo. Die Claude-Hülle am Dateianfang wird entfernt.
  - `wort-des-tages/` = Lernspiel im Abschnitt «Lernspiele» (`#lernspiele`, Knopf oben im Willkommensbereich). Original ohne eigene Wörter der Lehrperson, speichert nur in `localStorage`. Die Eule im Kopf wird zum Zurück-Knopf.
  - `spiele/<spiel>.html` = 17 Knobelspiele aus der Klassenkiste (Rechen-Rakete, Wie spät ist es?, Kiosk, Wort-Raten, Der die das, Silben-Puzzle, Bilderrätsel, Eulen-Weg, Bilder-Sudoku, Wasser-Weg, Zahlenmauer, Klötzli-Turm, Kisten-Packen, Laternen, Schiebe-Bild, Geheimcode, Irrgarten), im Abschnitt «Lernspiele» als eine Karte «Knobelkiste» (Bild `knobelkiste-bild.webp`) → `knobelkiste/index.html`: wie die Knobelkiste der Kinder in der Klassenkiste: Kopf mit Bild, Knöpfe «Alle / Mathematik / Deutsch / Knobeln» (keine Unterordner, gewählte Art im Hash `#mathematik` usw., Liste `SPIELE`) und Spielkarten mit Bild `spiele/<spiel>-bild.webp`. Sie entstehen im Knobelnest (`werkstatt/spiele/knobelspiele/bauen.py`); fertige Datei aus `knobelspiele/` nach `werkstatt/originale/spiele/` kopieren, dann `bauen.py` (Liste `KNOBELSPIELE`; setzt den Zurück-Knopf auf der Stufen-Seite, Ziel `../knobelkiste/#<fach>` (`FACH`)). Ohne Klassenkiste: keine Sterne, Ton und Rekorde nur im `localStorage`.
  - `englisch/index.html` = Lernspielordner «Englisch» (Karte im Abschnitt «Lernspiele», Bild `englisch-bild.webp`), gleich gebaut wie die Knobelkiste, ohne Art-Knöpfe. Spiele `spiele/kleiderschrank.html` (aus knobelspiele/ im Knobelnest) und `spiele/owl-town.html` (aus englisch/owl-town.html im Knobelnest); in `KNOBELSPIELE` mit `FACH` «englisch», Zurück → `../englisch/`. Kleiderschrank und Owl Town haben eine eigene Startseite (Stufen-Pfad `pf-top`), dort setzt `bauen.py` den Zurück-Knopf ebenfalls. Owl Town braucht three.js: liegt lokal in `bibliothek/three/` (Version 0.160.0, MIT), `bauen.py` biegt die Importmap von jsdelivr dorthin um.
  - Tagesfolie: entsteht in der Klassenkiste (Repo knobelnest, `werkstatt/einbau/tagesfolie/`). Original hier = deren fertige `tagesfolie.html` (läuft ohne Konto nur im Browser); `bauen.py` setzt nur Zurück-Knopf, Schriften-Pfad, «Halbklasse», graue Knöpfe und entfernt YouTube-Musik (eigene Musik höchstens 3 MB).
  - Tagesfolie: Arbeitsstand, Otterteich und Hausaufgaben grau in der Leiste («Nur in der Klassenkiste – jetzt anmelden und freischalten»); Link zum Kaufen später in `KN_LINK`.
- `pinnwand/` = Klassen-Pinnwand (Bild `pinnwand-bild.webp`). Ohne Konto: kleiner Speicher-Ersatz für `claude.use('db')` im Browser (`localStorage` «eulenkiste-pinnwand»), Hinweis «Kinder an eigenen Geräten: nur in der Klassenkiste». Dieselbe Pinnwand ist in der Klassenkiste (Repo knobelnest, `werkstatt/einbau/pinnwand/`, Korrekturen in `pin_fixes.py`).
- Die Lehrerin will, dass Änderungen an Tools, die es auch in der Klassenkiste gibt (Tagesfolie, Glücksrad, Lautstärkeregler, Pinnwand), immer in beiden Repos gemacht werden.
- Das Knobelnest heisst auf der Eulenkiste «Klassenkiste» (Bild `klassenkiste-bild.webp`). Das Portal selbst ist noch nicht umbenannt.
- Logo (von der Lehrerin gezeichnet): `logo.webp` (Lehrerin mit Eule in der Holzkiste), `eulenkiste.webp` (nur Eule, rund, Kopf), `eulenkiste-icon.png` (Browser-Tab).
- Karten: mittig, rundes Medaillon oben (`.bild-rund`, Bild wie `gluecksrad-bild.webp` oder Symbol mit Goldrand), Titel mit ✦ ✧ ✦ darunter. Kein «ohne Anmeldung»-Schild.
- Kein eigener Mauszeiger: Die Lehrerin hat die Feder (als CSS-Zeiger und als Bild, das der Maus folgt) ausprobiert und wieder abgelehnt.
- Schriftzug: «Eulen» dunkel, «kiste» gold (#c4952f).
- Karten alle gleich hoch (`grid-auto-rows:1fr`), darum Texte kurz halten.
- Schrift: überall Patrick Hand (`--ui`), nur eine Stärke (font-weight 400). Schatten blau und weich (`--schatten`).
- Cache-Bremse: `style.css?v=N` in den HTML-Dateien erhöhen, wenn sich `style.css` ändert.

## Veröffentlichen
Auf dem Arbeitszweig committen und pushen, dann Pull Request nach `main` und **selbst zusammenführen**: Die Lehrerin hat erlaubt, Änderungen immer direkt online zu stellen. Nach dem Zusammenführen den Arbeitszweig neu auf `main` aufsetzen.
