"""Enfoque B: repinta PER-01 desde la hoja con una deformacion 2D no rigida por vista.

Parte de proyectar_hoja.py (v3). Tras la alineacion global (una escala y un
desplazamiento por IoU de silueta), cada vista calcula un thin-plate spline (TPS)
que lleva el contorno exterior de la silueta rasterizada de la malla al contorno
de la hoja. Los pares salen de muestrear ambos contornos por longitud de arco
desde el punto mas alto (modo "arco") o de un emparejamiento monotono por
programacion dinamica sobre esas muestras (modo "dtw"). Puntos interiores fijos
(lejos de ambos contornos) frenan los pliegues. Se comprueba que el
determinante del jacobiano sea positivo en toda la silueta; si no, se sube la
regularizacion del TPS.

Peso por vista: visible * max(0, n.d)^1 * mascara(hoja en el punto deformado).
Mezcla: (suma(peso_v * hoja_v) + 0.01 * original) / (suma(peso_v) + 0.01) donde
alguna vista ve el texel; donde ninguna lo ve queda la textura original.
Opcional (--rasante): donde todas las vistas ven el texel muy de lado, se
vuelve suavemente a la textura original para no estirar colores.

Uso: python -I herramientas/mallas/proyectar_hoja_B.py [--pares dtw|arco] [--rasante 0.3]
Solo requiere numpy y Pillow. No modifica geometria, UV ni materiales.
"""
import argparse
import hashlib
import io
import json
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from proyectar_hoja import (CAJAS, EJES, HOJA, LOTE, alinear, fragmentos,  # noqa: E402
                            geometria, guardar_glb, leer_glb, mascara,
                            rasterizar, rellenar_bordes)

MARGEN = 160          # lienzo extra alrededor de la caja para el campo de deformacion
PASO_CAMPO = 2        # resolucion del campo TPS en pixeles de la hoja
DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]  # horario, y hacia abajo


# ---------------------------------------------------------------- mascaras y contornos

def rellenar_huecos(m):
    """Rellena los huecos internos: inunda el fondo desde el borde con un marco de 1 px."""
    p = np.pad(m, 1).astype(np.uint8) * 255
    # copy(): la imagen creada desde numpy es de solo lectura y floodfill no la cambiaria
    img = Image.fromarray(p).copy()
    ImageDraw.floodfill(img, (0, 0), 128)
    return (np.asarray(img) != 128)[1:-1, 1:-1]


def erosionar(m, radio):
    if radio <= 0:
        return m.copy()
    img = Image.fromarray(m.astype(np.uint8) * 255)
    # MinFilter con ventana grande es lento; se encadenan ventanas de 7 (radio 3).
    while radio > 0:
        r = min(radio, 3)
        img = img.filter(ImageFilter.MinFilter(2 * r + 1))
        radio -= r
    return np.asarray(img) > 0


def dilatar(m, radio):
    return ~erosionar(~m, radio)


def trazar_contorno(m):
    """Trazado de Moore del contorno exterior del componente que contiene el punto mas alto.

    Empieza en el pixel mas alto mas cercano al centro horizontal y recorre en
    sentido horario (en la imagen, con y hacia abajo). Devuelve (n, 2) en (x, y).
    """
    p = np.pad(m, 1)
    ys, xs = np.nonzero(p)
    y0 = ys.min()
    fila = xs[ys == y0]
    x0 = int(fila[np.argmin(np.abs(fila - xs.mean()))])
    inicio = (x0, int(y0))
    k = 0  # el vecino de retroceso esta al norte (fondo)
    actual = inicio
    puntos = [inicio]
    segundo = None
    for _ in range(200000):
        for i in range(1, 9):
            k2 = (k + i) % 8
            c = (actual[0] + DIRS[k2][0], actual[1] + DIRS[k2][1])
            if p[c[1], c[0]]:
                break
        else:
            break  # pixel aislado
        previo = (actual[0] + DIRS[(k2 - 1) % 8][0], actual[1] + DIRS[(k2 - 1) % 8][1])
        if actual == inicio and segundo is not None and c == segundo:
            break
        if segundo is None:
            segundo = c
        actual = c
        k = DIRS.index((previo[0] - c[0], previo[1] - c[1]))
        puntos.append(c)
    pts = np.array(puntos[:-1] if puntos[-1] == inicio else puntos, float) - 1.0
    return pts


