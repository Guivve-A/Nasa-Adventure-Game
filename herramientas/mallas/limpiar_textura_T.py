"""Estrategia T: limpia la textura proyectada de PER-01 (v5C) volviendo a la de Tripo donde la hoja es poco fiable.

Por texel (posicion y normal en 3D a partir de la malla y sus UV):
  g = max(n.d) sobre las tres vistas proyectadas (+X frente, -X espalda, +Z perfil derecho).
  - g < 0,35: textura ORIGINAL de Tripo (de L04_PER01_v4D_geometria.glb, mismas UV);
  - 0,35 <= g <= 0,6: mezcla suave (smoothstep);
  - g > 0,6: la de v5C.
  Ademas van enteros con Tripo:
  - el costado izquierdo de la cabeza (normal dominante -Z, y > 0,15);
  - la cadera, el gluteo y el muslo derechos, donde quedo pintado el bolso de la hoja
    (la version final lleva un bolso 3D aparte);
  - los mechones de pelo de la hoja que cayeron sobre piel junto a las orejas (Tripo dice piel,
    la hoja dice pelo, detras del ojo).
Lo que se toma de Tripo se ajusta en Lab (media y pendiente) por zona hacia los texels de v5C bien
proyectados (g >= 0,6) de la misma zona. Zona = banda de altura (cabeza, torso, piernas, pies) x grupo
de color de Tripo (k-medias), con pertenencia suave para no crear saltos de tono.
Despues:
  - repara las lineas finas sobre las aristas de los triangulos (texels de borde que en v5C perdieron la
    vista buena por la prueba de profundidad y quedaron con otro color);
  - baja un 30 % la saturacion y el brillo (HSV) de los reflejos naranjas del pelo (y > 0,15);
  - redondea el brillo cuadrado del ojo derecho del personaje (izquierda de la imagen de frente);
  - dilata las islas UV 16 px desde su interior (el filtrado no trae colores ajenos).

Uso: python -I herramientas/mallas/limpiar_textura_T.py [--v5c ...] [--tripo ...] [--salida ...] [--diagnosticos ...]
Solo requiere numpy y Pillow. No modifica geometria, UV ni materiales: solo cambia la imagen.
"""
import argparse
import hashlib
import io
import json
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import proyectar_hoja as ph  # noqa: E402
from proyectar_hoja_C import a_lab, asignar, bilineal, de_lab, kmeans  # noqa: E402

LOTE = ph.LOTE
G_BAJO, G_ALTO = 0.35, 0.6
Y_CABEZA = 0.15
DIRECCIONES = np.array([[1, 0, 0], [-1, 0, 0], [0, 0, 1]], np.float32)


def smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


# ---------- rasterizado en UV ----------
def rasterizar_uv(pos, uv, idx, w, h):
    """Por texel ocupado: indice plano, triangulo, posicion, normal de cara y distancia a la arista (px)."""
    uvs = uv * [w, h] - 0.5
    planos, tris, ps, ns, dists = [], [], [], [], []
    caras = np.cross(pos[idx[:, 1]] - pos[idx[:, 0]], pos[idx[:, 2]] - pos[idx[:, 0]])
    caras /= np.maximum(np.linalg.norm(caras, axis=1, keepdims=True), 1e-12)
    for t, v in enumerate(idx):
        tri = uvs[v]
        f = ph.fragmentos(tri, w, h)
        if f is None:
            continue
        yy, xx, b = f
        # altura de cada vertice sobre la arista opuesta, en px de textura
        area2 = abs((tri[1, 0] - tri[0, 0]) * (tri[2, 1] - tri[0, 1]) - (tri[2, 0] - tri[0, 0]) * (tri[1, 1] - tri[0, 1]))
        lados = np.array([np.linalg.norm(tri[2] - tri[1]), np.linalg.norm(tri[0] - tri[2]), np.linalg.norm(tri[1] - tri[0])])
        alturas = area2 / np.maximum(lados, 1e-9)
        planos.append(yy * w + xx)
        tris.append(np.full(len(yy), t, np.int32))
        ps.append((b @ pos[v]).astype(np.float32))
        ns.append(np.repeat(caras[t][None].astype(np.float32), len(yy), 0))
        dists.append((b * alturas[None]).min(1).astype(np.float32))
    plano = np.concatenate(planos)
    # Un texel compartido por varios triangulos se queda con el ultimo (como en los horneados previos).
    orden = np.arange(len(plano))
    _, ultimo = np.unique(plano[::-1], return_index=True)
    sel = orden[::-1][ultimo]
    return (plano[sel], np.concatenate(tris)[sel], np.concatenate(ps)[sel],
            np.concatenate(ns)[sel], np.concatenate(dists)[sel])


def normales_suaves(pos, idx, normales_vert, plano_tri, tris, ps):
    """Normal interpolada (la del GLB) en cada texel: baricentricas recalculadas en 3D."""
    a, b, c = (pos[idx[tris, k]] for k in range(3))
    v0, v1, v2 = b - a, c - a, ps - a
    d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1)
    d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1)
    den = np.where(np.abs(d00 * d11 - d01 * d01) < 1e-18, 1e-18, d00 * d11 - d01 * d01)
    l1 = (d11 * d20 - d01 * d21) / den
    l2 = (d00 * d21 - d01 * d20) / den
    l0 = 1 - l1 - l2
    n = (l0[:, None] * normales_vert[idx[tris, 0]] + l1[:, None] * normales_vert[idx[tris, 1]]
         + l2[:, None] * normales_vert[idx[tris, 2]])
    return (n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)).astype(np.float32)


