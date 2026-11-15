// Hojas de referencia de "Mision Artemis: Mas alla de las paginas" (base lunar 2D, vista lateral).
// Dibuja los props en pixel art, compone dos escenas sobre los fondos con parallax, el mapa del nivel y la paleta.
// Uso: node generar_hojas.js   -> crea ../hojas_de_referencia/*.png y ../recursos/props/*.png
const fs = require('fs'), zlib = require('zlib'), path = require('path');
const RAIZ = path.resolve(__dirname, '..'), REC = path.join(RAIZ, 'recursos'), SAL = path.join(RAIZ, 'hojas_de_referencia');
const DIR_PROPS = path.join(REC, 'props');
fs.mkdirSync(SAL, { recursive: true }); fs.mkdirSync(DIR_PROPS, { recursive: true });

// ---------- PNG ----------
const CRC = new Uint32Array(256);
for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; CRC[n] = c >>> 0; }
function crc(b) { let c = 0xffffffff; for (let i = 0; i < b.length; i++) c = CRC[(c ^ b[i]) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }
function chunk(t, d) { const l = Buffer.alloc(4); l.writeUInt32BE(d.length); const td = Buffer.concat([Buffer.from(t), d]); const c = Buffer.alloc(4); c.writeUInt32BE(crc(td)); return Buffer.concat([l, td, c]); }
function savePNG(file, im, s = 1) {
  const w = im.w * s, h = im.h * s, row = w * 4 + 1, raw = Buffer.alloc(row * h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const si = (((y / s) | 0) * im.w + ((x / s) | 0)) * 4, di = y * row + 1 + x * 4;
    for (let k = 0; k < 4; k++) raw[di + k] = im.d[si + k];
  }
  const ih = Buffer.alloc(13); ih.writeUInt32BE(w, 0); ih.writeUInt32BE(h, 4); ih[8] = 8; ih[9] = 6;
  fs.writeFileSync(file, Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ih), chunk('IDAT', zlib.deflateSync(raw, { level: 9 })), chunk('IEND', Buffer.alloc(0))]));
}
function loadPNG(file) {
  const b = fs.readFileSync(file); let p = 8, w = 0, h = 0; const idat = [];
  while (p < b.length) {
    const len = b.readUInt32BE(p), t = b.toString('ascii', p + 4, p + 8), d = b.subarray(p + 8, p + 8 + len);
    if (t === 'IHDR') { w = d.readUInt32BE(0); h = d.readUInt32BE(4); if (d[8] !== 8 || d[9] !== 6) throw new Error('PNG no RGBA8: ' + file); }
    if (t === 'IDAT') idat.push(d);
    p += 12 + len;
  }
  const raw = zlib.inflateSync(Buffer.concat(idat)), im = newImg(w, h), bpp = 4, row = w * 4;
  for (let y = 0; y < h; y++) {
    const f = raw[y * (row + 1)], o = y * (row + 1) + 1, dst = y * row;
    for (let i = 0; i < row; i++) {
      const a = i >= bpp ? im.d[dst + i - bpp] : 0, u = y ? im.d[dst - row + i] : 0, c = y && i >= bpp ? im.d[dst - row + i - bpp] : 0;
      let v = raw[o + i];
      if (f === 1) v += a; else if (f === 2) v += u; else if (f === 3) v += (a + u) >> 1;
      else if (f === 4) { const q = a + u - c, pa = Math.abs(q - a), pb = Math.abs(q - u), pc = Math.abs(q - c); v += pa <= pb && pa <= pc ? a : pb <= pc ? u : c; }
      im.d[dst + i] = v & 255;
    }
  }
  return im;
}

// ---------- lienzo ----------
const hex = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
function newImg(w, h) { return { w, h, d: new Uint8ClampedArray(w * h * 4) }; }
function set(im, x, y, c, a = 1) {
  x = Math.round(x); y = Math.round(y); if (x < 0 || y < 0 || x >= im.w || y >= im.h) return;
  const i = (y * im.w + x) * 4;
  if (a >= 1 || im.d[i + 3] === 0) { im.d[i] = c[0]; im.d[i + 1] = c[1]; im.d[i + 2] = c[2]; im.d[i + 3] = a >= 1 ? 255 : Math.round(a * 255); return; }
  for (let k = 0; k < 3; k++) im.d[i + k] = im.d[i + k] * (1 - a) + c[k] * a;
}
function alpha(im, x, y) { if (x < 0 || y < 0 || x >= im.w || y >= im.h) return 0; return im.d[(y * im.w + x) * 4 + 3]; }
function blit(dst, src, ox, oy, flip = false) {
  for (let y = 0; y < src.h; y++) for (let x = 0; x < src.w; x++) {
    const i = (y * src.w + (flip ? src.w - 1 - x : x)) * 4;
    if (src.d[i + 3]) set(dst, ox + x, oy + y, [src.d[i], src.d[i + 1], src.d[i + 2]], src.d[i + 3] / 255);
  }
}
function recorte(src, x0, y0, w, h) { const o = newImg(w, h); for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const i = ((y0 + y) * src.w + x0 + x) * 4, j = (y * w + x) * 4; for (let k = 0; k < 4; k++) o.d[j + k] = src.d[i + k]; } return o; }
function F(im, x0, y0, x1, y1, c, a = 1) { for (let y = Math.round(y0); y <= Math.round(y1); y++) for (let x = Math.round(x0); x <= Math.round(x1); x++) set(im, x, y, c, a); }
// caja sombreada: luz arriba y a la izquierda (el Sol esta bajo, a la izquierda)
function R(im, x0, y0, x1, y1, t) {
  for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) set(im, x, y, y === y0 || x === x0 ? t[2] : y === y1 || x === x1 ? t[0] : t[1]);
}
function E(im, cx, cy, rx, ry, t) {
  for (let y = Math.floor(cy - ry); y <= cy + ry; y++) for (let x = Math.floor(cx - rx); x <= cx + rx; x++) {
    const dx = (x + 0.5 - cx) / rx, dy = (y + 0.5 - cy) / ry; if (dx * dx + dy * dy > 1) continue;
    const s = -dx * 0.6 - dy * 0.8, dz = (x + y) & 1;
    set(im, x, y, s > 0.5 || (s > 0.38 && dz) ? t[2] : s < -0.2 || (s < -0.05 && dz) ? t[0] : t[1]);
  }
}
function L(im, x0, y0, x1, y1, c, a = 1) { const n = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0), 1); for (let i = 0; i <= n; i++) set(im, x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, c, a); }
function contorno(im, color) {
  const o = newImg(im.w, im.h); blit(o, im, 0, 0);
  for (let y = 0; y < im.h; y++) for (let x = 0; x < im.w; x++) {
    if (alpha(im, x, y)) continue;
    if (alpha(im, x - 1, y) || alpha(im, x + 1, y) || alpha(im, x, y - 1) || alpha(im, x, y + 1)) set(o, x, y, color);
  }
  return o;
}
function hash(a, b = 0) { let h = (a * 374761393 + b * 668265263) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; }

// ---------- letra 3x5 ----------
const G = {
  A: '010101111101101', B: '110101110101110', C: '011100100100011', D: '110101101101110', E: '111100110100111', F: '111100110100100',
  G: '011100101101011', H: '101101111101101', I: '111010010010111', J: '001001001101010', K: '101101110101101', L: '100100100100111',
  M: '101111111101101', N: '101111111111101', O: '111101101101111', P: '110101110100100', Q: '010101101110011', R: '110101110101101',
  S: '011100010001110', T: '111010010010010', U: '101101101101111', V: '101101101101010', W: '101101111111101', X: '101101010101101',
  Y: '101101010010010', Z: '111001010100111', 0: '011101101101110', 1: '010110010010111', 2: '110001010100111', 3: '110001010001110',
  4: '101101111001001', 5: '111100110001110', 6: '111100111101111', 7: '111001010010010', 8: '111101111101111', 9: '111101111001111',
  '.': '000000000000010', '=': '000111000111000', '-': '000000111000000', ':': '000010000010000', '/': '001001010100100', '%': '101001010100101',
  '+': '000010111010000', '?': '110001010000010', '!': '010010010000010', ',': '000000000010100', '(': '001010010010001', ')': '100010010010100',
};
function txt(im, s, x, y, c, k = 1) {
  s = String(s).toUpperCase();
  for (let i = 0; i < s.length; i++) { const g = G[s[i]]; if (g) for (let j = 0; j < 15; j++) if (g[j] === '1') F(im, x + (i * 4 + j % 3) * k, y + ((j / 3) | 0) * k, x + (i * 4 + j % 3) * k + k - 1, y + ((j / 3) | 0) * k + k - 1, c); }
}
const txtW = (s, k = 1) => (String(s).length * 4 - 1) * k;
const txtC = (im, s, cx, y, c, k = 1) => txt(im, s, Math.round(cx - txtW(s, k) / 2), y, c, k);

