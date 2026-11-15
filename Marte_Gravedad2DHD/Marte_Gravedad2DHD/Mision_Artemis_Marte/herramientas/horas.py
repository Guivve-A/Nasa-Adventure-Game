"""Escena E (noche marciana) en tres horas del día con el mismo paisaje: noche, día y golden hour."""
import numpy as np, math, random
from PIL import Image
from estilos2 import hx, ramp, vnoise

W, H = 384, 216

MODES = {
    'noche': dict(
        sky=('#0E0B22', '#14122E', '#1B1B3D', '#232A55', '#2D3E73', '#3F5C93', '#5F86B6'), sky_pow=1.6,
        glow='#7FA9D6', glow_a=0.5, stars=True, sun=None,
        far=('#7A3A44', '#5C2B3B', '#3E1F33'), near=('#B2473A', '#86352F', '#5A2630'),
        ground=('#4A2230', '#6E2E2E', '#93402F', '#B95A38', '#D47A45'), lip='#E39A5C',
        moon=('#2A1E2E', '#5A3540', '#8C5048', '#B87256', '#D9946A'), moon_lit=(-0.7, -0.5), light_from='left'),
    'dia': dict(
        sky=('#C99A6B', '#D4A675', '#DDB27F', '#E5BE8A', '#ECCA97', '#F1D5A6', '#F4DDB2'), sky_pow=1.0,
        glow='#F8E6C2', glow_a=0.45, stars=False, sun=(70, 34, 6, '#FFF8E6', '#FBE7C4'),
        far=('#C98A68', '#B4765C', '#9C6450'), near=('#D9714A', '#B5553A', '#8C4231'),
        ground=('#9A4A30', '#B85B38', '#CF7444', '#E08C52', '#ECA567'), lip='#F6C58A',
        moon=('#B99A86', '#C9A891', '#D6B59C', '#DDBDA5', '#E3C6AE'), moon_lit=(-0.6, -0.6), light_from='left'),
    'golden': dict(
        sky=('#2A2350', '#46305E', '#6E3C62', '#A24E5A', '#D2674A', '#EE8A3C', '#FFB347'), sky_pow=1.25,
        glow='#FFC56A', glow_a=0.6, stars='few', sun=(318, 146, 9, '#FFF1C2', '#FFB347'),
        far=('#9E4C4E', '#6A3048', '#442440'), near=('#E0743E', '#9A3A34', '#5E2433'),
        ground=('#4E2232', '#7A2F30', '#A8452F', '#D2683A', '#F08F46'), lip='#FFC36E',
        moon=('#4A2A3E', '#7A4050', '#B0605A', '#D8885E', '#F1A86A'), moon_lit=(0.75, 0.35), light_from='right'),
}

