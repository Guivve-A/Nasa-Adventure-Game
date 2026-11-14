"""Verificacion de la geometria de v5C contra la malla original de Tripo (solo lectura)."""
import json, struct, sys
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
BASE = "C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_1_Arte/Modelado/Lote_04/"


def leer(f):
    d = open(BASE + f, "rb").read()
    pos, js, b = 12, None, b""
    while pos < len(d):
        n, t = struct.unpack_from("<II", d, pos)
        c = d[pos + 8:pos + 8 + n]
        if t == 0x4E4F534A:
            js = json.loads(c)
        else:
            b = c
        pos += 8 + n
    tipos = {5121: np.uint8, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
    ncomp = {"SCALAR": 1, "VEC2": 2, "VEC3": 3}

    def acc(i):
        a = js["accessors"][i]
        v = js["bufferViews"][a["bufferView"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        dt = tipos[a["componentType"]]
        k = ncomp[a["type"]]
        arr = np.frombuffer(b, dt, a["count"] * k, off)
        return arr.reshape(-1, k) if k > 1 else arr

    p = js["meshes"][0]["primitives"][0]
    return (acc(p["attributes"]["POSITION"]).astype(float), acc(p["indices"]).reshape(-1, 3).astype(int),
            acc(p["attributes"]["NORMAL"]).astype(float), acc(p["attributes"]["TEXCOORD_0"]).astype(float))


def caras(P, F):
    a, b, c = P[F[:, 0]], P[F[:, 1]], P[F[:, 2]]
    n = np.cross(b - a, c - a)
    area = np.linalg.norm(n, axis=1) / 2
    return n, area


def main():
    P0, F0, N0, U0 = leer("L04_PER01_giro_tripo_mv.glb")
    P1, F1, N1, U1 = leer("L04_PER01_v5C.glb")
    print(f"vertices {len(P0)} / {len(P1)}, triangulos {len(F0)} / {len(F1)}")
    print("indices identicos:", np.array_equal(F0, F1), " UV identicas:", np.allclose(U0, U1))
    d = np.linalg.norm(P1 - P0, axis=1)
    print(f"desplazamiento (malla de 1 m): max {d.max()*1000:.1f} mm, medio {d.mean()*1000:.1f} mm, "
          f"p95 {np.percentile(d,95)*1000:.1f} mm, mediana {np.median(d)*1000:.1f} mm")
    i = d.argmax()
    print(f"  vertice de max desplazamiento {i}: orig {P0[i].round(3)} -> {P1[i].round(3)}")
    n0, a0 = caras(P0, F0)
    n1, a1 = caras(P1, F1)
    eps = 1e-10
    print(f"caras degeneradas (area < 1e-10 m2): orig {(a0<eps).sum()}, v5C {(a1<eps).sum()}")
    print(f"caras con area < 1e-8: orig {(a0<1e-8).sum()}, v5C {(a1<1e-8).sum()}")
    ok = (a0 > eps) & (a1 > eps)
    cosang = (n0[ok] * n1[ok]).sum(1) / (np.linalg.norm(n0[ok], axis=1) * np.linalg.norm(n1[ok], axis=1))
    inv = (cosang < 0).sum()
    print(f"caras invertidas (normal con signo opuesto): {inv} de {ok.sum()}")
    print(f"caras que giran >60 grados: {(cosang < 0.5).sum()}, >90: {inv}")
    idx_inv = np.where(ok)[0][cosang < 0]
    if len(idx_inv):
        cen = P1[F1[idx_inv]].mean(1)
        print("  centros de caras invertidas (y en m):", np.round(np.sort(cen[:, 1]), 3)[:30].tolist())
        print("  area relativa de las invertidas:", (a1[idx_inv] / np.median(a1)).round(2)[:30].tolist())
    # razon de area
    r = a1[ok] / a0[ok]
    print(f"razon de area cara v5C/orig: p1 {np.percentile(r,1):.2f} p50 {np.median(r):.2f} p99 {np.percentile(r,99):.2f} max {r.max():.1f} min {r.min():.3f}")
    # aristas
    def aristas(P, F):
        e = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
        return np.linalg.norm(P[e[:, 0]] - P[e[:, 1]], axis=1)
    e0, e1 = aristas(P0, F0), aristas(P1, F1)
    re = e1 / np.maximum(e0, 1e-9)
    print(f"razon de largo de arista: p1 {np.percentile(re,1):.2f} p99 {np.percentile(re,99):.2f} max {re.max():.1f}")
    # picos: desplazamiento del vertice respecto del promedio de sus vecinos (laplaciano), comparado con orig
    vec = [set() for _ in range(len(P0))]
    for a, b, c in F0:
        vec[a].update((b, c)); vec[b].update((a, c)); vec[c].update((a, b))
    def lap(P):
        return np.array([np.linalg.norm(P[k] - P[list(v)].mean(0)) if v else 0 for k, v in enumerate(vec)])
    l0, l1 = lap(P0), lap(P1)
    print(f"laplaciano (mm): orig p99 {np.percentile(l0,99)*1000:.2f} max {l0.max()*1000:.2f}; "
          f"v5C p99 {np.percentile(l1,99)*1000:.2f} max {l1.max()*1000:.2f}")
    dl = l1 - l0
    top = np.argsort(dl)[-8:][::-1]
    print("  vertices con mas aumento de laplaciano (mm, y):",
          [(int(k), round(dl[k]*1000, 2), round(P1[k, 1], 3)) for k in top])
    print(f"  vertices con laplaciano > 3x el max original: {(l1 > 3*l0.max()).sum()}")
    # normales del archivo vs geometria
    vn = np.zeros_like(P1)
    for j in range(3):
        np.add.at(vn, F1[:, j], n1)
    vn /= np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-12)
    cn = (vn * N1).sum(1)
    print(f"normales del archivo vs recalculadas: mediana cos {np.median(cn):.3f}, cos<0: {(cn<0).sum()}, cos<0.5: {(cn<0.5).sum()}")
    print("normales del archivo identicas a las originales:", np.allclose(N0, N1, atol=1e-4))
    print(f"bbox orig {P0.min(0).round(3)} {P0.max(0).round(3)}; v5C {P1.min(0).round(3)} {P1.max(0).round(3)}")


main()


def extra():
    # consistencia de normales en la original y ubicacion de las caras que giran >60 grados
    P0, F0, N0, _ = leer("L04_PER01_giro_tripo_mv.glb")
    P1, F1, N1, _ = leer("L04_PER01_v5C.glb")
    for nom, P, F, N in (("orig", P0, F0, N0), ("v5C", P1, F1, N1)):
        n, _ = caras(P, F)
        vn = np.zeros_like(P)
        for j in range(3):
            np.add.at(vn, F[:, j], n)
        vn /= np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-12)
        cn = (vn * N).sum(1)
        print(f"{nom}: normales archivo vs recalculadas cos<0: {(cn<0).sum()}, cos<0.5: {(cn<0.5).sum()}")
    n0, _ = caras(P0, F0); n1, _ = caras(P1, F1)
    c = (n0 * n1).sum(1) / (np.linalg.norm(n0, axis=1) * np.linalg.norm(n1, axis=1))
    k = np.where(c < 0.5)[0]
    cen = P1[F1[k]].mean(1)
    print("caras >60 grados: centros (x,y,z):", np.round(cen, 3).tolist())


extra()
