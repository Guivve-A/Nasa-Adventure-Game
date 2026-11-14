"""Reune FBX de un MISMO personaje Mixamo en un GLB con varias animaciones.

Uso (PowerShell, desde esta carpeta):
  & 'C:/ruta/blender.exe' -b --factory-startup --python-exit-code 1 `
    --python ./fbx_mixamo_a_glb.py -- --malla ./descargas/reposo.fbx `
    --animaciones './descargas/caminar.fbx,./descargas/correr.fbx' `
    --nombres reposo,caminar,correr --salida ./salidas/PER-01.glb

--nombres sigue este orden: accion de --malla (si existe), despues una por
FBX de --animaciones. Si --malla es una T-pose sin accion, NO incluir reposo.
Para solo un FBX, omitir --animaciones. No se sintetiza una animacion reposo.
Las rutas de una lista no pueden contener comas. Los FBX deben proceder del
mismo rig y usar la misma tasa de fotogramas. Conserva el movimiento de raiz.
Salidas limitadas a esta carpeta y sus subcarpetas. No hace retargeting.
Codigo preparado para API 5.2 con acciones por slots; SIN PROBAR EN BLENDER.
"""

import argparse
import json
import math
import os
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import traceback

import bpy
from mathutils import Matrix


ROOT = Path(__file__).resolve().parent


def lista(valor):
    if not valor.strip():
        return []
    elementos = [p.strip() for p in valor.split(',')]
    if not all(elementos):
        raise ValueError('Hay un elemento vacio en una lista separada por comas.')
    return elementos


def argumentos():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--malla', required=True)
    parser.add_argument('--animaciones', default='')
    parser.add_argument('--nombres', required=True)
    parser.add_argument('--salida', required=True)
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    args = parser.parse_args(argv)
    fuentes = [Path(p).expanduser().resolve(strict=True)
               for p in [args.malla] + lista(args.animaciones)]
    if any(p.suffix.lower() != '.fbx' for p in fuentes):
        raise ValueError('Todas las entradas deben ser .fbx.')
    if len(set(fuentes)) != len(fuentes):
        raise ValueError('Se ha repetido un FBX de entrada.')
    nombres = lista(args.nombres)
    if not nombres or len(set(nombres)) != len(nombres):
        raise ValueError('--nombres debe contener nombres no vacios y distintos.')
    salida = Path(args.salida).expanduser().resolve()
    if salida.suffix.lower() != '.glb' or not salida.is_relative_to(ROOT):
        raise ValueError(f'La salida debe ser .glb y quedar dentro de {ROOT}.')
    salida.parent.mkdir(parents=True, exist_ok=True)
    return fuentes, nombres, salida


def operador(op, **kwargs):
    faltantes = set(kwargs) - set(op.get_rna_type().properties.keys())
    if faltantes:
        raise RuntimeError(f'API incompatible en {op.idname()}: {sorted(faltantes)}')
    if 'FINISHED' not in op(**kwargs):
        raise RuntimeError(f'Operacion incompleta: {op.idname()}')


def fps():
    escena = bpy.context.scene
    return escena.render.fps / escena.render.fps_base


