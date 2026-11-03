/* Eulenkiste – Feder als Mauszeiger.
   Solange sich die Maus bewegt, ist die Feder der Mauszeiger (genau an der Mausspitze).
   Hält die Maus an, verblasst die Feder und der normale Mauszeiger erscheint wieder.
   So gibt es keinen doppelten Zeiger, auch nicht in Chrome auf dem Mac.
   Wo eine Seite bewusst einen eigenen Zeiger will (Textfeld, Verschieben, Grösse ändern),
   erscheint dieser statt der Feder. Nur mit Maus oder Trackpad. */
(function () {
  'use strict';
  if (!window.matchMedia || !matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  var skript = document.currentScript;
  var basis = skript && skript.src ? skript.src.replace(/feder\.js(\?.*)?$/, '') : '';
  var KLICKBAR = 'a,button,label,select,summary,.klickbar,[role=button],[data-add],[data-locked]';
  var normal = basis + 'feder@2x.png', gold = basis + 'feder-gold@2x.png';
  var html = document.documentElement;
  new Image().src = gold;

  var bild = document.createElement('img');
  bild.alt = '';
  bild.setAttribute('aria-hidden', 'true');
  bild.src = normal;
  bild.style.cssText = 'position:fixed;left:0;top:0;width:32px;height:32px;margin:0;padding:0;border:0;' +
    'pointer-events:none;z-index:2147483647;opacity:0;transition:opacity .35s ease;will-change:transform,opacity';
  function einbauen() { (document.body || html).appendChild(bild); }
  if (document.body) einbauen(); else document.addEventListener('DOMContentLoaded', einbauen);

  var x = 0, y = 0, ziel = null, warten = false, istGold = false, uhr = 0;
  function aus() { bild.style.opacity = '0'; html.classList.remove('feder'); }
  function zeichne() {
    warten = false;
    html.classList.add('feder');
    var t = ziel;
    // eigener Zeiger der Seite (z. B. Textfeld) oder Ruhemodus: Feder ausblenden
    if (!t || t.nodeType !== 1 || t.closest('.app.idle, body.idle') || getComputedStyle(t).cursor !== 'none') {
      bild.style.opacity = '0';
      return;
    }
    var g = !!t.closest(KLICKBAR);
    if (g !== istGold) { istGold = g; bild.src = g ? gold : normal; }
    bild.style.transform = 'translate(' + (x - 2) + 'px,' + (y - 30) + 'px)';
    bild.style.transition = 'none';
    bild.style.opacity = '1';
  }
  document.addEventListener('pointermove', function (e) {
    if (e.pointerType && e.pointerType !== 'mouse') { aus(); return; }
    x = e.clientX; y = e.clientY; ziel = e.target;
    clearTimeout(uhr);
    // nach kurzem Stillstand verblasst die Feder, der normale Zeiger kommt zurück
    uhr = setTimeout(function () { bild.style.transition = 'opacity .35s ease'; aus(); }, 450);
    if (!warten) { warten = true; requestAnimationFrame(zeichne); }
  }, { passive: true });
  document.addEventListener('mouseout', function (e) { if (!e.relatedTarget) aus(); });
  window.addEventListener('blur', aus);
})();
