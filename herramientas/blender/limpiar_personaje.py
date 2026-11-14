"""Limpia un personaje estatico y exporta LOD independientes, en metros.

Uso (PowerShell, desde esta carpeta):
    & 'C:/ruta/blender.exe' -b --factory-startup --python ./limpiar_personaje.py -- `
        --entrada 'C:/ruta/PER-01.glb' --salida './salidas/PER-01' `
        --objetivos 1500,3000,6000 --umbral-soldar 0.0005 --altura 1.7

Escrito para bpy 5.2. SIN PROBAR EN BLENDER: no esta instalado en este equipo.
La consulta de docs.blender.org/api/5.2/ no pudo completarse.
Cada objetivo es un limite superior del personaje completo, no de cada objeto.
Los nombres son <salida>_<objetivo>.glb. No sobrescribe archivos existentes.
Las salidas deben estar dentro de la carpeta que contiene este script.
Conserva el frente importado sin asumir +X/-X; no aplica otra conversion de ejes.
--altura mide la caja conjunta sobre Z, tras la conversion glTF del importador.
Solo admite mallas estaticas: rechaza rigs, animaciones, shape keys y modificadores.
Decimate conserva datos UV, pero puede deformar el dibujo y las siluetas.
La soldadura puede unir superficies cercanas. Las normales de superficies abiertas
no tienen un exterior inequivoco; se avisa de bordes abiertos/no manifold.
Los objetivos inferiores al minimo alcanzable fallan con un mensaje claro.
Para salida no cero aun en errores internos de Blender se puede agregar
--python-exit-code 1 antes de --python en el comando de lanzamiento.
"""

import argparse
import json
import math
from pathlib import Path
import struct
import sys
import tempfile
import traceback

import bpy
import bmesh
from mathutils import Matrix


def positivo(texto):
    valor = float(texto)
    if not math.isfinite(valor) or valor <= 0:
        raise argparse.ArgumentTypeError("Debe ser un numero finito mayor que cero.")
    return valor


def objetivos(texto):
    try:
        valores = [int(v.strip()) for v in texto.split(",")]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use enteros separados por comas.") from exc
    if not valores or any(v <= 0 for v in valores) or len(set(valores)) != len(valores):
        raise argparse.ArgumentTypeError("Los objetivos deben ser positivos y distintos.")
    return valores


def argumentos():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--entrada", required=True, type=Path)
    parser.add_argument("--salida", required=True, type=Path, help="Prefijo sin extension; dentro de esta carpeta.")
    parser.add_argument("--objetivos", type=objetivos, default=objetivos("1500,3000,6000"))
    parser.add_argument("--umbral-soldar", type=positivo, default=0.0005, help="Distancia en metros, despues de --altura.")
    parser.add_argument("--altura", type=positivo, help="Altura conjunta en metros sobre Z.")
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])


def exigir(condicion, mensaje):
    if not condicion:
        raise RuntimeError(mensaje)


def seleccionar(objetos):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objetos:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objetos[0]


def triangulos(malla):
    malla.calc_loop_triangles()
    return len(malla.loop_triangles)


def caja(objetos):
    minimo = [float("inf")] * 3
    maximo = [float("-inf")] * 3
    for obj in objetos:
        for vertice in obj.data.vertices:
            punto = obj.matrix_world @ vertice.co
            exigir(all(math.isfinite(v) for v in punto), f"Coordenada no finita en {obj.name}.")
            for eje in range(3):
                minimo[eje] = min(minimo[eje], punto[eje])
                maximo[eje] = max(maximo[eje], punto[eje])
    exigir(all(math.isfinite(v) for v in minimo + maximo), "La caja esta vacia.")
    return {"min_m": minimo, "max_m": maximo,
            "tamano_m": [maximo[i] - minimo[i] for i in range(3)]}


def limpiar(malla, umbral):
    capas_uv = tuple(c.name for c in malla.uv_layers)
    bm = bmesh.new()
    try:
        bm.from_mesh(malla)
        antes = len(bm.verts)
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=umbral)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        abiertos = sum(e.is_boundary for e in bm.edges)
        no_manifold = sum(not e.is_manifold for e in bm.edges)
        soldados = antes - len(bm.verts)
        bm.to_mesh(malla)
    finally:
        bm.free()
    malla.update()
    exigir(tuple(c.name for c in malla.uv_layers) == capas_uv, "La limpieza altero las capas UV.")
    for poligono in malla.polygons:
        poligono.use_smooth = False
    exigir(triangulos(malla) > 0, f"La limpieza dejo vacia la malla {malla.name}.")
    return soldados, abiertos, no_manifold