def importar(ruta, carpeta_importacion):
    # Aisla posibles archivos auxiliares del importador junto al FBX temporal.
    # Nunca se importa directamente desde la carpeta original de solo lectura.
    carpeta = Path(tempfile.mkdtemp(prefix='entrada_', dir=carpeta_importacion))
    copia = carpeta / ruta.name
    shutil.copyfile(ruta, copia)
    extensiones = {'.png', '.jpg', '.jpeg', '.tga', '.bmp', '.tif', '.tiff', '.webp'}
    for vecino in ruta.parent.iterdir():
        if vecino.is_file() and vecino.suffix.lower() in extensiones:
            shutil.copyfile(vecino, carpeta / vecino.name)
        elif vecino.is_dir() and vecino.name.lower() == ruta.stem.lower() + '.fbm':
            shutil.copytree(vecino, carpeta / vecino.name)
    antes = set(bpy.data.objects)
    acciones_antes = set(bpy.data.actions)
    # La conversion de ejes y centimetros FBX se deja al importador.
    # Mantener orientacion de huesos original permite compartir las acciones.
    operador(bpy.ops.import_scene.fbx, filepath=str(copia), global_scale=1.0,
             use_anim=True, anim_offset=0.0, automatic_bone_orientation=False,
             ignore_leaf_bones=False, use_prepost_rot=True)
    nuevos = set(bpy.data.objects) - antes
    rigs = [o for o in nuevos if o.type == 'ARMATURE']
    if len(rigs) != 1:
        raise ValueError(f'{ruta.name}: se esperaba un armature; se encontraron {len(rigs)}.')
    rig = rigs[0]
    if not rig.data.bones:
        raise ValueError(f'{ruta.name}: esqueleto sin huesos.')
    return nuevos, rig, set(bpy.data.actions) - acciones_antes


def curvas_slot(accion, slot):
    # API moderna: no usar Action.fcurves ni Action.id_root.
    curvas = []
    for capa in accion.layers:
        for tira in capa.strips:
            if tira.type != 'KEYFRAME':
                raise ValueError(f'{accion.name}: tipo de tira de accion no soportado: {tira.type}')
            for bolsa in tira.channelbags:
                if bolsa.slot_handle == slot.handle:
                    curvas.extend(bolsa.fcurves)
    return curvas


def obtener_accion(rig, ruta):
    datos = rig.animation_data
    if not datos or not datos.action:
        return None
    accion = datos.action
    slot = datos.action_slot
    if slot is None:
        raise ValueError(f'{ruta.name}: accion sin slot; se requiere API moderna de Blender 5.2.')
    if len(accion.slots) != 1:
        raise ValueError(f'{ruta.name}: se esperaba una accion de un solo objeto/slot.')
    curvas = curvas_slot(accion, slot)
    if not curvas or not any(c.data_path.startswith('pose.bones[') for c in curvas):
        raise ValueError(f'{ruta.name}: la accion no tiene curvas de huesos.')
    fotogramas = [p.co.x for c in curvas for p in c.keyframe_points]
    if not fotogramas or not all(math.isfinite(f) for f in fotogramas):
        raise ValueError(f'{ruta.name}: fotogramas vacios o no finitos.')
    inicio, fin = min(fotogramas), max(fotogramas)
    if fin - inicio < 1e-5:
        raise ValueError(f'{ruta.name}: accion de un solo instante; descargue una animacion real.')
    for curva in curvas:
        try:
            rig.path_resolve(curva.data_path)
        except (ValueError, KeyError) as exc:
            raise ValueError(f'{ruta.name}: curva sin destino: {curva.data_path}') from exc
    return accion, slot, inicio, fin


def firma_reposo(rig):
    # Debe llamarse despues de desvincular la accion para evitar poses animadas.
    bpy.context.view_layer.update()
    return {h.name: (h.parent.name if h.parent else None, h.matrix_local.copy(), h.length)
            for h in rig.data.bones}, rig.matrix_world.copy()


def comparar_rigs(base, otro, archivo):
    huesos_a, mundo_a = base
    huesos_b, mundo_b = otro
    if set(huesos_a) != set(huesos_b):
        raise ValueError(f'{archivo}: huesos distintos. Faltan={sorted(set(huesos_a)-set(huesos_b))}; '
                         f'sobran={sorted(set(huesos_b)-set(huesos_a))}. '
                         'Descargue todas las animaciones del mismo personaje Mixamo.')
    def cerca(a, b):
        return all(abs(x - y) <= 1e-4 * max(1.0, abs(x), abs(y))
                   for fila_a, fila_b in zip(a, b) for x, y in zip(fila_a, fila_b))
    if not cerca(mundo_a, mundo_b):
        raise ValueError(f'{archivo}: transformacion global/escala del armature distinta; '
                         'no es seguro transferir la accion sin retargeting.')
    for nombre, (padre, matriz, largo) in huesos_a.items():
        padre_b, matriz_b, largo_b = huesos_b[nombre]
        if padre != padre_b or not cerca(matriz, matriz_b) or abs(largo - largo_b) > 1e-4 * max(1, largo):
            raise ValueError(f'{archivo}: jerarquia o pose de reposo incompatible en {nombre}.')


