# Montaje de los movimientos I y II (P03 a P09). 0 creditos.
import subprocess, sys, json, math
from pathlib import Path
import numpy as np
from PIL import Image

RAIZ = Path(r"C:\Users\guill\Desktop\Juego 2d-hd\Nasa_Game\Fase_1_Arte\Exploracion")
CLIPS = RAIZ / "Lote_10" / "clips"
K07 = RAIZ / "Lote_09" / "L09b_K07_final_r1.png"
TMP = Path(__file__).parent / "seg"
TMP.mkdir(exist_ok=True)
W, H, FPS = 1280, 720, 24
PX, PY = 0.60 * W, 0.36 * H  # P* en el cuadro

ENC = ["-c:v", "libx264", "-preset", "slow", "-crf", "8", "-pix_fmt", "yuv420p10le", "-an"]


def ff(args):
    print(" ".join(map(str, args))[:300])
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + [str(a) for a in args], check=True)


def seg_clip(nombre, src, ss, nframes, vf):
    ff(["-ss", ss, "-i", CLIPS / src, "-vf", vf + ",fps=24", "-frames:v", nframes] + ENC + [TMP / f"{nombre}.mkv"])


def escritor(nombre):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                             "-r", str(FPS), "-i", "-"] + ENC + [str(TMP / f"{nombre}.mkv")], stdin=subprocess.PIPE)


