"""Verificador independiente del GLB con esqueleto: lee el archivo con struct y numpy, sin Blender.

Uso: python -I v_glb.py <rig.glb> <original.glb> <salida.json>
Mide: estructura, piel, pesos, clips, canales, caja en reposo, orientacion, estiramiento de aristas por clip
(skinning lineal propio), altura del vertice mas bajo, cierre de ciclos y texturas.
"""
import io
import json
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
TIPOS = {5120: ("b", 1), 5121: ("B", 1), 5122: ("h", 2), 5123: ("H", 2), 5125: ("I", 4), 5126: ("f", 4)}
NCOMP = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


def leer_glb(ruta):
    d = Path(ruta).read_bytes()
    magia, version, largo = struct.unpack_from("<4sII", d, 0)
    assert magia == b"glTF" and version == 2, (magia, version)
    assert largo == len(d), (largo, len(d))
    pos, js, binario = 12, None, None
    while pos < len(d):
        n, tipo = struct.unpack_from("<I4s", d, pos)
        cuerpo = d[pos + 8:pos + 8 + n]
        if tipo == b"JSON":
            js = json.loads(cuerpo)
        elif tipo == b"BIN\x00":
            binario = cuerpo
        pos += 8 + n
    return js, binario, len(d)


def accesor(js, binario, i):
    a = js["accessors"][i]
    bv = js["bufferViews"][a["bufferView"]]
    letra, tam = TIPOS[a["componentType"]]
    nc = NCOMP[a["type"]]
    ini = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    paso = bv.get("byteStride", 0)
    dt = np.dtype("<" + letra)
    if paso and paso != tam * nc:
        fila = np.frombuffer(binario, dtype=np.uint8, count=paso * (a["count"] - 1) + tam * nc, offset=ini)
        idx = (np.arange(a["count"])[:, None] * paso + np.arange(tam * nc)[None, :])
        arr = np.frombuffer(fila[idx].tobytes(), dtype=dt).reshape(a["count"], nc)
    else:
        arr = np.frombuffer(binario, dtype=dt, count=a["count"] * nc, offset=ini).reshape(a["count"], nc)
    if a.get("normalized"):
        arr = arr.astype(np.float64) / {5121: 255.0, 5123: 65535.0}[a["componentType"]]
    return arr


def trs(nodo):
    if "matrix" in nodo:
        return np.array(nodo["matrix"], dtype=np.float64).reshape(4, 4).T
    t = np.array(nodo.get("translation", [0, 0, 0]), dtype=np.float64)
    q = np.array(nodo.get("rotation", [0, 0, 0, 1]), dtype=np.float64)
    s = np.array(nodo.get("scale", [1, 1, 1]), dtype=np.float64)
    return compone(t, q, s)


def rot(q):
    x, y, z, w = q / np.linalg.norm(q)
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def compone(t, q, s):
    m = np.eye(4)
    m[:3, :3] = rot(q) * s[None, :]
    m[:3, 3] = t
    return m


def padres(js):
    p = {}
    for i, n in enumerate(js["nodes"]):
        for h in n.get("children", []):
            p[h] = i
    return p


def mundo(js, locales, pad, i, cache):
    if i in cache:
        return cache[i]
    m = locales[i]
    if i in pad:
        m = mundo(js, locales, pad, pad[i], cache) @ m
    cache[i] = m
    return m


def malla_mundo(js, binario):
    """Lista de primitivas en espacio de mundo SIN piel (para el original): posiciones e indices."""
    pad = padres(js)
    locales = [trs(n) for n in js["nodes"]]
    prims = []
    for i, n in enumerate(js["nodes"]):
        if "mesh" not in n:
            continue
        m = mundo(js, locales, pad, i, {})
        for pr in js["meshes"][n["mesh"]]["primitives"]:
            pos = accesor(js, binario, pr["attributes"]["POSITION"]).astype(np.float64)
            idx = accesor(js, binario, pr["indices"]).reshape(-1, 3) if "indices" in pr else np.arange(len(pos)).reshape(-1, 3)
            prims.append({"nodo": i, "nombre": n.get("name"), "pos_local": pos, "idx": idx, "M": m, "pr": pr,
                          "skin": n.get("skin")})
    return prims


