// Nimmt die kurzen Vorführ-Videos für «Weitere Tools in der Klassenkiste» auf (Test-Klassenkiste, Schein-Datenbank, erfundene Namen).
// 1) Im Repo knobelnest: bash werkstatt/test/testseite.sh   (startet http://localhost:8765/)
// 2) node werkstatt/videos/aufnehmen.js <ausgabeordner> [quiz umfrage tafel heft eltern vokabel]
// 3) Die .mp4 und .jpg aus dem Ausgabeordner nach klassenkiste/ kopieren. Braucht Playwright und ffmpeg.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const OUT = path.resolve(process.argv[2]); fs.mkdirSync(OUT, { recursive: true });
const NUR = process.argv.slice(3);
const RAW = path.join(OUT, 'roh'); fs.mkdirSync(RAW, { recursive: true });
const URL = 'http://localhost:8765/', W = 1280, H = 800;
const KN = process.env.KN || '/home/user/knobelnest';  // Repo knobelnest (Vokabelkiste und Bilder)
const KINDER = ['Lena', 'David', 'Mia', 'Noah', 'Lia', 'Jan', 'Emma', 'Luca', 'Nina', 'Tim', 'Sara', 'Leo'];

const CURSOR = `(function(){
  function mk(){ if (document.getElementById('__fc')) return; var d=document.createElement('div'); d.id='__fc';
    d.style.cssText='position:fixed;left:0;top:0;width:28px;height:28px;z-index:2147483647;pointer-events:none;display:none';
    d.innerHTML='<svg viewBox="0 0 24 24" width="28" height="28"><path d="M4 2.5l15 9.2-6.6 1.3 3.7 7.2-2.9 1.4-3.6-7.2L4.8 19z" fill="#1f2421" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
    var r=document.createElement('div'); r.id='__fr'; r.style.cssText='position:fixed;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;border:3px solid #d6ad45;z-index:2147483646;pointer-events:none;opacity:0';
    (document.body||document.documentElement).appendChild(d); (document.body||document.documentElement).appendChild(r); }
  document.addEventListener('mousemove', function(e){ mk(); var d=document.getElementById('__fc'); d.style.display='block'; d.style.left=(e.clientX-3)+'px'; d.style.top=(e.clientY-2)+'px'; }, true);
  document.addEventListener('mouseout', function(e){ if (!e.relatedTarget) { var d=document.getElementById('__fc'); if(d) d.style.display='none'; } }, true);
  document.addEventListener('mousedown', function(e){ mk(); var r=document.getElementById('__fr'); r.style.left=e.clientX+'px'; r.style.top=e.clientY+'px'; r.style.transition='none'; r.style.opacity='1'; r.style.transform='scale(.4)';
    requestAnimationFrame(function(){ requestAnimationFrame(function(){ r.style.transition='opacity .5s,transform .5s'; r.style.opacity='0'; r.style.transform='scale(1.3)'; }); }); }, true);
})();`;

class Film {
  static async neu(name) {
    const f = new Film(); f.name = name;
    f.b = await chromium.launch({ args: ['--lang=de-CH'], env: Object.assign({}, process.env, { LANG: 'de_CH.UTF-8', LANGUAGE: 'de_CH:de', LC_ALL: 'de_CH.UTF-8' }) });
    f.ctx = await f.b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, locale: 'de-CH', recordVideo: { dir: RAW, size: { width: W, height: H } } });
    for (const u of ['https://fonts.googleapis.com/**', 'https://fonts.gstatic.com/**']) await f.ctx.route(u, r => r.abort());
    await f.ctx.addInitScript(CURSOR);
    f.p = await f.ctx.newPage(); f.t0 = Date.now(); f.start = 0; f.mx = W / 2; f.my = H / 2;
    f.p.on('pageerror', e => console.log(name, 'FEHLER', e.message));
    return f;
  }
  los() { this.start = (Date.now() - this.t0) / 1000; }
  warte(ms) { return this.p.waitForTimeout(ms); }
  async hin(loc, klick = true, dauer = 650) { console.log('  hin', ((Date.now()-this.t0)/1000).toFixed(1));
    await loc.waitFor({ state: 'visible', timeout: 15000 });
    const bb = await loc.boundingBox(), x = bb.x + bb.width / 2, y = bb.y + bb.height / 2;
    const n = Math.max(8, Math.round(dauer / 16));
    for (let i = 1; i <= n; i++) { let t = i / n; t = t * t * (3 - 2 * t); await this.p.mouse.move(this.mx + (x - this.mx) * t, this.my + (y - this.my) * t); await this.p.waitForTimeout(16); }
    this.mx = x; this.my = y;
    if (klick) { await this.warte(180); await this.p.mouse.down(); await this.warte(70); await this.p.mouse.up(); await this.warte(250); }
  }
  async tippe(text, ms = 75) { for (const ch of text) { await this.p.keyboard.type(ch); await this.warte(ms); } }
  async fertig(ziel) {
    const ende = (Date.now() - this.t0) / 1000;
    const vid = await this.p.video().path(); await this.ctx.close(); await this.b.close();
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', this.start.toFixed(2), '-to', ende.toFixed(2), '-i', vid,
      '-vf', 'scale=960:-2,fps=25', '-c:v', 'libx264', '-preset', 'slow', '-crf', '30', '-pix_fmt', 'yuv420p', '-an', '-movflags', '+faststart', path.join(OUT, ziel + '.mp4')]);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', (this.start + 1.2).toFixed(2), '-i', vid, '-frames:v', '1', '-vf', 'scale=960:-2', '-q:v', '4', path.join(OUT, ziel + '.jpg')]);
    fs.unlinkSync(vid);
    console.log(ziel, 'fertig', (ende - this.start).toFixed(1), 's');
  }
}