// ---------- paleta (rampas de 3 tonos: oscuro, medio, claro) ----------
const P = {
  casco: ['#8f8672', '#d9d2c0', '#f6f1e4'], metal: ['#3d4252', '#6a6f7d', '#a9adb8'], oscuro: ['#161b2b', '#2a3040', '#3d4660'],
  cian: ['#2a9e9b', '#62e4e0', '#c3fbf8'], ambar: ['#a8601a', '#f2b134', '#ffe08a'], verde: ['#2c6e3a', '#8fd46a', '#c9f2a0'],
  magenta: ['#8a2a5c', '#e0559a', '#ffa6cf'], naranja: ['#a8401a', '#f08a5d', '#ffc09a'], azul: ['#16306e', '#2f62c4', '#7fb1f2'],
  oro: ['#7d5210', '#d39528', '#f6d277'], rojo: ['#8f1f22', '#d83a3a', '#f07070'], regolito: ['#4a4e68', '#7c8199', '#c4c9de'],
  vidrio: ['#1c3a52', '#3f86a8', '#a8e4f0'], hielo: ['#7fa9b0', '#cfeff0', '#f4ffff'],
};
const NOMBRES = { casco: 'CASCO CREMA', metal: 'METAL', oscuro: 'SOMBRA', cian: 'OXIGENO', ambar: 'ENERGIA', verde: 'ALIMENTOS', magenta: 'RADIACION', naranja: 'ALERTA', azul: 'PANEL SOLAR', oro: 'LAMINA ORO', rojo: 'BALIZA', regolito: 'REGOLITO', vidrio: 'VIDRIO', hielo: 'HIELO' };
const HEXP = JSON.parse(JSON.stringify(P));
for (const k in P) P[k] = P[k].map(hex);
const TINTA = hex('#12141f'), CREMA = hex('#f6e8c8'), CIELO = hex('#0b0e1a'), BLANCO = hex('#f2efe6'), SUAVE = hex('#aeb6c8');