def preparar(ruta_v5c, ruta_tripo, cache):
    doc5, bin5 = ph.leer_glb(ruta_v5c)
    doc0, bin0 = ph.leer_glb(ruta_tripo)
    pos, uv, idx, nv, tex5, imid = ph.geometria(doc5, bin5)
    pos0, uv0, idx0, _, tex0, _ = ph.geometria(doc0, bin0)
    if not (np.array_equal(pos, pos0) and np.array_equal(uv, uv0) and np.array_equal(idx, idx0)):
        raise ValueError("v5C y la malla de Tripo no comparten geometria y UV")
    if tex5.shape != tex0.shape:
        raise ValueError("Las texturas no tienen el mismo tamano")
    h, w = tex5.shape[:2]
    firma = hashlib.sha256(bin5[:200000] + bin0[:200000] + str(tex5.shape).encode()).hexdigest()[:16]
    if cache and cache.exists():
        d = np.load(cache)
        if str(d["firma"]) == firma:
            return doc5, bin5, imid, pos, idx, tex5, tex0, {k: d[k] for k in d.files}
    print("Rasterizando UV...", flush=True)
    plano, tris, ps, nc, dist = rasterizar_uv(pos, uv, idx, w, h)
    ns = normales_suaves(pos, idx, nv, plano, tris, ps)
    datos = {"plano": plano, "tris": tris, "ps": ps, "nc": nc, "ns": ns, "dist": dist, "firma": np.array(firma)}
    if cache:
        np.savez(cache, **datos)
    return doc5, bin5, imid, pos, idx, tex5, tex0, datos


# ---------- componentes conexos (sin scipy) ----------
def etiquetar(m):
    """Componentes 4-conexos de una mascara booleana por tramos de fila y union-busqueda."""
    h, w = m.shape
    padre = [0]

    def raiz(i):
        while padre[i] != i:
            padre[i] = padre[padre[i]]
            i = padre[i]
        return i

    tramos = []
    previos = []
    for y in range(h):
        dif = np.diff(np.concatenate(([0], m[y].astype(np.int8), [0])))
        ini, fin = np.flatnonzero(dif == 1), np.flatnonzero(dif == -1)
        actuales = []
        j = 0
        for x0, x1 in zip(ini.tolist(), fin.tolist()):
            nid = len(padre)
            padre.append(nid)
            while j < len(previos) and previos[j][1] <= x0:
                j += 1
            k = j
            while k < len(previos) and previos[k][0] < x1:
                ra, rb = raiz(nid), raiz(previos[k][2])
                if ra != rb:
                    padre[max(ra, rb)] = min(ra, rb)
                k += 1
            actuales.append((x0, x1, nid))
            tramos.append((y, x0, x1, nid))
        previos = actuales
    raices = np.array([raiz(i) for i in range(len(padre))], np.int32)
    _, compacto = np.unique(raices, return_inverse=True)
    lab = np.zeros((h, w), np.int32)
    for y, x0, x1, nid in tramos:
        lab[y, x0:x1] = compacto[nid]
    return lab, int(compacto.max()) + 1


def rellenar_onion(tex, conocido, objetivo, pasos=400, vecinos8=True):
    """Rellena 'objetivo' desde 'conocido' capa a capa con la media de los vecinos ya conocidos."""
    tex = tex.astype(np.float32)
    k = conocido.copy()
    falta = objetivo & ~k
    desp = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if vecinos8:
        desp += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    h, w = k.shape
    for _ in range(pasos):
        if not falta.any():
            break
        vec = np.zeros_like(k)
        vec[1:] |= k[:-1]; vec[:-1] |= k[1:]; vec[:, 1:] |= k[:, :-1]; vec[:, :-1] |= k[:, 1:]
        yy, xx = np.nonzero(vec & falta)
        if not len(yy):
            break
        suma = np.zeros((len(yy), 3), np.float32)
        cuenta = np.zeros(len(yy), np.float32)
        for dy, dx in desp:
            y, x = yy + dy, xx + dx
            ok = (y >= 0) & (y < h) & (x >= 0) & (x < w)
            ids = np.flatnonzero(ok)
            ids = ids[k[y[ids], x[ids]]]
            peso = 1.0 if dy == 0 or dx == 0 else 0.7
            suma[ids] += peso * tex[y[ids], x[ids]]
            cuenta[ids] += peso
        tex[yy, xx] = suma / cuenta[:, None]
        k[yy, xx] = True
        falta[yy, xx] = False
    return tex, k