async function einrichten(f, kinder = KINDER, vorher) {
  const p = f.p;
  await p.goto(URL); await p.waitForSelector('#lgMail');
  if (vorher) await vorher(p);
  await p.fill('#lgMail', 'admin@x.ch'); await p.fill('#lgPw', 'test1234'); await p.click('form[data-a=login] button.primary');
  await p.waitForSelector('#obName'); await p.fill('#obName', 'Frau Eule'); await p.click('text=Weiter');
  await p.waitForSelector('#cName'); await p.fill('#cName', '4a'); await p.click('form[data-a=createClass] button'); await p.waitForSelector('#kidBulk');
  await p.fill('#kidBulk', kinder.join('\n')); await p.click('form[data-a=addBulk] button'); await p.waitForTimeout(500);
  console.log('  eingerichtet', ((Date.now()-f.t0)/1000).toFixed(1)); return p.evaluate("__D.classes.find(c=>c.name==='4a').id");
}

const FILME = {};

FILME.quiz = async function () {
  const f = await Film.neu('quiz'), p = f.p;
  await einrichten(f);
  const fr = [
    { id: 'f1', typ: 'quiz', frage: 'Welches Tier kann fliegen?', bild: '', zeit: 20, punkte: 1, mehrfach: false, antworten: ['Eule', 'Igel', 'Fuchs', 'Otter'], richtig: [0] },
    { id: 'f2', typ: 'rf', frage: 'Die Erde dreht sich um die Sonne.', bild: '', zeit: 20, punkte: 1, mehrfach: false, antworten: ['Richtig', 'Falsch'], richtig: [0] }];
  await p.evaluate(fr => DB.storeSet('quiz', { list: [{ id: 'qz1', titel: 'Tiere im Wald', n: 2, at: Date.now() }, { id: 'qz2', titel: 'Einmaleins', n: 8, at: Date.now() - 86400000 }], ordner: [] })
    .then(() => DB.storeSet('quiz-qz1', { id: 'qz1', titel: 'Tiere im Wald', fragen: fr })), fr);
  await p.evaluate("location.hash='#/quiz'"); await p.waitForSelector('.folie iframe'); const fz = p.frameLocator('.folie iframe');
  await fz.locator('[data-a=live]').first().waitFor();
  await p.evaluate(() => { window.knQuiz.joinUrl = pin => 'https://klassenkiste.ch/#/q' + (pin ? '/' + pin : ''); });
  await f.warte(3500);
  f.los(); await f.warte(1200);
  await f.hin(fz.locator('[data-a=live]').first()); await f.warte(1800);
  const pin = await p.evaluate('__D.quiz[0].pin'), toks = [];
  for (const [n, a] of [['Lena', 'eule'], ['Noah', 'fuchs'], ['Mia', 'igel'], ['David', 'otter'], ['Emma', 'hase'], ['Luca', 'baer']]) {
    toks.push(await p.evaluate(([pin, n, a]) => DB.quizJoin(pin, n, a).then(r => r.token), [pin, n, a])); await f.warte(550);
  }
  await f.warte(1200);
  await f.hin(fz.locator('[data-a=hLos]')); await f.warte(2000);
  for (let i = 0; i < toks.length; i++) { await p.evaluate(([t, a]) => DB.quizAnswer(t, 0, [a]), [toks[i], i === 3 ? 2 : 0]); await f.warte(450); }
  await f.warte(1500);
  if (await fz.locator('[data-a=hSkip]').isVisible()) await f.hin(fz.locator('[data-a=hSkip]'));
  await f.warte(3000);
  await f.hin(fz.locator('[data-a=hWeiter]')); await f.warte(3200);
  await f.fertig('quiz');
};