// ---------- props (cada uno: imagen con la base en la ultima fila, y sus luces) ----------
function cupula() {
  const im = newImg(128, 72);
  E(im, 64, 72, 60, 62, P.casco);
  for (const lon of [-1.0, -0.5, 0, 0.5, 1.0]) for (let a = 0; a < 1.5; a += 0.01) set(im, 64 + 60 * Math.sin(lon) * Math.cos(a), 72 - 62 * Math.sin(a), P.casco[0]);
  for (const lat of [0.52, 1.0]) { const y = Math.round(72 - 62 * Math.sin(lat)), hw = 60 * Math.cos(lat); F(im, 64 - hw + 1, y, 64 + hw - 1, y, P.casco[0]); }
  R(im, 2, 62, 125, 71, P.metal);
  for (let x = 8; x < 122; x += 10) set(im, x, 66, P.cian[1]);
  for (const wx of [24, 100]) { E(im, wx, 47, 7, 7, P.metal); E(im, wx, 47, 5, 5, P.ambar); }
  R(im, 51, 34, 77, 71, P.metal); F(im, 54, 39, 74, 70, P.oscuro[0]); F(im, 57, 42, 71, 52, P.vidrio[1]); F(im, 57, 42, 71, 43, P.vidrio[2]);
  F(im, 54, 36, 74, 37, P.cian[1]);
  for (let x = 54; x <= 74; x++) F(im, x, 68, x, 70, ((x >> 2) & 1) ? P.ambar[1] : P.oscuro[0]);
  F(im, 63, 2, 64, 10, P.metal[1]); F(im, 63, 0, 64, 1, P.rojo[1]);
  return { im, luces: [[24, 47, 16, P.ambar[1]], [100, 47, 16, P.ambar[1]], [64, 40, 12, P.cian[1]], [64, 1, 7, P.rojo[1]]] };
}
function invernadero() {
  const im = newImg(112, 48);
  const dentro = (x, y) => { const dx = x < 14 ? 14 - x : x > 97 ? x - 97 : 0, dy = y < 16 ? 16 - y : y > 29 ? y - 29 : 0; return Math.hypot(dx, dy) <= 10; };
  for (let y = 6; y <= 39; y++) for (let x = 4; x <= 107; x++) if (dentro(x, y)) set(im, x, y, hex('#10323a'));
  for (let y = 11; y <= 20; y++) for (let x = 8; x <= 103; x++) if (dentro(x, y) && ((x + y) & 1 || y < 14)) set(im, x, y, P.magenta[0], 0.5);
  F(im, 12, 9, 99, 10, P.magenta[2]);
  F(im, 8, 35, 103, 36, P.metal[0]);
  for (let x = 10; x <= 100; x += 5) {
    const h = 6 + Math.floor(hash(x, 7) * 9);
    F(im, x, 35 - h, x, 34, P.verde[0]);
    for (let k = 2; k < h; k += 3) { set(im, x - 1, 35 - k, P.verde[1]); set(im, x + 1, 34 - k, P.verde[1]); }
    F(im, x - 1, 35 - h, x + 1, 35 - h, P.verde[2]);
    if (hash(x, 3) > 0.6) set(im, x + 1, 33 - (h >> 1), P.rojo[1]);
  }
  for (let i = 0; i < 26; i++) { set(im, 20 + i, 30 - i, P.vidrio[2], 0.35); set(im, 23 + i, 30 - i, P.vidrio[2], 0.2); set(im, 70 + i * 0.6, 26 - i * 0.6, P.vidrio[2], 0.3); }
  for (const x of [28, 52, 76]) F(im, x, 6, x + 1, 39, P.casco[1]);
  for (let y = 6; y <= 39; y++) for (let x = 4; x <= 107; x++) if (dentro(x, y) && !(dentro(x - 2, y) && dentro(x + 2, y) && dentro(x, y - 2) && dentro(x, y + 2))) set(im, x, y, y < 20 ? P.casco[2] : P.casco[1]);
  R(im, 0, 40, 111, 47, P.metal);
  for (let x = 6; x < 110; x += 12) set(im, x, 44, P.cian[1]);
  return { im, luces: [[56, 20, 34, P.magenta[1]], [30, 28, 18, P.verde[1]], [84, 28, 18, P.verde[1]]] };
}
function paneles() {
  const im = newImg(56, 44);
  const yt = x => Math.round(24 - (x - 2) * 16 / 51);
  F(im, 27, yt(27) + 8, 28, 40, P.metal[1]); L(im, 27, 30, 18, 40, P.metal[0]); R(im, 18, 40, 37, 43, P.metal);
  for (let x = 2; x <= 53; x++) for (let k = 0; k <= 11; k++) {
    const c = k === 0 ? P.azul[2] : k === 11 ? P.metal[0] : (x - 2) % 9 === 0 || k === 6 ? P.azul[0] : ((x * 3 + k * 5) % 17 === 0 ? P.azul[2] : P.azul[1]);
    set(im, x, yt(x) + k, c);
  }
  return { im, luces: [] };
}
function antena() {
  const im = newImg(48, 88);
  for (let y = 32; y < 80; y++) { set(im, 20, y, P.metal[2]); set(im, 27, y, P.metal[1]); }
  for (let y = 32; y < 80; y += 8) { L(im, 20, y, 27, y + 7, P.metal[0]); L(im, 27, y, 20, y + 7, P.metal[1]); }
  R(im, 12, 80, 35, 87, P.metal); set(im, 24, 84, P.cian[1]);
  F(im, 22, 28, 25, 33, P.metal[1]);
  E(im, 24, 20, 22, 11, P.casco); E(im, 25, 18, 17, 7, ['#6f6858', '#8f8672', '#b5ad98'].map(hex));
  L(im, 25, 18, 34, 4, P.metal[2]); L(im, 14, 14, 34, 4, P.metal[1]); F(im, 33, 2, 35, 4, P.rojo[1]);
  return { im, luces: [[34, 3, 8, P.rojo[1]]] };
}
function estacion() {
  const im = newImg(24, 44);
  R(im, 6, 12, 17, 39, P.casco); R(im, 3, 3, 20, 13, P.metal); F(im, 5, 5, 18, 10, P.oscuro[0]); F(im, 6, 6, 14, 9, P.ambar[1]); F(im, 15, 6, 17, 9, P.ambar[0]);
  for (const [x, y] of [[13, 17], [12, 18], [11, 19], [10, 20], [11, 20], [12, 20], [13, 20], [12, 21], [11, 22], [10, 23], [12, 16], [11, 24]]) set(im, x, y, P.ambar[0]);
  for (const [x, y] of [[13, 17], [12, 18], [11, 19], [12, 20], [13, 20], [12, 21], [11, 22]]) set(im, x, y, P.ambar[1]);
  L(im, 18, 22, 22, 31, P.oscuro[1]); F(im, 21, 31, 23, 34, P.metal[2]);
  set(im, 9, 35, P.cian[1]); set(im, 14, 35, P.cian[1]); R(im, 3, 40, 20, 43, P.metal);
  return { im, luces: [[11, 8, 10, P.ambar[1]]] };
}
function recarga() {
  const im = newImg(32, 44);
  for (const bx of [4, 18]) { R(im, bx, 11, bx + 9, 39, P.hielo); F(im, bx + 1, 9, bx + 8, 10, P.hielo[1]); F(im, bx, 20, bx + 9, 22, P.cian[1]); F(im, bx, 31, bx + 9, 32, P.cian[0]); set(im, bx + 2, 14, BLANCO); set(im, bx + 2, 15, BLANCO); }
  R(im, 2, 4, 29, 8, P.metal); F(im, 14, 9, 17, 39, P.metal[0]); F(im, 15, 1, 16, 3, P.cian[1]); F(im, 14, 24, 17, 27, P.cian[2]);
  R(im, 0, 40, 31, 43, P.metal);
  return { im, luces: [[16, 24, 14, P.cian[1]]] };
}
function deposito() {
  const im = newImg(56, 40);
  for (let y = 8; y <= 30; y++) for (let x = 2; x <= 53; x++) {
    const dx = x < 13 ? 13 - x : x > 42 ? x - 42 : 0, dy = y - 19; if (Math.hypot(dx, dy) > 11) continue;
    const d = (x + y) & 1; set(im, x, y, y < 12 || (y < 15 && d) ? P.casco[2] : y > 26 || (y > 23 && d) ? P.casco[0] : P.casco[1]);
    if (y > 24 && hash(x, y) > 0.5) set(im, x, y, P.cian[2], 0.6);
    if (x >= 18 && x <= 21) set(im, x, y, y < 13 ? P.naranja[2] : y > 25 ? P.naranja[0] : P.naranja[1]);
  }
  R(im, 9, 31, 13, 39, P.metal); R(im, 42, 31, 46, 39, P.metal); F(im, 30, 5, 31, 8, P.metal[1]); F(im, 30, 4, 38, 5, P.metal[2]);
  F(im, 34, 15, 38, 15, P.cian[1]); F(im, 34, 17, 36, 17, P.cian[1]);
  return { im, luces: [] };
}
function rover() {
  const im = newImg(64, 36);
  F(im, 12, 3, 12, 15, P.metal[2]); F(im, 9, 2, 15, 3, P.casco[1]); set(im, 12, 1, P.rojo[1]);
  R(im, 6, 11, 26, 14, P.azul); R(im, 4, 15, 59, 23, P.casco); F(im, 4, 21, 59, 21, P.naranja[1]);
  R(im, 30, 3, 55, 15, P.casco); F(im, 40, 5, 53, 12, P.oro[1]); F(im, 40, 5, 53, 6, P.oro[2]); F(im, 50, 9, 53, 12, P.oro[0]);
  F(im, 60, 17, 61, 19, P.ambar[2]);
  for (const wx of [11, 32, 53]) { E(im, wx, 29, 6.5, 6.5, P.oscuro); E(im, wx, 29, 2.5, 2.5, P.metal); L(im, wx, 23, wx, 26, P.metal[0]); }
  return { im, luces: [[61, 18, 9, P.ambar[2]]] };
}
function cajaCruda(t) {
  const im = newImg(16, 14);
  R(im, 0, 0, 15, 13, t); F(im, 1, 3, 14, 3, t[0]); F(im, 7, 1, 8, 12, t[0]); F(im, 11, 7, 13, 9, P.cian[1]);
  for (const [x, y] of [[0, 0], [15, 0], [0, 13], [15, 13]]) set(im, x, y, P.metal[2]);
  return im;
}
const caja = t => ({ im: cajaCruda(t), luces: [] });
function pila() {
  const im = newImg(40, 30);
  blit(im, cajaCruda(P.naranja), 0, 16); blit(im, cajaCruda(P.azul), 20, 16); blit(im, cajaCruda(P.verde), 10, 2);
  return { im, luces: [] };
}
function nave() {
  const im = newImg(72, 80);
  for (const d of [0, 1]) { L(im, 18 + d, 52, 5 + d, 76, P.metal[1]); L(im, 53 - d, 52, 66 - d, 76, P.metal[1]); L(im, 18, 40, 9, 64, P.metal[0]); L(im, 53, 40, 62, 64, P.metal[0]); }
  F(im, 1, 77, 11, 79, P.metal[2]); F(im, 60, 77, 70, 79, P.metal[2]);
  for (let y = 57; y <= 68; y++) { const hw = 4 + (y - 57) * 0.8; F(im, 36 - hw, y, 36 + hw, y, P.oscuro[y & 1 ? 1 : 2]); }
  F(im, 35, 6, 36, 15, P.metal[1]); set(im, 35, 5, P.rojo[1]);
  E(im, 36, 30, 18, 16, P.casco);
  R(im, 14, 30, 57, 56, P.oro);
  for (let y = 31; y < 56; y++) for (let x = 15; x < 57; x++) { const v = hash(x >> 1, y >> 1); if (v > 0.8) set(im, x, y, P.oro[2]); else if (v < 0.15) set(im, x, y, P.oro[0]); }
  F(im, 18, 34, 27, 43, P.oscuro[1]); F(im, 44, 34, 53, 43, P.oscuro[1]); F(im, 19, 35, 26, 36, P.azul[1]); F(im, 45, 35, 52, 36, P.azul[1]);
  R(im, 31, 40, 40, 55, P.metal); F(im, 33, 42, 38, 54, P.oscuro[0]); F(im, 33, 42, 38, 43, P.cian[1]);
  return { im, luces: [[36, 48, 12, P.cian[1]]] };
}
function veta(tipo) {
  const im = newImg(32, 20);
  E(im, 16, 22, 15, 14, tipo === 'hielo' ? ['#2b2f48', '#474c68', '#7c8199'].map(hex) : P.regolito);
  const pico = (cx, h, t) => { for (let i = 0; i < h; i++) { const w = i < h * 0.5 ? 1 : 0; F(im, cx - w, 14 - i, cx + w, 14 - i, i % 3 === 0 ? t[2] : t[1]); set(im, cx + w, 14 - i, t[0]); } };
  if (tipo === 'hielo') { pico(9, 6, P.cian); pico(16, 10, P.cian); pico(23, 7, P.cian); set(im, 16, 3, BLANCO); }
  else if (tipo === 'ilmenita') { for (const [x, y, s] of [[7, 11, 4], [14, 8, 5], [21, 11, 4]]) { R(im, x, y, x + s, y + s, P.oscuro); set(im, x + 1, y + 1, P.oro[1]); set(im, x + s - 1, y + 2, P.naranja[1]); } }
  else { for (let x = 6; x < 26; x++) for (let y = 9; y < 14; y++) if (hash(x, y) > 0.55) set(im, x, y, P.regolito[2]); F(im, 15, 2, 15, 9, P.metal[2]); F(im, 16, 2, 20, 4, P.cian[1]); }
  return { im, luces: tipo === 'hielo' ? [[16, 8, 12, P.cian[1]]] : [] };
}
function maquina() {
  const im = newImg(96, 88);
  for (const tx of [4, 82]) { R(im, tx, 12, tx + 9, 87, P.metal); for (let y = 16; y < 80; y += 12) { L(im, tx + 1, y, tx + 8, y + 9, P.metal[0]); L(im, tx + 8, y, tx + 1, y + 9, P.metal[0]); } }
  R(im, 0, 4, 95, 13, P.ambar);
  for (let y = 6; y <= 11; y++) for (let x = 1; x <= 94; x++) if (((x + y) >> 2) & 1) set(im, x, y, P.oscuro[0]);
  R(im, 40, 14, 55, 20, P.metal); F(im, 47, 21, 48, 40, P.metal[0]); F(im, 42, 40, 53, 42, P.metal[2]);
  for (const x of [42, 53]) F(im, x, 43, x, 45, P.metal[2]);
  R(im, 43, 45, 52, 54, P.casco); F(im, 43, 49, 52, 49, P.naranja[1]);
  for (const [x, y] of [[40, 47], [55, 50], [39, 53], [56, 44], [41, 57]]) set(im, x, y, P.ambar[2]);
  for (let y = 52; y <= 72; y++) { const k = (y - 52) * 0.3; F(im, 17 + k, y, 39 - k, y, y < 56 ? P.casco[2] : P.casco[1]); set(im, 39 - k, y, P.casco[0]); }
  F(im, 15, 50, 41, 51, P.casco[2]);
  for (const [x, y] of [[28, 56], [28, 57], [28, 58], [28, 59], [26, 59], [30, 59], [27, 60], [29, 60], [28, 61], [27, 59], [29, 59], [28, 60]]) set(im, x, y, P.cian[1]);
  F(im, 27, 73, 29, 79, P.metal[1]);
  R(im, 60, 56, 78, 79, P.casco); F(im, 62, 58, 76, 67, P.oscuro[0]); F(im, 63, 60, 71, 61, P.cian[1]); F(im, 63, 63, 68, 64, P.cian[0]); F(im, 73, 60, 75, 65, P.verde[1]);
  set(im, 63, 71, P.ambar[1]); set(im, 66, 71, P.rojo[1]); set(im, 69, 71, P.verde[1]); F(im, 63, 74, 75, 75, P.metal[1]);
  R(im, 14, 80, 81, 87, P.metal); for (let x = 18; x < 80; x += 8) set(im, x, 84, P.cian[1]);
  return { im, luces: [[48, 50, 14, P.ambar[1]], [69, 62, 12, P.cian[1]]] };
}
// cohete por fases: lo construido se dibuja; lo que falta se ve como plano de puntos cian (la imaginacion del lector)
function cohete(fase) {
  const lleno = newImg(56, 160), cx = 28;
  const cil = (y0, y1, hw, t) => { for (let y = y0; y <= y1; y++) for (let x = cx - hw; x < cx + hw; x++) { const k = (x - cx + hw) / (2 * hw), d = (x + y) & 1; set(lleno, x, y, k < 0.22 || (k < 0.32 && d) ? t[2] : k > 0.8 || (k > 0.68 && d) ? t[0] : t[1]); } };
  F(lleno, cx - 1, 0, cx, 11, P.metal[1]); F(lleno, cx - 2, 3, cx + 1, 4, P.metal[2]);
  for (let y = 12; y <= 39; y++) { const hw = Math.round(1 + (y - 12) * 11 / 27); for (let x = cx - hw; x < cx + hw; x++) { const k = (x - cx + hw) / (2 * hw), t = y < 20 ? P.rojo : P.casco; set(lleno, x, y, k < 0.25 ? t[2] : k > 0.75 ? t[0] : t[1]); } }
  cil(40, 79, 12, P.casco); cil(80, 83, 12, P.oscuro);
  E(lleno, cx, 54, 5, 5, P.metal); E(lleno, cx, 54, 3.5, 3.5, P.oro); F(lleno, cx - 12, 68, cx + 11, 69, P.cian[1]); F(lleno, cx - 12, 44, cx + 11, 44, P.casco[0]);
  cil(84, 127, 12, P.naranja); F(lleno, cx - 12, 100, cx + 11, 101, P.naranja[0]); F(lleno, cx - 12, 116, cx + 11, 117, P.naranja[0]);
  for (const bx of [10, 40]) { for (let y = 92; y <= 97; y++) { const hw = Math.round((y - 91) / 2); F(lleno, bx + 3 - hw, y, bx + 2 + hw, y, P.casco[2]); } for (let y = 98; y <= 150; y++) for (let x = bx; x < bx + 6; x++) set(lleno, x, y, x === bx ? P.casco[2] : x === bx + 5 ? P.casco[0] : P.casco[1]); F(lleno, bx, 120, bx + 5, 121, P.oscuro[1]); for (let y = 151; y <= 155; y++) F(lleno, bx + 1 - (y > 152 ? 1 : 0), y, bx + 4 + (y > 152 ? 1 : 0), y, P.oscuro[1]); }
  cil(128, 140, 12, P.metal);
  for (const nx of [20, 28, 36]) for (let y = 141; y <= 151; y++) { const hw = 2 + ((y - 141) >> 2); F(lleno, nx - hw, y, nx + hw - 1, y, y & 1 ? P.oscuro[1] : P.oscuro[2]); }
  R(lleno, 4, 154, 51, 159, P.metal); for (let x = 5; x <= 50; x++) if ((x >> 2) & 1) F(lleno, x, 156, x, 157, P.ambar[1]);
  const limite = [160, 128, 84, 40, 0][fase];
  const hecho = newImg(56, 160);
  for (let y = limite; y < 160; y++) for (let x = 0; x < 56; x++) { const i = (y * 56 + x) * 4; if (lleno.d[i + 3]) set(hecho, x, y, [lleno.d[i], lleno.d[i + 1], lleno.d[i + 2]]); }
  const im = contorno(hecho, TINTA);
  for (let y = 0; y < limite; y++) for (let x = 0; x < 56; x++) {
    if (!alpha(lleno, x, y)) continue;
    const borde = !alpha(lleno, x - 1, y) || !alpha(lleno, x + 1, y) || !alpha(lleno, x, y - 1) || !alpha(lleno, x, y + 1);
    if (borde && ((x + y) & 1)) set(im, x, y, P.cian[1]); else if ((x % 4 === 0 && y % 4 === 0)) set(im, x, y, P.cian[0], 0.7);
  }
  return { im, luces: fase < 4 ? [[28, limite - 10, 16, P.cian[1]]] : [[28, 54, 10, P.oro[2]]], sinContorno: true };
}
function refugio() {
  const im = newImg(80, 36);
  E(im, 40, 37, 38, 31, P.regolito);
  for (let y = 7; y < 36; y++) for (let x = 2; x < 78; x++) { if (!alpha(im, x, y)) continue; const fila = (y / 5) | 0; if (y % 5 === 0 || (x + (fila & 1) * 5) % 10 === 0) set(im, x, y, P.regolito[0], 0.55); }
  R(im, 29, 14, 51, 35, P.metal); F(im, 32, 18, 48, 35, P.oscuro[0]); F(im, 32, 18, 48, 19, P.cian[1]);
  F(im, 35, 10, 45, 12, P.magenta[1]); F(im, 38, 8, 42, 9, P.magenta[2]);
  for (const [x, y] of [[40, 23], [39, 24], [41, 24], [38, 25], [42, 25], [40, 26], [40, 27]]) set(im, x, y, P.magenta[1]);
  return { im, luces: [[40, 10, 10, P.magenta[1]]] };
}
// las banderas van rigidas, con una varilla horizontal arriba: en la Luna no hay viento que las extienda
function bandera(tipo) {
  const im = newImg(30, 52);
  F(im, 1, 2, 2, 51, P.metal[1]); F(im, 1, 2, 1, 51, P.metal[2]); F(im, 1, 2, 27, 2, P.metal[2]); F(im, 0, 50, 4, 51, P.regolito[1]);
  for (let y = 0; y < 14; y++) for (let x = 0; x < 24; x++) {
    let c;
    if (tipo === 'usa') c = x < 10 && y < 8 ? (x % 3 === 1 && y % 2 === 1 ? BLANCO : hex('#22408f')) : (y >> 1) % 2 === 0 ? hex('#c8323c') : BLANCO;
    else if (tipo === 'ecuador') c = y < 7 ? hex('#f6d32d') : y < 11 ? hex('#1f4fb0') : hex('#d2202f');
    else c = y > 11 ? hex('#dfeefa') : hex('#f4f9fd');
    set(im, 3 + x, 3 + y, c);
  }
  if (tipo === 'ecuador') { F(im, 13, 8, 16, 12, hex('#7a5a2a')); F(im, 14, 9, 15, 10, hex('#62b0e0')); F(im, 14, 11, 15, 11, hex('#3c8a4a')); F(im, 13, 7, 16, 7, hex('#3a2a1a')); }
  if (tipo === 'ieee') {
    const pts = [[7, 12], [10, 11], [12, 6], [14, 5], [16, 7], [18, 12], [20, 13], [22, 11], [24, 9]];
    for (let k = 0; k < pts.length - 1; k++) for (const d of [0, 1]) L(im, pts[k][0], pts[k][1] + d, pts[k + 1][0], pts[k + 1][1] + d, hex('#1f8a3a'));
    F(im, 6, 15, 23, 15, hex('#2a3560')); F(im, 24, 14, 25, 15, hex('#2f62c4'));
  }
  return { im, luces: [] };
}
function meteorito() {
  const im = newImg(44, 26);
  for (let i = 0; i < 30; i++) { const a = i / 30; L(im, i, i * 0.5, i, i * 0.5 + 1 + a * 4, i % 3 ? P.naranja[1] : P.ambar[2], 0.15 + a * 0.7); }
  E(im, 35, 19, 5, 5, ['#5a2a1a', '#a8501a', '#ffb46b'].map(hex)); set(im, 33, 17, P.ambar[2]);
  return { im, luces: [[35, 19, 12, P.naranja[1]]], sinContorno: true };
}