def escena(mode, seed=5):
    M = MODES[mode]; rnd = random.Random(seed); img = np.zeros((H, W, 3))
    t = np.linspace(0, 1, 150)[:, None] * np.ones((1, W))
    img[:150] = ramp(t ** M['sky_pow'], [hx(c) for c in M['sky']]); img[150:] = hx(M['sky'][-1])
    # estrellas (se sortean siempre para que el paisaje no cambie entre horas)
    stars = [(rnd.randrange(W), rnd.randrange(130), rnd.random()) for _ in range(170)]
    if M['stars']:
        for x, y, b in stars:
            if M['stars'] == 'few' and (y > 45 or b < 0.6): continue
            img[y, x] = hx('#FFF2D8') if b > 0.85 else (hx('#C9B7E0') if b > 0.5 else hx('#7E7BAA'))
            if b > 0.97 and M['stars'] is True:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < W and 0 <= y + dy < H: img[y + dy, x + dx] = hx('#E58A5A')
    if mode == 'noche':   # la Tierra: punto azul
        for dx, dy, c in ((0, 0, '#BFE6FF'), (1, 0, '#6FB6FF'), (0, 1, '#6FB6FF'), (-1, 0, '#3E7BD0'), (0, -1, '#3E7BD0')): img[64 + dy, 96 + dx] = hx(c)
    # sol con halo tramado
    if M['sun']:
        sx, sy, r, core, halo = M['sun']
        for y in range(max(0, sy - 5 * r), min(H, sy + 5 * r)):
            for x in range(max(0, sx - 5 * r), min(W, sx + 5 * r)):
                d = math.hypot(x - sx, y - sy)
                if d <= r: img[y, x] = hx(core)
                elif d <= r * 1.6: img[y, x] = hx(halo)
                elif d <= r * 2.6 and (x + y) % 2 == 0: img[y, x] = img[y, x] * 0.5 + hx(halo) * 0.5
                elif d <= r * 4.2 and (x + y) % 4 == 0: img[y, x] = img[y, x] * 0.7 + hx(halo) * 0.3
    # lunas (misma posición)
    def moon(cx, cy, r):
        n = vnoise(2 * r + 2, 2 * r + 2, r / 2, cx, 3); lx, ly = M['moon_lit']
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                d = math.hypot((x - cx) / r, (y - cy) / (r * 0.85))
                if d <= 1:
                    nz = math.sqrt(max(0, 1 - d * d)); nx, ny = (x - cx) / r, (y - cy) / r
                    l = max(0, (nx * lx + ny * ly) * 0.8 + nz * 0.5)
                    v = l * 0.85 + (n[y - cy + r, x - cx + r] - 0.5) * 0.35
                    c = ramp(np.array([[v]]), [hx(q) for q in M['moon']], dither=False)[0, 0]
                    if mode == 'dia': c = c * 0.55 + img[y, x] * 0.45      # de día la luna se ve pálida
                    img[y, x] = c
    moon(300, 52, 26); moon(212, 40, 6)
    # resplandor del horizonte
    for y in range(130, 160):
        k = (y - 130) / 30
        for x in range(W):
            if (x + y) % 2 == 0 or k > 0.5: img[y, x] = img[y, x] * (1 - M['glow_a'] * k) + hx(M['glow']) * M['glow_a'] * k
    # picos: misma geometría; cambia de qué lado llega la luz
    def peaks(base, amp, cols, seedk, freq):
        n = vnoise(W, 1, 10, seedk, 4)[0]
        top = [int(base - amp * (max(0, math.sin(2 * math.pi * freq * x / W + seedk)) ** 1.5 * 0.55
                                 + max(0, math.sin(2 * math.pi * freq * 2.3 * x / W + 2 * seedk)) ** 3 * 0.35 + (n[x] - 0.3) * 0.7)) for x in range(W)]
        for x in range(W):
            for y in range(max(0, top[x]), H):
                rel = y - top[x]
                if M['light_from'] == 'left': lit = top[x] < top[x - 1] if x > 0 else True
                else: lit = top[x] < top[x + 1] if x < W - 1 else True
                c = cols[0] if lit and rel < 6 else cols[1]
                if rel > 10: c = cols[2] if (x + y) % 2 or rel > 16 else cols[1]
                if mode == 'golden' and lit and rel < 2: c = hx('#FFB25A') * 0.6 + hx(cols[0]) * 0.4   # borde dorado
                img[y, x] = hx(c) if isinstance(c, str) else c
    peaks(170, 34, M['far'], 11, 2.2)
    peaks(182, 26, M['near'], 23, 3.4)
    # suelo plano
    gy = 184; n = vnoise(W, H - gy, 8, 31, 3)
    grad = np.linspace(0.3, -0.2, H - gy)[:, None]
    if mode == 'golden': grad = grad + np.linspace(-0.1, 0.15, W)[None, :]   # más luz hacia el sol (derecha)
    img[gy:] = ramp(0.2 + 0.6 * n + grad, [hx(c) for c in M['ground']]); img[gy] = hx(M['lip'])
    return img

if __name__ == '__main__':
    out = {}
    for m in ('noche', 'dia', 'golden'):
        im = Image.fromarray(np.clip(escena(m), 0, 255).astype(np.uint8)); im.save(f'E_{m}_1x.png')
        im.resize((W * 3, H * 3), Image.NEAREST).save(f'E_{m}_x3.png')
