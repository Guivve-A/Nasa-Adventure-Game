"""Ideas originales de Marte en pixel art inspiradas en tres estilos: desierto brumoso de píxel grande,
planeta con tramado (dithering) y paisaje nocturno estrellado."""
import numpy as np, math, random
from PIL import Image

def hx(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float)
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0

def vnoise(w, h, scale, seed, octaves=4):
    rng = np.random.default_rng(seed); out = np.zeros((h, w)); amp = 1; tot = 0
    for o in range(octaves):
        gw, gh = max(2, int(w / scale * 2 ** o)) + 1, max(2, int(h / scale * 2 ** o)) + 1
        g = Image.fromarray((rng.random((gh, gw)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += amp * np.asarray(g, float) / 255; tot += amp; amp *= 0.5
    return out / tot

def ramp(val, cols, dither=True):
    """val 0..1 → índice en una paleta con tramado ordenado tipo Bayer."""
    h, w = val.shape; n = len(cols) - 1
    v = np.clip(val, 0, 1) * n
    if dither:
        th = BAYER[np.arange(h)[:, None] % 4, np.arange(w)[None, :] % 4]
        idx = np.floor(v + (th - 0.5) * 0.9 + 0.5)
    else: idx = np.floor(v + 0.5)
    idx = np.clip(idx, 0, n).astype(int)
    return np.array(cols)[idx]

def save(img, name, k):
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)); im.save(name + '_1x.png')
    im.resize((im.width * k, im.height * k), Image.NEAREST).save(name + f'_x{k}.png'); return im

# ===================== D · Desierto brumoso (píxel grande) =====================
def desierto(storm=False, seed=3):
    W, H = 160, 90; img = np.zeros((H, W, 3))
    sky = [hx(c) for c in ('#E6C07E', '#E9C687', '#EDCC91', '#E3B77A')]
    for y in range(H): img[y] = sky[min(3, y * 4 // 60)]
    rnd = random.Random(seed)
    # capas de montañas: cada una más cercana = más oscura y contrastada
    layers = [  # (base_y, amp, freq, color claro, color sombra)
        (40, 10, 1.6, '#E8B57A', '#DDA56C'),
        (47, 14, 2.3, '#D99B60', '#C9874F'),
        (55, 13, 3.1, '#B9783F', '#9C6233'),
    ]
    if storm: layers = [(b, a, f, '#D8A877', '#CF9C6D') for b, a, f, _, _ in layers]
    for li, (base, amp, fr, cl, cd) in enumerate(layers):
        ph = rnd.uniform(0, 6.28); n1 = vnoise(W, 1, 18 - li * 4, seed + li, 3)[0]
        top = [int(base - amp * (0.5 + 0.5 * math.sin(2 * math.pi * fr * x / W + ph)) * (0.6 + 0.8 * n1[x])) for x in range(W)]
        for x in range(W):
            for y in range(top[x], H):
                slope = top[min(W - 1, x + 1)] - top[x]
                c = hx(cd) if slope < 0 or (y - top[x]) > (amp * 0.9) else hx(cl)   # caras que miran a la derecha en sombra
                if (y - top[x]) == 2 and li < 2: c = hx(cl) * 1.04                 # borde iluminado
                img[y, x] = c
    # llanura (suelo caminable plano)
    gy = 66
    sand = vnoise(W, H - gy, 6, seed + 9, 3)
    cols = [hx(c) for c in ('#C9803F', '#D68F49', '#E09A52', '#E6A35B')]
    img[gy:] = ramp(0.25 + 0.5 * sand + np.linspace(0, 0.2, H - gy)[:, None], cols, dither=False)
    for x in range(W): img[gy, x] = hx('#EDB46C')
    # rocas en primer plano con sombra de contacto
    def rock(cx, by, w, h):
        prof = vnoise(w, 1, 3, cx, 2)[0]
        for i in range(w):
            hh = int(h * math.sin(math.pi * (i + 0.5) / w) ** 0.7 * (0.7 + 0.5 * prof[i]))
            for j in range(hh):
                y = by - j; x = cx - w // 2 + i
                if not (0 <= x < W and 0 <= y < H): continue
                c = hx('#9A6A43') if i < w * 0.45 and j > hh * 0.4 else hx('#7B5032')
                if j == hh - 1 and i < w * 0.6: c = hx('#B07D52')
                if i > w * 0.7 or j < 2: c = hx('#4A2E1C')
                img[y, x] = c
        for i in range(w + 4):
            x = cx - w // 2 + i
            if 0 <= x < W and by + 1 < H: img[by + 1, x] = hx('#B8733A')
    for (cx, w, h) in [(18, 26, 12), (40, 14, 7), (128, 10, 4), (88, 6, 3), (148, 7, 3)]:
        rock(cx, gy + 4 + (2 if w < 12 else 0), w, h)
    if storm:   # polvo en suspensión
        dust = vnoise(W, H, 20, 77, 3)
        a = np.clip(0.25 + 0.35 * dust, 0, 0.6)[..., None]
        img = img * (1 - a) + hx('#D9A672') * a
        pal = [hx(c) for c in ('#8E5A33', '#A8714A', '#BF8A5C', '#D09E6E', '#DDAF7E', '#E8C08C')]
        lum = np.clip((img.mean(2) - 110) / 115, 0, 1)
        img = np.array(ramp(lum, pal, dither=False))
    return img

# ===================== E · Noche marciana estrellada =====================
def noche(seed=5):
    W, H = 384, 216; rnd = random.Random(seed); img = np.zeros((H, W, 3))
    t = np.linspace(0, 1, 150)[:, None] * np.ones((1, W))
    sky = ramp(t ** 1.6, [hx(c) for c in ('#0E0B22', '#14122E', '#1B1B3D', '#232A55', '#2D3E73', '#3F5C93', '#5F86B6')])
    img[:150] = sky; img[150:] = hx('#5F86B6')
    for _ in range(170):  # estrellas
        x, y = rnd.randrange(W), rnd.randrange(130); b = rnd.random()
        img[y, x] = hx('#FFF2D8') if b > 0.85 else (hx('#C9B7E0') if b > 0.5 else hx('#7E7BAA'))
        if b > 0.97:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= x + dx < W and 0 <= y + dy < H: img[y + dy, x + dx] = hx('#E58A5A')
    # la Tierra vista desde Marte: un punto azul brillante
    ex, ey = 96, 64
    for dx, dy, c in ((0, 0, '#BFE6FF'), (1, 0, '#6FB6FF'), (0, 1, '#6FB6FF'), (-1, 0, '#3E7BD0'), (0, -1, '#3E7BD0')): img[ey + dy, ex + dx] = hx(c)
    # Fobos grande con tramado (luna con cráteres) y Deimos pequeño
    def moon(cx, cy, r, lit=(-0.7, -0.5)):
        n = vnoise(2 * r + 2, 2 * r + 2, r / 2, cx, 3)
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                d = math.hypot((x - cx) / r, (y - cy) / (r * 0.85))
                if d <= 1:
                    nz = math.sqrt(max(0, 1 - d * d)); nx, ny = (x - cx) / r, (y - cy) / r
                    l = max(0, -(nx * lit[0] + ny * lit[1]) * 0.8 + nz * 0.5)
                    v = l * 0.85 + (n[y - cy + r, x - cx + r] - 0.5) * 0.35
                    img[y, x] = ramp(np.array([[v]]), [hx(c) for c in ('#2A1E2E', '#5A3540', '#8C5048', '#B87256', '#D9946A')], dither=False)[0, 0]
                    if (x + y) % 2 and 0.3 < v < 0.6: img[y, x] = img[y, x] * 0.9
    moon(300, 52, 26); moon(212, 40, 6)
    # resplandor azul del horizonte
    for y in range(130, 160):
        k = (y - 130) / 30
        for x in range(W):
            if (x + y) % 2 == 0 or k > 0.5: img[y, x] = img[y, x] * (1 - 0.5 * k) + hx('#7FA9D6') * 0.5 * k
    # picos dentados en silueta (dos capas) y suelo rojo
    def peaks(base, amp, cols, seedk, freq):
        n = vnoise(W, 1, 10, seedk, 4)[0]; r2 = random.Random(seedk)
        top = [int(base - amp * (max(0, math.sin(2 * math.pi * freq * x / W + seedk)) ** 1.5 * 0.55 + max(0, math.sin(2 * math.pi * freq * 2.3 * x / W + 2 * seedk)) ** 3 * 0.35 + (n[x] - 0.3) * 0.7)) for x in range(W)]
        for x in range(W):
            for y in range(max(0, top[x]), H):
                rel = (y - top[x])
                lit = top[x] < top[x - 1] if x > 0 else True
                c = cols[0] if lit and rel < 6 else cols[1]
                if rel > 10: c = cols[2] if (x + y) % 2 or rel > 16 else cols[1]
                img[y, x] = hx(c)
        return top
    peaks(170, 34, ('#7A3A44', '#5C2B3B', '#3E1F33'), 11, 2.2)
    peaks(182, 26, ('#B2473A', '#86352F', '#5A2630'), 23, 3.4)
    # llanura en primer plano (suelo plano) con textura
    gy = 184; n = vnoise(W, H - gy, 8, 31, 3)
    img[gy:] = ramp(0.2 + 0.6 * n + np.linspace(0.3, -0.2, H - gy)[:, None], [hx(c) for c in ('#4A2230', '#6E2E2E', '#93402F', '#B95A38', '#D47A45')])
    img[gy] = hx('#E39A5C')
    return img

# ===================== F · Planeta Marte con tramado =====================
def planeta(rot=0.0, seed=8, R=56):
    S = 2 * R + 8; img = np.zeros((S, S, 3)); img[:] = hx('#14121F'); c = S // 2
    # mapa de superficie (lat/lon) procedimental
    MW, MH = 360, 180
    base = vnoise(MW, MH, 40, seed, 5)
    lat = np.linspace(90, -90, MH)[:, None]; lon = np.linspace(-180, 180, MW)[None, :]
    # Valles Marineris: cañón oscuro largo cerca del ecuador; Olympus Mons: mancha clara
    canyon = np.exp(-((lat + 8 + 3 * np.sin(lon / 9)) / 2.2) ** 2) * ((lon > -75) & (lon < 20)) * (0.6 + 0.4 * np.sin(lon / 4)) + 0.6 * np.exp(-((lat + 2 + 0.4 * (lon + 70)) / 1.8) ** 2) * ((lon > -90) & (lon < -60))
    olymp = np.exp(-(((lat - 18) / 6) ** 2 + ((lon + 110) / 6) ** 2))
    dark = np.exp(-((lat + 25) / 18) ** 2) * (0.5 + 0.5 * np.sin(np.radians(lon) * 2 + 1))   # regiones oscuras del sur
    alb = 0.55 + 0.6 * (base - 0.5) - 0.45 * canyon + 0.3 * olymp - 0.25 * dark
    cap = (lat > 72) | (lat < -80)
    cols = [hx(x) for x in ('#3A1C2A', '#5E2A2C', '#8A3A2A', '#B5502C', '#D86A2E', '#F08A34', '#FBA94A')]
    for y in range(S):
        for x in range(S):
            dx, dy = (x - c) / R, (y - c) / R; d2 = dx * dx + dy * dy
            if d2 > 0.985: continue
            z = math.sqrt(1 - d2)
            tl = math.radians(22); ry = -dy * math.cos(tl) + z * math.sin(tl); rz = z * math.cos(tl) + dy * math.sin(tl)
            la = math.degrees(math.asin(max(-1, min(1, ry)))); lo = math.degrees(math.atan2(dx, rz)) + rot
            lo = (lo + 180) % 360 - 180
            mi, mj = int((90 - la) / 180 * (MH - 1)), int((lo + 180) / 360 * (MW - 1))
            light = max(0.0, dx * -0.45 + dy * -0.3 + z * 0.85)          # luz desde arriba a la izquierda
            v = alb[mi, mj] * (0.35 + 0.95 * light)
            v = min(1, max(0, v + (BAYER[y % 4, x % 4] - 0.5) * 0.12))
            col = cols[min(len(cols) - 1, int(v * (len(cols) - 1) + 0.5))]
            if cap[mi, 0] and light > 0.15: col = hx('#F6E7D2') if light > 0.45 else hx('#C9B4B0')
            img[y, x] = col
            if 0.94 < d2 and light > 0.35 and dx < 0: img[y, x] = img[y, x] * 0.6 + hx('#FFB36B') * 0.4   # atmósfera en el borde
    return img

if __name__ == '__main__':
    save(desierto(), 'idea_D_desierto', 6)
    save(desierto(storm=True), 'idea_D2_tormenta', 6)
    save(noche(), 'idea_E_noche', 3)
    save(planeta(), 'idea_F_planeta', 5)
    frames = [Image.fromarray(planeta(rot=r).astype(np.uint8)).resize((120 * 4, 120 * 4), Image.NEAREST) for r in range(0, 360, 10)]
    frames[0].save('idea_F_planeta_gira.gif', save_all=True, append_images=frames[1:], duration=90, loop=0)