const PROPS = {
  cupula: ['P01', 'CUPULA HABITAT', cupula], invernadero: ['P02', 'INVERNADERO', invernadero], refugio: ['P03', 'REFUGIO', refugio],
  nave: ['P04', 'NAVE DE CARGA', nave], antena: ['P05', 'ANTENA', antena], paneles: ['P06', 'PANEL SOLAR', paneles],
  recarga: ['P07', 'OXIGENO', recarga], estacion: ['P08', 'CARGA', estacion], deposito: ['P09', 'COMBUSTIBLE', deposito],
  rover: ['P10', 'ROVER', rover], pila: ['P11', 'SUMINISTROS', pila], caja_a: ['P12', 'CAJA', () => caja(P.naranja)],
  veta_ilmenita: ['P13', 'ILMENITA', () => veta('ilmenita')], veta_regolito: ['P14', 'REGOLITO', () => veta('regolito')], veta_hielo: ['P15', 'HIELO', () => veta('hielo')],
  maquina: ['P16', 'CONSTRUCTORA', maquina],
  cohete_1: ['P17', 'FASE 1', () => cohete(1)], cohete_2: ['P18', 'FASE 2', () => cohete(2)], cohete_3: ['P19', 'FASE 3', () => cohete(3)], cohete_4: ['P20', 'FASE 4', () => cohete(4)],
  bandera_usa: ['P21', 'EE.UU.', () => bandera('usa')], bandera_ecuador: ['P22', 'ECUADOR', () => bandera('ecuador')], bandera_ieee: ['P23', 'IEEE IAS', () => bandera('ieee')],
  meteorito: ['F01', 'METEORITO', meteorito],
};
const prop = {};
for (const id in PROPS) {
  const p = PROPS[id][2]();
  prop[id] = { id: PROPS[id][0], nombre: PROPS[id][1], im: p.sinContorno ? p.im : contorno(p.im, TINTA), luces: p.luces, d: p.sinContorno ? 0 : 0 };
  savePNG(path.join(DIR_PROPS, id + '.png'), prop[id].im);
}

