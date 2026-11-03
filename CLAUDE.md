# Lernkompass – Arbeitsanleitung für Claude

Übersichtsseite von Primarschuleulchen mit digitalen Tools. Geplante Adresse: `lernkompass.primarschuleulchen.com` (GitHub Pages, Branch `main`).
Die Benutzerin ist Lehrerin, keine Programmiererin: Antworten auf Deutsch in Schweizer Schreibweise («ss», «…»), kurz und ohne Fachjargon.

## Grundregel: keine Daten
- Keine Anmeldung, keine Datenbank, kein Supabase, keine KI-Dienste, keine Statistik, keine Cookies, keine externen Skripte oder Schriften.
- Alles läuft im Browser. Speichern höchstens in `localStorage` des eigenen Geräts.
- Was Daten braucht, gehört ins Knobelnest (eigenes Repository `primarschuleulchen/knobelnest`), nicht hierher.

## Aufbau
- `index.html` Übersicht mit Tool-Karten (`.karte` + Farbe `blau|rosa|gruen|gelb`, Hinweis `login|bald|frei`).
- Kleine Tools kommen als eigener Ordner dazu, z. B. `gluecksrad/index.html`, und nutzen `../style.css` bzw. die Schriften in `schriften/`.
- Cache-Bremse: `style.css?v=N` in den HTML-Dateien erhöhen, wenn sich `style.css` ändert.

## Veröffentlichen
Auf dem Arbeitszweig committen und pushen. «Online stellen» = Pull Request nach `main`, die Lehrerin führt zusammen.
