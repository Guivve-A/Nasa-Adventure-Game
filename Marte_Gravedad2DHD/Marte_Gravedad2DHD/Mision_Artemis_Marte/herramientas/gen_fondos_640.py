"""Fondos de Marte para Mision Artemis (640x360, mismas capas que la Luna) en tres horas: dia, atardecer, noche.
Capas: capa_0_espacio (opaca), capa_0b_sol_tierra (astros), capa_1/2/3 (montanas que se repiten cada 640 px).
Ademas: suelo_marte_<hora>.png (640x56, se repite) para el suelo caminable."""
import numpy as np, math, random, os, sys
from PIL import Image
from estilos2 import hx, ramp, vnoise
from capas import tnoise
import horas

W, H = 640, 360
HORIZ = 300            # el cielo se ve hasta aqui; el suelo del juego empieza en y=304

D = dict(horas.MODES['dia'])
D.update(sky=('#B65A2E', '#C2683A', '#CD7745', '#D78650', '#E0955B', '#E8A367', '#EEB174', '#F2BE82', '#F5C98F'),
         sky_pow=0.95, glow='#F9D29A', glow_a=0.4, sun=(150, 70, 8, '#FFF6E0', '#FFD9A0'),
         far=('#C47A55', '#AC6448', '#94523E'), mid=('#D27A50', '#B4603F', '#944B35'),
         moon=('#C48058', '#CF8F66', '#D99C72', '#E1A87E', '#E8B58C'))
G = dict(horas.MODES['golden']); G.update(sun=(540, 205, 11, '#FFF1C2', '#FFB347'), mid=('#C45A3C', '#86343A', '#52223A'))
N = dict(horas.MODES['noche']); N.update(mid=('#9A4038', '#702D34', '#4A2232'))
MODOS = {'dia': ('dia', D), 'atardecer': ('golden', G), 'noche': ('noche', N)}


def cielo(mode, M):
    img = np.zeros((H, W, 3))
    t = np.linspace(0, 1, HORIZ)[:, None] * np.ones((1, W))
    img[:HORIZ] = ramp(t ** M['sky_pow'], [hx(c) for c in M['sky']]); img[HORIZ:] = hx(M['sky'][-1])
    for y in range(200, H):                       # resplandor del horizonte, tramado
        k = min(1, (y - 200) / 70)
        for x in range(W):
            if (x + y) % 2 == 0 or k > 0.5:
                img[y, x] = img[y, x] * (1 - M['glow_a'] * k) + hx(M['glow']) * M['glow_a'] * k
    rnd = random.Random(7)
    if M['stars']:
        for _ in range(420):
            x, y, b = rnd.randrange(W), rnd.randrange(230), rnd.random()
            if M['stars'] == 'few' and (y > 90 or b < 0.65): continue
            img[y, x] = hx('#FFF2D8') if b > 0.85 else (hx('#C9B7E0') if b > 0.5 else hx('#7E7BAA'))
            if b > 0.975 and M['stars'] is True:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < W and 0 <= y + dy < H: img[y + dy, x + dx] = hx('#E58A5A')
    return img


def astros(mode, M):
    a = np.zeros((H, W, 4))
    def px(x, y, c, al=1.0):
        if 0 <= x < W and 0 <= y < H: a[y, x, :3] = c; a[y, x, 3] = al
    if mode == 'noche':                         # la Tierra: un punto azul brillante
        for dx, dy, c in ((0, 0, '#E6F6FF'), (1, 0, '#6FB6FF'), (0, 1, '#6FB6FF'), (-1, 0, '#3E7BD0'), (0, -1, '#3E7BD0')):
            px(170 + dx, 120 + dy, hx(c))
    if M['sun']:
        sx, sy, r, core, halo = M['sun']
        for y in range(sy - 5 * r, sy + 5 * r):
            for x in range(sx - 5 * r, sx + 5 * r):
                d = math.hypot(x - sx, y - sy)
                if d <= r: px(x, y, hx(core))
                elif d <= r * 1.6: px(x, y, hx(halo))
                elif d <= r * 2.6 and (x + y) % 2 == 0: px(x, y, hx(halo), 0.5)
                elif d <= r * 4.2 and (x + y) % 4 == 0: px(x, y, hx(halo), 0.3)
    # Fobos (grande, irregular) y Deimos (pequena)
    lx, ly = M['moon_lit']
    for (cx, cy, r, sk) in [(470, 96, 30, 1), (360, 70, 7, 2)]:
        n = vnoise(2 * r + 2, 2 * r + 2, r / 2, cx, 3)
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                d = math.hypot((x - cx) / r, (y - cy) / (r * 0.82))
                if d <= 1:
                    nz = math.sqrt(max(0, 1 - d * d)); nx, ny = (x - cx) / r, (y - cy) / r
                    l = max(0, (nx * lx + ny * ly) * 0.8 + nz * 0.5)
                    v = l * 0.85 + (n[y - cy + r, x - cx + r] - 0.5) * 0.35
                    c = ramp(np.array([[v]]), [hx(q) for q in M['moon']], dither=False)[0, 0]
                    px(x, y, c, 0.55 if mode == 'dia' else 1.0)
    return a