// ---------- personajes (hojas de Jean, cuadros de 32 x 32) ----------
const pj = {};
for (const id of ['jugador', 'comandante', 'geologa', 'ingeniero', 'piloto', 'medica']) pj[id] = loadPNG(path.join(REC, 'personajes', id + '.png'));
const cuadro = (id, col, fila) => recorte(pj[id], col * 32, fila * 32, 32, 32);

// ---------- mundo: un solo eje, de izquierda a derecha ----------
const ZONAS = [[0, 480, 'Z1 PISTA DE CARGA'], [480, 1280, 'Z2 BASE POLO SUR'], [1280, 1680, 'Z3 ASTILLERO'], [1680, 2240, 'Z4 CAMPO MINERO'], [2240, 2560, 'Z5 CRATER EN SOMBRA']];
const ANCHO_MUNDO = 2560;
const COLOCADOS = [
  ['nave', 60], ['pila', 150], ['caja_a', 206], ['pila', 300], ['veta_regolito', 400],
  ['recarga', 500], ['cupula', 552], ['estacion', 700], ['invernadero', 748], ['refugio', 884], ['paneles', 990], ['paneles', 1054], ['antena', 1130], ['pila', 1200],
  ['maquina', 1300], ['cohete', 1420], ['deposito', 1500], ['estacion', 1580], ['caja_a', 1620],
  ['rover', 1716], ['veta_ilmenita', 1820], ['veta_regolito', 1910], ['pila', 1954], ['veta_ilmenita', 2010], ['paneles', 2064], ['estacion', 2128], ['veta_ilmenita', 2170],
  ['recarga', 2248], ['veta_hielo', 2330], ['veta_hielo', 2410], ['veta_hielo', 2490],
];
const GENTE = [['piloto', 236], ['comandante', 716], ['medica', 850], ['ingeniero', 1390], ['geologa', 1860]];
function alturaCruda(tx) {
  const wx = tx * 16;
  if (wx >= 480 && wx < 1680) return 0;
  const borde = Math.min(Math.abs(wx - 480), Math.abs(wx - 1680)) / 64;
  let h = Math.round(Math.min(1, borde) * (1.5 * Math.sin(tx * 0.45) + 1.2 * Math.sin(tx * 0.17 + 2))) * 8;
  if (wx >= 2240) h -= Math.round((wx - 2240) / 40) * 8;
  return h;
}
const ALT = []; for (let tx = 0; tx < ANCHO_MUNDO / 16; tx++) ALT.push(alturaCruda(tx));
function aplanar(x0, w) { const a = Math.max(0, x0 >> 4), b = Math.min(ALT.length - 1, (x0 + w - 1) >> 4), h = ALT[(a + b) >> 1]; for (let t = a; t <= b; t++) ALT[t] = h; return h; }
const nombreProp = (id, fase) => id === 'cohete' ? 'cohete_' + fase : id;
for (const [id, x] of COLOCADOS) aplanar(x, prop[nombreProp(id, 2)].im.w);
for (const [, x] of GENTE) aplanar(x + 8, 16);
const altura = wx => ALT[Math.max(0, Math.min(ALT.length - 1, wx >> 4))];

