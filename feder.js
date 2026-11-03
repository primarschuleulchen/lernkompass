/* Eulenkiste – Feder als Mauszeiger.
   Ein kleines Bild folgt der Maus. Das ist zuverlässiger als ein reiner CSS-Mauszeiger,
   der in Chrome auf dem Mac manchmal zum Textstrich wurde.
   Nur mit Maus oder Trackpad; auf Handy, Tablet und mit dem Smartboard-Stift bleibt alles normal.
   Wo eine Seite bewusst einen eigenen Zeiger will (Textfeld, Verschieben, Grösse ändern),
   erscheint dieser statt der Feder. */
(function () {
  'use strict';
  if (!window.matchMedia || !matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  var skript = document.currentScript;
  var basis = skript && skript.src ? skript.src.replace(/feder\.js(\?.*)?$/, '') : '';
  var KLICKBAR = 'a,button,label,select,summary,.klickbar,[role=button],[data-add],[data-locked]';
  var html = document.documentElement;

  var bild = document.createElement('img');
  bild.alt = '';
  bild.setAttribute('aria-hidden', 'true');
  bild.style.cssText = 'position:fixed;left:0;top:0;width:32px;height:32px;margin:0;padding:0;border:0;' +
    'pointer-events:none;z-index:2147483647;display:none;will-change:transform';
  var normal = basis + 'feder@2x.png', gold = basis + 'feder-gold@2x.png';
  new Image().src = gold;
  bild.src = normal;

  function einbauen() {
    html.classList.add('feder');
    (document.body || html).appendChild(bild);
  }
  if (document.body) einbauen(); else document.addEventListener('DOMContentLoaded', einbauen);

  var x = 0, y = 0, ziel = null, warten = false, istGold = false;
  function zeichne() {
    warten = false;
    var zeigen = false;
    if (ziel && ziel.nodeType === 1 && !ziel.closest('.app.idle, body.idle')) {
      // Nur wo kein eigener Zeiger gewünscht ist, die Feder zeigen
      zeigen = getComputedStyle(ziel).cursor === 'none';
    }
    if (!zeigen) { bild.style.display = 'none'; return; }
    var g = !!ziel.closest(KLICKBAR);
    if (g !== istGold) { istGold = g; bild.src = g ? gold : normal; }
    bild.style.transform = 'translate(' + (x - 2) + 'px,' + (y - 30) + 'px)';
    bild.style.display = 'block';
  }
  document.addEventListener('pointermove', function (e) {
    if (e.pointerType && e.pointerType !== 'mouse') { html.classList.remove('feder'); bild.style.display = 'none'; return; }
    html.classList.add('feder');
    x = e.clientX; y = e.clientY; ziel = e.target;
    if (!warten) { warten = true; requestAnimationFrame(zeichne); }
  }, { passive: true });
  document.addEventListener('mouseout', function (e) { if (!e.relatedTarget) bild.style.display = 'none'; });
  window.addEventListener('blur', function () { bild.style.display = 'none'; });
})();