def opciones_operador(operador, opciones):
    # No omitir silenciosamente opciones que controlan el resultado.
    disponibles = operador.get_rna_type().properties.keys()
    exigir(all(k in disponibles for k in opciones),
           "La API glTF instalada no ofrece las opciones requeridas: "
           + ", ".join(k for k in opciones if k not in disponibles))
    return opciones


def crear_nivel(base, objetivo):
    copias = []
    modificadores = []
    original = sum(triangulos(o.data) for o in base)
    try:
        for fuente in base:
            obj = fuente.copy()
            obj.data = fuente.data.copy()
            obj.name = f"{fuente.name}_LOD_{objetivo}"
            bpy.context.scene.collection.objects.link(obj)
            copias.append(obj)
            if original > objetivo:
                mod = obj.modifiers.new(name="LOD_Collapse", type="DECIMATE")
                mod.decimate_type = "COLLAPSE"
                mod.use_collapse_triangulate = True
                modificadores.append(mod)

        if modificadores:
            depsgraph = bpy.context.evaluated_depsgraph_get()

            def medir(proporcion):
                for obj, mod in zip(copias, modificadores):
                    mod.ratio = proporcion
                    obj.update_tag()
                bpy.context.view_layer.update()
                total = 0
                for obj in copias:
                    evaluado = obj.evaluated_get(depsgraph)
                    malla = evaluado.to_mesh()
                    try:
                        cuenta = triangulos(malla)
                        # No aceptar que desaparezca una pieza del personaje.
                        if cuenta == 0:
                            return None
                        total += cuenta
                    finally:
                        evaluado.to_mesh_clear()
                return total

            # Buscar el mayor ratio medido que respete el presupuesto.
            bajo, alto = 0.0, 1.0
            mejor = None
            for _ in range(28):
                ratio = (bajo + alto) / 2
                total = medir(ratio)
                if total is None:
                    bajo = ratio
                elif total <= objetivo:
                    mejor = ratio
                    bajo = ratio
                else:
                    alto = ratio
            exigir(mejor is not None,
                   f"No se alcanza {objetivo} triangulos sin perder una pieza; aumente el objetivo.")
            medir(mejor)
            for obj, mod in zip(copias, modificadores):
                seleccionar([obj])
                exigir(bpy.ops.object.modifier_apply(modifier=mod.name) == {"FINISHED"},
                       f"No se pudo aplicar Decimate a {obj.name}.")

        # Recalcular orientacion y fijar caras planas tambien tras Decimate.
        for fuente, obj in zip(base, copias):
            bm = bmesh.new()
            try:
                bm.from_mesh(obj.data)
                bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
                bm.to_mesh(obj.data)
            finally:
                bm.free()
            for poligono in obj.data.polygons:
                poligono.use_smooth = False
            obj.data.update()
            exigir(tuple(c.name for c in fuente.data.uv_layers) == tuple(c.name for c in obj.data.uv_layers),
                   f"Decimate altero las capas UV de {obj.name}.")
            exigir(list(fuente.data.materials) == list(obj.data.materials), "Se alteraron los materiales.")
            exigir(triangulos(obj.data) > 0, f"Desaparecio una pieza: {obj.name}.")
        total = sum(triangulos(o.data) for o in copias)
        exigir(total <= objetivo or original <= objetivo, "El nivel supera su presupuesto.")
        return copias, total
    except Exception:
        eliminar(copias)
        raise


def eliminar(objetos):
    for obj in objetos:
        malla = obj.data
        bpy.data.objects.remove(obj, do_unlink=True)
        if malla.users == 0:
            bpy.data.meshes.remove(malla)