def lector(src, extra_vf, ss=None, t=None):
    a = ["ffmpeg", "-v", "error"]
    if ss is not None:
        a += ["-ss", str(ss)]
    if t is not None:
        a += ["-t", str(t)]
    a += ["-i", str(src), "-vf", extra_vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.run(a, capture_output=True, check=True)
    buf = np.frombuffer(p.stdout, np.uint8)
    return buf.reshape(-1, H, W, 3)


def colocar(plate, k, ax, ay, tx, ty, ss=2):
    """Escala plate por k y pone su punto (ax, ay) en (tx, ty) del cuadro, con precision subpixel."""
    Wb, Hb = W * ss, H * ss
    kk = k * ss
    sw = max(1, int(math.ceil(plate.width * kk)))
    sh = max(1, int(math.ceil(plate.height * kk)))
    pre = plate.resize((sw, sh), Image.LANCZOS)
    rx, ry = sw / plate.width, sh / plate.height  # escala real del pre
    res = kk / rx  # escala residual (~1)
    # coordenadas de salida -> entrada (pre)
    a = 1 / res
    c = ax * rx - tx * ss * a
    f = ay * ry - ty * ss * a
    out = pre.transform((Wb, Hb), Image.AFFINE, (a, 0, c, 0, a, f), resample=Image.BICUBIC, fillcolor=(0, 0, 0))
    if ss != 1:
        out = out.resize((W, H), Image.LANCZOS)
    return out


# ---------- P07: la Tierra (imagen fija) ----------
def placa_tierra():
    im = np.asarray(Image.open(K07).convert("RGB")).astype(np.float32)
    lum = im.mean(axis=2)
    hh = im.shape[0]
    # circulo ajustado por minimos cuadrados al borde iluminado (derecha y cima)
    pts = []
    for y in range(470, 1515, 5):
        xs = np.where(lum[y] > 25)[0]
        if len(xs):
            pts.append((xs[-1], y))
    for x in range(1300, 2200, 10):
        ys = np.where(lum[:, x] > 25)[0]
        if len(ys):
            pts.append((x, ys[0]))
    P = np.array(pts, float)
    A = np.c_[2 * P[:, 0], 2 * P[:, 1], np.ones(len(P))]
    sol = np.linalg.lstsq(A, (P ** 2).sum(1), rcond=None)[0]
    cx, cy = sol[0], sol[1]
    r = math.sqrt(sol[2] + cx * cx + cy * cy) - 1.0
    corte = hh - 1
    print(f"K07: r {r:.1f}, centro ({cx:.1f}, {cy:.1f}), corte {corte}, base {cy + r:.0f}")
    m = 40
    S = int(2 * (r + m))
    ox, oy = cx - r - m, cy - r - m
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    gx, gy = xx + ox, yy + oy  # coordenadas en K07
    # relleno del casquete que falta: junto al corte, espejo sobre el corte (continuo);
    # mas abajo, espejo sobre el ecuador del disco (mismo radio: el borde y la atmosfera casan)
    xi = np.clip(np.round(gx).astype(int), 0, im.shape[1] - 1)
    y_corte = np.clip(np.round(2 * corte - gy).astype(int), 0, hh - 1)
    y_ecu = np.clip(np.round(2 * cy - gy).astype(int), 0, hh - 1)
    y_dir = np.clip(np.round(gy).astype(int), 0, hh - 1)
    a_dir, a_cor, a_ecu = im[y_dir, xi], im[y_corte, xi], im[y_ecu, xi]
    # fundido de 140 px que termina 30 filas antes del corte (las ultimas filas de K07 vienen estiradas)
    fin = corte - 30
    tb = np.clip((gy - (fin - 140)) / 140.0, 0, 1)
    wb = (tb * tb * (3 - 2 * tb))[..., None]
    placa = (1 - wb) * a_dir + wb * a_ecu
    espejo = gy > fin - 140
    fuera = (gy < 0) | (gx < 0) | (gx > im.shape[1] - 1)
    placa[fuera] = 0
    nx, ny = (gx - cx) / r, (gy - cy) / r
    rho = np.sqrt(nx ** 2 + ny ** 2)
    disco = np.clip((r + 0.75 - rho * r) / 1.5, 0, 1)
    # en la mitad baja se recorta al circulo; queda un halo azul de 14 px
    halo = np.where(rho > 1, np.clip(1 - (rho - 1) * r / 14.0, 0, 1), 1)
    baja = ny > 0.25
    placa[baja] *= np.maximum(disco, halo * 0.9)[baja][:, None]
    # banda de noche abajo a la izquierda (terminador suave) que cubre casi todo el relleno
    n = np.array([-0.30, 0.95]); n /= np.linalg.norm(n)
    d = nx * n[0] + ny * n[1]
    t = np.clip((d - 0.08) / (0.50 - 0.08), 0, 1)
    sombra = 1 - t * t * (3 - 2 * t)
    placa *= sombra[..., None]
    placa = np.clip(placa, 0, 255).astype(np.uint8)
    img = Image.fromarray(placa)
    img.save(TMP / "placa_tierra.png")
    return img, r + m, m, r  # (ax, ay) = cima del disco en la placa


def seg_p07(nframes, t0):
    placa, ax, ay, r = placa_tierra()
    p = escritor("S07")
    for i in range(nframes):
        t = t0 + i / FPS  # tiempo dentro del plano (0 a 8 s)
        frac = math.exp(math.log(0.60) + (math.log(0.25) - math.log(0.60)) * (t / 8.0))
        k = frac * H / (2 * r)
        fr = colocar(placa, k, ax, ay, PX, PY)
        p.stdin.write(np.asarray(fr, np.uint8).tobytes())
    p.stdin.close(); p.wait()


# ---------- P09: estirado, acercamiento y congelado ----------
def seg_p09(gain):
    # 0 a 4,0 s del clip estirados a 5,0 s con interpolacion de movimiento
    fr = lector(CLIPS / "P09_elegido.mp4",
                "setpts=1.25*PTS,minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
                ss=0, t=4.0)
    fr = fr[:120]
    print("P09 cuadros estirados:", len(fr))
    p = escritor("S09")
    cxp, cyp = 0.50 * W, 0.55 * H
    ultimo = None
    for i in range(216):
        if i < 120:
            src = fr[min(i, len(fr) - 1)].astype(np.float32) * gain
            img = Image.fromarray(np.clip(src, 0, 255).astype(np.uint8))
            z = 1.0 + 0.12 * (i / 119.0)  # constante, se detiene en seco a los 5 s
            ultimo = colocar(img, z, cxp, cyp, cxp, cyp)
        p.stdin.write(np.asarray(ultimo, np.uint8).tobytes())
    p.stdin.close(); p.wait()


def luma_superficie(arr):
    l = arr.astype(np.float32) @ np.array([0.2126, 0.7152, 0.0722])
    return float(l[l > 20].mean())


if __name__ == "__main__":
    paso = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if paso in ("clips", "todo"):
        seg_clip("S03", "P03_elegido.mp4", 0, 216, "scale=1280:720:flags=lanczos")
        seg_clip("S04", "P04_elegido.mp4", 0.5, 180, "crop=1184:666:0:27,scale=1280:720:flags=lanczos")
        seg_clip("S05", "P05_elegido.mp4", 0, 156, "scale=1280:720:flags=lanczos")
        seg_clip("S06", "P06_elegido.mp4", 0, 162,
                 "crop=2286:1286:269:41,scale=1280:720:flags=lanczos,tpad=stop_mode=clone:stop_duration=0.5")
        seg_clip("S08", "P08_elegido.mp4", 0, 162, f"setpts=PTS*{6.75/6.584:.5f},scale=1280:720:flags=lanczos")
    if paso in ("p07", "todo"):
        seg_p07(228, -0.75)
    if paso in ("p09", "todo"):
        a = lector(CLIPS / "P08_elegido.mp4", "scale=1280:720", ss=6.4)[-1]
        b = lector(CLIPS / "P09_elegido.mp4", "scale=1280:720", ss=0, t=0.1)[0]
        la, lb = luma_superficie(a), luma_superficie(b)
        gain = la / lb
        print(f"luma superficie P08 fin {la:.1f}, P09 inicio {lb:.1f}, ganancia {gain:.3f}")
        json.dump({"P08_fin": la, "P09_inicio": lb, "ganancia": gain}, open(TMP / "luma.json", "w"))
        seg_p09(gain)