function colorSuelo(wx, d, y) {
  const sombra = wx >= 2240, base = wx >= 480 && wx < 1680;
  let c;
  if (base && d < 4) { c = d === 0 ? P.metal[2] : d === 3 ? P.oscuro[1] : (wx % 16 === 0 ? P.metal[0] : P.metal[1]); if (d === 1 && wx % 16 === 8) c = P.metal[2]; if (d === 2 && (wx >> 3) % 9 === 0) c = P.ambar[1]; return c; }
  // bajo la cubierta: soportes, una tuberia de oxigeno y un cable de energia
  if (base && d < 14) { if (wx % 48 < 3) return P.metal[d === 4 ? 1 : 0]; if (d === 6) return (wx >> 3) % 6 === 0 ? P.cian[1] : P.cian[0]; if (d === 9) return (wx >> 2) % 9 === 0 ? P.ambar[1] : P.ambar[0]; if (d < 11) return hex('#1c2032'); }
  if (d === 0) c = P.regolito[2]; else if (d <= 2) c = hex('#9499b3');
  else { const v = hash(wx >> 2, y >> 2); c = hex(v < 0.25 ? '#4a4e68' : v < 0.7 ? '#565b78' : '#666b88'); if (d > 20 && hash(wx >> 1, y >> 1) < (d - 20) / 44) c = hex('#34384f'); if (hash(wx, y) > 0.985) c = P.regolito[1]; }
  if (sombra) { c = c.map(v => v * 0.5); if (d < 3 && hash(wx, 99) > 0.8) c = P.cian[d === 0 ? 2 : 0]; }
  return c;
}
function luz(im, x, y, r, c, fuerza = 0.4) {
  for (let yy = Math.floor(y - r); yy <= y + r; yy++) for (let xx = Math.floor(x - r); xx <= x + r; xx++) {
    const d = Math.hypot(xx - x, yy - y) / r; if (d >= 1) continue;
    const a = Math.floor((1 - d) * 3 + ((xx + yy) & 1) * 0.5) / 3 * fuerza; if (a > 0) set(im, xx, yy, c, Math.min(a, 0.9));
  }
}
function capas(escena) { return ['capa_0_espacio', 'capa_0b_sol_tierra', 'capa_1_montanas_lejanas', 'capa_2_montanas_medias', 'capa_3_colinas_cercanas'].map(n => loadPNG(path.join(REC, 'fondos_luna', escena, n + '.png'))); }
const FRAC = [0.02, 0.06, 0.18, 0.35, 0.6];
const FONDO = capas('5_polo_sur_sol_eterno');   // sin base dibujada al fondo, con la Tierra pegada al horizonte y hielo en las sombras
function blitCapa(im, capa, off, dy) {
  for (let y = 0; y < capa.h; y++) { const yy = y + dy; if (yy < 0 || yy >= im.h) continue; for (let x = 0; x < im.w; x++) { const sx = (((x + off) % capa.w) + capa.w) % capa.w, i = (y * capa.w + sx) * 4; if (capa.d[i + 3]) set(im, x, yy, [capa.d[i], capa.d[i + 1], capa.d[i + 2]], capa.d[i + 3] / 255); } }
}
// dibuja una ventana del mundo. o: { fase, desde (primera capa de fondo), jugador: [x, anim, cuadro, mira] }
function mundo(W, Hh, camX, o = {}) {
  const im = newImg(W, Hh), GY = Hh - 56, dy = Hh - 360;
  F(im, 0, 0, W - 1, Hh - 1, CIELO);
  for (let k = o.desde || 0; k < 5; k++) blitCapa(im, FONDO[k], Math.round(camX * FRAC[k]) - (k === 1 ? 72 : 0), dy);   // el Sol se queda a la izquierda en todo el nivel
  const top = sx => GY - altura(sx + camX);
  for (let sx = 0; sx < W; sx++) { const wx = sx + camX; if (wx < 0 || wx >= ANCHO_MUNDO) continue; for (let y = top(sx); y < Hh; y++) set(im, sx, y, colorSuelo(wx, y - top(sx), y)); if (hash(wx >> 1, 5) > 0.93 && !(wx >= 480 && wx < 1680)) { F(im, sx, top(sx) - 1, sx, top(sx) - 1, P.regolito[1]); } }
  const lista = COLOCADOS.map(([id, x]) => ({ p: prop[nombreProp(id, o.fase || 2)], x })).filter(e => e.x + e.p.im.w + 160 > camX && e.x < camX + W);
  // sombras largas hacia la derecha: el Sol esta a pocos grados sobre el horizonte
  for (const e of lista) { const largo = Math.min(150, e.p.im.h * 1.4); for (let wx = e.x + e.p.im.w - 4; wx < e.x + e.p.im.w + largo; wx++) { const sx = wx - camX; if (sx < 0 || sx >= W) continue; F(im, sx, top(sx), sx, top(sx) + 3, TINTA, 0.45); } }
  for (const e of lista) { const sx = e.x - camX, by = GY - altura(e.x + (e.p.im.w >> 1)); blit(im, e.p.im, sx, by - e.p.im.h + (e.p.d || 0)); }
  for (const [id, x] of GENTE) { if (x + 32 < camX || x > camX + W) continue; const mira = o.jugador ? o.jugador[0] < x : true; blit(im, cuadro(id, o.habla === id ? 1 : 0, o.habla === id ? 1 : 0), x - camX, GY - altura(x + 16) - 32, mira); }
  if (o.jugador) { const [x, fila, col, izq] = o.jugador; blit(im, cuadro('jugador', col, fila), x - camX, GY - altura(x + 16) - 32 - (o.salto || 0), izq); }
  for (const e of lista) { const sx = e.x - camX, by = GY - altura(e.x + (e.p.im.w >> 1)) - e.p.im.h; for (const [lx, ly, r, c] of e.p.luces) luz(im, sx + lx, by + ly, r, c); }
  // capa frontal (x1.3): rocas oscuras en primer plano que pasan mas rapido que el suelo
  if (o.frente) for (let sx = 0; sx < W; sx++) {
    const fx = sx + camX * 1.3, h = Math.round(22 * Math.max(0, Math.sin(fx * 0.011) * 0.7 + Math.sin(fx * 0.029 + 1.3) * 0.5 - 0.35) + (hash(fx >> 2, 3) > 0.5 ? 1 : 0));
    if (h < 3) continue;
    F(im, sx, Hh - h, sx, Hh - 1, hex('#0c0f1c')); set(im, sx, Hh - h, hex('#2a3040')); if (hash(fx >> 1, 9) > 0.7) set(im, sx, Hh - h + 2, hex('#1a1f33'));
  }
  return im;
}

// ---------- HUD ----------
const ICONOS = {
  o2: ['..#....', '..#....', '.###...', '.###...', '#####..', '#####..', '.###...'], energia: ['...##..', '..##...', '.##....', '#####..', '..##...', '.##....', '##.....'],
  comida: ['..#.#..', '.#####.', '.#####.', '..###..', '...#...', '...#...', '..###..'], radiacion: ['#..#..#', '.#.#.#.', '..###..', '#######', '..###..', '.#.#.#.', '#..#..#'],
};
function icono(im, n, x, y, c) { ICONOS[n].forEach((f, j) => { for (let i = 0; i < 7; i++) if (f[i] === '#') set(im, x + i, y + j, c); }); }
function panel(im, x0, y0, x1, y1, borde) { F(im, x0, y0, x1, y1, CIELO, 0.78); for (let x = x0; x <= x1; x++) { set(im, x, y0, borde); set(im, x, y1, borde); } for (let y = y0; y <= y1; y++) { set(im, x0, y, borde); set(im, x1, y, borde); } }
function hud(im, v, obj) {
  panel(im, 6, 6, 126, 52, hex('#33405e'));
  [['o2', 'OXIGENO', P.cian, v[0]], ['energia', 'ENERGIA', P.ambar, v[1]], ['comida', 'ALIMENTOS', P.verde, v[2]], ['radiacion', 'RADIACION', P.magenta, v[3]]].forEach(([n, t, col, val], i) => {
    const y = 10 + i * 10; icono(im, n, 10, y, col[1]); txt(im, t, 21, y + 1, val < 0.25 && i < 3 || val > 0.7 && i === 3 ? P.naranja[1] : BLANCO);
    for (let s = 0; s < 13; s++) F(im, 62 + s * 4, y + 1, 64 + s * 4, y + 5, s < Math.round(val * 13) ? (s === Math.round(val * 13) - 1 ? col[2] : col[1]) : hex('#232a40'));
    txt(im, Math.round(val * 100) + '%', 115 - txtW(Math.round(val * 100) + '%') + 9, y + 1, SUAVE);
  });
  panel(im, 474, 6, 633, 52, hex('#33405e'));
  txt(im, obj.titulo, 480, 10, P.cian[1]); txt(im, obj.texto, 480, 18, BLANCO);
  for (let k = 0; k < 4; k++) { F(im, 480 + k * 12, 26, 489 + k * 12, 31, k < obj.fase ? P.ambar[1] : hex('#232a40')); }
  txt(im, 'FASE ' + obj.fase + '/4', 532, 27, P.ambar[2]);
  obj.recursos.forEach((r, k) => txt(im, r, 480 + (k % 2) * 78, 36 + ((k / 2) | 0) * 8, SUAVE));
}
// marco de pagina: todo ocurre dentro del libro que lee la protagonista
function marco(im, capitulo) {
  for (let k = 0; k < 2; k++) { for (let x = k; x < im.w - k; x++) { set(im, x, k, CREMA); set(im, x, im.h - 1 - k, CREMA); } for (let y = k; y < im.h - k; y++) { set(im, k, y, CREMA); set(im, im.w - 1 - k, y, CREMA); } }
  const w = txtW(capitulo) + 12, x0 = (im.w - w) >> 1; F(im, x0, 0, x0 + w, 9, CREMA); F(im, x0 + 1, 10, x0 + w - 1, 10, CREMA); txtC(im, capitulo, im.w / 2, 3, hex('#4a3322'));
}
function bocadillo(im, cx, y, s, c) { const w = txtW(s) + 8; panel(im, Math.round(cx - w / 2), y, Math.round(cx + w / 2), y + 10, c); txtC(im, s, cx, y + 3, c); }