def remuestrear(pts, n):
    """n puntos equiespaciados por longitud de arco sobre el contorno cerrado, desde pts[0]."""
    cerrado = np.vstack((pts, pts[:1]))
    seg = np.linalg.norm(np.diff(cerrado, axis=0), axis=1)
    acum = np.concatenate(([0], np.cumsum(seg)))
    t = np.linspace(0, acum[-1], n, endpoint=False)
    x = np.interp(t, acum, cerrado[:, 0])
    y = np.interp(t, acum, cerrado[:, 1])
    return np.column_stack((x, y))


def emparejar_dtw(a, b):
    """Emparejamiento monotono de dos contornos cerrados con el mismo inicio.

    Devuelve, para cada punto de a, la media de los puntos de b emparejados.
    """
    n, k = len(a), len(b)
    c = np.linalg.norm(a[:, None] - b[None], axis=2)
    d = np.full((n + 1, k + 1), np.inf)
    d[0, 0] = 0
    for i in range(1, n + 1):
        fila = c[i - 1]
        prev = d[i - 1]
        # min(diagonal, arriba) vectorizado; luego el termino de la izquierda en bucle acumulado
        base = np.minimum(prev[:-1], prev[1:]) + fila
        di = d[i]
        for j in range(1, k + 1):
            v = base[j - 1]
            w = di[j - 1] + fila[j - 1]
            di[j] = v if v < w else w
    # camino de vuelta
    i, j = n, k
    pares = []
    while i > 0 and j > 0:
        pares.append((i - 1, j - 1))
        opciones = (d[i - 1, j - 1], d[i - 1, j], d[i, j - 1])
        m = int(np.argmin(opciones))
        if m == 0:
            i, j = i - 1, j - 1
        elif m == 1:
            i -= 1
        else:
            j -= 1
    suma = np.zeros((n, 2))
    cuenta = np.zeros(n)
    for ia, jb in pares:
        suma[ia] += b[jb]
        cuenta[ia] += 1
    return suma / np.maximum(cuenta, 1)[:, None]


# ---------------------------------------------------------------- thin-plate spline

def _u(r2):
    with np.errstate(divide="ignore", invalid="ignore"):
        v = 0.5 * r2 * np.log(r2)
    return np.nan_to_num(v)


class TPS:
    def __init__(self, origen, destino, lam, escala):
        self.s = escala
        c = origen / escala
        t = destino / escala
        n = len(c)
        K = _u(((c[:, None] - c[None]) ** 2).sum(-1))
        P = np.column_stack((np.ones(n), c))
        A = np.zeros((n + 3, n + 3))
        A[:n, :n] = K + lam * np.eye(n)
        A[:n, n:] = P
        A[n:, :n] = P.T
        B = np.zeros((n + 3, 2))
        B[:n] = t
        sol = np.linalg.solve(A, B)
        self.c, self.w, self.a = c, sol[:n], sol[n:]

    def __call__(self, pts):
        p = pts / self.s
        out = np.empty_like(p)
        for i in range(0, len(p), 20000):
            q = p[i:i + 20000]
            U = _u(((q[:, None] - self.c[None]) ** 2).sum(-1))
            out[i:i + 20000] = U @ self.w + self.a[0] + q @ self.a[1:]
        return out * self.s


# ---------------------------------------------------------------- vista con deformacion

