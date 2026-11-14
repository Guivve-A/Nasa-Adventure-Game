"""Compara la geometria de v5A con la original de Tripo (giro_tripo_mv) y con v4D_geometria."""
import json
import struct
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
BASE = Path(r"C:\Users\guill\Desktop\Juego 2d-hd\Nasa_Game\Fase_1_Arte\Modelado\Lote_04")
TIPOS = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
NCOMP = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}


def leer(ruta):
    d = ruta.read_bytes()
    _, _, largo = struct.unpack_from("<III", d, 0)
    pos, js, b = 12, None, b""
    while pos < largo:
        n, t = struct.unpack_from("<II", d, pos)
        tr = d[pos + 8:pos + 8 + n]
        if t == 0x4E4F534A:
            js = json.loads(tr)
        else:
            b = tr
        pos += 8 + n

    def acc(i):
        a = js["accessors"][i]
        v = js["bufferViews"][a["bufferView"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        nc = NCOMP[a["type"]]
        dt = np.dtype(TIPOS[a["componentType"]])
        stride = v.get("byteStride", 0) or dt.itemsize * nc
        raw = np.frombuffer(b, dtype=np.uint8, count=stride * (a["count"] - 1) + dt.itemsize * nc, offset=off)
        out = np.lib.stride_tricks.as_strided(raw, shape=(a["count"], dt.itemsize * nc), strides=(stride, 1))
        return np.frombuffer(out.copy().tobytes(), dtype=dt).reshape(a["count"], nc)

    p = js["meshes"][0]["primitives"][0]
    pos_ = acc(p["attributes"]["POSITION"]).astype(np.float64)
    idx = acc(p["indices"]).reshape(-1, 3).astype(np.int64)
    uv = acc(p["attributes"]["TEXCOORD_0"]) if "TEXCOORD_0" in p["attributes"] else None
    # aplicar transform de nodo si hay
    nodos = [n for n in js["nodes"] if "mesh" in n]
    info = {k: nodos[0].get(k) for k in ("matrix", "scale", "rotation", "translation") if k in nodos[0]}
    return pos_, idx, uv, info


def normales(v, f):
    a, b, c = v[f[:, 0]], v[f[:, 1]], v[f[:, 2]]
    n = np.cross(b - a, c - a)
    area = np.linalg.norm(n, axis=1) / 2
    return n, area


def informe(nombre, v, f, v0, f0):
    print(f"--- {nombre} contra original")
    print(f"vertices {len(v)} vs {len(v0)}; triangulos {len(f)} vs {len(f0)}; indices iguales: {np.array_equal(f, f0)}")
    alto0 = v0[:, 1].max() - v0[:, 1].min()
    print(f"caja original min {v0.min(0).round(4)} max {v0.max(0).round(4)} alto {alto0:.4f}")
    print(f"caja nueva    min {v.min(0).round(4)} max {v.max(0).round(4)} alto {v[:,1].max()-v[:,1].min():.4f}")
    dv = np.linalg.norm(v - v0, axis=1)
    print(f"desplazamiento: max {dv.max():.4f} m ({100*dv.max()/alto0:.1f} % del alto), medio {dv.mean():.4f}, "
          f"p95 {np.percentile(dv,95):.4f}, p99 {np.percentile(dv,99):.4f}")
    imax = dv.argmax()
    print(f"  vertice de max desplazamiento {imax}: original {v0[imax].round(4)} -> {v[imax].round(4)}")
    n, area = normales(v, f)
    n0, area0 = normales(v0, f0)
    print(f"area total {area.sum():.4f} vs {area0.sum():.4f}")
    deg = area < 1e-9
    deg0 = area0 < 1e-9
    print(f"caras degeneradas (area<1e-9): {deg.sum()} (original {deg0.sum()}); nuevas degeneradas {(deg & ~deg0).sum()}")
    ok = (area > 1e-12) & (area0 > 1e-12)
    cosang = np.einsum("ij,ij->i", n[ok], n0[ok]) / (np.linalg.norm(n[ok], axis=1) * np.linalg.norm(n0[ok], axis=1))
    inv = cosang < 0
    print(f"caras invertidas (normal con signo opuesto a la original): {inv.sum()} ({100*inv.mean():.2f} %)")
    print(f"caras que giran mas de 60 grados: {(cosang < 0.5).sum()}; mas de 90: {inv.sum()}")
    ratio = area[ok] / np.maximum(area0[ok], 1e-15)
    print(f"cambio de area por cara: p1 {np.percentile(ratio,1):.3f} mediana {np.median(ratio):.3f} p99 {np.percentile(ratio,99):.3f} max {ratio.max():.2f}")
    print(f"caras estiradas x5 o mas: {(ratio > 5).sum()}; encogidas a <0.1: {(ratio < 0.1).sum()}")
    # picos: vertice que se aleja de la media de sus vecinos mucho mas que en la original
    E = np.vstack([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
    E = np.vstack([E, E[:, ::-1]])
    nv = len(v)
    cnt = np.bincount(E[:, 0], minlength=nv).astype(float)
    def lap(P):
        s = np.zeros_like(P)
        np.add.at(s, E[:, 0], P[E[:, 1]])
        return np.linalg.norm(P - s / np.maximum(cnt, 1)[:, None], axis=1)
    L, L0 = lap(v), lap(v0)
    pico = L - L0
    print(f"laplaciano (salida respecto a vecinos): max nuevo {L.max():.4f} vs original {L0.max():.4f}; "
          f"aumento max {pico.max():.4f} m; vertices con aumento > 1 cm: {(pico > 0.01).sum()}, > 5 mm: {(pico > 0.005).sum()}")
    top = np.argsort(-pico)[:5]
    for i in top:
        print(f"  pico v{i} pos {v[i].round(3)} lap {L[i]:.4f} (orig {L0[i]:.4f}) desplazado {dv[i]:.4f}")
    # longitud de aristas
    le = np.linalg.norm(v[E[:, 0]] - v[E[:, 1]], axis=1)
    le0 = np.linalg.norm(v0[E[:, 0]] - v0[E[:, 1]], axis=1)
    r = le / np.maximum(le0, 1e-12)
    print(f"cambio de longitud de aristas: p1 {np.percentile(r,1):.3f} p99 {np.percentile(r,99):.3f} max {r.max():.2f}")
    # zonas: desplazamiento medio por banda de altura
    y = (v0[:, 1] - v0[:, 1].min()) / alto0
    for a, b in [(0, .1), (.1, .3), (.3, .5), (.5, .7), (.7, .85), (.85, 1.01)]:
        m = (y >= a) & (y < b)
        print(f"  banda alto {a:.2f}-{b:.2f}: n {m.sum()}, desplazamiento medio {dv[m].mean():.4f}, max {dv[m].max():.4f}")


v0, f0, uv0, i0 = leer(BASE / "L04_PER01_giro_tripo_mv.glb")
vD, fD, uvD, iD = leer(BASE / "L04_PER01_v4D_geometria.glb")
vA, fA, uvA, iA = leer(BASE / "L04_PER01_v5A.glb")
print("transform de nodo:", i0, iD, iA)
print("UV iguales v5A vs original:", None if uvA is None else (uvA.shape == uv0.shape and np.allclose(uvA, uv0)))
print("posiciones v5A iguales a v4D_geometria:", vA.shape == vD.shape and np.allclose(vA, vD, atol=1e-6),
      "max dif", np.abs(vA - vD).max() if vA.shape == vD.shape else "n/a")
informe("v5A", vA, fA, v0, f0)