// ---------- hoja 2: escena en calma (la base) ----------
{
  const cam = 470, im = mundo(640, 360, cam, { fase: 2, jugador: [668, 0, 0, false], habla: 'comandante' });
  hud(im, [0.82, 0.64, 0.55, 0.12], { titulo: 'OBJETIVO 1', texto: 'CONSTRUYE EL COHETE', fase: 2, recursos: ['CAJAS 3/6', 'MINERAL 5/8', 'HIELO 0/4', 'COMBUSTIBLE 0%'] });
  panel(im, 70, 318, 570, 350, P.cian[1]);
  txt(im, 'CMTE. RIVAS', 78, 323, P.cian[1]); txt(im, 'PUEDES AYUDARNOS EN LA CONSTRUCCION DEL COHETE?', 78, 332, BLANCO); txt(im, 'NECESITAMOS MAS RECURSOS. LAS CAJAS LLEGAN A LA PISTA DE CARGA.', 78, 340, BLANCO);
  txt(im, 'E: SEGUIR', 530, 323, SUAVE);
  bocadillo(im, 872 - cam + 16, 304 - 46, 'E HABLAR', P.cian[1]);
  marco(im, 'CAPITULO 1 - LA LUNA');
  savePNG(path.join(SAL, '02_escena_base_en_calma.png'), im, 3);
}
// ---------- hoja 3: astillero con lluvia solar y meteoritos ----------
{
  const cam = 1236, im = mundo(640, 360, cam, { fase: 2, jugador: [1560, 1, 0, true], frente: true });
  F(im, 0, 0, 639, 359, P.magenta[1], 0.1);
  for (let i = 0; i < 110; i++) { const x = hash(i, 1) * 700 - 40, y = hash(i, 2) * 300, l = 5 + hash(i, 3) * 12; L(im, x, y, x + l, y + l * 0.33, hash(i, 4) > 0.5 ? P.magenta[2] : P.naranja[1], 0.75); }
  blit(im, prop.meteorito.im, 452, 96); luz(im, 487, 115, 16, P.naranja[1], 0.6);
  blit(im, prop.meteorito.im, 150, 40);
  for (let i = 0; i < 16; i++) { const a = Math.PI * (1 + i / 15), r = 6 + hash(i, 8) * 12; set(im, 596 + Math.cos(a) * r, 300 + Math.sin(a) * r, i % 2 ? P.regolito[2] : P.naranja[1]); }
  luz(im, 596, 300, 14, P.naranja[1], 0.5);
  hud(im, [0.46, 0.38, 0.5, 0.78], { titulo: 'OBJETIVO 1', texto: 'CONSTRUYE EL COHETE', fase: 2, recursos: ['CAJAS 4/6', 'MINERAL 6/8', 'HIELO 1/4', 'COMBUSTIBLE 25%'] });
  panel(im, 196, 22, 444, 46, P.magenta[1]); icono(im, 'radiacion', 204, 26, P.magenta[2]); icono(im, 'radiacion', 430, 26, P.magenta[2]);
  txtC(im, 'LLUVIA SOLAR', 320, 26, P.magenta[2], 2); txtC(im, 'REFUGIATE EN UNA CUPULA: 12 S', 320, 38, BLANCO);
  bocadillo(im, 1300 + 28 - cam, 304 - 100, 'E ENTREGAR 4 CAJAS', P.ambar[1]);
  marco(im, 'CAPITULO 1 - LA LUNA');
  savePNG(path.join(SAL, '03_escena_astillero_lluvia_solar.png'), im, 3);
}
// ---------- hoja 1: props ----------
{
  const im = newImg(640, 560); F(im, 0, 0, 639, 559, hex('#141a2a'));
  txt(im, 'MISION ARTEMIS - HOJA 1: PROPS DE LA BASE LUNAR (1 CASILLA = 16 PX, JUGADOR = 32 PX)', 10, 8, CREMA);
  const fila = (ids, base, x0, hueco) => {
    F(im, 6, base, 633, base + 1, P.regolito[1]); F(im, 6, base + 2, 633, base + 5, hex('#565b78'));
    let x = x0;
    for (const id of ids) {
      const p = typeof id === 'string' ? prop[id] : id;
      blit(im, p.im, x, base - p.im.h); const cx = x + p.im.w / 2;
      txtC(im, p.id, cx, base + 9, P.cian[1]); txtC(im, p.nombre, cx, base + 16, BLANCO); txtC(im, p.im.w + 'X' + p.im.h, cx, base + 23, SUAVE);
      x += p.im.w + hueco;
    }
  };
  fila(['cupula', 'invernadero', 'refugio', 'nave', 'antena', 'paneles'], 112, 14, 22);
  fila(['recarga', 'estacion', 'deposito', 'rover', 'pila', 'caja_a', 'veta_ilmenita', 'veta_regolito', 'veta_hielo', 'bandera_usa', 'bandera_ecuador', 'bandera_ieee'], 208, 14, 13);
  const gente = ['jugador', 'comandante', 'geologa', 'ingeniero', 'piloto', 'medica'].map((id, k) => ({ im: cuadro(id, 0, 0), id: 'N0' + k, nombre: id.toUpperCase() }));
  fila(['maquina', 'cohete_1', 'cohete_2', 'cohete_3', 'cohete_4', ...gente], 408, 12, 10);
  txt(im, 'FX Y HUD', 10, 446, CREMA);
  blit(im, prop.meteorito.im, 14, 462); txt(im, 'F01 METEORITO', 14, 494, BLANCO);
  for (let i = 0; i < 40; i++) { const x = 90 + hash(i, 1) * 90, y = 458 + hash(i, 2) * 30, l = 5 + hash(i, 3) * 10; L(im, x, y, x + l, y + l * 0.33, hash(i, 4) > 0.5 ? P.magenta[2] : P.naranja[1]); }
  txt(im, 'F02 LLUVIA SOLAR', 90, 494, BLANCO);
  const h = newImg(640, 60); hud(h, [0.82, 0.64, 0.55, 0.12], { titulo: 'OBJETIVO 1', texto: 'CONSTRUYE EL COHETE', fase: 2, recursos: ['CAJAS 3/6', 'MINERAL 5/8', 'HIELO 0/4', 'COMBUSTIBLE 0%'] });
  blit(im, recorte(h, 6, 6, 121, 47), 210, 456); blit(im, recorte(h, 474, 6, 160, 47), 344, 456);
  txt(im, 'U01 MEDIDORES', 210, 508, BLANCO); txt(im, 'U02 OBJETIVO', 344, 508, BLANCO);
  ['o2', 'energia', 'comida', 'radiacion'].forEach((n, k) => { F(im, 520 + k * 28, 458, 540 + k * 28, 478, CIELO); for (const [dx, dy] of [[0, 0], [1, 0], [0, 1], [1, 1]]) ICONOS[n].forEach((f, j) => { for (let i = 0; i < 7; i++) if (f[i] === '#') set(im, 523 + k * 28 + i * 2 + dx, 461 + j * 2 + dy, [P.cian, P.ambar, P.verde, P.magenta][k][1]); }); });
  txt(im, 'U03 ICONOS', 520, 508, BLANCO);
  txt(im, 'LUZ: SOL BAJO A LA IZQUIERDA. CONTORNO TINTA 12141F. EL COHETE SIN CONSTRUIR SE VE COMO PLANO DE PUNTOS CIAN.', 10, 530, SUAVE);
  txt(im, 'LAS BANDERAS VAN RIGIDAS CON VARILLA: EN LA LUNA NO HAY VIENTO.', 10, 540, SUAVE);
  savePNG(path.join(SAL, '01_props.png'), im, 3);
}
// ---------- hoja 4: mapa del nivel (4 tiras de 640 px = 2560 px de mundo) ----------
{
  const AT = 216, im = newImg(640, 16 + AT * 4); F(im, 0, 0, im.w - 1, im.h - 1, hex('#141a2a'));
  txt(im, 'MISION ARTEMIS - HOJA 4: MAPA DEL NIVEL LUNAR, DE IZQUIERDA A DERECHA (2560 PX = 160 CASILLAS)', 10, 5, CREMA);
  for (let r = 0; r < 4; r++) {
    const t = mundo(640, 200, r * 640, { fase: 2, desde: 2 });
    for (const [a, b, n] of ZONAS) { const x0 = a - r * 640, x1 = b - r * 640; if (x1 < 0 || x0 >= 640) continue; if (x0 >= 0) for (let y = 0; y < 200; y += 2) set(t, x0, y, CREMA); if (x0 >= 0 || b > r * 640 + 60 && !ZONAS.some(z => z[0] > r * 640 && z[0] < r * 640 + 110)) txt(t, n, Math.max(4, x0 + 4), 4, CREMA); }
    for (let wx = r * 640; wx < r * 640 + 640; wx += 160) { F(t, wx - r * 640, 194, wx - r * 640, 199, CREMA); txt(t, (wx / 16) + '', wx - r * 640 + 3, 193, CREMA); }
    blit(im, t, 0, 16 + r * AT);
  }
  savePNG(path.join(SAL, '04_mapa_del_nivel.png'), im, 2);
}
// ---------- hoja 5: paleta, capas de parallax y proporciones ----------
{
  const im = newImg(640, 400); F(im, 0, 0, 639, 399, hex('#141a2a'));
  txt(im, 'MISION ARTEMIS - HOJA 5: PALETA, CAPAS DE PARALLAX Y PROPORCIONES', 10, 8, CREMA);
  Object.keys(P).forEach((k, i) => { const x = 10 + (i % 7) * 90, y = 22 + ((i / 7) | 0) * 34; F(im, x - 1, y - 1, x + 54, y + 14, hex('#33405e')); P[k].forEach((c, j) => F(im, x + j * 18, y, x + j * 18 + 17, y + 13, c)); txt(im, NOMBRES[k], x, y + 16, BLANCO); txt(im, HEXP[k][1].slice(1), x, y + 23, SUAVE); });
  txt(im, 'CAPAS DE PARALLAX DE LA LUNA (VELOCIDAD RESPECTO A LA CAMARA)', 10, 96, CREMA);
  const nombres = ['0 ESPACIO X0.02', '1 SOL Y TIERRA X0.06', '2 MONTANAS LEJANAS X0.18', '3 MONTANAS MEDIAS X0.35', '4 COLINAS CERCANAS X0.60', '5 SUELO JUGABLE X1.00'];
  for (let k = 0; k < 6; k++) {
    const x = 10 + (k % 6) * 104, y = 106; F(im, x, y, x + 99, y + 55, CIELO);
    if (k < 5) { for (let yy = 0; yy < 56; yy++) for (let xx = 0; xx < 100; xx++) { const i = ((Math.floor(yy * 6.4)) * 640 + Math.floor(xx * 6.4)) * 4; if (FONDO[k].d[i + 3]) set(im, x + xx, y + yy, [FONDO[k].d[i], FONDO[k].d[i + 1], FONDO[k].d[i + 2]]); } }
    else { const t = mundo(640, 360, 470, { fase: 2, desde: 5 }); for (let yy = 0; yy < 56; yy++) for (let xx = 0; xx < 100; xx++) { const i = ((Math.floor(yy * 6.4)) * 640 + Math.floor(xx * 6.4)) * 4; if (yy * 6.4 > 150) set(im, x + xx, y + yy, [t.d[i], t.d[i + 1], t.d[i + 2]]); } }
    txt(im, nombres[k], x, y + 59, k === 5 ? P.cian[1] : BLANCO);
  }
  txt(im, 'MARTE (PENDIENTE: LOS FONDOS LOS ENTREGA DOMENICA). MISMAS 6 RANURAS Y VELOCIDADES', 10, 182, CREMA);
  for (let k = 0; k < 6; k++) { const x = 10 + k * 104, y = 192; F(im, x, y, x + 99, y + 55, hex(['#1a0f14', '#2a1518', '#4a2018', '#6e2f1c', '#94441f', '#b85a2a'][k])); for (let i = 0; i < 100; i += 4) { set(im, x + i, y, CREMA); set(im, x + i, y + 55, CREMA); } for (let i = 0; i < 56; i += 4) { set(im, x, y + i, CREMA); set(im, x + 99, y + i, CREMA); } txtC(im, 'CAPA ' + k, x + 50, y + 22, CREMA); txtC(im, 'PENDIENTE', x + 50, y + 30, CREMA); }
  txt(im, 'PROPORCIONES (CUADRICULA DE 16 PX)', 10, 262, CREMA);
  const bx = 10, by = 388;
  for (let x = 0; x <= 620; x += 16) F(im, bx + x, by - 112, bx + x, by, hex('#1f2940')); for (let y = 0; y <= 112; y += 16) F(im, bx, by - y, bx + 620, by - y, hex('#1f2940'));
  F(im, bx, by, bx + 620, by + 1, P.regolito[2]);
  let x = bx + 16;
  for (const [o, n] of [[{ im: cuadro('jugador', 0, 0) }, '2 ALTO'], [prop.caja_a, '1'], [prop.estacion, '1.5X3'], [prop.rover, '4X2'], [prop.cupula, '8X4.5'], [prop.invernadero, '7X3'], [prop.antena, '3X5.5']]) { blit(im, o.im, x, by - o.im.h); txtC(im, n, x + o.im.w / 2, by - o.im.h - 8, P.ambar[2]); x += Math.ceil((o.im.w + 20) / 16) * 16; }
  txt(im, 'COHETE: 3.5 X 10 CASILLAS. SALTO DEL JUGADOR: 3 CASILLAS (GRAVEDAD LUNAR 1/6).', 250, 262, SUAVE);
  savePNG(path.join(SAL, '05_paleta_capas_proporciones.png'), im, 3);
}
// ---------- datos y texturas del nivel para Godot ----------
{
  const DIR = path.join(REC, 'nivel'); fs.mkdirSync(DIR, { recursive: true }); fs.mkdirSync(path.join(RAIZ, 'datos'), { recursive: true });
  const c0 = cohete(0); savePNG(path.join(DIR_PROPS, 'cohete_0.png'), c0.im);
  const BASE = 104, s = newImg(ANCHO_MUNDO, 200);
  for (let x = 0; x < ANCHO_MUNDO; x++) { const top = BASE - altura(x); for (let y = top; y < 200; y++) set(s, x, y, colorSuelo(x, y - top, y + 200)); if (hash(x >> 1, 5) > 0.93 && !(x >= 480 && x < 1680)) set(s, x, top - 1, P.regolito[1]); }
  for (const [id, x] of COLOCADOS) { const p = prop[nombreProp(id, 2)], largo = Math.min(150, p.im.h * 1.4); for (let wx = x + p.im.w - 4; wx < Math.min(ANCHO_MUNDO, x + p.im.w + largo); wx++) F(s, wx, BASE - altura(wx), wx, BASE - altura(wx) + 3, TINTA, 0.45); }
  savePNG(path.join(DIR, 'suelo_luna.png'), s);
  const f = newImg(1280, 26);
  for (let x = 0; x < 1280; x++) { const a = x * Math.PI * 2 / 1280, h = Math.round(22 * Math.max(0, Math.sin(a * 3) * 0.7 + Math.sin(a * 7 + 1.3) * 0.5 - 0.35) + (hash(x >> 2, 3) > 0.5 ? 1 : 0)); if (h < 3) continue; F(f, x, 26 - h, x, 25, hex('#0c0f1c')); set(f, x, 26 - h, hex('#2a3040')); if (hash(x >> 1, 9) > 0.7) set(f, x, 28 - h, hex('#1a1f33')); }
  savePNG(path.join(DIR, 'frente_luna.png'), f);
  const aHex = c => '#' + c.map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  const datos = {
    ancho: ANCHO_MUNDO, casilla: 16, suelo_base: BASE, alturas: ALT,
    zonas: [[0, 480, 'Pista de carga'], [480, 1280, 'Base del polo sur'], [1280, 1680, 'Astillero'], [1680, 2240, 'Campo minero'], [2240, 2560, 'Cráter en sombra']],
    props: COLOCADOS.map(([id, x]) => { const p = id === 'cohete' ? { im: c0.im, luces: [] } : prop[id]; return { id, x, w: p.im.w, h: p.im.h, luces: p.luces.map(([lx, ly, r, c]) => [lx, ly, r, aHex(c)]) }; }),
    gente: GENTE,
  };
  fs.writeFileSync(path.join(RAIZ, 'datos', 'nivel_luna.json'), JSON.stringify(datos));
}
console.log('hojas listas en', SAL);