class VistaB:
    def __init__(self, nombre, hoja, pos, idx, carpeta, args):
        self.nombre = nombre
        self.tolerancia = args.tolerancia_px
        self.exponente = args.exponente
        self.rgb =np.asarray(hoja.crop(CAJAS[nombre]).convert("RGB"))
        m0, self.fondo = mascara(self.rgb)
        # apertura 3x3 para quitar motas sueltas
        self.m = dilatar(erosionar(m0, 1), 1) & m0
        h, w = self.m.shape
        self.eje, self.direccion = map(lambda a: np.array(a, float), EJES[nombre])
        # cache de la alineacion global (lenta: decenas de rasterizados por vista)
        clave = hashlib.sha256(self.m.tobytes() + pos.tobytes() + idx.tobytes()).hexdigest()
        ruta_cache = carpeta / f"{nombre}_alineacion_cache.json"
        cache = json.loads(ruta_cache.read_text(encoding="utf-8")) if ruta_cache.exists() else {}
        if cache.get("clave") == clave:
            self.escala, self.tras, self.info = cache["escala"], np.array(cache["tras"]), cache["info"]
        else:
            self.escala, self.tras, self.info = alinear(pos, idx, self.eje, self.m)
            ruta_cache.write_text(json.dumps({"clave": clave, "escala": float(self.escala),
                                              "tras": np.asarray(self.tras).tolist(), "info": self.info}), encoding="utf-8")
        q = self.proyectar(pos)

        # visibilidad (igual que v3): bufer de profundidad al doble y planos por triangulo
        self.super = 2
        self.z, self.du = rasterizar((q + MARGEN) * self.super, pos @ self.direccion, idx,
                                     (w + 2 * MARGEN) * self.super, (h + 2 * MARGEN) * self.super)
        matrices = np.concatenate((q[idx], np.ones((len(idx), 3, 1))), axis=2)
        validos = np.abs(np.linalg.det(matrices)) > 1e-10
        self.planos = np.zeros((len(idx), 3))
        self.planos[validos] = np.linalg.solve(matrices[validos], (pos @ self.direccion)[idx][validos, :, None])[..., 0]

        # silueta de la malla en el lienzo con margen
        _, du1 = rasterizar(q + MARGEN, np.zeros(len(pos)), idx, w + 2 * MARGEN, h + 2 * MARGEN)
        sil_malla = rellenar_huecos(du1 >= 0)
        sil_hoja = rellenar_huecos(np.pad(self.m, MARGEN))
        self.sil_malla, self.sil_hoja = sil_malla, sil_hoja

        # contornos y pares
        cm = trazar_contorno(sil_malla)
        ch = trazar_contorno(sil_hoja)
        n_den = 600
        am = remuestrear(cm, n_den)
        ah = remuestrear(ch, n_den)
        paso = n_den // args.puntos
        if args.pares == "dtw":
            destino_den = emparejar_dtw(am, ah)
        else:
            destino_den = ah
        origen = am[::paso]
        destino = destino_den[::paso]

        # puntos interiores fijos: lejos de los dos contornos
        dentro = erosionar(sil_malla, args.dist_interior) & erosionar(sil_hoja, args.dist_interior)
        gy, gx = np.mgrid[0:dentro.shape[0]:args.rejilla, 0:dentro.shape[1]:args.rejilla]
        sel = dentro[gy, gx]
        fijos = np.column_stack((gx[sel], gy[sel])).astype(float)
        self.n_contorno, self.n_fijos = len(origen), len(fijos)
        todos_o = np.vstack((origen, fijos))
        todos_d = np.vstack((destino, fijos))
        if args.sin_deformacion:  # control: misma tuberia sin TPS (campo identidad)
            destino = origen.copy()
            todos_d = todos_o.copy()

        # TPS con regularizacion creciente hasta que el jacobiano sea positivo
        hh, ww = sil_malla.shape
        cy, cx = np.mgrid[0:hh + PASO_CAMPO:PASO_CAMPO, 0:ww + PASO_CAMPO:PASO_CAMPO]
        rejilla = np.column_stack((cx.ravel(), cy.ravel())).astype(float)
        zona = dilatar(sil_malla, 6)
        zona_g = zona[np.minimum(cy, hh - 1), np.minimum(cx, ww - 1)]
        historial = []
        for lam in args.lambdas:
            tps = TPS(todos_o, todos_d, lam, float(h))
            campo = tps(rejilla).reshape(cy.shape + (2,))
            dxx = np.gradient(campo[..., 0], PASO_CAMPO, axis=1)
            dxy = np.gradient(campo[..., 0], PASO_CAMPO, axis=0)
            dyx = np.gradient(campo[..., 1], PASO_CAMPO, axis=1)
            dyy = np.gradient(campo[..., 1], PASO_CAMPO, axis=0)
            det = dxx * dyy - dxy * dyx
            dz = det[zona_g]
            residuo = np.linalg.norm(tps(origen) - destino, axis=1)
            historial.append({"lambda": lam, "det_min": float(dz.min()), "det_p1": float(np.percentile(dz, 1)),
                              "det_max": float(dz.max()), "residuo_contorno_medio_px": float(residuo.mean()),
                              "residuo_contorno_max_px": float(residuo.max())})
            print(f"  {nombre}: lambda {lam:g}, det min {dz.min():.3f}, p1 {np.percentile(dz, 1):.3f}, "
                  f"max {dz.max():.3f}, residuo medio {residuo.mean():.2f} px", flush=True)
            if dz.min() > args.det_min:
                break
        else:
            raise RuntimeError(f"{nombre}: el TPS se pliega con todas las regularizaciones")
        self.campo = campo  # coordenadas destino (lienzo con margen) en la rejilla de paso PASO_CAMPO
        self.det = det
        self.lam = lam
        desplaz = np.linalg.norm(campo - np.stack((cx, cy), -1), axis=-1)[zona_g]

        # hoja extendida: el color de cada pixel de fondo es el del pixel interior mas cercano
        nucleo = erosionar(self.m, 2)
        ext = np.pad(self.rgb, ((MARGEN, MARGEN), (MARGEN, MARGEN), (0, 0))).copy()
        ocupado = np.pad(nucleo, MARGEN)
        ext[~ocupado] = 0
        rellenar_bordes(ext, ocupado, pasos=40)
        self.ext = ext.astype(np.float32)
        self.m_valida = dilatar(np.pad(self.m, MARGEN), 2)
        self.contribuciones = self.ocultos = self.fuera = 0

        self.info.update({"tps_lambda": lam, "tps_historial": historial,
                          "puntos_contorno": self.n_contorno, "puntos_fijos": self.n_fijos,
                          "pares": args.pares, "desplazamiento_medio_px": float(desplaz.mean()),
                          "desplazamiento_max_px": float(desplaz.max()),
                          "long_contorno_malla_px": float(np.linalg.norm(np.diff(np.vstack((cm, cm[:1])), axis=0), axis=1).sum()),
                          "long_contorno_hoja_px": float(np.linalg.norm(np.diff(np.vstack((ch, ch[:1])), axis=0), axis=1).sum())})
        self.diagnosticos(carpeta, origen, destino, fijos, q, pos, idx)

    def proyectar(self, puntos):
        return np.column_stack((puntos @ self.eje, -puntos[:, 1])) * self.escala + self.tras

    def deformar(self, qm):
        """qm en coordenadas del lienzo con margen; devuelve el punto de la hoja (mismo lienzo)."""
        g = qm / PASO_CAMPO
        hh, ww = self.campo.shape[:2]
        x = np.clip(g[:, 0], 0, ww - 1.001)
        y = np.clip(g[:, 1], 0, hh - 1.001)
        x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
        fx, fy = (x - x0)[:, None], (y - y0)[:, None]
        c = self.campo
        return (c[y0, x0] * (1 - fx) * (1 - fy) + c[y0, x0 + 1] * fx * (1 - fy)
                + c[y0 + 1, x0] * (1 - fx) * fy + c[y0 + 1, x0 + 1] * fx * fy)

    def muestrear_hoja(self, p):
        hh, ww = self.ext.shape[:2]
        x = np.clip(p[:, 0], 0, ww - 1.001)
        y = np.clip(p[:, 1], 0, hh - 1.001)
        x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
        fx, fy = (x - x0)[:, None], (y - y0)[:, None]
        e = self.ext
        col = (e[y0, x0] * (1 - fx) * (1 - fy) + e[y0, x0 + 1] * fx * (1 - fy)
               + e[y0 + 1, x0] * (1 - fx) * fy + e[y0 + 1, x0 + 1] * fx * fy)
        valida = self.m_valida[np.rint(y).astype(int), np.rint(x).astype(int)]
        return col, valida

    def muestrear(self, puntos, normales, triangulo):
        qm = self.proyectar(puntos) + MARGEN
        hh, ww = self.sil_malla.shape
        dot = normales @ self.direccion
        pesos = np.zeros(len(puntos), np.float32)
        colores = np.zeros((len(puntos), 3), np.float32)
        valido = (qm[:, 0] >= 0) & (qm[:, 0] < ww - 1) & (qm[:, 1] >= 0) & (qm[:, 1] < hh - 1) & (dot > 0)
        ids = np.flatnonzero(valido)
        if not len(ids):
            return colores, pesos
        pix = np.rint(qm[ids] * self.super).astype(int)
        du = self.du[pix[:, 1], pix[:, 0]]
        zreal = puntos[ids] @ self.direccion
        qv = qm[ids] - MARGEN
        pl = self.planos[np.maximum(du, 0)]
        zvisible = (pl[:, :2] * qv).sum(1) + pl[:, 2]
        # Tolerancia de profundidad de unos 3 px de la hoja: con 2e-5 m (v3) los texels del borde de
        # cada triangulo caian sobre el plano del vecino, se rechazaban y dejaban lineas de la original.
        # Brazo y torso estan separados por varios centimetros, asi que la oclusion real se sigue detectando.
        tol = self.tolerancia / self.escala
        visible = (du >= 0) & ((du == triangulo[ids]) | (zreal >= zvisible - tol))
        self.ocultos += int((~visible).sum())
        ids = ids[visible]
        if not len(ids):
            return colores, pesos
        destino = self.deformar(qm[ids])
        col, ok = self.muestrear_hoja(destino)
        self.fuera += int((~ok).sum())
        ids, col = ids[ok], col[ok]
        colores[ids] = col
        pesos[ids] = np.maximum(dot[ids], 0) ** self.exponente
        self.contribuciones += len(ids)
        return colores, pesos

    def diagnosticos(self, carpeta, origen, destino, fijos, q, pos, idx):
        hh, ww = self.sil_malla.shape
        # 1) siluetas, pares y puntos fijos
        sup = np.full((hh, ww, 3), 40, np.uint8)
        sup[self.sil_hoja & self.sil_malla] = [200, 200, 200]
        sup[self.sil_hoja & ~self.sil_malla] = [220, 60, 60]
        sup[self.sil_malla & ~self.sil_hoja] = [70, 110, 230]
        img = Image.fromarray(sup)
        d = ImageDraw.Draw(img)
        for o, t in zip(origen, destino):
            d.line([tuple(o), tuple(t)], fill=(255, 220, 0), width=1)
            d.ellipse([o[0] - 2, o[1] - 2, o[0] + 2, o[1] + 2], fill=(0, 200, 255))
            d.ellipse([t[0] - 2, t[1] - 2, t[0] + 2, t[1] + 2], fill=(255, 120, 0))
        for f in fijos:
            d.rectangle([f[0] - 1, f[1] - 1, f[0] + 1, f[1] + 1], fill=(0, 255, 0))
        d.ellipse([origen[0][0] - 5, origen[0][1] - 5, origen[0][0] + 5, origen[0][1] + 5], outline=(255, 0, 255), width=2)
        img.save(carpeta / f"{self.nombre}_pares.png")
        # 2) la hoja vista a traves de la deformacion, solo dentro de la silueta de la malla
        cy, cx = np.mgrid[0:hh, 0:ww]
        pts = np.column_stack((cx.ravel(), cy.ravel())).astype(float)
        dentro = self.sil_malla.ravel()
        out = np.full((hh * ww, 3), 60, np.float32)
        col, ok = self.muestrear_hoja(self.deformar(pts[dentro]))
        col[~ok] = [255, 0, 255]
        out[dentro] = col
        Image.fromarray(out.reshape(hh, ww, 3).astype(np.uint8)).save(carpeta / f"{self.nombre}_hoja_deformada.png")
        # 3) rejilla deformada (lineas cada 20 px del espacio de la malla llevadas a la hoja)
        base = np.pad(self.rgb, ((MARGEN, MARGEN), (MARGEN, MARGEN), (0, 0)), constant_values=90)
        img = Image.fromarray(base.copy())
        d = ImageDraw.Draw(img)
        for x in range(0, ww, 20):
            ys = np.arange(0, hh, 4, dtype=float)
            keep = self.sil_malla[ys.astype(int), x]
            p = self.deformar(np.column_stack((np.full(len(ys), x, float), ys)))
            for i in range(len(ys) - 1):
                if keep[i] and keep[i + 1]:
                    d.line([tuple(p[i]), tuple(p[i + 1])], fill=(0, 230, 255), width=1)
        for y in range(0, hh, 20):
            xs = np.arange(0, ww, 4, dtype=float)
            keep = self.sil_malla[y, xs.astype(int)]
            p = self.deformar(np.column_stack((xs, np.full(len(xs), y, float))))
            for i in range(len(xs) - 1):
                if keep[i] and keep[i + 1]:
                    d.line([tuple(p[i]), tuple(p[i + 1])], fill=(0, 230, 255), width=1)
        img.save(carpeta / f"{self.nombre}_rejilla.png")
        # 4) mapa del determinante del jacobiano
        det = self.det
        v = np.clip((det - 0.0) / 2.0, 0, 1)
        mapa = np.stack((255 * (1 - v), 255 * v, 80 * np.ones_like(v)), -1).astype(np.uint8)
        hg, wg = det.shape
        zona = self.sil_malla[np.minimum(np.arange(hg) * PASO_CAMPO, hh - 1)][:, np.minimum(np.arange(wg) * PASO_CAMPO, ww - 1)]
        mapa[~zona] = 30
        Image.fromarray(mapa).resize((wg * PASO_CAMPO, hg * PASO_CAMPO), Image.NEAREST).save(carpeta / f"{self.nombre}_jacobiano.png")


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", type=Path, default=LOTE / "L04_PER01_giro_tripo_mv.glb")
    ap.add_argument("--salida", type=Path, default=LOTE / "L04_PER01_v4B.glb")
    ap.add_argument("--hoja", type=Path, default=HOJA)
    ap.add_argument("--diagnosticos", type=Path, default=LOTE / "parecido/v4B")
    ap.add_argument("--pares", choices=("dtw", "arco"), default="dtw")
    ap.add_argument("--puntos", type=int, default=100, help="pares de contorno por vista (60 a 120)")
    ap.add_argument("--rejilla", type=int, default=45, help="separacion de los puntos fijos interiores, px")
    ap.add_argument("--dist-interior", type=int, default=30, help="distancia minima de los fijos a ambos contornos, px")
    ap.add_argument("--lambdas", type=float, nargs="+", default=[0.0, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1])
    ap.add_argument("--det-min", type=float, default=0.05, help="determinante minimo aceptado del jacobiano")
    ap.add_argument("--peso-original", type=float, default=0.01)
    ap.add_argument("--exponente", type=float, default=1.0, help="exponente de max(0, n.d) en el peso de cada vista")
    ap.add_argument("--rasante", type=float, default=0.0,
                    help="si > 0, vuelve a la original donde el mejor peso de vista es menor que este valor")
    ap.add_argument("--tolerancia-px", type=float, default=3.0,
                    help="tolerancia de profundidad para la visibilidad, en pixeles de la hoja")
    ap.add_argument("--sin-deformacion", action="store_true", help="control sin TPS (solo alineacion global)")
    ap.add_argument("--solo-deformacion", action="store_true", help="calcula la deformacion y sus diagnosticos, sin hornear")
    a = ap.parse_args()
    if a.entrada.resolve() == a.salida.resolve():
        raise ValueError("La salida no puede sobrescribir la entrada")
    inicio = time.monotonic()
    a.diagnosticos.mkdir(parents=True, exist_ok=True)
    doc, binario = leer_glb(a.entrada)
    pos, uv, idx, normales, original, imid = geometria(doc, binario)
    hoja = Image.open(a.hoja).convert("RGB")
    vistas = []
    for nombre in CAJAS:
        print(f"Alineando y deformando {nombre}...", flush=True)
        v = VistaB(nombre, hoja, pos, idx, a.diagnosticos, a)
        vistas.append(v)
        print(f"  IoU global {v.info['iou']:.4f}, contorno {v.n_contorno} + fijos {v.n_fijos}, "
              f"desplazamiento medio {v.info['desplazamiento_medio_px']:.1f} px", flush=True)
    if a.solo_deformacion:
        return

    h, w = original.shape[:2]
    tex = original.copy()
    ocupado = np.zeros((h, w), bool)
    pintado = np.zeros((h, w), bool)
    uvs = uv * [w, h] - 0.5
    po = a.peso_original
    bloque = 300
    for t0 in range(0, len(idx), bloque):
        YY, XX, TT, BB = [], [], [], []
        for t in range(t0, min(t0 + bloque, len(idx))):
            f = fragmentos(uvs[idx[t]], w, h)
            if f is None:
                continue
            yy, xx, b = f
            YY.append(yy); XX.append(xx); BB.append(b); TT.append(np.full(len(yy), t, np.int32))
        if not YY:
            continue
        yy, xx, b, tri = np.concatenate(YY), np.concatenate(XX), np.concatenate(BB), np.concatenate(TT)
        vt = idx[tri]
        puntos = (b[:, :, None] * pos[vt]).sum(1)
        n = (b[:, :, None] * normales[vt]).sum(1)
        n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        orig = original[yy, xx].astype(np.float32)
        acum = np.zeros((len(yy), 3), np.float32)
        peso = np.zeros(len(yy), np.float32)
        pmax = np.zeros(len(yy), np.float32)
        for vista in vistas:
            color, pv = vista.muestrear(puntos, n, tri)
            acum += color * pv[:, None]
            peso += pv
            pmax = np.maximum(pmax, pv)
        visto = peso > 0
        mezcla = (acum + po * orig) / (peso + po)[:, None]
        if a.rasante > 0:
            s = smoothstep(a.rasante, 0.5 * a.rasante, pmax)[:, None]
            mezcla = mezcla * (1 - s) + orig * s
        final = np.where(visto[:, None], mezcla, orig)
        tex[yy, xx] = np.clip(np.rint(final), 0, 255).astype(np.uint8)
        ocupado[yy, xx] = True
        pintado[yy, xx] = visto
        print(f"Horneando triangulo {min(t0 + bloque, len(idx))}/{len(idx)}", flush=True)

    print("Rellenando bordes UV...", flush=True)
    padding = rellenar_bordes(tex, ocupado)
    imagen = Image.fromarray(tex)
    imagen.save(a.diagnosticos / "textura.png")
    Image.fromarray(pintado).save(a.diagnosticos / "texels_hoja.png")
    buf = io.BytesIO()
    imagen.save(buf, format="PNG")
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    guardar_glb(a.salida, doc, binario, buf.getvalue(), imid)
    d2, b2 = leer_glb(a.salida)
    d0, b0 = leer_glb(a.entrada)
    assert b2[:len(b0)] == b0
    for clave in ("meshes", "nodes", "accessors", "materials", "textures", "scenes"):
        assert d2[clave] == d0[clave], clave
    assert d2["bufferViews"][:-1] == d0["bufferViews"]
    meta = {"entrada": str(a.entrada), "salida": str(a.salida), "hoja": str(a.hoja),
            "sha256_entrada": hashlib.sha256(a.entrada.read_bytes()).hexdigest(),
            "sha256_hoja": hashlib.sha256(a.hoja.read_bytes()).hexdigest(),
            "argumentos": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(a).items()},
            "triangulos": len(idx), "textura_px": [w, h],
            "texels_superficie": int(ocupado.sum()), "texels_con_hoja": int(pintado.sum()),
            "texels_con_hoja_pct_superficie": float(100 * pintado.sum() / ocupado.sum()),
            "padding_texels": padding,
            "vistas": {v.nombre: {**v.info, "muestras_aceptadas": v.contribuciones,
                                    "muestras_ocultas_rechazadas": v.ocultos,
                                    "muestras_fuera_de_mascara": v.fuera} for v in vistas},
            "segundos": round(time.monotonic() - inicio, 1)}
    (a.diagnosticos / "horneado.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("texels_con_hoja_pct_superficie", "segundos")}), flush=True)


if __name__ == "__main__":
    main()