def interp(tiempos, valores, t, es_rot):
    if t <= tiempos[0]:
        return valores[0]
    if t >= tiempos[-1]:
        return valores[-1]
    k = np.searchsorted(tiempos, t) - 1
    f = (t - tiempos[k]) / (tiempos[k + 1] - tiempos[k])
    a, b = valores[k], valores[k + 1]
    if es_rot:
        if np.dot(a, b) < 0:
            b = -b
        q = a * (1 - f) + b * f
        return q / np.linalg.norm(q)
    return a * (1 - f) + b * f


def imagenes(js, binario):
    out = []
    for im in js.get("images", []):
        bv = js["bufferViews"][im["bufferView"]]
        datos = binario[bv.get("byteOffset", 0):bv.get("byteOffset", 0) + bv["byteLength"]]
        w, h = Image.open(io.BytesIO(datos)).size
        out.append({"nombre": im.get("name"), "mime": im.get("mimeType"), "bytes": len(datos), "ancho": w, "alto": h})
    return out


def main():
    ruta, ruta_orig, salida = sys.argv[1:4]
    js, binario, tam = leer_glb(ruta)
    jo, bo, tam_o = leer_glb(ruta_orig)
    r = {"archivo": ruta, "bytes": tam, "bytes_original": tam_o}
    r["extensiones_requeridas"] = js.get("extensionsRequired", [])
    r["imagenes"] = imagenes(js, binario)
    r["imagenes_original"] = imagenes(jo, bo)

    # original en mundo
    po = malla_mundo(jo, bo)
    vo = np.concatenate([(p["M"][:3, :3] @ p["pos_local"].T).T + p["M"][:3, 3] for p in po])
    r["original"] = {"triangulos": int(sum(len(p["idx"]) for p in po)), "vertices": int(len(vo)),
                     "caja_min": vo.min(0).round(5).tolist(), "caja_max": vo.max(0).round(5).tolist(),
                     "primitivas": [(p["nombre"], len(p["pos_local"]), len(p["idx"])) for p in po]}

    # rig
    pad = padres(js)
    nodos = js["nodes"]
    r["skins"] = len(js.get("skins", []))
    sk = js["skins"][0]
    art = sk["joints"]
    r["huesos"] = len(art)
    r["nombres_huesos"] = [nodos[j].get("name") for j in art]
    r["padre_de_hueso"] = {nodos[j].get("name"): (nodos[pad[j]].get("name") if j in pad else None) for j in art}
    ibm = accesor(js, binario, sk["inverseBindMatrices"]).astype(np.float64).reshape(-1, 4, 4).transpose(0, 2, 1)
    locales0 = [trs(n) for n in nodos]
    escalas = [n.get("scale") for n in nodos if "scale" in n]
    r["nodos_con_escala"] = escalas

    prims = malla_mundo(js, binario)
    r["primitivas"] = [(p["nombre"], len(p["pos_local"]), len(p["idx"]), p["skin"]) for p in prims]
    r["triangulos"] = int(sum(len(p["idx"]) for p in prims))
    datos = []
    sumas, maxinf, fuera = [], 0, 0
    for p in prims:
        at = p["pr"]["attributes"]
        if "JOINTS_0" not in at:
            r.setdefault("primitivas_sin_piel", []).append(p["nombre"])
            continue
        J = accesor(js, binario, at["JOINTS_0"]).astype(np.int64)
        W = accesor(js, binario, at["WEIGHTS_0"]).astype(np.float64)
        r["hay_JOINTS_1"] = r.get("hay_JOINTS_1", False) or ("JOINTS_1" in at)
        sumas.append(W.sum(1))
        maxinf = max(maxinf, int((W > 0).sum(1).max()))
        fuera += int((J[W > 0] >= len(art)).sum())
        datos.append((p, J, W))
    s = np.concatenate(sumas)
    r["pesos"] = {"suma_min": float(s.min()), "suma_max": float(s.max()), "max_influencias": maxinf,
                  "indices_fuera_de_rango": fuera, "negativos": int(sum((d[2] < 0).sum() for d in datos))}

    def piel(locales):
        cache = {}
        G = np.stack([mundo(js, locales, pad, j, cache) for j in art]) @ ibm
        vs = []
        for p, J, W in datos:
            v = np.concatenate([p["pos_local"], np.ones((len(p["pos_local"]), 1))], axis=1)
            acc = np.zeros((len(v), 3))
            for k in range(4):
                M = G[J[:, k]]
                acc += W[:, k:k + 1] * np.einsum("nij,nj->ni", M[:, :3, :], v)
            vs.append(acc)
        return vs

    reposo = piel(locales0)
    todo0 = np.concatenate(reposo)
    r["reposo"] = {"caja_min": todo0.min(0).round(5).tolist(), "caja_max": todo0.max(0).round(5).tolist(),
                   "vertices": int(len(todo0))}
    # comparacion con el original: distancia de cada vertice del rig al mas cercano del original (muestra)
    if len(todo0) == len(vo):
        r["reposo"]["dif_max_mismo_orden"] = float(np.abs(todo0 - vo).max())
    from_scipy = None
    try:
        from scipy.spatial import cKDTree
        d1, _ = cKDTree(vo).query(todo0)
        d2, _ = cKDTree(todo0).query(vo)
        r["reposo"]["dist_max_al_original"] = float(max(d1.max(), d2.max()))
        from_scipy = True
    except Exception as e:  # sin scipy: fuerza bruta por bloques
        dm = 0.0
        for a in range(0, len(todo0), 2000):
            dm = max(dm, float(np.sqrt(((todo0[a:a + 2000, None, :] - vo[None, :, :]) ** 2).sum(-1)).min(1).max()))
        for a in range(0, len(vo), 2000):
            dm = max(dm, float(np.sqrt(((vo[a:a + 2000, None, :] - todo0[None, :, :]) ** 2).sum(-1)).min(1).max()))
        r["reposo"]["dist_max_al_original"] = dm

    # orientacion: la cara mira a +X. Indicador geometrico: en la franja de la cabeza (y > 0.19) el pelo queda detras,
    # asi que el centroide de los pies (y < -0.44) esta adelantado respecto al tobillo -> punta del pie hacia +X.
    pies = todo0[todo0[:, 1] < -0.46]
    tob = todo0[(todo0[:, 1] > -0.42) & (todo0[:, 1] < -0.36)]
    r["reposo"]["pies_x_medio"] = float(pies[:, 0].mean())
    r["reposo"]["tobillos_x_medio"] = float(tob[:, 0].mean())
    pies_o = vo[vo[:, 1] < -0.46]
    tob_o = vo[(vo[:, 1] > -0.42) & (vo[:, 1] < -0.36)]
    r["original"]["pies_x_medio"] = float(pies_o[:, 0].mean())
    r["original"]["tobillos_x_medio"] = float(tob_o[:, 0].mean())

    # aristas
    aristas = []
    base = 0
    for (p, J, W), v in zip(datos, reposo):
        t = p["idx"].astype(np.int64) + base
        aristas.append(np.concatenate([t[:, [0, 1]], t[:, [1, 2]], t[:, [2, 0]]]))
        base += len(v)
    aristas = np.unique(np.sort(np.concatenate(aristas), axis=1), axis=0)
    l0 = np.linalg.norm(todo0[aristas[:, 0]] - todo0[aristas[:, 1]], axis=1)
    valida = l0 > 1e-5
    aristas, l0 = aristas[valida], l0[valida]
    r["aristas"] = int(len(aristas))

    # animaciones
    clips = {}
    idx_art = {j: k for k, j in enumerate(art)}
    for an in js.get("animations", []):
        canales = []
        tmax, tmin = 0.0, 1e9
        rutas = {}
        interps = set()
        ajenos = []
        for ch in an["channels"]:
            sm = an["samplers"][ch["sampler"]]
            t = accesor(js, binario, sm["input"]).astype(np.float64).ravel()
            v = accesor(js, binario, sm["output"]).astype(np.float64)
            interps.add(sm.get("interpolation", "LINEAR"))
            nodo, camino = ch["target"]["node"], ch["target"]["path"]
            canales.append((nodo, camino, t, v))
            rutas[camino] = rutas.get(camino, 0) + 1
            tmax, tmin = max(tmax, t[-1]), min(tmin, t[0])
            if nodo not in idx_art:
                ajenos.append(nodos[nodo].get("name"))
        nombre = an.get("name")
        info = {"canales": rutas, "t_inicio": tmin, "duracion": tmax, "interpolaciones": sorted(interps),
                "canales_fuera_del_esqueleto": ajenos,
                "claves_max": int(max(len(c[2]) for c in canales))}
        tras = sorted({nodos[c[0]].get("name") for c in canales if c[1] == "translation"})
        info["huesos_con_traslacion"] = tras
        # traslacion: que ejes cambian
        for c in canales:
            if c[1] == "translation":
                info.setdefault("traslacion_rango", {})[nodos[c[0]].get("name")] = (c[3].max(0) - c[3].min(0)).round(6).tolist()
            if c[1] == "rotation":
                nq = np.linalg.norm(c[3], axis=1)
                info["quat_norma_min"] = min(info.get("quat_norma_min", 9), float(nq.min()))
                info["quat_norma_max"] = max(info.get("quat_norma_max", 0), float(nq.max()))

        def pose(t):
            loc = [m.copy() for m in locales0]
            porn = {}
            for nodo, camino, tt, vv in canales:
                porn.setdefault(nodo, {})[camino] = interp(tt, vv, t, camino == "rotation")
            for nodo, d in porn.items():
                n = nodos[nodo]
                T = np.array(d.get("translation", n.get("translation", [0, 0, 0])), dtype=np.float64)
                Q = np.array(d.get("rotation", n.get("rotation", [0, 0, 0, 1])), dtype=np.float64)
                S = np.array(d.get("scale", n.get("scale", [1, 1, 1])), dtype=np.float64)
                loc[nodo] = compone(T, Q, S)
            return loc

        n_cuadros = int(round(tmax * 50)) + 1
        ts = np.linspace(0.0, tmax, n_cuadros)
        ymin, p995, pmax, frac22 = [], [], [], []
        v_ini = v_fin = None
        for k, t in enumerate(ts):
            v = np.concatenate(piel(pose(t)))
            if k == 0:
                v_ini = v
            v_fin = v
            l = np.linalg.norm(v[aristas[:, 0]] - v[aristas[:, 1]], axis=1) / l0
            ymin.append(float(v[:, 1].min()))
            p995.append(float(np.percentile(l, 99.5)))
            pmax.append(float(l.max()))
            frac22.append(float((l < 2.2).mean()))
        info["cuadros"] = n_cuadros
        info["y_min_rango"] = [min(ymin), max(ymin)]
        info["estiramiento_p995_peor"] = max(p995)
        info["estiramiento_p995_t"] = float(ts[int(np.argmax(p995))])
        info["estiramiento_max"] = max(pmax)
        info["estiramiento_max_t"] = float(ts[int(np.argmax(pmax))])
        info["frac_aristas_bajo_2_2_peor"] = min(frac22)
        info["cierre_vertices_max_m"] = float(np.abs(v_ini - v_fin).max())
        # cierre por canal
        cq = 0.0
        ct = 0.0
        for nodo, camino, tt, vv in canales:
            if camino == "rotation":
                d = abs(float(np.dot(vv[0] / np.linalg.norm(vv[0]), vv[-1] / np.linalg.norm(vv[-1]))))
                cq = max(cq, float(np.degrees(2 * np.arccos(min(1.0, d)))))
            else:
                ct = max(ct, float(np.abs(vv[0] - vv[-1]).max()))
        info["cierre_giro_max_grados"] = cq
        info["cierre_traslacion_max_m"] = ct
        # reposo del clip en t=0 frente a la pose de union
        info["t0_frente_a_union_max_m"] = float(np.abs(v_ini - todo0).max())
        clips[nombre] = info
    r["clips"] = clips
    r["orden_clips"] = [a.get("name") for a in js.get("animations", [])]
    Path(salida).write_text(json.dumps(r, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(r, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