def verificar_glb(ruta, esperados, requiere_textura):
    # Leer el contenedor escrito para comprobar triangulos y recursos incluidos.
    with ruta.open("rb") as archivo:
        cabecera = archivo.read(12)
        exigir(len(cabecera) == 12, "GLB incompleto.")
        magic, version, largo = struct.unpack("<4sII", cabecera)
        exigir(magic == b"glTF" and version == 2 and largo == ruta.stat().st_size, "Cabecera GLB invalida.")
        documento = None
        binario = 0
        while archivo.tell() < largo:
            bloque = archivo.read(8)
            exigir(len(bloque) == 8, "Bloque GLB truncado.")
            longitud, tipo = struct.unpack("<II", bloque)
            contenido = archivo.read(longitud)
            exigir(len(contenido) == longitud, "Datos GLB truncados.")
            if tipo == 0x4E4F534A:
                documento = json.loads(contenido)
            elif tipo == 0x004E4942:
                binario += longitud
    exigir(documento is not None and binario > 0, "Faltan JSON o datos binarios en GLB.")
    exigir(not any("uri" in b for b in documento.get("buffers", [])), "GLB con buffer externo.")
    imagenes = documento.get("images", [])
    exigir(not requiere_textura or bool(imagenes), "La exportacion perdio la textura.")
    exigir(all("bufferView" in i and "uri" not in i for i in imagenes), "Textura no incrustada.")
    cuenta = 0
    for nodo in documento.get("nodes", []):
        if "mesh" not in nodo:
            continue
        for primitiva in documento["meshes"][nodo["mesh"]]["primitives"]:
            exigir(primitiva.get("mode", 4) == 4, "La exportacion contiene geometria no triangular.")
            accessor = primitiva.get("indices", primitiva["attributes"]["POSITION"])
            cantidad = documento["accessors"][accessor]["count"]
            exigir(cantidad % 3 == 0, "Primitiva triangular incompleta.")
            cuenta += cantidad // 3
    exigir(cuenta == esperados, f"GLB: {cuenta} triangulos; se esperaban {esperados}.")
    exigir(not documento.get("skins") and not documento.get("animations"), "GLB estatico inesperadamente animado.")
    return len(imagenes)