def copiar_accion(info, destino):
    accion, slot, inicio, fin = info
    indice = list(accion.slots).index(slot)
    copia = accion.copy()
    destino.animation_data_create()
    destino.animation_data.action = copia
    destino.animation_data.action_slot = copia.slots[indice]
    # Comprueba que las rutas siguen siendo validas en el esqueleto principal.
    for curva in curvas_slot(copia, copia.slots[indice]):
        destino.path_resolve(curva.data_path)
    destino.animation_data.action = None
    return copia, copia.slots[indice], inicio, fin


def validar_materiales(mallas):
    imagenes = set()
    for objeto in mallas:
        if not objeto.data.uv_layers:
            raise ValueError(f'{objeto.name}: falta UV.')
        materiales = [m for m in objeto.data.materials if m]
        if not materiales:
            raise ValueError(f'{objeto.name}: falta material.')
        for material in materiales:
            if not material.use_nodes:
                raise ValueError(f'{material.name}: material sin nodos.')
            principales = [n for n in material.node_tree.nodes if n.type == 'BSDF_PRINCIPLED']
            if not principales:
                raise ValueError(f'{material.name}: falta Principled BSDF exportable.')
            for nodo in material.node_tree.nodes:
                if nodo.type == 'TEX_IMAGE' and nodo.image:
                    imagen = nodo.image
                    if not imagen.has_data or imagen.size[0] == 0:
                        raise ValueError(f'Textura ausente: {imagen.name}. '
                                         'Incluya la carpeta .fbm o la textura original junto al FBX.')
                    imagenes.add(imagen)
    if not imagenes:
        raise ValueError('No se encontro textura. Mixamo debe devolver el material y sus imagenes.')
    return len(imagenes)


def verificar_glb(ruta, nombres, huesos, triangulos):
    with ruta.open('rb') as f:
        if f.read(4) != b'glTF':
            raise ValueError('La salida no es GLB.')
        version, longitud = struct.unpack('<II', f.read(8))
        if version != 2 or longitud != ruta.stat().st_size:
            raise ValueError('Cabecera GLB invalida.')
        tamano, tipo = struct.unpack('<II', f.read(8))
        if tipo != 0x4E4F534A:
            raise ValueError('Falta el bloque JSON GLB.')
        doc = json.loads(f.read(tamano))
    animaciones = doc.get('animations', [])
    if sorted(a.get('name', '') for a in animaciones) != sorted(nombres):
        raise ValueError(f'Animaciones exportadas distintas: {[a.get("name") for a in animaciones]} '
                         f'frente a {nombres}.')
    pieles = doc.get('skins', [])
    # Varias mallas pueden generar varias pieles con los mismos joints.
    conjuntos = {frozenset(p['joints']) for p in pieles}
    if len(conjuntos) != 1 or len(next(iter(conjuntos))) != huesos:
        raise ValueError('El GLB no contiene el conjunto completo de huesos esperado.')
    if any('uri' in b for b in doc.get('buffers', [])):
        raise ValueError('El GLB referencia un buffer externo.')
    imagenes = doc.get('images', [])
    if not imagenes or any('bufferView' not in i or 'uri' in i for i in imagenes):
        raise ValueError('Faltan imagenes incrustadas en el GLB.')
    cuenta = 0
    for malla in doc.get('meshes', []):
        for primitiva in malla['primitives']:
            if primitiva.get('mode', 4) != 4:
                raise ValueError('La salida contiene primitivas que no son triangulos.')
            acceso = primitiva.get('indices', primitiva['attributes']['POSITION'])
            cuenta += doc['accessors'][acceso]['count'] // 3
            material = doc.get('materials', [])[primitiva['material']] if 'material' in primitiva else {}
            if 'baseColorTexture' not in material.get('pbrMetallicRoughness', {}):
                raise ValueError('Una primitiva no conserva la textura de color base.')
    if cuenta != triangulos:
        raise ValueError(f'Triangulos distintos tras exportar: {cuenta}, esperados {triangulos}.')
    duraciones = {}
    for animacion in animaciones:
        if not animacion.get('channels') or not animacion.get('samplers'):
            raise ValueError(f'Animacion vacia: {animacion.get("name")}')
        tiempos = [doc['accessors'][s['input']] for s in animacion['samplers']]
        inicio = min(t['min'][0] for t in tiempos)
        fin = max(t['max'][0] for t in tiempos)
        if fin <= inicio:
            raise ValueError(f'Animacion sin duracion: {animacion.get("name")}')
        duraciones[animacion['name']] = {'inicio_s': inicio, 'fin_s': fin, 'duracion_s': fin - inicio}
    return duraciones, len(imagenes)