FILME.umfrage = async function () {
  const f = await Film.neu('umfrage'), p = f.p;
  const cid = await einrichten(f);
  await p.evaluate(`location.hash='#/umfrage/${cid}'`); await p.waitForSelector('[data-a=uTpl]'); await f.warte(3500);
  f.los(); await f.warte(1000);
  await f.hin(p.locator('[data-a=uTpl]').first()); await f.warte(1500);
  await f.hin(p.locator('[data-a=uStart]').first()); await f.warte(700);
  await f.hin(p.locator('[data-a=uStartK]')); await f.warte(1500);
  const kids = await p.evaluate(`__D.kids.filter(k=>k.class_id==='${cid}').map(k=>k.id)`);
  const setz = (q, k, v) => p.evaluate(([cid, k, q, v]) => { const s = __D.store[Object.keys(__D.store).find(x => x.endsWith('umfrage-' + cid))]; s.ans[q] = s.ans[q] || {}; s.ans[q][k] = v; }, [cid, k, q, v]);
  const cur = () => p.evaluate(cid => __D.store[Object.keys(__D.store).find(k => k.endsWith('umfrage-' + cid))].live.cur, cid);
  let q = await cur(); const wahl = [0, 1, 0, 2, 0, 1, 1, 0, 3, 0];
  for (let i = 0; i < 10; i++) { await setz(q, kids[i], [wahl[i]]); await f.warte(500); }
  await f.warte(1800);
  await f.hin(p.locator('[data-a=uNav][data-d="1"]')); await f.warte(1200);
  // Wortwolke: je öfter ein Wort, desto grösser
  q = await cur(); const w = [['lustig'], ['spannend', 'lustig'], ['lustig'], ['müde'], ['super', 'lustig'], ['spannend'], ['lustig', 'cool'],
    ['super'], ['lustig'], ['spannend', 'super'], ['toll'], ['lustig', 'spannend']];
  for (let i = 0; i < w.length && i < kids.length; i++) { await setz(q, kids[i], w[i]); await f.warte(450); }
  await f.warte(3500);
  await f.fertig('umfrage');
};

// sanft scrollen (Mausrad an der aktuellen Mausposition)
async function rolle(f, dy, schritte = 18) { for (let i = 0; i < schritte; i++) { await f.p.mouse.wheel(0, dy / schritte); await f.warte(30); } }

FILME.tafel = async function () {
  const f = await Film.neu('tafel'), p = f.p;
  const cid = await einrichten(f);
  await p.evaluate(`location.hash='#/wandtafel/${cid}'`); await p.waitForSelector('.matrix, .board'); await f.warte(3500);
  const info = await p.evaluate(cid => ({ subs: __D.subjects.filter(s => s.class_id === cid && s.active).map(s => s.id), kids: __D.kids.filter(k => k.class_id === cid).map(k => k.id) }), cid);
  const setz = (k, s, c) => p.evaluate(([cid, k, s, c]) => { __D.entries = __D.entries.filter(e => e.kid_id !== k); if (s) __D.entries.push({ kid_id: k, class_id: cid, subject_id: s, col: c }); }, [cid, k, s, c]);
  f.los(); await f.warte(1500);
  const plan = [[0, 0, 'klar'], [1, 0, 'frage'], [2, 1, 'helfen'], [3, 0, 'helfen'], [4, 1, 'klar'], [5, 2, 'frage'], [6, 0, 'klar'], [7, 1, 'frage'], [8, 2, 'klar'], [9, 3, 'klar'], [10, 0, 'klar'], [11, 3, 'helfen']];
  for (const [k, s, c] of plan) { await setz(info.kids[k], info.subs[s], c); await f.warte(700); }
  await f.warte(1500);
  await setz(info.kids[1], info.subs[0], 'klar'); await f.warte(1800);
  await setz(info.kids[5], info.subs[2], 'klar'); await f.warte(2500);
  await f.fertig('arbeitsstand');
};