def main():
    args = argumentos()
    # instalado: Blender 5.3 (2026-11-12); se escribio contra la API 5.2, que la 5.3 conserva
    exigir(bpy.app.version[:2] >= (5, 2), "Se requiere Blender 5.2 o posterior; version detectada: " + bpy.app.version_string)
    entrada = args.entrada.resolve()
    prefijo = args.salida.resolve()
    raiz = Path(__file__).resolve().parent
    exigir(prefijo.is_relative_to(raiz), "El prefijo de salida debe estar dentro de " + str(raiz))
    exigir(entrada.is_file() and entrada.suffix.lower() == ".glb", "--entrada debe ser un GLB existente.")
    destinos = [prefijo.with_name(f"{prefijo.name}_{n}.glb") for n in args.objetivos]
    exigir(all(d != entrada and not d.exists() for d in destinos), "Una salida ya existe o coincide con la entrada.")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    escena = bpy.context.scene
    escena.unit_settings.system = "METRIC"
    escena.unit_settings.scale_length = 1.0
    resultado = bpy.ops.import_scene.gltf(**opciones_operador(
        bpy.ops.import_scene.gltf, {"filepath": str(entrada), "import_pack_images": True}))
    exigir(resultado == {"FINISHED"}, "No se pudo importar el GLB.")
    objetos = list(escena.objects)
    huesos = sum(len(o.data.bones) for o in objetos if o.type == "ARMATURE")
    exigir(not any(o.type == "ARMATURE" for o in objetos) and huesos == 0,
           f"Entrada con {huesos} huesos: esta herramienta requiere un personaje estatico.")
    exigir(len(bpy.data.actions) == 0 and not any(o.animation_data for o in objetos),
           "Entrada con acciones o animacion; no se pueden conservar con este flujo estatico.")
    base = [o for o in objetos if o.type == "MESH"]
    exigir(base, "El GLB no contiene mallas.")
    exigir(all(o.type in {"MESH", "EMPTY"} for o in objetos), "Entrada con objetos no admitidos.")
    for obj in base:
        exigir(not obj.data.shape_keys and not obj.modifiers and not obj.constraints,
               f"{obj.name} tiene shape keys, modificadores o restricciones no admitidos.")
        exigir(not obj.data.animation_data, f"Animacion de malla en {obj.name}.")
        exigir(triangulos(obj.data) > 0, f"Malla vacia: {obj.name}.")
    # Capturar todas las matrices antes de quitar padres; aplicar al dato de malla.
    matrices = [o.matrix_world.copy() for o in base]
    for obj, matriz in zip(base, matrices):
        exigir(abs(matriz.determinant()) > 1e-12, f"Transformacion singular en {obj.name}.")
        obj.data = obj.data.copy()
        obj.parent = None
        obj.matrix_world = Matrix.Identity(4)
        obj.data.transform(matriz)
    bpy.context.view_layer.update()
    altura = caja(base)["tamano_m"][2]
    exigir(altura > 1e-9, "La altura Z del personaje es nula.")
    if args.altura is not None:
        escala = Matrix.Scale(args.altura / altura, 4)
        for obj in base:
            obj.data.transform(escala)
    for obj in base:
        soldados, abiertos, no_manifold = limpiar(obj.data, args.umbral_soldar)
        print(f"LIMPIEZA {obj.name}: soldados={soldados}, bordes_abiertos={abiertos}, no_manifold={no_manifold}", flush=True)
        if no_manifold:
            print("AVISO: la orientacion exterior no es inequivoca en superficies abiertas/no manifold.", flush=True)
    imagenes = set()
    for obj in base:
        tiene_textura = False
        for material in obj.data.materials:
            if material and material.use_nodes:
                exigir(not material.node_tree.animation_data, "Material animado no admitido.")
                for nodo in material.node_tree.nodes:
                    if nodo.type == "TEX_IMAGE" and nodo.image:
                        # sin ventana, una imagen empaquetada del GLB no se carga hasta usarla:
                        # basta con que este empaquetada o tenga tamano (probado en Blender 5.3)
                        exigir(nodo.image.packed_file is not None or nodo.image.size[0] > 0,
                               f"Textura sin datos: {nodo.image.name}.")
                        imagenes.add(nodo.image)
                        tiene_textura = True
        if tiene_textura:
            exigir(bool(obj.data.uv_layers), f"Malla texturizada sin UV: {obj.name}.")
    exigir(imagenes, "No se encontro la textura original; se esperaba un GLB texturizado.")
    prefijo.parent.mkdir(parents=True, exist_ok=True)
    resumen = []
    escritos = []
    try:
        # Preparar y verificar todos los niveles antes de publicar sus nombres finales.
        with tempfile.TemporaryDirectory(prefix=".limpiar_", dir=prefijo.parent) as temporal:
            pendientes = []
            for objetivo, destino in zip(args.objetivos, destinos):
                nivel, total = crear_nivel(base, objetivo)
                try:
                    seleccionar(nivel)
                    ruta = Path(temporal) / destino.name
                    opciones = {"filepath": str(ruta), "export_format": "GLB", "use_selection": True,
                                "export_yup": True, "export_materials": "EXPORT", "export_image_format": "AUTO",
                                "export_texcoords": True, "export_normals": True, "export_animations": False,
                                "export_skins": False, "export_morph": False, "export_apply": False}
                    exigir(bpy.ops.export_scene.gltf(**opciones_operador(bpy.ops.export_scene.gltf, opciones)) == {"FINISHED"},
                           f"No se pudo exportar {destino.name}.")
                    incluidas = verificar_glb(ruta, total, True)
                    resumen.append({"objetivo": objetivo, "triangulos": total, "caja_blender_z_arriba": caja(nivel),
                                    "huesos": 0, "acciones": 0, "imagenes_incluidas": incluidas, "archivo": str(destino)})
                    pendientes.append((ruta, destino))
                    print(f"NIVEL VERIFICADO {objetivo}: {total} triangulos", flush=True)
                finally:
                    eliminar(nivel)
            for ruta, destino in pendientes:
                # rename en Windows falla si alguien creo el destino mientras tanto.
                exigir(not destino.exists(), f"La salida aparecio durante el proceso: {destino}")
                ruta.rename(destino)
                escritos.append(destino)
    except Exception:
        for ruta in escritos:
            ruta.unlink(missing_ok=True)
        raise
    print("RESUMEN_JSON=" + json.dumps({"entrada": str(entrada), "unidades": "metros",
          "version_blender": bpy.app.version_string, "frente": "conservado sin reorientar",
          "niveles": resumen, "archivos_escritos": [str(p) for p in escritos]}, ensure_ascii=True), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR limpiar_personaje: {error}", file=sys.stderr, flush=True)
        traceback.print_exc()
        sys.exit(1)
