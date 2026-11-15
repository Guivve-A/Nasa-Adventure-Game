# Parche de los brazos de la torre de P04: cambia el enrejado con seudoletras
# por una celosia lisa (diagonales regulares). El color se toma de cada cuadro
# (cordones oscuros del propio brazo y cielo de encima), asi sigue el resplandor.
import sys, glob, os
import numpy as np
from PIL import Image

entrada, salida = sys.argv[1], sys.argv[2]
os.makedirs(salida, exist_ok=True)
archivos = sorted(glob.glob(os.path.join(entrada, "*.png")))
cuadros = [np.asarray(Image.open(a).convert("RGB")).astype(np.float32) for a in archivos]
n = len(cuadros)

# brazo: filas de las marcas (y0..y1 incl.), filas de cordones oscuros, fila de cielo, x0..x1
BRAZOS = [
    dict(y0=168, y1=175, cordon=[166, 167, 176, 177, 178], cielo=158, x0=668, x1=738),
    dict(y0=270, y1=278, cordon=[268, 269, 279, 280, 281], cielo=259, x0=668, x1=740),
    dict(y0=383, y1=390, cordon=[381, 382, 391, 392, 393], cielo=372, x0=668, x1=740),
]
PLUMA = 3        # px de fundido en los extremos izquierdo y derecho
PERIODO = 12.0   # px por cada V de la celosia
MEZCLA = 0.34   # fuerza de las diagonales hacia el color del cielo
rng = np.random.default_rng(7)


def suavizar_x(v, k=9):
    # media movil por columnas, con bordes replicados
    pad = k // 2
    vp = np.pad(v, ((pad, pad), (0, 0)), mode="edge")
    c = np.cumsum(vp, axis=0)
    c = np.vstack([np.zeros((1, v.shape[1])), c])
    return (c[k:] - c[:-k]) / k


# colores por cuadro y columna
bases, cielos = [], []
for b in BRAZOS:
    xs = slice(b["x0"] - 4, b["x1"] + 5)
    base_t, cielo_t = [], []
    for im in cuadros:
        base = np.median(im[b["cordon"], xs], axis=0)
        cielo = im[b["cielo"] - 2:b["cielo"] + 1, xs].mean(axis=0)
        base_t.append(suavizar_x(base)[4:-4])
        cielo_t.append(suavizar_x(cielo)[4:-4])
    base_t, cielo_t = np.array(base_t), np.array(cielo_t)
    # suavizado temporal de 7 cuadros para que no parpadee
    k = 7
    bp = np.pad(base_t, ((k // 2, k // 2), (0, 0), (0, 0)), mode="edge")
    cp = np.pad(cielo_t, ((k // 2, k // 2), (0, 0), (0, 0)), mode="edge")
    bases.append(np.array([bp[i:i + k].mean(axis=0) for i in range(n)]))
    cielos.append(np.array([cp[i:i + k].mean(axis=0) for i in range(n)]))

# patron de celosia fijo para cada brazo (0..1), linea de 1 px con antialias
patrones, mascaras = [], []
for b in BRAZOS:
    h, w = b["y1"] - b["y0"] + 1, b["x1"] - b["x0"] + 1
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = (xx % PERIODO) / PERIODO           # 0..1 dentro de cada V
    zig = np.abs(2 * t - 1) * (h - 1)      # diagonal que baja y sube
    d = np.abs(yy - zig)
    pat = np.clip(1.2 - d, 0, 1)
    # montantes verticales finos en cada vertice inferior
    post = np.clip(1.0 - np.abs(((xx + PERIODO / 2) % PERIODO) - 0.0), 0, 1) * 0.5
    pat = np.maximum(pat, post)
    # desenfoque leve (1-2-1) para igualar la suavidad del video
    pp = np.pad(pat, 1, mode="edge")
    pat = (pp[:-2, 1:-1] + 2 * pp[1:-1, 1:-1] + pp[2:, 1:-1]) / 4
    pp = np.pad(pat, 1, mode="edge")
    pat = (pp[1:-1, :-2] + 2 * pp[1:-1, 1:-1] + pp[1:-1, 2:]) / 4
    pat = np.clip(pat * 1.3, 0, 1)
    patrones.append(pat[..., None])
    m = np.ones((h, w), np.float32)
    rampa = np.clip((xx + 1) / PLUMA, 0, 1) * np.clip((w - xx) / PLUMA, 0, 1)
    mascaras.append((m * rampa)[..., None])

for i, im in enumerate(cuadros):
    out = im.copy()
    for j, b in enumerate(BRAZOS):
        y0, y1, x0, x1 = b["y0"], b["y1"], b["x0"], b["x1"]
        base = bases[j][i][None, :, :]
        cielo = cielos[j][i][None, :, :]
        linea = base + MEZCLA * (cielo - base)
        relleno = base + patrones[j] * (linea - base)
        ruido = rng.normal(0, 1.6, relleno.shape[:2])[..., None]
        relleno = relleno + ruido
        zona = out[y0:y1 + 1, x0:x1 + 1]
        out[y0:y1 + 1, x0:x1 + 1] = zona + mascaras[j] * (relleno - zona)
    Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(
        os.path.join(salida, os.path.basename(archivos[i])))
print("cuadros", n)
