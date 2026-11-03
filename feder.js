/* Eulenkiste – Feder als Glitzer.
   Der normale Mauszeiger bleibt. Daneben schwebt eine kleine Feder sanft hinterher
   und verblasst, sobald die Maus stillsteht. Über Knöpfen und Karten wird sie golden.
   Nur mit Maus oder Trackpad, nicht bei «Bewegung reduzieren» und nicht auf Touch-Geräten. */
(function () {
  'use strict';
  if (!window.matchMedia || !matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var skript = document.currentScript;
  var basis = skript && skript.src ? skript.src.replace(/feder\.js(\?.*)?$/, '') : '';
  var KLICKBAR = 'a,button,label,select,summary,.klickbar,[role=button],[data-add],[data-locked]';
  var normal = basis + 'feder@2x.png', gold = basis + 'feder-gold@2x.png';
  new Image().src = gold;

  var bild = document.createElement('img');
  bild.alt = '';
  bild.setAttribute('aria-hidden', 'true');
  bild.src = normal;
  bild.style.cssText = 'position:fixed;left:0;top:0;width:26px;height:26px;margin:0;padding:0;border:0;' +
    'pointer-events:none;z-index:2147483647;opacity:0;transition:opacity .45s ease;will-change:transform,opacity';
  function einbauen() { (document.body || document.documentElement).appendChild(bild); }
  if (document.body) einbauen(); else document.addEventListener('DOMContentLoaded', einbauen);

  var zx = 0, zy = 0, fx = 0, fy = 0, laeuft = false, uhr = 0, istGold = false, erst = true;
  function schritt() {
    fx += (zx - fx) * 0.18;
    fy += (zy - fy) * 0.18;
    // etwas rechts unterhalb vom Mauszeiger, leicht schaukelnd
    var w = Math.sin(Date.now() / 260) * 6;
    bild.style.transform = 'translate(' + (fx + 16) + 'px,' + (fy + 4) + 'px) rotate(' + w + 'deg)';
    if (Math.abs(zx - fx) + Math.abs(zy - fy) > 0.3 || bild.style.opacity !== '0') requestAnimationFrame(schritt);
    else laeuft = false;
  }
  document.addEventListener('pointermove', function (e) {
    if (e.pointerType && e.pointerType !== 'mouse') return;
    zx = e.clientX; zy = e.clientY;
    if (erst) { fx = zx; fy = zy; erst = false; }
    var t = e.target, ruhig = t && t.closest && t.closest('.app.idle, body.idle');
    var g = !!(t && t.closest && t.closest(KLICKBAR));
    if (g !== istGold) { istGold = g; bild.src = g ? gold : normal; }
    bild.style.opacity = ruhig ? '0' : '1';
    clearTimeout(uhr);
    uhr = setTimeout(function () { bild.style.opacity = '0'; }, 650);
    if (!laeuft) { laeuft = true; requestAnimationFrame(schritt); }
  }, { passive: true });
  document.addEventListener('mouseout', function (e) { if (!e.relatedTarget) bild.style.opacity = '0'; });
  window.addEventListener('blur', function () { bild.style.opacity = '0'; });
})();