FILME.heft = async function () {
  const f = await Film.neu('heft'), p = f.p;
  const cid = await einrichten(f);
  await p.evaluate(`location.hash='#/hausaufgaben/${cid}'`); await p.waitForTimeout(2500);
  const fr = p.frameLocator('.folie iframe'); await fr.locator('.dadd').first().waitFor(); await f.warte(2500);
  f.los(); await f.warte(1000);
  const eintrag = async (tag, art, fach, titel, zeit) => {
    await f.hin(fr.locator('.dadd').nth(tag)); await f.warte(800);
    if (art) await f.hin(fr.locator('button:has-text("' + art + '")').first());
    await f.hin(fr.locator('button:text-is("' + fach + '")').first());
    await f.hin(fr.locator('.inp.rt.t').first()); await f.tippe(titel, 55);
    if (zeit) { await f.hin(fr.locator('input.inp[placeholder*="Min"]').first()); await f.tippe(zeit, 55); }
    await f.warte(400); await f.hin(fr.locator('button:has-text("Eintragen")').last()); await f.warte(1200);
  };
  await eintrag(0, null, 'M', 'Mathbuch S. 24, Nr. 1–5', '20 Min.');
  await eintrag(2, null, 'E', 'Wörter Unit 2 üben', '10 Min.');
  await eintrag(4, 'Lernkontrolle', 'D', 'Diktat: Wörter mit ie', null);
  await f.warte(2500);
  await f.fertig('hausaufgabenheft');
};

FILME.eltern = async function () {
  const f = await Film.neu('eltern'), p = f.p;
  const cid = await einrichten(f, KINDER.slice(0, 8));
  // Gespräch mit Terminen und Anmeldungen der Eltern vorbereiten (wie nach ein paar Tagen)
  await p.evaluate(cid => {
    const sl = []; let m = 16 * 60; const hm = x => String(Math.floor(x / 60)).padStart(2, '0') + ':' + String(x % 60).padStart(2, '0');
    for (let i = 0; i < 8; i++, m += 25) sl.push({ id: 's' + i, d: '2026-11-24', t: hm(m), e: hm(m + 20) });
    const ks = __D.kids.filter(k => k.class_id === cid), wahl = [[0, 1, 2], [1, 3], [2, 4, 5], [0, 6], [3, 7], [5, 6, 7], [4], [1, 2, 6]], ans = {};
    ks.forEach((k, i) => { ans[k.id] = { name: 'Familie ' + k.name, slots: wahl[i].map(j => 's' + j), note: '', none: false, key: null, at: new Date().toISOString(), lp: false }; });
    __D.talks = [{ id: '7a1e0c2b-4d3f-4e5a-9b6c-1d2e3f4a5b6c', class_id: cid, token: 'tok1', cfg: { title: 'Elterngespräche November 2026', info: 'Die Gespräche finden im Schulzimmer statt.', open: false, slots: sl, diff: {}, fixed: {}, dur: 20, gap: 5 }, answers: ans, created_at: new Date().toISOString() }];
  }, cid);
  await p.evaluate(`location.hash='#/gespraeche/${cid}'`); await p.waitForSelector('.eg-ttitle'); await f.warte(3500);
  f.los(); await f.warte(900);
  await f.hin(p.locator('a.btn:has-text("Öffnen")').first());
  await f.warte(1800);
  await f.hin(p.locator('[data-a=egOpen]')); await f.warte(1500);
  const ziel = await p.evaluate(() => { const h = [...document.querySelectorAll('h2')].find(x => /Plan/.test(x.textContent)); return h ? h.getBoundingClientRect().top - 70 : 700; });
  await rolle(f, ziel, 45); await f.warte(1500);
  const fix = p.locator('text=fixieren >> visible=true').first(); if (await fix.count()) { await f.hin(fix); await f.warte(1200); }
  await f.warte(2000);
  await f.fertig('elterngespraeche');
};

