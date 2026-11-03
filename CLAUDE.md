# Eulenkiste – Arbeitsanleitung für Claude

Übersichtsseite von Primarschuleulchen mit digitalen Tools. Geplante Adresse: `eulenkiste.primarschuleulchen.com` (Repository heisst noch `lernkompass`) (GitHub Pages, Branch `main`).
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
  - `otterteich/` = Karte «Lautstärkenregler» (Bild `lautstaerke-bild.webp`). Original hat eigene strenge Sicherheitsregeln (CSP); `img-src` erlaubt zusätzlich `'self'` für Logo und Feder. Die Claude-Hülle am Dateianfang wird entfernt.
  - Tagesfolie: Arbeitsstand und Otterteich grau in der Leiste («Nur in der Klassenkiste – jetzt anmelden und freischalten»); Link zum Kaufen später in `KN_LINK`.
- Das Knobelnest heisst auf der Eulenkiste «Klassenkiste» (Bild `klassenkiste-bild.webp`). Das Portal selbst ist noch nicht umbenannt.
- Logo (von der Lehrerin gezeichnet): `logo.webp` (Lehrerin mit Eule in der Holzkiste), `eulenkiste.webp` (nur Eule, rund, Kopf), `eulenkiste-icon.png` (Browser-Tab).
- Karten: mittig, rundes Medaillon oben (`.bild-rund`, Bild wie `gluecksrad-bild.webp` oder Symbol mit Goldrand), Titel mit ✦ ✧ ✦ darunter. Kein «ohne Anmeldung»-Schild.
- Mauszeiger: Feder (`feder.png`, beim Zeigen auf Links `feder-gold.png`; Quelle `feder.svg`).
- Schrift: überall Patrick Hand (`--ui`), nur eine Stärke (font-weight 400). Schatten blau und weich (`--schatten`).
- Cache-Bremse: `style.css?v=N` in den HTML-Dateien erhöhen, wenn sich `style.css` ändert.

## Veröffentlichen
Auf dem Arbeitszweig committen und pushen, dann Pull Request nach `main` und **selbst zusammenführen**: Die Lehrerin hat erlaubt, Änderungen immer direkt online zu stellen. Nach dem Zusammenführen den Arbeitszweig neu auf `main` aufsetzen.
