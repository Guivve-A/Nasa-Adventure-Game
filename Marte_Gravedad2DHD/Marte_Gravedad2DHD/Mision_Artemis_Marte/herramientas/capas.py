"""Exporta el entorno de Marte (escena E) por capas, en tres horas, con capas que se repiten sin cortes.
Capas fijas (384×216): cielo.png, astros.png.  Capas repetibles (768×216): montanas_lejanas, montanas_cercanas, suelo."""
import numpy as np, math, random, os, sys
from PIL import Image
from estilos2 import hx, ramp
import horas

VW, H, W = 384, 216, 768   # vista, alto, ancho de las capas repetibles
GROUND_Y = 184

def tnoise(w, h, cells_x, seed, octaves=4):
    """Ruido de valor que se repite horizontalmente (tileable en X)."""
    rng = np.random.default_rng(seed); out = np.zeros((h, w)); amp = 1; tot = 0
    for o in range(octaves):
        cx = cells_x * 2 ** o; cy = max(1, int(round(cx * h / w)))
        g = rng.random((cy + 1, cx))
        g = np.pad(g, ((0, 0), (2, 2)), mode='wrap')               # envolver en X
        px = w / cx
        big = Image.fromarray((g * 255).astype(np.uint8)).resize((int(round(px * (cx + 4))), h), Image.BICUBIC)
        a = np.asarray(big, float)[:, int(round(2 * px)):int(round(2 * px)) + w] / 255
        out += amp * a; tot += amp; amp *= 0.5
    return out / tot