def tirar_empujar(tex, conocido):
    """Relleno de todo lo desconocido con una piramide de medias (sin bordes duros a ninguna escala)."""
    niveles = [(tex.astype(np.float32) * conocido[..., None], conocido.astype(np.float32))]
    while min(niveles[-1][1].shape) > 1:
        c, p = niveles[-1]
        h, w = p.shape
        c = c[:h // 2 * 2, :w // 2 * 2].reshape(h // 2, 2, w // 2, 2, 3).sum((1, 3))
        p = p[:h // 2 * 2, :w // 2 * 2].reshape(h // 2, 2, w // 2, 2).sum((1, 3))
        niveles.append((c, p))
    c, p = niveles[-1]
    col = c / np.maximum(p, 1e-6)[..., None]
    for c, p in reversed(niveles[:-1]):
        sube = np.repeat(np.repeat(col, 2, 0), 2, 1)
        sube = np.pad(sube, ((0, p.shape[0] - sube.shape[0]), (0, p.shape[1] - sube.shape[1]), (0, 0)), mode="edge")
        propio = c / np.maximum(p, 1e-6)[..., None]
        a = np.clip(p, 0, 1)[..., None]
        col = a * propio + (1 - a) * sube
    return col


def abrir_cerrar(m, cuarto, modo):
    """Apertura o cierre morfologico a 1/4 de resolucion con filtros de rango de Pillow."""
    h, w = m.shape
    im = Image.fromarray(m.astype(np.uint8) * 255).resize((w // 4, h // 4), Image.BOX)
    im = im.point(lambda v: 255 if v >= 128 else 0)
    f1, f2 = (ImageFilter.MaxFilter, ImageFilter.MinFilter) if modo == "cerrar" else (ImageFilter.MinFilter, ImageFilter.MaxFilter)
    im = im.filter(f1(cuarto)).filter(f2(cuarto))
    return np.asarray(im.resize((w, h), Image.NEAREST)) > 127


# ---------- color ----------
def lab_a_lch(lab):
    return np.hypot(lab[:, 1], lab[:, 2]), np.degrees(np.arctan2(lab[:, 2], lab[:, 1]))


def rgb_a_hsv(c):
    c = c / 255.0
    mx, mn = c.max(1), c.min(1)
    v = mx
    s = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
    d = np.maximum(mx - mn, 1e-6)
    r, g, b = c.T
    hh = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6.0
    return np.column_stack((hh, s, v))


def hsv_a_rgb(hsv):
    h, s, v = hsv.T
    i = np.floor(h * 6).astype(int) % 6
    f = h * 6 - np.floor(h * 6)
    p, q, t = v * (1 - s), v * (1 - f * s), v * (1 - (1 - f) * s)
    r = np.choose(i, [v, q, p, p, t, v]); g = np.choose(i, [t, v, v, q, p, p]); b = np.choose(i, [p, p, t, v, v, q])
    return np.column_stack((r, g, b)) * 255.0


BANDAS = [("cabeza", 0.16, 9.0), ("torso", 0.0, 0.16), ("piernas", -0.38, 0.0), ("pies", -9.0, -0.38)]
RAMPA_BANDA = 0.015
K_ZONAS = 6
SIGMA_ZONA = 8.0


def nombre_zona(banda, c):
    L, a, b = c
    croma = np.hypot(a, b)
    if banda == "pies":
        return "zapatos"
    if L < 40 and banda == "cabeza":
        return "pelo"
    if a > 12 and b > 22 and L > 48 and croma > 30:
        return "piel"
    if banda == "piernas":
        return "pantalon"
    if banda == "torso" and L > 60:
        return "camisa"
    if banda == "torso" and L < 35:
        return "camiseta"
    return "otro"


def ajustar_zonas(lab0, lab5, y, bueno, objetivo, semilla=11):
    """Lleva el Lab de Tripo hacia v5C por banda de altura x grupo de color (pertenencia suave).

    En cada grupo: (o - media_o) * r + media_n, con r = corr * sd_n / sd_o acotada a [0,5; 1,5]
    (la pendiente de la regresion: el ruido de registro de v5C no infla el contraste).
    Las medias y desviaciones se miden en los texels buenos (v5C bien proyectado) de la zona.
    """
    salida = np.zeros((len(objetivo), 3), np.float32)
    peso_total = np.zeros(len(objetivo), np.float32)
    info = []
    rng = np.random.default_rng(semilla)
    yo = y[objetivo]
    o_obj = lab0[objetivo]
    for nombre, lo, hi in BANDAS:
        pb_todos = smooth(lo - RAMPA_BANDA, lo + RAMPA_BANDA, y) * (1 - smooth(hi - RAMPA_BANDA, hi + RAMPA_BANDA, y))
        en_banda = pb_todos > 0.5
        ids = np.flatnonzero(en_banda)
        muestra = lab0[rng.choice(ids, min(150_000, len(ids)), replace=False)].astype(np.float64)
        cen = kmeans(muestra.copy(), K_ZONAS)
        sel = np.flatnonzero(en_banda & bueno)
        g = asignar(lab0[sel], cen)
        o_all, n_all = lab0[sel].astype(np.float64), lab5[sel].astype(np.float64)
        mapas = []
        for k in range(K_ZONAS):
            s = g == k
            if s.sum() < 1500:
                s = np.ones(len(sel), bool)
            o, n = o_all[s], n_all[s]
            # recorte robusto: fuera los texels de v5C muy lejos de la mediana del grupo (otro material)
            med = np.median(n, 0)
            cerca = np.linalg.norm(n - med, axis=1) < 25
            if cerca.sum() > 500:
                o, n = o[cerca], n[cerca]
            mo, so = o.mean(0), o.std(0) + 1e-3
            mn, sn = n.mean(0), n.std(0) + 1e-3
            corr = ((o - mo) * (n - mn)).mean(0) / (so * sn)
            r = np.clip(corr * sn / so, 0.5, 1.5)
            mapas.append((mo, mn, r))
            info.append({"banda": nombre, "grupo": k, "zona": nombre_zona(nombre, cen[k]),
                         "centro_tripo_lab": np.round(cen[k], 1).tolist(), "texels_buenos": int((g == k).sum()),
                         "media_tripo": np.round(mo, 1).tolist(), "media_v5c": np.round(mn, 1).tolist(),
                         "pendiente": np.round(r, 3).tolist()})
        pb = pb_todos[objetivo]
        act = np.flatnonzero(pb > 0)
        if not len(act):
            continue
        for i in range(0, len(act), 500_000):
            trozo = act[i:i + 500_000]
            o = o_obj[trozo].astype(np.float64)
            d2 = ((o[:, None, :] - cen[None]) ** 2).sum(-1)
            d2 -= d2.min(1, keepdims=True)
            wk = np.exp(-d2 / (2 * SIGMA_ZONA ** 2))
            wk /= wk.sum(1, keepdims=True)
            adj = np.zeros((len(trozo), 3))
            for k, (mo, mn, r) in enumerate(mapas):
                adj += wk[:, k:k + 1] * ((o - mo) * r + mn)
            salida[trozo] += (pb[trozo, None] * adj).astype(np.float32)
            peso_total[trozo] += pb[trozo]
    salida /= np.maximum(peso_total, 1e-6)[:, None]
    return salida, info


AREA_HUECO = 8000
FRAC_BORDE = 0.75


def huecos(falta, bueno):
    """Componentes pequenos de 'falta' rodeados casi del todo por 'bueno' (no por vacio de la UV)."""
    h, w = falta.shape
    lab_c, n_c = etiquetar(falta)
    area = np.bincount(lab_c[falta], minlength=n_c)
    borde_bueno = np.zeros(n_c, np.float64)
    borde_total = np.zeros(n_c, np.float64)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        vec = np.zeros_like(falta)
        lab_v = np.zeros_like(lab_c)
        ys = slice(max(dy, 0), h + min(dy, 0)); yd = slice(max(-dy, 0), h + min(-dy, 0))
        xs = slice(max(dx, 0), w + min(dx, 0)); xd = slice(max(-dx, 0), w + min(-dx, 0))
        vec[yd, xd] = falta[ys, xs]
        lab_v[yd, xd] = lab_c[ys, xs]
        frontera = vec & ~falta
        borde_total += np.bincount(lab_v[frontera], minlength=n_c)
        borde_bueno += np.bincount(lab_v[frontera & bueno], minlength=n_c)
    frac = borde_bueno / np.maximum(borde_total, 1)
    es = (area <= AREA_HUECO) & (frac >= FRAC_BORDE)
    es[0] = False
    return falta & es[lab_c], int(es.sum()), int(n_c - 1)


# ---------- ojo derecho ----------
CAJA_OJO = {"y": (0.268, 0.322), "z": (0.015, 0.065), "x_min": 0.12, "nx_min": 0.4}
CELDA_OJO = 0.0002   # 0,2 mm por celda en el plano frontal (z, y)


def reparar_ojo(final, ps, ns, hueco_b):
    """Cambia la zona del brillo cuadrado del ojo derecho (+Z) por la pupila del ojo izquierdo en espejo.

    El cuadro es un hueco del paso de la cara de v5C (hueco_b) dentro de la pupila derecha. Las dos
    pupilas de la hoja llevan el brillo redondo hacia la nariz, asi que la izquierda reflejada en z
    (respecto del centro de cada pupila) da la pupila y el brillo redondo que faltan.
    """
    yv, zv = ps[:, 1], ps[:, 2]
    base = (ns[:, 0] > CAJA_OJO["nx_min"]) & (ps[:, 0] > CAJA_OJO["x_min"]) & (yv > CAJA_OJO["y"][0]) & (yv < CAJA_OJO["y"][1])
    der = base & (zv > CAJA_OJO["z"][0]) & (zv < CAJA_OJO["z"][1])
    izq = base & (-zv > CAJA_OJO["z"][0]) & (-zv < CAJA_OJO["z"][1])
    lab = a_lab(final[der | izq])
    lum = np.zeros(len(final), np.float32)
    lum[der | izq] = lab[:, 0]
    croma = np.zeros(len(final), np.float32)
    croma[der | izq] = np.hypot(lab[:, 1], lab[:, 2])
    malos = der & hueco_b
    if malos.sum() < 20:
        return final, {"reparado": False, "motivo": "no se hallo el cuadro (hueco de la cara) en la pupila derecha"}
    centros = {}
    for nombre, m in (("der", der), ("izq", izq)):
        osc = m & (lum < 40) & ~hueco_b
        centros[nombre] = np.array([zv[osc].mean(), yv[osc].mean()])
    # zona a cambiar: caja del cuadro y del brillo propio, mas 1,2 mm
    # el cuadro esta dentro de la pupila: elipse de los texels oscuros (2 desviaciones), al 85 %
    osc = der & (lum < 40) & ~hueco_b
    sz, sy = 2 * zv[osc].std(), 2 * yv[osc].std()
    dentro = ((zv - centros["der"][0]) / (0.85 * sz)) ** 2 + ((yv - centros["der"][1]) / (0.85 * sy)) ** 2 <= 1
    malos = malos & dentro
    if malos.sum() < 20:
        return final, {"reparado": False, "motivo": "no hay huecos de la cara dentro de la pupila derecha"}
    # brillo propio: claro y sin color, a menos de 2 mm del cuadro (el blanco del ojo queda mas lejos)
    m0z, m1z, m0y, m1y = zv[malos].min(), zv[malos].max(), yv[malos].min(), yv[malos].max()
    junto = (zv > m0z - 0.002) & (zv < m1z + 0.002) & (yv > m0y - 0.002) & (yv < m1y + 0.002)
    brillo = der & junto & (lum > 75) & (croma < 25)
    zona = malos | brillo
    z0, z1 = zv[zona].min() - 0.0012, zv[zona].max() + 0.0012
    y0, y1 = yv[zona].min() - 0.0012, yv[zona].max() + 0.0012
    # imagen frontal del ojo izquierdo reflejado, en coordenadas relativas a su pupila
    cz, cy = centros["izq"]
    dz = -(zv[izq] - cz)            # reflejo en z
    dy = yv[izq] - cy
    lim = 0.03
    n = int(2 * lim / CELDA_OJO) + 1
    gx = np.clip(((dz + lim) / CELDA_OJO).astype(int), 0, n - 1)
    gy = np.clip(((dy + lim) / CELDA_OJO).astype(int), 0, n - 1)
    suma = np.zeros((n, n, 3), np.float64)
    cuenta = np.zeros((n, n), np.float64)
    np.add.at(suma, (gy, gx), final[izq])
    np.add.at(cuenta, (gy, gx), 1)
    rejilla = suma / np.maximum(cuenta, 1)[..., None]
    rejilla, _ = rellenar_onion(rejilla, cuenta > 0, np.ones((n, n), bool), pasos=n)
    # muestreo bilineal para los texels de la zona
    feather = 0.0008
    cerca = der & (zv > z0 - feather) & (zv < z1 + feather) & (yv > y0 - feather) & (yv < y1 + feather)
    ids = np.flatnonzero(cerca)
    rz = (zv[ids] - centros["der"][0] + lim) / CELDA_OJO - 0.5   # centros de celda
    ry = (yv[ids] - centros["der"][1] + lim) / CELDA_OJO - 0.5
    rz = np.clip(rz, 0, n - 1.001)
    ry = np.clip(ry, 0, n - 1.001)
    col = bilineal(rejilla.astype(np.float32), rz, ry)
    fuera = np.maximum.reduce([z0 - zv[ids], zv[ids] - z1, y0 - yv[ids], yv[ids] - y1, np.zeros(len(ids))])
    peso = 1 - smooth(0, feather, fuera)
    final = final.copy()
    final[ids] = peso[:, None] * col + (1 - peso[:, None]) * final[ids]
    return final, {"reparado": True, "texels_cuadro": int(malos.sum()), "texels_cambiados": int((peso > 0).sum()),
                   "centro_pupila_der_zy": np.round(centros["der"], 4).tolist(),
                   "centro_pupila_izq_zy": np.round(centros["izq"], 4).tolist(),
                   "caja_zy_m": [round(float(v), 4) for v in (z0, z1, y0, y1)]}


# ---------- correa de la espalda ----------
CORREA = {"arriba": ((-0.04, 0.12), (0.03, 0.02)),   # tramo pintado por encima del cinturon (z, y)
          "a": (0.050, -0.008), "b": (0.118, -0.058),  # prolongacion hasta el bolso 3D
          "ancho": 0.021}


def segmento(pz, py, a, b):
    a, b = np.array(a), np.array(b)
    d = b - a
    t = np.clip(((pz - a[0]) * d[0] + (py - a[1]) * d[1]) / (d @ d), 0, 1)
    return np.hypot(pz - (a[0] + t * d[0]), py - (a[1] + t * d[1]))


def prolongar_correa(final, c5, ps, ns):
    x, y, z, nx = ps[:, 0], ps[:, 1], ps[:, 2], ns[:, 0]
    muestra = (nx < -0.5) & (segmento(z, y, *CORREA["arriba"]) < 0.004)
    color = np.median(c5[muestra], 0)
    sel = np.flatnonzero((nx < 0.0) & (z > 0.02) & (z < 0.14) & (y > -0.085) & (y < 0.012))
    dist = segmento(z[sel], y[sel], CORREA["a"], CORREA["b"])
    medio = CORREA["ancho"] / 2
    peso = 1 - smooth(medio - 0.0012, medio + 0.0012, dist)
    borde = smooth(0.55 * medio, medio, dist)
    col = color[None] * (1 - 0.15 * borde[:, None])
    final = final.copy()
    final[sel] = peso[:, None] * col + (1 - peso[:, None]) * final[sel]
    return final, {"color_rgb": np.round(color, 1).tolist(), "texels_muestra": int(muestra.sum()),
                   "texels_pintados": int((peso > 0.5).sum()), **{k: v for k, v in CORREA.items()}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--v5c", type=Path, default=LOTE / "L04_PER01_v5C.glb")
    ap.add_argument("--v5c-diag", type=Path, default=LOTE / "parecido/v5C",
                    help="carpeta del horneado de v5C (texels_hoja.png y texels_cara.png)")
    ap.add_argument("--tripo", type=Path, default=LOTE / "L04_PER01_v4D_geometria.glb")
    ap.add_argument("--salida", type=Path, default=LOTE / "L04_PER01_v7T.glb")
    ap.add_argument("--diagnosticos", type=Path, default=LOTE / "parecido/v7T")
    ap.add_argument("--cache", type=Path, default=None, help="npz con el rasterizado UV (acelera repeticiones)")
    ap.add_argument("--dilatacion", type=int, default=16)
    ap.add_argument("--reduccion-brillos", type=float, default=0.30)
    ap.add_argument("--solo-preparar", action="store_true")
    ap.add_argument("--guardar-pesos", type=Path, default=None, help="npz de diagnostico con los pesos por texel")
    ap.add_argument("--desactivar", nargs="*", default=[], choices=["izq", "bolso", "brazo", "oreja_der", "mechon"],
                    help="reglas forzadas a omitir (pruebas)")
    a = ap.parse_args()
    if a.salida.resolve() in (a.v5c.resolve(), a.tripo.resolve()):
        raise ValueError("La salida no puede sobrescribir una entrada")
    t0 = time.monotonic()
    a.diagnosticos.mkdir(parents=True, exist_ok=True)
    doc5, bin5, imid5, pos, idx, tex5, tex0, d = preparar(a.v5c, a.tripo, a.cache)
    h, w = tex5.shape[:2]
    pl = d["plano"]
    print(f"texels ocupados {len(pl)} de {h * w}, {time.monotonic() - t0:.1f} s", flush=True)
    if a.solo_preparar:
        return
    ps, ns = d["ps"], d["ns"]
    x, y, z = ps[:, 0], ps[:, 1], ps[:, 2]
    nx, nz = ns[:, 0], ns[:, 2]
    ocupado = np.zeros(h * w, bool)
    ocupado[pl] = True
    ocupado = ocupado.reshape(h, w)
    info = {}

    # 1) Huecos de v5C, rellenados desde los texels buenos que los rodean:
    #    a) texels que ninguna vista acepto (fallo de la prueba de profundidad en las aristas) y que
    #       quedaron con la textura de Tripo ajustada: lineas punteadas claras y naranjas;
    #    b) texels de la cara donde el paso de la cara fallo y quedo la proyeccion del cuerpo, con otro
    #       registro: el cuadro claro dentro de la pupila del ojo derecho.
    hoja_m = np.asarray(Image.open(a.v5c_diag / "texels_hoja.png")) > 0
    cara_m = np.asarray(Image.open(a.v5c_diag / "texels_cara.png")) > 0
    if hoja_m.shape != (h, w) or cara_m.shape != (h, w):
        raise ValueError("Las mascaras de v5C no coinciden con la textura")
    visto = hoja_m | cara_m
    print("Etiquetando huecos...", flush=True)
    hueco_a, na, ca = huecos(ocupado & ~visto, visto)
    # (los puntos de a) cruzan la cara y unirian cada hueco de b con el cuerpo: cuentan como buenos)
    hueco_b, nb, cb = huecos(ocupado & ~cara_m & ~hueco_a, cara_m | hueco_a)
    hueco = hueco_a | hueco_b
    print(f"  visibilidad: {na} huecos, {int(hueco_a.sum())} texels; cara: {nb} huecos, {int(hueco_b.sum())} texels", flush=True)
    tex5r, _ = rellenar_onion(tex5, ocupado & ~hueco, hueco)
    tex5r = np.clip(np.rint(tex5r), 0, 255).astype(np.uint8)
    info["huecos"] = {"visibilidad": {"componentes": ca, "huecos": na, "texels": int(hueco_a.sum())},
                      "cara": {"componentes": cb, "huecos": nb, "texels": int(hueco_b.sum())},
                      "criterio": f"area <= {AREA_HUECO} texels y borde bueno >= {FRAC_BORDE:.0%}"}

    # 2) Pesos de v5C por texel.
    c5 = tex5r.reshape(-1, 3)[pl].astype(np.float32)
    c0 = tex0.reshape(-1, 3)[pl].astype(np.float32)
    lab5 = a_lab(c5).astype(np.float32)
    lab0 = a_lab(c0).astype(np.float32)
    g = np.maximum(np.abs(nx), nz)
    w_g = smooth(G_BAJO, G_ALTO, g)
    # En la cara registrada (paso de la cara de v5C, n.d > 0,2 con rampa a 0,3) la hoja es fiable a
    # menos inclinacion: alli se usa esa misma rampa, salvo en la cara inferior de la mandibula.
    en_cara = cara_m.reshape(-1)[pl] & ~hueco.reshape(-1)[pl]
    w_cara = en_cara * smooth(0.2, 0.3, nx) * (1 - smooth(0.5, 0.7, -ns[:, 1]))
    w_g = np.maximum(w_g, w_cara)
    f_izq = smooth(Y_CABEZA - 0.02, Y_CABEZA + 0.02, y) * smooth(-0.1, 0.1, -nz - np.abs(nx))
    tope = -0.01 + 0.045 * smooth(0.4, 0.7, nz)
    # de frente se respeta la correa pintada hasta el borde del bolso 3D (z = 0,058): el bolso de la hoja
    # que queda a la derecha de ese borde lo tapa el bolso 3D
    z_bolso = 0.015 + 0.045 * smooth(0.35, 0.55, nx)
    f_bolso = (smooth(z_bolso - 0.012, z_bolso + 0.012, z) * (1 - smooth(0.14, 0.16, z))
               * smooth(-0.212, -0.188, y) * (1 - smooth(tope - 0.012, tope + 0.012, y)))
    f_brazo = smooth(0.14, 0.16, z) * smooth(-0.22, -0.20, y) * (1 - smooth(0.08, 0.10, y))
    # oreja, patilla y mandibula del costado derecho (entre la nuca y el ojo): la vista de perfil de la
    # hoja corre ahi el mechon y el contorno de la mandibula; Tripo trae la misma patilla limpia
    # (debajo del rabillo del ojo, y < 0,29, llega hasta x = 0,105 para tomar todo el mechon)
    x_tope = 0.091 + 0.014 * (1 - smooth(0.282, 0.292, y))
    f_der = (smooth(0.17, 0.19, y) * (1 - smooth(0.29, 0.31, y)) * smooth(-0.01, 0.01, x)
             * (1 - smooth(x_tope - 0.006, x_tope + 0.006, x)) * smooth(-0.1, 0.1, nz - np.abs(nx)))
    # piel de Tripo (sin los brillos pequenos del pelo, por apertura) para la regla de mechones
    cr0, hue0 = lab_a_lch(lab0)
    piel0 = (lab0[:, 0] > 50) & (cr0 > 30) & (hue0 > 35) & (hue0 < 75)
    m = np.zeros(h * w, bool); m[pl] = piel0
    piel0_ab = abrir_cerrar(m.reshape(h, w), 5, "abrir").reshape(-1)[pl]
    pelo0 = (lab0[:, 0] < 45) & (y > Y_CABEZA)
    m[:] = False; m[pl] = pelo0
    # sin la cara registrada: las cejas, los ojos y la boca de Tripo son oscuros y estan en otro sitio
    pelo_zona = (abrir_cerrar(abrir_cerrar(m.reshape(h, w), 3, "abrir"), 5, "cerrar").reshape(-1)[pl]
                 & (y > Y_CABEZA) & ~cara_m.reshape(-1)[pl])

    # 2b) Boca y trazos finos de Tripo junto a la cara registrada: la boca de Tripo esta en otro sitio y
    #     al mezclarla en el costado de la cara sale una segunda boca. Se tapan con su piel vecina.
    m[:] = False; m[pl] = piel0
    piel_cerrada = abrir_cerrar(m.reshape(h, w), 5, "cerrar")
    zona_boca = np.zeros(h * w, bool)
    zona_boca[pl] = ((y > 0.17) & (y < 0.265) & (x > 0.10)) & ~piel0
    trazo = piel_cerrada & zona_boca.reshape(h, w) & ocupado
    tex0f, _ = rellenar_onion(tex0, ocupado & m.reshape(h, w), trazo)
    c0 = tex0f.reshape(-1, 3)[pl].astype(np.float32)
    lab0 = a_lab(c0).astype(np.float32)
    info["trazos_tripo_tapados"] = int(trazo.sum())

    # 3) Ajuste de color de Tripo hacia v5C por zona, medido en los texels buenos.
    forzado = np.maximum.reduce([f_izq, f_bolso, f_brazo, f_der])
    bueno = (visto.reshape(-1)[pl]) & (w_g >= 0.999) & (forzado <= 0) & ~(hueco.reshape(-1)[pl])
    print("Ajustando color por zonas...", flush=True)
    todos = np.ones(len(pl), bool)
    adj_lab, info_zonas = ajustar_zonas(lab0, lab5, y, bueno, todos)
    info["zonas"] = info_zonas

    # 4) Mechones de la hoja sobre piel junto a las orejas y linea oscura de la mandibula: en los
    #    costados de la cabeza, detras del ojo, donde Tripo dice piel y v5C es mucho mas oscuro.
    cab = smooth(Y_CABEZA, Y_CABEZA + 0.02, y) * (1 - smooth(0.33, 0.35, y))
    lateral = 1 - smooth(0.5, 0.65, nx)
    ojo = smooth(0.088, 0.098, x) * smooth(0.25, 0.26, y)
    delante = smooth(0.125, 0.135, x)
    oscuro = smooth(8, 20, adj_lab[:, 0] - lab5[:, 0])
    f_mechon = cab * lateral * (1 - ojo) * (1 - delante) * piel0_ab * oscuro
    reglas = {"izq": f_izq, "bolso": f_bolso, "brazo": f_brazo, "oreja_der": f_der, "mechon": f_mechon}
    for nombre in a.desactivar:
        reglas[nombre] = np.zeros_like(reglas[nombre])
    f_izq, f_bolso, f_brazo, f_der, f_mechon = (reglas[k] for k in ("izq", "bolso", "brazo", "oreja_der", "mechon"))
    info["reglas_desactivadas"] = list(a.desactivar)
    w5 = w_g * (1 - f_izq) * (1 - f_bolso) * (1 - f_brazo) * (1 - f_der) * (1 - f_mechon)
    if a.guardar_pesos:
        np.savez(a.guardar_pesos, w5=w5.astype(np.float16), w_g=w_g.astype(np.float16), f_izq=f_izq.astype(np.float16),
                 f_mechon=f_mechon.astype(np.float16))
    adj_rgb = de_lab(adj_lab).astype(np.float32)
    final = w5[:, None] * c5 + (1 - w5[:, None]) * adj_rgb
    info["pesos"] = {"g_menor_035_pct": float(100 * (g < G_BAJO).mean()),
                     "g_mezcla_pct": float(100 * ((g >= G_BAJO) & (g < G_ALTO)).mean()),
                     "costado_izq_cabeza_texels": int((f_izq > 0.5).sum()),
                     "zona_bolso_texels": int((f_bolso > 0.5).sum()), "brazo_derecho_texels": int((f_brazo > 0.5).sum()),
                     "mechones_texels": int((f_mechon > 0.5).sum()),
                     "oreja_patilla_derecha_texels": int((f_der > 0.5).sum()),
                     "v5c_puro_pct": float(100 * (w5 >= 0.999).mean()), "tripo_puro_pct": float(100 * (w5 <= 0.001).mean()),
                     "texels_buenos_para_estadistica": int(bueno.sum())}

    # 4b) Correa de la espalda: al quitar el bolso pintado en el gluteo, la correa terminaba en el cinturon.
    #     Se prolonga por la espalda hasta la esquina superior interior del bolso 3D (accesorio_bolso.py,
    #     angulo 45), con el color de la misma correa por encima del cinturon.
    final, info["correa_espalda"] = prolongar_correa(final, c5, ps, ns)

    # 5) Reflejos naranjas del pelo: -30 % de saturacion y brillo (HSV), con peso suave.
    labf = a_lab(final).astype(np.float32)
    crf, huef = lab_a_lch(labf)
    hw = (pelo_zona * smooth(28, 45, crf) * smooth(35, 50, labf[:, 0]) * smooth(25, 40, huef) * (1 - smooth(90, 105, huef))).astype(np.float32)
    sel = np.flatnonzero(hw > 0)
    hsv = rgb_a_hsv(final[sel])
    k = 1 - a.reduccion_brillos * hw[sel]
    hsv[:, 1] *= k
    hsv[:, 2] *= k
    final[sel] = hsv_a_rgb(hsv)
    info["brillos_pelo"] = {"texels": int(len(sel)), "texels_peso_completo": int((hw > 0.999).sum()),
                            "reduccion": a.reduccion_brillos}

    # 5b) Brillo cuadrado del ojo derecho.
    final, info["ojo"] = reparar_ojo(final, ps, ns, hueco_b.reshape(-1)[pl])
    print("Ojo:", json.dumps(info["ojo"]), flush=True)

    # 6) Textura, dilatacion de islas y relleno del resto.
    tex = np.zeros((h, w, 3), np.float32)
    tex.reshape(-1, 3)[pl] = final
    print("Dilatando islas...", flush=True)
    tex, conocido = rellenar_onion(tex, ocupado, np.ones_like(ocupado), pasos=a.dilatacion)
    resto = tirar_empujar(tex, conocido)
    tex = np.where(conocido[..., None], tex, resto)
    tex = np.clip(np.rint(tex), 0, 255).astype(np.uint8)
    info["dilatacion_px"] = a.dilatacion
    imagen = Image.fromarray(tex)
    imagen.save(a.diagnosticos / "textura.png")
    # mapas de diagnostico
    mapa = np.zeros((h * w, 3), np.uint8)
    mapa[pl, 0] = np.clip(255 * (1 - w5), 0, 255).astype(np.uint8)
    mapa[pl, 1] = np.clip(255 * w5, 0, 255).astype(np.uint8)
    mapa[pl, 2] = np.clip(255 * hw, 0, 255).astype(np.uint8)
    Image.fromarray(mapa.reshape(h, w, 3)).resize((1024, 1024), Image.BOX).save(a.diagnosticos / "pesos_v5c_verde_tripo_rojo_brillo_azul.png")
    Image.fromarray(hueco).resize((1024, 1024), Image.BOX).save(a.diagnosticos / "huecos_rellenados.png")
    buf = io.BytesIO()
    imagen.save(buf, format="PNG")
    doc0, bin0 = ph.leer_glb(a.tripo)
    _, _, _, _, _, imid0 = ph.geometria(doc0, bin0)
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    ph.guardar_glb(a.salida, json.loads(json.dumps(doc0)), bin0, buf.getvalue(), imid0)
    d2, b2 = ph.leer_glb(a.salida)
    assert b2[:len(bin0)] == bin0
    for clave in ("meshes", "nodes", "accessors", "materials", "textures", "scenes"):
        assert d2[clave] == doc0[clave], clave
    meta = {"v5c": str(a.v5c), "tripo": str(a.tripo), "salida": str(a.salida),
            "sha256_v5c": hashlib.sha256(a.v5c.read_bytes()).hexdigest(),
            "sha256_tripo": hashlib.sha256(a.tripo.read_bytes()).hexdigest(),
            "sha256_salida": hashlib.sha256(a.salida.read_bytes()).hexdigest(),
            "umbral_g": [G_BAJO, G_ALTO], "texels_superficie": int(len(pl)), **info,
            "segundos": round(time.monotonic() - t0, 1)}
    (a.diagnosticos / "limpieza.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("huecos", "pesos", "brillos_pelo", "segundos")}, indent=1), flush=True)


if __name__ == "__main__":
    main()
