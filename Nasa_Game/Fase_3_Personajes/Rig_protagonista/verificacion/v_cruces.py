"""Cruces entre piezas por paridad de rayos (verificador). Uso: python v_cruces.py <rig.glb> <salida.json>
Mide por clip y cuadro: vertices del bolso dentro del cuerpo, vertices de antebrazo y mano dentro del bolso,
vertices de antebrazo y mano dentro del resto del cuerpo (sin los brazos), fase de brazos y piernas, y
deslizamiento del pie de apoyo."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v_glb as g  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ruta, salida = sys.argv[1:3]
js, binario, _ = g.leer_glb(ruta)
nodos = js["nodes"]
pad = g.padres(js)
sk = js["skins"][0]
art = sk["joints"]
nomb = [nodos[j]["name"] for j in art]
ibm = g.accesor(js, binario, sk["inverseBindMatrices"]).astype(np.float64).reshape(-1, 4, 4).transpose(0, 2, 1)
loc0 = [g.trs(n) for n in nodos]
prims = {p["nombre"]: p for p in g.malla_mundo(js, binario)}
dat = {}
for n, p in prims.items():
    at = p["pr"]["attributes"]
    dat[n] = (p["pos_local"], g.accesor(js, binario, at["JOINTS_0"]).astype(np.int64),
              g.accesor(js, binario, at["WEIGHTS_0"]).astype(np.float64), p["idx"].astype(np.int64))


def piel(loc):
    cache = {}
    W_ = np.stack([g.mundo(js, loc, pad, j, cache) for j in art])
    G = W_ @ ibm
    out = {}
    for n, (pos, J, W, idx) in dat.items():
        v = np.concatenate([pos, np.ones((len(pos), 1))], axis=1)
        acc = np.zeros((len(v), 3))
        for k in range(4):
            acc += W[:, k:k + 1] * np.einsum("nij,nj->ni", G[J[:, k]][:, :3, :], v)
        out[n] = acc
    return out, {nomb[k]: W_[k][:3, 3] for k in range(len(art))}


def dentro(P, V, T, dirs):
    """Paridad de rayos de cada punto P contra la malla (V, T), mayoria entre varias direcciones."""
    votos = np.zeros(len(P), dtype=int)
    a, b, c = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    e1, e2 = b - a, c - a
    for d in dirs:
        d = np.asarray(d, dtype=np.float64)
        d /= np.linalg.norm(d)
        h = np.cross(d, e2)                      # (T,3)
        det = (e1 * h).sum(1)                    # (T,)
        ok = np.abs(det) > 1e-14
        inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
        cuenta = np.zeros(len(P), dtype=int)
        for i0 in range(0, len(P), 400):
            s = P[i0:i0 + 400, None, :] - a[None, :, :]          # (p,T,3)
            u = (s * h[None]).sum(-1) * inv[None]
            q = np.cross(s, e1[None])
            v = (q * d[None, None]).sum(-1) * inv[None]
            t = (q * e2[None]).sum(-1) * inv[None]
            hit = ok[None] & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-9)
            cuenta[i0:i0 + 400] = hit.sum(1)
        votos += (cuenta % 2)
    return votos * 2 > len(dirs)


DIRS = [(0.31, 0.89, 0.33), (-0.57, 0.21, 0.79), (0.12, -0.35, -0.93)]
posC, JC, WC, TC = dat["PER01_cuerpo"]
posB, JB, WB, TB = dat["PER01_bolso"]
ih = {n: i for i, n in enumerate(nomb)}


def peso_de(huesos):
    w = np.zeros(len(posC))
    for h in huesos:
        w += (WC * (JC == ih[h])).sum(1)
    return w


brazos = {l: peso_de(["hombro_" + l, "brazo_" + l, "antebrazo_" + l, "mano_" + l]) for l in ("izq", "der")}
mano_ante = {l: peso_de(["antebrazo_" + l, "mano_" + l]) > 0.6 for l in ("izq", "der")}
w_brazos = brazos["izq"] + brazos["der"]
tri_sin_brazos = TC[(w_brazos[TC] < 0.5).all(1)]
print("vertices antebrazo+mano", {l: int(m.sum()) for l, m in mano_ante.items()}, "tri sin brazos", len(tri_sin_brazos), "de", len(TC))

res = {}
for an in js["animations"]:
    canales = []
    tmax = 0.0
    for ch in an["channels"]:
        sm = an["samplers"][ch["sampler"]]
        t = g.accesor(js, binario, sm["input"]).astype(np.float64).ravel()
        v = g.accesor(js, binario, sm["output"]).astype(np.float64)
        canales.append((ch["target"]["node"], ch["target"]["path"], t, v))
        tmax = max(tmax, t[-1])

    def pose(t):
        loc = [m.copy() for m in loc0]
        porn = {}
        for nodo, camino, tt, vv in canales:
            porn.setdefault(nodo, {})[camino] = g.interp(tt, vv, t, camino == "rotation")
        for nodo, d in porn.items():
            n = nodos[nodo]
            loc[nodo] = g.compone(np.array(d.get("translation", n.get("translation", [0, 0, 0])), dtype=float),
                                  np.array(d.get("rotation", n.get("rotation", [0, 0, 0, 1])), dtype=float),
                                  np.array(d.get("scale", n.get("scale", [1, 1, 1])), dtype=float))
        return loc

    n_c = int(round(tmax * 50)) + 1
    ts = np.linspace(0, tmax, n_c)[::2]          # cada 0,04 s
    filas = []
    for t in ts:
        v, huesos = piel(pose(t))
        vc, vb = v["PER01_cuerpo"], v["PER01_bolso"]
        b_en_c = dentro(vb, vc, TC, DIRS)
        f = {"t": round(float(t), 3), "bolso_en_cuerpo": float(b_en_c.mean())}
        for l in ("izq", "der"):
            pts = vc[mano_ante[l]]
            f["brazo_%s_en_bolso" % l] = float(dentro(pts, vb, TB, DIRS).mean())
            f["brazo_%s_en_cuerpo" % l] = float(dentro(pts, vc, tri_sin_brazos, DIRS).mean())
            f["mano_%s" % l] = [round(float(x), 4) for x in huesos["mano_" + l]]
            f["pie_%s" % l] = [round(float(x), 4) for x in huesos["pie_" + l]]
        filas.append(f)
    r = {"cuadros": len(filas)}
    for k in ("bolso_en_cuerpo", "brazo_izq_en_bolso", "brazo_der_en_bolso", "brazo_izq_en_cuerpo", "brazo_der_en_cuerpo"):
        vals = [f[k] for f in filas]
        r[k] = {"max": round(max(vals), 4), "t_max": filas[int(np.argmax(vals))]["t"], "media": round(float(np.mean(vals)), 4)}
    # fase brazo/pierna: correlacion entre x de la mano y x del pie del mismo lado (debe ser negativa al andar)
    for l in ("izq", "der"):
        mx = np.array([f["mano_" + l][0] for f in filas])
        px = np.array([f["pie_" + l][0] for f in filas])
        if mx.std() > 1e-4 and px.std() > 1e-4:
            r["corr_mano_pie_" + l] = round(float(np.corrcoef(mx, px)[0, 1]), 3)
        r["rango_x_mano_" + l] = round(float(mx.max() - mx.min()), 4)
        r["rango_x_pie_" + l] = round(float(px.max() - px.min()), 4)
    r["filas"] = filas
    res[an["name"]] = r
    print(an["name"], {k: v for k, v in r.items() if k != "filas"})
Path(salida).write_text(json.dumps(res, indent=1), encoding="utf-8")