// Bild quadratisch machen (durchsichtiger Rand), damit alle Kärtchen gleich gross sind
function quadrat(datei) {
  const aus = require('path').join(require('os').tmpdir(), 'vk-' + require('path').basename(datei));
  require('child_process').execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', datei, '-vf',
    "scale='min(400,iw*400/max(iw,ih))':'min(400,ih*400/max(iw,ih))',pad=400:400:(ow-iw)/2:(oh-ih)/2:color=0x00000000,format=yuva420p",
    '-c:v', 'libwebp', '-quality', '80', aus]);
  return fs.readFileSync(aus).toString('base64');
}
FILME.vokabel = async function () {
  const f = await Film.neu('vokabel'), p = f.p;
  // Vokabelkiste mit Bildern: für die Kleider in «U1 - Teil 3» die Zeichnungen der Lehrerin aus dem Kleiderschrank
  let html = fs.readFileSync(KN + '/werkstatt/originale/vokabelkiste.html', 'utf8');
  const m = html.match(/(<script[^>]*id=["']vk-content["'][^>]*>)([\s\S]*?)(<\/script>)/), d = JSON.parse(m[2]);
  const BILD = { shirt: 'shirt', trousers: 'trousers', jumper: 'jumper', tie: 'tie', shoe: 'shoes', skirt: 'skirt', dress: 'dress' };
  const teil = d.subjects[0].tree[0].kids[0].kids[2];
  const SRC = {};  // Bild → Wort, damit die Maus immer richtig wählt
  teil.words.forEach(w => {
    if (BILD[w.f]) { w.img = 'data:image/webp;base64,' + quadrat(KN + '/werkstatt/spiele/knobelspiele/kleider_bilder/karte-' + BILD[w.f] + '.webp'); SRC[w.f] = w.img; }
    else w.img = '-';  // Wörter ohne Zeichnung kommen in «Bild & Wort» nicht vor
  });
  html = html.replace(m[0], m[1] + JSON.stringify(d) + m[3]);
  const cid = await einrichten(f, KINDER, p => p.evaluate(h => DB.saveGame({ title: 'Vokabelkiste', fach: 'Englisch', thema: '', stufe: '4.–6. Klasse', html: h, for_all: true }), html));
  // Wortlisten der Klasse (so liest sie die Vokabelkiste im Portal)
  await p.evaluate(([cid, c]) => { const g = __D.games.find(x => x.title === 'Vokabelkiste'); __D.gsettings = __D.gsettings || {}; __D.gsettings[cid + '|' + g.id] = { content: c }; }, [cid, d]);
  await p.click('[data-a=tab] >> text=Übersicht'); await f.warte(800);
  await p.click('[data-a=vkOpen]'); await f.warte(4500);
  const fr = p.frameLocator('iframe[src*="vokabelkiste"]');
  f.los(); await f.warte(1000);
  await f.hin(fr.locator('text=Unit 1 >> visible=true').first(), false); await rolle(f, 420); await f.warte(800);
  await f.hin(fr.locator('text=Unit 1 >> visible=true').first()); await f.warte(1500);
  await f.hin(fr.locator('text=Teil 3 >> visible=true').first()); await f.warte(1800);
  // Übung «Bild & Wort»
  await f.hin(fr.locator('text=Bild & Wort >> visible=true').first()); await f.warte(2200);
  for (let i = 0; i < 4; i++) {
    // richtige Antwort suchen: Bild → Wort (.opt) oder Wort → Bild (.bopt)
    const n = await fr.locator('body').evaluate((b, SRC) => {
      const big = b.querySelector('.bbig img'), wort = b.querySelector('.bword');
      if (big) { const w = Object.keys(SRC).find(k => SRC[k] === big.getAttribute('src')); return [...b.querySelectorAll('.opt')].findIndex(o => o.textContent.replace(/^\d+/, '').trim() === w); }
      if (wort) { const w = wort.textContent.trim(); return [...b.querySelectorAll('.bopt')].findIndex(o => (o.querySelector('img') || {}).getAttribute && o.querySelector('img').getAttribute('src') === SRC[w]); }
      return -1;
    }, SRC);
    if (n < 0) break;
    await f.hin(fr.locator('[data-i="' + n + '"] >> visible=true').first()); await f.warte(2000);
  }
  await f.warte(1500);
  await f.fertig('vokabelkiste');
};

(async () => {
  for (const n of Object.keys(FILME)) if (!NUR.length || NUR.includes(n)) { try { await FILME[n](); } catch (e) { console.log(n, 'ABBRUCH', e.message.split('\n')[0]); process.exit(1); } }
})();