def montes(mode, M, base, amp, cols, seed, f1, f2, strata=True):
    n = tnoise(W, 1, 40, seed, 4)[0]
    tex = tnoise(W, H, 24, seed + 50, 3)
    top = [int(base - amp * (max(0, math.sin(2 * math.pi * f1 * x / W + seed)) ** 1.5 * 0.55
                             + max(0, math.sin(2 * math.pi * f2 * x / W + 2 * seed)) ** 3 * 0.35 + (n[x] - 0.3) * 0.7)) for x in range(W)]
    lay = np.zeros((H, W, 4))
    for x in range(W):
        lit = top[x] < top[(x - 1) % W] if M['light_from'] == 'left' else top[x] < top[(x + 1) % W]
        for y in range(max(0, top[x]), H):
            rel = y - top[x]
            c = hx(cols[0]) if lit and rel < 6 else hx(cols[1])
            if rel > 10: c = hx(cols[2]) if (x + y) % 2 or rel > 16 else hx(cols[1])
            if strata and rel > 6 and tex[y, x] > 0.7 and (y // 4) % 3 == 0: c = hx(cols[1])     # vetas de roca
            if mode == 'golden' and lit and rel < 2: c = hx('#FFB25A') * 0.6 + hx(cols[0]) * 0.4
            if mode == 'noche' and lit and rel < 2: c = hx(cols[0]) * 0.7 + hx('#7FA9D6') * 0.3
            lay[y, x, :3] = c; lay[y, x, 3] = 1
    return lay


def suelo(mode, M):
    h = 56; g = np.zeros((h, W, 4)); n = tnoise(W, h, 64, 31, 3)
    grad = np.linspace(0.35, -0.25, h)[:, None]
    g[:, :, :3] = ramp(0.2 + 0.6 * n + grad, [hx(c) for c in M['ground']]); g[:, :, 3] = 1
    g[0, :, :3] = hx(M['lip']); g[1, ::2, :3] = hx(M['lip'])
    rnd = random.Random(12)
    dark = hx(M['ground'][0]); lite = hx(M['lip'])
    for _ in range(46):                            # piedritas con brillo arriba
        x, y, r = rnd.randrange(W), rnd.randrange(6, h - 4), rnd.choice((1, 1, 2, 2, 3))
        for yy in range(-r, r + 1):
            for xx in range(-r - 1, r + 2):
                if (xx / (r + 1)) ** 2 + (yy / r) ** 2 <= 1:
                    g[y + yy, (x + xx) % W, :3] = lite * 0.5 + dark * 0.5 if yy < 0 else dark
    tinte = {'dia': (1.0, 1.0, 1.0), 'golden': (0.95, 0.8, 0.72), 'noche': (0.5, 0.48, 0.66)}[mode]
    g[:, :, :3] *= np.array(tinte)
    return g


def tod(a):
    if a.shape[2] == 3: return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    b = np.concatenate([np.clip(a[..., :3], 0, 255), a[..., 3:] * 255], 2)
    return Image.fromarray(b.astype(np.uint8), 'RGBA')


if __name__ == '__main__':
    out = sys.argv[1]
    for nombre, (mode, M) in MODOS.items():
        d = os.path.join(out, 'fondos_marte', nombre); os.makedirs(d, exist_ok=True)
        tod(cielo(mode, M)).save(os.path.join(d, 'capa_0_espacio.png'))
        tod(astros(mode, M)).save(os.path.join(d, 'capa_0b_sol_tierra.png'))
        tod(montes(mode, M, 238, 70, M['far'], 11, 2, 5)).save(os.path.join(d, 'capa_1_montanas_lejanas.png'))
        tod(montes(mode, M, 272, 44, M['mid'], 17, 3, 7)).save(os.path.join(d, 'capa_2_montanas_medias.png'))
        tod(montes(mode, M, 300, 22, M['near'], 23, 4, 9)).save(os.path.join(d, 'capa_3_colinas_cercanas.png'))
        dn = os.path.join(out, 'nivel'); os.makedirs(dn, exist_ok=True)
        tod(suelo(mode, M)).save(os.path.join(dn, 'suelo_marte_' + nombre + '.png'))
    print('ok')