def procesar(fuentes, nombres, salida, carpeta_importacion):
    print(f'Blender {bpy.app.version_string}; objetivo API 5.2; script SIN PROBAR EN BLENDER.')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    escena = bpy.context.scene
    escena.unit_settings.system = 'METRIC'
    escena.unit_settings.scale_length = 1.0
    objetos_base, principal, _ = importar(fuentes[0], carpeta_importacion)
    tasa = fps()
    mallas = [o for o in objetos_base if o.type == 'MESH']
    if not mallas:
        raise ValueError('--malla no contiene malla; descargue ese FBX con skin.')
    for malla in mallas:
        mods = [m for m in malla.modifiers if m.type == 'ARMATURE' and m.object == principal]
        if not mods or not malla.vertex_groups:
            raise ValueError(f'{malla.name}: no esta vinculada al armature principal mediante pesos.')
        if malla.animation_data and malla.animation_data.action:
            raise ValueError(f'{malla.name}: animacion de objeto adicional no soportada.')
        for poligono in malla.data.polygons:
            poligono.use_smooth = False
    texturas = validar_materiales(mallas)
    info_base = obtener_accion(principal, fuentes[0])
    principal.animation_data_clear()
    for hueso in principal.pose.bones:
        hueso.matrix_basis = Matrix.Identity(4)
    firma = firma_reposo(principal)
    acciones = [copiar_accion(info_base, principal)] if info_base else []
    for fuente in fuentes[1:]:
        objetos, rig, acciones_importadas = importar(fuente, carpeta_importacion)
        if any(o.type == 'MESH' for o in objetos):
            raise ValueError(f'{fuente.name}: contiene malla; descargue las adicionales Without Skin.')
        if abs(fps() - tasa) > 1e-6:
            raise ValueError(f'{fuente.name}: FPS {fps()} frente a {tasa}. '
                             'Descargue todas las animaciones a los mismos FPS.')
        info = obtener_accion(rig, fuente)
        if info is None:
            raise ValueError(f'{fuente.name}: no contiene accion en el armature.')
        rig.animation_data_clear()
        comparar_rigs(firma, firma_reposo(rig), fuente.name)
        acciones.append(copiar_accion(info, principal))
        for objeto in objetos:
            bpy.data.objects.remove(objeto, do_unlink=True)
        for accion in acciones_importadas:
            if accion.users == 0:
                bpy.data.actions.remove(accion)
    if len(nombres) != len(acciones):
        raise ValueError(f'Hay {len(acciones)} acciones y {len(nombres)} nombres. '
                         f'El FBX de malla {"SI" if info_base else "NO"} aporta accion; '
                         'despues va una por cada FBX adicional.')
    if not acciones:
        raise ValueError('No hay animaciones para exportar.')
    # Libera los nombres originales para impedir sufijos .001 involuntarios.
    for i, accion in enumerate(bpy.data.actions):
        accion.name = f'__mixamo_temporal_{i:05d}'
    principal.name = 'Personaje'
    principal.animation_data_create()
    resumen = []
    for nombre, (accion, slot, inicio, fin) in zip(nombres, acciones):
        accion.name = nombre
        accion.use_fake_user = True
        pista = principal.animation_data.nla_tracks.new()
        pista.name = nombre
        # Una pista por clip; NLA_TRACKS exporta cada pista por separado.
        tira = pista.strips.new(nombre, 0, accion)
        tira.action_slot = slot
        tira.action_frame_start = inicio
        tira.action_frame_end = fin
        tira.frame_start = 0.0
        tira.frame_end = fin - inicio
        tira.blend_type = 'REPLACE'
        tira.extrapolation = 'NOTHING'
        resumen.append({'nombre': nombre, 'fotogramas_fuente': [inicio, fin],
                        'duracion_fuente_s': (fin - inicio) / tasa})
    principal.animation_data.action = None
    principal.data.pose_position = 'POSE'
    escena.frame_start = 0
    escena.frame_end = math.ceil(max(fin - inicio for _, _, inicio, fin in acciones))
    escena.frame_set(0)
    bpy.ops.object.select_all(action='DESELECT')
    for objeto in objetos_base:
        if objeto.type in {'MESH', 'ARMATURE', 'EMPTY'}:
            objeto.select_set(True)
    bpy.context.view_layer.objects.active = principal
    triangulos = 0
    for malla in mallas:
        malla.data.calc_loop_triangles()
        triangulos += len(malla.data.loop_triangles)
    if not triangulos:
        raise ValueError('La malla no tiene triangulos.')
    with tempfile.TemporaryDirectory(prefix='.mixamo_', dir=salida.parent) as temporal:
        provisional = Path(temporal) / salida.name
        operador(bpy.ops.export_scene.gltf, filepath=str(provisional), export_format='GLB',
                 use_selection=True, export_yup=True, export_texcoords=True,
                 export_normals=True, export_materials='EXPORT', export_image_format='AUTO',
                 export_animations=True, export_animation_mode='NLA_TRACKS',
                 export_frame_range=False, export_frame_step=1, export_force_sampling=True,
                 export_skins=True, export_def_bones=False, export_all_influences=True)
        duraciones, imagenes_glb = verificar_glb(provisional, nombres, len(principal.data.bones), triangulos)
        for clip in resumen:
            exportado = duraciones[clip['nombre']]
            clip['exportado'] = exportado
            if abs(exportado['duracion_s'] - clip['duracion_fuente_s']) > 1.1 / tasa:
                raise ValueError(f'Duracion exportada distinta en {clip["nombre"]}: {exportado}')
        os.replace(provisional, salida)
    print('RESUMEN ' + json.dumps({
        'blender': bpy.app.version_string, 'triangulos': triangulos,
        'armatures': 1, 'huesos': len(principal.data.bones),
        'nombres_huesos': sorted(h.name for h in principal.data.bones),
        'fps': tasa, 'acciones': resumen, 'cantidad_acciones': len(resumen),
        'texturas_blender': texturas, 'imagenes_glb': imagenes_glb,
        'movimiento_raiz': 'conservado', 'unidades': 'metros',
        'archivos_escritos': [str(salida)], 'bytes': salida.stat().st_size,
    }, ensure_ascii=False, indent=2))


def main():
    fuentes, nombres, salida = argumentos()
    with tempfile.TemporaryDirectory(prefix='.mixamo_importacion_', dir=ROOT) as temporal:
        procesar(fuentes, nombres, salida, Path(temporal))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR fbx_mixamo_a_glb: {exc}', file=sys.stderr)
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)