def build(mode, M):
    rnd = random.Random(5)
    # ---------- cielo (fijo, opaco) con resplandor del horizonte
    sky = np.zeros((H, VW, 3)); t = np.linspace(0, 1, 150)[:, None] * np.ones((1, VW))
    sky[:150] = ramp(t ** M['sky_pow'], [hx(c) for c in M['sky']]); sky[150:] = hx(M['sky'][-1])
    for y in range(130, H):
        k = min(1, (y - 130) / 30)
        for x in range(VW):
            if (x + y) % 2 == 0 or k > 0.5: sky[y, x] = sky[y, x] * (1 - M['glow_a'] * k) + hx(M['glow']) * M['glow_a'] * k
    # ---------- astros (fijo, transparente): estrellas, Tierra, sol, lunas
    ast = np.zeros((H, VW, 4))
    def px(x, y, c, a=1.0):
        if 0 <= x < VW and 0 <= y < H: ast[y, x, :3] = c; ast[y, x, 3] = a
    stars = [(rnd.randrange(VW), rnd.randrange(130), rnd.random()) for _ in range(170)]
    if M['stars']:
        for x, y, b in stars:
            if M['stars'] == 'few' and (y > 45 or b < 0.6): continue
            px(x, y, hx('#FFF2D8') if b > 0.85 else (hx('#C9B7E0') if b > 0.5 else hx('#7E7BAA')))
            if b > 0.97 and M['stars'] is True:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): px(x + dx, y + dy, hx('#E58A5A'))
    if mode == 'noche':
        for dx, dy, c in ((0, 0, '#BFE6FF'), (1, 0, '#6FB6FF'), (0, 1, '#6FB6FF'), (-1, 0, '#3E7BD0'), (0, -1, '#3E7BD0')): px(96 + dx, 64 + dy, hx(c))
    if M['sun']:
        sx, sy, r, core, halo = M['sun']
        for y in range(max(0, sy - 5 * r), min(H, sy + 5 * r)):
            for x in range(max(0, sx - 5 * r), min(VW, sx + 5 * r)):
                d = math.hypot(x - sx, y - sy)
                if d <= r: px(x, y, hx(core))
                elif d <= r * 1.6: px(x, y, hx(halo))
                elif d <= r * 2.6 and (x + y) % 2 == 0: px(x, y, hx(halo), 0.5)
                elif d <= r * 4.2 and (x + y) % 4 == 0: px(x, y, hx(halo), 0.3)
    full_sky = horas.escena(mode)          # para copiar las lunas exactamente como en la imagen aprobada
    for (cx, cy, r) in [(300, 52, 26), (212, 40, 6)]:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if math.hypot((x - cx) / r, (y - cy) / (r * 0.85)) <= 1: px(x, y, full_sky[y, x])
    # ---------- montañas (repetibles): misma forma en las tres horas
    def peaks(base, amp, cols, seedk, freq):
        n = tnoise(W, 1, 40, seedk, 4)[0]
        f1, f2 = round(freq * W / VW), round(freq * 2.3 * W / VW)      # frecuencias enteras → se repite sin corte
        top = [int(base - amp * (max(0, math.sin(2 * math.pi * f1 * x / W + seedk)) ** 1.5 * 0.55
                                 + max(0, math.sin(2 * math.pi * f2 * x / W + 2 * seedk)) ** 3 * 0.35 + (n[x] - 0.3) * 0.7)) for x in range(W)]
        lay = np.zeros((H, W, 4))
        for x in range(W):
            lit = top[x] < top[(x - 1) % W] if M['light_from'] == 'left' else top[x] < top[(x + 1) % W]
            for y in range(max(0, top[x]), H):
                rel = y - top[x]
                c = hx(cols[0]) if lit and rel < 6 else hx(cols[1])
                if rel > 10: c = hx(cols[2]) if (x + y) % 2 or rel > 16 else hx(cols[1])
                if mode == 'golden' and lit and rel < 2: c = hx('#FFB25A') * 0.6 + hx(cols[0]) * 0.4
                lay[y, x, :3] = c; lay[y, x, 3] = 1
        return lay
    far = peaks(170, 34, M['far'], 11, 2.2)
    near = peaks(182, 26, M['near'], 23, 3.4)
    # ---------- suelo (repetible)
    g = np.zeros((H, W, 4)); n = tnoise(W, H - GROUND_Y, 48, 31, 3)
    grad = np.linspace(0.3, -0.2, H - GROUND_Y)[:, None]
    if mode == 'golden': grad = grad + 0.04 * np.sin(np.linspace(0, 2 * np.pi, W, endpoint=False))[None, :]
    g[GROUND_Y:, :, :3] = ramp(0.2 + 0.6 * n + grad, [hx(c) for c in M['ground']]); g[GROUND_Y:, :, 3] = 1
    g[GROUND_Y, :, :3] = hx(M['lip'])
    return dict(cielo=sky, astros=ast, montanas_lejanas=far, montanas_cercanas=near, suelo=g)

def tod(a):
    a = np.clip(a, 0, 255) if a.shape[2] == 3 else np.concatenate([np.clip(a[..., :3], 0, 255), a[..., 3:] * 255], 2)
    return Image.fromarray(a.astype(np.uint8))

if __name__ == '__main__':
    out = sys.argv[1]
    # paleta del día aprobada (v2, más naranja)
    D = horas.MODES['dia']
    D.update(sky=('#B65A2E', '#C2683A', '#CD7745', '#D78650', '#E0955B', '#E8A367', '#EEB174', '#F2BE82', '#F5C98F'),
             sky_pow=0.95, glow='#F9D29A', glow_a=0.4, sun=(70, 34, 6, '#FFF6E0', '#FFD9A0'),
             far=('#C47A55', '#AC6448', '#94523E'), moon=('#C48058', '#CF8F66', '#D99C72', '#E1A87E', '#E8B58C'))
    for mode, folder in (('dia', 'dia'), ('golden', 'atardecer'), ('noche', 'noche')):
        d = os.path.join(out, folder); os.makedirs(d, exist_ok=True)
        for k, arr in build(mode, horas.MODES[mode]).items():
            tod(arr).save(os.path.join(d, k + '.png'))
    print('ok')
